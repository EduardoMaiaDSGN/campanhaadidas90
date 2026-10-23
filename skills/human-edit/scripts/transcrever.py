"""Transcrição com tempo de cada palavra (mlx-whisper large-v3-turbo, Apple Silicon).

  python transcrever.py AUDIO_OU_VIDEO saida.json [--prompt "jargões do vídeo, nomes, marcas"]

O prompt ajuda o whisper a escrever certo os termos do assunto (nomes de produtos, ferramentas, marcas).
condition_on_previous_text=False evita que um erro contamine os takes seguintes (o bruto repete muito as frases).
"""
import argparse, json
import mlx_whisper

ap = argparse.ArgumentParser()
ap.add_argument("audio")
ap.add_argument("saida")
ap.add_argument("--prompt", default="")
ap.add_argument("--lingua", default="pt")
A = ap.parse_args()
r = mlx_whisper.transcribe(
    A.audio,
    path_or_hf_repo="mlx-community/whisper-large-v3-turbo",
    language=A.lingua,
    word_timestamps=True,
    condition_on_previous_text=False,
    verbose=False,
    initial_prompt=A.prompt or None,
)
json.dump(r, open(A.saida, "w"), ensure_ascii=False, indent=1)
for i, s in enumerate(r["segments"]):
    print(f"#{i:<3} [{s['start']:7.2f} - {s['end']:7.2f}] {s['text'].strip()}")
