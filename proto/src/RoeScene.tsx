import React, {useMemo} from 'react';
import {AbsoluteFill, Audio, Img, OffthreadVideo, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {geoMercator, geoPath} from 'd3-geo';
import {
  Atmosphere, BAR, Caption, DateStamp, GOLD, INK, MapLabel, W, H, catmull, clamp01, ease, fadeInOut, fonts, graticule, india, land, sans, serif, win,
} from './Scene';
import roeWords from './roe-words.json';

export const ROE_DURATION_S = 22.8;

// ---------------------------------------------------------------- timeline
const T = {
  ship: [0, 5.0], map: [4.8, 11.3], bichitr: [10.8, 13.9], darbar: [13.65, 17.0], cards: [16.75, 20.3], foothold: [20.05, ROE_DURATION_S],
} as const;
const seg = (t: number, a: number, fade = 0.55) => win(t, a, a + fade);

// ---------------------------------------------------------------- captions
type Word = {text: string; s: number; e: number};
const WORDS: Word[] = (roeWords as any[]).map(([text, s, e]) => ({text, s, e}));
const sentences: Word[][] = [];
{
  let cur: Word[] = [];
  WORDS.forEach((w) => { cur.push(w); if (/[.]$/.test(w.text)) { sentences.push(cur); cur = []; } });
  if (cur.length) sentences.push(cur);
}

// ---------------------------------------------------------------- generic spline camera
type Key = {t: number; lon: number; lat: number; z: number};
const hermite = (p0: number, p1: number, m0: number, m1: number, u: number) => {
  const u2 = u * u, u3 = u2 * u;
  return (2 * u3 - 3 * u2 + 1) * p0 + (u3 - 2 * u2 + u) * m0 + (-2 * u3 + 3 * u2) * p1 + (u3 - u2) * m1;
};
const makeCam = (keys: Key[]) => (t: number) => {
  const n = keys.length;
  const tt = Math.min(keys[n - 1].t, Math.max(keys[0].t, t));
  let i = 0;
  while (i < n - 2 && tt > keys[i + 1].t) i++;
  const k0 = keys[Math.max(0, i - 1)], k1 = keys[i], k2 = keys[i + 1], k3 = keys[Math.min(n - 1, i + 2)];
  const dt = k2.t - k1.t, u = clamp01((tt - k1.t) / dt);
  const f = (g: (k: Key) => number) => {
    const m1 = ((g(k2) - g(k0)) / Math.max(1e-6, k2.t - k0.t)) * dt * 0.8;
    const m2 = ((g(k3) - g(k1)) / Math.max(1e-6, k3.t - k1.t)) * dt * 0.8;
    return hermite(g(k1), g(k2), m1, m2, u);
  };
  return {lon: f((k) => k.lon), lat: f((k) => k.lat), z: Math.exp(f((k) => Math.log(k.z)))};
};
const camA = makeCam([
  {t: 4.8, lon: 24, lat: 30, z: 440}, {t: 6.4, lon: 40, lat: 24, z: 560}, {t: 7.9, lon: 64, lat: 22, z: 1200},
  {t: 8.9, lon: 73.5, lat: 23.2, z: 4200}, {t: 10.4, lon: 74.4, lat: 23.8, z: 6000}, {t: 11.4, lon: 74.4, lat: 23.9, z: 6300},
]);
const camB = makeCam([{t: 20.05, lon: 73.6, lat: 21.5, z: 3000}, {t: 21.6, lon: 73.0, lat: 21.2, z: 7000}, {t: 22.8, lon: 72.9, lat: 21.15, z: 9500}]);

const SAIL: [number, number][] = [
  [-4.1, 50.35], [-9.5, 43.5], [-16, 31], [-18, 16], [-12, 2], [1, -22], [17, -36], [33, -31], [44, -14], [56, 4], [66, 15], [72.75, 21.1],
];
const SURAT: [number, number] = [72.83, 21.17];
const AJMER: [number, number] = [74.64, 26.45];
// Surat -> Burhanpur -> Mandu -> Ajmer (the road Roe took inland)
const INLAND: [number, number][] = [SURAT, [74.4, 21.25], [76.23, 21.31], [75.4, 22.36], [74.9, 24.4], AJMER];
const sailRoute = catmull(SAIL);
const inlandRoute = catmull(INLAND, 30);

// ---------------------------------------------------------------- map layer
const MapLayer: React.FC<{t: number; second?: boolean}> = ({t, second}) => {
  const cam = second ? camB(t) : camA(t);
  const proj = geoMercator().scale(cam.z).center([cam.lon, cam.lat]).translate([W / 2, H / 2]).clipExtent([[-60, -60], [W + 60, H + 60]]).precision(0.4);
  const path = geoPath(proj);
  const P = (lo: number, la: number) => proj([lo, la]) as [number, number];
  const landD = path(land) || '', indiaD = path(india) || '', gratD = path(graticule) || '';

  const sail = win(t, 5.0, 7.6);
  const si = Math.min(sailRoute.length - 1, Math.floor(sail * (sailRoute.length - 1)));
  const sp = sailRoute.map(([a, b]) => P(a, b));
  const ship = sp[si], prev = sp[Math.max(0, si - 2)], nxt = sp[Math.min(sp.length - 1, si + 2)];
  const ang = (Math.atan2(nxt[1] - prev[1], nxt[0] - prev[0]) * 180) / Math.PI;
  const shipO = win(t, 4.9, 5.4) * (1 - win(t, 7.6, 8.1));

  const ride = win(t, 7.95, 10.55);
  const ri = Math.min(inlandRoute.length - 1, Math.floor(ride * (inlandRoute.length - 1)));
  const ip = inlandRoute.map(([a, b]) => P(a, b));
  const rider = ip[ri];

  const surat = P(...SURAT), ajmer = P(...AJMER);
  const pulse = (t * 0.9) % 1;
  const px = cam.z * 0.01745;
  const grow = win(t, 20.9, 22.5);

  return (
    <AbsoluteFill style={{filter: 'contrast(1.08) saturate(0.92) sepia(0.14)'}}>
      <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{position: 'absolute', inset: 0}}>
        <defs>
          <radialGradient id="rocean" cx="50%" cy="48%" r="75%"><stop offset="0" stopColor="#12384a" /><stop offset="0.6" stopColor="#0a2230" /><stop offset="1" stopColor="#040c12" /></radialGradient>
          <linearGradient id="rland" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#3b3426" /><stop offset="1" stopColor="#241f17" /></linearGradient>
          <filter id="rglow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6" /></filter>
          <clipPath id="rIndia"><path d={indiaD} /></clipPath>
        </defs>
        <rect width={W} height={H} fill="url(#rocean)" />
        <path d={gratD} fill="none" stroke="#5fa3b8" strokeOpacity={0.09} />
        <path d={landD} fill="url(#rland)" stroke="#8a7a55" strokeOpacity={0.55} strokeWidth={1.2} />
        <path d={landD} fill="none" stroke="#caa766" strokeOpacity={0.18} strokeWidth={4} filter="url(#rglow)" />
        <path d={indiaD} fill={GOLD} fillOpacity={0.1 + 0.12 * win(t, 7.5, 9)} stroke={GOLD} strokeOpacity={0.4 + 0.35 * win(t, 7.5, 9)} strokeWidth={1.6} />
        {second && (
          <g opacity={win(t, 20.6, 21.4)}>
            <g clipPath="url(#rIndia)"><circle cx={surat[0]} cy={surat[1]} r={grow * px * 3.2} fill="#c0272d" fillOpacity={0.55} /></g>
            <circle cx={surat[0]} cy={surat[1]} r={grow * px * 3.2} fill="none" stroke="#ff6b5e" strokeOpacity={0.8} strokeWidth={2.2} />
          </g>
        )}
        {!second && (
          <>
            <path d={'M' + sp.map((p) => p.join(',')).join('L')} fill="none" stroke={GOLD} strokeOpacity={0.14} strokeWidth={2} strokeDasharray="2 9" />
            <path d={'M' + sp.slice(0, si + 1).map((p) => p.join(',')).join('L')} fill="none" stroke={GOLD} strokeWidth={5} strokeOpacity={0.25} filter="url(#rglow)" />
            <path d={'M' + sp.slice(0, si + 1).map((p) => p.join(',')).join('L')} fill="none" stroke={GOLD} strokeWidth={2.4} strokeLinecap="round" strokeDasharray="10 7" />
            <path d={'M' + ip.slice(0, ri + 1).map((p) => p.join(',')).join('L')} fill="none" stroke="#fff3d0" strokeWidth={3.2} strokeLinecap="round" strokeDasharray="3 9" opacity={0.95} />
            <g transform={`translate(${ship[0]},${ship[1]})`} opacity={shipO}>
              <circle r={26} fill={GOLD} opacity={0.18} filter="url(#rglow)" />
              <g transform={`scale(${Math.abs(ang) > 90 ? -1.8 : 1.8},1.8)`}>
                <path d="M-15 4 L15 4 L11 10 L-11 10 Z" fill="#1a1208" stroke={GOLD} strokeWidth={1.4} />
                <line x1="0" y1="4" x2="0" y2="-20" stroke={GOLD} strokeWidth={1.6} />
                <path d="M1 -19 Q13 -10 1 1 Z" fill="#f2e8cf" stroke={GOLD} strokeWidth={1} />
                <path d="M-1 -15 Q-10 -8 -1 0 Z" fill="#e9dcbd" stroke={GOLD} strokeWidth={1} />
              </g>
            </g>
            <g transform={`translate(${rider[0]},${rider[1]})`} opacity={win(t, 7.9, 8.3)}>
              <circle r={22} fill={GOLD} opacity={0.3} filter="url(#rglow)" /><circle r={6} fill="#fff3d0" />
            </g>
            <g opacity={win(t, 10.0, 10.5)} transform={`translate(${ajmer[0]},${ajmer[1]})`}>
              {[0, 0.5].map((o, k) => { const p = (pulse + o) % 1; return <circle key={k} r={8 + p * 60} fill="none" stroke="#ff9d5e" strokeWidth={2} opacity={(1 - p) * 0.8} />; })}
              <circle r={7} fill="#ffd9a8" />
            </g>
          </>
        )}
        <g opacity={second ? 1 : win(t, 7.1, 7.6)} transform={`translate(${surat[0]},${surat[1]})`}>
          {[0, 0.5].map((o, k) => { const p = (pulse + o) % 1; return <circle key={k} r={8 + p * 56} fill="none" stroke={GOLD} strokeWidth={2} opacity={(1 - p) * 0.8} />; })}
          <circle r={6} fill="#fff3d0" /><circle r={14} fill={GOLD} opacity={0.35} filter="url(#rglow)" />
        </g>
      </svg>
      {!second && <>
        <MapLabel p={P(-1.5, 52.5)} text="ENGLAND" o={fadeInOut(t, 4.9, 5.4, 5.8, 6.4) * 0.9} dx={-90} dy={-34} />
        <MapLabel p={P(-18, 4)} text="ATLANTIC" o={fadeInOut(t, 5.2, 5.8, 6.4, 7.0) * 0.4} size={34} spacing={20} />
        <MapLabel p={P(...SURAT)} text="SURAT · SEP 1615" o={fadeInOut(t, 7.2, 7.8, 99, 100) * clamp01((cam.z - 900) / 1500)} dx={-250} dy={-4} size={24} />
        <MapLabel p={P(...AJMER)} text="AJMER · THE MUGHAL COURT · JAN 1616" o={win(t, 10.0, 10.7)} dx={0} dy={-52} size={26} spacing={10} />
      </>}
      {second && <MapLabel p={P(...SURAT)} text="SURAT" o={win(t, 20.5, 21.2)} dx={-120} dy={-4} size={30} />}
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- painting helpers
const Drift: (t: number, k: number) => {x: number; y: number} = (t, k) => ({x: Math.sin(t * 0.6) * 9 * k, y: Math.cos(t * 0.45) * 6 * k});

const PImg: React.FC<{src: string; iw: number; ih: number; cx: number; cy: number; z: number; d?: {x: number; y: number}; style?: React.CSSProperties}> = ({src, iw, ih, cx, cy, z, d = {x: 0, y: 0}, style}) => (
  <Img src={staticFile(src)} style={{position: 'absolute', left: W / 2 - cx * iw * z + d.x, top: H / 2 - cy * ih * z + d.y, width: iw * z, height: ih * z, maxWidth: 'none', ...style}} />
);

const lerp = (a: number, b: number, u: number) => a + (b - a) * u;
const Blur: React.FC<{src: string; o?: number; t: number}> = ({src, o = 0.5, t}) => (
  <AbsoluteFill style={{overflow: 'hidden'}}>
    <Img src={staticFile(src)} style={{position: 'absolute', left: -120 + Math.sin(t * 0.3) * 20, top: -400, width: W + 240, height: 'auto', filter: `blur(34px) brightness(${o}) saturate(1.2)`}} />
  </AbsoluteFill>
);

// Painting with Jahangir on a gold halo (Bichitr). Three depth planes: backdrop, floral border, inner scene.
const BichitrScene: React.FC<{t: number}> = ({t}) => {
  const u = clamp01((t - T.bichitr[0]) / (T.darbar[0] - T.bichitr[0] + 0.5));
  const e = ease(u);
  const cx = lerp(0.5, 0.41, e), cy = lerp(0.5, 0.57, e), z = lerp(0.34, 0.60, e);
  const IW = 2474, IH = 3600;
  const inner = 'inset(14.4% 20.8% 16.7% 14.5%)';
  const outer = 'polygon(evenodd, 0 0, 100% 0, 100% 100%, 0 100%, 0 0, 14.5% 14.4%, 14.5% 83.3%, 79.2% 83.3%, 79.2% 14.4%, 14.5% 14.4%)';
  const zi = z * 1.07;
  // ring around King James I (lower left of the inner scene)
  const jx = W / 2 + (0.275 - cx) * IW * zi, jy = H / 2 + (0.655 - cy) * IH * zi;
  const ro = win(t, 12.0, 12.6) * (1 - win(t, 13.4, 13.9));
  return (
    <AbsoluteFill style={{background: INK, filter: 'saturate(1.05) contrast(1.04)'}}>
      <Blur src="roe/bichitr.jpg" o={0.42} t={t} />
      <PImg src="roe/bichitr.jpg" iw={IW} ih={IH} cx={cx} cy={cy} z={z} d={Drift(t, 1)} style={{clipPath: outer, filter: 'drop-shadow(0 20px 40px #000)'}} />
      <PImg src="roe/bichitr.jpg" iw={IW} ih={IH} cx={cx} cy={cy} z={zi} d={Drift(t, -2.2)} style={{clipPath: inner}} />
      <div style={{position: 'absolute', left: jx, top: jy, width: 300, height: 300, transform: 'translate(-50%,-50%)', borderRadius: '50%', border: `3px solid ${GOLD}`, boxShadow: `0 0 40px ${GOLD}aa, inset 0 0 40px ${GOLD}55`, opacity: ro, scale: String(0.8 + 0.2 * ro)}} />
      <div style={{position: 'absolute', left: jx + 180, top: jy - 40, opacity: ro, fontFamily: sans, color: '#f6efdc', textShadow: '0 2px 14px #000'}}>
        <div style={{fontWeight: 600, fontSize: 22, letterSpacing: 5, color: GOLD}}>KING JAMES I OF ENGLAND</div>
        <div style={{fontSize: 18, letterSpacing: 2, opacity: 0.85, marginTop: 4}}>shown at Jahangir's feet, c. 1620</div>
      </div>
    </AbsoluteFill>
  );
};

// Darbar: far plane (balcony) and near plane (crowd) drift at different rates.
const DarbarScene: React.FC<{t: number}> = ({t}) => {
  const u = clamp01((t - T.darbar[0]) / (T.cards[0] - T.darbar[0] + 0.5));
  const e = ease(u);
  const IW = 2327, IH = 4000;
  const cx = lerp(0.47, 0.5, e), cy = lerp(0.2, 0.45, e), z = lerp(0.86, 0.95, e);
  return (
    <AbsoluteFill style={{background: INK, filter: 'saturate(1.05) contrast(1.05) brightness(0.95)'}}>
      <PImg src="roe/darbar.jpg" iw={IW} ih={IH} cx={cx} cy={cy} z={z} d={Drift(t, 0.6)} />
      <PImg src="roe/darbar.jpg" iw={IW} ih={IH} cx={cx} cy={cy} z={z * 1.06} d={Drift(t, -1.6)}
        style={{WebkitMaskImage: 'linear-gradient(to bottom, transparent 0%, transparent 31.6%, #000 32.6%, #000 100%)', maskImage: 'linear-gradient(to bottom, transparent 0%, transparent 31.6%, #000 32.6%, #000 100%)', filter: 'drop-shadow(0 -10px 14px rgba(0,0,0,.6))'}} />
    </AbsoluteFill>
  );
};

const Card: React.FC<{src: string; w: number; h: number; x: number; y: number; t: number; t0: number; rot: number; ph: number; plate: string; sub?: string}> = ({src, w, h, x, y, t, t0, rot, ph, plate, sub}) => {
  const o = win(t, t0, t0 + 0.6) * (1 - win(t, 19.8, 20.3));
  const fy = Math.sin(t * 0.9 + ph) * 8, fx = Math.cos(t * 0.6 + ph) * 5;
  return (
    <div style={{position: 'absolute', left: x + fx, top: y + fy + (1 - o) * 40, width: w, opacity: o, transform: `perspective(1400px) rotateY(${rot}deg)`}}>
      <div style={{padding: 14, background: 'linear-gradient(135deg,#e6c27a,#8b6a2c)', boxShadow: '0 30px 60px rgba(0,0,0,.65), 0 0 0 2px #3a2a0e'}}>
        <Img src={staticFile(src)} style={{width: w - 28, height: h, objectFit: 'cover', display: 'block', filter: 'sepia(0.15) contrast(1.05)'}} />
      </div>
      <div style={{textAlign: 'center', marginTop: 20, fontFamily: sans, fontWeight: 600, fontSize: 20, letterSpacing: 6, color: GOLD, textShadow: '0 2px 12px #000'}}>{plate}</div>
      {sub && <div style={{textAlign: 'center', marginTop: 6, fontFamily: sans, fontSize: 15, letterSpacing: 2, color: '#d9d2c0', opacity: 0.85}}>{sub}</div>}
    </div>
  );
};

const CardsScene: React.FC<{t: number}> = ({t}) => (
  <AbsoluteFill style={{background: INK}}>
    <Blur src="roe/elephant.jpg" o={0.38} t={t * 1.3} />
    <Card src="roe/roe.jpg" w={540} h={620} x={330} y={185} t={t} t0={17.0} rot={7} ph={0} plate="SIR THOMAS ROE" sub="English envoy to the Mughal court" />
    <Card src="roe/dutch.jpg" w={500} h={640} x={1085} y={175} t={t} t0={17.5} rot={-7} ph={2} plate="ROE'S JOURNEY TO JAHANGIR" sub="from a Dutch account" />
  </AbsoluteFill>
);

// Footage: crop of tall-ship masts, graded warm, slow push-in.
const ShipScene: React.FC<{t: number}> = ({t}) => (
  <AbsoluteFill style={{background: INK, overflow: 'hidden'}}>
    <div style={{position: 'absolute', inset: 0, transform: `scale(${1.02 + t * 0.014})`, filter: 'sepia(0.45) saturate(0.7) contrast(1.15) brightness(0.82) hue-rotate(-8deg)'}}>
      <OffthreadVideo src={staticFile('roe/ship.mp4')} muted style={{width: W, height: H, objectFit: 'cover'}} />
    </div>
    <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(10,30,45,.35), rgba(200,120,40,.18))', mixBlendMode: 'multiply'}} />
    <DateStamp text="1615" sub="KING JAMES I SENDS HIS ENVOY" o={fadeInOut(t, 0.5, 1.3, 3.8, 4.6)} />
  </AbsoluteFill>
);

const CREDITS: [number, number, string][] = [
  [0, 4.8, 'FOOTAGE · TALL SHIPS RACES — KAUKO HELAVUO · CC BY 3.0 · WIKIMEDIA COMMONS'],
  [4.8, 10.8, 'MAP DATA · NATURAL EARTH'],
  [10.8, 13.65, 'BICHITR · JAHANGIR PREFERRING A SUFI SHAIKH TO KINGS · PUBLIC DOMAIN · WIKIMEDIA COMMONS'],
  [13.65, 16.75, 'ABU AL-HASAN · JAHANGIR IN DARBAR · PUBLIC DOMAIN · WIKIMEDIA COMMONS'],
  [16.75, 20.05, 'PORTRAIT & DUTCH ACCOUNT · PUBLIC DOMAIN · WIKIMEDIA COMMONS · BACKDROP: FARRUKH CHELA, MET MUSEUM · CC0'],
  [20.05, 99, 'MAP DATA · NATURAL EARTH'],
];

export const RoeScene: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;

  const flash = (c: number) => Math.exp(-Math.pow((t - c) / 0.22, 2));
  const flashO = 0.22 * (flash(T.map[0] + 0.1) + flash(T.bichitr[0] + 0.1) + flash(T.darbar[0] + 0.1) + flash(T.cards[0] + 0.1) + flash(T.foothold[0] + 0.1));
  const sweep = ((t * 0.12) % 1) * 2600 - 700; // slow diagonal light shaft
  const fadeIn = win(t, 0, 0.8), fadeOut = 1 - win(t, ROE_DURATION_S - 0.8, ROE_DURATION_S);
  const sent = sentences.find((s) => t >= s[0].s - 0.15 && t <= s[s.length - 1].e + 0.45);
  const cr = CREDITS.find(([a, b]) => t >= a && t < b);
  const crO = cr ? win(t, cr[0] + 0.3, cr[0] + 0.8) : 0;

  return (
    <AbsoluteFill style={{background: INK, opacity: fadeIn * fadeOut}}>
      <style>{fonts}</style>
      {t < T.map[0] + 0.8 && <ShipScene t={t} />}
      {t >= T.map[0] - 0.1 && t < T.map[1] + 0.2 && <AbsoluteFill style={{opacity: seg(t, T.map[0])}}><MapLayer t={t} /></AbsoluteFill>}
      {t >= T.bichitr[0] - 0.1 && t < T.darbar[1] + 0.2 && <AbsoluteFill style={{opacity: seg(t, T.bichitr[0])}}><BichitrScene t={t} /></AbsoluteFill>}
      {t >= T.darbar[0] - 0.1 && t < T.cards[0] + 0.7 && <AbsoluteFill style={{opacity: seg(t, T.darbar[0])}}><DarbarScene t={t} /></AbsoluteFill>}
      {t >= T.cards[0] - 0.1 && t < T.foothold[0] + 0.7 && <AbsoluteFill style={{opacity: seg(t, T.cards[0])}}><CardsScene t={t} /></AbsoluteFill>}
      {t >= T.foothold[0] - 0.1 && (
        <AbsoluteFill style={{opacity: seg(t, T.foothold[0])}}>
          <MapLayer t={t} second />
          <DateStamp text="1618" sub="TRADING RIGHTS GRANTED AT SURAT" o={fadeInOut(t, 20.5, 21.2, 22.3, 22.8)} red />
        </AbsoluteFill>
      )}

      {/* light: moving shaft + cut flashes, then dust, vignette, grain */}
      <AbsoluteFill style={{pointerEvents: 'none', mixBlendMode: 'screen', opacity: t > 4.8 ? 0.55 : 0.2}}>
        <div style={{position: 'absolute', top: -300, left: sweep, width: 380, height: 1700, transform: 'rotate(18deg)', background: 'linear-gradient(90deg, transparent, rgba(255,214,150,.18), transparent)', filter: 'blur(26px)'}} />
      </AbsoluteFill>
      <AbsoluteFill style={{background: '#ffe6b3', opacity: flashO, mixBlendMode: 'screen', pointerEvents: 'none'}} />
      <Atmosphere t={t} frame={frame} />

      <div style={{position: 'absolute', left: 0, right: 0, top: 0, height: BAR, background: '#000'}} />
      <div style={{position: 'absolute', left: 0, right: 0, bottom: 0, height: BAR, background: '#000'}} />
      {cr && <div style={{position: 'absolute', left: 0, right: 0, top: 0, height: BAR, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: sans, fontSize: 15, letterSpacing: 3, color: '#b9b09a', opacity: crO * 0.9}}>{cr[2]}</div>}
      {sent && <Caption sent={sent} t={t} />}

      <Audio src={staticFile('roe/mix.mp3')} />
    </AbsoluteFill>
  );
};
