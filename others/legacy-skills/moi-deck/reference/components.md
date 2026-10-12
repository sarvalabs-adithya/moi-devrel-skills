# Slide components

Every slide is a `<section class="slide …">` holding a `<div class="pad">`. The stage is a fixed
1920×1080 box that scales to the window, so the numbers below are real pixels and the budget is hard.

## Backgrounds

| Class | Looks like | Use for |
| --- | --- | --- |
| `slide light` | near-white lavender | most content slides |
| `slide lav` | pale lavender | alternate with `light` so neighbours differ |
| `slide dark grad` | deep indigo gradient | title, section breaks, the close |
| `slide dark` | flat near-black | rare, when a gradient fights an image |

Dark slides need the light logo: `<svg class="corner-logo"><use href="#moiOnDark"/></svg>`. Light and
lav slides use `#moiOnLight`. The cover and close usually drop the corner logo for a large centred one.

## Skeleton

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

`rv` fades an element in; `d1` to `d5` stagger it. Number the badge to match the page.

## Cards

Three at most, two reads better when the text is long. `ul` and `d` are alternatives, not partners.

```html
<div class="cards" style="margin-top:48px">
  <div class="card rv d3"><div class="k">Kicker</div><div class="v">Card headline</div>
    <ul><li>Point one</li><li>Point two</li></ul></div>
  <div class="card rv d4"><div class="k">Kicker</div><div class="v">Card headline</div>
    <div class="d">A sentence or two instead of bullets.</div></div>
</div>
```

## Stats

Three tiles, or four with `stats four`. `n` is the number, `l` the label. An optional logo sits above.

```html
<div class="stats" style="margin-top:52px">
  <div class="stat rv d3"><div class="n">17.3%</div><div class="l">visibility</div></div>
</div>

<div class="stats four" style="margin-top:48px">
  <div class="stat rv d3"><img class="elogo" src="assets/engines/perplexity.svg" alt="Perplexity">
    <div class="n">20%</div><div class="l">Perplexity</div></div>
</div>
```

A long `n` such as a word needs `style="font-size:44px"` or it crowds the tile.

## Comparison table

For rows of things with a value each, like versions. `t` is the small second line inside a cell.
`tr.hero` fills the row in MOI purple; use it once, for the row that matters.

```html
<table class="cmp rv d3" style="margin-top:32px; font-size:26px">
  <tr><th></th><th>What changed</th><th>Version</th></tr>
  <tr><td>moipod</td><td>Fee delegation<span class="t">Sender and payer read from the interaction.</span></td>
      <td>v0.13.0<span class="t">devnet</span></td></tr>
  <tr class="hero"><td>Install</td><td><span style="font-family:ui-monospace,Menlo,monospace; font-size:26px; color:#fff">npm i …</span></td><td>&nbsp;</td></tr>
</table>
```

## Steps, code, photos, inline code

```html
<div class="steps rv d2" style="margin-top:52px">
  <div class="step"><span class="c">monospace left</span><span>plain right</span></div>
</div>

<div class="code rv d4" style="margin-top:40px"><span class="c">// comment</span>
<span class="kw">endpoint</span> Name(arg Type):  <span class="s">"string"</span></div>

<div class="photos rv d3" style="margin-top:48px; gap:44px">
  <div class="photo" style="aspect-ratio:3/2"><span class="ph">assets/name.png</span>
    <img src="assets/name.png" alt="What it shows" onerror="this.remove()"></div>
</div>

<span class="mono">KMOI_ASSET_ID</span>
```

The `photo` frame shows its filename until the file exists, and the border turns solid once an image
loads. `steps` and `code` are built for dark slides.

## Cover and close

The cover uses a big centred logo, a chip, an `h1` and one `sub` line. `<div class="ghost-num">14</div>`
puts a huge translucent numeral behind it, bleeding off the right edge. The close is the same shape
with fewer words.

## Spacing budget

The 1080px stage minus 110px padding top and bottom leaves about 860px. A chip is ~50, an `h2` at 76px
is ~85 per line, a `sub` ~45 per line. So: title, sub, one component, and at most one closing line.
When a slide overflows, cut words before shrinking type. If it still overflows, it is two slides.
