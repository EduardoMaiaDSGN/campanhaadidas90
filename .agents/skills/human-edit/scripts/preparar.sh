#!/bin/zsh
# Prepara o ambiente da Human Edit (uma vez por máquina; rodar de novo é inofensivo).
#  - Python 3.12 num venv fora de pastas temporárias: ~/Library/Caches/human-edit/venv
#  - numpy, pillow, opencv (sem GUI), scipy e mlx-whisper (transcrição local no Apple Silicon)
#  - detector de rosto da Apple (Vision) compilado ao lado dos scripts: scripts/faces
# Pré-requisitos: macOS em Apple Silicon, ffmpeg (brew install ffmpeg), uv (brew install uv), Xcode Command Line Tools.
set -e
DIR="${0:A:h}"
VENV="$HOME/Library/Caches/human-edit/venv"
command -v ffmpeg >/dev/null || { echo "falta o ffmpeg: brew install ffmpeg"; exit 1; }
command -v uv >/dev/null || { echo "falta o uv: brew install uv"; exit 1; }
if [[ ! -x "$VENV/bin/python" ]]; then
  mkdir -p "${VENV:h}"
  uv venv -q --python 3.12 "$VENV"
fi
uv pip install -q --python "$VENV/bin/python" numpy pillow "opencv-python-headless<5" scipy mlx-whisper
if [[ ! -x "$DIR/faces" || "$DIR/faces.swift" -nt "$DIR/faces" ]]; then
  swiftc -O "$DIR/faces.swift" -o "$DIR/faces"
fi
"$VENV/bin/python" -c "import cv2, PIL, numpy, scipy, mlx_whisper; print('ok: python', __import__('sys').version.split()[0], '| opencv', cv2.__version__)"
echo "python da skill: $VENV/bin/python"
