#!/usr/bin/env bash
# scratch-tests.sh: re-run every script and sequence test of moi-devrel/ship on throwaway repositories.
#
# Usage:   SKILLS=<folder that holds the moi-* skills> bash "$SKILLS/moi-devrel/ship/evals/scratch-tests.sh"
# Output:  one line per check, "ok" or "NOT OK" with the value seen, then a count. Exit 0 when every check
#          is ok, 1 when any is not, 2 when SKILLS, git or python3 is missing.
# Safety:  everything happens in a folder made with mktemp -d and deleted at the end when all checks pass
#          (kept, with its path printed, when one fails). The remotes are local bare repositories, so
#          nothing is pushed anywhere. The real preflight.sh runs once (it reads your own gh login).
#          Secret-shaped inputs are built at run time from a prefix plus filler. Your global git
#          configuration is ignored. Works with bash 3.2 and zsh installed (the zsh checks are skipped
#          when zsh is missing).
[ -n "${SKILLS:-}" ] && [ -f "$SKILLS/moi-devrel/ship/scripts/ship-preflight.sh" ] || { echo "scratch-tests: set SKILLS to the folder that holds the moi-* skills" >&2; exit 2; }
for tool in git python3; do command -v "$tool" >/dev/null 2>&1 || { echo "scratch-tests: $tool is needed" >&2; exit 2; }; done
export GIT_CONFIG_GLOBAL=/dev/null
S="$SKILLS/moi-devrel/ship/scripts/ship-preflight.sh"
RP="$SKILLS/moi-devrel/ship/scripts/rebase-proof.sh"
AWKF="$SKILLS/moi-devrel/ship/templates/strip-ai-lines.awk"
export GIT_CONFIG_NOSYSTEM=1
T="$(mktemp -d)" && [ -d "$T" ] || { echo "scratch-tests: cannot make a scratch folder" >&2; exit 2; }
echo "scratch=$T"
FILLER="$(python3 -c "print('zq'*20)")"
PHRASE="$(python3 -c "print(' '.join(chr(97 + i) * 6 for i in range(12)))")"   # twelve placeholder words, built at run time
PASS=0; FAILN=0
check() { # name, expected, actual
  if [ "$2" = "$3" ]; then PASS=$((PASS+1)); echo "ok      $1 -> $3"; else FAILN=$((FAILN+1)); echo "NOT OK  $1 -> expected [$2] got [$3]"; fi
}
has() { # name, haystack-file, needle
  if grep -q -- "$3" "$2"; then PASS=$((PASS+1)); echo "ok      $1"; else FAILN=$((FAILN+1)); echo "NOT OK  $1 (missing: $3)"; fi
}
hasnot() {
  if grep -q -- "$3" "$2"; then FAILN=$((FAILN+1)); echo "NOT OK  $1 (found: $3)"; else PASS=$((PASS+1)); echo "ok      $1"; fi
}
run() { # file, command...
  local out="$1"; shift
  "$@" >"$out" 2>&1; echo $?
}
mkrepo() { # name -> creates $T/<name>-remote.git and $T/<name> with main, two commits
  git init -q --bare "$T/$1-remote.git"; git -C "$T/$1-remote.git" symbolic-ref HEAD refs/heads/main
  git clone -q "$T/$1-remote.git" "$T/$1" 2>/dev/null
  ( cd "$T/$1" && git config user.name "Test Operator" && git config user.email operator@example.org \
    && git switch -q -c main && printf 'a1\n' > a.txt && printf 'page1\n' > page.md && printf 'o1\no2\no3\n' > other.md \
    && git add . && git commit -q -m "base: first" && printf 'a2\n' > a.txt && git commit -qam "base: second" \
    && git push -q -u origin main 2>/dev/null && git remote set-head origin main )
}
export PREFLIGHT_WORK_DOMAINS=example.org

echo "=== ship-preflight.sh"
mkrepo p; cd "$T/p"
git switch -q --no-track -c fix/page origin/main; printf 'page2\n' > page.md; git add page.md; git commit -q -m "docs: update page"
check "P01 good branch, full preflight, exit" 0 "$(run "$T/o01" bash "$S" origin/main)"
has   "P01 preflight section printed" "$T/o01" "moi-devrel preflight.sh"
has   "P01 files changed listed" "$T/o01" "M  page.md"
check "P02 good branch, --no-preflight, exit" 0 "$(run "$T/o02" bash "$S" --no-preflight origin/main)"
has   "P02 says identity unchecked" "$T/o02" "WARN  moi-devrel preflight.sh was skipped"
git switch -q main
check "P03 on main, exit" 1 "$(run "$T/o03" bash "$S" --no-preflight origin/main)"
has   "P03 FAIL branch is deploy branch" "$T/o03" "FAIL  branch main is the default branch"
has   "P03 FAIL nothing to ship" "$T/o03" "FAIL  no commit ahead"
git switch -q --no-track -c t/claude origin/main; printf x > ai.txt; git add ai.txt; git commit -q -m "feat: x" -m "Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"  # slop-lint:ignore
check "P04 Claude trailer, exit" 1 "$(run "$T/o04" bash "$S" --no-preflight origin/main)"
has   "P04 FAIL AI trailer" "$T/o04" "FAIL  1 of 1 commit(s) carry an AI co-author trailer"
git switch -q --no-track -c t/copilot origin/main; printf x > ai.txt; git add ai.txt; git commit -q -m "feat: y" -m "Co-authored-by: Copilot <copilot@users.noreply.github.com>"  # slop-lint:ignore
check "P05 Copilot trailer, exit" 1 "$(run "$T/o05" bash "$S" --no-preflight origin/main)"
git switch -q --no-track -c t/footer origin/main; printf x > ai.txt; git add ai.txt; git commit -q -m "feat: z" -m "$(printf '\xf0\x9f\xa4\x96 Generated with [Claude Code](https://claude.com/claude-code)')"  # slop-lint:ignore
check "P06 generated-with footer, exit" 1 "$(run "$T/o06" bash "$S" --no-preflight origin/main)"
git switch -q --no-track -c t/human origin/main; printf x > h.txt; git add h.txt; git commit -q -m "feat: h" -m "Co-authored-by: Real Person <real@example.org>"  # slop-lint:ignore
check "P07 human co-author, exit" 0 "$(run "$T/o07" bash "$S" --no-preflight origin/main)"
has   "P07 PASS no AI line" "$T/o07" "PASS  no AI co-author trailer"
git switch -q --no-track -c t/legit origin/main; printf x > l.txt; git add l.txt; git commit -q -m "feat: chat endpoint" -m "Uses the OpenAI SDK and the Claude API for replies. Gemini support is planned."
check "P08 message that only names AI products, exit" 0 "$(run "$T/o08" bash "$S" --no-preflight origin/main)"
git switch -q --no-track -c t/personal origin/main; printf x > p.txt; git add p.txt; git -c user.email=someone@gmail.com commit -q -m "feat: p"
check "P09 personal-provider address, exit" 1 "$(run "$T/o09" bash "$S" --no-preflight origin/main)"
has   "P09 FAIL personal address" "$T/o09" "FAIL  2 author or committer address(es) at a personal mail provider"
git switch -q --no-track -c t/env origin/main; printf 'FOO=bar\n' > .env.local; git add -f .env.local; git commit -q -m "feat: env"
check "P10 env-named file committed, exit" 1 "$(run "$T/o10" bash "$S" --no-preflight origin/main)"
has   "P10 name hidden" "$T/o10" "A  \[env-named file\]"
hasnot "P10 real name not printed" "$T/o10" "env.local"
git switch -q --no-track -c t/envex origin/main; printf 'FOO=\n' > .env.example; git add .env.example; git commit -q -m "chore: env example"
check "P11 .env.example committed, exit" 0 "$(run "$T/o11" bash "$S" --no-preflight origin/main)"
git switch -q --no-track -c t/secret origin/main; printf 'token = "%s"\n' "sk-ant-$FILLER" > cfg.txt; git add cfg.txt; git commit -q -m "feat: cfg ghp_$FILLER"
check "P12 secret-shaped file and message, exit" 1 "$(run "$T/o12" bash "$S" --no-preflight origin/main)"
has   "P12 FAIL secret scan" "$T/o12" "FAIL  secret-scan.sh found"
hasnot "P12 filler never echoed" "$T/o12" "zqzqzq"
git switch -q --no-track -c t/phrase origin/main; printf '%s\n' "$PHRASE" > notes.txt; git add notes.txt; git commit -q -m "chore: $PHRASE"
check "P13 recovery-phrase-shaped subject and file, exit" 1 "$(run "$T/o13" bash "$S" --no-preflight origin/main)"
has   "P13 subject masked" "$T/o13" "masked: 12 or more short words"
hasnot "P13 phrase never echoed" "$T/o13" "aaaaaa bbbbbb"
git switch -q main
# base moves, conflict, behind, upstream states
git clone -q "$T/p-remote.git" "$T/p-mate" 2>/dev/null
( cd "$T/p-mate" && git config user.name Mate && git config user.email mate@example.org && printf 'page BASE\n' > page.md && git commit -qam "base: page" && git push -q origin main )
git switch -q fix/page; git fetch -q origin
check "P14 behind base and conflicting, exit" 0 "$(run "$T/o14" bash "$S" --no-preflight origin/main)"
has   "P14 WARN behind" "$T/o14" "WARN  1 commit(s) behind origin/main"
has   "P14 WARN predicted conflict in page.md" "$T/o14" "would conflict in 1 file(s): page.md"
git push -q -u origin fix/page 2>/dev/null
check "P15 in step with upstream, exit" 0 "$(run "$T/o15" bash "$S" --no-preflight origin/main)"
has   "P15 PASS in step" "$T/o15" "PASS  in step with origin/fix/page"
( cd "$T/p-mate" && git fetch -q origin && git switch -q fix/page && printf m > m.txt && git add m.txt && git commit -q -m "mate" && git push -q origin fix/page )
git fetch -q origin
check "P16 teammate pushed, exit" 0 "$(run "$T/o16" bash "$S" --no-preflight origin/main)"
has   "P16 WARN behind upstream" "$T/o16" "WARN  1 commit(s) behind origin/fix/page"
git commit -q --allow-empty -m "local: extra"
check "P17 diverged, exit" 0 "$(run "$T/o17" bash "$S" --no-preflight origin/main)"
has   "P17 WARN diverged, tells you to read the remote commits first" "$T/o17" "Read the 1 commit(s) the remote has and you lack"
git reset -q --hard HEAD~1
git switch -q --no-track -c t/merge "$(git rev-parse origin/main~1)"; printf o > own.txt; git add own.txt; git commit -q -m "feat: own"; git merge -q --no-ff -m "Merge main" origin/main 2>&1 | tail -1
check "P18 merge commit in range, exit" 0 "$(run "$T/o18" bash "$S" --no-preflight origin/main)"
has   "P18 WARN merge commit" "$T/o18" "WARN  1 merge commit(s) in the range"
git remote add pts https://github.com/sarvalabs/moi-project.git
check "P19 Points remote with main as base, exit" 0 "$(run "$T/o19" bash "$S" --no-preflight origin/main)"
has   "P19 WARN Points deploys from feature/ci-cd" "$T/o19" "this looks like the Points Program repo"
git remote remove pts
git switch -q --detach origin/main
check "P20 detached HEAD, exit" 1 "$(run "$T/o20" bash "$S" --no-preflight origin/main)"
git switch -q fix/page
# bad input
mkdir -p "$T/notrepo"
check "P21 not a repository, exit" 2 "$( cd "$T/notrepo" && run "$T/o21" bash "$S" --no-preflight origin/main )"
check "P22 base that does not exist, exit" 2 "$(run "$T/o22" bash "$S" --no-preflight origin/nope)"
check "P23 unknown option, exit" 2 "$(run "$T/o23" bash "$S" --upload-pack=x)"
check "P24 two bases, exit" 2 "$(run "$T/o24" bash "$S" origin/main origin/main)"
check "P25 env-named base, exit" 2 "$(run "$T/o25" bash "$S" --no-preflight .env)"
has   "P25 placeholder printed" "$T/o25" "\[env-named file\]"
check "P26 secret-shaped base, exit" 2 "$(run "$T/o26" bash "$S" --no-preflight "ghp_$FILLER")"
hasnot "P26 filler never echoed" "$T/o26" "zqzqzq"
check "P27 base with a newline, exit" 2 "$(run "$T/o27" bash "$S" --no-preflight $'origin/main\nfoo')"
check "P28 --help, exit" 0 "$(run "$T/o28" bash "$S" --help)"
git init -q "$T/empty"; check "P29 unborn HEAD, exit" 2 "$( cd "$T/empty" && run "$T/o29" bash "$S" --no-preflight )"
check "P30 bare repository, exit" 2 "$( cd "$T/p-remote.git" && run "$T/o30" bash "$S" --no-preflight main )"
mkdir -p "$T/nopy" "$T/nogit"; ln -sf "$(command -v git)" "$T/nopy/git"; ln -sf "$(command -v python3)" "$T/nogit/python3"
check "P31 python3 missing from PATH, exit" 2 "$(PATH="$T/nopy:/bin:/usr/bin" run "$T/o31" /bin/bash -c 'PATH="'"$T"'/nopy"; /bin/bash "'"$S"'" origin/main')"
check "P32 git missing from PATH, exit" 2 "$(run "$T/o32" /bin/bash -c 'PATH="'"$T"'/nogit"; /bin/bash "'"$S"'" origin/main')"
mkdir -p "$T/lonely/moi-devrel/ship"; cp -R "$SKILLS/moi-devrel/ship/scripts" "$T/lonely/moi-devrel/ship/"
check "P33 moi-devrel/scripts not three folders up, SKILLS unset, exit" 1 "$(run "$T/o33" env -u SKILLS bash "$T/lonely/moi-devrel/ship/scripts/ship-preflight.sh" origin/main)"
has   "P33 FAIL says where to look" "$T/o33" "FAIL  moi-devrel preflight.sh was not found"
check "P33b the same copy with SKILLS set to the real folder, exit" 0 "$(run "$T/o33b" env SKILLS="$SKILLS" bash "$T/lonely/moi-devrel/ship/scripts/ship-preflight.sh" origin/main)"
has   "P33b SKILLS was preferred, preflight ran" "$T/o33b" "preflight.sh reported no FAIL"
mkdir -p "$T/my skills/moi-devrel"; cp -R "$SKILLS/moi-devrel/scripts" "$SKILLS/moi-devrel/ship" "$T/my skills/moi-devrel/"
check "P34 folder name with a space, SKILLS unset (own location), exit" 0 "$(run "$T/o34" env -u SKILLS bash "$T/my skills/moi-devrel/ship/scripts/ship-preflight.sh" origin/main)"
has   "P34 preflight ran" "$T/o34" "preflight.sh reported no FAIL"
check "P34b SKILLS path with a space, exit" 0 "$(run "$T/o34b" env SKILLS="$T/my skills" bash "$T/my skills/moi-devrel/ship/scripts/ship-preflight.sh" origin/main)"
has   "P34b preflight ran" "$T/o34b" "preflight.sh reported no FAIL"
# read-only proof
mtime() { stat -f %m "$1" 2>/dev/null || stat -c %Y "$1"; }
snap() { git for-each-ref | cksum; git count-objects -v | cksum; git status --porcelain | cksum; mtime .git/index; git stash list | cksum; }
A="$(snap)"; bash "$S" --no-preflight origin/main >/dev/null 2>&1; B="$(snap)"
check "P35 read-only: refs, objects, status, index mtime, stash unchanged" "$A" "$B"

echo "=== rebase-proof.sh"
mkrepo r; cd "$T/r"
git switch -q --no-track -c fix/topic origin/main; printf 'page-topic\n' > page.md; git commit -qam "topic: page"; printf 'new\n' > new.md; git add new.md; git commit -q -m "topic: new file"
git clone -q "$T/r-remote.git" "$T/r-mate" 2>/dev/null
( cd "$T/r-mate" && git config user.name M && git config user.email m@example.org && printf 'o1\no2-BASE\no3\n' > other.md && printf 'a3\n' > a.txt && git commit -qam "base: move" && git push -q origin main )
git fetch -q origin; BK=backup/fix-topic-before-rebase-2026-10-03
git branch "$BK" fix/topic; git rebase origin/main >/dev/null 2>&1
check "R01 clean rebase, exit" 0 "$(run "$T/r01" bash "$RP" "$BK" fix/topic origin/main)"
has   "R01 SAME" "$T/r01" "^SAME:"
OBJ1="$(git count-objects -v | cksum)"; bash "$RP" "$BK" fix/topic origin/main >/dev/null 2>&1; OBJ2="$(git count-objects -v | cksum)"
check "R02 read-only: object store unchanged after a run" "$OBJ1" "$OBJ2"
git switch -q -c t/drop fix/topic; git rm -q new.md; git commit -qm "oops drop"
check "R03 dropped file, exit" 1 "$(run "$T/r03" bash "$RP" "$BK" t/drop origin/main)"
has   "R03 DIFFERENT lists D new.md" "$T/r03" "D  new.md"
git switch -q -c t/stale fix/topic; git show "origin/main~1:other.md" > other.md; git commit -qam "stale other"
check "R04 stale copy of a base-updated file, exit" 1 "$(run "$T/r04" bash "$RP" "$BK" t/stale origin/main)"
has   "R04 DIFFERENT lists M other.md" "$T/r04" "M  other.md"
git switch -q -c t/extra fix/topic; printf x > extra.md; git add extra.md; git commit -qm extra
check "R05 extra file, exit" 1 "$(run "$T/r05" bash "$RP" "$BK" t/extra origin/main)"
has   "R05 DIFFERENT lists A extra.md" "$T/r05" "A  extra.md"
check "R06 backup is the rebased ref (not on the new base), exit" 1 "$(run "$T/r06" bash "$RP" "$BK" "$BK" origin/main)"
has   "R06 NOT ON THE NEW BASE" "$T/r06" "NOT ON THE NEW BASE"
# conflict resolved by hand
git switch -q -c t/c1 "$(git merge-base origin/main "$BK")"; printf 'o1\no2-TOPIC\no3\n' > other.md; git commit -qam "topic: other"; git branch backup/c1 t/c1
git rebase origin/main >/dev/null 2>&1; printf 'o1\no2-BOTH\no3\n' > other.md; git add other.md; GIT_EDITOR=true git rebase --continue >/dev/null 2>&1
check "R07 conflict resolved by hand, exit" 1 "$(run "$T/r07" bash "$RP" backup/c1 t/c1 origin/main)"
has   "R07 UNPROVEN lists C other.md" "$T/r07" "C  other.md"
check "R08 no arguments, exit" 2 "$(run "$T/r08" bash "$RP")"
check "R09 two arguments, exit" 2 "$(run "$T/r09" bash "$RP" a b)"
check "R10 unknown ref, exit" 2 "$(run "$T/r10" bash "$RP" nope fix/topic origin/main)"
check "R11 option-looking ref, exit" 2 "$(run "$T/r11" bash "$RP" --upload-pack=x fix/topic origin/main)"
check "R12 env-named ref, exit" 2 "$(run "$T/r12" bash "$RP" .env fix/topic origin/main)"
check "R13 secret-shaped ref, exit" 2 "$(run "$T/r13" bash "$RP" "ghp_$FILLER" fix/topic origin/main)"
hasnot "R13 filler never echoed" "$T/r13" "zqzqzq"
check "R14 not inside a repository, exit" 2 "$( cd "$T/notrepo" && run "$T/r14" bash "$RP" a b c )"
git init -q "$T/unrel"; ( cd "$T/unrel" && git config user.name x && git config user.email x@example.org && printf u > u.txt && git add u.txt && git commit -qm u && git branch -m umain && git fetch -q "$T/r" fix/topic:rtopic )
check "R15 no common history, exit" 2 "$( cd "$T/unrel" && run "$T/r15" bash "$RP" rtopic rtopic umain )"
git switch -q -c t/envf fix/topic; printf 'K=1\n' > .env.prod; git add -f .env.prod; git commit -qm env
check "R16 env-named file in the difference, exit" 1 "$(run "$T/r16" bash "$RP" "$BK" t/envf origin/main)"
has   "R16 placeholder printed" "$T/r16" "A  \[env-named file\]"
hasnot "R16 real name not printed" "$T/r16" "env.prod"
git switch -q -c t/sec fix/topic; printf x > "ghp_$FILLER.txt"; git add .; git commit -qm sec
check "R17 secret-shaped file name in the difference, exit" 1 "$(run "$T/r17" bash "$RP" "$BK" t/sec origin/main)"
hasnot "R17 filler never echoed" "$T/r17" "zqzqzq"
if command -v zsh >/dev/null 2>&1; then check "R18 same run under zsh, exit" 0 "$(run "$T/r18" zsh "$RP" "$BK" fix/topic origin/main)"; fi
check "R19 python3 missing from PATH, exit" 2 "$(run "$T/r19" /bin/bash -c 'PATH="'"$T"'/nopy"; /bin/bash "'"$RP"'" a b c')"
check "R20 -h, exit" 0 "$(run "$T/r20" bash "$RP" -h)"

echo "=== strip-ai-lines.awk"
a() { printf "$1" | awk -f "$AWKF" | tr '\n' '|'; }
check "A01 Claude trailer removed with its blank line" 'docs: x||Body.|' "$(a 'docs: x\n\nBody.\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\n')"  # slop-lint:ignore
check "A02 human trailer kept, Copilot trailer removed" 'docs: x||Body.||Co-authored-by: Real Person <real@example.org>|' "$(a 'docs: x\n\nBody.\n\nCo-authored-by: Real Person <real@example.org>\nCo-authored-by: Copilot <copilot@users.noreply.github.com>\n')"  # slop-lint:ignore
check "A03 generated-with footer removed" 'docs: x||Body line.|' "$(a 'docs: x\n\nBody line.\n\n\xf0\x9f\xa4\x96 Generated with [Claude Code](https://claude.com/claude-code)\n')"  # slop-lint:ignore
check "A04 generated-by Cursor removed, later text kept" 'docs: x||Later paragraph kept.|' "$(a 'docs: x\n\nGenerated by Cursor\n\nLater paragraph kept.\n')"
check "A05 a message that only names a product is untouched" 'docs: y||Uses the OpenAI SDK.|' "$(a 'docs: y\n\nUses the OpenAI SDK.\n')"
check "A06 empty input gives empty output" 0 "$(printf '' | awk -f "$AWKF" | wc -c | tr -d ' ')"

echo "=== sequences on a scratch repository"
mkrepo q; cd "$T/q"
# branch creation
git switch -q -c t/track1 origin/main; U1="$(git rev-parse --abbrev-ref '@{upstream}' 2>&1)"; git switch -q main
git switch -q --no-track -c t/track2 origin/main; U2="$(git rev-parse --abbrev-ref '@{upstream}' 2>&1 | head -1 | cut -c1-20)"; git switch -q main
check "Q01 without --no-track the upstream is the base" "origin/main" "$U1"
check "Q02 with --no-track there is no upstream" "fatal: no upstream c" "$U2"
mkdir -p ledger-x; printf 'l\n' > ledger-x/ledger.csv; printf '*\n' > ledger-x/.gitignore; git add -A; N1="$(git status --short | wc -l | tr -d ' ')"; git reset -q; rm -rf ledger-x
check "Q03 folder with a .gitignore holding * stages nothing" 0 "$N1"
mkdir -p review-pkg; printf 'n\n' > review-pkg/n.md; printf 'review-pkg/\n' >> .git/info/exclude; git add -A; N2="$(git status --short | wc -l | tr -d ' ')"; git reset -q; rm -rf review-pkg; sed -i.bak '/review-pkg/d' .git/info/exclude; rm -f .git/info/exclude.bak
check "Q04 .git/info/exclude stages nothing" 0 "$N2"
# trailer removal on a branch that is already pushed
git switch -q --no-track -c geo/fixes origin/main
printf 'one\n' > f1.md; git add f1.md; git commit -q -m "docs: one" -m "Body line." -m "Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"  # slop-lint:ignore
printf 'two\n' > f2.md; git add f2.md; git commit -q -m "docs: two" -m "Body two." -m "Co-authored-by: Real Person <real@example.org>  # slop-lint:ignore
Co-Authored-By: Claude <noreply@anthropic.com>"  # slop-lint:ignore
printf 'three\n' > f3.md; git add f3.md; git commit -q -m "docs: three" -m "$(printf '\xf0\x9f\xa4\x96 Generated with [Claude Code](https://claude.com/claude-code)')"  # slop-lint:ignore
printf 'four\n' > f4.md; git add f4.md; git commit -q -m "docs: four (no trailer)"
git push -q -u origin geo/fixes 2>/dev/null; git fetch -q origin
BR=geo/fixes; BASEREF=origin/main; BASE="$(git merge-base $BASEREF $BR)"; B="backup/$BR-before-rewrite-2026-10-03"; LAST_SEEN="$(git rev-parse origin/$BR)"
check "Q05 preflight sees 3 of 4 commits with an AI line" 1 "$(run "$T/q05" bash "$S" --no-preflight origin/main)"
has   "Q05 FAIL names 3 of 4" "$T/q05" "3 of 4 commit(s) carry an AI co-author trailer"
git branch "$B" "$BR"; export AWKFILE="$AWKF"
git switch -q "$BR"
FILTER_BRANCH_SQUELCH_WARNING=1 git filter-branch -f --msg-filter 'awk -f "$AWKFILE"' -- "$BASE"..HEAD >/dev/null 2>&1
check "Q06 filter-branch leaves refs/original" 1 "$(git for-each-ref refs/original | wc -l | tr -d ' ')"
git update-ref -d "refs/original/refs/heads/$BR"
check "Q07 refs/original removed" 0 "$(git for-each-ref refs/original | wc -l | tr -d ' ')"
check "Q08 tree equal to the backup" "$(git rev-parse "$B^{tree}")" "$(git rev-parse 'HEAD^{tree}')"
F='%an|%ae|%aI|%cn|%ce|%cI|%s'
check "Q09 authors, dates, subjects equal" "$(git log --format="$F" $BASE..$B)" "$(git log --format="$F" $BASE..HEAD)"
check "Q10 no AI line left in the range" 0 "$(git log --format=%B $BASE..HEAD | grep -ciE 'co-authored-by:.*(claude|anthropic|copilot|chatgpt|openai|codex|gemini|cursor)|generated (with|by).*(claude|anthropic|copilot|chatgpt|openai|codex|gemini|cursor)')"  # slop-lint:ignore
check "Q11 human co-author kept" 1 "$(git log --format=%B $BASE..HEAD | grep -c 'Real Person')"
check "Q12 rebase-proof says SAME for the rewrite, exit" 0 "$(run "$T/q12" bash "$RP" "$B" "$BR" "$BASEREF")"
check "Q13 range-diff: 3 commits changed, 1 equal" "3 1" "$(git range-diff $BASE..$B $BASE..HEAD | grep -E '^[0-9]+:' | awk '{ if ($3=="!") c++; else if ($3=="=") e++ } END { print c, e }')"
check "Q14 preflight passes the AI check after the rewrite, exit" 0 "$(run "$T/q14" bash "$S" --no-preflight origin/main)"
has   "Q14 PASS no AI line" "$T/q14" "PASS  no AI co-author trailer"
check "Q15 a plain push is refused" 1 "$(git push origin $BR >/dev/null 2>&1; echo $?)"
check "Q16 pinned lease push (full commit) is accepted" 0 "$(git push --force-with-lease=$BR:$LAST_SEEN origin $BR >/dev/null 2>&1; echo $?)"
check "Q17 read-back: remote equals local" "$(git rev-parse HEAD)" "$(git ls-remote origin refs/heads/$BR | cut -f1)"
# teammate pushes, then we fetch: bare lease vs pinned
git clone -q "$T/q-remote.git" "$T/q-mate" 2>/dev/null
( cd "$T/q-mate" && git config user.name M && git config user.email m@example.org && git switch -q $BR && printf m > m.md && git add m.md && git commit -q -m mate && git push -q origin $BR )
PIN="$(git rev-parse --short=12 HEAD)"; git commit -q --allow-empty -m "my rewrite tip"
check "Q18 pinned (12 characters) refused before any fetch" 1 "$(git push --force-with-lease=$BR:$PIN origin $BR >/dev/null 2>&1; echo $?)"
git fetch -q origin
check "Q19 after a fetch the bare lease would force over the teammate" "forced update" "$(git push --dry-run --force-with-lease origin $BR 2>&1 | grep -o 'forced update')"
check "Q20 after a fetch the pinned lease is still refused" "stale info" "$(git push --dry-run --force-with-lease=$BR:$PIN origin $BR 2>&1 | grep -o 'stale info')"
RT="$(git ls-remote origin refs/heads/$BR | cut -f1)"
check "Q20b a 12-character pin of the real remote tip is accepted" 0 "$(git push --force-with-lease=$BR:$(echo $RT | cut -c1-12) origin $BR >/dev/null 2>&1; echo $?)"
# relabel and drop
git reset -q --hard HEAD~1; git switch -q -c relabel $BR
printf 'five\n' > f5.md; git add f5.md; GIT_AUTHOR_DATE="2026-10-01T10:00:00+0000" GIT_COMMITTER_DATE="2026-10-01T10:00:00+0000" git -c user.email=someone@gmail.com -c user.name="Personal Handle" commit -q -m "docs: five"
printf 'six\n' > f6.md; git add f6.md; git commit -q -m "docs: six (work)"
BR=relabel; BASE="$(git merge-base $BASEREF $BR)"; B="backup/$BR-before-rewrite-2026-10-03"; git branch "$B" "$BR"
printf 'dirty\n' >> a.txt; MSG="$(FILTER_BRANCH_SQUELCH_WARNING=1 git filter-branch -f --env-filter 'true' -- "$BASE"..HEAD 2>&1 | tail -1)"; git checkout -q -- a.txt
check "Q21 filter-branch refuses a dirty tree" "Cannot rewrite branches: You have unstaged changes." "$MSG"
export OLD_EMAIL="someone@gmail.com" NEW_NAME="$(git config user.name)" NEW_EMAIL="$(git config user.email)"
FILTER_BRANCH_SQUELCH_WARNING=1 git filter-branch -f --env-filter '
if [ "$GIT_AUTHOR_EMAIL" = "$OLD_EMAIL" ]; then export GIT_AUTHOR_NAME="$NEW_NAME"; export GIT_AUTHOR_EMAIL="$NEW_EMAIL"; fi
if [ "$GIT_COMMITTER_EMAIL" = "$OLD_EMAIL" ]; then export GIT_COMMITTER_NAME="$NEW_NAME"; export GIT_COMMITTER_EMAIL="$NEW_EMAIL"; fi
' -- "$BASE"..HEAD >/dev/null 2>&1; git update-ref -d "refs/original/refs/heads/$BR"
check "Q22 old address gone from the range" 0 "$(git log --format='%ae%n%ce' $BASE..HEAD | grep -c gmail)"
check "Q23 tree equal after relabel" "$(git rev-parse "$B^{tree}")" "$(git rev-parse 'HEAD^{tree}')"
F2='%aI|%cI|%s'
check "Q24 dates and subjects equal after relabel" "$(git log --format="$F2" $BASE..$B)" "$(git log --format="$F2" $BASE..HEAD)"
export DROP_PATH="f5.md"
FILTER_BRANCH_SQUELCH_WARNING=1 git filter-branch -f --index-filter 'git rm --cached --ignore-unmatch -q -- "$DROP_PATH"' --prune-empty -- "$BASE"..HEAD >/dev/null 2>&1; git update-ref -d "refs/original/refs/heads/$BR"
check "Q25 no commit touches the dropped file" 0 "$(git log --format=%H $BASE..HEAD -- "$DROP_PATH" | wc -l | tr -d ' ')"
check "Q26 the only difference from the backup is that file" "D	f5.md" "$(git diff --name-status $B HEAD)"
# squash-merge then --onto
mkrepo s; cd "$T/s"
git switch -q --no-track -c layer1 origin/main; printf '1\n' > l1.txt; git add l1.txt; git commit -q -m "l1 a"; printf '1b\n' >> l1.txt; git commit -qam "l1 b"
git switch -q -c layer2 layer1; printf '2\n' > l2.txt; git add l2.txt; git commit -q -m "l2"
git switch -q main; git merge -q --squash layer1 >/dev/null 2>&1; git commit -qm "squash: layer1 (#1)"; git push -q origin main; git fetch -q origin
OLDTIP="$(git rev-parse layer1)"; git switch -q layer2; git branch backup/layer2-before-rebase-2026-10-03 layer2
git rebase origin/main >"$T/s-plain" 2>&1; PLAIN=$?; git rebase --abort 2>/dev/null
check "Q27 plain rebase after a squash merge stops on a conflict" 1 "$PLAIN"
git rebase --onto origin/main "$OLDTIP" layer2 >/dev/null 2>&1
check "Q28 --onto replays only the layer's own commit" 1 "$(git rev-list --count origin/main..layer2)"
check "Q29 rebase-proof says SAME after --onto, exit" 0 "$(run "$T/q29" bash "$RP" backup/layer2-before-rebase-2026-10-03 layer2 origin/main)"
# stack tree equality
git switch -q -c original origin/main~1; printf '1\n1b\n' > l1.txt; printf '2\n' > l2.txt; git add .; git commit -qm orig
git switch -q -c L1 origin/main~1; git checkout -q original -- l1.txt; git commit -qm L1; git switch -q -c L2 L1; git checkout -q original -- l2.txt; git commit -qm L2
check "Q30 three-layer stack: top tree equals the original" "$(git rev-parse 'original^{tree}')" "$(git rev-parse 'L2^{tree}')"
git switch -q -c Lbad L1; git commit -q --allow-empty -m Lbad
check "Q31 a split that left a file out is named" "A	l2.txt" "$(git diff --name-status Lbad original)"
# merge versus squash revert
git switch -q main; git switch -q -c feat-x; printf x > x.txt; git add x.txt; git commit -qm x; git switch -q main; git merge -q --no-ff -m "Merge pull request #9 from org/feat-x" feat-x; M="$(git rev-parse HEAD)"
git revert --no-edit $M >/dev/null 2>&1; RV=$?; [ $RV -ne 0 ] && RV=nonzero
check "Q32 plain revert of a merge commit fails" nonzero "$RV"
check "Q33 revert -m 1 of a merge commit works" 0 "$(git revert --no-edit -m 1 $M >/dev/null 2>&1; echo $?)"
# read-only report loop, in bash and zsh
mkrepo u; cd "$T/u"
git switch -q --no-track -c b1 origin/main; printf 'x\n' > b1.txt; git add b1.txt; git commit -qm b1
git switch -q --no-track -c b2 origin/main; printf 'page-b2\n' > page.md; git commit -qam b2
git clone -q "$T/u-remote.git" "$T/u-mate" 2>/dev/null; ( cd "$T/u-mate" && git config user.name M && git config user.email m@example.org && printf 'page-base\n' > page.md && git commit -qam base && git push -q origin main ); git fetch -q origin
cat > "$T/report.sh" <<'EOS'
TMPO="$(mktemp -d)"
for b in b1 b2; do
  set -- $(git rev-list --left-right --count "origin/main...$b")
  if GIT_OBJECT_DIRECTORY="$TMPO" GIT_ALTERNATE_OBJECT_DIRECTORIES="$(git rev-parse --absolute-git-dir)/objects" git merge-tree --write-tree "origin/main" "$b" >/dev/null 2>&1; then c=clean; else c=CONFLICT; fi
  echo "$b behind=$1 ahead=$2 merge=$c"
done
rm -rf "$TMPO"
EOS
O1="$(git count-objects -v | cksum)"
check "Q34 report loop in bash" "b1 behind=1 ahead=1 merge=clean b2 behind=1 ahead=1 merge=CONFLICT" "$(bash "$T/report.sh" | tr '\n' ' ' | sed 's/ $//')"
if command -v zsh >/dev/null 2>&1; then check "Q35 report loop in zsh" "b1 behind=1 ahead=1 merge=clean b2 behind=1 ahead=1 merge=CONFLICT" "$(zsh "$T/report.sh" | tr '\n' ' ' | sed 's/ $//')"; fi
check "Q36 report loop writes no object to the repository" "$O1" "$(git count-objects -v | cksum)"
# staged push with a pause
for n in 1 2 3; do git switch -q --no-track -c "stage/$n" origin/main; printf "$n" > "s$n.txt"; git add "s$n.txt"; git commit -q -m "stage $n"; done
OUT=""; for n in 1 2 3; do git push -q -u origin "stage/$n" 2>/dev/null; sleep 1; OUT="$OUT$(git ls-remote origin refs/heads/stage/$n | cut -f1 | cut -c1-7)=$(git rev-parse --short=7 stage/$n) "; done
SAME=1; for n in 1 2 3; do [ "$(git ls-remote origin refs/heads/stage/$n | cut -f1)" = "$(git rev-parse stage/$n)" ] || SAME=0; done
check "Q37 staged push of three branches in order, each read back" 1 "$SAME"
echo "---"
echo "checks ok: $PASS   not ok: $FAILN"
cd / || exit 2
if [ "$FAILN" -eq 0 ]; then rm -rf "$T"; echo "scratch folder removed"; exit 0; fi
echo "scratch folder kept: $T"
exit 1
