#!/usr/bin/env python3
"""Convert a .ipynb notebook back to a Colab-style .py file.

Usage:
    python nb_to_py.py [input.ipynb] [output.py]

Defaults: bhuvanfitterpierce.ipynb -> bhuvanfitterpierce.py
"""

import json
import sys
from pathlib import Path


def nb_to_py(ipynb_path, py_path):
    nb = json.loads(Path(ipynb_path).read_text(encoding='utf-8'))
    cells = nb.get('cells', [])

    sections = []
    for cell in cells:
        src = ''.join(cell['source'])
        if not src.strip():
            continue

        if cell['cell_type'] == 'markdown':
            # Wrap in triple-quoted string (Colab .py style)
            # Escape any triple-quotes inside the markdown content
            src = src.replace('"""', r'\"\"\"')
            sections.append(f'"""{src}\n"""')
        else:
            sections.append(src)

    output = '\n\n'.join(sections) + '\n'
    Path(py_path).write_text(output, encoding='utf-8')
    print(f"Converted {ipynb_path} -> {py_path}  ({len(cells)} cells)")


if __name__ == '__main__':
    ipynb_path = sys.argv[1] if len(sys.argv) > 1 else 'bhuvanfitterpierce.ipynb'
    py_path    = sys.argv[2] if len(sys.argv) > 2 else ipynb_path.replace('.ipynb', '.py')
    nb_to_py(ipynb_path, py_path)
