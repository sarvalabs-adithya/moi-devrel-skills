# awesome-moi: list entry format and pull request skeleton

For `moi-foundation/awesome-moi`. The only rule the repo states is "Fork the repo, add your resource, and submit a PR" with these fields: name, short description, link, category (Paper, Network, Community). Everything else below is proposed (`references/awesome-moi.md`, "What belongs"). Confirm with Rahul. Opening a pull request, pushing and merging are each a GATE, and a merge publishes the list.

## The entry
One line in the section's list. This is the shape the repo already uses in `essentials/README.md`:
```
- **[Name](https://canonical.address/path)** - One sentence that says what it is.
```
| Field | Rule |
|---|---|
| Name | The project's own name, spelled as it spells itself. "js-moi-sdk" is always lowercase. "Coco" is the language, and "Coco (also known as Cocolang)" on first mention in a file |
| Link | The canonical address. No tracking query, no redirect when a final address exists. Opened by hand. Passes `python3 "$SKILLS/moi-education-programs/scripts/link-check.py" <file.md>` |
| Description | One sentence, plain words, what it is and who it is for. No claim about speed, price, partners or "first". No metaphor. Participant-centric wording. "Devnet", never "testnet". No faucet amount. A figure goes through `moi-devrel/claim-check` |
| Category | A section that exists: Essentials (Paper, Network, Community), JS SDK, Coco, Developer Tools. A new section needs Rahul's yes |
| Not allowed | A private repository, a login wall, a devnet id or asset id that a reset kills, a promotional post, "Coming Soon" without a date |

## Removing a stale entry
Delete the line and say why in the pull request: the address, the date it failed and what was tried (`link-check.py` output, the replacement if one exists).

## The pull request description
No AI co-author line and no "generated with" footer (house rule 4). Work identity only: `bash "$SKILLS/moi-devrel/scripts/preflight.sh"` before the commit. One pull request per review, with every fix on one branch.
```
## What changed
- {{Added / removed / fixed}}: {{entry or file}}

## Checks run
- Link check on {{files}} on {{YYYY-MM-DD}}: {{n}} links, {{n}} dead, {{n}} redirected, {{n}} opened by hand.
- Wording lint on {{files}}: {{0 errors}}.
- For a repository: public, {{licence}}, last commit {{date}}, runs on devnet with js-moi-sdk {{version}} and Coco {{version}} on {{date}}.
- For a tutorial: followed once on devnet on {{date}}.

## Not checked
- {{Anything not opened or run, and why}}
```
