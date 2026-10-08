"""Audio -> narration.wav + words.json + segs.json for a new episode.
   python3 tools/prep_audio.py <episode_dir> part1.wav part2.wav ...      (parts are joined with 0.3 s gaps, in the order given)
   python3 tools/prep_audio.py <episode_dir> --only narration.wav        (already one file)
Needs: ffmpeg, numpy, faster-whisper (pip install faster-whisper; model small.en, int8, downloads once).
Writes <episode_dir>/narration.wav, words.json [{w,t0,t1}], segs.json [{id,start}] (clause-cut shots S01..), END.txt (total seconds).
Cuts: at punctuation or pauses >= 0.28 s, shot length 1.6-6.4 s, about 10 words per shot. ALWAYS read segs.json against the
script afterwards and fix by hand (merge a dangling "and", split a long list); the hand fixes are the director's job."""
import sys, os, json, subprocess, wave, numpy as np
SR = 16000
def pcm(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", "44100", "-f", "s16le", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.int16)
def main():
    ep = sys.argv[1]; parts = [a for a in sys.argv[2:] if a != "--only"]; os.makedirs(ep, exist_ok=True)
    gap = np.zeros(int(0.3*44100), np.int16); chunks = []
    for i, p in enumerate(parts): chunks += ([gap] if i and "--only" not in sys.argv else []) + [pcm(p)]
    a = np.concatenate(chunks)
    with wave.open(os.path.join(ep, "narration.wav"), "w") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(44100); w.writeframes(a.tobytes())
    total = len(a)/44100; open(os.path.join(ep, "END.txt"), "w").write(f"{total:.2f}\n")
    from faster_whisper import WhisperModel
    f32 = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(ep, "narration.wav"), "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"], capture_output=True).stdout, np.int16).astype(np.float32)/32768
    segs, _ = WhisperModel("small.en", compute_type="int8").transcribe(f32, word_timestamps=True, language="en", beam_size=1)   # raw array: avoids a PyAV path bug
    words = [dict(w=w.word.strip(), t0=round(w.start, 3), t1=round(w.end, 3)) for s in segs for w in s.words]
    json.dump(words, open(os.path.join(ep, "words.json"), "w"))
    cuts = [0]; n = 0
    for i, w in enumerate(words):
        n += 1; nxt = words[i+1]["t0"] if i + 1 < len(words) else total; pause = nxt - w["t1"]; start = words[cuts[-1]]["t0"]
        length = nxt - start; punct = w["w"][-1:] in ",.;:?!"
        if i + 1 < len(words) and (length >= 6.0 or (length >= 1.6 and n >= 4 and (pause >= 0.28 or punct)) or (n >= 12 and length >= 1.6)):
            cuts.append(i + 1); n = 0
    S = [dict(id=f"S{j+1:02d}", start=round(words[c]["t0"] if j else 0.0, 3)) for j, c in enumerate(cuts)]
    json.dump(S, open(os.path.join(ep, "segs.json"), "w"), indent=0)
    print(f"{total:.1f}s, {len(words)} words, {len(S)} shots, median {np.median(np.diff([s['start'] for s in S]+[total])):.1f}s/shot")
main()
