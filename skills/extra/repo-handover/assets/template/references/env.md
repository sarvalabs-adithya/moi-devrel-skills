# Environment variables

## Where the values live

| Place | What it holds | Who can read it |
| --- | --- | --- |
| local `{{.env file}}` | dev values | you |
| {{CI secret store}} | production secrets | write-only |
| {{host env file / platform panel}} | production values as deployed | {{who}} |
| {{build image}} | anything baked in at build time | rebuild to change |

State plainly which copy is the only *readable* copy of production secrets.

## Required to boot

| Variable | What it does | Where to get it | Secret? | Rotate? |
| --- | --- | --- | --- | --- |
| `{{VAR}}` | {{purpose}} | {{dashboard path / command / person}} | yes/no | freely / with a step / never |

## Feature groups

Group the rest by what they unlock (delivery, model provider, payments, optional features). For each optional group say what happens when it is unset.

## Not server config

Variables read by scripts or client runtimes, so nobody hunts for them on the server.

## What to hand over in person

Three lists: readable now and where; safe to rotate instead; request from the owning team rather than copy.
