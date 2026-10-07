# Lakshadweep 1080p master — download & join

The 737 MB video is split into `Lakshadweep_Telugu_1080p24.mp4.part00 … part07` (GitHub's limit is 100 MB per file).
Download **all** parts into one folder, then join them:

**Mac / Linux**
```sh
cat Lakshadweep_Telugu_1080p24.mp4.part* > Lakshadweep_Telugu_1080p24.mp4
```

**Windows (Command Prompt)**
```bat
copy /b Lakshadweep_Telugu_1080p24.mp4.part00+Lakshadweep_Telugu_1080p24.mp4.part01+Lakshadweep_Telugu_1080p24.mp4.part02+Lakshadweep_Telugu_1080p24.mp4.part03+Lakshadweep_Telugu_1080p24.mp4.part04+Lakshadweep_Telugu_1080p24.mp4.part05+Lakshadweep_Telugu_1080p24.mp4.part06+Lakshadweep_Telugu_1080p24.mp4.part07 Lakshadweep_Telugu_1080p24.mp4
```

Check the result with `sha256sum` (Mac/Linux) or `certutil -hashfile Lakshadweep_Telugu_1080p24.mp4 SHA256` (Windows) against `SHA256.txt`.
