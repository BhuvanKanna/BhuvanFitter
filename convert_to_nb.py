#!/usr/bin/env python3
"""Convert a Colab-generated .py file to .ipynb format.

Usage:
    python convert_to_nb.py [input.py] [output.ipynb]

Defaults: bhuvanfitterpierce.py -> bhuvanfitterpierce.ipynb
"""

import json
import re
import sys
from pathlib import Path


def py_to_cells(source):
    """Parse a Colab .py file into (cell_type, source) tuples."""
    lines = source.splitlines(True)
    cells = []
    code_buf = []

    def flush_code():
        block = ''.join(code_buf).strip('\n')
        if block.strip():
            cells.append(('code', block + '\n'))
        code_buf.clear()

    i = 0
    while i < len(lines):
        line = lines[i]

        # Standalone triple-quoted string at column 0 → Markdown cell
        if re.match(r'^"""', line) or re.match(r"^'''", line):
            flush_code()
            quote = '"""' if line.startswith('"""') else "'''"
            rest = line[3:]

            # Single-line: """content"""
            if quote in rest:
                inner = rest[:rest.index(quote)]
                cells.append(('markdown', inner.strip()))
                i += 1
                continue

            # Multi-line: collect until closing quotes
            md_lines = [rest]
            i += 1
            while i < len(lines):
                l = lines[i]
                if quote in l:
                    md_lines.append(l[:l.index(quote)])
                    i += 1
                    break
                md_lines.append(l)
                i += 1

            cells.append(('markdown', ''.join(md_lines).strip('\n')))
        else:
            code_buf.append(line)
            i += 1

    flush_code()
    return cells


def make_nb(cells):
    nb_cells = []
    for ctype, src in cells:
        if ctype == 'markdown':
            nb_cells.append({
                "cell_type": "markdown",
                "metadata": {},
                "source": src,
            })
        else:
            nb_cells.append({
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": src,
            })

    return {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.10.0"
            },
            "colab": {
                "provenance": []
            }
        },
        "cells": nb_cells,
    }


def convert(py_path, ipynb_path):
    src = Path(py_path).read_text(encoding='utf-8')
    cells = py_to_cells(src)
    nb = make_nb(cells)
    Path(ipynb_path).write_text(
        json.dumps(nb, indent=1, ensure_ascii=False) + '\n',
        encoding='utf-8'
    )
    print(f"Converted {py_path} -> {ipynb_path}  ({len(cells)} cells)")


if __name__ == '__main__':
    py_path    = sys.argv[1] if len(sys.argv) > 1 else 'bhuvanfitterpierce.py'
    ipynb_path = sys.argv[2] if len(sys.argv) > 2 else py_path.replace('.py', '.ipynb')
    convert(py_path, ipynb_path)
