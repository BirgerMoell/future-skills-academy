"""Make web-sized copies + posters in assets/video/ from the 1080p masters."""
import glob
import os
import subprocess

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "assets", "video")
os.makedirs(OUT, exist_ok=True)
masters = sorted(glob.glob(os.path.join(ROOT, "videos", "*.mp4")) + glob.glob(os.path.join(ROOT, "videos", "practice", "*.mp4")))
for m in masters:
    slug = os.path.basename(m)[:-4]
    mp4 = os.path.join(OUT, slug + ".mp4")  # posters come from make.py/practice.py --posters
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", m, "-vf", "scale=720:1280", "-c:v", "libx264", "-preset", "slow",
                    "-crf", "26", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", mp4], check=True)
    print(slug, round(os.path.getsize(mp4) / 1e6, 2), "MB")
