# MTS Email Course — 18-email drip sequence for Kit

Setup in Kit: **Automate → Visual Automations** → trigger: "Joins form: MTS email course"
→ add a **Sequence** with the 18 emails below. Send cadence: **Tuesday + Thursday, 09:00**
(email 1 sends immediately on signup). Sender: Birger Moëll · hello@futureskillsacademy.ai.
Add one personal line at the top of each email before publishing — that's the voice the
sequence is missing by design.

Link base: https://futureskillsacademy.ai/tracks/member-of-technical-staff.html

---

## Email 1 — sent immediately

**Subject:** Lesson 1: What a model actually is
**Preview:** Plausible is not the same as true.

Welcome — you just started the Member of Technical Staff track. Eighteen lessons, two a week, each a few minutes long with one practice assignment. Do the practice; that's the course.

Here's lesson one.

A language model is not a database and not a colleague. It's an extremely capable pattern engine producing the most plausible continuation of the context you give it. Plausible is not the same as true — and that gap is where every production incident lives. Once this clicks, the model stops being mysterious: brilliant on familiar patterns, confident even when guessing, entirely dependent on what you put in front of it.

The consequence: you control quality through context and verification, not hope. Everything else in this track follows from that sentence.

**Practice:** Ask a model a question in your own specialty, deep enough that you can grade the answer. Note where it was right, where it was plausible-but-wrong, and what context would have prevented the error.

Read it on the site → [Lesson 1.1](https://futureskillsacademy.ai/tracks/member-of-technical-staff.html#email-course)

---

## Email 2

**Subject:** Lesson 2: Machines draft, humans decide
**Preview:** Half your week is on the wrong side of this line.

The 2026 division of labor is simple: machines draft, humans decide. AI takes the breadth — boilerplate, first drafts, test scaffolding, research sweeps. You keep the depth: architecture, trade-offs, the definition of done, anything where being wrong is expensive.

Juniors fail by doing work the machine should do. Seniors fail by delegating decisions the machine should never own. Audit your week against this line and you'll typically find 40–60% of your hours sitting on the wrong side of it.

**Practice:** List everything you did at work last week. Mark each item: draft (AI), decide (you), or both. Move one recurring task across the line this week.

---

## Email 3

**Subject:** Lesson 3: Verification as a way of life
**Preview:** Fast teams don't trust more. They check faster.

The defining habit of the AI era is cheap, systematic verification. Every machine-made artifact arrives with an invisible question mark; your job is the fastest honest way to remove it — run the code, click the flow, check the citation, re-derive the number.

Teams that ship fast with AI aren't the ones who trust it most. They're the ones whose verification loop is so fast that trust is unnecessary. Scale the effort to the blast radius: a typo fix gets a glance; a payment path gets tests, review, and a staged rollout — no matter who or what wrote it.

**Practice:** For your current project, write down the three cheapest checks that would catch 80% of AI mistakes. Make them a habit before accepting any generated change.

---

## Email 4

**Subject:** Lesson 4: The context window is the workspace
**Preview:** "The AI is dumb" usually means "I gave it two vague sentences."

A model can only reason over what's in front of it. Most disappointing output traces back to context: the constraints you knew but didn't include, the conventions you assumed, the goal you left implicit. Treat the context window like a new hire's first day — the relevant files, the conventions, the goal, the things that must not break.

And curate hard. Burying the signal under irrelevant dumps degrades output as surely as starving it. The skill is selection: enough context to determine the right answer, little enough that the right answer is easy to find.

**Practice:** Take a task an AI recently did poorly for you. Rewrite the request with curated context — goal, constraints, examples, relevant code — and compare results side by side.

---

## Email 5

**Subject:** Lesson 5: Prompts are specifications
**Preview:** The eternal skill hiding inside "prompting."

Strip away the buzzword and prompting is specification writing — the thing great engineers were always better at. State the goal, the inputs and outputs, the edge cases, the non-goals, what done looks like. A model fills every gap in your spec with the statistically most common choice, which is rarely your choice.

Write specs in plain language, with examples. One example of the desired output is worth ten paragraphs of description — for machines exactly as for contractors.

**Practice:** Write a one-page spec for a small feature and hand it to an AI agent untouched. Every clarifying question it needs to ask is a hole in your spec.

---

## Email 6

**Subject:** Lesson 6: Grounding — when the answer must be true
**Preview:** Most hallucination problems are grounding problems wearing a scary name.

When plausible isn't good enough, ground the model in real sources: your documents, your database, live search, your codebase. Retrieval is the general pattern — fetch the relevant facts, put them in context, and instruct the model to answer from them and to say so when they don't contain the answer.

Design rule: any claim that will be acted on should be traceable to a source a human can check in one click.

**Practice:** Build a tiny grounded assistant over ten of your own documents, with citations. Test it with five questions you know the answers to — including one the documents cannot answer.

---

## Email 7

**Subject:** Lesson 7: Tools, not chat
**Preview:** An agent is a model in a loop. Its quality is mostly its tools.

An agent reads state, decides, acts, observes, repeats. Its quality is mostly the quality of its tools — small, well-named actions with crisp inputs and honest error messages. A vague tool produces a flailing agent the same way a vague API produces buggy clients.

Start embarrassingly small: one agent, three tools, one job. Reliability at small scope is the foundation everything larger gets built on.

**Practice:** Build a single-purpose agent with at most three tools that completes one real task you do weekly. Run it ten times; log every failure and its cause.

---

## Email 8

**Subject:** Lesson 8: Decomposition and orchestration
**Preview:** Big tasks defeat single agents the way big functions defeat single programmers.

The remedy is the same: decomposition. Split work into steps with checkable outputs, fan independent steps out in parallel, and keep control flow in deterministic code while the model handles judgment inside each step. The orchestrator decides *what* happens; agents decide *how*.

A good decomposition has a test at every seam — you can tell which step failed without reading every transcript.

**Practice:** Take a task too big for one prompt (a research report, a multi-file refactor). Draw the pipeline: steps, what each consumes and produces, how you verify each seam. Then build it.

---

## Email 9

**Subject:** Lesson 9: Assume the agent will do the worst thing it can
**Preview:** Then shrink what it can.

Agents fail in characteristic ways: they loop, overreach, declare victory early, or take a destructive shortcut that satisfies the letter of the goal. Engineer for it — least-privilege tools, budgets on time and actions, human approval on irreversible steps, logs you can replay.

The goal isn't an agent that never fails. It's a system where failure is bounded, visible, and cheap.

**Practice:** Red-team your own agent. Write the three worst things it could do with its current permissions; redesign so the worst is impossible and the other two are recoverable.

---

## Email 10

**Subject:** Lesson 10: Why demos lie
**Preview:** The demo is run by the builder, on inputs it handles.

Every AI feature demos well. Production is run by strangers on inputs you never imagined, and the gap between the two is invisible until you measure it. Teams without evals oscillate between overconfidence and panic — shipping on anecdotes, rolling back on anecdotes.

An eval is just a held-out set of real inputs with graded expected outputs, run on every change. Unit testing for behavior that is probabilistic instead of deterministic.

**Practice:** Collect twenty real inputs for an AI feature you use or build — including the ugly ones. Define what a passing answer looks like for each. That's your first eval set.

---

## Email 11

**Subject:** Lesson 11: The eval loop
**Preview:** Without it, improving your AI system is superstition.

A working loop has four parts: a dataset of real cases, a grader (exact match, assertions, or a model judging against a rubric), a score tracked over time, and the habit — every prompt change, model swap, or pipeline edit runs the evals before shipping.

Grade what matters, not what's easy: correctness first, then tone, format, cost. And keep feeding production failures back into the dataset; that's where evals earn their keep.

**Practice:** Automate yesterday's twenty cases into a script that outputs a score. Change your prompt and watch the number move. Then improve the score without breaking a previously passing case.

---

## Email 12

**Subject:** Lesson 12: Reviewing machine-written code
**Preview:** Never approve a diff you couldn't explain line by line.

AI code review is a different sport. The machine doesn't get tired or skip the boring parts — but it confidently invents APIs, silently drops requirements, and handles error paths that can't occur while missing the one that will.

Review for intent first: does this do what was asked? Then for the classic tells: unverified assumptions, dead code dressed as robustness, tests that assert the bug. The standard that keeps velocity from becoming debt: never approve a diff you couldn't explain line by line to a colleague.

**Practice:** Have an AI implement a small feature, then review with a written checklist: requirements covered, APIs verified to exist, errors handled honestly, tests that would fail if the feature broke.

---

## Email 13

**Subject:** Lesson 13: The one-day prototype
**Preview:** The correct response to "would this work?" is a prototype by tomorrow.

AI collapsed the cost of finding out. The skill is scoping: cut the idea to its single riskiest assumption, build only what tests it, fake everything else. A prototype is a question, not a product — it succeeds by producing an answer, even when the answer is no.

People who prototype weekly develop an unfair advantage: their opinions are backed by evidence while everyone else's are backed by slides.

**Practice:** Pick an idea you've debated for over a month. Define its riskiest assumption, then build the smallest thing that tests it — in one day, using every AI tool you have.

(Halfway, by the way. Quick question, reply in one word if you like: are you doing this track solo, or thinking about your team? If it's a team, this is exactly what our workshop does in a day — futureskillsacademy.ai/for-companies.html)

---

## Email 14

**Subject:** Lesson 14: From demo to production
**Preview:** The distance hasn't collapsed — it's become a checklist.

Handle the malformed input, add auth, bound the costs, log enough to debug a 3 a.m. failure, decide what happens when the model is down or slow or wrong. AI writes most of this too — but only if you ask. Models optimize for the happy path unless the spec says otherwise.

Ship behind a flag, to a small slice, with a way back. Boring deployment hygiene is what makes aggressive speed safe.

**Practice:** Write your prototype's production-gap list — everything between here and real users. Estimate each item, then knock out the top three with AI assistance.

---

## Email 15

**Subject:** Lesson 15: Operating AI systems
**Preview:** The code is unchanged but the world shifts.

AI systems degrade differently: new input patterns, model updates, a data source that quietly changed format. Operating one means watching quality, not just uptime — eval scores on live traffic samples, cost per request, latency, and the rate of "the AI said something weird" reports.

Every incident becomes a new eval case. That's the flywheel. And budget honestly: a system you can't afford to watch is a system you can't afford to run.

**Practice:** Write a one-page runbook for an AI feature: three quality metrics, alert thresholds, the rollback procedure, where new failure cases get filed.

---

## Email 16

**Subject:** Lesson 16: Reading code is the superpower now
**Preview:** When machines write most of it, the binding skill flips.

Reading fast and deep — tracing data flow, spotting silent assumptions, sensing where a design fights itself — is what lets you review ten times more code than you write. The engineers who thrive are the ones for whom a 500-line diff is an afternoon, not a week.

Reading is trainable the same way writing is: deliberately, on excellent material, with questions in hand.

**Practice:** Spend 45 minutes reading a well-regarded open-source codebase in your stack. Write down its three best design decisions and one you'd challenge — and why.

---

## Email 17

**Subject:** Lesson 17: Debugging as epistemology
**Preview:** "Ask the AI to fix it" in a loop is gambling with extra steps.

Debugging is the verification mindset at its purest: form a hypothesis, design the cheapest experiment that could kill it, run it, update. It transfers to everything — broken pipelines, weird agent behavior, business numbers that don't add up.

AI is a phenomenal debugging partner, but only for the person who can state symptoms precisely and judge proposed causes against evidence.

**Practice:** Next bug, write the hypothesis before touching code: "I believe X because Y; if true, Z will show it." Run exactly that check. Count how many hypotheses the bug takes.

---

## Email 18 — final

**Subject:** Lesson 18: The courage to be simple
**Preview:** Every component is cheap to create and expensive forever.

When generating code is free, complexity becomes the silent killer. Systems thinking is seeing the whole — where state lives, what talks to what, which dependency hurts you in a year. The discipline that follows is subtraction. The best AI-native engineers are conspicuous for how little they build.

Ask of every addition: what would have to be true for us to delete this in six months? If nothing, you're building a permanent liability.

**Practice:** Diagram your current system from memory. Find one component that exists for historical reasons, and write the one-paragraph case for deleting it.

That's the track. Two ways to keep going:

1. **The capstone** — ship an agentic product in fourteen days, spec to production. The full brief is on the track page.
2. **Bring it to your team.** Reading changes a person; practicing together changes a team. We run this as a one-day workshop on your own codebase: https://futureskillsacademy.ai/for-companies.html

Thanks for doing the work. Reply anytime — I read everything.
— Birger
