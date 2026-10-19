#!/bin/bash
# Prepara un clip real (celular) para meterlo en un reel HTML: lo corta, lo lleva a 1080x1920
# (recorte al centro si vino horizontal) y lo pasa a cuadros JPG a 30 fps.
#
# Uso:  scripts/preparar-clip.sh video.mp4 [inicio_seg=0] [duracion_seg=6]
# Sale: produccion/sintetico/img/clip/0001.jpg … (no se commitea) y el comando de render listo.
set -e
entrada="$1"; ini="${2:-0}"; dur="${3:-6}"
[ -f "$entrada" ] || { echo "Uso: $0 video.mp4 [inicio_seg] [duracion_seg]"; exit 1; }
raiz="$(cd "$(dirname "$0")/.." && pwd)"; dir="$raiz/produccion/sintetico/img/clip"
rm -rf "$dir"; mkdir -p "$dir"
ffmpeg -v error -ss "$ini" -t "$dur" -i "$entrada" \
  -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30" -q:v 3 "$dir/%04d.jpg"
n=$(ls "$dir" | wc -l)
IFS=x read w h < <(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 "$entrada")
[ "$w" -gt "$h" ] && echo "  ojo: el clip es horizontal (${w}x${h}); se recortó al centro."
echo "  $n cuadros en produccion/sintetico/img/clip/"
echo "  render: node scripts/render-reel.mjs produccion/sintetico/reel-experiencia-v5.html produccion/sintetico/out/video1-con-clip.mp4 --v 3 --q \"clip=img/clip&clipn=$n\""
