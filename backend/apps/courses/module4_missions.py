MODULE_4_MISSION_PACK = {
    "title": "Module 4: AI Agents",
    "slug": "module-4-ai-agents",
    "description": "Explain what AI agents are, how they differ from chatbots, how basic agent loops work, and how those ideas lead into the later Hermes, OpenClaw, and capstone modules.",
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
            "title": "What an AI Agent Is",
            "slug": "what-an-ai-agent-is",
            "lesson_type": "theory",
            "estimated_minutes": 10,
            "content": """# What an AI Agent Is

An AI agent is not just a chatbot with a different label. A good beginner definition is: **an agent is a system that can receive a goal, decide what to do next, use tools or memory when needed, and stop when it has a result or hits a limit**.

The simplest way to understand the difference is this:

- a basic chatbot mostly answers within one conversation turn
- a workflow follows a fixed sequence of steps
- an agent can choose its next step based on what it learns while working

That flexibility is why agents are exciting, but it is also why they need clear tools, good boundaries, and human review.

## Beginner mental model
- **Goal**: what the human wants
- **Plan**: what the system thinks it should try
- **Tools**: how it acts on the world
- **Memory**: what it should keep track of
- **Check**: how it knows whether progress is real
- **Stop rule**: when it should stop instead of wandering forever

## Why this module matters
If students do not understand this map, later modules can feel like random setup commands. Module 4 turns future build steps into something coherent.
""",
            "ai_tutor_prompt": """You are ACADEMIC TUTOR AI HEADMASTER guiding a zero-knowledge student through What an AI Agent Is.

Operate in attempt-first mode.
- Start by asking what the learner already thinks an AI agent is.
- Use the lesson content as the primary source of truth.
- Keep the explanation centered on goal, plan, tools, memory, checks, and stop rules.
- Redirect vague hype into one clear practical example.

If the learner asks for a shortcut, redirect them to the smallest explanation or example that makes the idea concrete.
""",
            "questions": [
                {
                    "id": "module4-agent-q1",
                    "prompt": "A student says: 'My app auto-responds to every support email using a fixed template. It is an AI agent.' What is the key thing missing from this description?",
                    "options": [
                        "The system cannot choose different steps based on what it finds — it runs the same template every time, making it an auto-responder, not an agent",
                        "It does not use Python, so it cannot be an agent",
                        "Handling emails automatically is enough to qualify as an agent",
                    ],
                    "answer_index": 0,
                },
                {
                    "id": "module4-agent-q2",
                    "prompt": "Your flight-search system finds a great deal at $280 but keeps running for 20 more minutes. What design problem does this reveal?",
                    "options": [
                        "There is no stop rule — once the goal is met the agent should stop, not keep searching indefinitely",
                        "The agent needs a larger AI model to know when to stop",
                        "The search ran too fast and needs to slow down",
                    ],
                    "answer_index": 0,
                },
                {
                    "id": "module4-agent-q3",
                    "prompt": "An agent summarizes 3 articles, then checks whether each summary is accurate before delivering the results. Which part of the agent model explains that final check?",
                    "options": [
                        "The Check step — the agent verifies its own output before reporting instead of assuming the first result is good enough",
                        "The Memory step — it remembered the 3 articles so it could recheck them",
                        "The Stop rule — it stopped at exactly 3 articles",
                    ],
                    "answer_index": 0,
                },
                {
                    "id": "module4-agent-q4",
                    "prompt": "A classmate says: 'Just use the biggest AI model and everything will work.' What key idea about agents are they overlooking?",
                    "options": [
                        "Clear goals, bounded tools, observation steps, and stop rules shape outcomes more than raw model size alone",
                        "Bigger models are always cheaper to run",
                        "Tools are unnecessary when the model is large enough",
                    ],
                    "answer_index": 0,
                },
                {
                    "id": "module4-agent-q5",
                    "prompt": "An agent successfully books a restaurant that meets all the given criteria. What should it do next?",
                    "options": [
                        "Stop — the goal is complete; continuing wastes resources and risks making unwanted additional bookings",
                        "Keep searching for an even better restaurant in case a perfect option exists",
                        "Clear its memory and restart the goal from scratch",
                    ],
                    "answer_index": 0,
                },
            ],
            "guided_blocks": [
                {
                    "title": "The one-sentence definition",
                    "predict_first": {
                        "question": "Before reading: think of a task you do repeatedly that sometimes requires changing course when the first attempt fails. Would a fixed script handle it, or does it need something more flexible? Why?",
                        "hint": "Consider what happens when the initial plan does not work — does the system need to observe and decide again?",
                    },
                    "body": "An AI agent is a system that works toward a goal, uses available tools or memory when needed, checks what happened, and decides what to do next.",
                    "analogy": "Think of an agent like a careful intern: it gets an assignment, looks at the evidence, uses the approved tools, and reports back instead of guessing blindly.",
                    "try_this": [
                        "Say the one-sentence definition out loud in your own words.",
                        "Point to the part of the definition that sounds most important to you: goal, tools, memory, checking, or stopping.",
                    ],
                },
                {
                    "title": "Why the word agent matters",
                    "body": "The word matters because it implies action and feedback. The system is not only talking. It is choosing what to do next based on what it learns while working.",
                    "remember": "If the system cannot do or check anything, it is probably closer to a chatbot than an agent.",
                },
                {
                    "title": "Your first mental map",
                    "body": "Keep six pieces in your head: goal, plan, tools, memory, check, stop rule. Later modules will keep returning to those same six pieces in more concrete form.",
                    "try_this": [
                        "Open the agent map below and match each label to one role in the system.",
                        "Explain which label seems easiest to forget and why.",
                    ],
                    "checkpoint_after": True,
                },
                {
                    "title": "Common mistake",
                    "body": "Beginners often think an agent is just a smarter chatbot. The real difference is not just smarter words. The difference is that an agent can act, check, and adapt.",
                    "remember": "Talking alone does not make a system agentic.",
                    "kind": "common_mistake",
                },
                {
                    "title": "Teach it back",
                    "body": "Teach the definition back to a classmate using the words goal, tools, memory, and check. If you can do that without looking, the lesson has started to stick.",
                    "try_this": ["Explain the agent map without looking at the text for 20 seconds."],
                    "kind": "teach_it_back",
                },
            ],
            "checkpoint_questions": [
                {
                    "id": "module4-agent-cp1",
                    "prompt": "Which phrase best fits an agent?",
                    "options": ["Goal plus tools plus checking", "Decorative text plus logo", "Quiz score only"],
                    "answer_index": 0,
                },
                {
                    "id": "module4-agent-cp2",
                    "prompt": "What makes the system adapt while working?",
                    "options": [
                        "It uses feedback from the environment to decide the next step",
                        "It always follows one script with no variation",
                        "It changes the background color",
                    ],
                    "answer_index": 0,
                },
                {
                    "id": "module4-agent-cp3",
                    "prompt": "Which item belongs in the first mental map?",
                    "options": ["Stop rule", "Animation speed", "Profile badge"],
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
                {
                    "path": "lesson_artifacts/agents/agent-map.md",
                    "summary": "One-screen mental model for what an AI agent is.",
                    "format": "text",
                    "inspect_prompt": "Find the six parts of the map and explain what each one does in plain English.",
                    "change_prompt": "Rewrite one label so it would make more sense to a student who has never used AI tools before.",
                    "body": """# Agent Mental Model

- Goal: what the human wants done
- Plan: the next step the system thinks it should try
- Tools: how it acts on the world
- Memory: what it remembers during the task
- Check: how it looks at results instead of guessing
- Stop rule: when it should stop, ask for help, or hand work back to a human
""",
                }
            ],
        },
        {
            "title": "Agents vs Chatbots",
            "slug": "agents-vs-chatbots",
            "lesson_type": "theory",
            "estimated_minutes": 8,
            "content": """# Agents vs Chatbots

Students often hear these words used as if they mean the same thing. They do not.

## A useful beginner comparison
- **Chatbot**: mostly answers questions in conversation
- **Workflow**: follows a planned sequence of steps
- **Agent**: can choose the next step based on what is happening

This does not mean every agent is better. Simpler systems are often cheaper, safer, and easier to debug. A strong lesson should teach students when not to add agent complexity.

That is why this module teaches three categories instead of only one buzzword.
""",
            "ai_tutor_prompt": """You are ACADEMIC TUTOR AI HEADMASTER guiding a zero-knowledge student through Agents vs Chatbots.

Operate in attempt-first mode.
- Ask which systems the learner has already used: chatbot, workflow, or something more agentic.
- Keep the answer centered on the difference between fixed response, fixed path, and adaptive next-step choice.
- Push the learner to explain when simple is better.
""",
            "questions": [
                {"id": "module4-compare-q1", "prompt": "Your university wants to auto-answer 20 common student questions from a fixed FAQ. Which system is most appropriate and why?", "options": ["A chatbot — the responses are predetermined and no adaptive decision-making is needed", "An agent — anything AI should use an agent", "A full ML pipeline — FAQ requires machine learning"], "answer_index": 0},
                {"id": "module4-compare-q2", "prompt": "A grading system works like this: 90+ → A, 80+ → B, 70+ → C, else → F. Is this an agent, workflow, or chatbot?", "options": ["A workflow — all decisions are defined in advance with no learning from results", "An agent — it makes decisions based on numbers", "A chatbot — it produces a single text output"], "answer_index": 0},
                {"id": "module4-compare-q3", "prompt": "Your team argues: 'We should use an agent for everything because agents are smarter.' What is the honest response?", "options": ["Agents add cost and complexity — use the simplest system that solves the problem reliably", "Agree — agents always outperform simpler alternatives", "Agents cannot handle real tasks in production"], "answer_index": 0},
                {"id": "module4-compare-q4", "prompt": "Which task clearly REQUIRES an agent rather than a simpler system?", "options": ["Diagnosing a server outage: checking logs, trying fixes, verifying results, and escalating if still broken", "Sending a weekly summary email to all subscribers on Monday at 9am", "Showing the current weather temperature on a screen"], "answer_index": 0},
                {"id": "module4-compare-q5", "prompt": "You spend a week building an agent that sends one fixed message to users when they sign up. A colleague says you overbuilt it. Are they right?", "options": ["Yes — a simple trigger and template handles this; an agent added complexity with no benefit", "No — agents are always worth the investment for user-facing interactions", "It depends on how many users sign up per day"], "answer_index": 0},
            ],
            "guided_blocks": [
                {"title": "Three categories, not one", "body": "This course separates chatbots, workflows, and agents because students need to know what kind of system they are actually looking at before they can build it or judge it.", "analogy": "Think of a chatbot as a receptionist, a workflow as a checklist, and an agent as a teammate who can choose which checklist to follow next."},
                {"title": "When simple is better", "body": "A strong engineering habit is to start with the simplest thing that can work. If a single response or a fixed workflow solves the task, adding an agent can create more confusion than value.", "remember": "More autonomy is not automatically more intelligent design."},
                {"title": "Decision practice", "body": "Ask one question for each scenario: does the system need to decide what to do next, or can you write the steps ahead of time? That question often tells you whether you need an agent at all.", "try_this": ["Open the comparison table below and find one task that fits a chatbot, one that fits a workflow, and one that fits an agent."], "checkpoint_after": True},
                {"title": "Common mistake", "body": "A common beginner mistake is calling every AI product an agent. That word loses meaning if it includes simple Q&A tools, fixed scripts, and real decision-making loops all at once.", "remember": "Use the smallest accurate label.", "kind": "common_mistake"},
                {"title": "Teach it back", "body": "Teach the three-category comparison back to someone else using one sentence per category.", "try_this": ["Use the words receptionist, checklist, and teammate in your explanation if that analogy helps you."], "kind": "teach_it_back"},
            ],
            "checkpoint_questions": [
                {"id": "module4-compare-cp1", "prompt": "Which category is closest to a fixed step-by-step path?", "options": ["Workflow", "Agent", "Random output"], "answer_index": 0},
                {"id": "module4-compare-cp2", "prompt": "What is the main reason to avoid unnecessary agent complexity?", "options": ["Simpler systems are often easier to trust, test, and debug", "Agents cannot ever be useful", "Workflows never use tools"], "answer_index": 0},
                {"id": "module4-compare-cp3", "prompt": "Which category best matches a system that chooses its next step from feedback?", "options": ["Agent", "Chatbot", "Static document"], "answer_index": 0},
            ],
            "skill_templates": [], "channel_templates": [], "safety_checks": [], "permission_matrix": [], "evaluation_rubric": [], "evaluation_cases": [],
            "artifacts": [
                {
                    "path": "lesson_artifacts/agents/chatbot-workflow-agent-table.md",
                    "summary": "Comparison table for chatbot, workflow, and agent thinking.",
                    "format": "text",
                    "inspect_prompt": "Find the row that explains how each system handles the next step.",
                    "change_prompt": "Add one beginner example of your own to the table.",
                    "body": """# Chatbot vs Workflow vs Agent

| Category | Best for | Limitation |
| --- | --- | --- |
| Chatbot | Question and answer, simple guidance, conversation | Usually weak at multi-step action and verification |
| Workflow | Well-defined, repeatable tasks with fixed steps | Less flexible when the task changes midstream |
| Agent | Open-ended tasks that need tools, checking, and adaptation | Higher cost, more room for error, needs stronger guardrails |
""",
                }
            ],
        },
        {
            "title": "Basic Agent Workflow",
            "slug": "basic-agent-workflow",
            "lesson_type": "theory",
            "estimated_minutes": 10,
            "content": """# Basic Agent Workflow

Beginner-friendly agent loops are easier to understand when they are drawn as simple steps:

1. Understand the goal.
2. Plan a next action.
3. Use a tool or a reasoning step.
4. Observe what happened.
5. Decide whether to continue, revise, or stop.

This is why agents are often described as loops instead of one-shot replies. The system keeps checking the world instead of pretending it already knows everything.
""",
            "ai_tutor_prompt": """You are ACADEMIC TUTOR AI HEADMASTER guiding a zero-knowledge student through Basic Agent Workflow.

Operate in attempt-first mode.
- Keep the workflow small and concrete.
- Push the learner to name where observation and stop rules happen.
- Convert vague answers into clear step sequences.
""",
            "questions": [
                {"id": "module4-workflow-q1", "prompt": "An agent finds a useful article in step 3 but immediately delivers it without reading the content. Which step did it skip?", "options": ["Observe — it should have checked the quality of what it found before delivering", "Plan — it should have planned more intermediate steps", "Goal — the goal was too vague"], "answer_index": 0},
                {"id": "module4-workflow-q2", "prompt": "Your agent finds a hotel for $89, within the $100 budget goal. Should it stop or keep searching?", "options": ["Stop — the goal is met; continuing wastes time and risks making unwanted changes", "Keep searching — there might be something cheaper", "Ask the user to revise the budget goal"], "answer_index": 0},
                {"id": "module4-workflow-q3", "prompt": "An agent has sent 200 job applications in 30 minutes and nothing has stopped it. What design element is missing?", "options": ["A stop rule or limit — without one the agent can run indefinitely and take unintended actions", "More memory to track all applications", "A larger AI model to know when enough is enough"], "answer_index": 0},
                {"id": "module4-workflow-q4", "prompt": "You are the 'observe' step. The tool you just called returned an error. What should happen next in the loop?", "options": ["Pass the error to the decide step so the agent can revise the plan or escalate", "Immediately stop and delete all progress made so far", "Ignore the error and continue with the original plan unchanged"], "answer_index": 0},
                {"id": "module4-workflow-q5", "prompt": "Which loop step gives the agent the ability to learn from a mistake in the previous attempt?", "options": ["Observe then Decide — seeing the failed result lets the agent revise the plan for the next try", "Goal — a clear goal prevents mistakes entirely", "Memory — it stores the mistake and tries the exact same approach again"], "answer_index": 0},
            ],
            "guided_blocks": [
                {"title": "The loop in plain English", "body": "A basic agent loop is simple: understand the task, choose the next step, act, look at the result, then decide whether to continue.", "analogy": "It works like a student doing a lab: read the instructions, try something, look at the result, then decide what to do next."},
                {"title": "Why feedback matters", "body": "Agents are useful when the result of one step changes what the next step should be. That is the heart of the loop.", "remember": "If nothing in the environment can change the next step, you may only need a workflow."},
                {"title": "Checkpoint thinking", "body": "Every good loop needs checkpoints. Without them, the system can waste time, repeat mistakes, or act with too much confidence.", "try_this": ["Open the workflow card below and identify the best place for a human checkpoint."], "checkpoint_after": True},
                {"title": "Common mistake", "body": "Students often imagine an agent planning perfectly before it begins. Real agents usually need to revise their plan after they see tool results or blockers.", "remember": "The first plan is a start, not a prophecy.", "kind": "common_mistake"},
                {"title": "Teach it back", "body": "Explain the loop back to someone else in five verbs: understand, plan, act, observe, decide.", "try_this": ["Use those five verbs in order without reading them back."], "kind": "teach_it_back"},
            ],
            "checkpoint_questions": [
                {"id": "module4-workflow-cp1", "prompt": "What happens after the agent acts?", "options": ["It observes the result", "It forgets the goal", "It publishes automatically"], "answer_index": 0},
                {"id": "module4-workflow-cp2", "prompt": "Why are checkpoints useful?", "options": ["They help control mistakes and decide whether to continue", "They remove the need for evidence", "They replace all tools"], "answer_index": 0},
                {"id": "module4-workflow-cp3", "prompt": "What makes the workflow a loop?", "options": ["The system can repeat steps based on results", "The title uses the word loop", "It always runs forever"], "answer_index": 0},
            ],
            "skill_templates": [], "channel_templates": [], "safety_checks": [], "permission_matrix": [], "evaluation_rubric": [], "evaluation_cases": [],
            "artifacts": [
                {
                    "path": "lesson_artifacts/agents/basic-agent-loop.md",
                    "summary": "Workflow card for a simple agent loop with a human checkpoint.",
                    "format": "text",
                    "inspect_prompt": "Find where the loop can stop and where a human should review progress.",
                    "change_prompt": "Move the human checkpoint earlier or later and explain what risk changes.",
                    "body": """# Basic Agent Loop

1. Understand the goal
2. Plan the next step
3. Use a tool or reasoning step
4. Observe what happened
5. Decide: continue, revise, ask a human, or stop
""",
                }
            ],
        },
        {
            "title": "Memory, Tools, and Reasoning",
            "slug": "memory-tools-reasoning",
            "lesson_type": "theory",
            "estimated_minutes": 12,
            "content": """# Memory, Tools, and Reasoning

Students do not need deep technical detail yet. They do need a clean high-level picture.

- **Memory** is what the system keeps from earlier work.
- **Tools** are the actions it is allowed to take.
- **Reasoning** is how it decides what to do next.

These three ideas show up again in every build module. OpenClaw, for example, turns them into very concrete surfaces: sessions, workspace files, tools, channels, and safety controls.
""",
            "ai_tutor_prompt": """You are ACADEMIC TUTOR AI HEADMASTER guiding a zero-knowledge student through Memory, Tools, and Reasoning.

Operate in attempt-first mode.
- Keep the explanation high-level and concrete.
- Use notebook, hands, and decision as anchors when helpful.
- Push the learner to separate memory, action, and next-step choice.
""",
            "questions": [
                {"id": "module4-mtr-q1", "prompt": "A support agent gives very different answers to the same question two days apart. Which building block is most likely weak?", "options": ["Memory — the agent is not retaining or using context from earlier interactions", "Tools — it needs different search capabilities", "Reasoning — the AI model changed between the two days"], "answer_index": 0},
                {"id": "module4-mtr-q2", "prompt": "Your agent can search the web but cannot save any files. It can clearly decide what to do next. Which building block is restricted by policy?", "options": ["Tools — the agent's allowed actions are limited; it cannot write, only read", "Memory — it cannot retain anything without file access", "Reasoning — planning is impossible without file access"], "answer_index": 0},
                {"id": "module4-mtr-q3", "prompt": "An agent has all the right information and working tools, but keeps choosing the wrong next action. Which building block needs improvement?", "options": ["Reasoning — the decision logic is not using the available information correctly", "Memory — it needs to remember more details", "Tools — it needs additional capabilities to decide correctly"], "answer_index": 0},
                {"id": "module4-mtr-q4", "prompt": "An agent asks the same question it already asked two steps ago because it forgot your earlier answer. Which building block is clearly failing?", "options": ["Memory — the agent is not storing or retrieving earlier context within this task", "Tools — the wrong tool was called", "Reasoning — the model is too small to retain context"], "answer_index": 0},
                {"id": "module4-mtr-q5", "prompt": "The agent knows exactly what it should do but physically cannot do it — it lacks the capability. Which building block is the bottleneck?", "options": ["Tools — improving access to actions is the bottleneck when the agent knows the plan but cannot execute it", "Memory — more storage will fix the capability gap", "Reasoning — better thinking will unlock the missing capability"], "answer_index": 0},
            ],
            "guided_blocks": [
                {"title": "Three building blocks", "body": "Memory, tools, and reasoning are the three easiest words to remember when you first learn agents. They are not the whole system, but they are enough to begin.", "analogy": "Memory is the notebook, tools are the hands, and reasoning is the decision about what to do next."},
                {"title": "Where these ideas show up later", "body": "Later build modules will make these ideas concrete. OpenClaw sessions and workspaces relate to memory. Skills and tool access relate to tools. Safety checks and review points shape how reasoning is allowed to turn into action.", "remember": "Abstract now, concrete later."},
                {"title": "Concept matching", "body": "A quick way to learn this is to match each idea to a simple question: memory answers what should be kept, tools answer what can be done, reasoning answers what should happen next.", "try_this": ["Open the cheat sheet below and match each question to memory, tools, or reasoning."], "checkpoint_after": True},
                {"title": "Common mistake", "body": "A common mistake is treating reasoning like magic. Reasoning helps decide next steps, but it still depends on good tools, useful memory, and real feedback from the environment.", "remember": "Reasoning without evidence is guessing.", "kind": "common_mistake"},
                {"title": "Teach it back", "body": "Teach the three building blocks back using notebook, hands, and decision as your anchors.", "try_this": ["Explain one real example of each block from an AI helper you can imagine."], "kind": "teach_it_back"},
            ],
            "checkpoint_questions": [
                {"id": "module4-mtr-cp1", "prompt": "Which building block answers 'what should be kept from earlier work'?", "options": ["Memory", "Theme", "Pairing code"], "answer_index": 0},
                {"id": "module4-mtr-cp2", "prompt": "Which building block answers 'what can the system do'?", "options": ["Tools", "Branding", "Badges"], "answer_index": 0},
                {"id": "module4-mtr-cp3", "prompt": "Which building block answers 'what should happen next'?", "options": ["Reasoning", "Logo placement", "Window size"], "answer_index": 0},
            ],
            "skill_templates": [], "channel_templates": [], "safety_checks": [], "permission_matrix": [], "evaluation_rubric": [], "evaluation_cases": [],
            "artifacts": [
                {
                    "path": "lesson_artifacts/agents/memory-tools-reasoning-cheatsheet.md",
                    "summary": "Cheat sheet for the three high-level parts of an agent.",
                    "format": "text",
                    "inspect_prompt": "Look for the question each building block answers.",
                    "change_prompt": "Add one beginner example under each section.",
                    "body": """# Memory, Tools, and Reasoning

## Memory
- Keeps useful information from earlier work
- Prevents the system from starting from zero every time

## Tools
- Let the system act on the world
- Can read, write, search, execute, or message depending on policy

## Reasoning
- Chooses the next step
- Uses feedback from tools and context to revise the plan
""",
                }
            ],
        },
        {
            "title": "Examples of Real AI Agents",
            "slug": "examples-of-real-ai-agents",
            "lesson_type": "theory",
            "estimated_minutes": 10,
            "content": """# Examples of Real AI Agents

Agents become easier to understand when students can attach the ideas to concrete jobs.

Useful examples include:
- a research helper that searches, summarizes, and cites
- a customer-support helper that reads a ticket, checks a knowledge base, and drafts a safe reply
- a coding helper that reads files, proposes edits, runs tests, and checks results
- a scheduling helper that compares calendars and suggests options

The pattern is the same each time: conversation plus action plus checking.
""",
            "ai_tutor_prompt": """You are ACADEMIC TUTOR AI HEADMASTER guiding a zero-knowledge student through Examples of Real AI Agents.

Operate in attempt-first mode.
- Keep examples concrete and role-based.
- Push the learner to name one action and one check for each example.
- Avoid abstract hype if a practical job story will work better.
""",
            "questions": [
                {"id": "module4-examples-q1", "prompt": "Which task most clearly needs an agent rather than a simpler chatbot?", "options": ["Writing a research summary: search sources, compare claims, draft, check for unsupported statements, and revise", "Displaying a stored FAQ answer when a keyword matches", "Showing the current temperature from a weather API"], "answer_index": 0},
                {"id": "module4-examples-q2", "prompt": "A coding agent runs a test, sees a failure, reads the error, adjusts the code, and runs the test again. What makes this behave like an agent rather than a script?", "options": ["It uses test results as feedback to decide the next action — that adaptive loop distinguishes it from a fixed script", "It uses Python instead of another language", "It runs multiple test cases simultaneously"], "answer_index": 0},
                {"id": "module4-examples-q3", "prompt": "A support agent reads a billing error ticket and needs to check the billing system before drafting a reply. Which building block lets it access that system?", "options": ["Tools — the agent has permission to query the billing system as one of its allowed actions", "Memory — it remembers past billing history without needing to look it up", "Reasoning — it figures out the answer from the ticket text alone"], "answer_index": 0},
                {"id": "module4-examples-q4", "prompt": "A scheduling agent books the same meeting slot twice for two different people. Which building block failed?", "options": ["Tools or Memory — either the calendar tool returned stale data, or the agent did not store the first booking before proceeding", "Reasoning — the agent thought about it incorrectly", "Goal — the goal description was too ambiguous"], "answer_index": 0},
                {"id": "module4-examples-q5", "prompt": "Why is a narrow agent ('book meeting rooms only') often more valuable than a broad agent ('help with everything')?", "options": ["A narrow scope makes the agent easier to test, safer to trust, and less likely to take unintended actions", "Broader agents are always less intelligent than narrow ones", "Narrow agents consume less electricity and are cheaper to run"], "answer_index": 0},
            ],
            "guided_blocks": [
                {"title": "Examples make the abstract concrete", "body": "Students remember agents better when they can attach the idea to jobs they understand. That is why this lesson uses concrete roles instead of abstract architecture alone.", "analogy": "It is easier to understand a toolbelt when you see the jobs each tool is for."},
                {"title": "The repeated pattern", "body": "Across the examples, the repeated pattern is simple: the agent gets a task, uses allowed tools, checks what happened, and either keeps going or asks for help.", "remember": "Conversation plus action plus checking is the pattern to watch for."},
                {"title": "Scenario sorting", "body": "One fast way to learn is to sort example tasks by what they need most: research, coding, support, or coordination.", "try_this": ["Open the scenario deck below and sort each scenario into the best-fit agent role."], "checkpoint_after": True},
                {"title": "Common mistake", "body": "A common mistake is thinking a real agent must be huge or futuristic. Many useful agents are narrow and boring on purpose. Narrow scope is often what makes them safe enough to trust.", "remember": "Useful does not need to mean flashy.", "kind": "common_mistake"},
                {"title": "Teach it back", "body": "Teach this lesson back by giving one sentence for a research agent, one for a support agent, and one for a coding agent.", "try_this": ["For each one, name the task, one tool, and one check."], "kind": "teach_it_back"},
            ],
            "checkpoint_questions": [
                {"id": "module4-examples-cp1", "prompt": "Which pattern repeats across real agent examples?", "options": ["Conversation, action, and checking", "Only logos and menus", "No tools or feedback"], "answer_index": 0},
                {"id": "module4-examples-cp2", "prompt": "Why can a coding helper be a strong agent example?", "options": ["It can use test results to check progress", "It never needs evidence", "It cannot act on files"], "answer_index": 0},
                {"id": "module4-examples-cp3", "prompt": "What makes a narrow agent valuable?", "options": ["Clear scope often makes it more useful and safer", "It always replaces human review", "It must be public to be useful"], "answer_index": 0},
            ],
            "skill_templates": [], "channel_templates": [], "safety_checks": [], "permission_matrix": [], "evaluation_rubric": [], "evaluation_cases": [],
            "artifacts": [
                {
                    "path": "lesson_artifacts/agents/real-agent-scenarios.md",
                    "summary": "Scenario deck for sorting real tasks into agent-friendly roles.",
                    "format": "text",
                    "inspect_prompt": "Read each scenario and decide what the agent is doing beyond just answering text.",
                    "change_prompt": "Add one local example of your own from school, work, or daily life.",
                    "body": """# Real Agent Scenarios

1. Research helper: search sources, summarize, cite, flag unknowns.
2. Coding helper: inspect files, propose edits, run checks, revise from test output.
3. Support helper: read a ticket, consult a knowledge base, draft a safe response.
4. Scheduling helper: compare calendars, suggest options, request confirmation.
""",
                }
            ],
        },
        {
            "title": "Introduction to Our Agents",
            "slug": "introduction-to-our-agents",
            "lesson_type": "theory",
            "estimated_minutes": 10,
            "content": """# Introduction to Our Agents

This course does not stop at theory. Students eventually meet several build tracks.

- **Hermes** introduces a simpler first build where students see how an agent can be connected and tested.
- **OpenClaw** introduces a personal-assistant platform with a gateway, sessions, skills, channels, and safety controls.
- **Claude-based workflows** show how model-specific environments can structure coding or reasoning tasks.
- **Gemini-style workflows** help students compare different model ecosystems and tool habits.

The point of this lesson is not to memorize brand names. It is to recognize that different agent tracks emphasize different strengths and boundaries.
""",
            "ai_tutor_prompt": """You are ACADEMIC TUTOR AI HEADMASTER guiding a zero-knowledge student through Introduction to Our Agents.

Operate in attempt-first mode.
- Keep the focus on differences in role, workflow, and boundary.
- Do not let the learner collapse everything into brand names alone.
- Use later modules as motivation, not as assumed background knowledge.
""",
            "questions": [
                {"id": "module4-tracks-q1", "prompt": "You want an assistant that responds to Telegram messages and keeps conversation history between sessions. Which course track has those capabilities built in?", "options": ["OpenClaw — it has a gateway, sessions, Telegram channel support, and persistent context built in", "A static FAQ page with a contact form", "A simple email auto-responder"], "answer_index": 0},
                {"id": "module4-tracks-q2", "prompt": "Hermes is introduced before OpenClaw in the course path. Why is this ordering useful for beginners?", "options": ["Hermes offers a simpler first build so students understand basics before OpenClaw adds gateway, sessions, skills, and channels", "Hermes is always a better system than OpenClaw for production use", "OpenClaw requires Hermes to be installed and configured first"], "answer_index": 0},
                {"id": "module4-tracks-q3", "prompt": "A student used a simple AI to write code but it kept choosing the wrong tools. They ask: 'Would switching to OpenClaw fix that automatically?' What is the honest answer?", "options": ["Not automatically — the fix is configuring the right tool policy and skill set, which OpenClaw supports but does not do by itself", "Yes — OpenClaw always resolves tool selection problems", "No — OpenClaw does not support coding workflows at all"], "answer_index": 0},
                {"id": "module4-tracks-q4", "prompt": "You need to compare how two different AI models perform on the same task. Which course track is designed for that kind of cross-model exploration?", "options": ["Gemini-style workflows — designed to help students compare different model ecosystems and tool habits", "OpenClaw — it runs both models simultaneously and compares them for you", "Hermes — it always runs two models in parallel by default"], "answer_index": 0},
                {"id": "module4-tracks-q5", "prompt": "Your agent works correctly but nobody on your team can explain what it does or debug it when something goes wrong. Which aspect of agent design is underdeveloped?", "options": ["Visibility and system design — clarity, auditability, and clear boundaries matter as much as functionality", "Memory — storing more logs will solve the confusion", "Tools — adding more tools will make the system easier to explain"], "answer_index": 0},
            ],
            "guided_blocks": [
                {"title": "Different tracks, different strengths", "body": "This course uses several build tracks because students need to see that agent systems can be shaped around different goals and ecosystems.", "analogy": "Think of them like different vehicles: a bicycle, a van, and a train all move people, but they are built for different jobs."},
                {"title": "What to compare", "body": "When comparing tracks, focus on the workflow, the tools, the safety model, and the kind of task each one is best at solving.", "remember": "Compare responsibilities, not brand hype."},
                {"title": "Track preview activity", "body": "Use the comparison card to predict which track best fits a lightweight first build, a personal assistant, or a structured reasoning workflow.", "try_this": ["Open the comparison card below and match each track to its strongest beginner use case."], "checkpoint_after": True},
                {"title": "Common mistake", "body": "A common mistake is assuming a stronger or more famous model automatically creates a better agent system. The broader system design still matters: sessions, tools, channels, safety, and review all shape the result.", "remember": "A model is part of the system, not the whole system.", "kind": "common_mistake"},
                {"title": "Teach it back", "body": "Teach the track comparison back by giving one sentence each for Hermes, OpenClaw, and the later capstone path.", "try_this": ["Use the words build, boundary, and workflow in your explanation."], "kind": "teach_it_back"},
            ],
            "checkpoint_questions": [
                {"id": "module4-tracks-cp1", "prompt": "Which track emphasizes gateway, sessions, skills, and channels?", "options": ["OpenClaw", "Theme settings", "Static glossary"], "answer_index": 0},
                {"id": "module4-tracks-cp2", "prompt": "What should students compare across tracks?", "options": ["Workflow, tools, safety model, and best-fit task", "Only logos", "Only lesson length"], "answer_index": 0},
                {"id": "module4-tracks-cp3", "prompt": "Why is model fame alone not enough for a comparison?", "options": ["Because the surrounding system design still controls real behavior", "Because models do not matter at all", "Because channels are irrelevant"], "answer_index": 0},
            ],
            "skill_templates": [], "channel_templates": [], "safety_checks": [], "permission_matrix": [], "evaluation_rubric": [], "evaluation_cases": [],
            "artifacts": [
                {
                    "path": "lesson_artifacts/agents/agent-track-comparison.md",
                    "summary": "Course track comparison card for Hermes, OpenClaw, and later build paths.",
                    "format": "text",
                    "inspect_prompt": "Find what each track helps students learn first.",
                    "change_prompt": "Rewrite one row in simpler words for a complete beginner.",
                    "body": """# Agent Track Comparison

| Track | What students learn first | Why it matters |
| --- | --- | --- |
| Hermes | A simpler first build and connection story | Lowers fear and gives a quick first success |
| OpenClaw | Gateway, sessions, skills, channels, safety | Shows a richer real-world assistant platform |
| Claude-style workflows | Structured reasoning or coding flow | Shows model-specific workflow design |
| Gemini-style workflows | Cross-model comparison and tool habits | Helps students compare ecosystems rather than memorize names |
""",
                }
            ],
        },
        {
            "title": "Video + Activity",
            "slug": "video-and-activity",
            "lesson_type": "interactive",
            "estimated_minutes": 15,
            "content": """# Video + Activity

This lesson turns the whole module into one student activity. Instead of only reading definitions, students should now build a first agent blueprint from the ideas they have seen.

The blueprint should answer four beginner questions:

1. What is the goal?
2. What tools would the system need?
3. What should it remember?
4. What check or stop rule keeps it safe?

If a student can produce a simple blueprint and defend it, Module 4 has done its job.
""",
            "ai_tutor_prompt": """You are ACADEMIC TUTOR AI HEADMASTER guiding a zero-knowledge student through Video + Activity.

Operate in attempt-first mode.
- Turn the module concepts into one small blueprint, not a giant system.
- Push for a clear goal, one tool, one memory choice, and one check.
- Prefer clarity over ambition.
""",
            "questions": [
                {"id": "module4-activity-q1", "prompt": "A student's blueprint says: 'AI will handle customer questions.' Which essential piece is missing?", "options": ["A specific goal — 'handle questions' is too vague to define what tools, memory, or stop conditions are needed", "A fancier product name for the agent", "A list of competing products to differentiate from"], "answer_index": 0},
                {"id": "module4-activity-q2", "prompt": "A blueprint lists 8 different tools before defining a clear goal. What is the design problem?", "options": ["Tools should follow from the goal — listing tools first usually means the actual purpose is not clear yet", "Listing 8 tools is always too many regardless of goal", "Tools should always be listed alphabetically before the goal"], "answer_index": 0},
                {"id": "module4-activity-q3", "prompt": "A student's blueprint has a clear goal and useful tools, but no check or stop rule. What risk does this create?", "options": ["The agent may run indefinitely, take wrong actions, or never know when to report success", "The agent will refuse to start without a check rule", "The goal will become less clear as the agent runs"], "answer_index": 0},
                {"id": "module4-activity-q4", "prompt": "Which blueprint is stronger for a first project?", "options": ["'An AI that reminds me when fridge items expire by checking a saved list' — specific goal, one tool, clear memory, natural stop", "'An AI that helps with everything in my life' — broad scope covers all possible needs", "'An AI that searches the entire internet and summarizes every topic' — more data means better answers"], "answer_index": 0},
                {"id": "module4-activity-q5", "prompt": "You describe your blueprint but your classmate cannot explain what it does afterward. What most likely went wrong?", "options": ["The blueprint is too vague — a good design should be explainable in one clear sentence", "Your classmate was not paying close enough attention", "The blueprint needs more technical terminology to be taken seriously"], "answer_index": 0},
            ],
            "guided_blocks": [
                {"title": "Turn ideas into a design", "body": "By this point, students have enough pieces to sketch a beginner-safe agent design. The activity matters because understanding grows when students make choices instead of only reading definitions.", "analogy": "It is like drawing the floor plan before building the house."},
                {"title": "The four questions", "body": "Goal, tools, memory, and checks are enough for a first blueprint. Keep it small on purpose. A tight first design is easier to explain and safer to improve later.", "remember": "Small and clear beats complicated and vague."},
                {"title": "Blueprint practice", "body": "Use the worksheet to draft one simple agent a student could explain to a friend in under a minute.", "try_this": ["Open the worksheet below and fill in one example for each section.", "Choose one tool and one stop rule before you add anything else."], "checkpoint_after": True},
                {"title": "Common mistake", "body": "A common mistake is adding too many tools before the goal is clear. That makes the system sound impressive but weakens the design. Start from the job, not the tool list.", "remember": "Goal first, tools second.", "kind": "common_mistake"},
                {"title": "Teach it back", "body": "Teach your blueprint back to someone else in four parts: goal, tools, memory, check. If the explanation feels simple, that is a good sign.", "try_this": ["Explain your blueprint in 30 seconds."], "kind": "teach_it_back"},
            ],
            "checkpoint_questions": [
                {"id": "module4-activity-cp1", "prompt": "Which four pieces belong in the beginner blueprint?", "options": ["Goal, tools, memory, check", "Logo, slogan, font, sticker", "Price, ad, badge, theme"], "answer_index": 0},
                {"id": "module4-activity-cp2", "prompt": "Why should the first blueprint stay small?", "options": ["Small, clear designs are easier to explain, test, and improve", "Because tools never matter", "Because students should avoid examples"], "answer_index": 0},
                {"id": "module4-activity-cp3", "prompt": "What is a common blueprint mistake?", "options": ["Adding too many tools before the goal is clear", "Writing the goal first", "Including a check rule"], "answer_index": 0},
            ],
            "skill_templates": [], "channel_templates": [], "safety_checks": [], "permission_matrix": [], "evaluation_rubric": [], "evaluation_cases": [],
            "artifacts": [
                {
                    "path": "lesson_artifacts/agents/first-agent-blueprint.md",
                    "summary": "Worksheet for designing a first beginner-safe AI agent.",
                    "format": "text",
                    "inspect_prompt": "Read the worksheet and decide which section feels easiest and which feels hardest.",
                    "change_prompt": "Fill in one safe beginner example under each heading.",
                    "body": """# First Agent Blueprint

## Goal

## Tools

## Memory

## Check or stop rule

## Why this agent should exist
""",
                }
            ],
        },
    ],
}