from __future__ import annotations

import importlib.util
import json
import os
import shlex
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path
from unittest import mock

SKILL_ROOT = Path(__file__).resolve().parents[1]
TOOL = SKILL_ROOT / "scripts" / "modern_python.py"
SPEC = importlib.util.spec_from_file_location("modern_python_tool", TOOL)
assert SPEC and SPEC.loader
modern_python = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = modern_python
SPEC.loader.exec_module(modern_python)

DEFAULT_TARGET_SOURCE = "Ruff default (no project configuration found)"

# A fake Ruff driven through MODERN_PYTHON_RUFF_COMMAND. Real Ruff is never run. Knobs, all
# environment variables: FAKE_RUFF_LOG (append every argv as a JSON line), FAKE_RUFF_VERSION
# (what --version reports, default 9.8.7), FAKE_SETTINGS_PATH (print a "Settings path" line),
# FAKE_NO_METADATA (make `rule --all` fail), FAKE_CHECK_DIAGNOSTICS (make `check` report one
# finding), FAKE_RUFF_CURLY (wrap "PEP 585" in U+201C/U+201D curly quotes in the UP006 text).
# `rule --all` is written as raw UTF-8 bytes on purpose, so the tool's decoding is exercised;
# the UP006 text carries a U+2192 arrow that cp1252 cannot encode, and U+201D's UTF-8 bytes
# include 0x9D, which cp1252 cannot decode at all.
FAKE_RUFF = r"""
import json
import os
import sys
from pathlib import Path

args = sys.argv[1:]
log = os.environ.get("FAKE_RUFF_LOG")
if log:
    with open(log, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(args) + "\n")
rules = [
    {
        "name": "non-pep585-annotation",
        "code": "UP006",
        "summary": "Use modern generics → PEP 585",
        "explanation": "## What it does\nChecks old generics → use PEP 585.\n\n## Example\n```python\nfrom typing import List\nx: List[int]\n```\n\nUse instead:\n```python\nx: list[int]\n```",
        "preview": False,
        "status": {"Stable": {"since": "0.1.0"}},
    },
    {
        "name": "non-pep604-annotation-optional",
        "code": "UP045",
        "summary": "Use PEP 604",
        "explanation": "## What it does\nChecks Optional annotations.\n\nWith __future__ annotations this applies earlier.\n\n## Example\n```python\nfrom typing import Optional\nx: Optional[int]\n```\n\nUse instead:\n```python\nx: int | None\n```",
        "preview": False,
        "status": {"Stable": {"since": "0.1.0"}},
    },
    {
        "name": "removed-rule",
        "code": "UP038",
        "summary": "Removed",
        "explanation": "## Removed\nDo not use.",
        "preview": False,
        "status": {"Removed": {"since": "0.2.0"}},
    },
    {
        "name": "preview-rule",
        "code": "UP051",
        "summary": "Preview",
        "explanation": "## What it does\nChecks preview syntax.\n\n## Example\n```python\npreview()\n```",
        "preview": True,
        "status": {"Preview": {"since": "0.3.0"}},
    },
    {
        "name": "print-empty-string",
        "code": "FURB105",
        "summary": "Avoid empty print args",
        "explanation": "## What it does\nChecks empty print arguments.\n\n## Example\n```python\nprint(\"\")\n```\n\nUse instead:\n```python\nprint()\n```",
        "preview": False,
        "status": {"Stable": {"since": "0.1.0"}},
    },
]
if os.environ.get("FAKE_RUFF_CURLY"):
    rules[0]["explanation"] = rules[0]["explanation"].replace(
        "use PEP 585.", "use “PEP 585”."
    )

if args == ["--version"]:
    print("ruff " + os.environ.get("FAKE_RUFF_VERSION", "9.8.7"))
elif args[:2] == ["check", "--show-settings"]:
    settings_path = os.environ.get("FAKE_SETTINGS_PATH")
    if settings_path:
        print('Settings path: "' + settings_path + '"')
    print("linter.unresolved_target_version = 3.12")
    print("linter.per_file_target_version = {}")
    print("linter.preview = disabled")
    print("linter.explicit_preview_rules = false")
    print("linter.rules.enabled = [")
    for code in ("UP006", "UP045", "FURB105", "SIM101", "C400", "PIE790", "PTH100", "FLY002", "PERF101", "F401"):
        print(f"\tfake-rule ({code}),")
    print("]")
    print("linter.per_file_ignores = {}")
elif args[:3] == ["rule", "--all", "--output-format"] and os.environ.get("FAKE_NO_METADATA"):
    print("unsupported", file=sys.stderr)
    raise SystemExit(2)
elif args[:3] == ["rule", "--all", "--output-format"]:
    sys.stdout.buffer.write(json.dumps(rules, ensure_ascii=False).encode("utf-8"))
elif args and args[0] == "rule":
    rule = next((rule for rule in rules if rule["code"] == args[1]), None)
    print(json.dumps(rule or {"code": args[1], "summary": "details"}))
elif args and args[0] == "check" and "--isolated" in args:
    root = Path(args[1])
    target = args[args.index("--target-version") + 1]
    diagnostics = []
    for path in root.rglob("*.py"):
        code = path.parent.name
        contents = path.read_text(encoding="utf-8")
        future = "from __future__ import annotations" in contents
        applies = (
            code == "FURB105"
            or code == "UP006" and (target != "py38" or future)
            or code == "UP045" and (target not in {"py38", "py39"} or future)
            or code == "UP051" and "--preview" in args
        )
        if applies:
            diagnostics.append({"code": code, "filename": str(path)})
    print(json.dumps(diagnostics))
elif args and args[0] == "check":
    if os.environ.get("FAKE_CHECK_DIAGNOSTICS"):
        print(
            json.dumps(
                [
                    {
                        "code": "UP006",
                        "message": "Use `list` instead of `List` for type annotation",
                        "filename": args[1],
                        "location": {"row": 1, "column": 4},
                        "end_location": {"row": 1, "column": 13},
                        "fix": None,
                        "noqa_row": 1,
                        "url": "https://docs.astral.sh/ruff/rules/non-pep585-annotation",
                    }
                ]
            )
        )
    else:
        print("[]")
else:
    print("unexpected arguments", file=sys.stderr)
    raise SystemExit(2)
"""


class ModernPythonToolTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.fake_ruff = self.directory / "fake_ruff.py"
        self.fake_ruff.write_text(textwrap.dedent(FAKE_RUFF), encoding="utf-8")
        self.log = self.directory / "fake_ruff_invocations.jsonl"

    def ruff_command(self) -> str:
        parts = [sys.executable, str(self.fake_ruff)]
        if os.name == "nt":
            # The tool splits the override with shlex in non-POSIX mode on Windows, which keeps
            # quote characters inside the tokens, so the value has to stay unquoted there.
            if any(" " in part for part in parts):
                self.skipTest("the Windows override cannot carry paths that contain spaces")
            return " ".join(parts)
        return shlex.join(parts)

    def run_tool(
        self, *arguments: str, isolate_path: bool = False
    ) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        environment["MODERN_PYTHON_RUFF_COMMAND"] = self.ruff_command()
        environment["FAKE_RUFF_LOG"] = str(self.log)
        if isolate_path:
            # Nothing but the override must be discoverable: no uvx, no pipx, no ruff.
            empty = self.directory / "empty-path"
            empty.mkdir(exist_ok=True)
            environment["PATH"] = str(empty)
        self.log.unlink(missing_ok=True)
        return subprocess.run(
            [sys.executable, str(TOOL), *arguments],
            cwd=self.directory,
            env=environment,
            check=False,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
        )

    def invocations(self) -> list[list[str]]:
        if not self.log.exists():
            return []
        lines = self.log.read_text(encoding="utf-8").splitlines()
        return [json.loads(line) for line in lines if line]

    def check_invocation(self) -> list[str]:
        checks = [
            argv
            for argv in self.invocations()
            if argv[:1] == ["check"] and "--show-settings" not in argv and "--isolated" not in argv
        ]
        self.assertEqual(len(checks), 1, checks)
        return checks[0]

    def test_probe_reports_target_and_runner(self) -> None:
        result = self.run_tool("probe", "--file", "example.py")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["target_python"], "3.12")
        self.assertEqual(payload["ruff_version"], "9.8.7")
        self.assertEqual(payload["runner"], "MODERN_PYTHON_RUFF_COMMAND")

    def test_check_uses_modern_profile_and_json_output(self) -> None:
        result = self.run_tool("check", "example.py")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), [])
        arguments = self.check_invocation()
        self.assertIn("UP,FURB,SIM,C4,PIE,PTH,FLY,PERF,F401", arguments)
        self.assertIn("--output-format", arguments)
        self.assertIn("--exit-zero", arguments)

    def test_check_and_fix_pass_no_cache(self) -> None:
        self.run_tool("check", "example.py")
        self.assertIn("--no-cache", self.check_invocation())
        self.run_tool("fix", "example.py")
        self.assertIn("--no-cache", self.check_invocation())

    def test_check_without_paths_is_a_usage_error(self) -> None:
        result = self.run_tool("check")
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertIn("required: paths", result.stderr)
        self.assertEqual(self.invocations(), [])

    def test_fix_without_paths_is_a_usage_error(self) -> None:
        result = self.run_tool("fix")
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertIn("required: paths", result.stderr)
        self.assertEqual(self.invocations(), [])

    def test_check_exits_1_with_findings_and_0_without(self) -> None:
        clean = self.run_tool("check", "example.py")
        self.assertEqual(clean.returncode, 0, clean.stderr)
        self.assertEqual(json.loads(clean.stdout), [])
        with mock.patch.dict(os.environ, {"FAKE_CHECK_DIAGNOSTICS": "1"}):
            findings = self.run_tool("check", "example.py")
            fixed = self.run_tool("fix", "example.py")
        self.assertEqual(findings.returncode, 1, findings.stderr)
        self.assertEqual([item["code"] for item in json.loads(findings.stdout)], ["UP006"])
        self.assertEqual(fixed.returncode, 1, fixed.stderr)
        self.assertEqual([item["code"] for item in json.loads(fixed.stdout)], ["UP006"])

    def test_list_returns_guidance_before_editing(self) -> None:
        result = self.run_tool("list", "--file", "example.py", "--format", "json")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["target_python"], "3.12")
        self.assertEqual(
            [rule["code"] for rule in payload["baseline"]],
            ["UP006", "UP045", "FURB105"],
        )
        self.assertNotIn("UP038", [rule["code"] for rule in payload["baseline"]])

    def test_future_annotations_rules_are_marked_conditional(self) -> None:
        result = self.run_tool(
            "list",
            "--file",
            "example.py",
            "--target-version",
            "py39",
            "--format",
            "json",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual([rule["code"] for rule in payload["conditional"]], ["UP045"])

    def test_missing_metadata_requires_update_or_explicit_stale_fallback(self) -> None:
        with mock.patch.dict(os.environ, {"FAKE_NO_METADATA": "1"}):
            blocked = self.run_tool("list", "--file", "example.py", "--format", "json")
            allowed = self.run_tool(
                "list",
                "--file",
                "example.py",
                "--allow-stale",
                "--format",
                "json",
            )
        self.assertEqual(blocked.returncode, 3)
        self.assertIn("Ask the user whether to update", blocked.stderr)
        self.assertEqual(allowed.returncode, 0, allowed.stderr)
        self.assertEqual(json.loads(allowed.stdout)["status"], "degraded")

    def test_no_config_target_is_reported_as_ruff_default_with_a_warning(self) -> None:
        probe = self.run_tool("probe", "--file", "example.py")
        self.assertEqual(probe.returncode, 0, probe.stderr)
        payload = json.loads(probe.stdout)
        self.assertEqual(payload["target_source"], DEFAULT_TARGET_SOURCE)
        warning = next((item for item in payload["warnings"] if "not declared" in item), None)
        self.assertIsNotNone(warning, payload["warnings"])
        self.assertIn("--target-version", warning)

        listed = self.run_tool("list", "--file", "example.py", "--format", "json")
        self.assertEqual(listed.returncode, 0, listed.stderr)
        payload = json.loads(listed.stdout)
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["target_source"], DEFAULT_TARGET_SOURCE)
        self.assertTrue(
            any("not declared" in item for item in payload["warnings"]), payload["warnings"]
        )

    def test_target_override_and_config_file_do_not_warn_about_the_default(self) -> None:
        override = self.run_tool(
            "list", "--file", "example.py", "--target-version", "py39", "--format", "json"
        )
        self.assertEqual(override.returncode, 0, override.stderr)
        payload = json.loads(override.stdout)
        self.assertEqual(payload["target_source"], "command-line override")
        self.assertFalse(
            any("not declared" in item for item in payload["warnings"]), payload["warnings"]
        )

        config = self.directory / "pyproject.toml"
        config.write_text('[tool.ruff]\ntarget-version = "py312"\n', encoding="utf-8")
        with mock.patch.dict(os.environ, {"FAKE_SETTINGS_PATH": str(config)}):
            probe = self.run_tool("probe", "--file", "example.py")
        self.assertEqual(probe.returncode, 0, probe.stderr)
        payload = json.loads(probe.stdout)
        self.assertEqual(payload["target_source"], "pyproject.toml")
        self.assertFalse(
            any("not declared" in item for item in payload["warnings"]), payload["warnings"]
        )

    def test_fix_is_safe_by_default(self) -> None:
        result = self.run_tool("fix", "example.py")
        self.assertEqual(result.returncode, 0, result.stderr)
        arguments = self.check_invocation()
        self.assertIn("--fix", arguments)
        self.assertNotIn("--unsafe-fixes", arguments)

    def test_unsafe_fixes_option_is_not_accepted(self) -> None:
        result = self.run_tool("fix", "--unsafe-fixes", "example.py")
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertIn("unrecognized arguments: --unsafe-fixes", result.stderr)
        self.assertEqual(self.invocations(), [])

    def test_explain_returns_only_requested_rules(self) -> None:
        result = self.run_tool("explain", "UP001", "FURB001")
        payload = json.loads(result.stdout)
        self.assertEqual([rule["code"] for rule in payload["rules"]], ["UP001", "FURB001"])

    def test_invalid_rule_code_fails(self) -> None:
        result = self.run_tool("explain", "not-a-code")
        self.assertEqual(result.returncode, 2)
        self.assertIn("invalid Ruff rule code", result.stderr)

    def test_explain_output_is_utf8(self) -> None:
        result = self.run_tool("explain", "UP006")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["rules"][0]["summary"], "Use modern generics → PEP 585")

    def test_ruff_output_is_decoded_as_utf8(self) -> None:
        with mock.patch.dict(os.environ, {"FAKE_RUFF_CURLY": "1"}):
            result = self.run_tool("list", "--file", "example.py", "--format", "json")
        self.assertEqual(result.returncode, 0, result.stderr)
        descriptions = {
            rule["code"]: rule["description"] for rule in json.loads(result.stdout)["baseline"]
        }
        self.assertEqual(
            descriptions["UP006"], "Checks old generics → use “PEP 585”."
        )

    def test_text_output_has_no_em_dash(self) -> None:
        result = self.run_tool("list", "--file", "example.py")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Ruff: 9.8.7, MODERN_PYTHON_RUFF_COMMAND [project]", result.stdout)
        self.assertNotIn(chr(0x2014), result.stdout)

    def test_pixi_project_uses_pixi_runner(self) -> None:
        (self.directory / "pixi.toml").write_text(
            '[workspace]\nname = "example"\n', encoding="utf-8"
        )
        with mock.patch.object(
            modern_python.shutil,
            "which",
            side_effect=lambda name: "/usr/bin/pixi" if name == "pixi" else None,
        ):
            candidates = modern_python.candidate_runners(self.directory)

        self.assertIn(
            modern_python.RunnerCandidate("Pixi environment", ("pixi", "run", "ruff"), "project"),
            candidates,
        )

    def test_pixi_pyproject_is_detected(self) -> None:
        (self.directory / "pyproject.toml").write_text(
            '[tool.pixi.workspace]\nname = "example"\n', encoding="utf-8"
        )
        self.assertTrue(modern_python.is_pixi_project(self.directory))

    def test_bundled_fallback_uses_the_pinned_constant(self) -> None:
        self.assertRegex(modern_python.PINNED_RUFF, r"^\d+\.\d+\.\d+$")
        with mock.patch.object(
            modern_python.shutil,
            "which",
            side_effect=lambda name: "/usr/bin/uvx" if name == "uvx" else None,
        ):
            candidates = modern_python.bundled_candidates()
        self.assertEqual(
            candidates,
            [
                modern_python.RunnerCandidate(
                    "bundled uvx fallback",
                    ("/usr/bin/uvx", "--from", f"ruff=={modern_python.PINNED_RUFF}", "ruff"),
                    "bundled",
                )
            ],
        )

    def test_bundled_candidates_have_no_pipx_runner(self) -> None:
        with mock.patch.object(
            modern_python.shutil, "which", side_effect=lambda name: f"/usr/bin/{name}"
        ):
            candidates = modern_python.bundled_candidates()
        self.assertEqual([candidate.label for candidate in candidates], ["bundled uvx fallback"])
        self.assertFalse(
            any("pipx" in part for candidate in candidates for part in candidate.argv)
        )

    def test_reference_comparison_is_gone(self) -> None:
        for name in ("discover_bundled_reference", "reference_differences", "parse_version"):
            self.assertFalse(hasattr(modern_python, name), name)

    def test_list_never_compares_with_a_bundled_reference(self) -> None:
        # A project Ruff older than the pin used to trigger a second, downloaded runner.
        with mock.patch.dict(os.environ, {"FAKE_RUFF_VERSION": "0.1.0"}):
            result = self.run_tool(
                "list", "--file", "example.py", "--format", "json", isolate_path=True
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["ruff_version"], "0.1.0")
        self.assertEqual(
            [rule["code"] for rule in payload["baseline"]], ["UP006", "UP045", "FURB105"]
        )
        self.assertFalse(
            any("bundled" in item or "compare" in item for item in payload["warnings"]),
            payload["warnings"],
        )

    def test_per_file_target_and_ignore_match_the_intended_file(self) -> None:
        settings = f'''linter.unresolved_target_version = 3.9
linter.per_file_target_version = {{
    absolute_matcher = "{(self.directory / "special.py").as_posix()}"
basename_matcher = "special.py"
negated = false
data = 3.12

}}
linter.per_file_ignores = {{
    absolute_matcher = "{(self.directory / "special.py").as_posix()}"
basename_matcher = "special.py"
negated = false
data = [
    non-pep604-annotation-optional (UP045),
]

}}
'''
        target, source = modern_python.target_from_settings(settings, self.directory / "special.py")
        self.assertEqual((target, source), ("3.12", "per-file-target-version"))
        self.assertEqual(
            modern_python.per_file_ignored_codes(settings, self.directory / "special.py"),
            frozenset({"UP045"}),
        )

    def test_legacy_removed_heading_is_excluded(self) -> None:
        rule = {"code": "UP038", "preview": False, "explanation": "## Removed\nRetired."}
        self.assertEqual(modern_python.rule_status(rule), "Removed")

    def test_explicit_preview_rules_only_allow_native_exact_selection(self) -> None:
        settings = modern_python.ResolvedSettings(
            intended_file=self.directory / "example.py",
            subject=self.directory,
            target_python="3.12",
            target_version="py312",
            target_source="test",
            preview=True,
            explicit_preview_rules=True,
            config_path=None,
            inferred_file_context=False,
        )
        settings_text = """linter.rules.enabled = [
    fake-rule (UP048),
]
linter.per_file_ignores = {}
"""
        policy = modern_python.resolve_policy(
            settings,
            settings_text,
            frozenset({"UP048", "UP051"}),
            preview_codes_requiring_native_selection=frozenset({"UP048", "UP051"}),
        )
        self.assertEqual(policy.allowed, frozenset({"UP048"}))

    def test_global_ignore_selectors_are_read_from_pyproject(self) -> None:
        config = self.directory / "pyproject.toml"
        config.write_text(
            '[tool.ruff.lint]\nignore = ["UP006"]\nextend-ignore = ["FURB"]\n',
            encoding="utf-8",
        )
        self.assertEqual(
            modern_python.resolved_ignore_selectors(config),
            frozenset({"UP006", "FURB"}),
        )


if __name__ == "__main__":
    unittest.main()
