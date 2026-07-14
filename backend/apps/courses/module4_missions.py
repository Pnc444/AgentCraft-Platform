def _artifact(
    path: str,
    summary: str,
    artifact_format: str,
    *,
    inspect_prompt: str | None = None,
    change_prompt: str | None = None,
) -> dict:
    artifact = {
        "path": path,
        "summary": summary,
        "format": artifact_format,
    }
    if inspect_prompt is not None:
        artifact["inspect_prompt"] = inspect_prompt
    if change_prompt is not None:
        artifact["change_prompt"] = change_prompt
    return artifact


def _tutor_prompt(lesson_title: str, focus: str) -> str:
    return f"""You are the AgentCraft course tutor for the lesson "{lesson_title}".

Who you are teaching: an intelligent adult beginner with zero AI background. Assume they can think clearly. Never assume they know jargon. Introduce every technical word with a plain-English anchor the first time it appears.

How to behave:
- Attempt-first: before explaining, ask what they currently think, then build on their own words.
- One idea per reply. End every reply with the single next step, never a menu of options.
- Use the course's running example (Juno, the research helper) before inventing new examples.
- If the learner answers correctly and then asks whether they are really sure, confirm once in one plain sentence and move forward. Do not reopen a settled point. Re-explaining a correct answer teaches doubt.
- If they are wrong, name what was right first, then give the one adjustment.
- Never dramatize risk. If something can go wrong, say exactly what would happen and how it is undone.
- Never use em dashes in your replies.
- When the learner can do what the lesson's "Done means done" list asks, say so plainly and tell them it is safe to stop.

Focus for this lesson: {focus}
"""


MODULE_4_MISSION_PACK = {
    "title": "Module 4: How Agents Think",
    "slug": "module-4-ai-agents",
    "description": (
        "Meet one small AI helper, learn the six questions that describe any agent, "
        "and design your own on paper. No installs, no jargon, one idea at a time."
    ),
    "difficulty": 2,
    "order": 5,
    "publish_rules": [
        "requires_non_placeholder_content",
        "requires_tutor_prompts",
        "requires_valid_quiz_banks",
        "requires_guided_blocks",
        "requires_checkpoint_banks",
        "requires_agent_learning_artifacts",
    ],
    "lessons": [
        {
            "title": "What an Agent Actually Is",
            "slug": "what-an-ai-agent-is",
            "lesson_type": "theory",
            "estimated_minutes": 10,
            "content": """# What an Agent Actually Is

*Lesson 1 of 7 · about 10 minutes · nothing to install, nothing to memorize.*

Here is the plan for this module: meet one small imaginary helper, watch how it thinks, and by the last lesson design your own version on paper. No code. No setup. One idea at a time.

## Meet Juno

Juno is a research helper. You say:

> "Find me three good articles about how sleep affects memory, and summarize each one."

Juno searches, skims what it finds, throws away the junk, writes three short summaries, shows them to you, and then stops.

That little story contains everything an AI agent is.

**An agent is a system that takes a goal, works toward it in steps, uses tools when it needs them, checks its own work, and stops when the job is done.**

A chatbot *answers* you. An agent *does something* for you, then reports back. That is the whole difference.

## The six questions

Any agent can be described by six plain questions:

1. **Goal**: what does the human actually want?
2. **Plan**: what should it try next?
3. **Tools**: what is it allowed to do? (search, read, write)
4. **Memory**: what should it keep track of while working?
5. **Check**: how does it know its work is any good?
6. **Stop**: how does it know it is finished?

For Juno: the goal is "three good summaries." The plan starts with "search." Its tools are search and read. Its memory is the list of articles found so far. Its check is "is this article actually about sleep and memory?" Its stop rule is "three good summaries delivered."

You do **not** need to memorize these. Lessons 2 through 6 each pick one or two of them up and turn them over slowly. They stick from use, not rehearsal.

## Done means done

You are done with this lesson when you can:

- say what Juno does in one sentence
- name roughly what the six questions cover (peeking at the Agent Map below is fine)

One pass through this page is enough. If the six questions feel loose, that is normal. The rest of the module exists to tighten them.
""",
            "ai_tutor_prompt": _tutor_prompt(
                "What an Agent Actually Is",
                "the one-sentence definition of an agent, told through Juno the research helper, and a first gentle pass over the six questions (goal, plan, tools, memory, check, stop).",
            ),
            "questions": [
                {
                    "id": "module4-agent-q1",
                    "prompt": "You ask Juno for three article summaries. It delivers them and stops. Which part of the six questions did the stopping come from?",
                    "options": [
                        "The plan: its original plan happened to include stopping at that point",
                        "The stop rule: the finish line was defined before the work started",
                        "The memory: it forgot what else to do",
                    ],
                    "answer_index": 1,
                },
                {
                    "id": "module4-agent-q2",
                    "prompt": "An app replies to every support email with the same fixed template. A friend calls it an AI agent. What is the kindest accurate correction?",
                    "options": [
                        "It never chooses a next step based on what it finds, so it is an auto-responder, not an agent",
                        "It is an agent, just a very small one, since replying automatically is acting on the world",
                        "It would be an agent if it were written in a different language",
                    ],
                    "answer_index": 0,
                },
                {
                    "id": "module4-agent-q3",
                    "prompt": "Juno reads an article and asks itself 'is this actually about sleep and memory?' before keeping it. Which question is Juno answering?",
                    "options": [
                        "Goal: it is re-reading the instructions",
                        "Tools: it is choosing what it is allowed to do",
                        "Check: it is judging its own work before trusting it",
                    ],
                    "answer_index": 2,
                },
                {
                    "id": "module4-agent-q4",
                    "prompt": "What separates an agent from a chatbot in this course's definition?",
                    "options": [
                        "An agent acts toward a goal and checks its work; a chatbot mainly answers",
                        "An agent runs on a bigger and more advanced AI model than a chatbot does",
                        "An agent always talks to more than one person at a time",
                    ],
                    "answer_index": 0,
                },
                {
                    "id": "module4-agent-q5",
                    "prompt": "Juno finds its three good articles in two minutes but keeps searching for twenty more. What is missing from its design?",
                    "options": [
                        "More memory to hold extra articles",
                        "A better plan: the first search should have been written more carefully",
                        "A working stop rule: the goal was met, so the work should end",
                    ],
                    "answer_index": 2,
                },
            ],
            "guided_blocks": [
                {
                    "title": "One helper, one errand",
                    "predict_first": {
                        "question": "Before reading further: imagine you asked a capable friend to 'find three good articles about sleep and memory and summarize them.' What would your friend actually do, step by step?",
                        "hint": "Your friend would probably search, skim, reject some results, keep others, and know when to stop. Hold that picture.",
                    },
                    "body": "Whatever steps you just imagined (search, skim, judge, keep, stop) are exactly what an agent does. You already understand the idea. This module just gives its parts names.",
                    "analogy": "An agent is a careful helper running an errand: it gets the assignment, uses the tools it is allowed to use, judges what it finds, and reports back instead of guessing.",
                },
                {
                    "title": "The six questions, one pass",
                    "body": "Goal, plan, tools, memory, check, stop. Read the Agent Map below once, matching each question to what Juno does. One pass is enough; every later lesson reuses these six.",
                    "try_this": [
                        "Open the Agent Map artifact and read it once, top to bottom.",
                        "Say out loud which question 'three good summaries delivered' belongs to.",
                    ],
                    "checkpoint_after": True,
                },
                {
                    "title": "What makes it an agent and not a chatbot",
                    "body": "The word 'agent' earns its keep in two places: the helper *acts* (it does things, not just says things) and it *checks* (it looks at results instead of assuming). If a system can neither act nor check, it is a chatbot wearing a costume.",
                    "remember": "Acts and checks. Everything else is detail.",
                },
                {
                    "title": "If you're tempted to call everything an agent",
                    "body": "Out in the world, the word 'agent' gets stamped on all kinds of products, including plain question-and-answer tools. The labels out there really are inconsistent. This course uses one steady definition so you always have solid ground.",
                    "remember": "When in doubt, ask: does it act, and does it check?",
                    "kind": "common_mistake",
                },
                {
                    "title": "Say it back, once",
                    "body": "Explain Juno to an imaginary friend in two sentences: what it does, and how it knows when it is finished. If you can do that, even clumsily, this lesson has done its job.",
                    "try_this": [
                        "Two sentences, out loud or in your head. Once is enough.",
                    ],
                    "kind": "teach_it_back",
                },
            ],
            "checkpoint_questions": [
                {
                    "id": "module4-agent-cp1",
                    "prompt": "In one phrase, what does an agent do that a chatbot does not?",
                    "options": [
                        "It acts toward a goal and checks its work",
                        "It talks in longer paragraphs",
                        "It runs on a special kind of computer",
                    ],
                    "answer_index": 0,
                },
                {
                    "id": "module4-agent-cp2",
                    "prompt": "Which of these is one of the six questions?",
                    "options": [
                        "What color is the interface?",
                        "How does it know it is finished?",
                        "How many users does it have?",
                    ],
                    "answer_index": 1,
                },
                {
                    "id": "module4-agent-cp3",
                    "prompt": "Do you need to memorize the six questions before the next lesson?",
                    "options": [
                        "Yes, the next lesson assumes perfect recall",
                        "Yes, there is a closed-book test first",
                        "No, later lessons reuse them, so they stick from use",
                    ],
                    "answer_index": 2,
                },
            ],
            "skill_templates": [],
            "channel_templates": [],
            "safety_checks": [],
            "permission_matrix": [],
            "evaluation_rubric": [],
            "evaluation_cases": [],
            "artifacts": [
                _artifact(
                    "lesson_artifacts/agents/agent-map.md",
                    "The six questions that describe any agent, with Juno's answers filled in.",
                    "text",
                    inspect_prompt="Read the map once. For each of the six questions, notice Juno's answer sitting right next to it.",
                    change_prompt="Cover Juno's column and fill in the six answers for a helper that reminds you when library books are due. Rough answers count.",
                )
            ],
        },
        {
            "title": "Answerer, Checklist, or Agent?",
            "slug": "agents-vs-chatbots",
            "lesson_type": "theory",
            "estimated_minutes": 8,
            "content": """# Answerer, Checklist, or Agent?

*Lesson 2 of 7 · about 8 minutes · builds on Juno from Lesson 1.*

You know what an agent is. This lesson gives you the two things an agent is *not*, because telling them apart is what keeps the word from turning into fog.

## Three shapes of helper

- **An answerer** (a chatbot) replies to what you ask. Question in, answer out. It does not act on the world.
- **A checklist** (a workflow) runs the same fixed steps every time. Step 1, step 2, step 3, done. Reliable, but it cannot change course.
- **An agent** chooses its next step based on what it just found. It can change course mid-errand.

Same topic, three shapes. A sleep-and-memory *answerer* quotes a saved paragraph. A sleep-and-memory *checklist* always fetches the same three websites and pastes their intros. Juno, the *agent*, searches, judges what it finds, and searches again if the results are junk.

## The honest part: simpler is usually better

Here is something the hype never says: **most jobs do not need an agent.**

If a fixed answer solves it, use an answerer. If the steps never change, use a checklist. Agents cost more, can wander, and take more care to trust. Choosing the boring shape when the boring shape works is what good engineers do.

One question sorts almost every case:

> **Can I write down all the steps in advance?**

If yes, you want a checklist. If the next step depends on what the last step found, the way Juno's second search depends on the first, that is when an agent earns its cost.

## Done means done

You are done when you can:

- name the three shapes with a one-line difference between them
- answer the sorting question for one example of your own

There is no hidden nuance here. The three-shape picture really is this simple, on purpose.
""",
            "ai_tutor_prompt": _tutor_prompt(
                "Answerer, Checklist, or Agent?",
                "telling chatbots (answerers), workflows (checklists), and agents apart, and practicing the sorting question: can I write down all the steps in advance? Reinforce that choosing the simpler shape is good judgment.",
            ),
            "questions": [
                {
                    "id": "module4-compare-q1",
                    "prompt": "A university wants to auto-answer twenty fixed FAQ questions. Which shape fits, and why?",
                    "options": [
                        "An agent, because anything involving AI should use one",
                        "An answerer: the responses are fixed, so nothing needs to decide a next step",
                        "A checklist: each of the twenty questions is one fixed step to run in order",
                    ],
                    "answer_index": 1,
                },
                {
                    "id": "module4-compare-q2",
                    "prompt": "A grading script maps 90+ to A, 80+ to B, 70+ to C, else F. Which shape is it?",
                    "options": [
                        "A checklist: every step and rule is written in advance",
                        "An agent: it makes decisions about numbers",
                        "An answerer: it produces one output per input",
                    ],
                    "answer_index": 0,
                },
                {
                    "id": "module4-compare-q3",
                    "prompt": "A teammate says: 'Let's use agents for everything, they're smarter.' What is the fair reply?",
                    "options": [
                        "Agree: agents are the most capable shape, and capability is always worth having",
                        "Disagree: agents cannot handle real production work",
                        "Agents cost more and need more care; use the simplest shape that solves the job reliably",
                    ],
                    "answer_index": 2,
                },
                {
                    "id": "module4-compare-q4",
                    "prompt": "Which task genuinely needs an agent rather than a simpler shape?",
                    "options": [
                        "Sending the same fixed weekly summary email to every subscriber each Monday at 9am",
                        "Diagnosing a server outage: check logs, try a fix, verify, escalate if still broken",
                        "Showing today's temperature on a dashboard",
                    ],
                    "answer_index": 1,
                },
                {
                    "id": "module4-compare-q5",
                    "prompt": "You spent a week building an agent that sends one fixed welcome message on signup. A colleague says a simple trigger would have done it. Are they right?",
                    "options": [
                        "Yes: the steps never change, so a checklist-style trigger was the right size",
                        "No: anything users see justifies an agent, and the week was an investment in quality",
                        "Only if the number of signups is small",
                    ],
                    "answer_index": 0,
                },
            ],
            "guided_blocks": [
                {
                    "title": "Three helpers, one errand",
                    "predict_first": {
                        "question": "Three helpers are asked about sleep and memory. One recites a saved paragraph. One always fetches the same three websites. One searches, judges, and re-searches if results are junk. Which one is Juno?",
                        "hint": "Which helper's next step depends on what the previous step found?",
                    },
                    "body": "The third helper is Juno. The first is an answerer, the second a checklist. All three are legitimate designs. The skill you are building is naming which one you are looking at.",
                    "analogy": "An answerer is a receptionist, a checklist is a recipe, and an agent is a teammate who can decide the recipe needs changing halfway through.",
                },
                {
                    "title": "The sorting question",
                    "body": "One question does almost all the work: can I write down all the steps in advance? If yes, a checklist will be cheaper, steadier, and easier to trust. If the next step depends on findings, you are in agent territory.",
                    "remember": "Steps knowable in advance: checklist. Steps that depend on findings: agent.",
                    "try_this": [
                        "Open the comparison table below and read the 'How to spot one' row. Once through is plenty.",
                    ],
                    "checkpoint_after": True,
                },
                {
                    "title": "Permission to choose the boring option",
                    "body": "If you catch yourself thinking 'a plain checklist would work here, but an agent sounds more impressive,' the checklist is the right answer. Systems you can fully predict are systems you can fully trust.",
                    "remember": "Boring and predictable is a compliment in engineering.",
                },
                {
                    "title": "The label trap",
                    "body": "Marketing calls all three shapes 'agents.' If a product's label and its behavior disagree, trust the behavior. Does it act? Does it check? Does its next step depend on findings? The label cannot change the answers.",
                    "remember": "Judge the behavior, not the label.",
                    "kind": "common_mistake",
                },
                {
                    "title": "Say it back, once",
                    "body": "One sentence per shape, then one more for the sorting question. Four sentences total, once, and you are done here.",
                    "try_this": [
                        "Four sentences. Use receptionist, recipe, and teammate if the analogy helps.",
                    ],
                    "kind": "teach_it_back",
                },
            ],
            "checkpoint_questions": [
                {
                    "id": "module4-compare-cp1",
                    "prompt": "Which shape follows the same fixed steps every time?",
                    "options": [
                        "The agent",
                        "The answerer",
                        "The checklist",
                    ],
                    "answer_index": 2,
                },
                {
                    "id": "module4-compare-cp2",
                    "prompt": "What is the sorting question from this lesson?",
                    "options": [
                        "Can I write down all the steps in advance?",
                        "Which shape uses the newest AI model?",
                        "How many users will the system have?",
                    ],
                    "answer_index": 0,
                },
                {
                    "id": "module4-compare-cp3",
                    "prompt": "Why prefer a simpler shape when it solves the job?",
                    "options": [
                        "Simpler shapes are always faster to build",
                        "Predictable systems are easier to test and trust",
                        "Agents are not allowed in production",
                    ],
                    "answer_index": 1,
                },
            ],
            "skill_templates": [],
            "channel_templates": [],
            "safety_checks": [],
            "permission_matrix": [],
            "evaluation_rubric": [],
            "evaluation_cases": [],
            "artifacts": [
                _artifact(
                    "lesson_artifacts/agents/chatbot-workflow-agent-table.md",
                    "One-screen table: answerer vs checklist vs agent, with a 'how to spot one' row.",
                    "text",
                    inspect_prompt="Find the 'How to spot one' row and read it against the three shapes.",
                    change_prompt="Add one example of your own from daily life to any column. School, work, or home all count.",
                )
            ],
        },
        {
            "title": "The Loop: Watch Juno Work",
            "slug": "basic-agent-workflow",
            "lesson_type": "theory",
            "estimated_minutes": 10,
            "content": """# The Loop: Watch Juno Work

*Lesson 3 of 7 · about 10 minutes · one complete errand, seen from the inside.*

You know what an agent is and when one is worth building. Now watch one run. Agents work in a **loop**, a small cycle of five steps that repeats until the job is done:

1. **Understand** the goal.
2. **Plan** the next step.
3. **Act**: use a tool.
4. **Look** at what happened.
5. **Decide**: continue, adjust, or stop.

That reads abstract, so here is the same thing as a story.

## Juno's errand, from the inside

**Your request:** "Find three good articles about sleep and memory. Summarize each."

> **Understand.** Three articles. Must be good. Must be summarized.
>
> **Plan.** Start with a search for "sleep memory research."
>
> **Act.** Search runs. Ten results come back.
>
> **Look.** Result 1 is a mattress advertisement. Result 2 is a solid university study. Result 3 is paywalled and unreadable.
>
> **Decide.** Keep result 2. Skip the ad and the paywall. Two more needed. Continue.
>
> **Plan.** Try a narrower search: "sleep deprivation memory study."
>
> **Act, look, decide.** Two more solid articles found. That makes three. Summarize each, deliver, **stop.**

Notice two things about that trace.

**The paywall was not a crisis.** A tool came back with a result Juno could not use, and the loop simply absorbed it: look, decide, adjust. In a loop, a failed step is just information for the next step.

**The first plan was not the final plan.** Juno's opening search was not good enough, and that was fine. Agents are built on the assumption that plans get revised. The first plan is a starting point, not a promise.

## Done means done

You are done when you can:

- recite the five steps in order (the artifact card holds them permanently)
- point at the moment in Juno's trace where the loop absorbed a failure

Next lesson takes the two quietest words in the loop, *look* and *stop*, and shows why they matter most.
""",
            "ai_tutor_prompt": _tutor_prompt(
                "The Loop: Watch Juno Work",
                "the five-step loop (understand, plan, act, look, decide), taught through Juno's errand trace. Emphasize that failed steps are absorbed calmly by the loop and that first plans are meant to be revised.",
            ),
            "questions": [
                {
                    "id": "module4-workflow-q1",
                    "prompt": "In Juno's trace, the paywalled article gets skipped and the plan adjusts. Which loop steps did that?",
                    "options": [
                        "Understand and plan: Juno went back and re-read the goal before continuing",
                        "Look and decide: the result was examined, then the plan changed",
                        "Act alone: the tool fixed it automatically",
                    ],
                    "answer_index": 1,
                },
                {
                    "id": "module4-workflow-q2",
                    "prompt": "An agent finds an article and delivers it immediately without reading what it found. Which step did it skip?",
                    "options": [
                        "Look: it never examined the result before trusting it",
                        "Plan: it should have planned a longer search",
                        "Understand: the goal was too vague",
                    ],
                    "answer_index": 0,
                },
                {
                    "id": "module4-workflow-q3",
                    "prompt": "A hotel-booking agent finds a room for $89 against a $100 budget. What should the decide step conclude?",
                    "options": [
                        "Keep searching: an even cheaper room might still exist somewhere out there",
                        "Ask the user to revise the budget goal",
                        "Stop: the goal is met; continuing adds time and risk for no gain",
                    ],
                    "answer_index": 2,
                },
                {
                    "id": "module4-workflow-q4",
                    "prompt": "A tool call returns an error mid-loop. What happens next in a well-built agent?",
                    "options": [
                        "The error flows into look-and-decide, and the plan adjusts",
                        "The agent halts and erases all progress so far",
                        "The agent repeats the identical call until it succeeds",
                    ],
                    "answer_index": 0,
                },
                {
                    "id": "module4-workflow-q5",
                    "prompt": "Why is 'the first plan is a starting point, not a promise' good agent design rather than sloppiness?",
                    "options": [
                        "Because writing one careful plan up front would take longer than the errand itself",
                        "Because the world answers back: results arrive that no plan could fully predict",
                        "Because agents cannot store plans in memory",
                    ],
                    "answer_index": 1,
                },
            ],
            "guided_blocks": [
                {
                    "title": "Five steps, one cycle",
                    "predict_first": {
                        "question": "You try a new recipe and the sauce comes out too thin. What do you do next, and what does that say about how you handle steps that misfire?",
                        "hint": "You look at the sauce, judge it, and adjust. You do not throw out the meal.",
                    },
                    "body": "Understand, plan, act, look, decide. You already run this loop whenever you cook, debug, or pack for a trip. The agent version is the same cycle made explicit, which is exactly what lets a machine run it.",
                    "analogy": "The loop is a lab session: read the instructions, try something, look at the result, decide what to try next.",
                },
                {
                    "title": "The failure that wasn't",
                    "body": "Re-read the paywall moment in Juno's trace. A step failed and the loop treated it as ordinary input: look, decide, adjust. The loop exists precisely so that no single step has to go perfectly.",
                    "remember": "In a loop, a failed step is information, not an emergency.",
                    "checkpoint_after": True,
                },
                {
                    "title": "Where a human fits",
                    "body": "The decide step has one more option: *ask a human*. Real agents pause and hand control back when a step is risky or ambiguous. In Modules 6 and 8 this becomes a setting you configure, so there is no need to hold onto it now.",
                    "try_this": [
                        "Open the loop card below and find where 'ask a human' sits in the decide step.",
                    ],
                },
                {
                    "title": "The perfect-plan trap",
                    "body": "It is tempting to think a well-built agent plans everything perfectly up front, and that revising a plan means failing. The opposite is true: revision is the loop working as designed. The same grace applies to you as you learn this material.",
                    "remember": "Revising the plan is the loop succeeding, not failing.",
                    "kind": "common_mistake",
                },
                {
                    "title": "Say it back, once",
                    "body": "Tell Juno's errand as a story in five beats, including the paywall moment. Once through, out loud or silently, and this lesson is complete.",
                    "try_this": [
                        "Five beats, one pass. If you forget a beat, glance at the card and finish. That still counts.",
                    ],
                    "kind": "teach_it_back",
                },
            ],
            "checkpoint_questions": [
                {
                    "id": "module4-workflow-cp1",
                    "prompt": "What does the agent do immediately after it acts?",
                    "options": [
                        "It looks at what happened",
                        "It forgets the goal",
                        "It delivers whatever it has",
                    ],
                    "answer_index": 0,
                },
                {
                    "id": "module4-workflow-cp2",
                    "prompt": "What makes the workflow a loop rather than a straight line?",
                    "options": [
                        "It always runs forever",
                        "The decide step can send work back to planning",
                        "The word loop appears in the title",
                    ],
                    "answer_index": 1,
                },
                {
                    "id": "module4-workflow-cp3",
                    "prompt": "How does a well-built loop treat a failed step?",
                    "options": [
                        "As proof the whole errand must restart",
                        "As something to hide from the user",
                        "As information for the next decide step",
                    ],
                    "answer_index": 2,
                },
            ],
            "skill_templates": [],
            "channel_templates": [],
            "safety_checks": [],
            "permission_matrix": [],
            "evaluation_rubric": [],
            "evaluation_cases": [],
            "artifacts": [
                _artifact(
                    "lesson_artifacts/agents/basic-agent-loop.md",
                    "The five-step loop card, plus Juno's errand trace condensed to one screen.",
                    "text",
                    inspect_prompt="Find where 'ask a human' lives in the decide step, and find the moment the trace absorbs a failure.",
                    change_prompt="Rewrite the trace for a different errand, like finding a free study room, keeping the same five beats.",
                )
            ],
        },
        {
            "title": "Checks and Stop Rules",
            "slug": "knowing-when-to-stop",
            "lesson_type": "theory",
            "estimated_minutes": 8,
            "content": """# Checks and Stop Rules

*Lesson 4 of 7 · about 8 minutes · the two quietest words in the loop, and why they matter most.*

Last lesson, two small words did heavy lifting: *look* and *stop*. This lesson gives them their full names, **checks** and **stop rules**. They are the difference between an agent you can trust and one you can't.

## Checks: the agent doubts itself so you don't have to

A **check** is a moment where the agent examines its own work before believing it. Juno asking "is this article actually about sleep and memory?" is a check. A coding agent running the tests after an edit is a check.

Checks matter because AI systems can produce confident-sounding work that is wrong. A good agent assumes this about itself and verifies instead of trusting its first draft. The burden of doubting the work belongs to the system, by design.

## Stop rules: the finish line is drawn before the race

A **stop rule** is written *before* the work starts, and it comes in three kinds:

1. **Goal met.** "Three good summaries delivered." Stop.
2. **Limit hit.** "No more than ten searches" or "no more than five minutes." Stop and report what you have.
3. **Ask a human.** Anything ambiguous or risky: stop and hand it back.

The second kind deserves a highlight. A limit means the agent stops *even if the goal is not met*. It comes back and says "here is how far I got." An agent that can say that is far more trustworthy than one that promises to succeed, because it can never silently run away with a task.

There is a quiet lesson here that goes beyond agents: **well-designed work has its finish line drawn in advance.** It is why every lesson in this course ends with a "done means done" list. When the finish line is written down, you get to actually finish.

## Done means done

You are done when you can:

- give one example of a check (Juno's article test counts)
- name the three kinds of stop rules, roughly

Short lesson on purpose. The idea is small, sharp, and worth keeping undiluted.
""",
            "ai_tutor_prompt": _tutor_prompt(
                "Checks and Stop Rules",
                "checks (the agent verifies its own work so the human does not carry the doubt) and the three kinds of stop rules (goal met, limit hit, ask a human). Emphasize that limits make agents more trustworthy, and that finish lines drawn in advance are what allow real completion.",
            ),
            "questions": [
                {
                    "id": "module4-stop-q1",
                    "prompt": "An agent has sent 200 job applications in 30 minutes and is still going. What is missing?",
                    "options": [
                        "A bigger model that knows when enough is enough",
                        "A limit-type stop rule: a cap on actions or time",
                        "More memory to track the applications sent",
                    ],
                    "answer_index": 1,
                },
                {
                    "id": "module4-stop-q2",
                    "prompt": "Juno summarizes three articles, then verifies each summary against its source before delivering. What is that final pass?",
                    "options": [
                        "A check: the agent examines its own work before trusting it",
                        "A stop rule: it stopped at exactly three",
                        "A plan revision: it changed course mid-errand",
                    ],
                    "answer_index": 0,
                },
                {
                    "id": "module4-stop-q3",
                    "prompt": "Why does 'no more than ten searches, then report what you have' make an agent MORE trustworthy?",
                    "options": [
                        "It guarantees the goal is achieved before the searches are used up",
                        "It makes the agent run faster overall",
                        "It means the agent can never silently run away with a task",
                    ],
                    "answer_index": 2,
                },
                {
                    "id": "module4-stop-q4",
                    "prompt": "An agent hits something ambiguous: the user asked for 'good' articles and two candidates seem borderline. Which stop rule fits best?",
                    "options": [
                        "Goal met: deliver the borderline ones and end",
                        "Ask a human: hand the judgment call back",
                        "Limit hit: the errand has taken too long",
                    ],
                    "answer_index": 1,
                },
                {
                    "id": "module4-stop-q5",
                    "prompt": "When should an agent's finish line be defined?",
                    "options": [
                        "Before the work starts",
                        "Whenever the agent feels the work is complete",
                        "After a human reviews the first draft",
                    ],
                    "answer_index": 0,
                },
            ],
            "guided_blocks": [
                {
                    "title": "Who carries the doubt?",
                    "predict_first": {
                        "question": "Two assistants summarize an article. One hands you its first draft. One re-reads the article, verifies its own summary, then hands it over. Which do you re-check more, and who is doing the doubting in each case?",
                        "hint": "With the first assistant, the doubting is your job. With the second, the system carries it.",
                    },
                    "body": "A check moves the burden of doubt from the human into the system. That is its entire purpose. When an agent verifies its own work, you are being handed work that has already been examined.",
                    "analogy": "A check is the carpenter's 'measure twice, cut once,' built into the tool itself.",
                },
                {
                    "title": "Three ways to stop",
                    "body": "Goal met. Limit hit. Ask a human. Every trustworthy agent has at least the first two, and the second is the unsung hero: an agent with a limit always comes back, even when the errand goes sideways.",
                    "remember": "Goal met, limit hit, ask a human. 'Limit hit' is the one that makes agents safe to leave alone.",
                    "try_this": [
                        "Open the card below and read the three stop rules once.",
                    ],
                    "checkpoint_after": True,
                },
                {
                    "title": "Finish lines drawn in advance",
                    "body": "The stop rule is written before the loop starts, which is what lets the agent genuinely finish. This course is built the same way: each lesson's 'done means done' list is a stop rule for you. When you meet it, you may close the page.",
                    "remember": "A finish line drawn in advance is what makes finishing real.",
                },
                {
                    "title": "The 'one more search' trap",
                    "body": "The tempting design mistake is letting an agent keep going in case something better exists. A perfect answer might always be one more search away, which is exactly why the search must end by rule, not by feeling. Good enough, verified, and delivered beats perfect and never finished.",
                    "remember": "End by rule, not by feeling.",
                    "kind": "common_mistake",
                },
                {
                    "title": "Say it back, once",
                    "body": "One sentence for checks, one for each stop rule. Four sentences, one pass, done.",
                    "try_this": [
                        "Optional, 30 seconds: name a stop rule you could borrow for your own studying.",
                    ],
                    "kind": "teach_it_back",
                },
            ],
            "checkpoint_questions": [
                {
                    "id": "module4-stop-cp1",
                    "prompt": "What is a check?",
                    "options": [
                        "The agent examining its own work before trusting it",
                        "A human approving the agent's budget",
                        "The agent pausing between loop steps",
                    ],
                    "answer_index": 0,
                },
                {
                    "id": "module4-stop-cp2",
                    "prompt": "Which stop rule means the agent stops even if the goal is not met?",
                    "options": [
                        "Goal met",
                        "Ask a human",
                        "Limit hit",
                    ],
                    "answer_index": 2,
                },
                {
                    "id": "module4-stop-cp3",
                    "prompt": "When is an agent's finish line written?",
                    "options": [
                        "Before the work starts",
                        "While the loop is running",
                        "After the results are delivered",
                    ],
                    "answer_index": 0,
                },
            ],
            "skill_templates": [],
            "channel_templates": [],
            "safety_checks": [],
            "permission_matrix": [],
            "evaluation_rubric": [],
            "evaluation_cases": [],
            "artifacts": [
                _artifact(
                    "lesson_artifacts/agents/stop-rules-and-checks.md",
                    "One-screen card: two kinds of checks and three kinds of stop rules, with Juno examples.",
                    "text",
                    inspect_prompt="Find which stop rule lets an agent come back without finishing, and why that builds trust.",
                    change_prompt="Write one stop rule for a helper of your own invention. One honest sentence is a complete answer.",
                )
            ],
        },
        {
            "title": "Notebook, Hands, Judgment",
            "slug": "memory-tools-reasoning",
            "lesson_type": "theory",
            "estimated_minutes": 9,
            "content": """# Notebook, Hands, Judgment

*Lesson 5 of 7 · about 9 minutes · no new behavior, just names for parts you have already watched.*

A promise before anything else: **this lesson contains nothing you have not already seen.** You watched Juno work in Lesson 3. This lesson takes the machine apart and labels three components. If parts feel familiar, that is the design working.

An agent is built from three parts:

## Memory: the notebook

What the agent keeps track of while it works. Juno's notebook held "one solid study so far, need two more." Without it, every loop cycle would start from zero and Juno would re-find the same article forever.

*Memory answers: what should be kept?*

## Tools: the hands

What the agent is allowed to *do*. Juno had two: search and read. A coding agent might have: read files, edit files, run tests. Tools are granted, not assumed. An agent without a "write" tool cannot write anything, no matter how clever it is. A human grants each tool, and you will do that yourself in Module 6.

*Tools answer: what can be done?*

## Judgment: the deciding

The part that chooses the next step: keep this article, skip that one, search again, stop now. In real agents this is the AI model's job. Judgment is only as good as what feeds it. With a thin notebook or the wrong hands, even brilliant judgment fails, which is why builders spend most of their effort on memory and tools.

*Judgment answers: what should happen next?*

## Where you will touch these for real

In Module 6 you will build an assistant with a tool called OpenClaw, and these three become things you can open on your computer: memory lives in folders and files, tools are granted in a settings file, judgment comes from the AI model you pick. That is all the preview you need. Module 6 re-teaches everything from scratch.

## Done means done

You are done when you can:

- match notebook, hands, and judgment to memory, tools, and reasoning
- say which question each part answers: kept, done, or next

The cheat sheet below holds these permanently, so your head does not have to.
""",
            "ai_tutor_prompt": _tutor_prompt(
                "Notebook, Hands, Judgment",
                "the three components of an agent: memory (notebook: what is kept?), tools (hands: what can be done?), and judgment (what happens next?). Reassure the learner that familiarity is deliberate: this lesson names parts they already watched in Juno's trace.",
            ),
            "questions": [
                {
                    "id": "module4-mtr-q1",
                    "prompt": "A support agent gives contradictory answers to the same question two days apart because it retains nothing between conversations. Which part is weak?",
                    "options": [
                        "Judgment: the model reasons differently from one day to the next",
                        "Memory: nothing from earlier work is being kept or used",
                        "Tools: it lacks a search capability",
                    ],
                    "answer_index": 1,
                },
                {
                    "id": "module4-mtr-q2",
                    "prompt": "An agent can search the web but cannot save files, by policy. It plans well and remembers context. Which part has been deliberately restricted?",
                    "options": [
                        "Tools: its allowed actions stop at reading",
                        "Memory: it cannot retain anything",
                        "Judgment: it cannot plan without file access",
                    ],
                    "answer_index": 0,
                },
                {
                    "id": "module4-mtr-q3",
                    "prompt": "An agent has accurate information and working tools but keeps choosing unhelpful next steps. Which part needs work?",
                    "options": [
                        "Memory: it should store more details",
                        "Tools: it needs more capabilities to choose from",
                        "Judgment: the deciding is not using what it has",
                    ],
                    "answer_index": 2,
                },
                {
                    "id": "module4-mtr-q4",
                    "prompt": "An agent asks you the same question it asked two steps ago, having lost your earlier answer. Which part failed?",
                    "options": [
                        "Memory: earlier context within the task was not kept",
                        "Tools: the question-asking tool was accidentally called a second time",
                        "Judgment: the model is too small",
                    ],
                    "answer_index": 0,
                },
                {
                    "id": "module4-mtr-q5",
                    "prompt": "Why do experienced agent-builders spend more effort on memory and tools than on chasing the cleverest model?",
                    "options": [
                        "Clever models are too expensive to run on everyday agent errands",
                        "Judgment can only work with what the notebook and hands provide it",
                        "Memory and tools are easier to advertise",
                    ],
                    "answer_index": 1,
                },
            ],
            "guided_blocks": [
                {
                    "title": "You have already seen all three",
                    "predict_first": {
                        "question": "Think back to Juno's errand trace. Where did Juno keep 'one solid study so far'? What let it search? What chose to skip the mattress ad?",
                        "hint": "Three different parts did those three different jobs.",
                    },
                    "body": "The tally of articles was memory. The search was a tool. Skipping the ad was judgment. Nothing new happened in this lesson; the machine you already watched just got labels on its parts.",
                    "analogy": "Memory is the notebook, tools are the hands, judgment is the deciding mind.",
                },
                {
                    "title": "Three questions, three parts",
                    "body": "Memory answers 'what should be kept?' Tools answer 'what can be done?' Judgment answers 'what should happen next?' Route those three questions to the three parts and you have the whole lesson.",
                    "try_this": [
                        "Open the cheat sheet below and match each question to its part. One pass.",
                    ],
                    "checkpoint_after": True,
                },
                {
                    "title": "Tools are granted, not assumed",
                    "body": "An agent's hands are given to it by a human, deliberately, one at a time. An agent physically cannot take an action nobody granted it. In Module 6, granting a tool is a line you write in a settings file, once, calmly, in advance.",
                    "remember": "No tool granted, no action possible. The human decides.",
                },
                {
                    "title": "The magic-judgment trap",
                    "body": "It is easy to treat the AI model as magic and expect judgment to compensate for a thin notebook or missing hands. It cannot. Judgment without evidence is guessing, which is why the fix for a struggling agent is usually better memory or better tools, not a fancier model.",
                    "remember": "Feed the judgment; don't worship it.",
                    "kind": "common_mistake",
                },
                {
                    "title": "Say it back, once",
                    "body": "Notebook, hands, judgment: one real-life example of each, from any helper you can imagine. Three sentences, one pass, done.",
                    "try_this": [
                        "Reusing Juno as your example is fully allowed.",
                    ],
                    "kind": "teach_it_back",
                },
            ],
            "checkpoint_questions": [
                {
                    "id": "module4-mtr-cp1",
                    "prompt": "Which part answers 'what should be kept from earlier work'?",
                    "options": [
                        "Memory",
                        "Tools",
                        "Judgment",
                    ],
                    "answer_index": 0,
                },
                {
                    "id": "module4-mtr-cp2",
                    "prompt": "Which part answers 'what can the system actually do'?",
                    "options": [
                        "Memory",
                        "Judgment",
                        "Tools",
                    ],
                    "answer_index": 2,
                },
                {
                    "id": "module4-mtr-cp3",
                    "prompt": "Who grants an agent its tools?",
                    "options": [
                        "The agent grants itself tools as needed",
                        "A human, deliberately, in advance",
                        "The AI model vendor, automatically",
                    ],
                    "answer_index": 1,
                },
            ],
            "skill_templates": [],
            "channel_templates": [],
            "safety_checks": [],
            "permission_matrix": [],
            "evaluation_rubric": [],
            "evaluation_cases": [],
            "artifacts": [
                _artifact(
                    "lesson_artifacts/agents/memory-tools-reasoning-cheatsheet.md",
                    "Cheat sheet: notebook, hands, judgment. What each part is, the question it answers, and Juno's version.",
                    "text",
                    inspect_prompt="Match each part to the question it answers: kept, done, or next.",
                    change_prompt="Add one everyday example under any part. One line is a complete contribution.",
                )
            ],
        },
        {
            "title": "Four Agents You Already Understand",
            "slug": "examples-of-real-ai-agents",
            "lesson_type": "theory",
            "estimated_minutes": 8,
            "content": """# Four Agents You Already Understand

*Lesson 6 of 7 · about 8 minutes · everything you've learned, recognized in the wild.*

You now hold the full toolkit: the six questions, the loop, checks and stop rules, notebook-hands-judgment. This lesson points that toolkit at four real agents. The satisfying part: **you can already read them.**

Each example uses the same four beats: goal, one tool, one check, one stop rule.

## 1. The research helper (Juno, all grown up)
**Goal:** gather sources on a topic and summarize them, with citations.
**Tool:** web search. **Check:** every claim traces back to a source. **Stop:** requested number of sources delivered, or search limit reached.

## 2. The support helper
**Goal:** draft a reply to a customer ticket.
**Tool:** the company knowledge base. **Check:** the draft only promises what policy allows. **Stop:** a draft is ready. A human sends it. Note where the human sits: the agent drafts, the person decides.

## 3. The coding helper
**Goal:** fix a failing test in a codebase.
**Tool:** read and edit files, run tests. **Check:** the test suite, an automatic judge built into the job. **Stop:** tests pass, or attempt limit reached, then report.

## 4. The scheduling helper
**Goal:** find a meeting time for four people.
**Tool:** calendar lookups. **Check:** the proposed slot conflicts with nobody. **Stop:** it *suggests* options and asks for confirmation. Booking is the human's move.

## The pattern worth keeping

All four agents are **narrow**. None of them "helps with everything." Narrow is what makes them checkable, and checkable is what makes them trustworthy. The support helper never sends; the scheduler never books. Each has a small territory with a human at the edge.

When you design your own agent next lesson, you will feel a pull toward making it do everything. These four are your permission slip to keep it small.

## Done means done

You are done when you can:

- pick any one of the four and recite its goal, tool, check, and stop
- say in one sentence why narrow beats broad for a first agent
""",
            "ai_tutor_prompt": _tutor_prompt(
                "Four Agents You Already Understand",
                "reading four real agents (research, support, coding, scheduling) through the goal/tool/check/stop lens, and internalizing that narrow scope is what makes agents checkable and therefore trustworthy.",
            ),
            "questions": [
                {
                    "id": "module4-examples-q1",
                    "prompt": "Which task most clearly needs an agent rather than an answerer?",
                    "options": [
                        "Displaying a stored FAQ answer whenever a matching keyword appears in a question",
                        "Showing the current temperature from a weather feed",
                        "Researching a topic: search, judge sources, draft, verify claims, revise",
                    ],
                    "answer_index": 2,
                },
                {
                    "id": "module4-examples-q2",
                    "prompt": "The coding helper runs tests, reads the failure, adjusts the code, runs tests again. What makes this an agent rather than a script?",
                    "options": [
                        "Test results feed back into what it tries next",
                        "It is written in a programming language",
                        "It runs several test files at once",
                    ],
                    "answer_index": 0,
                },
                {
                    "id": "module4-examples-q3",
                    "prompt": "In the support-helper example, why does a human send the reply instead of the agent?",
                    "options": [
                        "The agent's tools cannot technically send email",
                        "Sending is the risky, outward-facing step, so it sits with a person by design",
                        "Customers dislike automated replies, so a person is kept visible at the end",
                    ],
                    "answer_index": 1,
                },
                {
                    "id": "module4-examples-q4",
                    "prompt": "The scheduling helper books the same room twice for two people. Which parts are the prime suspects?",
                    "options": [
                        "Goal: the request was too ambiguous to act on",
                        "Judgment: the model simply thought incorrectly about which slot was free",
                        "Tools or memory: stale calendar data, or the first booking was never recorded",
                    ],
                    "answer_index": 2,
                },
                {
                    "id": "module4-examples-q5",
                    "prompt": "Why is 'books meeting rooms only' often a better first agent than 'helps with everything'?",
                    "options": [
                        "Narrow scope is easier to check, and checkable is what earns trust",
                        "Broad agents overwhelm their users with too many options and settings",
                        "Narrow agents use less electricity",
                    ],
                    "answer_index": 0,
                },
            ],
            "guided_blocks": [
                {
                    "title": "Read one agent with your own toolkit",
                    "predict_first": {
                        "question": "Before reading the examples: a coding helper's job is 'fix the failing test.' What would its check be? You genuinely have enough to answer this now.",
                        "hint": "What built-in judge does a codebase already have that says pass or fail?",
                    },
                    "body": "The test suite is the check, an automatic judge that comes with the job. Noticing that you could answer this yourself is the real content of this lesson: the toolkit from Lessons 1 to 5 reads real systems, not just Juno.",
                    "analogy": "It is the moment in a language course where you overhear a real conversation and realize you followed it.",
                },
                {
                    "title": "Four beats, four agents",
                    "body": "Goal, tool, check, stop. The same four beats describe all four agents. Read the scenario cards below once, watching the beats repeat. Agents differ in territory, not in anatomy.",
                    "try_this": [
                        "Open the scenario cards and read all four. One pass, no note-taking needed.",
                    ],
                    "checkpoint_after": True,
                },
                {
                    "title": "Where the human stands",
                    "body": "In every example, find the human: sending the support reply, confirming the meeting, reviewing the research. Real agents are designed with a person at the edge of their territory. In Modules 6 and 8, that placement becomes a setting you write down.",
                    "remember": "Every good agent has a human standing at its border.",
                },
                {
                    "title": "The 'everything helper' trap",
                    "body": "Broad agents demo well and work badly: their territory is too large to check, so trust never accumulates. If a product claims to do everything, you now know what to ask it: what's the check, and where's the stop?",
                    "remember": "Useful does not need to mean flashy. Narrow, checkable, trusted, in that order.",
                    "kind": "common_mistake",
                },
                {
                    "title": "Say it back, once",
                    "body": "Pick your favorite of the four agents and give its four beats from memory. One agent, four sentences, done. All four would be rehearsal, and rehearsal is not required.",
                    "try_this": [
                        "One agent only. Choosing the one you'd most want to exist is encouraged.",
                    ],
                    "kind": "teach_it_back",
                },
            ],
            "checkpoint_questions": [
                {
                    "id": "module4-examples-cp1",
                    "prompt": "Which four beats describe every agent in this lesson?",
                    "options": [
                        "Goal, tool, check, stop",
                        "Name, brand, price, launch date",
                        "Search, summarize, send, repeat",
                    ],
                    "answer_index": 0,
                },
                {
                    "id": "module4-examples-cp2",
                    "prompt": "What is the coding helper's built-in check?",
                    "options": [
                        "A human reading every line it writes",
                        "The test suite passing or failing",
                        "A second AI model watching the first",
                    ],
                    "answer_index": 1,
                },
                {
                    "id": "module4-examples-cp3",
                    "prompt": "Why does narrow scope make an agent more trustworthy?",
                    "options": [
                        "Narrow agents are cheaper to advertise",
                        "Narrow agents never make mistakes, so there is nothing to check",
                        "A small territory can actually be checked, so trust can accumulate",
                    ],
                    "answer_index": 2,
                },
            ],
            "skill_templates": [],
            "channel_templates": [],
            "safety_checks": [],
            "permission_matrix": [],
            "evaluation_rubric": [],
            "evaluation_cases": [],
            "artifacts": [
                _artifact(
                    "lesson_artifacts/agents/real-agent-scenarios.md",
                    "Four agent cards (research, support, coding, scheduling), each in the same four beats, plus two unsorted scenarios to classify.",
                    "text",
                    inspect_prompt="Read the four cards and notice the same four beats repeating. Then try the two unsorted scenarios at the bottom.",
                    change_prompt="Write a fifth card for a helper from your own life, using the same four beats. Rough is fine.",
                )
            ],
        },
        {
            "title": "Design Your Own Juno (On Paper)",
            "slug": "design-your-first-agent",
            "lesson_type": "interactive",
            "estimated_minutes": 15,
            "content": """# Design Your Own Juno (On Paper)

*Lesson 7 of 7 · about 15 minutes · the module's finish line. Paper only. Nothing can break.*

Six lessons of ideas become one small act of making: you design an agent of your own, on paper, using a four-box blueprint. Then Module 4 is complete.

Two ground rules that take the pressure off:

1. **There is no wrong blueprint.** This is a sketch, not a submission. In Module 6 you rebuild it with real tools, and it will change then anyway. First drafts are supposed to be replaced.
2. **The finish line is defined below, before you start.** When each box holds one honest sentence, the blueprint is finished. Not polished. Finished. Those are different things, and finished is the one that matters today.

## The four boxes

1. **Goal**: one specific job. "Reminds me when library books are due" beats "helps with my life."
2. **One tool**: the single capability it needs most. Just one.
3. **One memory**: the one thing it must keep track of. For the library helper: the list of due dates.
4. **One check + one stop**: how it knows the work is good, and when it ends.

The worksheet below has a filled-in example (Juno's own blueprint) and an empty copy for yours.

## A hint for choosing your goal

Pick a small irritation from your actual week, something you already wish someone would just handle. The best first agents are almost embarrassingly specific. If your idea can be explained to a friend in one breath, it is the right size.

## Done means done, for the blueprint and the module

Your blueprint is finished when:

- each of the four boxes contains one honest sentence
- you could read it to a friend in under thirty seconds

And with that, Module 4 is finished. Every idea here returns in Modules 5 and 6 attached to real tools, so there is nothing to hold in your head between now and then. The course carries it forward for you.

**Where this goes next, in three sentences:** Module 5 gives you a quick first build called Hermes, to prove the wiring works. Module 6 gives your agent a real home with a tool called OpenClaw. Module 8 is where you put guardrails around it and decide, with evidence, that you trust it.
""",
            "ai_tutor_prompt": _tutor_prompt(
                "Design Your Own Juno (On Paper)",
                "guiding the learner to a finished four-box blueprint: one goal, one tool, one memory, one check plus stop. Enforce smallness kindly. A blueprint is finished when each box holds one honest sentence; when it does, say so and close the module warmly.",
            ),
            "questions": [
                {
                    "id": "module4-activity-q1",
                    "prompt": "A blueprint's goal box says 'AI will handle customer questions.' What is the actual problem with it?",
                    "options": [
                        "It needs a catchier product name",
                        "It never says which customers it serves or which languages it must support",
                        "It is too vague to tell you what tool, memory, or stop rule the agent needs",
                    ],
                    "answer_index": 2,
                },
                {
                    "id": "module4-activity-q2",
                    "prompt": "A blueprint lists eight tools before the goal box is filled in. What has gone wrong?",
                    "options": [
                        "Tools should follow from the goal: a tool list without a goal means the purpose is not clear yet",
                        "Eight is fine, since a thorough blueprint lists every tool that might ever help the agent someday",
                        "The tools simply need to be listed in alphabetical order",
                    ],
                    "answer_index": 0,
                },
                {
                    "id": "module4-activity-q3",
                    "prompt": "A blueprint has a clear goal and a good tool but no check and no stop. What risk is built in?",
                    "options": [
                        "The agent will refuse to start until a check and a stop rule are added",
                        "It can deliver unverified work and never know when it is finished",
                        "The goal will drift as the agent runs",
                    ],
                    "answer_index": 1,
                },
                {
                    "id": "module4-activity-q4",
                    "prompt": "Which is the stronger first blueprint?",
                    "options": [
                        "'An AI that helps with everything in my life': one assistant covering every need beats many small ones",
                        "'An AI that reads the entire internet daily': more information means better answers",
                        "'An AI that tells me which fridge items expire this week, from a list I keep': one job, one tool, natural stop",
                    ],
                    "answer_index": 2,
                },
                {
                    "id": "module4-activity-q5",
                    "prompt": "You read your blueprint to a friend and they cannot say what it does. What is the most likely fix?",
                    "options": [
                        "Add more technical vocabulary so it sounds rigorous",
                        "Find a more attentive friend",
                        "Shrink the goal until it fits in one breath",
                    ],
                    "answer_index": 2,
                },
            ],
            "guided_blocks": [
                {
                    "title": "Before you design: the pressure valve",
                    "predict_first": {
                        "question": "What do you think happens to this blueprint after today: is it graded, kept, or built exactly as written?",
                        "hint": "Think about what Lesson 3 said about first plans.",
                    },
                    "body": "None of those. It is a first plan, and you know what this course thinks of first plans: starting points, not promises. Today's only job is a sketch with four honest sentences.",
                    "analogy": "This is the napkin drawing before the house. Nobody inspects a napkin for building-code violations.",
                },
                {
                    "title": "Fill the four boxes, in order",
                    "body": "Goal first: one specific irritation from your real week. Then the single tool that goal needs most, the single thing worth remembering, and one check plus one stop. Every box after the first is easier because the goal is specific.",
                    "try_this": [
                        "Open the worksheet below. Read Juno's filled-in example once.",
                        "Fill your four boxes, one sentence each. A ten-minute timer helps you stop tinkering.",
                    ],
                    "checkpoint_after": True,
                },
                {
                    "title": "The thirty-second read",
                    "body": "Read your blueprint out loud, once, timed. Under thirty seconds and understandable? It is the right size. Over thirty seconds usually means the goal box is hiding two jobs. Keep the one you'd want first; the other can be its own agent someday.",
                    "remember": "One breath, one job, one agent.",
                },
                {
                    "title": "The polish trap",
                    "body": "The riskiest moment of this lesson is after the boxes are full, when the urge arrives to reword everything until it is perfect. The finish line was defined before you started: four honest sentences, thirty-second read. Past it, the blueprint is finished. Revising a finished sketch is Module 6's job, not tonight's.",
                    "remember": "Finished was defined in advance. You are allowed to believe it.",
                    "kind": "common_mistake",
                },
                {
                    "title": "Close the module",
                    "body": "Read your four sentences to someone: a friend, a rubber duck, the room. That is the module's teach-it-back and the last thing Module 4 asks of you. Everything here returns in later modules, carried forward by the course, not by your memory.",
                    "try_this": [
                        "One read-aloud. Then close the page. Genuinely done.",
                    ],
                    "kind": "teach_it_back",
                },
            ],
            "checkpoint_questions": [
                {
                    "id": "module4-activity-cp1",
                    "prompt": "What are the four boxes of the blueprint?",
                    "options": [
                        "Goal, one tool, one memory, one check + stop",
                        "Name, logo, price, launch plan",
                        "Model, dataset, server, budget",
                    ],
                    "answer_index": 0,
                },
                {
                    "id": "module4-activity-cp2",
                    "prompt": "When is the blueprint finished?",
                    "options": [
                        "When it has been rewritten until no better wording exists",
                        "When each box holds one honest sentence and it reads in thirty seconds",
                        "When it lists every tool the agent could ever need",
                    ],
                    "answer_index": 1,
                },
                {
                    "id": "module4-activity-cp3",
                    "prompt": "What happens to the blueprint in Module 6?",
                    "options": [
                        "It is graded against other students' blueprints",
                        "It must be memorized before starting",
                        "It gets rebuilt with real tools. Changing then is expected",
                    ],
                    "answer_index": 2,
                },
            ],
            "skill_templates": [],
            "channel_templates": [],
            "safety_checks": [],
            "permission_matrix": [],
            "evaluation_rubric": [],
            "evaluation_cases": [],
            "artifacts": [
                _artifact(
                    "lesson_artifacts/agents/first-agent-blueprint.md",
                    "The four-box blueprint worksheet: Juno's filled-in example, an empty copy, and the finish-line definition.",
                    "text",
                    inspect_prompt="Read Juno's example blueprint and notice that every box is one plain sentence. That is the target amount of polish.",
                    change_prompt="Fill in the empty blueprint with your own four sentences. When all four boxes are full, you are done.",
                )
            ],
        },
    ],
}
