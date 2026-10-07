"""Wire the videos into the website. Idempotent: safe to re-run after adding videos.

 - injects a click-to-play poster into each lesson that has a practice video
 - (re)generates videos.html (gallery, filter by track)
 - adds a "Videos" nav link and a home-page teaser
Run web.py first so assets/video/ exists.
"""
import html
import os
import re
import subprocess

from practice import LESSONS, TRACKS

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
VID = os.path.join(ROOT, "assets", "video")

INTRO = [
    ("01-judgment-is-the-bottleneck", "When intelligence is abundant, judgment is the bottleneck",
     "The thesis behind the academy in under a minute."),
    ("02-five-skills-that-dont-expire", "Five skills that don't expire",
     "The five tracks and what each one trains."),
    ("03-learn-drill-ship", "Learn it. Drill it. Ship it.", "How every lesson, module and track works."),
    ("04-three-habits-that-never-expire", "Three habits that never expire",
     "Verify everything. Own the outcome. Play long games."),
]


def read(p):
    return open(os.path.join(ROOT, p)).read()


def write(p, s):
    open(os.path.join(ROOT, p), "w").write(s)


def secs(slug):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1",
                                   os.path.join(VID, slug + ".mp4")])
    return round(float(out))


def player(slug, base, label, dur):
    return (f'<div class="video-frame" data-video="{base}assets/video/{slug}.mp4" data-slug="{slug}">'
            f'<button class="video-play" type="button" aria-label="Play: {html.escape(label, quote=True)} ({dur} seconds)">'
            f'<img src="{base}assets/video/{slug}.jpg" alt="" loading="lazy" width="270" height="480" />'
            f'<span class="video-play-icon" aria-hidden="true"></span>'
            f'<span class="video-dur">{dur // 60}:{dur % 60:02d}</span></button></div>')


# ------------------------------------------------------------ lesson pages
lessons = []  # (n, slug, id, key, title)
for n, (lid, slug, *_rest) in enumerate(LESSONS, 1):
    key = lid.rsplit("-", 2)[0]
    page = f"tracks/{TRACKS[key][1]}.html"
    src = read(page)
    m = re.search(rf'<details class="lesson" id="{lid}".*?<span class="lesson-title">([^<]*)</span>', src, re.S)
    title = html.unescape(m.group(1))
    no = ".".join(lid.rsplit("-", 2)[1:])
    vslug = f"{n:02d}-{slug}"
    lessons.append((n, vslug, lid, key, title, no, secs(vslug)))

for key, (name, page) in TRACKS.items():
    path = f"tracks/{page}.html"
    src = read(path)
    for n, vslug, lid, k, title, no, dur in lessons:
        if k != key:
            continue
        fig = (f'<figure class="lesson-video" data-lesson-video="{lid}">{player(vslug, "../", title, dur)}'
               f'<figcaption>Watch the idea and the practice in {dur} seconds.</figcaption></figure>')
        pat = re.compile(rf'(<details class="lesson" id="{lid}".*?<div class="lesson-body">)(\s*<figure class="lesson-video".*?</figure>)?', re.S)
        src, c = pat.subn(lambda m: m.group(1) + "\n                " + fig, src, count=1)
        assert c == 1, lid
    if 'href="../videos.html"' not in src:
        src = src.replace('<a class="nav-cta" href="../for-companies.html">', '<a href="../videos.html">Videos</a>\n        <a class="nav-cta" href="../for-companies.html">')
    write(path, src)

# ---------------------------------------------------------------- nav links
for path in ("index.html", "for-companies.html"):
    src = read(path)
    if 'href="videos.html"' not in src:
        src = src.replace('<a href="for-companies.html">For companies</a>', '<a href="videos.html">Videos</a>\n        <a href="for-companies.html">For companies</a>', 1)
        src = src.replace('<a class="nav-cta" href="for-companies.html">', '<a href="videos.html">Videos</a>\n        <a class="nav-cta" href="for-companies.html">', 1) if 'href="videos.html"' not in src else src
    write(path, src)

# ----------------------------------------------------------- home teaser
src = read("index.html")
teaser = f'''<!-- watch:start -->
      <section class="watch wrap" id="watch">
        <div class="watch-grid">
          <div class="reveal">
            {player(INTRO[0][0], "", INTRO[0][1], secs(INTRO[0][0]))}
          </div>
          <div>
            <p class="section-note reveal">Watch</p>
            <h2 class="section-title reveal">The idea in a minute. The practice in ten.</h2>
            <p class="section-lede reveal">
              Short videos for every track: the thesis, the method, and bite-sized practice clips
              that turn a single lesson into something you can do today.
            </p>
            <a class="btn reveal" href="videos.html">See all videos →</a>
          </div>
        </div>
      </section>
      <!-- watch:end -->
'''
if "<!-- watch:start -->" in src:
    src = re.sub(r"<!-- watch:start -->.*?<!-- watch:end -->\n", lambda m: teaser, src, flags=re.S)
else:
    src = src.replace('      <section class="pillars" id="tracks">', teaser + '\n      <section class="pillars" id="tracks">', 1)
write("index.html", src)

# ------------------------------------------------------------- gallery page
cards = []
for slug, title, blurb in INTRO:
    cards.append(f'''<article class="vcard" data-track="intro">
            {player(slug, "", title, secs(slug))}
            <h3>{html.escape(title)}</h3>
            <p>{html.escape(blurb)}</p>
          </article>''')
intro_html = "\n          ".join(cards)
by_track = {}
for n, vslug, lid, k, title, no, dur in lessons:
    by_track.setdefault(k, []).append(f'''<article class="vcard" data-track="{k}">
            {player(vslug, "", title, dur)}
            <span class="vcard-tag">{TRACKS[k][0]} · {no}</span>
            <h3>{html.escape(title)}</h3>
            <a class="vcard-link" href="tracks/{TRACKS[k][1]}.html#{lid}">Read the lesson →</a>
          </article>''')
filters = '<button type="button" class="vfilter is-active" data-filter="all">All</button>' + "".join(
    f'<button type="button" class="vfilter" data-filter="{k}">{TRACKS[k][0]}</button>' for k in TRACKS)
practice_html = "\n          ".join("\n          ".join(v) for v in by_track.values())

head = read("for-companies.html").split("<body>")[0]
head = re.sub(r"<title>.*?</title>", "<title>Videos — Future Skills Academy</title>", head, flags=re.S)
head = re.sub(r'<link rel="canonical"[^>]*>', '<link rel="canonical" href="https://futureskillsacademy.ai/videos.html" />', head)
head = re.sub(r'(<meta\s+name="description"\s+content=")[^"]*', r"\1Short videos from Future Skills Academy: the thesis, the method, and bite-sized practice clips from the lessons.", head, flags=re.S)
head = re.sub(r'(<meta property="og:url" content=")[^"]*', r"\1https://futureskillsacademy.ai/videos.html", head)
head = re.sub(r'(<meta property="og:title" content=")[^"]*', r"\1Videos — Future Skills Academy", head)
head = re.sub(r'(<meta name="twitter:title" content=")[^"]*', r"\1Videos — Future Skills Academy", head)
for attr in ('property="og:description"', 'name="twitter:description"'):
    head = re.sub(rf'(<meta {attr} content=")[^"]*', r"\1Short videos from Future Skills Academy: the thesis, the method, and bite-sized practice clips.", head)
header = re.search(r"<header.*?</header>", read("index.html"), re.S).group(0)
header = header.replace('href="#thesis"', 'href="index.html#thesis"').replace('href="#tracks"', 'href="index.html#tracks"') \
    .replace('href="#method"', 'href="index.html#method"').replace('href="#join"', 'href="index.html#join"')
page = f'''{head}<body>
    {header}

    <main>
      <section class="wrap videos-hero">
        <p class="section-note reveal">Videos</p>
        <h1 class="reveal">Short lessons you can <span class="accent">watch</span> and then do.</h1>
        <p class="hero-lede reveal">
          Start with the four introductions, then pick a track. Each practice clip is under a minute:
          one idea from a lesson, and the exercise that makes it stick.
        </p>
      </section>

      <section class="wrap videos-section">
        <h2 class="section-title reveal">Start here</h2>
        <div class="vgrid">
          {intro_html}
        </div>
      </section>

      <section class="wrap videos-section">
        <h2 class="section-title reveal">Practice clips</h2>
        <div class="vfilters" role="group" aria-label="Filter by track">{filters}</div>
        <div class="vgrid" data-vgrid>
          {practice_html}
        </div>
      </section>
    </main>

    <footer>
      <span>Future Skills Academy</span>
      <span>Member of Technical Staff · High Agency · Taste · Relationships · Communication</span>
      <span>Stockholm / 2026</span>
    </footer>

    <script data-goatcounter="https://futureskillsacademy.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>
    <script src="script.js"></script>
  </body>
</html>
'''
write("videos.html", page)
print("lessons with video:", len(lessons))
