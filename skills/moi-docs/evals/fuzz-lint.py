#!/usr/bin/env python3
"""fuzz-lint.py: mutate real pages at random and check that docs-page-lint.py never raises.

Usage (SKILLS is the folder that holds the moi-* skills, quoted because a path can hold spaces):
    python3 "$SKILLS/moi-docs/evals/fuzz-lint.py" <folder of pages> <empty scratch folder> [rounds]
Reads the .md, .mdx, .rst and _category_.json files under the first folder (a copy of a docs tree, for example
`git archive` output; never an env-named file or a file in an env-named folder). Writes only inside the scratch
folder, one mutated file at a time. Each round truncates, deletes, duplicates or inserts a fence, a quote, `---`,
a component or a secret-shaped filler (a known prefix plus filler) into a page, then runs the lint on it in this
process. The seed is fixed, so a run can be repeated. Prints one summary line.
Exit codes: 0 no exception in any round, 1 at least one exception (the page and the exception type are printed,
never page text), 2 bad input. Python 3 standard library only. No network.
"""
import contextlib
import importlib.util
import io
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LINT = os.path.join(HERE, "..", "scripts", "docs-page-lint.py")
SNIPS = ["---\n", "```\n", '"', "'", "<HowToSchema", "::", "\n\n", "\r\n", "[x](", "](", "{#", "$(", "\x00", "\ufeff", "# ", "## ",
         ":::", "<head>", "import X from '@site/src/components/X';\n", "sk-ant-" + "zq" * 10, chr(0x2014), "`", "|",
         ".. meta::\n   :description: "]


def main(argv):
    if len(argv) not in (3, 4) or not os.path.isdir(argv[1]) or not os.path.isdir(argv[2]) or os.listdir(argv[2]):
        print("usage: fuzz-lint.py <folder of pages> <empty scratch folder> [rounds]", file=sys.stderr)
        return 2
    try:
        rounds = int(argv[3]) if len(argv) == 4 else 1500
    except ValueError:
        print("fuzz-lint: rounds must be a whole number", file=sys.stderr)
        return 2
    spec = importlib.util.spec_from_file_location("lint", LINT)
    lint = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(lint)
    files = []
    for root, dirs, names in os.walk(argv[1]):
        dirs[:] = [d for d in dirs if not lint.env_name(d)]
        for n in names:
            p = os.path.join(root, n)
            if n.endswith((".md", ".mdx", ".rst", ".json")) and not lint.is_env_file(p) and os.path.getsize(p) < 60000:
                files.append(p)
    if not files:
        print("fuzz-lint: no page found under %s" % argv[1], file=sys.stderr)
        return 2
    random.seed(7)
    failures = 0
    for i in range(rounds):
        src = random.choice(files)
        with open(src, encoding="utf-8", errors="replace") as fh:
            text = fh.read()
        for _ in range(random.randint(1, 4)):
            if not text:
                break
            kind = random.choice(["truncate", "delete", "duplicate", "insert"])
            a = random.randrange(len(text))
            b = min(len(text), a + random.randint(1, 300))
            if kind == "truncate":
                text = text[:a]
            elif kind == "delete":
                text = text[:a] + text[b:]
            elif kind == "duplicate":
                text = text[:b] + text[a:b] + text[b:]
            else:
                text = text[:a] + random.choice(SNIPS) + text[a:]
        rel = os.path.relpath(src, argv[1])
        dst = os.path.join(argv[2], rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(dst, "w", encoding="utf-8", newline="") as fh:
            fh.write(text)
        try:
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                lint.main(["x", "--no-slop-lint", dst])
        except SystemExit:
            pass
        except Exception as exc:  # the point of the test: report the type, never the page text
            failures += 1
            print("fuzz-lint: %s raised %s" % (rel, type(exc).__name__))
    print("fuzz-lint: %d mutations of %d pages, %d exception(s)" % (rounds, len(files), failures))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
