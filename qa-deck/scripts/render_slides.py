"""Render every slide of a .pptx to a JPG image.

Usage:
    python render_slides.py <deck.pptx> <out_dir> [--dpi 150]

Outputs slide-01.jpg, slide-02.jpg, ... in <out_dir>.

Strategy:
  1. Convert .pptx -> .pdf via LibreOffice (soffice) headless mode.
  2. Convert .pdf -> per-page JPG via PyMuPDF (preferred) or pdftoppm.

Works on Windows, macOS, and Linux. Picks the right tools automatically.
Run with --help for options.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


def find_soffice() -> str | None:
    """Locate LibreOffice's soffice executable across platforms."""
    candidates = [
        "soffice",
        "libreoffice",
        r"C:\Program Files\LibreOffice\program\soffice.exe",
        r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
        "/Applications/LibreOffice.app/Contents/MacOS/soffice",
        "/usr/bin/soffice",
        "/usr/bin/libreoffice",
        "/usr/local/bin/soffice",
    ]
    for c in candidates:
        if shutil.which(c) or (os.path.isfile(c) and os.access(c, os.X_OK)):
            return c if shutil.which(c) else c
    return None


def pptx_to_pdf(pptx_path: Path, out_dir: Path) -> Path:
    soffice = find_soffice()
    if not soffice:
        raise RuntimeError(
            "LibreOffice (soffice) not found. Install LibreOffice or add soffice to PATH."
        )
    out_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        soffice,
        "--headless",
        "--convert-to",
        "pdf",
        "--outdir",
        str(out_dir),
        str(pptx_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"soffice failed (code {result.returncode})\nstdout: {result.stdout}\nstderr: {result.stderr}"
        )
    pdf_path = out_dir / (pptx_path.stem + ".pdf")
    if not pdf_path.exists():
        raise RuntimeError(f"Expected PDF not found at {pdf_path}")
    return pdf_path


def pdf_to_jpgs_pymupdf(pdf_path: Path, out_dir: Path, dpi: int) -> list[Path]:
    import fitz  # PyMuPDF
    doc = fitz.open(str(pdf_path))
    zoom = dpi / 72.0
    mat = fitz.Matrix(zoom, zoom)
    out_dir.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    for i, page in enumerate(doc, start=1):
        pix = page.get_pixmap(matrix=mat, alpha=False)
        out = out_dir / f"slide-{i:02d}.jpg"
        pix.save(str(out))
        paths.append(out)
    return paths


def pdf_to_jpgs_pdftoppm(pdf_path: Path, out_dir: Path, dpi: int) -> list[Path]:
    if not shutil.which("pdftoppm"):
        raise RuntimeError("pdftoppm not on PATH")
    out_dir.mkdir(parents=True, exist_ok=True)
    prefix = out_dir / "slide"
    cmd = ["pdftoppm", "-jpeg", "-r", str(dpi), str(pdf_path), str(prefix)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"pdftoppm failed (code {result.returncode})\nstdout: {result.stdout}\nstderr: {result.stderr}"
        )
    paths = sorted(out_dir.glob("slide-*.jpg"))
    return paths


def render(pptx_path: Path, out_dir: Path, dpi: int = 150) -> list[Path]:
    pdf_path = pptx_to_pdf(pptx_path, out_dir)
    # Prefer PyMuPDF; fall back to pdftoppm.
    try:
        import fitz  # noqa: F401
        return pdf_to_jpgs_pymupdf(pdf_path, out_dir, dpi)
    except ImportError:
        return pdf_to_jpgs_pdftoppm(pdf_path, out_dir, dpi)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("pptx", type=Path, help="Path to the .pptx file")
    p.add_argument("out_dir", type=Path, help="Directory to write slide-NN.jpg into")
    p.add_argument("--dpi", type=int, default=150, help="Render DPI (default 150)")
    args = p.parse_args()

    if not args.pptx.exists():
        print(f"error: {args.pptx} not found", file=sys.stderr)
        return 1
    if args.pptx.suffix.lower() != ".pptx":
        print(f"error: expected .pptx, got {args.pptx.suffix}", file=sys.stderr)
        return 1

    try:
        paths = render(args.pptx, args.out_dir, args.dpi)
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    print(f"Rendered {len(paths)} slides to {args.out_dir}")
    for p in paths:
        print(f"  {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
