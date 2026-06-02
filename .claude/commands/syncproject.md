Save the current state of the project to GitHub.

Steps to follow exactly:

1. Read `bhuvanfitterpierce.py` in full and read `claude.md`. Compare them and update `claude.md` if any of the following have changed:
   - New or removed functions, classes, or notebook sections
   - Changes to fitting models, TI metric names, or the batch API
   - New required Drive files or data format changes
   - Any constraint or invariant the next Claude instance needs to know
   Keep the update minimal — only change what is actually out of date. Do not add generic advice.

2. Run `python convert_to_nb.py bhuvanfitterpierce.py bhuvanfitterpierce.ipynb` to regenerate the notebook from the .py source.

3. Run `git diff --stat HEAD` and `git status` to see what changed.

4. Based on the actual diff, write a concise commit message (1–2 sentences). Be specific — e.g. "Add MLE fallback to BFGS optimiser" not "Update code". Do not use generic messages like "WIP" or "Update".

5. Stage the files: `git add bhuvanfitterpierce.py bhuvanfitterpierce.ipynb claude.md convert_to_nb.py nb_to_py.py .gitignore .claude/`

6. Commit with the message you composed.

7. Push: `git push -u origin master` (use `-u` only if the upstream is not set yet; otherwise just `git push`).

8. Report the commit hash and confirm claude.md was reviewed (and whether it was updated).
