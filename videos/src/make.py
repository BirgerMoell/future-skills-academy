"""Usage: python3 make.py [--preview] [slug ...]"""
import os
import sys

from engine import Beat, render

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, ".."))
WORK = os.environ.get("FSA_WORK", "/private/tmp/claude-501/-Users-birger-future-skills-academy/9452d800-f020-4ae7-9902-cc77e96acf38/scratchpad/work")

TRACKS = [
    ("Member of Technical Staff", "Technical craft · AI-native engineering"),
    ("High Agency", "Leadership · Ownership · Decisions"),
    ("Taste", "Design · UX · Quality judgment"),
    ("Relationships", "Sales · Customers · Trust"),
    ("Communication", "Writing · Speaking · Clarity"),
]
STEPS = [
    ("Learn", "Short, dense lessons"),
    ("Drill", "Practice on real stakes"),
    ("Ship", "A capstone you can show"),
]
PRINCIPLES = [
    ("Verify everything", "Check outputs, claims, and your own assumptions"),
    ("Own the outcome", "Delegate the work, never the responsibility"),
    ("Play long games", "Optimize for the decade, not the demo"),
]


def outro(say, text=None):
    kw = dict(text=text) if text else {}
    return Beat(say, "outro", gap=0.8, **kw)


VIDEOS = {
    "01-judgment-is-the-bottleneck": lambda: [
        Beat("Something changed in the last two years.", text="Something *changed.*", kicker="The thesis"),
        Beat("Code, copy, designs, and decks. What used to take weeks now takes hours.", "list",
             items=[("Code", "weeks to hours"), ("Copy", "weeks to hours"), ("Designs", "weeks to hours"),
                    ("Decks", "weeks to hours")], kicker="Execution got cheap", numbers=False),
        Beat("Anyone can produce.", text="Anyone can *produce.*"),
        Beat("So execution stops being the moat. The cost of making things falls toward zero. "
             "The value of knowing what to make keeps rising.", "chart", gap=0.9),
        Beat("What stays scarce is what you choose to build, what you refuse to ship, and who trusts you.", "list",
             items=[("What you choose to build", ""), ("What you refuse to ship", ""), ("Who trusts you", "")],
             kicker="What stays scarce"),
        Beat("When intelligence is abundant, judgment is the bottleneck.",
             text="When intelligence is abundant, *judgment* is the bottleneck.", size=118, gap=0.9),
        Beat("The best people now work like editors in chief of a fleet of A I systems.",
             text="Work like an editor-in-chief of a fleet of *AI systems.*", size=96, kicker="The new unit of work"),
        Beat("They set intent. They delegate aggressively. They verify ruthlessly. And they take responsibility.", "list",
             items=[("Set intent", ""), ("Delegate aggressively", ""), ("Verify ruthlessly", ""),
                    ("Take responsibility", "")], numbers=False),
        outro("Future Skills Academy. The skills that compound when A I does the rest. "
              "Future Skills Academy dot A I."),
    ],
    "02-five-skills-that-dont-expire": lambda: [
        Beat("If A I does the execution, what should you train?", text="If AI does the execution, what do you *train?*",
             size=104),
        Beat("Five skills that have always mattered. A I just made them worth more.",
             text="Five skills that have always mattered. AI made them *worth more.*", size=96),
        Beat("Member of Technical Staff. Build real systems with A I as your engineering team, and know when the "
             "machine is wrong.", "list", items=TRACKS, lsize=58, focus=0, kicker="The five tracks", gap=0.4,
             fade_out=False),
        Beat("High Agency. Make things happen without permission, and own the outcome.", "list", items=TRACKS, lsize=58,
             focus=1, stagger=False, fade_in=False, fade_out=False, kicker="The five tracks", gap=0.4),
        Beat("Taste. When anyone can generate a thousand options, knowing which one is good is the rare skill.",
             "list", items=TRACKS, lsize=58, focus=2, stagger=False, fade_in=False, fade_out=False,
             kicker="The five tracks", gap=0.4),
        Beat("Relationships. In a world of synthetic everything, a human who listens and keeps promises is the "
             "scarcest asset.", "list", items=TRACKS, lsize=58, focus=3, stagger=False, fade_in=False, fade_out=False,
             kicker="The five tracks", gap=0.4),
        Beat("Communication. Fluent words are free now. Clarity is not.", "list", items=TRACKS, lsize=58, focus=4,
             stagger=False, fade_in=False, kicker="The five tracks"),
        Beat("Six modules per track. Eighteen lessons. Eight weeks, alongside a job.",
             text="Six modules. Eighteen lessons. *Eight weeks,* alongside a job.", size=100),
        outro("Pick a track and start. Future Skills Academy dot A I.",
              text="Pick a track. *Start today.*"),
    ],
    "03-learn-drill-ship": lambda: [
        Beat("Most learning is passive. You watch. You nod. You forget.",
             text="You watch. You nod. You *forget.*", size=110, kicker="The problem"),
        Beat("Future Skills Academy works differently. Three steps.", text="Three steps. *No passive learning.*",
             size=104),
        Beat("One. Learn. Each lesson is a few minutes of reading that changes how you work the same day.", "list",
             items=STEPS, focus=0, kicker="The method", gap=0.4, fade_out=False),
        Beat("Two. Drill. Every lesson ends with practice that uses your real job, project, or customers. "
             "Never toy exercises.", "list", items=STEPS, focus=1, stagger=False, fade_in=False, fade_out=False,
             kicker="The method", gap=0.4),
        Beat("Three. Ship. Each track closes with a capstone. A shipped system, a led project, a redesigned product, "
             "or a won relationship. Proof, not certificates.", "list", items=STEPS, focus=2, stagger=False,
             fade_in=False, kicker="The method"),
        Beat("Learn it. Drill it. Ship it.", text="Learn it.\nDrill it.\n*Ship it.*", size=150, gap=0.9),
        outro("Learn it. Drill it. Ship it. Future Skills Academy dot A I.", text="Proof, *not certificates.*"),
    ],
    "04-three-habits-that-never-expire": lambda: [
        Beat("Technology changes every quarter. Three habits do not.", text="Tools change every quarter.\n*Habits don't.*",
             size=104, kicker="House principles"),
        Beat("One. Verify everything. Abundant intelligence produces abundant, plausible nonsense. "
             "The professional habit of twenty twenty six is checking.", "list", items=PRINCIPLES, focus=0,
             kicker="Three habits", gap=0.4, fade_out=False),
        Beat("Two. Own the outcome. You can delegate the work to people or to machines. You can never delegate the "
             "responsibility.", "list", items=PRINCIPLES, focus=1, stagger=False, fade_in=False, fade_out=False,
             kicker="Three habits", gap=0.4),
        Beat("Three. Play long games. Quality, reputation, and trust compound slowly, and collapse instantly.",
             "list", items=PRINCIPLES, focus=2, stagger=False, fade_in=False, kicker="Three habits"),
        Beat("Optimize for the decade, not the demo.", text="Optimize for the *decade,*\nnot the demo.", size=112,
             gap=0.9),
        outro("Future Skills Academy. The skills the future cannot automate away. Future Skills Academy dot A I.",
              text="Build the skills the future *cannot automate away.*"),
    ],
}

POSTER_DIR = os.path.abspath(os.path.join(OUT, "..", "assets", "video"))

if __name__ == "__main__":
    args = sys.argv[1:]
    preview = "--preview" in args
    slugs = [a for a in args if not a.startswith("--")] or list(VIDEOS)
    for s in slugs:
        match = [k for k in VIDEOS if k.startswith(s)]
        for k in match:
            render(k, VIDEOS[k](), OUT, WORK, preview=preview, poster=POSTER_DIR and os.path.join(POSTER_DIR, k + ".jpg") if "--posters" in args else None)
