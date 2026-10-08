"""Extra synthesized SFX (added after Qwen run 1): rocket_rumble, engine_roar. numpy only."""
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
save("rocket_rumble", rocket_rumble()); save("engine_roar", engine_roar())
print("ok")
