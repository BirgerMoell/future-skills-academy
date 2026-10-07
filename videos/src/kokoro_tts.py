"""Batch-synthesize lines with Kokoro (same model/voice as BirgerMoell/voice-agent).
Usage: kokoro_tts.py JOBS.json   where JOBS is {"out.wav": "text", ...}"""
import json
import sys

import numpy as np
import soundfile as sf
from mlx_audio.tts.utils import load_model

jobs = json.load(open(sys.argv[1]))
speed = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
model = load_model("mlx-community/Kokoro-82M-bf16")
for out, text in jobs.items():
    parts = list(model.generate(text=text, voice="af_heart", speed=speed, lang_code="a"))
    audio = np.concatenate([np.asarray(p.audio).squeeze() for p in parts])
    sf.write(out, audio, int(getattr(parts[0], "sample_rate", 24000)))
    print("ok", out, flush=True)
