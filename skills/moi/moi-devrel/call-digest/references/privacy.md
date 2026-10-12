# Privacy: what a transcript can contain that must not be repeated or stored

Facts are as of 2026-10-03. The rules come from `moi-devrel/references/consent-and-identity.md` (sections 4 and 5), applied to transcripts. "The operator" is the human working with Claude now. Back to `../GUIDE.md`.

## 1. Why this file exists
A recorded call keeps whatever is said aloud. On 2026-09-24 the confirmation words of a wallet recovery phrase were requested on a screen share, during a Launchpad onboarding walkthrough, and the Gemini notes of that meeting captured them. The notes document holds words that can unlock a wallet, and the recording may hold them too. Treat any phrase ever read on a recorded call as exposed. Claude never handles a recovery phrase, including a throwaway one, and never repeats one.

The rule has two halves. During a call, nobody reads, shows or confirms recovery words. After a call, the digest holds none of them, and says where they were.

## 2. What a transcript can hold, and what to do
| It holds | Record of it | What you do |
|---|---|---|
| Recovery-phrase words: a whole phrase, words one at a time, or confirmation words by position ("word number three") | 2026-09-24, Gemini notes of a screen-shared wallet setup | Do not copy, quote or summarise them. The script masks the shapes it knows. Say where they are and that the wallet is exposed (section 3a) |
| A key, token, password or webhook URL said aloud or typed on a shared screen | Gemini notes can capture secrets read aloud. Separately, keys and bot tokens were pasted into chat on several days between 2026-06 and 2026-09 | Same. Name the kind and the line, never the value (section 3b) |
| Personal contact details of attendees: personal email addresses, phone numbers | The Gemini notes of the Presidency Forge kickoff list dozens of invitees by personal email | The clean copy masks personal-provider emails and phone numbers. The digest names no one by email or phone (section 3c) |
| Names of students, guests and audience members | Forge calls and the public community call have outside attendees | Use "a student" or "an attendee" unless the work needs the name. Keep a name out of any text that may be shared |
| A security finding about a live product | Not recorded in this library, on purpose | Write only the sentence in section 3d. Add no detail of any kind |
| Private source paths, unmerged features, cancelled sessions, reviewer names, internal opinions | Public text leaks are a recorded failure (`moi-devrel/SKILL.md` fact 7) | The digest is internal. Mark such lines `internal`. They must not reach public text without `moi-devrel/claim-check` and the operator's yes |
| A wallet address, a hash or an asset id | Public on chain, but the clean copy masks any hex string of 24 or more characters, because a private key has the same shape | If the call named one you need, ask the operator to read it from the original and check it on the explorer |

## 3. What to tell the operator
Tell them as soon as the script exits 1 or you meet one by reading. Use the operator's words, plain and short. Do not repeat the value.

a. A recovery phrase shape.
"The transcript has what looks like recovery words at lines 212 to 224. I have not copied them and the clean copy hides them. Treat that wallet as exposed and stop using it. The notes document holds them and the recording may. Deleting either is your own action in Drive, after you ask the file's owner. I do not delete anything. ASK: Rahul who owns the info@ recordings."

b. A key, token or password.
"A <kind> is exposed in the transcript at line 40. I have not copied it. Treat it as exposed: the person who grants it should rotate or revoke it, and `moi-devrel/references/keys-and-access.md` says who that is." One exception: `AGENT_KEY_ENCRYPTION_SECRET` of the Launchpad is never rotated, because every stored agent key becomes unreadable. ASK: Upendhar before anyone changes it.

c. Personal details.
"The notes list attendees by personal email and phone. The clean copy hides them and the digest names no one by contact detail. Do not forward the original."

d. A security finding.
If the product the call named is one that `moi-devrel/references/repo-map.md` marks, write exactly this in the digest, with the product's name before it: "A security finding is open on this product as of 2026-10-02. ASK: Adithya for the handover note before touching its admin." For any other product, write no sentence: give only the line range and tell the operator in the conversation to ASK: Rahul who receives security reports. The only other thing the digest may hold is the line range of the clean copy where the talk sits. Nothing else about it goes in the digest, the chat or a message. If the operator asks what was said, point to those lines and let them read them; do not summarise them.

e. Something you cannot tell.
"I could not tell whether the screen share showed a wallet setup. Please check lines 300 to 340 of the original yourself."

## 4. Where transcripts and copies live
1. In the self-ignoring digest folder (`printf '*\n' > <folder>/.gitignore`). On 2026-06-08 a call transcript was committed and had to be scrubbed from history. The folder is created per call, in the working copy where the follow-up work will happen, and nothing in it is committed. `moi-foundation/MOI-Webinars` is public, so a push there publishes. That repo's ignore file lists the folder `otter-transcript/` and a few named files of session 7 (read on `origin/main`, which matched GitHub's `main`, 2026-10-03). That covers those names in that repo and nothing else.
2. The original stays where it is. Claude reads the clean copy. The script writes the copy readable by its owner only.
3. A transcript or digest is never uploaded to Drive or other cloud storage, never pasted into another tool or a summarising service, and never sent as a message, without the operator's yes. Large transcripts are easy to paste into other tools. Prefer the Summary and Decisions blocks of Gemini notes for anything that must be pasted, and read them as leads.
4. Claude does not delete a transcript, a recording or a notes document. The clean copy and the report are the operator's to keep or remove. They are in the ignored folder.
5. Before the digest is shared, run `bash "$SKILLS/moi-devrel/scripts/secret-scan.sh" <digest>` and read it once for emails, phone numbers and names. The scan is a backstop. It knows common key shapes and phrases of 12 or more short words, and a clean result does not mean the file is safe to share.

## 5. When the operator pastes a transcript into the chat
1. Read it for the shapes in section 2 before you use it.
2. If it holds a secret or recovery words, do not repeat them, do not quote the line, and tell the operator it is exposed (section 3). Carry on with the rest of the text.
3. Do not save the pasted text to a file yourself. The script needs a file, so ask the operator to save the transcript into the digest folder and give the path. Until then work from the paste and mark the digest "no script pass".

## 6. What the script catches and what it misses
It masks these shapes:
- key and token prefixes (the same families as `secret-scan.sh`), JWTs, webhook URLs, bot tokens and private key headers;
- hex strings of 24 or more characters, and mixed letter and digit tokens of 24 or more characters;
- a secret-named assignment, and a spoken password that holds a digit;
- personal-provider email addresses and phone numbers (international, US and Indian shapes);
- recovery-phrase shapes: 12 or more short words in a run, also with list numbers between them ("1. word 2. word"), 12 or more one-word lines, the word after "word number three is", "the 5th word is" or "number 11 is", and, in the 25 lines after "seed phrase" or "recovery phrase" is mentioned, any line of up to 11 short words with no common English word.

The report prints a word of 12 or more characters that holds a digit as a placeholder, and any word of 20 or more characters as another, so a short unknown token is not echoed there.

It misses: a key or phrase spelled out letter by letter, a phrase said with common words between the recovery words, a value shown only on the shared screen (the transcript cannot see a screen), a secret in a recording, and any shape it does not know. A clean report is not proof. When the call included a wallet setup, a login or an `.env` on screen, read that stretch of the original yourself or ask the operator to.

The phrase rules assume the 2048-word BIP-39 English list that the MOI Wallet uses: words of 3 to 8 letters. A real phrase holds only those words, so a run that contains another common English word is treated as prose. If you add a word to `STOPWORDS` in `scripts/transcript-prep.py`, check it against that list first; "that", "this" and "right" are on it.

## Not yet known
- Who owns the recordings and notes in the shared Google accounts, and who may delete them. ASK: Rahul.
- Whether the recording of the 2026-09-24 walkthrough and its notes were removed. The research records only that the notes held the words. ASK: Adithya.
- Whether Otter or Zoom keep transcripts on their servers after export, and who can see them. ASK: Rahul who holds those accounts.
