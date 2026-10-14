#!/usr/bin/env python3
"""selftest.py: run post-lint.py and copy-lint.py on good and bad inputs built at run time.

Usage (SKILLS is the folder that holds the moi-* skills):
    python3 "$SKILLS/moi-blog/scripts/selftest.py"

Builds every input in a temporary folder from the example post and the templates, runs each lint, and compares the
exit code and the rule names with what is expected. Writes nothing outside the temporary folder, uses no network and
needs no key. check-live.py runs here only on the cases that need no network: the rest of it needs the live site (see evals/evals.md).
Exit codes: 0 every case passed (or --help), 1 a case failed, 2 the skill folder could not be found.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
POST_LINT = HERE / "post-lint.py"
COPY_LINT = HERE / "copy-lint.py"
CHECK_LIVE = HERE / "check-live.py"
EXAMPLE = SKILL / "examples" / "moi-september-2026-release.md"
TEMPLATES = SKILL / "templates"

results = []
EM = chr(0x2014)  # built from its code point so this file never holds the character itself


def run(script, args, env_extra=None, unset=()):
    env = dict(os.environ)
    env.setdefault("SKILLS", str(SKILL.parent))
    for k in unset:
        env.pop(k, None)
    if env_extra:
        env.update(env_extra)
    r = subprocess.run([sys.executable, "-B", str(script)] + [str(a) for a in args], capture_output=True, text=True, env=env)
    return r.returncode, r.stdout + r.stderr


def case(name, code, out, want_code, rules=(), not_rules=()):
    ok = code == want_code
    for r in rules:
        ok = ok and (r in out)
    for r in not_rules:
        ok = ok and (r not in out)
    results.append(ok)
    print("%s %s (exit %d, want %d)%s" % ("PASS" if ok else "FAIL", name, code, want_code, "" if ok else "\n" + out))


def main():
    if any(a in ("-h", "--help") for a in sys.argv[1:]):
        print((__doc__ or "").strip())
        return 0
    if not EXAMPLE.is_file() or not POST_LINT.is_file():
        sys.stderr.write("selftest: cannot find the example post or post-lint.py next to this script\n")
        return 2
    tmp = Path(tempfile.mkdtemp(prefix="moi-blog-selftest-"))
    try:
        good = EXAMPLE.read_text(encoding="utf-8")

        def post(name, text):
            p = tmp / name
            p.write_text(text, encoding="utf-8")
            return p

        def mutate(old, new, name):
            assert old in good, "fixture text moved: %r" % old[:40]
            return post(name, good.replace(old, new, 1))

        # ---- post-lint ----
        c, o = run(POST_LINT, ["--strict", EXAMPLE])
        case("post-lint: the cleaned example, strict, outside a clone (one honest warning)", c, o, 0, ["0 error(s), 1 warning(s)", "siblings-not-checked"])
        c, o = run(POST_LINT, [TEMPLATES / "post-skeleton.md"])
        case("post-lint: the post skeleton is not publishable", c, o, 1, ["placeholder"])
        c, o = run(POST_LINT, [TEMPLATES / "release-post-skeleton.md"])
        case("post-lint: the release skeleton is not publishable", c, o, 1, ["placeholder"])
        p = mutate("summary:", "description:", "no-summary.md")
        c, o = run(POST_LINT, [p])
        case("post-lint: description instead of summary", c, o, 1, ["missing-field", "the blog field is `summary`"])
        p = post("author-string.md", re.sub(r'author:\n  name: "[^"]*"\n  role: "[^"]*"\n', 'author: "Someone"\n', good))
        c, o = run(POST_LINT, [p])
        case("post-lint: author as a plain string", c, o, 1, ["author-type"])
        p = mutate('  role: "Ecosystem, Sarva Labs"', '  role: "Ecosystem"\n  url: "sarvalabs.com"', "bare-url.md")
        c, o = run(POST_LINT, [p])
        case("post-lint: author.url without https", c, o, 1, ["author-url"])
        p = mutate("moipod is the software", "moipod " + EM + " the software", "emdash.md")
        c, o = run(POST_LINT, [p])
        case("post-lint: em dash character", c, o, 1, ["em-dash"])
        p = mutate("moipod is the software", "moipod &mdash; the software", "entity.md")
        c, o = run(POST_LINT, [p])
        case("post-lint: em dash entity", c, o, 1, ["em-dash"])
        p = mutate("\n## What is fee delegation?", "\n# A second title\n\n## What is fee delegation?", "h1.md")
        c, o = run(POST_LINT, [p])
        case("post-lint: H1 in the body", c, o, 1, ["h1-in-body"])
        p = mutate("\n## What is fee delegation?", "\n#### Skipped\n\n## What is fee delegation?", "skip.md")
        c, o = run(POST_LINT, [p])
        case("post-lint: heading level skipped", c, o, 1, ["heading-order"])
        p = mutate("[Sponsor Interactions tutorial](https://docs.moi.technology/docs/build/tutorials/sponsored-ix-tutorial) walks",
                   "[Sponsor Interactions tutorial](docs.moi.technology/docs/build/tutorials/sponsored-ix-tutorial) walks", "noscheme.md")
        c, o = run(POST_LINT, [p])
        case("post-lint: link without a scheme", c, o, 1, ["link-no-scheme"])
        p = mutate("moipod is the software", "<!-- check -->moipod is the software", "comment.md")
        c, o = run(POST_LINT, [p])
        case("post-lint: HTML comment", c, o, 1, ["html-comment"])
        p = mutate("moipod is the software", "TODO moipod is the software", "todo.md")  # slop-lint:ignore
        c, o = run(POST_LINT, [p])
        case("post-lint: TODO left in", c, o, 1, ["placeholder"])  # slop-lint:ignore
        p = mutate("moipod is the software", "{{what changed, in plain words}} moipod is the software", "braces.md")
        c, o = run(POST_LINT, [p])
        case("post-lint: a {{x}} placeholder in the body", c, o, 1, ["placeholder"])
        p = mutate('title: "', 'title: "{{Month}} ', "braces-title.md")
        c, o = run(POST_LINT, [p])
        case("post-lint: a {{x}} placeholder in the frontmatter", c, o, 1, ["placeholder"])
        p = mutate("moipod is the software", "Write `{{x}}` in the template. moipod is the software", "braces-code.md")
        c, o = run(POST_LINT, [p])
        case("post-lint: {{x}} inside inline code is not a placeholder", c, o, 0, not_rules=["placeholder"])
        c, o = run(POST_LINT, [post(".env", "title: not a post\n")])
        case("post-lint: an env file is refused and never opened", c, o, 2, ["refusing to read .env"], not_rules=["frontmatter-missing", "not a post"])
        c, o = run(POST_LINT, [post("marker.env", "MARK=Voyage devnet is account-centric\n")])
        case("post-lint: a *.env file is refused, no line echoed", c, o, 2, ["refusing to read marker.env"], not_rules=["account-centric", "MARK"])
        p = mutate('summary: "moipod v0.13.0 is live on devnet.', 'summary: moipod v0.13.0: live on devnet.', "colon.md")
        c, o = run(POST_LINT, [p])
        case("post-lint: unquoted colon in a value", c, o, 1, ["frontmatter-yaml", "unquoted colon"])
        p = mutate('tags: ["protocol", "native-assets"', 'tags: ["protocol", "native assets"', "tags.md")
        c, o = run(POST_LINT, [p])
        case("post-lint: a tag with a space", c, o, 1, ["tag-not-slug"])
        p = mutate("version 0.13.0 is live on devnet.", "version 0.13.0 is live on Voyage devnet.", "retired.md")  # slop-lint:ignore
        c, o = run(POST_LINT, [p])
        case("post-lint: retired term found by slop-lint", c, o, 1, ["slop-lint/voyage-devnet"])
        p = mutate("date: 2026-09-11", "date: 2026-13-45", "baddate.md")
        c, o = run(POST_LINT, [p])
        case("post-lint: impossible date", c, o, 1, ["date-invalid"])
        p = mutate("date: 2026-09-11", "date: 2026-09-11\ndate: 2026-09-12", "dupkey.md")
        c, o = run(POST_LINT, [p])
        case("post-lint: duplicate frontmatter key", c, o, 1, ["frontmatter-yaml", "duplicate key"])
        p = post("nofm.md", "## Heading\n\nText.\n")
        c, o = run(POST_LINT, [p])
        case("post-lint: no frontmatter", c, o, 1, ["frontmatter-missing"])
        long_summary = re.sub(r'summary: "[^"]*"', 'summary: "' + ("A long sentence about the release. " * 8).strip() + '"', good, count=1)
        p = post("longsummary.md", long_summary)
        c, o = run(POST_LINT, [p])
        case("post-lint: long summary is a warning", c, o, 0, ["WARN:summary-length"])
        c, o = run(POST_LINT, ["--strict", p])
        case("post-lint: long summary fails with --strict", c, o, 1, ["ERROR:summary-length"])
        p = post("subscribe.md", good + "\n<Subscribe />\n")
        c, o = run(POST_LINT, [p])
        case("post-lint: stray <Subscribe /> is a warning", c, o, 0, ["stray-subscribe"])
        p = mutate('  - "Use parseKmoi', '  - "Hmm"\n  - "Use parseKmoi', "nine.md")
        c, o = run(POST_LINT, [p])
        case("post-lint: nine takeaways is a warning", c, o, 0, ["takeaways-count"])

        # a fake repo for the image, cover and sibling checks
        repo = tmp / "repo"
        (repo / "blog" / "src" / "content" / "posts").mkdir(parents=True)
        (repo / "blog" / "src" / "assets" / "demo").mkdir(parents=True)
        (repo / "blog" / "public" / "covers").mkdir(parents=True)
        (repo / "blog" / "src" / "content" / "posts" / "sibling-post.md").write_text("---\ntitle: x\n---\n", encoding="utf-8")
        for sib in ("moi-august-2026-release", "what-is-moi-network"):
            (repo / "blog" / "src" / "content" / "posts" / (sib + ".md")).write_text("---\ntitle: x\n---\n", encoding="utf-8")
        c, o = run(POST_LINT, ["--strict", "--repo", repo, EXAMPLE])
        case("post-lint: the cleaned example, strict, with a clone to check its links against", c, o, 0, ["0 error(s), 0 warning(s)"])
        img = "\n![The payer signs the interaction before the sender sends it](../../assets/demo/flow.png)\n"
        p = repo / "blog" / "src" / "content" / "posts" / "with-image.md"
        p.write_text(good.replace("\n## What is fee delegation?", img + "\n## What is fee delegation?", 1), encoding="utf-8")
        c, o = run(POST_LINT, ["--repo", repo, p])
        case("post-lint: image that does not exist", c, o, 1, ["image-missing"])
        (repo / "blog" / "src" / "assets" / "demo" / "flow.png").write_bytes(b"\x89PNG")
        c, o = run(POST_LINT, ["--repo", repo, p])
        case("post-lint: image that exists", c, o, 0, not_rules=["image-missing"])
        c, o = run(POST_LINT, [p])
        case("post-lint: repo found from the file path", c, o, 0, not_rules=["image-missing", "images-not-checked"])
        outside = post("outside-image.md", p.read_text(encoding="utf-8"))
        c, o = run(POST_LINT, [outside])
        case("post-lint: images outside a repo are reported as not checked", c, o, 0, ["images-not-checked"])
        cov = good.replace('draft: false', 'cover: "/covers/demo.svg"\ndraft: false', 1)
        p2 = repo / "blog" / "src" / "content" / "posts" / "with-cover.md"
        p2.write_text(cov, encoding="utf-8")
        (repo / "blog" / "public" / "covers" / "demo.svg").write_text("<svg/>", encoding="utf-8")
        c, o = run(POST_LINT, ["--repo", repo, p2])
        case("post-lint: SVG cover without its PNG", c, o, 1, ["cover-png-missing"])
        (repo / "blog" / "public" / "covers" / "demo.png").write_bytes(b"\x89PNG")
        c, o = run(POST_LINT, ["--repo", repo, p2])
        case("post-lint: SVG cover with its PNG", c, o, 0, not_rules=["cover-png-missing", "cover-missing"])
        p3 = repo / "blog" / "src" / "content" / "posts" / "with-sibling.md"
        p3.write_text(good + "\nSee [the other post](https://blog.moi.technology/article/no-such-post/) too.\n", encoding="utf-8")
        c, o = run(POST_LINT, ["--repo", repo, p3])
        case("post-lint: link to a sibling that does not exist is a warning", c, o, 0, ["sibling-not-found"])

        # the lint must never echo a secret that sits in a post (values are built here from a prefix plus filler)
        k_anthropic = "sk-" + "ant-" + "A" * 30
        k_github = "gh" + "p_" + "b" * 36
        k_aws = "AK" + "IA" + "C" * 16
        p = mutate('tags: ["protocol"', 'tags: ["%s", "protocol"' % k_anthropic, "secret-tag.md")
        c, o = run(POST_LINT, [p])
        case("post-lint: a key-shaped tag is reported and never echoed", c, o, 1, ["tag-not-slug", "<masked>"], not_rules=[k_anthropic[:12]])
        p = mutate("[js-moi-sdk](https://github.com/sarvalabs/js-moi-sdk)", "[js-moi-sdk](docs.moi.technology/x?token=%s)" % k_github, "secret-link.md")
        c, o = run(POST_LINT, [p])
        case("post-lint: a token in a link address is reported and never echoed", c, o, 1, ["link-no-scheme", "token=<masked>"], not_rules=[k_github[:8]])
        p = mutate("date: 2026-09-11", "date: %s" % k_aws, "secret-date.md")
        c, o = run(POST_LINT, [p])
        case("post-lint: a key-shaped date is reported and never echoed", c, o, 1, ["date-invalid"], not_rules=[k_aws[:8]])
        p = post("tabs.md", "---\ntitle: x\n\tsummary: y\n---\n## H\n")
        c, o = run(POST_LINT, [p])
        case("post-lint: unreadable YAML skips the field checks, so no false missing field", c, o, 1, ["frontmatter-yaml", "tab used"], not_rules=["missing-field"])
        p = post("outside-sibling.md", good + "\nSee [the other post](https://blog.moi.technology/article/what-is-moi-network/) too.\n")
        c, o = run(POST_LINT, [p])
        case("post-lint: sibling links are reported as not checked outside a repo", c, o, 0, ["siblings-not-checked"])

        p = mutate("moipod is the software", "moipod " + chr(0x1F680) + " is the software", "emoji.md")
        c, o = run(POST_LINT, [p])
        case("post-lint: an emoji is a warning", c, o, 0, ["WARN:emoji"])

        p = post("crlf.md", good.replace("\n", "\r\n"))
        c, o = run(POST_LINT, ["--strict", p])
        case("post-lint: Windows line endings read the same as Unix ones", c, o, 0, ["0 error(s)"])
        p = post("bom.md", "\ufeff" + good)
        c, o = run(POST_LINT, ["--strict", p])
        case("post-lint: a byte order mark at the start is ignored", c, o, 0, ["0 error(s)"])

        # slop-lint wiring
        iso = tmp / "isolated"
        iso.mkdir()
        shutil.copy(str(POST_LINT), str(iso / "post-lint.py"))
        c, o = run(iso / "post-lint.py", [EXAMPLE], unset=("SKILLS",))
        case("post-lint: missing slop-lint.sh is an error", c, o, 1, ["slop-lint-missing"])
        c, o = run(iso / "post-lint.py", ["--no-slop-lint", EXAMPLE], unset=("SKILLS",))
        case("post-lint: --no-slop-lint skips it on purpose", c, o, 0, not_rules=["slop-lint-missing"])
        c, o = run(POST_LINT, [tmp / "does-not-exist.md"])
        case("post-lint: unreadable file", c, o, 2)
        c, o = run(POST_LINT, [])
        case("post-lint: no argument", c, o, 2)
        c, o = run(POST_LINT, ["--repo", tmp / "nowhere", EXAMPLE])
        case("post-lint: --repo without a blog folder", c, o, 2)

        # ---- copy-lint ----
        social = tmp / "social"
        social.mkdir()
        good_copy = (
            "---\nslug: moi-september-2026-release\ntitle: \"MOI September 2026 Release: fee delegation and anu pricing\"\n"
            "published: 2026-09-11\n\nx: |\n  An interaction on MOI can now name a separate fee payer. The payer signs it too and pays the fuel instead of the sender.\n\n"
            "  moipod v0.13.0 is live on devnet.\n\n  {{link}}\n\nlinkedin: |\n  If you build on MOI, moipod v0.13.0 changes how fuel is paid.\n\n"
            "  An interaction can now name a separate fee payer. The fee payer also signs the interaction and pays the fuel cost instead of the sender.\n\n  {{link}}\n---\n\nNotes: none.\n")

        def copy(name, text):
            p = social / name
            p.write_text(text, encoding="utf-8")
            return p

        gp = copy("moi-september-2026-release.md", good_copy)
        c, o = run(COPY_LINT, ["--post", EXAMPLE, gp])
        case("copy-lint: hand-written X and LinkedIn copy", c, o, 0, ["0 error(s), 0 warning(s)"])
        c, o = run(COPY_LINT, [TEMPLATES / "announce" / "social-copy.md"])
        case("copy-lint: the template is not sendable", c, o, 1, ["placeholder"])
        seeded = good_copy.replace(
            good_copy[good_copy.index("x: |"):good_copy.index("linkedin: |")],
            "x: |\n  moipod v0.13.0 is live on devnet. An interaction can name a separate fee payer, KMOI has a capped supply and a new asset id, and fuel and storage are priced in anu.\n\n  {{link}}\n\n")
        sp = copy("seeded.md", seeded.replace("slug: moi-september-2026-release", "slug: seeded"))
        c, o = run(COPY_LINT, ["--post", EXAMPLE, sp])
        case("copy-lint: X block still the seeded summary", c, o, 1, ["unrewritten-scaffold"])
        long_x = good_copy.replace("  moipod v0.13.0 is live on devnet.\n", "  " + ("A very long sentence about the release. " * 9).strip() + "\n")
        c, o = run(COPY_LINT, ["--post", EXAMPLE, copy("moi-september-2026-release.md", long_x)])
        case("copy-lint: X copy over 280 characters", c, o, 1, ["too-long"])
        bt = good_copy.replace("pays the fuel instead", "pays the `fuel` instead")
        c, o = run(COPY_LINT, ["--post", EXAMPLE, copy("moi-september-2026-release.md", bt)])
        case("copy-lint: backticks in X copy", c, o, 1, ["markup"])
        dc = good_copy.replace("---\n\nNotes", "\ndiscord: |\n  Fee delegation is live on devnet.\n\n  {{link}}\n---\n\nNotes")
        c, o = run(COPY_LINT, ["--post", EXAMPLE, copy("moi-september-2026-release.md", dc)])
        case("copy-lint: a Discord block is a warning", c, o, 0, ["immediate-channel"])
        em = good_copy.replace("fuel instead of the sender.", "fuel " + EM + " instead of the sender.", 1)
        c, o = run(COPY_LINT, ["--post", EXAMPLE, copy("moi-september-2026-release.md", em)])
        case("copy-lint: em dash found by slop-lint", c, o, 1, ["em-dash"])
        c, o = run(COPY_LINT, ["--post", EXAMPLE, copy("other-name.md", good_copy)])
        case("copy-lint: slug differs from the file name", c, o, 1, ["slug-mismatch"])
        nl = good_copy.replace("  moipod v0.13.0 is live on devnet.\n\n  {{link}}", "  moipod v0.13.0 is live on devnet.")
        c, o = run(COPY_LINT, ["--post", EXAMPLE, copy("moi-september-2026-release.md", nl)])
        case("copy-lint: no link token is a warning", c, o, 0, ["no-link-token"])
        td = good_copy.replace("is live on devnet.", "went live today.", 1)
        c, o = run(COPY_LINT, ["--post", EXAMPLE, copy("moi-september-2026-release.md", td)])
        case("copy-lint: a relative word is a warning", c, o, 0, ["relative-word"])
        em_ = good_copy.replace("is live on devnet.", "is live on devnet " + chr(0x1F680), 1)
        c, o = run(COPY_LINT, ["--post", EXAMPLE, copy("moi-september-2026-release.md", em_)])
        case("copy-lint: an emoji is a warning", c, o, 0, ["WARN:emoji"])
        bad_indent = good_copy.replace("\n  moipod v0.13.0 is live on devnet.\n", "\nmoipod v0.13.0 is live on devnet.\n")
        c, o = run(COPY_LINT, ["--post", EXAMPLE, copy("moi-september-2026-release.md", bad_indent)])
        case("copy-lint: a block line indented too little", c, o, 1, ["frontmatter-yaml"])
        c, o = run(COPY_LINT, [tmp / "missing.md"])
        case("copy-lint: unreadable file", c, o, 2)
        c, o = run(COPY_LINT, [post(".env.local", "slug: x\n")])
        case("copy-lint: an env file is refused and never opened", c, o, 2, ["refusing to read .env.local"], not_rules=["frontmatter-missing"])
        c, o = run(COPY_LINT, ["--post", tmp / "marker.env", gp])
        case("copy-lint: an env file named as --post is refused", c, o, 2, ["refusing to read marker.env"])
        sec_copy = good_copy.replace("  moipod v0.13.0 is live on devnet.\n", "  Ask at https://discord" + ".com/api/webhooks/" + "1" * 18 + "/" + "d" * 40 + "\n", 1)
        c, o = run(COPY_LINT, ["--post", EXAMPLE, copy("moi-september-2026-release.md", sec_copy)])
        case("copy-lint: a webhook address in copy is never echoed", c, o, 0, not_rules=["d" * 12, "1" * 18])

        # ---- check-live: only the cases that need no network ----
        c, o = run(CHECK_LIVE, ["Bad Slug"])
        case("check-live: a slug with a space and capitals", c, o, 2, ["lowercase with hyphens"])
        c, o = run(CHECK_LIVE, ["x", "--origin", "file:///etc"])
        case("check-live: a file address is refused", c, o, 2, ["http:// or https://"])
        c, o = run(CHECK_LIVE, ["x", "--apex", "ftp://example.invalid"])
        case("check-live: an ftp address is refused", c, o, 2, ["http:// or https://"])
        c, o = run(CHECK_LIVE, ["x", "--origin", "http://127.0.0.1:9/?key=" + "A" * 8 + "z9" * 8])
        case("check-live: an unreachable host exits 2 and hides the query string", c, o, 2, ["cannot reach the host", "<query hidden>"], not_rules=["A" * 8])
    finally:
        shutil.rmtree(str(tmp), ignore_errors=True)
    failed = results.count(False)
    print("selftest: %d passed, %d failed" % (results.count(True), failed))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
