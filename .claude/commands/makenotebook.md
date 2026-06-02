Convert `bhuvanfitterpierce.py` into `bhuvanfitterpierce.ipynb` using your built-in notebook editing tools. Do not use any external script.

## Steps

1. Read `bhuvanfitterpierce.py` in full.

2. Parse it into cells using this rule:
   - A **Markdown cell** is any block that is a standalone triple-quoted string literal at the top level (i.e. a line that is exactly `"""` or starts with `"""` and the string is not assigned to a variable and is not a docstring inside a function/class). These are the section header strings used as Colab markdown cells.
   - Everything else (imports, function definitions, class definitions, plain code, comments) is a **code cell**.
   - Consecutive code lines that are not separated by a markdown cell belong in the same code cell.

3. Write the notebook to `bhuvanfitterpierce.ipynb` using the NotebookEdit tool. The notebook should have:
   - `"nbformat": 4`, `"nbformat_minor": 5`
   - Kernel: `python3`
   - Each markdown block as a `markdown` cell
   - Each code block as a `code` cell with empty outputs

4. Confirm how many cells were written.
