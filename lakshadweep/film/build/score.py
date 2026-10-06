"""Original synthesized score + sound design for the Lakshadweep film.
Run: python3 score.py  ->  build/out/music.npy, sfx.npy (float32, shape (2,N), 48 kHz)
Everything is placed on the master timeline defined in timeline.py."""
import os, sys, functools, time
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import synth as S
from synth import SR, hz, place
from timeline import ACTS, START, SEG, TOTAL, gt

OUT = os.path.join(os.path.dirname(__file__), 'out'); os.makedirs(OUT, exist_ok=True)
N = int((TOTAL + 6) * SR)
rng = np.random.default_rng(5)

music = np.zeros((2, N), np.float32)       # dry music
music_rev = np.zeros((2, N), np.float32)   # music into reverb
sfx = np.zeros((2, N), np.float32)         # dry sfx
sfx_rev = np.zeros((2, N), np.float32)     # sfx into reverb

A = {i + 1: START[a] for i, a in enumerate(ACTS)}     # act global start (voice t=0)


def L(act, local):
    return A[act] + local


# ------------------------------------------------------------------ cached instrument clips
@functools.lru_cache(None)
def c_tanpura(freq, variant):
    return S.tanpura_string(freq, 8.0, seed=variant)


@functools.lru_cache(None)
def c_piano(name, vel):
    return S.piano(hz(name), 5.0, vel)


@functools.lru_cache(None)
def c_bell(name, vel):
    return S.bell(hz(name), 6.0, vel)


@functools.lru_cache(None)
def c_pad(name, dur, vel, bright, vib):
    return S.pad_note(hz(name), dur, vel, bright, vib)


# ------------------------------------------------------------------ musical helpers
def tanpura(t0, t1, vel=0.35, step=1.55):
    """Pa - Sa - Sa - low Sa, looped (key of D)."""
    strings = [110.0, 146.83, 146.83, 73.42]
    t = t0; i = 0
    while t < t1:
        f = strings[i % 4]
        clip = c_tanpura(f, (i % 3) + 1)
        fade = min(1.0, (t - t0) / 4.0, (t1 - t) / 3.0 + 0.2)
        place(music_rev, S.pan(clip, [-0.3, 0.15, -0.1, 0.3][i % 4]), t, vel * max(fade, 0))
        i += 1
        t += step if i % 4 else step * 1.35


def chords(t0, prog, each=8.0, vel=0.5, bright=1400, vib=0.0, overlap=3.0, oct_shift=0):
    for k, ch in enumerate(prog):
        for nm in ch:
            if oct_shift:
                nm = nm[:-1] + str(int(nm[-1]) + oct_shift)
            clip = c_pad(nm, round(each + overlap, 1), vel, bright, vib)
            place(music_rev, clip, t0 + k * each, 1.0)


def piano_seq(t0, notes, vel=0.6, rev=True):
    """notes: [(beat, name, vel_scale)] 1 beat = 1 second"""
    for b, nm, *v in notes:
        vs = v[0] if v else 1.0
        clip = c_piano(nm, round(vel * vs, 2))
        place(music_rev if rev else music, S.pan(clip, rng.uniform(-0.25, 0.25)), t0 + b, 1.0)


def arp(t0, chord, step=0.5, count=16, vel=0.4, pattern=(0, 1, 2, 3, 2, 1), fade_out=True):
    for k in range(count):
        nm = chord[pattern[k % len(pattern)] % len(chord)]
        sc = vel * (0.75 + 0.25 * ((k % 4) == 0))
        if fade_out:
            sc *= 1 - 0.5 * k / count
        clip = c_piano(nm, round(sc, 2))
        place(music_rev, S.pan(clip, rng.uniform(-0.3, 0.3)), t0 + k * step, 1.0)


def flute_seq(t0, notes, vel=0.7, vib=1.0):
    """notes: [(beat, name, dur_beats, [glide_from])]"""
    prev = None
    for b, nm, d, *g in notes:
        gf = hz(g[0]) if g else (hz(prev) * 0.97 if prev and rng.random() < 0.4 else None)
        clip = S.flute(hz(nm), d * 1.0 + 0.25, vel, glide_from=gf, vib=vib)
        place(music_rev, S.pan(clip, 0.15), t0 + b, 1.0)
        prev = nm


def bells_growth(t0, t1, d0=0.2, d1=1.6, scale=('D5', 'E5', 'F#5', 'A5', 'B5', 'D6', 'E6', 'F#6'), vel=0.32, rising=True):
    """accelerating, ascending glass bells = coral growing."""
    t = t0
    while t < t1:
        frac = (t - t0) / (t1 - t0)
        dens = d0 + (d1 - d0) * frac ** 1.3
        lo = int(frac * 3) if rising else 0
        nm = scale[rng.integers(lo, min(len(scale), lo + 5))]
        clip = c_bell(nm, round(vel * rng.uniform(0.55, 1.0), 2))
        place(music_rev, S.pan(clip, rng.uniform(-0.8, 0.8)), t, 1.0)
        t += rng.exponential(1.0 / dens) + 0.05


def pulse(t0, t1, period=1.0, vel=0.35, f=48.0):
    """sub heartbeat"""
    t = t0
    d = S.boom(f * 1.4, f, 1.2, vel)
    while t < t1:
        place(music, d, t, 1.0)
        t += period


def groove(t0, t1, bpm=100.0, vel=0.4, drum=True, shak=True, hi=True):
    beat = 60.0 / bpm
    t = t0; k = 0
    fd = S.frame_drum(0.7); dh = S.dhol_hi(0.5); sh = S.shaker(0.5)
    while t < t1:
        fade = min(1, (t - t0) / 3.0, (t1 - t) / 2.0 + 0.3)
        v = vel * max(fade, 0)
        if drum and k % 8 in (0, 3, 6):
            place(music_rev, S.pan(fd, -0.2), t, v)
        if hi and k % 8 in (2, 5, 7):
            place(music_rev, S.pan(dh, 0.3), t, v * 0.7)
        if shak:
            place(music_rev, S.pan(sh, 0.5 if k % 2 else -0.4), t, v * (0.9 if k % 2 == 0 else 0.55))
        t += beat / 2; k += 1


def hit(t, vel=0.8, f0=90, f1=34, dur=3.5, target='music'):
    (music if target == 'music' else sfx)[:, :] += 0  # no-op, keeps linters quiet
    place(music if target == 'music' else sfx, S.pan(S.boom(f0, f1, dur, vel), 0), t, 1.0)


# ------------------------------------------------------------------ chord library (D Dorian world)
Dm9 = ['D2', 'A2', 'E3', 'F3', 'A3']
Gadd9 = ['G2', 'D3', 'A3', 'B3']
Cmaj7 = ['C3', 'G3', 'B3', 'E4']
Bbmaj7 = ['Bb2', 'F3', 'A3', 'D4']
Am = ['A2', 'E3', 'A3', 'C4']
F = ['F2', 'C3', 'F3', 'A3']
Dsus2 = ['D3', 'A3', 'E4']
Dmaj = ['D2', 'A2', 'F#3', 'A3', 'D4']
Dmaj7 = ['D2', 'A2', 'F#3', 'C#4', 'E4']
Em7 = ['E2', 'B2', 'D3', 'G3']
Bm = ['B2', 'F#3', 'B3', 'D4']
Gmaj = ['G2', 'D3', 'G3', 'B3']
Eb = ['Eb3', 'Bb3', 'G4']
Dm = ['D2', 'A2', 'D3', 'F3', 'A3']

# motifs (beat, note, dur)
MOTIF_A = [(0, 'A4', 2.0), (2.5, 'D5', 1.5), (4, 'E5', 1.0), (5, 'F5', 3.0), (9, 'E5', 1.5), (10.5, 'D5', 4.0)]
MOTIF_B = [(0, 'F5', 1.5), (1.5, 'G5', 1.5), (3, 'A5', 3.0), (6.5, 'G5', 1.5), (8, 'F5', 1.5), (9.5, 'E5', 1.0), (10.5, 'D5', 4.0)]
MOTIF_C = [(0, 'A5', 2.0), (2.5, 'G5', 1.5), (4, 'F5', 2.0), (6.5, 'E5', 1.5), (8, 'D5', 5.0)]
MOTIF_D = [(0, 'D5', 0.5), (0.5, 'F#5', 0.5), (1, 'A5', 1.0), (2, 'G5', 0.5), (2.5, 'F#5', 0.5), (3, 'E5', 1.0),
           (4, 'F#5', 0.5), (4.5, 'A5', 0.5), (5, 'B5', 1.0), (6, 'A5', 2.0)]
MOTIF_E = [(0, 'D5', 1.5), (2, 'F#5', 1.5), (4, 'A5', 3.0), (7.5, 'B5', 1.0), (8.5, 'A5', 1.5), (10, 'F#5', 1.5), (12, 'D5', 5.0)]


def compose():
    t_all = time.time()
    # ================= PRE-ROLL / ACT 1 ================================================
    tanpura(0.6, L(1, 47), vel=0.30)
    music[:, :] += 0
    place(music, S.pan(S.sub(36.7, 8.0, 0.45, a=4.0, r=2.0), 0), 0.0)
    place(music, S.sweep_noise(4.6, 220, 2600, 2.5, 0.22, 'in'), 0.3)
    hit(L(1, 0.0) - 0.05, 0.75, 80, 32, 4.0)
    chords(L(1, 0.0), [Dm9, Gadd9, Dm9, Cmaj7, Dm9, Gadd9], each=8.0, vel=0.42)
    # pulse of piano as the numbers appear
    arp(L(1, 6.2), ['D4', 'A4', 'E5', 'F5'], step=0.75, count=14, vel=0.30)
    arp(L(1, 22.0), ['A3', 'E4', 'A4', 'C5', 'E5'], step=0.5, count=22, vel=0.28, pattern=(0, 1, 2, 3, 4, 3, 2, 1))
    flute_seq(L(1, 23.0), MOTIF_A, vel=0.55)
    place(music_rev, S.sweep_noise(5.5, 300, 5200, 2.0, 0.28, 'in'), L(1, 30.1))
    pulse(L(1, 34.3), L(1, 45.8), 1.0, 0.28)
    place(music_rev, S.sweep_noise(10.0, 200, 7000, 2.0, 0.40, 'in'), L(1, 36.0))
    hit(L(1, 46.1), 0.85, 85, 30, 5.0)

    # ================= ACT 2: formation ================================================
    a = 2
    tanpura(L(a, 0.0), L(a, 31), vel=0.18)
    place(music, S.pan(S.sub(36.7, 30.0, 0.55, a=6.0, r=5.0), 0), L(a, -0.5))
    chords(L(a, 0.0), [Dm9, Dm9, Bbmaj7, Dm9], each=8.0, vel=0.32, bright=900)
    # Mountains form: slow tectonic rumble + low sweep
    hit(L(a, 8.2), 0.8, 70, 28, 6.0)
    place(music, S.sweep_noise(8.0, 60, 400, 1.2, 0.45, 'swell'), L(a, 8.0))
    place(music_rev, S.sweep_noise(6.0, 400, 2800, 2.5, 0.12, 'swell'), L(a, 16.0))
    # polyps: bells that accelerate and climb
    bells_growth(L(a, 23.0), L(a, 46.0), 0.3, 2.0, vel=0.34)
    # mountain sinks
    f_sink = np.concatenate([S.sub(73.4, 4.0, 0.5, a=1.0, r=0.5), S.sub(55.0, 4.0, 0.5, a=0.2, r=3.0)])
    place(music, S.pan(f_sink, 0), L(a, 36.6))
    # ring appears -> warm major
    chords(L(a, 41.0), [Dmaj, Dmaj7, Dmaj], each=7.0, vel=0.46, bright=1700)
    place(music_rev, S.sweep_noise(5.0, 250, 4500, 2.0, 0.3, 'in'), L(a, 43.6))
    flute_seq(L(a, 46.0), [(0, 'F#5', 2.5), (3, 'A5', 3.5), (7, 'E5', 5.0)], vel=0.55)
    hit(L(a, 49.2), 0.65, 75, 30, 5.0)
    piano_seq(L(a, 51.4), [(0, 'D4'), (1.2, 'A4', 0.9), (2.4, 'F#5', 0.9), (3.6, 'E5', 0.8), (5.0, 'D5', 0.8), (7.2, 'A4', 0.6)], vel=0.55)

    # ================= ACT 3: first people =============================================
    a = 3
    tanpura(L(a, -0.5), L(a, 63.7), vel=0.22)
    chords(L(a, 0.0), [Dm9, Gadd9, Dm9, Cmaj7, Dm9, Gadd9, Dm9, Cmaj7], each=8.0, vel=0.34)
    flute_seq(L(a, 3.0), MOTIF_B, vel=0.55)
    groove(L(a, 10.6), L(a, 28.0), bpm=60.0, vel=0.28, hi=False)       # sailors / traders: slow pulse
    # Ubaidullah / tomb: reverent, bare
    chords(L(a, 28.0), [Am, F, Cmaj7, Gmaj], each=3.6, vel=0.36, bright=1100, overlap=2.5)
    piano_seq(L(a, 30.0), [(0, 'A4'), (2.0, 'C5', 0.8), (4.0, 'E5', 0.8), (6.5, 'D5', 0.7), (9.0, 'C5', 0.6)], vel=0.5)
    place(music_rev, S.pan(S.bell(hz('D4'), 7.0, 0.35), 0.0), L(a, 35.8))
    # coconut / coir: gentle, rhythmic, optimistic
    groove(L(a, 48.1), L(a, 62.5), bpm=96.0, vel=0.36)
    arp(L(a, 48.2), ['D4', 'F#4', 'A4', 'B4', 'D5'], step=0.3125, count=44, vel=0.30, pattern=(0, 2, 1, 3, 2, 4, 3, 1), fade_out=False)
    flute_seq(L(a, 50.0), MOTIF_D, vel=0.52)
    chords(L(a, 48.0), [Dmaj, Gmaj, Em7, Dmaj], each=4.0, vel=0.34, bright=1700)

    # ================= ACT 4: rulers, traders, empire ==================================
    a = 4
    tanpura(L(a, -0.5), L(a, 60.6), vel=0.20)
    chords(L(a, 0.0), [Dm, Bbmaj7, Dm, Gadd9], each=8.0, vel=0.38, bright=1000)
    for k in range(0, 16, 4):
        place(music, S.pan(S.frame_drum(0.8, 70, 0.9), 0), L(a, 6.0 + k), 0.35)
    flute_seq(L(a, 12.0), MOTIF_C, vel=0.45)
    # Portuguese arrive: low brass-ish swell + tension
    chords(L(a, 16.0), [['D2', 'A2', 'D3', 'F3', 'Ab3'], ['Bb2', 'F3', 'Db4']], each=7.0, vel=0.40, bright=700, vib=0.8)
    place(music_rev, S.sweep_noise(6.5, 160, 3600, 1.6, 0.33, 'in'), L(a, 23.6))
    hit(L(a, 30.2), 0.9, 95, 36, 4.0)                                    # "the locals did not stay quiet"
    # poison story: sparse eerie glass + low dissonance
    chords(L(a, 31.0), [['Eb2', 'Bb2', 'Gb3', 'D4']], each=9.0, vel=0.30, bright=800, vib=1.0)
    for k, nm in enumerate(['F#6', 'C6', 'Ab5', 'E6', 'Bb5']):
        place(music_rev, S.pan(S.bell(hz(nm), 6.0, 0.18), -0.7 + 0.35 * k), L(a, 33.0 + 1.55 * k))
    # resolve: "did not easily accept"
    place(music, S.pan(S.frame_drum(0.9, 65, 0.9), 0), L(a, 42.7), 0.6)
    place(music, S.pan(S.frame_drum(0.9, 65, 0.9), 0), L(a, 43.9), 0.6)
    place(music, S.pan(S.frame_drum(0.9, 65, 0.9), 0), L(a, 45.1), 0.7)
    chords(L(a, 42.6), [Dm, Dm9], each=7.0, vel=0.48, bright=1500)
    # Tipu -> British: ticking march, fading to stillness
    groove(L(a, 49.0), L(a, 59.0), bpm=88.0, vel=0.22, hi=False, shak=True)
    for k in range(10):
        place(music_rev, S.pan(S.tick(0.35), 0.4), L(a, 49.0 + k * 0.68), 1.0)
    flute_seq(L(a, 53.0), [(0, 'D5', 3.0), (3.5, 'C5', 2.5), (6.5, 'D5', 1.5)], vel=0.4)

    # ================= ACT 5: 1947 =====================================================
    a = 5
    tanpura(L(a, -0.5), L(a, 60.5), vel=0.18)
    piano_seq(L(a, 0.5), [(0, 'D4'), (2.4, 'A4', 0.8), (5.0, 'F4', 0.8), (8.0, 'E4', 0.7), (11.0, 'G4', 0.6)], vel=0.55)
    chords(L(a, 0.0), [Dm9, Gadd9, Dm9], each=8.0, vel=0.30)
    # the problem / distant corner: suspended, lonely flute
    flute_seq(L(a, 6.0), [(0, 'A4', 3.5), (4.5, 'D5', 3.0)], vel=0.42)
    # warning + chase: clock ticks, rising ostinato
    for k in range(int(19.2), int(33.2)):
        place(music_rev, S.pan(S.tick(0.22 + 0.10 * (k - 19) / 14), 0.0), L(a, k) + 0.0, 1.0)
    arp(L(a, 19.3), ['D3', 'A3', 'D4', 'F4', 'A4'], step=0.25, count=54, vel=0.26, pattern=(0, 1, 2, 3, 4, 3, 2, 1), fade_out=False)
    chords(L(a, 19.0), [['D2', 'A2', 'D3', 'F3'], ['Bb2', 'F3', 'D4'], ['G2', 'D3', 'Bb3', 'D4']], each=5.0, vel=0.38, bright=1100)
    place(music_rev, S.sweep_noise(8.0, 200, 6500, 1.8, 0.42, 'in'), L(a, 20.0))
    place(sfx, S.cloth_flap(3.6, 0.55), L(a, 26.4), 1.0)                   # flag raised
    place(music, S.pan(S.frame_drum(0.9, 90, 0.9), 0), L(a, 26.4), 0.7)
    place(music, S.pan(S.frame_drum(0.9, 90, 0.9), 0), L(a, 27.6), 0.7)
    # "by then the flag was already flying" -> triumphant but restrained D major
    hit(L(a, 33.33), 0.75, 80, 31, 5.0)
    chords(L(a, 33.2), [Dmaj, Gmaj, Dmaj7, Bm], each=6.5, vel=0.50, bright=2000)
    flute_seq(L(a, 33.8), MOTIF_E, vel=0.6)
    piano_seq(L(a, 35.6), [(0, 'D4'), (1.0, 'F#4', 0.8), (2.0, 'A4', 0.8), (3.0, 'D5', 0.9)], vel=0.55)
    arp(L(a, 39.8), ['D3', 'A3', 'F#4', 'A4', 'D5'], step=0.5, count=26, vel=0.30)
    flute_seq(L(a, 52.0), MOTIF_A, vel=0.45)

    # ================= ACT 6: island life ==============================================
    a = 6
    tanpura(L(a, -0.5), L(a, 65.4), vel=0.20)
    chords(L(a, 0.0), [Dmaj, Gmaj, Em7, Dmaj, Gmaj, Dmaj7, Bm, Gmaj], each=8.0, vel=0.38, bright=1800)
    flute_seq(L(a, 0.8), MOTIF_D, vel=0.50)
    flute_seq(L(a, 10.8), MOTIF_E, vel=0.46)
    arp(L(a, 14.2), ['D4', 'F#4', 'A4', 'B4', 'D5'], step=0.5, count=24, vel=0.30)
    groove(L(a, 27.2), L(a, 47.5), bpm=100.0, vel=0.40)
    flute_seq(L(a, 28.0), MOTIF_D, vel=0.50)
    arp(L(a, 31.0), ['D4', 'F#4', 'A4', 'B4', 'D5'], step=0.3, count=52, vel=0.26, pattern=(0, 2, 1, 3, 2, 4, 3, 1), fade_out=False)
    groove(L(a, 55.2), L(a, 65.3), bpm=116.0, vel=0.58)
    for k in range(34):
        place(music_rev, S.pan(S.tick(0.30), 0.5 if k % 2 else -0.5), L(a, 55.6 + k * 0.26), 1.0)   # kolkali sticks
    place(music_rev, S.sweep_noise(3.0, 400, 6000, 2.0, 0.20, 'in'), L(a, 60.0))

    # ================= ACT 7: challenges ===============================================
    a = 7
    tanpura(L(a, -0.5), L(a, 4.6), vel=0.20)
    chords(L(a, 0.0), [Dmaj, Gmaj], each=2.4, vel=0.30, bright=1700, overlap=1.0)
    place(music, S.pan(S.sub(36.7, 80.0, 0.50, a=1.0, r=6.0), 0), L(a, 4.4))
    chords(L(a, 4.5), [['D2', 'A2', 'C3', 'F3', 'Ab3'], ['Bb2', 'F3', 'Ab3', 'D4'], ['G2', 'Db3', 'F3', 'B3'], ['D2', 'A2', 'Eb3', 'G3']], each=9.0, vel=0.38, bright=950, vib=0.6)
    pulse(L(a, 6.0), L(a, 24.0), 1.5, 0.22, 44.0)
    flute_seq(L(a, 8.0), MOTIF_C, vel=0.42)
    # bleaching: glass bells fall and die
    for k, nm in enumerate(['A6', 'F#6', 'E6', 'C#6', 'B5', 'A5', 'F#5', 'E5', 'D5', 'A4']):
        place(music_rev, S.pan(S.bell(hz(nm), 6.0, 0.30 * (1 - 0.06 * k)), -0.7 + 0.15 * k), L(a, 24.2 + 1.0 * k + 0.1 * k * k / 6), 1.0)
    # Ockhi
    hit(L(a, 38.5), 0.95, 100, 30, 5.0)
    chords(L(a, 38.4), [['D2', 'A2', 'Eb3', 'Gb3', 'C4'], ['Eb2', 'Bb2', 'Gb3', 'D4']], each=5.0, vel=0.46, bright=1200, vib=1.2)
    for k in range(0, 10):
        place(music, S.pan(S.frame_drum(0.9, 60 + 4 * (k % 3), 0.9), 0), L(a, 38.6 + k * 0.5 + (0 if k < 5 else 0.0)), 0.55)
    place(music_rev, S.sweep_noise(9.0, 150, 5000, 1.5, 0.35, 'swell'), L(a, 38.8))
    # connectivity: calmer, sparse, a hint of digital glints
    chords(L(a, 47.8), [Dm9, Gadd9, Dm9], each=8.5, vel=0.34, bright=1200)
    for k in range(7):
        place(music_rev, S.pan(S.bell(hz(['A5', 'D6', 'E6', 'F6', 'A6', 'E6', 'D6'][k]), 3.0, 0.12), 0.5 - 0.15 * k), L(a, 57.8 + 0.5 * k), 1.0)
    for k in range(9):
        place(music_rev, S.pan(S.tick(0.18), -0.3 + 0.07 * k), L(a, 62.3 + 0.42 * k), 1.0)
    # fresh water: hope
    chords(L(a, 67.2), [Dmaj, Gmaj, Dmaj7], each=4.0, vel=0.46, bright=1900)
    piano_seq(L(a, 67.6), [(0, 'D4'), (0.9, 'F#4', 0.8), (1.8, 'A4', 0.8), (2.7, 'D5', 0.8), (4.5, 'E5', 0.8), (6.0, 'F#5', 0.8), (8.0, 'A5', 0.7)], vel=0.55)
    flute_seq(L(a, 70.0), [(0, 'A5', 3.0), (3.5, 'F#5', 2.0), (6, 'D5', 5.0)], vel=0.48)

    # ================= ACT 8: reflection ===============================================
    a = 8
    tanpura(L(a, -0.5), L(a, 66.5), vel=0.20)
    chords(L(a, 0.0), [Dm9, Bbmaj7, Gadd9, Dm9], each=8.0, vel=0.34)
    piano_seq(L(a, 1.0), [(0, 'D4'), (2.5, 'F4', 0.8), (5.0, 'A4', 0.8), (8.0, 'G4', 0.7), (11.0, 'E4', 0.6)], vel=0.52)
    place(music, S.pan(S.sub(73.4, 12.0, 0.4, a=4.0, r=4.0), 0), L(a, 15.0))   # pressure
    chords(L(a, 16.5), [['D2', 'A2', 'Eb3', 'G3'], Dm9], each=6.0, vel=0.34, bright=900, vib=0.6)
    flute_seq(L(a, 26.4), [(0, 'A4', 2.5), (3, 'D5', 2.0), (5.5, 'F5', 3.0)], vel=0.42)
    chords(L(a, 32.5), [Dmaj, Gmaj], each=6.0, vel=0.44, bright=1700)          # balance found
    bells_growth(L(a, 39.2), L(a, 46.0), 0.5, 2.2, vel=0.32)                    # echo of the coral from act 2
    chords(L(a, 38.8), [Dmaj, Gmaj, Bm, Gmaj], each=5.0, vel=0.52, bright=2100, vib=1.0)
    place(music_rev, S.sweep_noise(6.0, 250, 6000, 1.8, 0.30, 'in'), L(a, 39.8))
    flute_seq(L(a, 46.2), MOTIF_E, vel=0.60)
    piano_seq(L(a, 50.9), [(0, 'D4'), (1.0, 'A4', 0.8), (2.0, 'F#5', 0.8), (3.5, 'E5', 0.8), (5.0, 'D5', 0.9)], vel=0.55)
    hit(L(a, 53.85), 0.7, 80, 30, 6.0)
    chords(L(a, 54.0), [Dmaj, Dmaj7], each=7.0, vel=0.46, bright=1800)
    arp(L(a, 62.7), ['D4', 'F#4', 'A4', 'D5'], step=0.4, count=10, vel=0.3)
    # outro: last flute and silence
    flute_seq(L(a, 68.0), [(0, 'A4', 3.0), (3.5, 'D5', 3.0), (7.0, 'F#5', 6.0)], vel=0.42)
    chords(L(a, 66.8), [Dmaj], each=12.0, vel=0.34, bright=1500, overlap=0.5)
    print('compose %.1fs' % (time.time() - t_all))


# ------------------------------------------------------------------ sound design (environment)
def level_curve(points):
    return S.smooth_env(points, N)


def sound_design():
    t_all = time.time()
    dur = TOTAL + 5
    # ---- ocean bed across the whole film with shaped level ----
    oc = S.ocean(dur, 1.0, 1.0, seed=21)
    ev = [(0, 0.0), (1.0, 0.55), (4.8, 0.65), (L(1, 12), 0.40), (L(1, 28), 0.30), (L(1, 46), 0.50), (A[2] - 0.5, 0.25),
          (L(2, 8), 0.0), (L(2, 40), 0.0), (L(2, 46), 0.30), (L(2, 61), 0.30),
          (A[3], 0.45), (L(3, 28), 0.30), (L(3, 63), 0.45),
          (A[4], 0.28), (L(4, 60), 0.30),
          (A[5], 0.30), (L(5, 60), 0.35),
          (A[6], 0.55), (L(6, 27), 0.40), (L(6, 65), 0.45),
          (A[7], 0.50), (L(7, 22), 0.22), (L(7, 38), 0.30), (L(7, 48), 0.50), (L(7, 78), 0.34),
          (A[8], 0.34), (L(8, 40), 0.22), (L(8, 62), 0.40), (TOTAL - 8.0, 0.45), (TOTAL, 0.0)]
    ev.sort()
    oc *= level_curve(ev)[None, :len(oc[0])] if oc.shape[1] <= N else 1
    place(sfx_rev, oc * 0.05, 0.0)
    place(sfx, oc * 0.62, 0.0)
    # ---- wind ----
    w = S.wind(dur, 1.0, 0.7, seed=22)
    wl = [(0, 0.0), (1, 0.12), (A[1] + 10, 0.10), (A[1] + 40, 0.06), (A[2], 0.0),
          (A[4] + 15, 0.10), (A[4] + 35, 0.12), (A[4] + 52, 0.06), (A[5], 0.10), (L(5, 20), 0.14), (L(5, 31), 0.22), (L(5, 34), 0.10), (L(5, 60), 0.10),
          (A[6], 0.10), (L(6, 30), 0.14), (A[7], 0.10), (L(7, 4.6), 0.18), (L(7, 22), 0.30), (L(7, 38), 0.55), (L(7, 44), 0.95), (L(7, 49), 0.20), (L(7, 78), 0.10),
          (A[8], 0.10), (TOTAL - 6, 0.12), (TOTAL, 0.0)]
    wl.sort()
    w *= level_curve(wl)[None, :w.shape[1]]
    place(sfx, w, 0.0)
    # ---- underwater world: Act 2 (polyps/ridge) + Act 7 (bleaching) ----
    uw = S.underwater(80.0, 1.0, 6)
    c = np.ones(uw.shape[1], np.float32)
    ux = S.smooth_env([(0, 0), (L(2, 8) - A[2] + 0, 0.0)], 10)
    for (t0, t1, lv) in [(L(2, 4), L(2, 48), 0.55)]:
        seg = uw[:, :int((t1 - t0) * SR)] * lv
        seg *= S.smooth_env([(0, 0), (4, 1), (t1 - t0 - 5, 1), (t1 - t0, 0)], seg.shape[1])[None, :]
        place(sfx, seg, t0)
    seg = uw[:, :int(18 * SR)] * 0.45
    seg *= S.smooth_env([(0, 0), (3, 1), (14, 1), (18, 0)], seg.shape[1])[None, :]
    place(sfx, seg, L(7, 22.5))
    seg = uw[:, :int(14 * SR)] * 0.45
    seg *= S.smooth_env([(0, 0), (3, 1), (11, 1), (14, 0)], seg.shape[1])[None, :]
    place(sfx, seg, L(8, 37.5))

    # ---- gulls (sparse) ----
    for tg, f0, v, p in [(L(1, 2.0), 1650, 0.14, -0.5), (L(1, 14.0), 1800, 0.12, 0.6), (L(1, 27.5), 1500, 0.13, -0.3),
                         (L(3, 4.0), 1700, 0.12, 0.4), (L(3, 22.0), 1550, 0.11, -0.6), (L(6, 3.0), 1750, 0.12, 0.5),
                         (L(6, 38.0), 1600, 0.14, -0.4), (L(6, 45.0), 1850, 0.12, 0.7), (L(8, 62.0), 1650, 0.10, 0.3),
                         (L(5, 5.0), 1500, 0.10, -0.2), (A[8] + 14.5, 1700, 0.10, 0.5)]:
        place(sfx_rev, S.pan(S.gull(f0, 1.1, v), p), tg)
        place(sfx, S.pan(S.gull(f0, 1.1, v), p), tg, 0.5)

    # ---- map pings (intro) ----
    for tp in [L(1, 6.3), L(1, 8.95), L(1, 11.2), L(1, 14.0), L(1, 18.6), L(1, 22.2)]:
        place(sfx_rev, S.pan(S.ping(1175, 0.16), 0.2), tp)
    for tp, fq in [(L(2, 16.2), 880), (L(3, 36.0), 660), (L(7, 49.9), 1175), (L(7, 52.5), 1480)]:
        place(sfx_rev, S.pan(S.ping(fq, 0.18), 0.0), tp)

    # ---- act 3: boats + creak, coconut/rope ----
    for tc in [L(3, 3.0), L(3, 12.0), L(3, 20.5), L(3, 52.0), L(3, 57.5)]:
        place(sfx_rev, S.pan(S.creak(1.0, 0.16, 210 + rng.uniform(-40, 40)), rng.uniform(-0.5, 0.5)), tc)
    # ---- act 4: ships ----
    for tc in [L(4, 3.0), L(4, 17.0), L(4, 21.0), L(4, 25.0), L(4, 53.0)]:
        place(sfx_rev, S.pan(S.creak(1.2, 0.18, 170 + rng.uniform(-30, 30)), rng.uniform(-0.6, 0.6)), tc)
    for tp in [L(4, 46.0), L(4, 50.0), L(4, 54.0)]:
        place(sfx_rev, S.pan(S.paper_flutter(0.7, 0.12), 0.3), tp)
    # ---- act 5: paper / newsreel flutter, ship horn ----
    for tp in [L(5, 0.5), L(5, 2.0), L(5, 3.5)]:
        place(sfx_rev, S.pan(S.paper_flutter(0.7, 0.18), rng.uniform(-0.4, 0.4)), tp)
    # ---- act 6: fishing splashes & pulls ----
    for k, tp in enumerate([35.5, 36.7, 37.9, 39.0, 40.2, 41.2]):
        place(sfx_rev, S.pan(S.splash(0.28), rng.uniform(-0.5, 0.5)), L(6, tp))
    for tp in [34.0, 36.0, 38.5, 40.5]:
        place(sfx_rev, S.pan(S.creak(0.8, 0.14, 260), 0.2), L(6, tp))
    # ---- act 7: storm ----
    rn = S.rain(14.0, 1.0)
    rn *= S.smooth_env([(0, 0), (2, 0.7), (11, 1.0), (14, 0)], rn.shape[1])[None, :]
    place(sfx, rn * 0.75, L(7, 38.0))
    for tp, v, seed in [(L(7, 38.5), 0.6, 9), (L(7, 41.6), 0.55, 10), (L(7, 44.3), 0.5, 11)]:
        place(sfx_rev, S.pan(S.thunder(5.0, v, seed), 0), tp)
        place(sfx, S.pan(S.thunder(5.0, v * 0.6, seed), 0), tp)
    # plane flyover (jet-ish whoosh) + ship horn
    place(sfx_rev, S.pan(S.sweep_noise(9.0, 300, 900, 1.2, 0.22, 'swell'), 0.0), L(7, 50.6))
    horn = (S.sub(98, 3.0, 0.3, a=0.2, r=1.2) + S.sub(147, 3.0, 0.18, a=0.2, r=1.2))
    place(sfx_rev, S.pan(horn, 0.3), L(7, 54.8))
    # water drips for desalination
    for k in range(10):
        place(sfx_rev, S.pan(S.bubbles(0.5, 3.0, 0.2, 100 + k), rng.uniform(-0.5, 0.5)), L(7, 69.2 + 0.9 * k))
    print('sound design %.1fs' % (time.time() - t_all))


def finish():
    t_all = time.time()
    ir_m = S.make_ir(4.2, seed=4, bright=0.5)
    ir_s = S.make_ir(2.4, seed=8, bright=0.45)
    m = music + S.reverb(music_rev, ir_m, 0.85) + music_rev * 0.35
    s = sfx + S.reverb(sfx_rev, ir_s, 0.7) + sfx_rev * 0.5
    np.save(os.path.join(OUT, 'music.npy'), m.astype(np.float32))
    np.save(os.path.join(OUT, 'sfx.npy'), s.astype(np.float32))
    print('reverb+save %.1fs  music peak %.2f rms %.3f | sfx peak %.2f rms %.3f' % (
        time.time() - t_all, np.abs(m).max(), np.sqrt((m ** 2).mean()), np.abs(s).max(), np.sqrt((s ** 2).mean())))


if __name__ == '__main__':
    compose()
    sound_design()
    finish()
