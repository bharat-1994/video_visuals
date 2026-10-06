import React, {useMemo} from 'react';
import {AbsoluteFill, Audio, Easing, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {geoMercator, geoPath, geoGraticule10} from 'd3-geo';
import {feature} from 'topojson-client';
import land50 from 'world-atlas/land-50m.json';
import countries50 from 'world-atlas/countries-50m.json';
import words from './words.json';

export const W = 1920;
export const H = 1080;
export const BAR = 118; // cinematic letterbox
export const GOLD = '#e6c27a';
export const INK = '#07121a';

export const land = feature(land50 as any, (land50 as any).objects.land) as any;
const countries = (feature(countries50 as any, (countries50 as any).objects.countries) as any).features as any[];
export const india = countries.find((c) => c.properties.name === 'India');
export const graticule = geoGraticule10();

// ---------- helpers ----------
export const clamp01 = (x: number) => Math.min(1, Math.max(0, x));
export const ease = Easing.bezier(0.45, 0, 0.55, 1);
export const win = (t: number, a: number, b: number) => ease(clamp01((t - a) / (b - a)));
export const fadeInOut = (t: number, a: number, b: number, c: number, d: number) => win(t, a, b) * (1 - win(t, c, d));

// smooth camera: cardinal spline through keyframes (no stop-start between keys)
type Key = {t: number; lon: number; lat: number; z: number};
const keys: Key[] = [
  {t: 0, lon: -4, lat: 46, z: 1000},
  {t: 1.3, lon: -14, lat: 28, z: 760},
  {t: 2.5, lon: 8, lat: -26, z: 650},
  {t: 3.6, lon: 52, lat: -3, z: 600},
  {t: 4.7, lon: 60, lat: 12, z: 520},
  {t: 8.6, lon: 62, lat: 16, z: 560},
  {t: 11.6, lon: 67, lat: 18, z: 900},
  {t: 15.2, lon: 72.9, lat: 21.1, z: 3800},
  {t: 17.7, lon: 72.85, lat: 21.15, z: 8000},
  {t: 20.3, lon: 78, lat: 21.5, z: 1250},
  {t: 23.6, lon: 79, lat: 22.5, z: 1050},
];
const hermite = (p0: number, p1: number, m0: number, m1: number, u: number) => {
  const u2 = u * u, u3 = u2 * u;
  return (2 * u3 - 3 * u2 + 1) * p0 + (u3 - 2 * u2 + u) * m0 + (-2 * u3 + 3 * u2) * p1 + (u3 - u2) * m1;
};
const camera = (t: number) => {
  const n = keys.length;
  let i = 0;
  while (i < n - 2 && t > keys[i + 1].t) i++;
  const k0 = keys[Math.max(0, i - 1)], k1 = keys[i], k2 = keys[i + 1], k3 = keys[Math.min(n - 1, i + 2)];
  const dt = k2.t - k1.t;
  const u = clamp01((t - k1.t) / dt);
  const f = (get: (k: Key) => number) => {
    const m1 = ((get(k2) - get(k0)) / Math.max(1e-6, k2.t - k0.t)) * dt * 0.8;
    const m2 = ((get(k3) - get(k1)) / Math.max(1e-6, k3.t - k1.t)) * dt * 0.8;
    return hermite(get(k1), get(k2), m1, m2, u);
  };
  return {lon: f((k) => k.lon), lat: f((k) => k.lat), z: Math.exp(f((k) => Math.log(k.z)))};
};

// ---------- route England -> Cape -> Surat ----------
const waypoints: [number, number][] = [
  [-4.1, 50.35], [-9.5, 43.5], [-16, 31], [-18, 16], [-12, 2], [1, -22], [17, -36], [33, -31], [44, -14], [56, 4], [66, 15], [72.75, 21.1],
];
export const catmull = (pts: [number, number][], per = 40) => {
  const out: [number, number][] = [];
  for (let i = 0; i < pts.length - 1; i++) {
    const p0 = pts[Math.max(0, i - 1)], p1 = pts[i], p2 = pts[i + 1], p3 = pts[Math.min(pts.length - 1, i + 2)];
    for (let s = 0; s < per; s++) {
      const u = s / per, u2 = u * u, u3 = u2 * u;
      const c = (a: number, b: number, c_: number, d: number) =>
        0.5 * (2 * b + (-a + c_) * u + (2 * a - 5 * b + 4 * c_ - d) * u2 + (-a + 3 * b - 3 * c_ + d) * u3);
      out.push([c(p0[0], p1[0], p2[0], p3[0]), c(p0[1], p1[1], p2[1], p3[1])]);
    }
  }
  out.push(pts[pts.length - 1]);
  return out;
};
const route = catmull(waypoints);

// ---------- word / caption data ----------
type Word = {text: string; s: number; e: number};
const W_ALL: Word[] = (words as any[]).map(([text, s, e]) => ({text, s, e}));
const sentences: Word[][] = [];
{
  let cur: Word[] = [];
  W_ALL.forEach((w) => {
    cur.push(w);
    if (w.text.endsWith('.')) { sentences.push(cur); cur = []; }
  });
  if (cur.length) sentences.push(cur);
}

export const serif = "'Cormorant Garamond', Georgia, serif";
export const sans = "'Inter', system-ui, sans-serif";

export const fonts = `
@font-face{font-family:'Cormorant Garamond';font-weight:500;src:url(${staticFile('fonts/cormorant-garamond-latin-500-normal.woff2')}) format('woff2');}
@font-face{font-family:'Cormorant Garamond';font-weight:600;src:url(${staticFile('fonts/cormorant-garamond-latin-600-normal.woff2')}) format('woff2');}
@font-face{font-family:'Inter';font-weight:400;src:url(${staticFile('fonts/inter-latin-400-normal.woff2')}) format('woff2');}
@font-face{font-family:'Inter';font-weight:600;src:url(${staticFile('fonts/inter-latin-600-normal.woff2')}) format('woff2');}
`;

// ---------- the scene ----------
export const Scene: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;

  const cam = camera(t);
  const proj = useMemo(() => geoMercator(), []);
  proj.scale(cam.z).center([cam.lon, cam.lat]).translate([W / 2, H / 2]).clipExtent([[-60, -60], [W + 60, H + 60]]).precision(0.4);
  const path = geoPath(proj);
  const P = (lon: number, lat: number) => proj([lon, lat]) as [number, number];
  const px = cam.z * 0.0174533; // pixels per degree-ish at equator

  const landD = path(land) || '';
  const indiaD = path(india) || '';
  const gratD = path(graticule) || '';

  // ship + route
  const sail = win(t, 0.35, 4.75);
  const shipIdx = Math.min(route.length - 1, Math.floor(sail * (route.length - 1)));
  const routePts = route.map(([lo, la]) => P(lo, la));
  const routeD = 'M' + routePts.slice(0, shipIdx + 1).map((p) => p.join(',')).join('L');
  const routeFullD = 'M' + routePts.map((p) => p.join(',')).join('L');
  const ship = routePts[shipIdx];
  const prev = routePts[Math.max(0, shipIdx - 2)];
  const nxt = routePts[Math.min(routePts.length - 1, shipIdx + 2)];
  const ang = (Math.atan2(nxt[1] - prev[1], nxt[0] - prev[0]) * 180) / Math.PI;
  const shipOpacity = win(t, 0.3, 0.8) * (1 - win(t, 4.9, 5.6));
  const routeOpacity = 0.9 * (1 - 0.55 * win(t, 5, 6)) * (1 - win(t, 12.5, 14.5));

  // trade goods flowing back along the route
  const goods = useMemo(() => Array.from({length: 54}, (_, i) => ({
    i, color: i % 3 === 0 ? '#ffb347' : i % 3 === 1 ? '#f4f1ea' : '#e0405a', off: (i * 0.6180339) % 1, kind: i % 3,
  })), []);
  const goodsOn = fadeInOut(t, 7.2, 8.0, 11.2, 12.2);
  const flow = (t - 7.2) * 0.095;

  // Surat
  const surat = P(72.83, 21.17);
  const pulse = (t * 0.9) % 1;
  const suratShow = win(t, 11.9, 13.0) * (1 - win(t, 21, 22));

  // red expansion from presidency towns
  const seeds: [number, number, number][] = [[72.83, 18.95, 0.2], [80.27, 13.08, 0.1], [88.36, 22.57, 0.0], [72.83, 21.17, 0.35], [84.5, 25.6, 0.45], [78.5, 17.4, 0.4]];
  const grow = win(t, 18.0, 22.6);
  const redOpacity = win(t, 17.7, 19);

  // year counter
  const yr = Math.round(1612 + (1765 - 1612) * win(t, 18.2, 21.6));

  // camera shake / drift
  const driftX = Math.sin(t * 0.7) * 5, driftY = Math.cos(t * 0.53) * 4;
  const fadeIn = win(t, 0, 0.9);
  const fadeOut = 1 - win(t, 22.6, 23.5);

  // caption
  const sent = sentences.find((s) => t >= s[0].s - 0.15 && t <= s[s.length - 1].e + 0.45);

  const labelOpacity = (min: number, max: number) => clamp01((cam.z - min) / (max - min));

  return (
    <AbsoluteFill style={{background: INK, opacity: fadeIn * fadeOut}}>
      <style>{fonts}</style>
      <AbsoluteFill style={{filter: 'contrast(1.08) saturate(0.92) sepia(0.12)'}}>
        <div style={{position: 'absolute', inset: -30, transform: `translate(${driftX}px,${driftY}px)`}}>
          <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{position: 'absolute', left: 30, top: 30}}>
            <defs>
              <radialGradient id="ocean" cx="50%" cy="48%" r="75%">
                <stop offset="0" stopColor="#12384a" />
                <stop offset="0.6" stopColor="#0a2230" />
                <stop offset="1" stopColor="#040c12" />
              </radialGradient>
              <linearGradient id="landg" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0" stopColor="#3b3426" />
                <stop offset="1" stopColor="#241f17" />
              </linearGradient>
              <filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6" /></filter>
              <clipPath id="indiaClip"><path d={indiaD} /></clipPath>
              <mask id="redMask">
                <rect width={W} height={H} fill="black" />
                {seeds.map(([lo, la, delay], k) => {
                  const c = P(lo, la);
                  const g = clamp01((grow - delay) / (1 - delay));
                  return <circle key={k} cx={c[0]} cy={c[1]} r={g * px * 11.5} fill="white" />;
                })}
              </mask>
            </defs>

            <rect width={W} height={H} fill="url(#ocean)" />
            <path d={gratD} fill="none" stroke="#5fa3b8" strokeOpacity={0.09} strokeWidth={1} />

            {/* land */}
            <path d={landD} fill="url(#landg)" stroke="#8a7a55" strokeOpacity={0.55} strokeWidth={1.2} />
            <path d={landD} fill="none" stroke="#caa766" strokeOpacity={0.18} strokeWidth={4} filter="url(#glow)" />

            {/* India highlight */}
            <path d={indiaD} fill={GOLD} fillOpacity={0.1 + 0.12 * win(t, 10.8, 12.5)} stroke={GOLD} strokeOpacity={0.35 + 0.4 * win(t, 10.8, 12.5)} strokeWidth={1.6} />
            <g mask="url(#redMask)" opacity={redOpacity}>
              <path d={indiaD} fill="#c0272d" fillOpacity={0.62} />
              <path d={indiaD} fill="none" stroke="#ff6b5e" strokeWidth={2.4} strokeOpacity={0.9} />
            </g>

            {/* voyage */}
            <g opacity={routeOpacity}>
              <path d={routeFullD} fill="none" stroke={GOLD} strokeOpacity={0.14} strokeWidth={2} strokeDasharray="2 9" />
              <path d={routeD} fill="none" stroke={GOLD} strokeWidth={5} strokeOpacity={0.25} filter="url(#glow)" />
              <path d={routeD} fill="none" stroke={GOLD} strokeWidth={2.4} strokeLinecap="round" strokeDasharray="10 7" />
            </g>

            {/* goods stream, India -> England */}
            <g opacity={goodsOn}>
              {goods.map((g) => {
                const f = ((g.off + flow) % 1 + 1) % 1;
                const idx = Math.floor((1 - f) * (route.length - 1));
                const p = routePts[idx];
                const wob = Math.sin(t * 3 + g.i) * 4;
                return <circle key={g.i} cx={p[0] + wob * 0.5} cy={p[1] + wob} r={g.kind === 1 ? 4.2 : 3.4} fill={g.color} opacity={0.9}>
                </circle>;
              })}
            </g>

            {/* ship */}
            <g transform={`translate(${ship[0]},${ship[1]})`} opacity={shipOpacity}>
              <circle r={26} fill={GOLD} opacity={0.18} filter="url(#glow)" />
              <g transform={`scale(${Math.abs(ang) > 90 ? -1.8 : 1.8},1.8)`}>
                <path d="M-15 4 L15 4 L11 10 L-11 10 Z" fill="#1a1208" stroke={GOLD} strokeWidth={1.4} />
                <line x1="0" y1="4" x2="0" y2="-20" stroke={GOLD} strokeWidth={1.6} />
                <path d="M1 -19 Q13 -10 1 1 Z" fill="#f2e8cf" stroke={GOLD} strokeWidth={1} />
                <path d="M-1 -15 Q-10 -8 -1 0 Z" fill="#e9dcbd" stroke={GOLD} strokeWidth={1} />
              </g>
            </g>

            {/* Surat marker */}
            <g opacity={suratShow} transform={`translate(${surat[0]},${surat[1]})`}>
              {[0, 0.5].map((o, k) => {
                const p = (pulse + o) % 1;
                return <circle key={k} r={8 + p * 70} fill="none" stroke={GOLD} strokeWidth={2} opacity={(1 - p) * 0.8} />;
              })}
              <circle r={6} fill="#fff3d0" />
              <circle r={14} fill={GOLD} opacity={0.35} filter="url(#glow)" />
            </g>
          </svg>
        </div>
      </AbsoluteFill>

      {/* map labels (HTML so they stay crisp) */}
      <MapLabel p={P(-1.5, 52.5)} text="ENGLAND" o={fadeInOut(t, 0.2, 0.9, 4, 5.4) * labelOpacity(300, 700)} dx={-90} dy={-34} />
      <MapLabel p={P(15, 3)} text="AFRICA" o={fadeInOut(t, 1.5, 2.6, 4.4, 5.6) * 0.5} size={44} spacing={22} />
      <MapLabel p={P(79.5, 25)} text="INDIA" o={fadeInOut(t, 9.5, 11, 16.6, 17.4) * 0.8 + win(t, 20.5, 21.5) * 0.0} size={62} spacing={28} />
      <MapLabel p={P(72.83, 21.17)} text="SURAT" o={suratShow * labelOpacity(1800, 3800)} dx={-120} dy={-8} size={26} />

      {/* big date stamps */}
      <DateStamp text="1600" sub="THE EAST INDIA COMPANY IS FOUNDED" o={fadeInOut(t, 0.25, 1.1, 3.6, 4.5)} />
      <DateStamp text="1612" sub="SURAT · FIRST TRADING POST" o={fadeInOut(t, 10.9, 11.7, 15.9, 16.7)} />
      <DateStamp text={String(yr)} sub="COMPANY CONTROL · ILLUSTRATIVE" o={fadeInOut(t, 18.1, 18.8, 22.3, 23.2)} red />

      {/* trade goods tags */}
      <GoodsTag text="SPICES" t0={8.15} t1={10.9} t={t} x={-1} color="#ffb347" />
      <GoodsTag text="COTTON" t0={9.04} t1={10.9} t={t} x={0} color="#f4f1ea" />
      <GoodsTag text="SILK" t0={9.93} t1={10.9} t={t} x={1} color="#e0405a" />

      {/* "not an empire" beat: a quiet statement */}
      <div style={{position: 'absolute', left: 0, right: 0, top: 430, textAlign: 'center', opacity: fadeInOut(t, 5.2, 5.9, 6.6, 7.3)}}>
        <div style={{fontFamily: serif, fontStyle: 'normal', fontWeight: 500, fontSize: 84, letterSpacing: 10, color: '#f4ead2', textShadow: '0 4px 30px #000'}}>
          NOT AN EMPIRE.
        </div>
        <div style={{fontFamily: sans, fontSize: 24, letterSpacing: 12, color: GOLD, marginTop: 10, opacity: win(t, 7, 7.6)}}>JUST TRADE</div>
      </div>

      <Atmosphere t={t} frame={frame} />

      {/* letterbox + captions */}
      <div style={{position: 'absolute', left: 0, right: 0, top: 0, height: BAR, background: '#000'}} />
      <div style={{position: 'absolute', left: 0, right: 0, bottom: 0, height: BAR, background: '#000'}} />
      {sent && <Caption sent={sent} t={t} />}

      <Audio src={staticFile('vo.mp3')} />
    </AbsoluteFill>
  );
};

export const MapLabel: React.FC<{p: [number, number]; text: string; o: number; size?: number; spacing?: number; dx?: number; dy?: number}> = ({p, text, o, size = 30, spacing = 14, dx = 0, dy = 0}) => (
  <div style={{position: 'absolute', left: p[0] + dx, top: p[1] + dy, transform: 'translate(-50%,-50%)', opacity: o, fontFamily: serif, fontWeight: 500, fontSize: size, letterSpacing: spacing, color: '#e9dcbd', textShadow: '0 2px 18px #000', whiteSpace: 'nowrap', pointerEvents: 'none'}}>
    {text}
  </div>
);

export const DateStamp: React.FC<{text: string; sub: string; o: number; red?: boolean}> = ({text, sub, o, red}) => (
  <div style={{position: 'absolute', left: 150, top: 175, opacity: o, transform: `translateY(${(1 - o) * 16}px)`}}>
    <div style={{fontFamily: serif, fontWeight: 600, fontSize: 210, lineHeight: 0.9, color: red ? '#ff7a6b' : GOLD, textShadow: `0 0 50px ${red ? '#c0272d' : '#b8862e'}88, 0 6px 30px #000`}}>{text}</div>
    <div style={{fontFamily: sans, fontWeight: 600, fontSize: 21, letterSpacing: 7, color: '#d9d2c0', marginTop: 14, paddingLeft: 6, textShadow: '0 2px 12px #000'}}>{sub}</div>
  </div>
);

const GoodsTag: React.FC<{text: string; t0: number; t1: number; t: number; x: number; color: string}> = ({text, t0, t1, t, x, color}) => {
  const o = win(t, t0 - 0.05, t0 + 0.35) * (1 - win(t, t1 - 0.4, t1));
  return (
    <div style={{position: 'absolute', left: 960 + x * 360 - 150, top: 640 - (1 - win(t, t0, t0 + 0.5)) * -20, width: 300, textAlign: 'center', opacity: o, transform: `scale(${0.9 + 0.1 * win(t, t0, t0 + 0.5)})`}}>
      <div style={{width: 18, height: 18, borderRadius: 9, background: color, margin: '0 auto 14px', boxShadow: `0 0 28px ${color}`}} />
      <div style={{fontFamily: serif, fontWeight: 600, fontSize: 64, letterSpacing: 10, color: '#f6efdc', textShadow: '0 4px 24px #000'}}>{text}</div>
    </div>
  );
};

export const Caption: React.FC<{sent: Word[]; t: number}> = ({sent, t}) => {
  const o = clamp01((t - (sent[0].s - 0.15)) / 0.2) * (1 - clamp01((t - (sent[sent.length - 1].e + 0.15)) / 0.3));
  return (
    <div style={{position: 'absolute', left: 0, right: 0, bottom: 0, height: BAR, display: 'flex', alignItems: 'center', justifyContent: 'center', opacity: o}}>
      <div style={{fontFamily: sans, fontWeight: 600, fontSize: 36, letterSpacing: 0.5, color: '#fff', maxWidth: 1500, textAlign: 'center', lineHeight: 1.25}}>
        {sent.map((w, i) => {
          const a = clamp01((t - w.s + 0.05) / 0.12);
          const active = t >= w.s && t <= w.e + 0.05;
          return <span key={i} style={{color: active ? GOLD : a > 0 ? '#ffffff' : 'rgba(255,255,255,0.38)', marginRight: 10}}>{w.text}</span>;
        })}
      </div>
    </div>
  );
};

// dust motes, vignette, light bloom, film grain
export const Atmosphere: React.FC<{t: number; frame: number}> = ({t, frame}) => {
  const motes = useMemo(() => Array.from({length: 46}, (_, i) => {
    const r = (n: number) => { const x = Math.sin(i * 127.1 + n * 311.7) * 43758.5453; return x - Math.floor(x); };
    return {x: r(1) * W, y: r(2) * H, s: 1 + r(3) * 2.6, v: 6 + r(4) * 18, ph: r(5) * 6.28, a: 0.15 + r(6) * 0.35};
  }), []);
  const gx = (frame * 37) % 512, gy = (frame * 91) % 512;
  return (
    <>
      <AbsoluteFill style={{pointerEvents: 'none'}}>
        {motes.map((m, i) => (
          <div key={i} style={{position: 'absolute', left: ((m.x + t * m.v) % (W + 20)) - 10, top: m.y + Math.sin(t * 0.6 + m.ph) * 22, width: m.s, height: m.s, borderRadius: '50%', background: '#fff1c9', opacity: m.a * (0.6 + 0.4 * Math.sin(t * 1.3 + m.ph)), filter: 'blur(0.6px)'}} />
        ))}
      </AbsoluteFill>
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 50%, rgba(0,0,0,0) 45%, rgba(0,0,0,0.62) 100%)', pointerEvents: 'none'}} />
      <AbsoluteFill style={{background: 'linear-gradient(115deg, rgba(255,170,80,0.10) 0%, rgba(255,170,80,0) 40%, rgba(40,110,150,0.10) 100%)', mixBlendMode: 'screen', pointerEvents: 'none'}} />
      <AbsoluteFill style={{backgroundImage: `url(${staticFile('grain.png')})`, backgroundSize: '512px 512px', backgroundPosition: `${gx}px ${gy}px`, opacity: 0.11, mixBlendMode: 'overlay', pointerEvents: 'none'}} />
    </>
  );
};
