"""Assemble voice + music + sfx, duck, master. Output: build/out/master.wav (48k/24bit stereo) and master_ln.wav (-16 LUFS)."""
import os, sys, subprocess, json
import numpy as np, scipy.signal as sg
sys.path.insert(0, os.path.dirname(__file__))
from timeline import ACTS, START, SEG, TOTAL
SR = 48000
HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, 'out')
AUD = os.path.join(os.path.dirname(HERE), 'audio')


def load_mp3(path):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).copy()


def peaking(x, f0, gain_db, q=1.0):
    A = 10 ** (gain_db / 40); w0 = 2 * np.pi * f0 / SR; al = np.sin(w0) / (2 * q)
    b = [1 + al * A, -2 * np.cos(w0), 1 - al * A]; a = [1 + al / A, -2 * np.cos(w0), 1 - al / A]
    return sg.lfilter(np.array(b) / a[0], np.array(a) / a[0], x)


def env_follow(x, attack=0.03, release=0.45, rate=200):
    """smoothed amplitude envelope (sampled at SR)."""
    a = np.abs(x)
    # decimate for speed
    hop = SR // rate
    n = len(a) // hop
    e = a[:n * hop].reshape(n, hop).max(axis=1)
    out = np.zeros_like(e); c = 0.0
    ka = np.exp(-1.0 / (attack * rate)); kr = np.exp(-1.0 / (release * rate))
    for i, v in enumerate(e):
        c = ka * c + (1 - ka) * v if v > c else kr * c + (1 - kr) * v
        out[i] = c
    return np.interp(np.arange(len(x)) / hop, np.arange(n), out).astype(np.float32)


def main():
    N = int((TOTAL + 6) * SR)
    voice = np.zeros(N, np.float32)
    for a in ACTS:
        v = load_mp3(os.path.join(AUD, a + '.mp3'))
        # chain: high-pass, warmth, presence, gentle compression
        v = sg.sosfilt(sg.butter(2, 75, 'high', fs=SR, output='sos'), v)
        v = peaking(v, 190, 1.5, 0.9); v = peaking(v, 3200, 2.2, 0.9); v = peaking(v, 9000, -1.5, 0.8)
        i = int(START[a] * SR)
        voice[i:i + len(v)] += v[:N - i]
    # compress: static soft knee
    thr, ratio = 0.12, 2.2
    mag = np.abs(voice)
    gain = np.where(mag > thr, (thr + (mag - thr) / ratio) / np.maximum(mag, 1e-9), 1.0)
    gain = sg.sosfiltfilt(sg.butter(2, 30, 'low', fs=SR, output='sos'), gain)
    voice = voice * gain
    speech = voice[np.abs(voice) > 0.01]
    vrms = np.sqrt(np.mean(speech ** 2))
    voice *= 0.115 / vrms                                 # speech RMS ~ -18.8 dBFS
    print('voice speech rms ->', np.sqrt(np.mean(voice[np.abs(voice) > 0.01] ** 2)))

    music = np.load(os.path.join(OUT, 'music.npy'))[:, :N]
    sfx = np.load(os.path.join(OUT, 'sfx.npy'))[:, :N]
    tp = os.path.join(OUT, 'trans_sfx.npy')
    trans = np.load(tp)[:, :N] if os.path.exists(tp) else None
    # normalise stems (long-term rms), then duck under voice
    def rms(x):
        return np.sqrt(np.mean(x ** 2))
    music *= 0.060 / rms(music)
    sfx *= 0.030 / rms(sfx)
    ve = env_follow(voice, 0.04, 0.55)
    duck_m = 1 - 0.62 * np.clip(ve / 0.06, 0, 1)
    duck_m = sg.sosfiltfilt(sg.butter(2, 3.0, 'low', fs=SR, output='sos'), duck_m).astype(np.float32)
    duck_s = 1 - 0.40 * np.clip(ve / 0.06, 0, 1)
    duck_s = sg.sosfiltfilt(sg.butter(2, 3.0, 'low', fs=SR, output='sos'), duck_s).astype(np.float32)
    mix = music * duck_m[None] + sfx * duck_s[None]
    if trans is not None:
        mix = mix + trans * 0.55 * (0.5 + 0.5 * duck_s[None])
    # voice: centre, with a touch of room
    ir = np.exp(-np.arange(int(0.45 * SR)) / (0.11 * SR)) * np.random.default_rng(1).standard_normal(int(0.45 * SR))
    ir /= np.sqrt(np.sum(ir ** 2))
    room = sg.oaconvolve(voice, ir)[:N] * 0.10
    vst = np.stack([voice + room, voice + np.roll(room, 37)])
    master = mix + vst
    # fade start/end
    fi = int(0.5 * SR); master[:, :fi] *= np.linspace(0, 1, fi)[None]
    fo = int(5.5 * SR); end = int(TOTAL * SR)
    master[:, end - fo:end] *= np.linspace(1, 0, fo)[None] ** 1.4
    master[:, end:] = 0
    master = master[:, :end]
    # gentle soft limiter
    master = np.tanh(master * 0.9) / np.tanh(0.9)
    print('master peak %.3f rms %.3f' % (np.abs(master).max(), rms(master)))
    # stems for later analysis/ducking visuals
    np.save(os.path.join(OUT, 'voice_env.npy'), ve[::SR // 100][:int(TOTAL * 100)].astype(np.float32))
    pcm = (np.clip(master, -1, 1).T * (2 ** 23 - 1)).astype(np.int32)
    # write 24-bit wav through ffmpeg (stdin f32)
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-', '-c:a', 'pcm_s24le',
                          os.path.join(OUT, 'master_raw.wav')], stdin=subprocess.PIPE)
    p.stdin.write(master.T.astype(np.float32).tobytes()); p.stdin.close(); p.wait()
    # loudness normalise (two-pass)
    r = subprocess.run(['ffmpeg', '-v', 'info', '-i', os.path.join(OUT, 'master_raw.wav'), '-af',
                        'loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'], capture_output=True, text=True)
    js = r.stderr[r.stderr.rfind('{'):r.stderr.rfind('}') + 1]
    m = json.loads(js)
    print({k: m[k] for k in ('input_i', 'input_tp', 'input_lra', 'input_thresh')})
    af = ('loudnorm=I=-16:TP=-1.5:LRA=11:measured_I=%s:measured_TP=%s:measured_LRA=%s:measured_thresh=%s:offset=%s:linear=true'
          % (m['input_i'], m['input_tp'], m['input_lra'], m['input_thresh'], m['target_offset']))
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', os.path.join(OUT, 'master_raw.wav'), '-af', af, '-ar', '48000', '-c:a', 'pcm_s24le',
                    os.path.join(OUT, 'master.wav')])
    print('done')


if __name__ == '__main__':
    main()
