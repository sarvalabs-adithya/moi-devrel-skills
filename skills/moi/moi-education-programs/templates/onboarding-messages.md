# Onboarding message set (drafts; the operator sends)

Claude drafts these. The operator reads each one, fills the `{{...}}` fields and sends it. Claude never sends a message, never messages a student or a college, and never promises anything on MOI's behalf. Plain text for chat: no emoji, no em dashes, no bold markers. Write times as a date, 24-hour UTC and IST: `bash "$SKILLS/moi-devrel/scripts/time-table.sh" "{{YYYY-MM-DD HH:MM}}" Asia/Kolkata` (it reads the time as India time; give `UTC` as the zone if you decided it in UTC). Before sending, run `bash "$SKILLS/moi-devrel/scripts/slop-lint.sh" <file>` over the filled text and open every link by hand. Say "devnet", "KMOI" and "MOI Wallet". Quote no faucet amount. Mention no internship, job, prize or payment unless Rahul has approved that sentence in writing.

Source for the Week 1 steps: the Forge onboarding guide (Drive, and an uncommitted rewrite in the previous operator's clone of awesome-moi; not recorded (the previous DevRel's notes); ASK: Rahul). Its wallet name and network links are stale, so the steps below are rewritten (`references/forge-cohort.md`).

## 1. Invitation (via the campus contact)
Channel: email or the campus group. Send once the event is approved.
```
Subject: {{Event name}} on {{date}}

{{Campus}} students are invited to {{event name}}, a {{n}}-day build with MOI. You build a project on MOI that uses participant-centric state and submit it by {{date}} at {{HH:MM}} UTC ({{HH:MM}} IST). No earlier blockchain experience is needed.
The kickoff is on {{date}} at {{HH:MM}} UTC ({{HH:MM}} IST) on {{platform}}: {{link}}
Details and the rules: {{README link}}
Questions go to {{channel}}.
```

## 2. Welcome and first steps (after sign-up)
```
Welcome to {{event or cohort}}. Do these before the kickoff:
1. Join {{channel}} and say hello. Announcements are also on {{Telegram or other}}.
2. Fill in {{onboarding form}}.
3. Install Node.js ({{version}}), npm and the Coco compiler from {{install link}}. Check with: node --version, then coco version.
4. Install the MOI Wallet extension and create your wallet. Write down your recovery phrase on paper. It is the only key to your wallet. Keep it in a gitignored .env file on your own machine. Never put it in a website, a form, a chat, a repository or a recorded call. Nobody from MOI will ask for it.
5. Register your wallet on chain: {{current step, ASK: Gokul}}. The faucet only funds accounts that already exist. Then get devnet funds from the Voyage faucet: {{link}}, and find your account on voyage.moi.technology. The explorer can take a few minutes to show it.
6. Run the devnet check and send us the output if it fails: {{the net.Version command from references/students.md}}
```

## 3. Kickoff reminder (the day before, and 30 minutes before)
```
{{Event name}} kicks off on {{date}} at {{HH:MM}} UTC ({{HH:MM}} IST) on {{platform}}: {{link}}. Have your wallet funded and your tools installed. We will say the recovery-phrase rule at the start.
```
Keep the date in the text. "Today" and "tomorrow" go stale in anything scheduled or recorded.

## 4. After the kickoff
```
Thanks for joining. The brief and the tracks are here: {{README link}}. Help is in {{channel}}. Office hours: {{exactly as they will be kept}}. Submissions are due {{date}} at {{HH:MM}} UTC ({{HH:MM}} IST) through {{form link}}.
```

## 5. Mid-way check-in
```
Halfway through. If you are stuck, ask in {{channel}} with your error message and what you ran. Never paste your recovery phrase. If your deployed assets or logics have disappeared, devnet may have been reset: tell us, and redeploy with your scripts.
```
If a reset happened, say what was wiped and the date (`moi-devrel/references/devnet.md`). Do not invent a cause.

## 6. Deadline reminder (24 hours before)
```
Submissions close {{date}} at {{HH:MM}} UTC ({{HH:MM}} IST). Your repository must be public and hold the Coco logic files and a README. Add a video of at most 2 minutes. Submit once per team through {{form link}}. {{Late rule decided with Rahul.}}
```

## 7. Submission received
```
We have your submission for {{team name}}. We will tell you the result by {{date, only if decided}}.
```

## 8. Result and thanks
```
Thank you to everyone who built. {{Result sentence approved by Rahul.}} {{Next step for the cohort, only if approved.}}
```
No sentence about jobs, internships, prizes or grants unless the approved text says so.

## 9. Mentor briefing
```
You are a mentor for {{event}}. The channel is {{channel}} and office hours are {{exactly as kept}}. Rules: answer in the channel, not in private messages, where you can. Never ask a student for a recovery phrase, and if one is pasted, tell the student at once to stop using that wallet. Promise nothing about jobs, internships or prizes. If devnet looks reset, tell {{operator name}}.
```

## 10. Faculty contact (the operator sends; terms are Rahul's)
```
Dear {{name}}, thank you for hosting {{event}} at {{campus}}. The dates are {{dates}}. We need {{room or platform}} and a way to reach the students: {{what}}. Please send questions to {{operator contact}}.
```
Any agreement, fee, data sharing or certificate is outside this draft. ASK: Rahul.

## 11. A student pasted a recovery phrase
Reply in the channel without repeating the phrase:
```
That looks like a recovery phrase. Treat that wallet as exposed: stop using it and make a new one in the MOI Wallet extension. Please delete your message. Keep the new phrase on paper and in a gitignored .env file only.
```
Deleting the message is a moderator action on that server: the operator or a server admin does it.
