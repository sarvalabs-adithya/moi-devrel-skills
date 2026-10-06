#!/usr/bin/env python3
"""make-fixtures.py: build the test pages for docs-page-lint.py in a scratch folder.

Usage:   python3 "$SKILLS/moi-docs/evals/make-fixtures.py" <empty scratch folder>
Output:  prints the folder it filled. Every file is made at run time. Anything secret-shaped is a known prefix
         plus filler (zq repeated), and the 12-word run is twelve made-up filler words; no real key, token or
         recovery phrase is involved. Exit 2 if the folder is missing or not empty.
Reads nothing but its argument. Writes only inside that folder.
"""
import os
import sys

EM = chr(0x2014)


def main():
    if len(sys.argv) != 2 or not os.path.isdir(sys.argv[1]) or os.listdir(sys.argv[1]):
        print("usage: make-fixtures.py <empty scratch folder>", file=sys.stderr)
        return 2
    base = sys.argv[1]

    def w(name, text, binary=False):
        path = os.path.join(base, name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if binary:
            with open(path, "wb") as fh:
                fh.write(text)
        else:
            with open(path, "w", encoding="utf-8", newline="") as fh:
                fh.write(text)

    d = ("Accounts hold the state of a participant on MOI, with keys, a sequence number and assets. "
         "This sample page is used to test the docs page lint end to end.")
    good = ("---\nimage: /img/moi-card-learn.png\nsidebar_position: 1\ntitle: Sample\ndescription: \"" + d + "\"\n---\n\n"
            "An account is the unit MOI uses to hold the state of a participant.\n\n## What is it?\n\nText.\n")
    L = "moidocs/docs/learn/x/"
    w(L + "good.md", good)
    w(L + "blank-first.md", "\n" + good)
    w(L + "colon.md", good.replace('description: "' + d + '"', "description: Accounts: how they work in MOI and what keys they hold"))
    w(L + "innerquote.md", good.replace('description: "' + d + '"', 'description: "He said "hi" and left"'))
    w(L + "unclosed.md", "---\ntitle: A\ndescription: B\n\nBody\n")
    w(L + "nofm.md", "# Just a heading\n\nNo frontmatter here.\n")
    w(L + "nodesc.md", "---\nimage: /img/moi-card-learn.png\nsidebar_position: 1\ntitle: Sample\n---\n\nAn account is the unit MOI uses to hold participant state and keys.\n")
    w(L + "crlf.md", good.replace("\n", "\r\n"))
    w(L + "bom.md", chr(0xFEFF) + good)
    w(L + "dupkey.md", good.replace("title: Sample", "title: Sample\ntitle: Again"))
    w(L + "multiline.md", good.replace('description: "' + d + '"', "description: >\n  Accounts hold the state of a participant on MOI, with keys and assets.\n  This sample page is used to test the lint."))
    w(L + "longtitle.md", good.replace("title: Sample", "title: A very long title that goes on and on past sixty characters in total for sure v0.9.2"))
    w(L + "wrongimage.md", good.replace("moi-card-learn", "moi-card-build"))
    w(L + "text.md", good + "\nSee Moi Wallet, MoiWallet, CoCo and CocoLang, JS-MOI-SDK, Moipod and SarvaLabs. `JS-MOI-SDK` in code is fine.\n"  # slop-lint: ignore
      "An em dash " + EM + " here.\nTODO write this. Also REPLACE-WITH-LINK and lorem ipsum.\nThe Agent Launchpad is covered elsewhere.\n"  # slop-lint: ignore
      "See C:\\" + "Users\\me\\x and /Us" + "ers/me/y.\n")
    w(L + "links.md", good + "\n[a](docs.moi.technology/docs/x) [b]() [c](http://example.com/x) [d](https://docs.moi.technology/docs/learn/x) "
      "[e](https://github.com/sarvalabs/go-moi/blob/main/x.go) [f](www.example.com) [g](hello@moi.technology) [h](#nope) "
      "[i](#what-is-it) [j](../ok.md) ![](img.png)\n")
    w("coco-docs/docs/book/x/links.md", "---\nsidebar_position: 1\ntitle: Links\ndescription: \"" + d + "\"\n---\n\n# Links\n\n"
      "A coco page opens by saying what it is, in one plain sentence about Coco.\n\n[a](/book/language/state) [b](/book/language/state/) "
      "[c](/book/language/state/#x) [d](https://cocolang.dev/book/x/) [e](/img/a.svg)\n")
    T = "moidocs/docs/build/tutorials/"
    build = good.replace("learn", "build")
    w(T + "noimport.md", build.replace("\n\nAn account", "\n\n<HowToSchema name=\"x\" steps={[{\"name\": \"a\", \"text\": \"b\"}]} />\n\nAn account"))
    w(T + "blankline.md", build.replace("\n\nAn account", "\n\nimport HowToSchema from '@site/src/components/HowToSchema';\n\n"
      "<HowToSchema name=\"x\" steps={[\n\n{\"name\": \"a\", \"text\": \"b\"}]} />\n\n# Title\n\nAn account"))
    w("voyage-docs/docs/endpoint-docs/schema.md", "---\nsidebar_position: 1\ntitle: Faq\ndescription: \"" + d + "\"\n---\n\n"
      "import FaqSchema from '@site/src/components/FaqSchema';\n\n<FaqSchema faqs={[{q: \"a\", a: \"b\"}]} />\n\nA sentence that says what this thing is.\n")
    w(T + "no-howto-tutorial.md", build)
    w(L + "headings.md", good + "\n# Second\n\n#### Deep\n\n```\n# not a heading\n```\n")
    w(L + "stub.md", "---\nimage: /img/moi-card-learn.png\nsidebar_position: 8\ntitle: Networks\ndescription: \"" + d + "\"\n---\n\n"
      ":::caution Coming Soon!\nDocumentation for this page is under development.\n:::\n")
    w(L + "stub-marked-finished.md", good.replace("---\n\nAn account", "---\n\n<head>\n  <meta name=\"robots\" content=\"noindex\" />\n</head>\n\nAn account")
      + " ".join(["The page is plain text and it has no real content at all."] * 20) + "\n")
    w(L + "throat.md", good.replace("An account is the unit MOI uses to hold the state of a participant.",
      "Before diving into accounts, it's worth understanding a bit about how MOI structures its network."))
    w("voyage-docs/docs/endpoint-docs/teaser.md", "---\nsidebar_position: 1\ntitle: Teaser\ndescription: \"Learn everything about the faucet in this page and much more besides, with plenty of detail to go on.\"\n---\n\nThe Faucet API gives test tokens.\n")
    filler = "zq" * 20
    words = " ".join(chr(97 + i) * 3 for i in range(12))  # twelve filler words: aaa bbb ccc ...
    w(L + "secrets.md", good + "\nkey sk-ant-" + filler + " and ghp_" + filler + " and AKIA" + "ZQ" * 8 + " and eyJ" + filler + ".eyJ" + filler + "." + filler
      + "\nphrase: " + words + "\n")
    w(".env", "SECRET=sk-ant-" + filler + "\n")
    w("prod.env", "x\n")
    w(".env.local", "x\n")
    w("binary.md", b"\xff\xfe\x00\x00binary", binary=True)
    w("latin1.md", "---\ntitle: caf\xe9\n---\n".encode("latin-1"), binary=True)
    w("empty.md", "")
    w("notes.txt", "hello\n")
    w("huge.md", "x" * 2100000)
    os.makedirs(os.path.join(base, "emptydir"))
    # Sphinx
    rd = "Install js-moi-sdk with npm and make your first calls to the MOI network - providers, wallet setup, and a first interaction in JavaScript or TypeScript."
    S = "sdk/docs/source/"
    w(S + "index.rst", "=============\nDocumentation\n=============\n\n.. toctree::\n   :maxdepth: 2\n\n   good\n   Nice Title <titled>\n")
    w(S + "good.rst", ".. meta::\n   :description: " + rd + "\n\n=====\nGood\n=====\n\nSome text.\n\nSection\n-------\n\nMore.\n")
    w(S + "titled.rst", ".. meta::\n   :description: " + rd + "\n\n======\nTitled\n======\n\nText.\n")
    w(S + "nometa.rst", "=====\nNoMeta\n=====\n\nText\n")
    w(S + "short.rst", ".. meta::\n   :description: " + rd + "\n\nA long title for a short line\n-----\n\nText and `bad <docs.moi.technology/x>`_ and "
      "`ok <https://moi.technology>`_ and JS-MOI-SDK and a dash " + EM + ".\n\n.. code-block:: js\n\n   const x = 'JS-MOI-SDK'; // TODO\n")  # slop-lint: ignore
    w(S + "orphan.rst", ".. meta::\n   :description: " + rd + "\n\n======\nOrphan\n======\n\nText.\n")
    w(S + "two.rst", ".. meta::\n   :description: " + rd + "\n\n=======\nTitle A\n=======\n\nText\n\n=======\nTitle B\n=======\n\nMore\n")
    w("sdk/docs/generate_llms.py", 'PAGES = {\n    "good": ("Good", "' + rd + '"),\n    "titled": ("Titled", "A different description that does not match what the page says at all, so the lint must complain."),\n}\n')
    w(S + "_extra/sitemap.xml", "<urlset><url><loc>https://js-moi-sdk.docs.moi.technology/good</loc></url></urlset>\n")
    w("moidocs/docs/learn/x/_category_.json", "{ not json")
    w("moidocs/docs/learn/_category_.json", '{"label":"L","link":{"type":"generated-index","description":"Too short."}}')
    # folder walk
    for sub in ("walk/static/docs", "walk/build", "walk/node_modules/x", "walk/docs/learn", "walk/docs/_extra"):
        w(sub + "/page.md", good)
    w("walk/docs/learn/_partial.md", good)
    w("walk/docs/build/page.md", build)
    w("walk/build/index.html", "<html></html>")
    # what a checkout holds: main versus the PR branch (docusaurus.config.js, section cards, schema components)
    cfg_main = "module.exports = { url: 'https://example.invalid', presets: [['classic', { docs: { sidebarPath: './sidebars.js' } }]] };\n"
    cfg_root = "module.exports = { url: 'https://example.invalid', presets: [['classic', { docs: { routeBasePath: '/' } }]] };\n"
    coco = ("---\nsidebar_position: 1\ntitle: Links\ndescription: \"" + d + "\"\n---\n\n# Links\n\n"
            "A coco page opens by saying what it is, in one plain sentence about Coco.\n\n[a](/book/language/state/) [b](/docs/book/language/state/) [c](/docs/book/language/state)\n")
    w("state/coco-main/docusaurus.config.js", cfg_main)
    w("state/coco-main/docs/book/x/page.md", coco)
    w("state/coco-pr/docusaurus.config.js", cfg_root)
    w("state/coco-pr/docs/book/x/page.md", coco)
    tut = ("---\nsidebar_position: 3\ntitle: Pay fuel\ndescription: \"" + d + "\"\n---\n\n"
           "import HowToSchema from '@site/src/components/HowToSchema';\n\n<HowToSchema name=\"x\" steps={[{\"name\": \"a\", \"text\": \"b\"}]} />\n\n"
           "A tutorial that shows how to pay fuel for another participant on MOI.\n")
    plain = tut.split("import HowToSchema")[0] + "A tutorial that shows how to pay fuel for another participant on MOI.\n"
    w("state/moidocs-main/docusaurus.config.js", cfg_main)
    w("state/moidocs-main/docs/build/tutorials/with-component.md", tut)
    w("state/moidocs-main/docs/build/tutorials/plain.md", plain)
    w("state/moidocs-main/docs/learn/x/noimage.md", good.replace("image: /img/moi-card-learn.png\n", ""))
    w("state/moidocs-main/docs/learn/x/withimage.md", good)
    w("state/moidocs-pr/docusaurus.config.js", cfg_main)
    w("state/moidocs-pr/src/components/HowToSchema.jsx", "export default function HowToSchema() { return null; }\n")
    w("state/moidocs-pr/static/img/moi-card-learn.png", b"png", binary=True)
    w("state/moidocs-pr/docs/build/tutorials/with-component.md", tut.replace("sidebar_position: 3", "image: /img/moi-card-build.png\nsidebar_position: 3"))
    w("state/moidocs-pr/docs/build/tutorials/plain.md", plain.replace("sidebar_position: 3", "image: /img/moi-card-build.png\nsidebar_position: 3"))
    w("state/moidocs-pr/docs/learn/x/noimage.md", good.replace("image: /img/moi-card-learn.png\n", ""))
    # secret-shaped text in the frontmatter, and an env-named folder
    w(L + "fm-secret.md", good.replace("title: Sample", "title: Sample sk-ant-" + filler))
    w("envdir/.env/docs/learn/page.md", good)
    print("filled", base)
    return 0


if __name__ == "__main__":
    sys.exit(main())
