"""Tiny kinetic-typography video engine for Future Skills Academy.

Frames are drawn with Pillow, narration comes from macOS `say`, an ambient pad
is synthesised with numpy, and ffmpeg muxes everything. No external assets
besides the logo files already in /assets.
"""
import math
import os
import re
import subprocess
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ASSETS = os.path.join(ROOT, "assets")

W, H, FPS = 1080, 1920, 30
MARGIN = 96
CENTER_Y = 860

BONE = (251, 248, 244)
PLUM = (51, 36, 50)
CARMINE = (189, 40, 72)
ROSE = (201, 106, 112)
BLUSH = (232, 183, 173)

SERIF = "/System/Library/Fonts/Supplemental/Georgia.ttf"
SERIF_I = "/System/Library/Fonts/Supplemental/Georgia Italic.ttf"
SANS = "/System/Library/Fonts/HelveticaNeue.ttc"

_fonts = {}


def font(path, size, index=0):
    key = (path, size, index)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(path, size, index=index)
    return _fonts[key]


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease_out(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def ease_io(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


# ---------------------------------------------------------------- text layout
def layout(markup, size, maxw, align="left", lead=1.16):
    """*accent* words render as carmine italic. Returns (words, height)."""
    f_r, f_i = font(SERIF, size), font(SERIF_I, size)
    space = f_r.getlength(" ")
    toks, acc = [], False
    for raw in markup.replace("\n", " \n ").split(" "):
        if raw == "":
            continue
        if raw == "\n":
            toks.append(("\n", False))
            continue
        a, w = acc, raw
        if w.startswith("*"):
            acc, a, w = True, True, w[1:]
        if w.endswith("*"):
            acc, w = False, w[:-1]
        toks.append((w, a))
    lines, cur, curw = [], [], 0
    for w, a in toks:
        if w == "\n":
            lines.append((cur, curw))
            cur, curw = [], 0
            continue
        wl = (f_i if a else f_r).getlength(w)
        if cur and curw + space + wl > maxw:
            lines.append((cur, curw))
            cur, curw = [], 0
        cur.append((w, a, wl))
        curw += wl + (space if len(cur) > 1 else 0)
    lines.append((cur, curw))
    words, y = [], 0
    for line, lw in lines:
        x = {"left": 0, "center": (maxw - lw) / 2}[align]
        for w, a, wl in line:
            f = f_i if a else f_r
            pad = size // 3
            m = Image.new("L", (int(wl) + pad * 2, int(size * 1.5)), 0)
            ImageDraw.Draw(m).text((pad, int(size * 0.1)), w, font=f, fill=255)
            words.append(dict(mask=m, pad=pad, x=x, y=y, accent=a))
            x += wl + space
        y += size * lead
    return words, int(y)


def blit(img, word, ox, oy, color, alpha, dy=0.0):
    if alpha <= 0.01:
        return
    m = word["mask"]
    if alpha < 0.99:
        lut = [int(i * alpha) for i in range(256)]
        m = m.point(lut)
    img.paste(color, (int(ox + word["x"] - word["pad"]), int(oy + word["y"] + dy)), m)


def draw_words(img, words, ox, oy, t, dur, base_color, alpha=1.0, spread=0.7, t0=0.15):
    n = max(1, len(words))
    for i, w in enumerate(words):
        start = t0 + (i / n) * dur * spread
        e = ease_out((t - start) / 0.55)
        color = CARMINE if w["accent"] else base_color
        blit(img, w, ox, oy, color, e * alpha, dy=(1 - e) * 38)


def spaced(draw, xy, text, fnt, fill, spacing):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += fnt.getlength(ch) + spacing


def kicker(img, text, y, alpha):
    if alpha <= 0.01:
        return
    layer = Image.new("RGBA", (W, 60), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    spaced(d, (MARGIN, 8), text.upper(), font(SANS, 28), CARMINE + (int(255 * alpha),), 7)
    img.paste(layer, (0, y), layer)


# ------------------------------------------------------------------ beat kinds
class Beat:
    def __init__(self, say, kind="text", fade_in=True, fade_out=True, gap=0.5, **kw):
        self.say, self.kind, self.fade_in, self.fade_out, self.gap = say, kind, fade_in, fade_out, gap
        self.kw = kw
        self.dur = 0.0
        self.start = 0.0
        self._cache = None

    # cached layout --------------------------------------------------------
    def prep(self):
        if self._cache is not None:
            return self._cache
        k, c = self.kw, {}
        if self.kind == "text":
            c["words"], c["h"] = layout(k["text"], k.get("size", 112), W - 2 * MARGIN, k.get("align", "left"))
        elif self.kind == "list":
            if k.get("title"):
                c["tw"], c["th"] = layout(k["title"], k.get("tsize", 84), W - 2 * MARGIN)
            ind = 130 if k.get("numbers", True) else 0
            rows, h = [], 0
            for label, sub in k["items"]:
                lw, lh = layout(label, k.get("lsize", 68), W - 2 * MARGIN - ind)
                sw = sh = 0
                if sub:
                    f = font(SANS, 34)
                    sw = _wrap(sub, f, W - 2 * MARGIN - ind)
                    sh = len(sw) * 46
                rows.append(dict(lw=lw, lh=lh, sw=sw, sh=sh, y=h))
                h += lh + sh + 58
            c["rows"], c["rh"] = rows, h
        elif self.kind == "outro":
            logo = Image.open(os.path.join(ASSETS, "future-skills-logo-transparent.png")).convert("RGBA")
            logo = logo.crop(logo.getbbox())
            s = 800 / logo.width
            c["logo"] = logo.resize((800, int(logo.height * s)), Image.LANCZOS)
            c["tw"], c["th"] = layout(k.get("text", "The skills that *compound* when AI does the rest."), 62, W - 2 * MARGIN, "center")
        self._cache = c
        return c

    # drawing --------------------------------------------------------------
    def draw(self, img, t):
        k, c = self.kw, self.prep()
        env = 1.0
        if self.fade_in:
            env = min(env, clamp(t / 0.3))
        if self.fade_out:
            env = min(env, clamp((self.dur - t) / 0.35))
        if self.kind == "text":
            h = c["h"]
            oy = k.get("y", CENTER_Y - h / 2)
            if k.get("kicker"):
                kicker(img, k["kicker"], int(oy - 90), env)
            draw_words(img, c["words"], MARGIN, oy, t, self.dur, PLUM, env)
        elif self.kind == "list":
            self._draw_list(img, t, env, c)
        elif self.kind == "chart":
            self._draw_chart(img, t, env)
        elif self.kind == "outro":
            self._draw_outro(img, t, env, c)

    def _draw_list(self, img, t, env, c):
        k = self.kw
        th = c.get("th", 0) + (70 if c.get("tw") else 0)
        total = th + c["rh"]
        oy = max(250, CENTER_Y - total / 2)
        if k.get("kicker"):
            kicker(img, k["kicker"], int(oy - 90), env)
        if c.get("tw"):
            draw_words(img, c["tw"], MARGIN, oy, t, self.dur, PLUM, env, spread=0.25)
        ind = 130 if k.get("numbers", True) else 0
        focus, stagger = k.get("focus"), k.get("stagger", True)
        n = len(c["rows"])
        d = ImageDraw.Draw(img)
        for i, r in enumerate(c["rows"]):
            ry = oy + th + r["y"]
            if stagger:
                e = ease_out((t - (0.4 + i * min(0.7, self.dur * 0.6 / n))) / 0.55)
            else:
                e = 1.0
            hot = focus is None or i == focus
            tgt = 1.0 if hot else 0.28
            a = e * env * tgt
            if a <= 0.01:
                continue
            dy = (1 - e) * 36
            if focus is not None and hot:
                bar_h = r["lh"] + r["sh"] - 6
                d.rectangle([MARGIN - 28, ry + 8 + dy, MARGIN - 22, ry + 8 + dy + bar_h], fill=CARMINE)
            if k.get("numbers", True):
                layer = Image.new("RGBA", (130, 60), (0, 0, 0, 0))
                ImageDraw.Draw(layer).text((0, 0), f"{i + 1:02d}", font=font(SANS, 34), fill=CARMINE + (int(255 * a),))
                img.paste(layer, (MARGIN, int(ry + 30 + dy)), layer)
            for w in r["lw"]:
                blit(img, w, MARGIN + ind, ry, CARMINE if w["accent"] else PLUM, a, dy)
            if r["sw"]:
                layer = Image.new("RGBA", (W, r["sh"] + 10), (0, 0, 0, 0))
                ld = ImageDraw.Draw(layer)
                for j, line in enumerate(r["sw"]):
                    ld.text((MARGIN + ind, j * 46), line, font=font(SANS, 34), fill=PLUM + (int(255 * a * 0.66),))
                img.paste(layer, (0, int(ry + r["lh"] + 10 + dy)), layer)

    def _draw_chart(self, img, t, env):
        S = 2
        cw, ch = W - 2 * MARGIN, 700
        layer = Image.new("RGBA", (cw * S, ch * S), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        a = int(255 * env)
        d.line([(0, ch * S), (cw * S, ch * S)], fill=PLUM + (int(90 * env),), width=3 * S)
        d.line([(0, 0), (0, ch * S)], fill=PLUM + (int(90 * env),), width=3 * S)
        p = clamp((t - 0.3) / (self.dur - 1.0))
        p = ease_io(p)
        N = 120
        cost = [(i / N, math.exp(-3.4 * i / N)) for i in range(N + 1)]
        val = [(i / N, 0.10 + 0.85 * (i / N) ** 1.7) for i in range(N + 1)]
        for pts, col, wd in ((cost, PLUM, 9), (val, CARMINE, 11)):
            xy = [(x * (cw - 20) * S + 10 * S, (1 - y) * (ch - 40) * S + 20 * S) for x, y in pts if x <= p]
            if len(xy) > 1:
                d.line(xy, fill=col + (a,), width=wd * S, joint="curve")
                ex, ey = xy[-1]
                r = 15 * S
                d.ellipse([ex - r, ey - r, ex + r, ey + r], fill=col + (a,))
        layer = layer.resize((cw, ch), Image.LANCZOS)
        oy = CENTER_Y - ch / 2 - 60
        img.paste(layer, (MARGIN, int(oy)), layer)
        # labels
        ld = Image.new("RGBA", (W, 200), (0, 0, 0, 0))
        dd = ImageDraw.Draw(ld)
        e = ease_out((t - 0.8) / 0.6) * env
        dd.text((MARGIN, 0), "Cost of execution, falling", font=font(SERIF, 52), fill=PLUM + (int(255 * e),))
        e2 = ease_out((t - 1.6) / 0.6) * env
        dd.text((MARGIN, 76), "Value of judgment, rising", font=font(SERIF_I, 52), fill=CARMINE + (int(255 * e2),))
        dd.text((MARGIN, 160), "Illustrative", font=font(SANS, 26), fill=PLUM + (int(110 * env),))
        img.paste(ld, (0, int(oy + ch + 50)), ld)

    def _draw_outro(self, img, t, env, c):
        logo = c["logo"]
        p = ease_io(t / 1.6)
        wipe = int(logo.width * p)
        if wipe > 0:
            crop = logo.crop((0, 0, wipe, logo.height))
            img.paste(crop, ((W - logo.width) // 2, 330), crop)
        e = ease_out((t - 1.4) / 0.7)
        oy = 330 + logo.height + 80
        draw_words(img, c["tw"], MARGIN, oy, t - 1.2, self.dur, PLUM, 1.0, spread=0.35, t0=0.0)
        e3 = ease_out((t - 2.6) / 0.7)
        layer = Image.new("RGBA", (W, 80), (0, 0, 0, 0))
        f = font(SANS, 38)
        txt = "futureskillsacademy.ai"
        tw = sum(f.getlength(ch) + 5 for ch in txt)
        spaced(ImageDraw.Draw(layer), ((W - tw) / 2, 10), txt, f, CARMINE + (int(255 * e3),), 5)
        img.paste(layer, (0, int(oy + c["th"] + 70)), layer)


def _wrap(text, f, maxw):
    lines, cur = [], ""
    for w in text.split(" "):
        trial = (cur + " " + w).strip()
        if f.getlength(trial) > maxw and cur:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    lines.append(cur)
    return lines


# ------------------------------------------------------------- global chrome
_brush = None


def background(gt, total):
    global _brush
    if _brush is None:
        b = Image.open(os.path.join(ASSETS, "future-skills-brush.png")).convert("RGBA")
        b = b.resize((1700, int(b.height * 1700 / b.width)), Image.LANCZOS)
        a = b.getchannel("A").point(lambda v: int(v * 0.20))
        b.putalpha(a)
        _brush = b
    img = Image.new("RGB", (W, H), BONE)
    drift = gt / total
    img.paste(_brush, (int(W - 1250 - drift * 120), int(H - 1000 + drift * 60)), _brush)
    d = ImageDraw.Draw(img)
    f_r, f_i = font(SERIF, 40), font(SERIF_I, 40)
    d.text((MARGIN, 96), "Future Skills ", font=f_r, fill=PLUM)
    d.text((MARGIN + f_r.getlength("Future Skills "), 96), "Academy", font=f_i, fill=CARMINE)
    y = 1650
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=(51, 36, 50, 40), width=2)
    d.line([(MARGIN, y), (MARGIN + (W - 2 * MARGIN) * gt / total, y)], fill=CARMINE, width=4)
    return img


# --------------------------------------------------------------------- audio
def probe(path):
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", path])
    return float(out)


def make_pad(path, seconds, sr=44100):
    chords = [
        [110.0, 164.81, 220.0, 261.63, 329.63],   # Am
        [87.31, 130.81, 174.61, 261.63, 349.23],  # F
        [130.81, 196.0, 261.63, 329.63, 392.0],   # C
        [98.0, 146.83, 196.0, 293.66, 392.0],     # G
    ]
    n = int(seconds * sr)
    t = np.arange(n) / sr
    out = np.zeros((n, 2))
    seg, hop = 10.0, 7.0
    k, start = 0, 0.0
    while start < seconds:
        env = np.clip((t - start) / seg, 0, 1)
        env = np.sin(np.pi * env) ** 2
        sig = np.zeros(n)
        for f in chords[k % 4]:
            for det in (-0.0025, 0.0025):
                sig += np.sin(2 * np.pi * f * (1 + det) * t + f) / (1 + f / 220)
        sig *= env * (0.85 + 0.15 * np.sin(2 * np.pi * 0.11 * t + k))
        out[:, 0] += sig
        out[:, 1] += np.roll(sig, 900)
        k += 1
        start += hop
    out /= np.abs(out).max()
    fade = np.clip(np.minimum(t, seconds - t) / 2.0, 0, 1)[:, None]
    out *= fade * 0.22
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes((out * 32767).astype("<i2").tobytes())


AI_RE = re.compile(r"\bA\.? ?I\b")


def spoken(text):
    """Strip markup and force "AI" to be said as the letters A-I (stress on the I)."""
    return AI_RE.sub("[AI](/ˌeɪˈaɪ/)", text.replace("*", ""))


# -------------------------------------------------------------------- render
def render(name, beats, outdir, work, speed=0.95, preview=False, poster=None):
    os.makedirs(work, exist_ok=True)
    os.makedirs(outdir, exist_ok=True)
    t = 0.5
    wavs, jobs = [], {}
    for i, b in enumerate(beats):
        aiff = os.path.join(work, f"{name}_{i:02d}.wav")
        if not os.path.exists(aiff):
            jobs[aiff] = spoken(b.say)
    if jobs:
        import json
        jf = os.path.join(work, f"{name}_jobs.json")
        json.dump(jobs, open(jf, "w"))
        subprocess.run(["uv", "run", "--python", "3.12", "--with", "mlx-audio", "--with", "misaki[en]",
                        "--with", "soundfile", "--with", "num2words", "--with", "spacy", "python",
                        os.path.join(HERE, "kokoro_tts.py"), jf, str(speed)], check=True)
    for i, b in enumerate(beats):
        aiff = os.path.join(work, f"{name}_{i:02d}.wav")
        clip = probe(aiff)
        b.dur = max(2.0, clip + b.gap + (0.4 if b.kind == "outro" else 0))
        b.start = t
        t += b.dur
        wavs.append((aiff, b))
    total = t + 0.6
    # voice track
    voice_wav = os.path.join(work, f"{name}_voice.wav")
    inputs, filt = [], []
    for i, (aiff, b) in enumerate(wavs):
        inputs += ["-i", aiff]
        filt.append(f"[{i}:a]aresample=44100,aformat=channel_layouts=mono,adelay={int(b.start * 1000)}:all=1[v{i}]")
    mix = "".join(f"[v{i}]" for i in range(len(wavs)))
    filt.append(f"{mix}amix=inputs={len(wavs)}:normalize=0,apad=whole_dur={total}[vo]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(filt),
                    "-map", "[vo]", "-t", str(total), voice_wav], check=True)
    pad = os.path.join(work, f"{name}_pad.wav")
    make_pad(pad, total)
    audio = os.path.join(work, f"{name}_audio.m4a")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", voice_wav, "-i", pad, "-filter_complex",
                    "[0:a]aformat=channel_layouts=stereo,volume=1.15[a];[a][1:a]amix=inputs=2:normalize=0[o]",
                    "-map", "[o]", "-c:a", "aac", "-b:a", "192k", audio], check=True)

    nframes = int(total * FPS)
    if poster:
        b = beats[0]
        b.fade_in = b.fade_out = False
        img = background(b.start + 1.0, total)
        b.draw(img, b.dur)
        img.resize((540, 960), Image.LANCZOS).save(poster, quality=88)
        return total

    def frame(fi):
        gt = fi / FPS
        img = background(gt, total)
        for b in beats:
            if b.start <= gt < b.start + b.dur:
                b.draw(img, gt - b.start)
        return img

    if preview:
        for b in beats:
            mid = b.start + min(b.dur - 0.5, b.dur * 0.85)
            frame(int(mid * FPS)).save(os.path.join(work, f"{name}_prev_{beats.index(b):02d}.png"))
        return total
    silent = os.path.join(work, f"{name}_silent.mp4")
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                          "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium",
                          "-crf", "18", "-pix_fmt", "yuv420p", silent], stdin=subprocess.PIPE)
    for fi in range(nframes):
        p.stdin.write(frame(fi).tobytes())
    p.stdin.close()
    p.wait()
    out = os.path.join(outdir, f"{name}.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", silent, "-i", audio, "-c:v", "copy",
                    "-c:a", "copy", "-shortest", "-movflags", "+faststart", out], check=True)
    print(f"{out}  {total:.1f}s")
    return total
