"""Export YouTube upload metadata for every video.

Writes videos/youtube/metadata.csv (+ metadata.json) and creates assets/video/youtube.json,
the slug -> YouTube video id manifest the site reads (null until uploaded).
Run site.py afterwards to rebuild pages from the manifest.
"""
import csv
import html
import json
import os
import re
import subprocess

from practice import LESSONS, TRACKS

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "videos", "youtube")
MANIFEST = os.path.join(ROOT, "assets", "video", "youtube.json")
CHANNEL = "UCdkq80e5NReDp23mxIa4vcw"
SITE = "https://futureskillsacademy.ai"
TAGS = ["AI skills", "future skills", "AI", "learning", "career", "Future Skills Academy"]
TRACK_TAG = {"mts": "AI engineering", "agency": "leadership", "taste": "design taste", "rel": "sales and relationships", "comm": "communication"}

INTRO = [
    ("01-judgment-is-the-bottleneck", "When intelligence is abundant, judgment is the bottleneck",
     "AI made execution cheap. What stays scarce is the human layer: judgment, agency, taste, trust and clarity."),
    ("02-five-skills-that-dont-expire", "Five skills that don't expire in the age of AI",
     "The five tracks of Future Skills Academy and what each one trains."),
    ("03-learn-drill-ship", "Learn it. Drill it. Ship it.", "How every lesson, module and track works: short lessons, practice on real stakes, and a capstone you can show."),
    ("04-three-habits-that-never-expire", "Three habits that never expire",
     "Verify everything. Own the outcome. Play long games."),
]


def duration(slug):
    p = os.path.join(ROOT, "assets", "video", slug + ".mp4")
    return round(float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", p])))


rows = []
for slug, title, blurb in INTRO:
    rows.append(dict(slug=slug, file=f"videos/{slug}.mp4", title=title[:100], playlist="Start here", seconds=duration(slug),
                     description=f"{blurb}\n\nFuture Skills Academy teaches the five skills that compound in an AI-native world. Free lessons and practice: {SITE}\n\n#Shorts #AI #FutureSkills",
                     tags=", ".join(TAGS)))
for n, (lid, slug, hook, ideas, steps, _say) in enumerate(LESSONS, 1):
    key = lid.rsplit("-", 2)[0]
    name, page = TRACKS[key]
    no = ".".join(lid.rsplit("-", 2)[1:])
    src = open(os.path.join(ROOT, "tracks", page + ".html")).read()
    lesson_title = html.unescape(re.search(rf'id="{lid}".*?lesson-title">([^<]*)<', src, re.S).group(1))
    vslug = f"{n:02d}-{slug}"
    plain = lambda s: s.replace("*", "")
    desc = (f"{plain(ideas[0][0])}\n\nTry it:\n" + "\n".join(f"{i}. {plain(s)}" for i, s in enumerate(steps, 1)) +
            f"\n\nRead the full lesson (free): {SITE}/tracks/{page}.html#{lid}\n"
            f"{name}, lesson {no}, from Future Skills Academy: {SITE}\n\n#Shorts #AI #{TRACK_TAG[key].replace(' ', '')}")
    rows.append(dict(slug=vslug, file=f"videos/practice/{vslug}.mp4", title=f"{lesson_title}: a practice from {name}"[:100],
                     playlist=name, seconds=duration(vslug), description=desc, tags=", ".join(TAGS + [TRACK_TAG[key], name])))

os.makedirs(OUT, exist_ok=True)
with open(os.path.join(OUT, "metadata.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
json.dump(rows, open(os.path.join(OUT, "metadata.json"), "w"), indent=1, ensure_ascii=False)

manifest = json.load(open(MANIFEST)) if os.path.exists(MANIFEST) else {}
manifest = {r["slug"]: manifest.get(r["slug"]) for r in rows}
json.dump(manifest, open(MANIFEST, "w"), indent=1)
print(len(rows), "videos;", max(len(r["title"]) for r in rows), "max title len;", max(len(r["description"]) for r in rows), "max desc len")
