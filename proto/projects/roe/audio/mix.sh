#!/usr/bin/env bash
# Procedural sound design (no samples) + voiceover, ducked and loudness-normalised.
# usage: mix.sh vo.mp3 out.mp3 total_seconds
set -euo pipefail
VO=$1; OUT=$2; D=${3:-22.8}
ffmpeg -y -loglevel error -i "$VO" \
 -f lavfi -i "anoisesrc=color=pink:d=$D:a=0.6:r=44100" \
 -f lavfi -i "sine=f=98:d=$D:r=44100" -f lavfi -i "sine=f=147:d=$D:r=44100" -f lavfi -i "sine=f=196.5:d=$D:r=44100" -f lavfi -i "sine=f=49:d=$D:r=44100" \
 -f lavfi -i "anoisesrc=color=brown:d=7:a=0.8:r=44100" \
 -f lavfi -i "anoisesrc=color=white:d=0.9:a=0.5:r=44100" \
 -f lavfi -i "aevalsrc='(sin(2*PI*523.25*t)+0.4*sin(2*PI*1046.5*t)+0.15*sin(2*PI*1568*t))*exp(-1.3*t)':d=4:s=44100" \
 -filter_complex "
 [0]adelay=350|350,aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo,apad=whole_dur=$D,asplit=2[vo][vokey];
 [1]lowpass=f=1400,highpass=f=140,tremolo=f=0.16:d=0.7,volume=0.55,afade=t=in:d=0.8,afade=t=out:st=4.0:d=1.8,apad=whole_dur=$D[sea];
 [2][3][4][5]amix=inputs=4:normalize=0,tremolo=f=0.27:d=0.25,volume=0.11,afade=t=in:d=2.5,afade=t=out:st=$(python3 -c "print($D-1.8)"):d=1.8[drone];
 [6]bandpass=f=750:width_type=h:w=900,tremolo=f=3.6:d=0.85,volume=0.5,afade=t=in:d=0.7,afade=t=out:st=5.6:d=1.2,adelay=10500|10500,apad=whole_dur=$D[murmur];
 [7]highpass=f=350,lowpass=f=5000,afade=t=in:d=0.4,afade=t=out:st=0.4:d=0.5,volume=0.28,asplit=5[w1][w2][w3][w4][w5];
 [w1]adelay=4450|4450[a1];[w2]adelay=10450|10450[a2];[w3]adelay=13250|13250[a3];[w4]adelay=16350|16350[a4];[w5]adelay=19650|19650[a5];
 [8]volume=0.35,adelay=20000|20000[bell];
 [sea][drone][murmur][a1][a2][a3][a4][a5][bell]amix=inputs=9:normalize=0,aformat=channel_layouts=stereo,apad=whole_dur=$D[bed];
 [bed][vokey]sidechaincompress=threshold=0.02:ratio=9:attack=15:release=450[ducked];
 [ducked][vo]amix=inputs=2:normalize=0,atrim=0:$D,loudnorm=I=-16:TP=-1.5:LRA=9,afade=t=out:st=$(python3 -c "print($D-0.9)"):d=0.9[out]" \
 -map "[out]" -ar 44100 -b:a 192k "$OUT"
