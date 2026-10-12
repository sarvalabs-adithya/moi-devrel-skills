// MOI marketing UI kit — components.jsx
// Loaded via <script type="text/babel" src="components.jsx"></script>

const ASSETS = "../../assets";

/* ────────────────────────────────────────────────────────────
   PRIMITIVES
   ──────────────────────────────────────────────────────────── */

function MonoEyebrow({ children, color = "var(--moi-main)", style }) {
  return (
    <span style={{
      fontFamily: "var(--font-mono)",
      fontWeight: 700,
      textTransform: "uppercase",
      letterSpacing: "0.08em",
      fontSize: "1.3rem",
      color,
      display: "inline-flex",
      alignItems: "center",
      gap: 8,
      ...style,
    }}>{children}</span>
  );
}

function HairlineDot({ width = 60, color = "currentColor" }) {
  return (
    <span style={{ position: "relative", display: "inline-block", width, height: 10, flexShrink: 0 }}>
      <span style={{
        position: "absolute", top: "50%", left: 0, right: 0, height: 2,
        background: `linear-gradient(90deg, transparent, ${color} 48%, transparent)`,
        transform: "translateY(-50%)",
      }} />
      <span style={{
        position: "absolute", top: "50%", left: "50%", width: 8, height: 8,
        borderRadius: "50%", background: color, transform: "translate(-50%, -50%)",
      }} />
    </span>
  );
}

function Button({ children, kind = "primary", onClick, style }) {
  const base = {
    cursor: "pointer", border: "none", outline: "none",
    fontFamily: "var(--font-sans)", fontWeight: 600, fontSize: "1.6rem",
    padding: "14px 24px", borderRadius: 999,
    transition: "transform 80ms ease-out, box-shadow 200ms ease",
    display: "inline-flex", alignItems: "center", gap: 8,
  };
  const kinds = {
    primary: {
      background: "var(--moi-main)", color: "var(--moi-haze)",
      boxShadow: "0 6px 20px rgba(75,23,229,0.30)",
    },
    "primary-on-dark": {
      background: "var(--moi-haze)", color: "var(--moi-black)",
      boxShadow: "inset 0 1.45px 33px rgba(255,255,255,0.25)",
    },
    secondary: {
      background: "transparent", color: "var(--moi-haze)",
      border: "1px solid rgba(217,204,255,0.4)",
      padding: "13px 24px",
    },
    "secondary-light": {
      background: "var(--tint-2)", color: "var(--moi-dark)",
      border: "1px solid var(--lav-1)",
    },
    ghost: {
      background: "transparent", color: "var(--moi-main)",
    },
  };
  return (
    <button
      style={{ ...base, ...kinds[kind], ...style }}
      onMouseDown={(e) => (e.currentTarget.style.transform = "scale(0.97)")}
      onMouseUp={(e) => (e.currentTarget.style.transform = "")}
      onMouseLeave={(e) => (e.currentTarget.style.transform = "")}
      onClick={onClick}>
      {children}
    </button>
  );
}

function Chip({ children, variant = "default" }) {
  const variants = {
    default: { background: "var(--tint-2)", color: "var(--moi-main)", border: "1px solid var(--lav-1)" },
    statement: { background: "var(--moi-black)", color: "var(--moi-lavender)" },
    success: { background: "rgba(31,174,107,0.10)", color: "#1FAE6B", border: "1px solid rgba(31,174,107,0.30)" },
    on_dark: { background: "rgba(245,242,255,0.08)", color: "var(--moi-haze)", border: "1px solid rgba(217,204,255,0.18)" },
    count: { background: "linear-gradient(180deg,#4B17E5,#320F99)", color: "var(--moi-haze)" },
  };
  return (
    <span style={{
      display: "inline-flex", alignItems: "center", gap: 8,
      padding: "6px 12px", borderRadius: 999,
      fontFamily: "var(--font-mono)", fontWeight: 700, fontSize: "1.2rem",
      textTransform: "uppercase", letterSpacing: "0.08em",
      ...variants[variant],
    }}>
      {variant !== "count" && (
        <span style={{ width: 6, height: 6, borderRadius: "50%", background: "currentColor" }} />
      )}
      {children}
    </span>
  );
}

/* ────────────────────────────────────────────────────────────
   DECOR — orbs, soft-star, dot grid
   ──────────────────────────────────────────────────────────── */

function Orb({ size = 120, x = 0, y = 0, hue = "main", style }) {
  const fills = {
    main:  "radial-gradient(circle at 30% 25%, #9871F2, #4B17E5 55%, #320F99)",
    dark:  "linear-gradient(135deg, #320F99, #0A0026)",
    light: "linear-gradient(160deg, #9871F2, #4B17E5)",
    haze:  "#D9CCFF",
  };
  return (
    <div style={{
      position: "absolute",
      left: x, top: y, width: size, height: size,
      borderRadius: "50%",
      background: fills[hue],
      boxShadow: "inset 0 1.45px 33px rgba(255,255,255,0.25)",
      pointerEvents: "none",
      ...style,
    }} />
  );
}

function SoftStar({ size = 80, color = "#F5F2FF", opacity = 0.6, style }) {
  return (
    <img src={`${ASSETS}/icons/soft-star.svg`} alt=""
      style={{
        width: size, height: size,
        filter: color === "#F5F2FF" ? "invert(95%)" :
                color === "#4B17E5" ? "invert(15%) sepia(85%) saturate(3500%) hue-rotate(248deg) brightness(95%)" :
                undefined,
        opacity,
        pointerEvents: "none",
        ...style,
      }} />
  );
}

function DotField({ color = "rgba(217,204,255,0.30)", size = 18 }) {
  return (
    <div style={{
      position: "absolute", inset: 0,
      backgroundImage: `radial-gradient(${color} 1.2px, transparent 1.2px)`,
      backgroundSize: `${size}px ${size}px`,
      pointerEvents: "none",
    }} />
  );
}

/* ────────────────────────────────────────────────────────────
   NAV
   ──────────────────────────────────────────────────────────── */

function Nav({ onCta }) {
  const [scrolled, setScrolled] = React.useState(false);
  React.useEffect(() => {
    const fn = () => setScrolled(window.scrollY > 30);
    window.addEventListener("scroll", fn); return () => window.removeEventListener("scroll", fn);
  }, []);
  return (
    <nav style={{
      position: "fixed", top: 0, left: 0, right: 0, zIndex: 100,
      display: "flex", alignItems: "center", justifyContent: "space-between",
      padding: "18px 48px",
      background: scrolled ? "rgba(10,0,38,0.65)" : "transparent",
      backdropFilter: scrolled ? "blur(20px)" : "none",
      transition: "background 200ms ease, backdrop-filter 200ms ease",
    }}>
      <div style={{ display: "flex", alignItems: "center", gap: 12, color: "var(--moi-haze)" }}>
        <img src={`${ASSETS}/logos/SVG/Default - Light.svg`} alt="MOI" style={{ height: 32 }} />
        <span style={{ width: 1, height: 22, background: "rgba(217,204,255,0.35)" }} />
        <span style={{ fontFamily: "var(--font-sans)", fontWeight: 500, fontSize: "1.7rem", color: "var(--moi-haze)" }}>
          moi.technology
        </span>
      </div>
      <div style={{ display: "flex", alignItems: "center", gap: 28 }}>
        {["Participants", "Validators", "Docs", "Manifesto"].map(l => (
          <a key={l} href="#" style={{
            fontFamily: "var(--font-sans)", fontWeight: 500, fontSize: "1.4rem",
            color: "var(--moi-haze)", opacity: 0.85, borderBottom: "1px solid transparent",
          }}>{l}</a>
        ))}
        <Button kind="primary-on-dark" onClick={onCta}>Become a participant</Button>
      </div>
    </nav>
  );
}

/* ────────────────────────────────────────────────────────────
   HERO
   ──────────────────────────────────────────────────────────── */

function Hero({ onCta }) {
  return (
    <section style={{
      position: "relative",
      minHeight: 760,
      padding: "160px 48px 96px",
      background: "linear-gradient(180deg, #0A0026 0%, #320F99 100%)",
      color: "var(--moi-haze)",
      overflow: "hidden",
    }}>
      {/* decor */}
      <DotField color="rgba(217,204,255,0.10)" />
      <Orb size={520} x="-180px" y="-180px" hue="main" style={{ opacity: 0.55, filter: "blur(8px)" }} />
      <Orb size={280} x="62%" y="55%" hue="light" style={{ opacity: 0.5, filter: "blur(2px)" }} />
      <SoftStar size={32} style={{ position: "absolute", top: 220, left: "44%" }} opacity={0.7} />
      <SoftStar size={20} style={{ position: "absolute", top: 540, left: "38%" }} opacity={0.5} />
      <SoftStar size={48} style={{ position: "absolute", top: 380, right: "12%" }} opacity={0.4} />

      <div style={{ position: "relative", maxWidth: 1280, margin: "0 auto", display: "grid", gridTemplateColumns: "1.1fr 1fr", gap: 48, alignItems: "center" }}>
        {/* left */}
        <div style={{ display: "flex", flexDirection: "column", gap: 24 }}>
          <MonoEyebrow color="var(--moi-lavender)">
            <span style={{ width: 6, height: 6, borderRadius: 999, background: "currentColor" }} />
            The participant layer · v0.9
          </MonoEyebrow>
          <h1 style={{
            fontFamily: "var(--font-sans)", fontWeight: 700, fontSize: "8.3rem",
            lineHeight: 0.95, letterSpacing: "-0.025em", margin: 0,
          }}>
            You haven't<br/>met the<br/>
            <span style={{ color: "var(--moi-lavender)" }}>participant</span> yet.
          </h1>
          <p style={{
            fontFamily: "var(--font-sans)", fontSize: "2.0rem", lineHeight: 1.4,
            color: "rgba(245,242,255,0.78)", maxWidth: 480, margin: 0,
          }}>
            You exist once, on chain, as a coherent participant. Your authority stays anchored to you,
            wherever your agents go. Monitor, scope and revoke AI Agents in real time.
          </p>
          <div style={{ display: "flex", gap: 12, alignItems: "center", flexWrap: "wrap", marginTop: 8 }}>
            <Button kind="primary-on-dark" onClick={onCta}>Become a participant →</Button>
            <Button kind="secondary">Watch the demo</Button>
            <Chip variant="count">2,100+ Validators</Chip>
          </div>
        </div>
        {/* right — Pip + orbital ring */}
        <div style={{ position: "relative", minHeight: 520 }}>
          <div className="pip-orbit" style={{
            position: "absolute", inset: 0, display: "flex", alignItems: "center", justifyContent: "center",
          }}>
            <img src={`${ASSETS}/mascot/pip-banner.png`} alt="Pip"
                 style={{ width: 520, maxWidth: "100%", filter: "drop-shadow(0 30px 80px rgba(75,23,229,0.45))" }} />
          </div>
        </div>
      </div>

      {/* bottom watermark */}
      <div style={{ position: "absolute", left: 48, bottom: 28, display: "flex", alignItems: "center", gap: 12, color: "rgba(245,242,255,0.55)" }}>
        <MonoEyebrow color="var(--moi-lavender)">@MOI_Tech</MonoEyebrow>
        <HairlineDot width={50} color="rgba(245,242,255,0.5)" />
        <span style={{ fontFamily: "var(--font-mono)", fontSize: "1.3rem" }}>scope · monitor · revoke</span>
      </div>
    </section>
  );
}

/* ────────────────────────────────────────────────────────────
   "Your authority, four ways."
   ──────────────────────────────────────────────────────────── */

const STEPS = [
  {
    label: "EXIST ON-CHAIN",
    title: "One coherent participant.",
    body: "Agents plug into you. You don't get cloned across credentials.",
    icon: ({ s = 1 }) => (
      <svg width={40 * s} height={40 * s} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.4">
        <circle cx="12" cy="12" r="3" />
        <circle cx="12" cy="12" r="9" />
        <circle cx="12" cy="3" r="1.2" fill="currentColor" />
        <circle cx="12" cy="21" r="1.2" fill="currentColor" />
      </svg>
    ),
  },
  {
    label: "MONITOR",
    title: "See every action in real time.",
    body: "Every call, every scope check — streamed to you, not after the fact.",
    icon: () => (
      <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.4">
        <path d="M3 12h4l3 -8l4 16l3 -8h4" />
      </svg>
    ),
  },
  {
    label: "SCOPE",
    title: "Choose what they can touch.",
    body: "Per-agent, per-resource, per-call. Standing scope replaces borrowed keys.",
    icon: () => (
      <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.4">
        <circle cx="12" cy="12" r="8" />
        <path d="M12 4v8l5 3" />
      </svg>
    ),
  },
  {
    label: "REVOKE",
    title: "Cut access at machine speed.",
    body: "One call. Globally enforced. No long-lived token left holding the bag.",
    icon: () => (
      <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.4">
        <path d="M3 12a9 9 0 1 0 3 -6.7" />
        <path d="M3 4v5h5" />
      </svg>
    ),
  },
];

function FourWays({ activeIdx, setActiveIdx }) {
  return (
    <section style={{
      padding: "120px 48px",
      background: "var(--moi-haze)",
      position: "relative",
    }}>
      <div style={{ maxWidth: 1280, margin: "0 auto" }}>
        <div style={{ display: "flex", alignItems: "baseline", justifyContent: "space-between", marginBottom: 56, flexWrap: "wrap", gap: 16 }}>
          <div>
            <MonoEyebrow>
              <span style={{ width: 6, height: 6, borderRadius: 999, background: "currentColor" }} />
              The four-way authority model
            </MonoEyebrow>
            <h2 style={{
              fontFamily: "var(--font-sans)", fontWeight: 700, fontSize: "5.8rem",
              letterSpacing: "-0.02em", color: "var(--moi-dark)", margin: "12px 0 0", lineHeight: 1,
            }}>Your authority, four ways.</h2>
          </div>
          <p style={{
            fontFamily: "var(--font-sans)", fontSize: "1.8rem", color: "var(--fg-2)",
            maxWidth: 380, lineHeight: 1.4, margin: 0,
          }}>
            Information about your authority is not your authority. Anywhere. Ever. So we stopped passing it around.
          </p>
        </div>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 16 }}>
          {STEPS.map((s, i) => {
            const active = i === activeIdx;
            const Icon = s.icon;
            return (
              <button key={i} onClick={() => setActiveIdx(i)}
                style={{
                  all: "unset", cursor: "pointer", display: "flex", flexDirection: "column", gap: 16,
                  padding: 24, borderRadius: 20,
                  background: active ? "var(--moi-black)" : "#fff",
                  color: active ? "var(--moi-haze)" : "var(--moi-dark)",
                  border: active ? "1px solid var(--moi-dark)" : "1px solid var(--border-soft)",
                  boxShadow: active
                    ? "0 24px 64px rgba(50,15,153,0.20), 0 0 60px rgba(75,23,229,0.30)"
                    : "0 4px 12px rgba(50,15,153,0.06)",
                  transform: active ? "translateY(-4px)" : "none",
                  transition: "all 250ms cubic-bezier(0.22,0.61,0.36,1)",
                  position: "relative", overflow: "hidden",
                }}>
                {active && <Orb size={140} x="60%" y="-50%" hue="main" style={{ opacity: 0.55 }} />}
                <div style={{
                  position: "relative",
                  display: "inline-flex", alignItems: "center", justifyContent: "center",
                  width: 56, height: 56, borderRadius: 14,
                  background: active ? "rgba(245,242,255,0.10)" : "var(--tint-2)",
                  color: active ? "var(--moi-haze)" : "var(--moi-main)",
                  border: active ? "1px solid rgba(217,204,255,0.25)" : "1px solid var(--lav-1)",
                }}>
                  <Icon />
                </div>
                <div style={{ position: "relative" }}>
                  <MonoEyebrow color={active ? "var(--moi-lavender)" : "var(--moi-main)"} style={{ fontSize: "1.1rem" }}>
                    0{i + 1} · {s.label}
                  </MonoEyebrow>
                  <div style={{
                    fontFamily: "var(--font-sans)", fontWeight: 700, fontSize: "2.3rem",
                    lineHeight: 1.1, marginTop: 8, color: active ? "var(--moi-haze)" : "var(--moi-dark)",
                  }}>{s.title}</div>
                  <div style={{
                    fontFamily: "var(--font-sans)", fontSize: "1.5rem", lineHeight: 1.4,
                    marginTop: 12, color: active ? "rgba(245,242,255,0.78)" : "var(--fg-2)",
                  }}>{s.body}</div>
                </div>
              </button>
            );
          })}
        </div>
      </div>
    </section>
  );
}

/* ────────────────────────────────────────────────────────────
   The Story Band (dark, with quote + code block)
   ──────────────────────────────────────────────────────────── */

function StoryBand() {
  return (
    <section style={{
      position: "relative", padding: "120px 48px",
      background: "linear-gradient(180deg, #0A0026 0%, #320F99 100%)",
      color: "var(--moi-haze)", overflow: "hidden",
    }}>
      <DotField color="rgba(217,204,255,0.10)" />
      <Orb size={420} x="-120px" y="-120px" hue="main" style={{ opacity: 0.35, filter: "blur(6px)" }} />
      <SoftStar size={120} style={{ position: "absolute", right: -30, top: 60 }} opacity={0.20} />

      <div style={{ position: "relative", maxWidth: 1280, margin: "0 auto", display: "grid", gridTemplateColumns: "1fr 1fr", gap: 64, alignItems: "center" }}>
        <div style={{ display: "flex", flexDirection: "column", gap: 24 }}>
          <MonoEyebrow color="var(--moi-lavender)">
            <span style={{ width: 6, height: 6, borderRadius: 999, background: "currentColor" }} />
            Why it matters
          </MonoEyebrow>
          <p style={{
            fontFamily: "var(--font-sans)", fontWeight: 600,
            fontSize: "3.2rem", lineHeight: 1.2, color: "var(--moi-haze)", margin: 0,
          }}>
            A month ago, a coding agent found an admin token in a file system. Used it and deleted a production database in
            <span style={{ color: "var(--moi-lavender)" }}> 9 seconds.</span> Wrote an apology after.
          </p>
          <p style={{ fontFamily: "var(--font-sans)", fontSize: "1.8rem", lineHeight: 1.5, color: "rgba(245,242,255,0.78)", margin: 0 }}>
            It's not the agent's fault. Architecture broke the agent and left it no other choice.
            MOI doesn't replace your AI stack. It makes it trustworthy.
          </p>
        </div>
        <div style={{
          background: "rgba(245,242,255,0.04)", border: "1px solid rgba(217,204,255,0.15)",
          borderRadius: 20, padding: 24, position: "relative", overflow: "hidden",
        }}>
          <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 18 }}>
            <MonoEyebrow color="var(--moi-lavender)" style={{ fontSize: "1.1rem" }}>
              moi · participant.revoke()
            </MonoEyebrow>
            <Chip variant="success">ok · 9ms</Chip>
          </div>
          <pre style={{
            fontFamily: "var(--font-mono)", fontSize: "1.55rem", lineHeight: 1.6,
            color: "var(--moi-haze)", margin: 0, whiteSpace: "pre-wrap",
          }}>
{`const me = moi.participant("0x4b17e5···320f99");

me.agent("claw-12")
  .scope({ read: true, write: false })
  .revoke();
// → cut at machine speed`}
          </pre>
        </div>
      </div>
    </section>
  );
}

/* ────────────────────────────────────────────────────────────
   Validators band
   ──────────────────────────────────────────────────────────── */

function ValidatorsBand() {
  return (
    <section style={{
      position: "relative", padding: "96px 48px",
      background: "var(--moi-haze)", overflow: "hidden",
    }}>
      <SoftStar size={300} color="#4B17E5" style={{ position: "absolute", left: -80, top: -80 }} opacity={0.10} />
      <SoftStar size={200} color="#4B17E5" style={{ position: "absolute", right: -40, bottom: -40 }} opacity={0.10} />
      <div style={{ position: "relative", maxWidth: 1280, margin: "0 auto", display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 24 }}>
        <Stat n="2,100+" label="Validators" />
        <Stat n="7 yrs" label="Building the participant layer" />
        <Stat n="9 ms" label="Median revoke latency" />
      </div>
      <div style={{
        position: "relative", display: "flex", alignItems: "center", justifyContent: "center",
        gap: 16, marginTop: 56, color: "var(--moi-dark)",
      }}>
        <span style={{ fontFamily: "var(--font-mono)", fontWeight: 700, fontSize: "1.3rem", textTransform: "uppercase", letterSpacing: "0.12em" }}>
          works with
        </span>
        <HairlineDot width={40} color="var(--moi-main)" />
        <PartnerPill name="@openclaw" status="LIVE" />
        <PartnerPill name="@LangChain" status="NEXT" />
        <PartnerPill name="@a16zcrypto" status="ALIGNED" />
      </div>
    </section>
  );
}

function Stat({ n, label }) {
  return (
    <div style={{
      background: "#fff", borderRadius: 20, padding: 28,
      border: "1px solid var(--border-soft)",
      display: "flex", flexDirection: "column", gap: 6,
      boxShadow: "0 12px 32px rgba(50,15,153,0.06)",
    }}>
      <div style={{ fontFamily: "var(--font-sans)", fontWeight: 700, fontSize: "6.6rem", lineHeight: 1, color: "var(--moi-dark)", letterSpacing: "-0.02em" }}>{n}</div>
      <div style={{ fontFamily: "var(--font-sans)", fontWeight: 500, fontSize: "1.6rem", color: "var(--fg-2)" }}>{label}</div>
    </div>
  );
}

function PartnerPill({ name, status }) {
  const live = status === "LIVE";
  return (
    <span style={{
      display: "inline-flex", alignItems: "center", gap: 10,
      padding: "8px 14px", borderRadius: 999,
      background: "#fff", border: "1px solid var(--border-soft)",
      fontFamily: "var(--font-mono)", fontSize: "1.3rem", fontWeight: 600,
      color: "var(--moi-dark)",
    }}>
      <span style={{ width: 6, height: 6, borderRadius: "50%",
        background: live ? "#1FAE6B" : "var(--moi-lavender)" }} />
      {name}
      <span style={{ fontSize: "1.1rem", color: "var(--fg-3)", textTransform: "uppercase", letterSpacing: "0.1em" }}>
        · {status}
      </span>
    </span>
  );
}

/* ────────────────────────────────────────────────────────────
   CTA + Footer
   ──────────────────────────────────────────────────────────── */

function CtaBand({ onCta }) {
  return (
    <section style={{
      position: "relative", padding: "140px 48px",
      background: "linear-gradient(180deg, #320F99 0%, #4B17E5 100%)",
      color: "var(--moi-haze)", overflow: "hidden", textAlign: "center",
    }}>
      <Orb size={680} x="-220px" y="40%" hue="main" style={{ opacity: 0.5, filter: "blur(10px)" }} />
      <Orb size={420} x="70%" y="-180px" hue="light" style={{ opacity: 0.45, filter: "blur(4px)" }} />
      <SoftStar size={80} style={{ position: "absolute", top: 60, left: "20%" }} opacity={0.5} />
      <SoftStar size={40} style={{ position: "absolute", bottom: 80, right: "22%" }} opacity={0.7} />

      <div style={{ position: "relative", maxWidth: 880, margin: "0 auto", display: "flex", flexDirection: "column", gap: 28, alignItems: "center" }}>
        <Chip variant="statement">OFFICIAL STATEMENT</Chip>
        <h2 style={{
          fontFamily: "var(--font-sans)", fontWeight: 700, fontSize: "7.4rem",
          letterSpacing: "-0.025em", lineHeight: 1, margin: 0,
        }}>Not your Context,<br/>Not your KitKat.</h2>
        <p style={{ fontFamily: "var(--font-sans)", fontSize: "2.0rem", lineHeight: 1.4, color: "rgba(245,242,255,0.78)", margin: 0 }}>
          Identity, not intelligence, is the bottleneck. Anchor yours.
        </p>
        <div style={{ display: "flex", gap: 12 }}>
          <Button kind="primary-on-dark" onClick={onCta}>Become a participant →</Button>
          <Button kind="secondary">Read the manifesto</Button>
        </div>
      </div>
    </section>
  );
}

function Footer() {
  return (
    <footer style={{ background: "var(--moi-black)", color: "var(--moi-haze)", padding: "56px 48px 36px" }}>
      <div style={{ maxWidth: 1280, margin: "0 auto", display: "grid", gridTemplateColumns: "1.4fr 1fr 1fr 1fr", gap: 32 }}>
        <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
            <img src={`${ASSETS}/logos/SVG/Default - Light.svg`} style={{ height: 36 }} />
            <span style={{ width: 1, height: 22, background: "rgba(217,204,255,0.35)" }} />
            <span style={{ fontFamily: "var(--font-sans)", fontWeight: 500, fontSize: "1.8rem", color: "var(--moi-haze)" }}>moi.technology</span>
          </div>
          <p style={{ fontFamily: "var(--font-sans)", fontSize: "1.4rem", color: "rgba(245,242,255,0.6)", maxWidth: 340, lineHeight: 1.5, margin: 0 }}>
            The on-chain authority layer for AI agents. Monitor, scope and revoke in real time.
          </p>
          <MonoEyebrow color="var(--moi-lavender)" style={{ fontSize: "1.2rem", marginTop: 12 }}>@MOI_Tech</MonoEyebrow>
        </div>
        {[
          ["Product", ["Participants", "Validators", "Scope DSL", "Revoke API"]],
          ["Build",   ["Docs", "@openclaw", "@LangChain (next)", "Status"]],
          ["Org",     ["Manifesto", "Team", "Press", "Contact"]],
        ].map(([h, items]) => (
          <div key={h} style={{ display: "flex", flexDirection: "column", gap: 10 }}>
            <MonoEyebrow color="var(--moi-lavender)" style={{ fontSize: "1.1rem" }}>{h}</MonoEyebrow>
            {items.map(i => (
              <a key={i} href="#" style={{
                fontFamily: "var(--font-sans)", fontSize: "1.5rem",
                color: "rgba(245,242,255,0.78)", borderBottom: "1px solid transparent",
              }}>{i}</a>
            ))}
          </div>
        ))}
      </div>
      <div style={{
        maxWidth: 1280, margin: "48px auto 0", paddingTop: 24,
        borderTop: "1px solid rgba(217,204,255,0.12)",
        display: "flex", justifyContent: "space-between", alignItems: "center",
        fontFamily: "var(--font-mono)", fontSize: "1.2rem", color: "rgba(245,242,255,0.45)",
      }}>
        <span>© MOI Protocol. You exist once.</span>
        <span>v0.9 · {new Date().getFullYear()}</span>
      </div>
    </footer>
  );
}

/* ────────────────────────────────────────────────────────────
   Sticky Toast — interactive demo of "revoke"
   ──────────────────────────────────────────────────────────── */

function RevokedToast({ open, onClose }) {
  if (!open) return null;
  return (
    <div style={{
      position: "fixed", bottom: 28, right: 28, zIndex: 200,
      background: "var(--moi-black)", color: "var(--moi-haze)",
      borderRadius: 16, padding: 16,
      border: "1px solid rgba(217,204,255,0.18)",
      display: "flex", gap: 14, alignItems: "center",
      boxShadow: "0 24px 64px rgba(10,0,38,0.5), 0 0 60px rgba(75,23,229,0.25)",
      animation: "slideIn 300ms cubic-bezier(0.22,0.61,0.36,1) both",
      maxWidth: 360,
    }}>
      <div style={{
        width: 44, height: 44, borderRadius: 12,
        background: "linear-gradient(180deg, #4B17E5, #320F99)",
        display: "flex", alignItems: "center", justifyContent: "center",
        boxShadow: "inset 0 1.45px 33px rgba(255,255,255,0.25)",
      }}>
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
          <path d="M3 12a9 9 0 1 0 3 -6.7" /><path d="M3 4v5h5" />
        </svg>
      </div>
      <div style={{ flex: 1 }}>
        <MonoEyebrow color="var(--moi-lavender)" style={{ fontSize: "1.1rem" }}>scope revoked</MonoEyebrow>
        <div style={{ fontFamily: "var(--font-sans)", fontWeight: 500, fontSize: "1.5rem", marginTop: 4 }}>
          agent:claw-12 lost write access. Globally enforced.
        </div>
      </div>
      <button onClick={onClose} style={{
        all: "unset", cursor: "pointer", padding: 6, color: "rgba(245,242,255,0.6)",
      }}>×</button>
    </div>
  );
}

Object.assign(window, {
  MonoEyebrow, HairlineDot, Button, Chip,
  Orb, SoftStar, DotField,
  Nav, Hero, FourWays, StoryBand, ValidatorsBand, CtaBand, Footer, RevokedToast,
});
