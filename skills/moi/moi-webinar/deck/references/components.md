# Slide components

Read this when writing slides. Every block below is copy-paste markup that was rendered and checked against `templates/template.html` (as of 2026-10-02). Every slide is a `<section class="slide ...">` holding one `<div class="pad">`. The stage is a fixed 1920 by 1080 box that scales to the window, so the pixel numbers here are real pixels.

## Backgrounds

| Class | Looks like | Use for |
| --- | --- | --- |
| `slide light` | near-white lavender | most content slides |
| `slide lav` | pale lavender | alternate with `light` |
| `slide dark grad` | deep indigo gradient | cover, section breaks, the close |
| `slide dark` | flat near-black | rare, when a gradient fights an image |

No two neighbouring slides may share a background. `check-deck.py` fails check d if they do, and warns when `dark` meets `dark grad` because they look alike. Dark slides use the light logo `#moiOnDark`, light and lav slides use `#moiOnLight`. Repeat the pattern dark, light, dark, lav, light and the alternation takes care of itself.

## Skeleton (a content slide)

```html
<section class="slide light">
  <svg class="corner-logo"><use href="#moiOnLight"/></svg>
  <div class="pad">
    <div class="rv"><span class="chip">Section label</span></div>
    <h2 class="rv d1" style="margin-top:36px; font-size:76px">Title with an <span class="accent">accent</span>.</h2>
    <div class="rv d2 sub" style="margin-top:22px; max-width:1560px; font-size:30px">One line of context.</div>
    <!-- one component here -->
  </div>
  <div class="slide-num">04</div>
</section>
```

`rv` fades an element in and `d1` to `d5` stagger it. `slide-num` is the corner badge: two digits, equal to the page number, inside this section, absent on the cover and the close. One `accent` span per title.

## Cover and close

```html
<section class="slide dark grad">
  <div class="ghost-num">14</div>
  <div class="pad" style="justify-content:center">
    <svg class="rv" style="width:190px;height:auto;margin-bottom:70px" viewBox="0 0 26 20"><use href="#moiOnDark"/></svg>
    <div class="rv d1"><span class="chip">Series name &middot; Month Year</span></div>
    <h1 class="rv d2" style="margin-top:44px; max-width:1500px">Deck <span class="accent">title</span></h1>
    <div class="rv d3 sub" style="margin-top:36px; max-width:1400px">One line under the title.</div>
  </div>
</section>
```

`ghost-num` is the huge translucent numeral behind the cover (the community call used its call number). Delete it when the deck has no number. The close is the same shape with a smaller logo, a single `h2` and nothing else, and no badge:

```html
<section class="slide dark grad">
  <div class="pad" style="justify-content:center">
    <svg class="rv" style="width:150px;height:auto;margin-bottom:60px" viewBox="0 0 26 20"><use href="#moiOnDark"/></svg>
    <h2 class="rv d1" style="font-size:84px">Thanks for building <span class="accent">with us</span>.</h2>
  </div>
</section>
```

## Cards

Two or three, never more than four. Inside one card use `ul` or `d`, not both.

```html
<div class="cards" style="margin-top:48px">
  <div class="card rv d3"><div class="k">Kicker</div><div class="v">Card headline</div>
    <ul><li>Point one</li><li>Point two</li></ul></div>
  <div class="card rv d4"><div class="k">Kicker</div><div class="v">Card headline</div>
    <div class="d">A sentence or two instead of bullets.</div></div>
</div>
```

`cards tight` shrinks the padding when text is long. On a dark slide the cards restyle themselves.

## Stats

Three tiles, or four with `stats four`. `n` is the number, `l` the label. A long `n` such as a word needs `style="font-size:44px"`. An optional logo sits above the number.

```html
<div class="stats" style="margin-top:52px">
  <div class="stat rv d3"><div class="n">00</div><div class="l">label</div></div>
</div>
<div class="stats four" style="margin-top:48px">
  <div class="stat rv d3"><img class="elogo" src="assets/engines/example.svg" alt="Example">
    <div class="n">00</div><div class="l">label</div></div>
</div>
```

## Comparison table

For rows that each carry a value, such as versions. `t` is the small second line inside a cell. `tr.hero` fills a row in MOI purple: use it once, for the row that matters. Inside a hero row write code with the inline white style shown, because `mono` is unreadable on purple.

```html
<table class="cmp rv d3" style="margin-top:32px; font-size:26px">
  <tr><th></th><th>What changed</th><th>Version</th></tr>
  <tr><td>Name</td><td>Change<span class="t">Detail line.</span></td><td>v0.0.0<span class="t">devnet</span></td></tr>
  <tr class="hero"><td>Install</td><td><span style="font-family:ui-monospace,Menlo,monospace; font-size:26px; color:#fff">npm i example</span></td><td>&nbsp;</td></tr>
</table>
```

## Steps and code (built for dark slides)

```html
<div class="steps rv d2" style="margin-top:52px">
  <div class="step"><span class="c">monospace left</span><span>plain right</span></div>
</div>
<div class="code rv d4" style="margin-top:40px"><span class="c">// comment</span>
<span class="kw">keyword</span> name(arg):  <span class="s">"string"</span></div>
```

`code` keeps line breaks as written (`white-space:pre`) and clips what does not fit, so a last line can vanish silently. `check-deck.py --layout` (check o) finds it. Inline code anywhere: `<span class="mono">KMOI_ASSET_ID</span>`.

## Beats (three or four demo steps, dark slides)

`beat no` is a quiet tile, `beat yes` is the purple one. Use `r` for the result, `m` for the line under it, or `<span class="num">01</span>` inside `n` for numbered steps.

```html
<div class="beats rv d3" style="margin-top:64px">
  <div class="beat no"><div class="n">1 &middot; First</div><div class="r">Refused</div><div class="m">what happened</div></div>
  <div class="beat yes"><div class="n">2 &middot; Second</div><div class="r">Allowed</div><div class="m">what happened</div></div>
</div>
```

## Pills (light and lav slides)

A row of status labels: `pill live` is filled, `pill res` is outlined. The outlined text is dark, so keep pills off dark slides.

```html
<div class="pills rv d2" style="margin-top:60px">
  <div class="pill live">Storage &middot; live</div><div class="pill res">Asset &middot; reserved</div>
</div>
```

## Photos

```html
<div class="photos rv d3" style="margin-top:48px; gap:44px">
  <div class="photo" style="aspect-ratio:3/2"><span class="ph">assets/name-1.png</span>
    <img src="assets/name-1.png" alt="What it shows" onerror="this.remove()"></div>
  <div class="photo" style="aspect-ratio:3/2"><span class="ph">assets/name-2.png</span>
    <img src="assets/name-2.png" alt="What it shows" onerror="this.remove()"></div>
</div>
```

The frame shows its filename until the file exists, and the border turns solid once an image loads. Frames share the row, so use two (3 by 2) or three (the default 4 by 3). A single frame spans the whole width and runs off the slide. Real files only, see `build.md`.

## Guest speaker

A large headshot with the guest's name, role, company, logo and topic beside it, with marked empty states for the two image files (`assets/guest/headshot.jpg`, `assets/guest/logo.svg`). The markup, the inputs and its spacing are in `guest-slide.md`. Do not build a guest slide from `photos`: CC14's draft did, with a small portrait under the text, and was rejected.

## Diagrams

Draw them as inline SVG, so they scale and print. Inside a card use `cdia`, on a slide of their own use `dia` (1620 wide). Use `currentColor` for strokes and text: it is dark on light slides and light on dark ones. Give every diagram `role="img"` and an `aria-label` that says what it shows.

```html
<svg class="dia" viewBox="0 0 1620 300" role="img" aria-label="Two boxes joined by an arrow.">
  <rect x="0" y="80" width="400" height="140" rx="20" fill="none" stroke="currentColor" stroke-width="3"/>
  <text x="200" y="160" text-anchor="middle" font-size="34" fill="currentColor">First</text>
</svg>
```

## Planetoid watermark

A faint outline of the logo bleeding off a dark slide's corner. Put it before `pad`; it is decoration only. Vary the side from slide to slide.

```html
<svg class="planetoid" style="right:-320px; top:-260px; width:1200px; opacity:.12" viewBox="0 0 26 20"><path fill="none" stroke="#BCA6FF" stroke-width=".35" d="m22.5,6.89c-2.58-1.49-6.09-2.74-6.5-2.89.35.07,3.11.68,5.99,1.62C20.37,2.29,16.95,0,13,0,8.4,0,4.52,3.1,3.36,7.34c-.13.47-.23.95-.28,1.44-.94.08-1.66.3-2.08.72-1.07,1.07.43,2.42,2.5,3.61,2.58,1.49,6.09,2.74,6.5,2.89-.35-.07-3.11-.68-5.99-1.62,1.63,3.33,5.04,5.62,8.99,5.62,4.6,0,8.48-3.11,9.64-7.34.13-.47.23-.95.28-1.44.94-.08,1.66-.3,2.08-.72,1.07-1.07-.43-2.42-2.5-3.61Z"/></svg>
```

## A statement slide

For one big sentence, centre the content: `<div class="pad" style="justify-content:center">`, then a chip, an `h2` at 84 to 88px with a `<br>` and one `accent`, and one or two `sub` lines. Used for the "why" moments in session 8.

## Spacing budget

The pad leaves 860px of height and 1640px of width. Measured on 2026-10-02 in headless Chrome 154 on macOS. Each height was read only after `document.fonts.ready`, with Poppins confirmed loaded (`document.fonts.check` true for weights 400 to 700, and a test string 1126px wide in Poppins against 1025px in the fallback sans-serif). Heights depend on the font: a run with the fallback sans-serif measured 7 to 9px less for a single block and up to 33px less for stacked ones (three steps), so on a machine without Poppins leave margin.

| Piece | Height |
| --- | --- |
| chip (the `div` that wraps it) | 55 |
| `h2` at 76px | 85 per line |
| `sub` at 30px | 45 per line (54 at the default 36px) |
| three cards, `d` of one line | 235 |
| three cards, `ul` of three one-line points | 331 |
| two cards, `d` of two lines | 271 (each further line of `d` adds 36; three lines is 307) |
| three cards, `ul` of four points of two lines each | 523 |
| stats, three tiles | 167 (four tiles with a logo: 221) |
| table | 69 header, 100 per row, plus 39 per `t` line |
| steps, three | 182 |
| code | 88 padding plus 44 per line |
| beats, one-line `m` | 274 (349 when `n` holds a numbered `<span class="num">`) |
| photos, two at 3 by 2 | 533 (three at 4 by 3: 393) |

Add the gaps (36 under the chip, 22 under the title, 48 before the component). Title, one-line sub and three bullet cards come to about 622, which fits. A two-line title, a two-line sub and cards with four two-line bullets come to about 944, which does not. Each extra wrapped line in a bullet adds 37px (24px at 1.55), so cut words before shrinking type, and if it still overflows it is two slides. Content that ends below y=990 enters the badge area. `check-deck.py --layout` (check o) measures every slide.
