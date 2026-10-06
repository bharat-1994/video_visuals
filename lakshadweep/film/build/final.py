import subprocess, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = os.path.join(ROOT, 'build/out/video_silent.mp4'); A = os.path.join(ROOT, 'build/out/master.wav')
OUT = os.path.join(ROOT, 'out'); os.makedirs(OUT, exist_ok=True)
main = os.path.join(OUT, 'Lakshadweep_Telugu_1080p24.mp4')
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', V, '-i', A, '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-movflags', '+faststart', '-shortest', main], check=True)
prev = os.path.join(OUT, 'Lakshadweep_Telugu_720p_preview.mp4')
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', main, '-vf', 'scale=1280:720:flags=lanczos', '-c:v', 'libx264', '-preset', 'medium', '-crf', '27', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', prev], check=True)
for f in (main, prev):
    print(f, os.path.getsize(f) // 1048576, 'MB')
