# The guest speaker slide

Read this when a deck introduces a guest: the monthly community call, or any session with an outside speaker. The component is in `templates/template.html` (classes `guest`, `gshot`, `gname`, `grole`, `gco`, `glogo`, `gtopic`, `slot`), so every deck made with `new-deck.sh` has it. A worked example is slide 12 of `moi-webinar/community-call/examples/cc14/deck/index-guest.html`. Back to `../GUIDE.md`.

## What it looks like

The headshot is the dominant element: a 720 by 720 rounded square on the left, top-aligned with the pad, with the house glow (soft lavender halo, `0 0 80px rgba(152,113,242,.30)`). Beside it, top-aligned too: the "Guest speaker" chip, the name at 96px, the role on one line, the company on the next, the company logo on a white plate, and the talk topic under a "Talking about" kicker. It replaces the CC14 draft slide (24 September 2026), a stack of name, a small logo, a sentence about the company, a 380px photo and a hand-over line, which the previous operator rejected on 9 October 2026 as needing "a nice big photo" with the role, company and a logo placeholder.

It works on `dark grad` (the default, the photo glows most there), `light` and `lav`. Pick the background the alternation needs (check d).

## What to ask the host or the guest for

Ask once, in one message (`moi-webinar/community-call/templates/input-request-messages.md`, message 7).

| Field | Where it goes | File and size | If it has not arrived |
| --- | --- | --- | --- |
| Headshot | `deck/assets/guest/headshot.jpg` | Square, at least 1200 by 1200 px, face centred, head and shoulders. JPG, PNG or WebP all work; rename the file or change the `src` | The frame shows a silhouette, the file name and the size wanted |
| Company logo | `deck/assets/guest/logo.svg` | A wordmark: SVG, or PNG with a transparent background, at least 600 by 200 px. A square mark: at least 400 by 400 px, and add `mark` to the slot | The plate shows the file name and the size wanted |
| Name | `gname` | As the guest writes it | Do not build the slide without it |
| Role | `grole` | As the guest writes it | A dashed `slot` reading "role, as the guest writes it" |
| Company | `gco` | As the guest writes it | Ask; never take it from a profile without the guest's yes |
| Topic | `gtopic .t` | One line in the guest's words, two at most | A dashed `slot` |

Never guess a role or a topic (rule 1 in `rules.md`; CC14's guest had no title on record, so it was left off). A logo the guest does not send is downloaded only with the operator's yes (`build.md`, "Photos and logos").

## Markup

Copy this, then change the background, the badge and the four text fields. The file names stay the same in every deck, so the hand-back can say "drop the two files into `deck/assets/guest/`".

```html
<section class="slide dark grad">
  <svg class="corner-logo"><use href="#moiOnDark"/></svg>
  <div class="pad">
    <div class="guest">
      <div class="gshot rv"><div class="frame">
        <div class="ph"><svg viewBox="0 0 120 120" fill="none" stroke="currentColor" stroke-width="3" aria-hidden="true"><circle cx="60" cy="44" r="22"/><path d="M18 112c4-24 22-38 42-38s38 14 42 38"/></svg><b>assets/guest/headshot.jpg</b>Square, 1200 &times; 1200 px or larger<br>Face centred, head and shoulders</div>
        <img src="assets/guest/headshot.jpg" alt="Guest name" onerror="this.remove()">
      </div></div>
      <div class="gtext">
        <div class="rv d1"><span class="chip">Guest speaker</span></div>
        <h2 class="gname rv d2">Guest Name</h2>
        <div class="grole rv d3"><span class="slot">role, as the guest writes it</span></div>
        <div class="gco rv d3">Company</div>
        <div class="glogo rv d4"><div class="ph"><b>assets/guest/logo.svg</b>SVG, or PNG on transparent<br>at least 600 &times; 200 px</div>
          <img src="assets/guest/logo.svg" alt="Company" onerror="this.remove()"></div>
        <div class="gtopic rv d5"><div class="k">Talking about</div><div class="t"><span class="slot">the talk in one line, in the guest's words</span></div></div>
      </div>
    </div>
  </div>
  <div class="slide-num">NN</div>
</section>
```

On a `light` or `lav` slide use `#moiOnLight` in the corner logo; the component restyles itself. When a text field arrives, replace the whole `<span class="slot">...</span>` with the plain text.

Options:
- **A square logo mark**: `<div class="glogo mark rv d4">` makes a 132 by 132 plate. Give its placeholder the short text `<b>assets/guest/<br>logo.svg</b>square mark<br>400 &times; 400 px`, or it will not fit.
- **A white logo made for dark backgrounds**: add `knock` to the slot (`glogo knock`) so the plate turns near-black once the image loads. Better: ask for the version for a light background.
- **The headshot crop**: the image fills the square and keeps the top third (`object-position:50% 30%`), which suits a head-and-shoulders photo. For a different framing, add `style="object-position:50% 50%"` to the `img`.

## How the empty state behaves

- Each frame shows its file name and the size wanted until the file exists. Once the image loads, the placeholder hides and the border turns solid. Check j of `check-deck.py` lists every missing file: put them in the hand-back.
- A slide with no files yet still looks deliberate in the browser and in the PDF. That is for drafts and review. Before the call, a text slot nobody filled is deleted, not left on screen: delete the `grole` line or the `gtopic` block. If the headshot has not arrived by the rehearsal, ask the operator whether to present the empty frame (rule 2 allows it) or cut the slide.
- `onerror="this.remove()"` is what makes a missing file fall back to the placeholder. Keep it on both images.

## Spacing

Measured on 2026-10-13 in Chrome on macOS, with Poppins loaded, on the 1920 by 1080 stage. The headshot runs from y=110 to y=830.

| Piece | Height |
| --- | --- |
| chip | 56, top at y=116 |
| name, per line | 100 (40 above it) |
| role, one line | 51 to 55 (26 above; a `slot` adds 10 below) |
| company, one line | 51 |
| logo plate | 132 (44 above) |
| topic block | 100 with one line, 147 with two (56 above) |

One-line name, one-line role and a two-line topic end at about y=833, level with the photo. A two-line name and a two-line topic end at y=925. Each further line adds about 51 (topic or role) or 100 (name), and content past y=990 enters the badge area (check o warns). So: a name of two lines at most, a role of one line, a topic of two lines. Shorten the topic before shrinking type.

## Not yet known

- Whether a guest gives written permission to show their photo on the recording and in the PDF. `moi-devrel/design/references/layout-and-backgrounds.md` asks for permission on record for identifiable people. ASK: Vardan, who arranges guests.
