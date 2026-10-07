"""Bite-sized practice videos: one lesson idea + its practice assignment.

Usage: python3 practice.py [--preview] [prefix ...]
Output: videos/practice/NN-slug.mp4 and videos/practice/captions.md
"""
import os
import sys

from engine import Beat, render

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, "..", "practice"))
WORK = os.environ.get("FSA_WORK", "/private/tmp/claude-501/-Users-birger-future-skills-academy/9452d800-f020-4ae7-9902-cc77e96acf38/scratchpad/work")

TRACKS = {
    "mts": ("Member of Technical Staff", "member-of-technical-staff"),
    "agency": ("High Agency", "high-agency"),
    "taste": ("Taste", "taste"),
    "rel": ("Relationships", "relationships"),
    "comm": ("Communication", "communication"),
}
SAY_NO = {"1.3": "one point three", "4.1": "four point one", "2.1": "two point one", "4.2": "four point two",
          "5.1": "five point one", "2.2": "two point two", "1.2": "one point two", "2.3": "two point three"}

# id, slug, hook (text, say, size), ideas [(text, say)], steps [text], practice say
LESSONS = [
    ("mts-1-3", "verify-ai-output",
     ("Every AI output arrives with an invisible *question mark.*", "Every A I output arrives with an invisible question mark.", 104),
     [("Fast teams don't trust AI more. Their *verification loop* is so fast that trust is unnecessary.",
       "The teams that ship fast with A I don't trust it more. Their verification loop is so fast that trust becomes unnecessary."),
      ("Scale checks to the *blast radius.* A typo needs a glance. A payment path needs tests, review, and a staged rollout.",
       "Scale your checks to the blast radius. A typo needs a glance. A payment path needs tests, review, and a staged rollout.")],
     ["Write down the three cheapest checks that catch 80% of AI mistakes.",
      "A test command. A smoke flow. A diff review ritual.",
      "Run them before you accept any generated change."],
     "Your practice. Write down the three cheapest checks that would catch eighty percent of A I mistakes. "
     "A test command, a smoke flow, a diff review ritual. Then run them before you accept any generated change."),
    ("mts-4-1", "why-demos-lie",
     ("Every AI demo *works.*", "Every A I demo works.", 130),
     [("The demo is run by the person who built it, on inputs it handles. Production is run by *strangers,* on inputs you never imagined.",
       "The demo is run by the person who built it, on inputs it handles. Production is run by strangers, on inputs you never imagined."),
      ("An eval is real inputs with graded answers, run on every change. *Unit tests* for behavior that is probabilistic.",
       "An eval is a set of real inputs with graded answers, run on every change. Unit tests for behavior that is probabilistic.")],
     ["Collect twenty real inputs for an AI feature, including the ugly ones.",
      "Define what a passing answer looks like for each.",
      "You have just written your first eval set."],
     "Your practice. Collect twenty real inputs for an A I feature you use or build, including the ugly ones. "
     "Define what a passing answer looks like for each. You've just written your first eval set."),
    ("agency-2-1", "one-way-two-way-doors",
     ("What does it cost to be *wrong?*", "Before any decision, ask: what does it cost to be wrong?", 112),
     [("*Two-way doors* are reversible. Decide, observe, adjust. *One-way doors* deserve deliberation.",
       "Two-way doors are reversible. Decide, observe, adjust. One-way doors, like hires and public commitments, deserve deliberation."),
      ("Most slowness is two-way doors treated with one-way ceremony. AI made many doors *two-way,* because finding out is cheap.",
       "Most slowness comes from treating two-way doors with one-way ceremony. And A I turned many one-way doors into two-way doors, because finding out is cheap.")],
     ["List the five decisions pending around you.",
      "Classify each: one-way or two-way.",
      "Decide every two-way door this week, with the cheapest test you can run."],
     "Your practice. List the five decisions pending around you. Classify each as one-way or two-way. "
     "Then decide every two-way door this week, with the cheapest test you can run."),
    ("agency-4-2", "direction-is-the-expensive-sentence",
     ("“Make onboarding better” *fails.*", "Make onboarding better. This goal fails.", 104),
     [("When execution is fast, a vague goal does damage at *machine speed.*",
       "When execution is fast, a vague goal does damage at machine speed."),
      ("“A new user reaches first success in under five minutes without help.” That *passes.* Outcome, constraints, non-goals.",
       "A new user reaches their first success in under five minutes without human help. That one passes. Write the outcome, the constraints, and the non goals.")],
     ["Take your team's current goal, as written.",
      "Ask two people, or two AI sessions, to paraphrase what it means for this week.",
      "If the paraphrases diverge, rewrite the goal until they don't."],
     "Your practice. Take your team's current goal, as written. Ask two people, or two A I sessions, to paraphrase "
     "what it means for this week. If the paraphrases diverge, rewrite the goal until they don't."),
    ("taste-4-1", "generate-wide-choose-narrow",
     ("AI's first option is always *competent.*", "A I's first option is always competent.", 108),
     [("Competent is the new baseline. Which means competent is the new *invisible.*",
       "Competent is the new baseline. Which means competent is the new invisible."),
      ("So generate *wide.* Twenty genuinely different directions. Then switch from generator to curator, and kill eighteen.",
       "So generate wide. Twenty genuinely different directions. Then switch roles, from generator to curator, and kill eighteen without mercy.")],
     ["Take one real design task and force twenty distinct AI directions.",
      "Pick two. Write down why those two.",
      "Iterate only on them, and compare to your usual first-idea workflow."],
     "Your practice. Take one real design task and force twenty meaningfully distinct A I directions. "
     "Pick two, and write down why those two. Then iterate only on them, and compare the result to your usual first idea workflow."),
    ("taste-5-1", "subtraction-by-default",
     ("Remove *thirty percent.*", "Take your finished work, and remove thirty percent.", 130),
     [("Addition feels like progress. Subtraction feels like loss. That's why disciplined removal is rare enough to be a *signature.*",
       "Addition feels like progress. Subtraction feels like loss. That is why disciplined removal is rare enough to be a signature."),
      ("Ask: if this vanished, would anyone's experience get *worse?* Most elements fail.",
       "Ask: if this element vanished, would anyone's experience get worse? Be honest, and most elements fail.")],
     ["Take a finished piece of your work.",
      "Cut 30% of the words, elements, or features, losing nothing essential.",
      "Ask an AI to argue for each cut. Then you judge."],
     "Your practice. Take a finished piece of your work and cut thirty percent, without losing anything essential. "
     "If you can't find thirty percent, you're not looking. Ask an A I to argue for each cut, then you judge."),
    ("rel-2-2", "the-discipline-of-shutting-up",
     ("The important thing comes after the *pause.*", "The important thing comes after the pause.", 110),
     [("Count *three full seconds* before you respond. Resist finishing their sentences.",
       "Count three full seconds before you respond. And resist finishing their sentences."),
      ("Then prove you heard: “So what I'm hearing is…” and let them *correct you.* Being accurately heard is rare.",
       "Then prove you heard. So what I'm hearing is, and let them correct you. Being accurately heard is so rare, it alone differentiates you.")],
     ["In your next three important conversations, wait three seconds before every response.",
      "Give one “what I'm hearing is…” summary before any opinion of yours.",
      "Note what surfaces in the pauses."],
     "Your practice. In your next three important conversations, wait three seconds before every response, "
     "and give one, what I'm hearing is, summary before any opinion of your own. Then note what surfaces in the pauses."),
    ("rel-1-2", "promise-smaller",
     ("Promise *smaller.*", "Promise smaller.", 150),
     [("You said Thursday. Did it arrive Thursday? Trust is a tiny loop everyone runs on you, *constantly.*",
       "You said Thursday. Did it arrive Thursday? Trust is a tiny loop that everyone runs on you, constantly."),
      ("Each kept promise is a deposit. Each quiet miss is a *withdrawal* at triple the rate.",
       "Each kept promise is a deposit. Each quiet miss is a withdrawal at triple the rate. A draft by Friday, kept, beats everything by Wednesday, missed.")],
     ["For one week, log every promise, including the casual ones.",
      "Track your keep rate, honestly.",
      "Shrink your promises until it's above 95%."],
     "Your practice. For one week, log every promise you make, including the casual ones. Track your keep rate honestly. "
     "Then shrink your promises until it's above ninety five percent."),
    ("comm-1-3", "conclusion-first",
     ("Nobody ever complained about hearing the point *too early.*", "Nobody has ever complained about being told the point too early.", 92),
     [("School taught you to build to a conclusion. Work punishes you for it. Busy people read *three lines* and decide.",
       "School taught you to build up to a conclusion. Work punishes you for it. Busy people read the first three lines and decide."),
      ("*Answer first.* Then reasons. Then evidence. Out loud too: “I recommend X. Three reasons.”",
       "Answer first. Then reasons. Then evidence. It works out loud too: I recommend X. Three reasons.")],
     ["Rewrite one real document conclusion-first: answer in line one.",
      "Three reasons as headers, evidence beneath each.",
      "Send both versions to a colleague. Ask which they'd rather receive."],
     "Your practice. Rewrite one real document, conclusion first. The answer in line one, three reasons as headers, "
     "evidence beneath each. Then send both versions to a colleague and ask which they'd rather receive."),
    ("comm-2-3", "writing-with-ai-keep-your-voice",
     ("AI writing is converging on one *forgettable* voice.", "A I writing is converging on one smooth, forgettable voice.", 100),
     [("Voice is now a signal of *authenticity.* You supply the point, the structure, the specifics. AI supplies critique and polish.",
       "Voice is now a signal of authenticity. You supply the point, the structure, and the specifics. A I supplies critique, compression, and polish."),
      ("*Author and editor.* Never the reverse.", "You are the author, and A I is the editor. Never the reverse.")],
     ["Write a short piece your way.",
      "Ask AI for its three strongest criticisms. Not a rewrite.",
      "Address them in your own words."],
     "Your practice. Write a short piece your way. Then ask A I for its three strongest criticisms, not a rewrite, "
     "and address them in your own words."),
]


def build(lesson):
    lid, slug, hook, ideas, steps, psay = lesson
    key = lid.rsplit("-", 2)[0]
    no = ".".join(lid.rsplit("-", 2)[1:])
    name, _ = TRACKS[key]
    kick = f"{name} · {no}"
    beats = [Beat(hook[1], text=hook[0], size=hook[2], kicker=kick, gap=0.7)]
    for i, (text, say) in enumerate(ideas):
        beats.append(Beat(say, text=text, size=76, kicker="The idea" if i == 0 else None))
    beats.append(Beat(psay, "list", title="Your *practice.*", items=[(s, "") for s in steps], lsize=56,
                      kicker="Practice", gap=0.8))
    spoken = no.replace(".", " point ").replace("1", "one").replace("2", "two").replace("3", "three") \
        .replace("4", "four").replace("5", "five")
    beats.append(Beat(f"Lesson {spoken}, from the {name} track. Free at Future Skills Academy dot A I.", "outro",
                      text=f"Lesson {no} · *{name}*", gap=0.8))
    return beats


def caption(lesson):
    lid, slug, hook, ideas, steps, _ = lesson
    key = lid.rsplit("-", 2)[0]
    name, page = TRACKS[key]
    plain = lambda s: s.replace("*", "")
    lines = [f"## {lid} · {plain(hook[0])}", "", plain(ideas[0][0]), "", "Practice:"]
    lines += [f"- {plain(s)}" for s in steps]
    lines += ["", f"https://futureskillsacademy.ai/tracks/{page}.html#{lid}", ""]
    return "\n".join(lines)


if __name__ == "__main__":
    args = sys.argv[1:]
    preview = "--preview" in args
    prefixes = [a for a in args if not a.startswith("--")]
    os.makedirs(OUT, exist_ok=True)
    for n, lesson in enumerate(LESSONS, 1):
        if prefixes and not any(lesson[0].startswith(p) or f"{n:02d}" == p for p in prefixes):
            continue
        render(f"{n:02d}-{lesson[1]}", build(lesson), OUT, WORK, preview=preview)
    if not prefixes and not preview:
        with open(os.path.join(OUT, "captions.md"), "w") as f:
            f.write("# Practice video captions\n\n" + "\n".join(caption(x) for x in LESSONS))
