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
    ("mts-2-2", "prompts-are-specifications",
     ("Ambiguity in, *ambiguity* out.", "Ambiguity in, ambiguity out.", 126),
     [("A model fills every gap in your spec with the most *statistically common* choice. Rarely yours.",
       "A model fills every gap in your spec with the most statistically common choice. Which is rarely yours."),
      ("State the goal, the edge cases, the non-goals, and what *done* looks like. One example beats ten paragraphs.",
       "State the goal, the inputs and outputs, the edge cases, the non goals, and what done looks like. An example of the desired output is worth ten paragraphs of description.")],
     ["Write a one-page spec for a small feature: goal, constraints, edge cases, acceptance checks.",
      "Hand it to an AI agent, untouched.",
      "Every clarifying question it asks is a hole in your spec."],
     "Your practice. Write a one page spec for a small feature. Goal, constraints, edge cases, acceptance checks. "
     "Hand it to an A I agent, untouched. Every clarifying question it needs to ask is a hole in your spec."),
    ("mts-3-3", "guardrails-and-failure-modes",
     ("Assume the agent will do the *worst thing* its permissions allow.", "Assume the agent will eventually do the worst thing its permissions allow.", 96),
     [("Agents loop. They overreach. They declare victory early. They take *destructive shortcuts.*",
       "Agents fail in characteristic ways. They loop. They overreach. They declare victory early. They take destructive shortcuts."),
      ("Then shrink the permissions. Least-privilege tools, budgets, human approval on irreversible steps. Failure should be *bounded, visible, and cheap.*",
       "Then shrink the permissions. Least privilege tools, budgets on time and actions, human approval on irreversible steps. The goal is a system where failure is bounded, visible, and cheap.")],
     ["Write down the three worst things your agent could do with its current permissions.",
      "Redesign so the worst one is impossible.",
      "Make the other two recoverable."],
     "Your practice. Red team your own agent. Write down the three worst things it could do with its current permissions. "
     "Then change the design so the worst one is impossible, and the other two are recoverable."),
    ("agency-1-2", "permission-is-imaginary",
     ("Permission is mostly *imaginary.*", "Permission is mostly imaginary.", 126),
     [("Most of the permission people wait for is a social guess about what might *annoy* someone.",
       "Most of the permission people wait for doesn't exist as a rule anywhere. It's a social guess about what might annoy someone."),
      ("Reversible? *Act and inform.* Irreversible? Ask fast, with a recommendation: “I plan to do X by Friday unless you object.”",
       "If it's reversible, act and inform. If it's expensive or irreversible, ask fast, with a recommendation attached. I plan to do X by Friday, unless you object, gets more done than should I do X ever has.")],
     ["Pick one thing you've been waiting for permission to do.",
      "Reversible? Do it this week, and inform.",
      "Not reversible? Send the “I plan to, unless you object” message today."],
     "Your practice. Pick one thing you've been waiting for permission to do. Is it reversible? If so, do it this week and inform. "
     "If not, send the, I plan to, unless you object, message today."),
    ("agency-3-2", "delegating-to-machines",
     ("Not “help me write this.” *“Own this report.”*", "Not, help me write this. Instead: own this whole report.", 102),
     [("Treat AI delegation as a *management* skill. Give the goal and constraints, not keystrokes. Demand artifacts you can verify.",
       "Treat A I delegation as a management skill, not a tool skill. Give the goal and the constraints, not keystroke instructions, and demand artifacts you can verify."),
      ("Review *early,* before errors compound. Keep a written record of what worked. Good briefers become the best AI operators.",
       "Review early, before errors compound. And keep a written record of what worked. The managers who were good at briefing people are suddenly the best A I operators.")],
     ["Choose one recurring deliverable you produce.",
      "Write a standing brief: goal, audience, quality bar, examples.",
      "Have AI produce the next one end to end. Review like a manager, not a co-author."],
     "Your practice. Choose one recurring deliverable you produce. Write a standing brief for it. Goal, audience, quality bar, examples. "
     "Have A I produce the next one end to end, and review it like a manager, not a co author."),
    ("taste-2-2", "the-language-of-critique",
     ("“Make it pop” is not *critique.*", "Make it pop. Is not critique.", 122),
     [("“The primary action competes with three other elements of equal weight.” That is *critique.* Specific, and tied to intent.",
       "The primary action competes with three other elements of equal weight. That is critique. It's specific, and tied to intent."),
      ("Start from intent. Judge against it, not your preferences. This is also the language that *steers AI tools.* They shrug at vibes.",
       "Start from intent. Judge against it, not against your preferences. And this is exactly the language that steers A I tools. They respond to precision and shrug at vibes.")],
     ["Critique one piece of work: a colleague's, a famous product's, or your own.",
      "Four sentences: intent, what serves it, what fights it, one concrete suggestion.",
      "Zero adjectives of pure preference."],
     "Your practice. Critique one piece of work this week, a colleague's, a famous product's, or your own. "
     "Four sentences minimum. Intent, what serves it, what fights it, and one concrete suggestion. Zero adjectives of pure preference."),
    ("taste-4-2", "directing-not-prompting",
     ("Prompting asks the machine to *guess* your taste.", "Prompting asks the machine to guess your taste. Directing supplies it.", 104),
     [("Directing means a *creative brief.* Who it's for. The one feeling it must produce. Three references. What's off the table.",
       "Directing means a creative brief. Who this is for. The one feeling it must produce. Three reference works, and the principle each contributes. And what is absolutely off the table."),
      ("Without a brief, AI returns the *statistical average* of everything. Which is precisely what mediocrity is.",
       "Without a brief, A I returns the statistical average of everything, which is precisely what mediocrity is.")],
     ["Write a one-page brief for a real task: audience, the single feeling, three annotated references, the forbidden list.",
      "Run it through your AI tool.",
      "Run the old two-line prompt too, and compare side by side."],
     "Your practice. Write a one page brief for a real task. Audience, the single feeling, three annotated references, and the forbidden list. "
     "Run it through your A I tool. Then run the same task with your old two line prompt, and put the results side by side."),
    ("rel-2-1", "discovery-questions",
     ("The past is *evidence.* The future is flattery.", "The past is evidence. The future is flattery.", 110),
     [("Don't ask “would you use a tool that…?” You'll get *polite fiction.*",
       "Don't ask people to predict. Would you use a tool that? You will get polite fiction."),
      ("Ask: “Walk me through the last time this happened.” Then “*tell me more*,” three levels down. That's where the real problem lives.",
       "Ask about the past. Walk me through the last time this happened. What did you do, what did it cost you? Then say, tell me more, three levels down. That is where the real problem lives.")],
     ["Run three twenty-minute discovery conversations this week.",
      "Past events only. “Tell me more” three levels down. Zero pitching.",
      "Write down the problem you found versus the one you expected."],
     "Your practice. Run three twenty minute discovery conversations this week. Past events only, tell me more, three levels down, and zero pitching. "
     "Then write down the problem you found, versus the problem you expected."),
    ("rel-4-2", "qualify-hard-pitch-plainly",
     ("Hope is not a *pipeline stage.*", "Hope is not a pipeline stage.", 126),
     [("Time is a salesperson's only inventory. Four questions: is the pain *real,* is there *money,* can they *decide,* is there a reason to act *now?*",
       "Time is the salesperson's only inventory. So qualify with four questions. Is the pain real? Is there money? Can your contact decide? And is there a reason to act now?"),
      ("Two or more no's: nurture politely and move on. Then pitch like a person. *Plainness* is a relief to people drowning in AI decks.",
       "Two or more no's, nurture politely and move on. When you do pitch, pitch like a person. Decision makers drowning in A I generated decks experience plainness as relief.")],
     ["Score your pipeline against the four questions.",
      "Retire every deal scoring below two, gracefully, with the door left open.",
      "Rewrite your pitch as five plain sentences."],
     "Your practice. Score your current pipeline against the four questions. Formally retire every deal scoring below two, "
     "with a graceful note that leaves the door open. Then rewrite your pitch as five plain sentences."),
    ("comm-3-1", "the-slide-is-not-the-talk",
     ("The slide is not the *talk.*", "The slide is not the talk.", 130),
     [("A presentation is a spoken argument with visual support. Not a document *performed aloud.*",
       "A presentation is a spoken argument with visual support. Not a document performed aloud."),
      ("Build it in order: one point, three beats, and only then slides. AI makes handsome decks in minutes, so the merely handsome deck is *worthless.*",
       "Build it in that order. The one point, the three beats that establish it, and only then slides. A I generates handsome decks in minutes now, which makes the merely handsome deck worthless.")],
     ["Write the talk first: one point, three beats, in spoken language.",
      "Build the fewest slides that support it.",
      "Rehearse aloud twice, standing up. Then deliver."],
     "Your practice. Take your next presentation and write the talk first. One point, three beats, in spoken language. "
     "Then build the fewest slides that support it. Rehearse aloud twice, standing up, and deliver."),
    ("comm-4-2", "altitude",
     ("Every idea has four *altitudes.*", "Every idea has four altitudes.", 126),
     [("One sentence for the hallway. One paragraph for the exec. One page for the decision. *Full depth* for the people doing the work.",
       "One sentence for the hallway. One paragraph for the exec. One page for the decision. And the deep version for the people doing the work."),
      ("The classic failure is *altitude mismatch.* Detail drowns a decision-maker. Hand-waving insults an expert. AI can compress, but it can't know what mattered. Review what it dropped.",
       "The classic failure is altitude mismatch. Drowning a decision maker in detail, or hand waving at an expert. A I can compress honestly, but it cannot know what was important enough to survive. Review what it dropped.")],
     ["Write your main project at four altitudes: sentence, paragraph, page, full depth.",
      "Test the sentence on someone senior, and the page on someone technical.",
      "Revise where their eyes glazed."],
     "Your practice. Take your current main project and write it at all four altitudes. One sentence, one paragraph, one page, and full depth. "
     "Test the sentence on someone senior, and the page on someone technical. Revise where their eyes glazed."),
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
        name = f"{n:02d}-{lesson[1]}"
        post = os.path.join(OUT, "..", "..", "assets", "video", name + ".jpg") if "--posters" in args else None
        render(name, build(lesson), OUT, WORK, preview=preview, poster=post)
    if not prefixes and not preview and "--posters" not in args:
        with open(os.path.join(OUT, "captions.md"), "w") as f:
            f.write("# Practice video captions\n\n" + "\n".join(caption(x) for x in LESSONS))
