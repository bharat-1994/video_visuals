"""Extra synthesized SFX (added after Qwen run 1): rocket_rumble, engine_roar; vietnam ep: metal_clang, stone_crumble, stamp. numpy only."""
import numpy as np, wave, os
SR = 44100; OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sfx")
rng = np.random.default_rng(7)
def lowpass(x, a):  # one-pole
    y = np.empty_like(x); acc = 0.0
    for i, v in enumerate(x): acc += a*(v-acc); y[i] = acc
    return y
def save(name, x):
    x = x/np.abs(x).max()*10**(-3/20); f = int(0.01*SR); x[:f] *= np.linspace(0, 1, f); x[-f*5:] *= np.linspace(1, 0, f*5)
    with wave.open(f"{OUT}/{name}.wav", "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x*32767).astype(np.int16).tobytes())
def rocket_rumble(d=3.0):
    n = int(d*SR); t = np.arange(n)/SR
    body = lowpass(lowpass(rng.standard_normal(n), 0.004), 0.01)*40        # deep roar
    crackle = lowpass(rng.standard_normal(n)*(rng.random(n) < 0.02), 0.2)*3  # popping exhaust crackle
    hiss = lowpass(rng.standard_normal(n), 0.15)*0.25
    env = np.minimum(1, t/0.25)*np.exp(-np.maximum(0, t-1.6)*1.2)          # ignition swell, long tail as it climbs
    thump = np.sin(2*np.pi*45*t)*np.exp(-t*6)*1.5                           # ignition thump
    return (body+crackle+hiss)*env + thump
def engine_roar(d=2.0):
    n = int(d*SR); t = np.arange(n)/SR
    f = 70 + 40*np.minimum(1, t/0.8)                                        # revving up
    ph = 2*np.pi*np.cumsum(f)/SR
    tone = np.sign(np.sin(ph))*0.5 + np.sin(2*ph)*0.3                      # gritty harmonic engine
    noise = lowpass(rng.standard_normal(n), 0.05)*2
    env = np.minimum(1, t/0.15)*np.minimum(1, (d-t)/0.4)
    return lowpass(tone, 0.08)*env*3 + noise*env
def metal_clang(d=1.4):
    """Iron cage slamming shut: inharmonic bar partials + short rattle."""
    n = int(d*SR); t = np.arange(n)/SR
    parts = sum(a*np.sin(2*np.pi*f*t)*np.exp(-t*k) for f, a, k in [(310, 1, 3.5), (847, .6, 5), (1530, .4, 7), (2410, .25, 9), (612, .5, 4)])
    hit = lowpass(rng.standard_normal(n), 0.4)*np.exp(-t*60)*2
    rattle = sum(np.sin(2*np.pi*1900*t)*np.exp(-np.maximum(0, t-o)*40)*(t > o)*.4 for o in (0.09, 0.16, 0.21, 0.25))
    return parts + hit + rattle + np.sin(2*np.pi*55*t)*np.exp(-t*12)*1.2
def stone_crumble(d=2.2):
    """Stone column collapsing: crack snaps, then tumbling block thumps over a gravel bed."""
    n = int(d*SR); t = np.arange(n)/SR; x = np.zeros(n)
    for o in (0.0, 0.07):                                                   # cracks
        m = t >= o; x[m] += lowpass(rng.standard_normal(m.sum()), 0.6)*np.exp(-(t[m]-o)*90)*1.5
    for o, f in [(0.35, 60), (0.6, 48), (0.8, 70), (1.0, 52), (1.15, 40), (1.4, 58)]:   # blocks hitting ground
        m = t >= o; tt = t[m]-o; x[m] += np.sin(2*np.pi*f*tt*(1-tt))*np.exp(-tt*14)*1.6 + lowpass(rng.standard_normal(m.sum()), 0.3)*np.exp(-tt*30)*.6
    gravel = lowpass(rng.standard_normal(n)*(rng.random(n) < 0.05), 0.35)*2*np.exp(-np.maximum(0, t-0.3)*1.6)*(t > 0.3)
    return x + gravel
def stamp(d=0.35):
    """Rubber stamp on paper: dull thunk + papery slap."""
    n = int(d*SR); t = np.arange(n)/SR
    return np.sin(2*np.pi*120*t*(1-t*1.5))*np.exp(-t*25) + lowpass(rng.standard_normal(n), 0.5)*np.exp(-t*80)*.8
if __name__ == "__main__":
    import sys
    want = sys.argv[1:] or ["rocket_rumble", "engine_roar", "metal_clang", "stone_crumble", "stamp"]
    for k in want: save(k, globals()[k]())
    print("ok")
