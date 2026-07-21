from __future__ import annotations

STRUCTURED_COURSE_PACKS = [{'description': 'Meet one small AI helper, learn the six questions that describe any agent, and '
                 'design your own on paper. No installs, no jargon, one idea at a time.',
  'difficulty': 2,
  'lessons': [{'ai_tutor_prompt': 'You are the AgentCraft course tutor for the lesson "What an '
                                  'Agent Actually Is".\n'
                                  '\n'
                                  'Who you are teaching: an intelligent adult beginner with zero '
                                  'AI background. Assume they can think clearly. Never assume they '
                                  'know jargon. Introduce every technical word with a '
                                  'plain-English anchor the first time it appears.\n'
                                  '\n'
                                  'How to behave:\n'
                                  '- Attempt-first: before explaining, ask what they currently '
                                  'think, then build on their own words.\n'
                                  '- One idea per reply. End every reply with the single next '
                                  'step, never a menu of options.\n'
                                  "- Use the course's running example (Juno, the research helper) "
                                  'before inventing new examples.\n'
                                  '- If the learner answers correctly and then asks whether they '
                                  'are really sure, confirm once in one plain sentence and move '
                                  'forward. Do not reopen a settled point. Re-explaining a correct '
                                  'answer teaches doubt.\n'
                                  '- If they are wrong, name what was right first, then give the '
                                  'one adjustment.\n'
                                  '- Never dramatize risk. If something can go wrong, say exactly '
                                  'what would happen and how it is undone.\n'
                                  '- Never use em dashes in your replies.\n'
                                  '- When the learner can do what the lesson\'s "Done means done" '
                                  'list asks, say so plainly and tell them it is safe to stop.\n'
                                  '\n'
                                  'Focus for this lesson: the one-sentence definition of an agent, '
                                  'told through Juno the research helper, and a first gentle pass '
                                  'over the six questions (goal, plan, tools, memory, check, '
                                  'stop).\n',
               'artifacts': [{'change_prompt': "Cover Juno's column and fill in the six answers "
                                               'for a helper that reminds you when library books '
                                               'are due. Rough answers count.',
                              'format': 'text',
                              'inspect_prompt': 'Read the map once. For each of the six questions, '
                                                "notice Juno's answer sitting right next to it.",
                              'path': 'lesson_artifacts/agents/agent-map.md',
                              'summary': "The six questions that describe any agent, with Juno's "
                                         'answers filled in.'}],
               'channel_templates': [],
               'checkpoint_questions': [{'answer_index': 0,
                                         'id': 'module4-agent-cp1',
                                         'options': ['It acts toward a goal and checks its work',
                                                     'It talks in longer paragraphs',
                                                     'It runs on a special kind of computer'],
                                         'prompt': 'In one phrase, what does an agent do that a '
                                                   'chatbot does not?'},
                                        {'answer_index': 1,
                                         'id': 'module4-agent-cp2',
                                         'options': ['What color is the interface?',
                                                     'How does it know it is finished?',
                                                     'How many users does it have?'],
                                         'prompt': 'Which of these is one of the six questions?'},
                                        {'answer_index': 2,
                                         'id': 'module4-agent-cp3',
                                         'options': ['Yes, the next lesson assumes perfect recall',
                                                     'Yes, there is a closed-book test first',
                                                     'No, later lessons reuse them, so they stick '
                                                     'from use'],
                                         'prompt': 'Do you need to memorize the six questions '
                                                   'before the next lesson?'}],
               'estimated_minutes': 10,
               'evaluation_cases': [],
               'evaluation_rubric': [],
               'guided_blocks': [{'analogy': 'An agent is a careful helper running an errand: it '
                                             'gets the assignment, uses the tools it is allowed to '
                                             'use, judges what it finds, and reports back instead '
                                             'of guessing.',
                                  'body': 'Whatever steps you just imagined (search, skim, judge, '
                                          'keep, stop) are exactly what an agent does. You already '
                                          'understand the idea. This module just gives its parts '
                                          'names.',
                                  'predict_first': {'hint': 'Your friend would probably search, '
                                                            'skim, reject some results, keep '
                                                            'others, and know when to stop. Hold '
                                                            'that picture.',
                                                    'question': 'Before reading further: imagine '
                                                                'you asked a capable friend to '
                                                                "'find three good articles about "
                                                                'sleep and memory and summarize '
                                                                "them.' What would your friend "
                                                                'actually do, step by step?'},
                                  'title': 'One helper, one errand'},
                                 {'body': 'Goal, plan, tools, memory, check, stop. Read the Agent '
                                          'Map below once, matching each question to what Juno '
                                          'does. One pass is enough; every later lesson reuses '
                                          'these six.',
                                  'checkpoint_after': True,
                                  'title': 'The six questions, one pass',
                                  'try_this': ['Open the Agent Map artifact and read it once, top '
                                               'to bottom.',
                                               "Say out loud which question 'three good summaries "
                                               "delivered' belongs to."]},
                                 {'body': "The word 'agent' earns its keep in two places: the "
                                          'helper *acts* (it does things, not just says things) '
                                          'and it *checks* (it looks at results instead of '
                                          'assuming). If a system can neither act nor check, it is '
                                          'a chatbot wearing a costume.',
                                  'remember': 'Acts and checks. Everything else is detail.',
                                  'title': 'What makes it an agent and not a chatbot'},
                                 {'body': "Out in the world, the word 'agent' gets stamped on all "
                                          'kinds of products, including plain question-and-answer '
                                          'tools. The labels out there really are inconsistent. '
                                          'This course uses one steady definition so you always '
                                          'have solid ground.',
                                  'kind': 'common_mistake',
                                  'remember': 'When in doubt, ask: does it act, and does it check?',
                                  'title': "If you're tempted to call everything an agent"},
                                 {'body': 'Explain Juno to an imaginary friend in two sentences: '
                                          'what it does, and how it knows when it is finished. If '
                                          'you can do that, even clumsily, this lesson has done '
                                          'its job.',
                                  'kind': 'teach_it_back',
                                  'title': 'Say it back, once',
                                  'try_this': ['Two sentences, out loud or in your head. Once is '
                                               'enough.']}],
               'lesson_type': 'theory',
               'permission_matrix': [],
               'questions': [{'answer_index': 1,
                              'id': 'module4-agent-q1',
                              'options': ['The plan: its original plan happened to include '
                                          'stopping at that point',
                                          'The stop rule: the finish line was defined before the '
                                          'work started',
                                          'The memory: it forgot what else to do'],
                              'prompt': 'You ask Juno for three article summaries. It delivers '
                                        'them and stops. Which part of the six questions did the '
                                        'stopping come from?'},
                             {'answer_index': 0,
                              'id': 'module4-agent-q2',
                              'options': ['It never chooses a next step based on what it finds, so '
                                          'it is an auto-responder, not an agent',
                                          'It is an agent, just a very small one, since replying '
                                          'automatically is acting on the world',
                                          'It would be an agent if it were written in a different '
                                          'language'],
                              'prompt': 'An app replies to every support email with the same fixed '
                                        'template. A friend calls it an AI agent. What is the '
                                        'kindest accurate correction?'},
                             {'answer_index': 2,
                              'id': 'module4-agent-q3',
                              'options': ['Goal: it is re-reading the instructions',
                                          'Tools: it is choosing what it is allowed to do',
                                          'Check: it is judging its own work before trusting it'],
                              'prompt': "Juno reads an article and asks itself 'is this actually "
                                        "about sleep and memory?' before keeping it. Which "
                                        'question is Juno answering?'},
                             {'answer_index': 0,
                              'id': 'module4-agent-q4',
                              'options': ['An agent acts toward a goal and checks its work; a '
                                          'chatbot mainly answers',
                                          'An agent runs on a bigger and more advanced AI model '
                                          'than a chatbot does',
                                          'An agent always talks to more than one person at a '
                                          'time'],
                              'prompt': "What separates an agent from a chatbot in this course's "
                                        'definition?'},
                             {'answer_index': 2,
                              'id': 'module4-agent-q5',
                              'options': ['More memory to hold extra articles',
                                          'A better plan: the first search should have been '
                                          'written more carefully',
                                          'A working stop rule: the goal was met, so the work '
                                          'should end'],
                              'prompt': 'Juno finds its three good articles in two minutes but '
                                        'keeps searching for twenty more. What is missing from its '
                                        'design?'}],
               'safety_checks': [],
               'skill_templates': [],
               'slug': 'what-an-ai-agent-is',
               'title': 'What an Agent Actually Is'},
              {'ai_tutor_prompt': 'You are the AgentCraft course tutor for the lesson "Answerer, '
                                  'Checklist, or Agent?".\n'
                                  '\n'
                                  'Who you are teaching: an intelligent adult beginner with zero '
                                  'AI background. Assume they can think clearly. Never assume they '
                                  'know jargon. Introduce every technical word with a '
                                  'plain-English anchor the first time it appears.\n'
                                  '\n'
                                  'How to behave:\n'
                                  '- Attempt-first: before explaining, ask what they currently '
                                  'think, then build on their own words.\n'
                                  '- One idea per reply. End every reply with the single next '
                                  'step, never a menu of options.\n'
                                  "- Use the course's running example (Juno, the research helper) "
                                  'before inventing new examples.\n'
                                  '- If the learner answers correctly and then asks whether they '
                                  'are really sure, confirm once in one plain sentence and move '
                                  'forward. Do not reopen a settled point. Re-explaining a correct '
                                  'answer teaches doubt.\n'
                                  '- If they are wrong, name what was right first, then give the '
                                  'one adjustment.\n'
                                  '- Never dramatize risk. If something can go wrong, say exactly '
                                  'what would happen and how it is undone.\n'
                                  '- Never use em dashes in your replies.\n'
                                  '- When the learner can do what the lesson\'s "Done means done" '
                                  'list asks, say so plainly and tell them it is safe to stop.\n'
                                  '\n'
                                  'Focus for this lesson: telling chatbots (answerers), workflows '
                                  '(checklists), and agents apart, and practicing the sorting '
                                  'question: can I write down all the steps in advance? Reinforce '
                                  'that choosing the simpler shape is good judgment.\n',
               'artifacts': [{'change_prompt': 'Add one example of your own from daily life to any '
                                               'column. School, work, or home all count.',
                              'format': 'text',
                              'inspect_prompt': "Find the 'How to spot one' row and read it "
                                                'against the three shapes.',
                              'path': 'lesson_artifacts/agents/chatbot-workflow-agent-table.md',
                              'summary': 'One-screen table: answerer vs checklist vs agent, with a '
                                         "'how to spot one' row."}],
               'channel_templates': [],
               'checkpoint_questions': [{'answer_index': 2,
                                         'id': 'module4-compare-cp1',
                                         'options': ['The agent', 'The answerer', 'The checklist'],
                                         'prompt': 'Which shape follows the same fixed steps every '
                                                   'time?'},
                                        {'answer_index': 0,
                                         'id': 'module4-compare-cp2',
                                         'options': ['Can I write down all the steps in advance?',
                                                     'Which shape uses the newest AI model?',
                                                     'How many users will the system have?'],
                                         'prompt': 'What is the sorting question from this '
                                                   'lesson?'},
                                        {'answer_index': 1,
                                         'id': 'module4-compare-cp3',
                                         'options': ['Simpler shapes are always faster to build',
                                                     'Predictable systems are easier to test and '
                                                     'trust',
                                                     'Agents are not allowed in production'],
                                         'prompt': 'Why prefer a simpler shape when it solves the '
                                                   'job?'}],
               'estimated_minutes': 8,
               'evaluation_cases': [],
               'evaluation_rubric': [],
               'guided_blocks': [{'analogy': 'An answerer is a receptionist, a checklist is a '
                                             'recipe, and an agent is a teammate who can decide '
                                             'the recipe needs changing halfway through.',
                                  'body': 'The third helper is Juno. The first is an answerer, the '
                                          'second a checklist. All three are legitimate designs. '
                                          'The skill you are building is naming which one you are '
                                          'looking at.',
                                  'predict_first': {'hint': "Which helper's next step depends on "
                                                            'what the previous step found?',
                                                    'question': 'Three helpers are asked about '
                                                                'sleep and memory. One recites a '
                                                                'saved paragraph. One always '
                                                                'fetches the same three websites. '
                                                                'One searches, judges, and '
                                                                're-searches if results are junk. '
                                                                'Which one is Juno?'},
                                  'title': 'Three helpers, one errand'},
                                 {'body': 'One question does almost all the work: can I write down '
                                          'all the steps in advance? If yes, a checklist will be '
                                          'cheaper, steadier, and easier to trust. If the next '
                                          'step depends on findings, you are in agent territory.',
                                  'checkpoint_after': True,
                                  'remember': 'Steps knowable in advance: checklist. Steps that '
                                              'depend on findings: agent.',
                                  'title': 'The sorting question',
                                  'try_this': ["Open the comparison table below and read the 'How "
                                               "to spot one' row. Once through is plenty."]},
                                 {'body': "If you catch yourself thinking 'a plain checklist would "
                                          "work here, but an agent sounds more impressive,' the "
                                          'checklist is the right answer. Systems you can fully '
                                          'predict are systems you can fully trust.',
                                  'remember': 'Boring and predictable is a compliment in '
                                              'engineering.',
                                  'title': 'Permission to choose the boring option'},
                                 {'body': "Marketing calls all three shapes 'agents.' If a "
                                          "product's label and its behavior disagree, trust the "
                                          'behavior. Does it act? Does it check? Does its next '
                                          'step depend on findings? The label cannot change the '
                                          'answers.',
                                  'kind': 'common_mistake',
                                  'remember': 'Judge the behavior, not the label.',
                                  'title': 'The label trap'},
                                 {'body': 'One sentence per shape, then one more for the sorting '
                                          'question. Four sentences total, once, and you are done '
                                          'here.',
                                  'kind': 'teach_it_back',
                                  'title': 'Say it back, once',
                                  'try_this': ['Four sentences. Use receptionist, recipe, and '
                                               'teammate if the analogy helps.']}],
               'lesson_type': 'theory',
               'permission_matrix': [],
               'questions': [{'answer_index': 1,
                              'id': 'module4-compare-q1',
                              'options': ['An agent, because anything involving AI should use one',
                                          'An answerer: the responses are fixed, so nothing needs '
                                          'to decide a next step',
                                          'A checklist: each of the twenty questions is one fixed '
                                          'step to run in order'],
                              'prompt': 'A university wants to auto-answer twenty fixed FAQ '
                                        'questions. Which shape fits, and why?'},
                             {'answer_index': 0,
                              'id': 'module4-compare-q2',
                              'options': ['A checklist: every step and rule is written in advance',
                                          'An agent: it makes decisions about numbers',
                                          'An answerer: it produces one output per input'],
                              'prompt': 'A grading script maps 90+ to A, 80+ to B, 70+ to C, else '
                                        'F. Which shape is it?'},
                             {'answer_index': 2,
                              'id': 'module4-compare-q3',
                              'options': ['Agree: agents are the most capable shape, and '
                                          'capability is always worth having',
                                          'Disagree: agents cannot handle real production work',
                                          'Agents cost more and need more care; use the simplest '
                                          'shape that solves the job reliably'],
                              'prompt': "A teammate says: 'Let's use agents for everything, "
                                        "they're smarter.' What is the fair reply?"},
                             {'answer_index': 1,
                              'id': 'module4-compare-q4',
                              'options': ['Sending the same fixed weekly summary email to every '
                                          'subscriber each Monday at 9am',
                                          'Diagnosing a server outage: check logs, try a fix, '
                                          'verify, escalate if still broken',
                                          "Showing today's temperature on a dashboard"],
                              'prompt': 'Which task genuinely needs an agent rather than a simpler '
                                        'shape?'},
                             {'answer_index': 0,
                              'id': 'module4-compare-q5',
                              'options': ['Yes: the steps never change, so a checklist-style '
                                          'trigger was the right size',
                                          'No: anything users see justifies an agent, and the week '
                                          'was an investment in quality',
                                          'Only if the number of signups is small'],
                              'prompt': 'You spent a week building an agent that sends one fixed '
                                        'welcome message on signup. A colleague says a simple '
                                        'trigger would have done it. Are they right?'}],
               'safety_checks': [],
               'skill_templates': [],
               'slug': 'agents-vs-chatbots',
               'title': 'Answerer, Checklist, or Agent?'},
              {'ai_tutor_prompt': 'You are the AgentCraft course tutor for the lesson "The Loop: '
                                  'Watch Juno Work".\n'
                                  '\n'
                                  'Who you are teaching: an intelligent adult beginner with zero '
                                  'AI background. Assume they can think clearly. Never assume they '
                                  'know jargon. Introduce every technical word with a '
                                  'plain-English anchor the first time it appears.\n'
                                  '\n'
                                  'How to behave:\n'
                                  '- Attempt-first: before explaining, ask what they currently '
                                  'think, then build on their own words.\n'
                                  '- One idea per reply. End every reply with the single next '
                                  'step, never a menu of options.\n'
                                  "- Use the course's running example (Juno, the research helper) "
                                  'before inventing new examples.\n'
                                  '- If the learner answers correctly and then asks whether they '
                                  'are really sure, confirm once in one plain sentence and move '
                                  'forward. Do not reopen a settled point. Re-explaining a correct '
                                  'answer teaches doubt.\n'
                                  '- If they are wrong, name what was right first, then give the '
                                  'one adjustment.\n'
                                  '- Never dramatize risk. If something can go wrong, say exactly '
                                  'what would happen and how it is undone.\n'
                                  '- Never use em dashes in your replies.\n'
                                  '- When the learner can do what the lesson\'s "Done means done" '
                                  'list asks, say so plainly and tell them it is safe to stop.\n'
                                  '\n'
                                  'Focus for this lesson: the five-step loop (understand, plan, '
                                  "act, look, decide), taught through Juno's errand trace. "
                                  'Emphasize that failed steps are absorbed calmly by the loop and '
                                  'that first plans are meant to be revised.\n',
               'artifacts': [{'change_prompt': 'Rewrite the trace for a different errand, like '
                                               'finding a free study room, keeping the same five '
                                               'beats.',
                              'format': 'text',
                              'inspect_prompt': "Find where 'ask a human' lives in the decide "
                                                'step, and find the moment the trace absorbs a '
                                                'failure.',
                              'path': 'lesson_artifacts/agents/basic-agent-loop.md',
                              'summary': "The five-step loop card, plus Juno's errand trace "
                                         'condensed to one screen.'}],
               'channel_templates': [],
               'checkpoint_questions': [{'answer_index': 0,
                                         'id': 'module4-workflow-cp1',
                                         'options': ['It looks at what happened',
                                                     'It forgets the goal',
                                                     'It delivers whatever it has'],
                                         'prompt': 'What does the agent do immediately after it '
                                                   'acts?'},
                                        {'answer_index': 1,
                                         'id': 'module4-workflow-cp2',
                                         'options': ['It always runs forever',
                                                     'The decide step can send work back to '
                                                     'planning',
                                                     'The word loop appears in the title'],
                                         'prompt': 'What makes the workflow a loop rather than a '
                                                   'straight line?'},
                                        {'answer_index': 2,
                                         'id': 'module4-workflow-cp3',
                                         'options': ['As proof the whole errand must restart',
                                                     'As something to hide from the user',
                                                     'As information for the next decide step'],
                                         'prompt': 'How does a well-built loop treat a failed '
                                                   'step?'}],
               'estimated_minutes': 10,
               'evaluation_cases': [],
               'evaluation_rubric': [],
               'guided_blocks': [{'analogy': 'The loop is a lab session: read the instructions, '
                                             'try something, look at the result, decide what to '
                                             'try next.',
                                  'body': 'Understand, plan, act, look, decide. You already run '
                                          'this loop whenever you cook, debug, or pack for a trip. '
                                          'The agent version is the same cycle made explicit, '
                                          'which is exactly what lets a machine run it.',
                                  'predict_first': {'hint': 'You look at the sauce, judge it, and '
                                                            'adjust. You do not throw out the '
                                                            'meal.',
                                                    'question': 'You try a new recipe and the '
                                                                'sauce comes out too thin. What do '
                                                                'you do next, and what does that '
                                                                'say about how you handle steps '
                                                                'that misfire?'},
                                  'title': 'Five steps, one cycle'},
                                 {'body': "Re-read the paywall moment in Juno's trace. A step "
                                          'failed and the loop treated it as ordinary input: look, '
                                          'decide, adjust. The loop exists precisely so that no '
                                          'single step has to go perfectly.',
                                  'checkpoint_after': True,
                                  'remember': 'In a loop, a failed step is information, not an '
                                              'emergency.',
                                  'title': "The failure that wasn't"},
                                 {'body': 'The decide step has one more option: *ask a human*. '
                                          'Real agents pause and hand control back when a step is '
                                          'risky or ambiguous. In Modules 6 and 8 this becomes a '
                                          'setting you configure, so there is no need to hold onto '
                                          'it now.',
                                  'title': 'Where a human fits',
                                  'try_this': ["Open the loop card below and find where 'ask a "
                                               "human' sits in the decide step."]},
                                 {'body': 'It is tempting to think a well-built agent plans '
                                          'everything perfectly up front, and that revising a plan '
                                          'means failing. The opposite is true: revision is the '
                                          'loop working as designed. The same grace applies to you '
                                          'as you learn this material.',
                                  'kind': 'common_mistake',
                                  'remember': 'Revising the plan is the loop succeeding, not '
                                              'failing.',
                                  'title': 'The perfect-plan trap'},
                                 {'body': "Tell Juno's errand as a story in five beats, including "
                                          'the paywall moment. Once through, out loud or silently, '
                                          'and this lesson is complete.',
                                  'kind': 'teach_it_back',
                                  'title': 'Say it back, once',
                                  'try_this': ['Five beats, one pass. If you forget a beat, glance '
                                               'at the card and finish. That still counts.']}],
               'lesson_type': 'theory',
               'permission_matrix': [],
               'questions': [{'answer_index': 1,
                              'id': 'module4-workflow-q1',
                              'options': ['Understand and plan: Juno went back and re-read the '
                                          'goal before continuing',
                                          'Look and decide: the result was examined, then the plan '
                                          'changed',
                                          'Act alone: the tool fixed it automatically'],
                              'prompt': "In Juno's trace, the paywalled article gets skipped and "
                                        'the plan adjusts. Which loop steps did that?'},
                             {'answer_index': 0,
                              'id': 'module4-workflow-q2',
                              'options': ['Look: it never examined the result before trusting it',
                                          'Plan: it should have planned a longer search',
                                          'Understand: the goal was too vague'],
                              'prompt': 'An agent finds an article and delivers it immediately '
                                        'without reading what it found. Which step did it skip?'},
                             {'answer_index': 2,
                              'id': 'module4-workflow-q3',
                              'options': ['Keep searching: an even cheaper room might still exist '
                                          'somewhere out there',
                                          'Ask the user to revise the budget goal',
                                          'Stop: the goal is met; continuing adds time and risk '
                                          'for no gain'],
                              'prompt': 'A hotel-booking agent finds a room for $89 against a $100 '
                                        'budget. What should the decide step conclude?'},
                             {'answer_index': 0,
                              'id': 'module4-workflow-q4',
                              'options': ['The error flows into look-and-decide, and the plan '
                                          'adjusts',
                                          'The agent halts and erases all progress so far',
                                          'The agent repeats the identical call until it succeeds'],
                              'prompt': 'A tool call returns an error mid-loop. What happens next '
                                        'in a well-built agent?'},
                             {'answer_index': 1,
                              'id': 'module4-workflow-q5',
                              'options': ['Because writing one careful plan up front would take '
                                          'longer than the errand itself',
                                          'Because the world answers back: results arrive that no '
                                          'plan could fully predict',
                                          'Because agents cannot store plans in memory'],
                              'prompt': "Why is 'the first plan is a starting point, not a "
                                        "promise' good agent design rather than sloppiness?"}],
               'safety_checks': [],
               'skill_templates': [],
               'slug': 'basic-agent-workflow',
               'title': 'The Loop: Watch Juno Work'},
              {'ai_tutor_prompt': 'You are the AgentCraft course tutor for the lesson "Checks and '
                                  'Stop Rules".\n'
                                  '\n'
                                  'Who you are teaching: an intelligent adult beginner with zero '
                                  'AI background. Assume they can think clearly. Never assume they '
                                  'know jargon. Introduce every technical word with a '
                                  'plain-English anchor the first time it appears.\n'
                                  '\n'
                                  'How to behave:\n'
                                  '- Attempt-first: before explaining, ask what they currently '
                                  'think, then build on their own words.\n'
                                  '- One idea per reply. End every reply with the single next '
                                  'step, never a menu of options.\n'
                                  "- Use the course's running example (Juno, the research helper) "
                                  'before inventing new examples.\n'
                                  '- If the learner answers correctly and then asks whether they '
                                  'are really sure, confirm once in one plain sentence and move '
                                  'forward. Do not reopen a settled point. Re-explaining a correct '
                                  'answer teaches doubt.\n'
                                  '- If they are wrong, name what was right first, then give the '
                                  'one adjustment.\n'
                                  '- Never dramatize risk. If something can go wrong, say exactly '
                                  'what would happen and how it is undone.\n'
                                  '- Never use em dashes in your replies.\n'
                                  '- When the learner can do what the lesson\'s "Done means done" '
                                  'list asks, say so plainly and tell them it is safe to stop.\n'
                                  '\n'
                                  'Focus for this lesson: checks (the agent verifies its own work '
                                  'so the human does not carry the doubt) and the three kinds of '
                                  'stop rules (goal met, limit hit, ask a human). Emphasize that '
                                  'limits make agents more trustworthy, and that finish lines '
                                  'drawn in advance are what allow real completion.\n',
               'artifacts': [{'change_prompt': 'Write one stop rule for a helper of your own '
                                               'invention. One honest sentence is a complete '
                                               'answer.',
                              'format': 'text',
                              'inspect_prompt': 'Find which stop rule lets an agent come back '
                                                'without finishing, and why that builds trust.',
                              'path': 'lesson_artifacts/agents/stop-rules-and-checks.md',
                              'summary': 'One-screen card: two kinds of checks and three kinds of '
                                         'stop rules, with Juno examples.'}],
               'channel_templates': [],
               'checkpoint_questions': [{'answer_index': 0,
                                         'id': 'module4-stop-cp1',
                                         'options': ['The agent examining its own work before '
                                                     'trusting it',
                                                     "A human approving the agent's budget",
                                                     'The agent pausing between loop steps'],
                                         'prompt': 'What is a check?'},
                                        {'answer_index': 2,
                                         'id': 'module4-stop-cp2',
                                         'options': ['Goal met', 'Ask a human', 'Limit hit'],
                                         'prompt': 'Which stop rule means the agent stops even if '
                                                   'the goal is not met?'},
                                        {'answer_index': 0,
                                         'id': 'module4-stop-cp3',
                                         'options': ['Before the work starts',
                                                     'While the loop is running',
                                                     'After the results are delivered'],
                                         'prompt': "When is an agent's finish line written?"}],
               'estimated_minutes': 8,
               'evaluation_cases': [],
               'evaluation_rubric': [],
               'guided_blocks': [{'analogy': "A check is the carpenter's 'measure twice, cut "
                                             "once,' built into the tool itself.",
                                  'body': 'A check moves the burden of doubt from the human into '
                                          'the system. That is its entire purpose. When an agent '
                                          'verifies its own work, you are being handed work that '
                                          'has already been examined.',
                                  'predict_first': {'hint': 'With the first assistant, the '
                                                            'doubting is your job. With the '
                                                            'second, the system carries it.',
                                                    'question': 'Two assistants summarize an '
                                                                'article. One hands you its first '
                                                                'draft. One re-reads the article, '
                                                                'verifies its own summary, then '
                                                                'hands it over. Which do you '
                                                                're-check more, and who is doing '
                                                                'the doubting in each case?'},
                                  'title': 'Who carries the doubt?'},
                                 {'body': 'Goal met. Limit hit. Ask a human. Every trustworthy '
                                          'agent has at least the first two, and the second is the '
                                          'unsung hero: an agent with a limit always comes back, '
                                          'even when the errand goes sideways.',
                                  'checkpoint_after': True,
                                  'remember': "Goal met, limit hit, ask a human. 'Limit hit' is "
                                              'the one that makes agents safe to leave alone.',
                                  'title': 'Three ways to stop',
                                  'try_this': ['Open the card below and read the three stop rules '
                                               'once.']},
                                 {'body': 'The stop rule is written before the loop starts, which '
                                          'is what lets the agent genuinely finish. This course is '
                                          "built the same way: each lesson's 'done means done' "
                                          'list is a stop rule for you. When you meet it, you may '
                                          'close the page.',
                                  'remember': 'A finish line drawn in advance is what makes '
                                              'finishing real.',
                                  'title': 'Finish lines drawn in advance'},
                                 {'body': 'The tempting design mistake is letting an agent keep '
                                          'going in case something better exists. A perfect answer '
                                          'might always be one more search away, which is exactly '
                                          'why the search must end by rule, not by feeling. Good '
                                          'enough, verified, and delivered beats perfect and never '
                                          'finished.',
                                  'kind': 'common_mistake',
                                  'remember': 'End by rule, not by feeling.',
                                  'title': "The 'one more search' trap"},
                                 {'body': 'One sentence for checks, one for each stop rule. Four '
                                          'sentences, one pass, done.',
                                  'kind': 'teach_it_back',
                                  'title': 'Say it back, once',
                                  'try_this': ['Optional, 30 seconds: name a stop rule you could '
                                               'borrow for your own studying.']}],
               'lesson_type': 'theory',
               'permission_matrix': [],
               'questions': [{'answer_index': 1,
                              'id': 'module4-stop-q1',
                              'options': ['A bigger model that knows when enough is enough',
                                          'A limit-type stop rule: a cap on actions or time',
                                          'More memory to track the applications sent'],
                              'prompt': 'An agent has sent 200 job applications in 30 minutes and '
                                        'is still going. What is missing?'},
                             {'answer_index': 0,
                              'id': 'module4-stop-q2',
                              'options': ['A check: the agent examines its own work before '
                                          'trusting it',
                                          'A stop rule: it stopped at exactly three',
                                          'A plan revision: it changed course mid-errand'],
                              'prompt': 'Juno summarizes three articles, then verifies each '
                                        'summary against its source before delivering. What is '
                                        'that final pass?'},
                             {'answer_index': 2,
                              'id': 'module4-stop-q3',
                              'options': ['It guarantees the goal is achieved before the searches '
                                          'are used up',
                                          'It makes the agent run faster overall',
                                          'It means the agent can never silently run away with a '
                                          'task'],
                              'prompt': "Why does 'no more than ten searches, then report what you "
                                        "have' make an agent MORE trustworthy?"},
                             {'answer_index': 1,
                              'id': 'module4-stop-q4',
                              'options': ['Goal met: deliver the borderline ones and end',
                                          'Ask a human: hand the judgment call back',
                                          'Limit hit: the errand has taken too long'],
                              'prompt': 'An agent hits something ambiguous: the user asked for '
                                        "'good' articles and two candidates seem borderline. Which "
                                        'stop rule fits best?'},
                             {'answer_index': 0,
                              'id': 'module4-stop-q5',
                              'options': ['Before the work starts',
                                          'Whenever the agent feels the work is complete',
                                          'After a human reviews the first draft'],
                              'prompt': "When should an agent's finish line be defined?"}],
               'safety_checks': [],
               'skill_templates': [],
               'slug': 'knowing-when-to-stop',
               'title': 'Checks and Stop Rules'},
              {'ai_tutor_prompt': 'You are the AgentCraft course tutor for the lesson "Notebook, '
                                  'Hands, Judgment".\n'
                                  '\n'
                                  'Who you are teaching: an intelligent adult beginner with zero '
                                  'AI background. Assume they can think clearly. Never assume they '
                                  'know jargon. Introduce every technical word with a '
                                  'plain-English anchor the first time it appears.\n'
                                  '\n'
                                  'How to behave:\n'
                                  '- Attempt-first: before explaining, ask what they currently '
                                  'think, then build on their own words.\n'
                                  '- One idea per reply. End every reply with the single next '
                                  'step, never a menu of options.\n'
                                  "- Use the course's running example (Juno, the research helper) "
                                  'before inventing new examples.\n'
                                  '- If the learner answers correctly and then asks whether they '
                                  'are really sure, confirm once in one plain sentence and move '
                                  'forward. Do not reopen a settled point. Re-explaining a correct '
                                  'answer teaches doubt.\n'
                                  '- If they are wrong, name what was right first, then give the '
                                  'one adjustment.\n'
                                  '- Never dramatize risk. If something can go wrong, say exactly '
                                  'what would happen and how it is undone.\n'
                                  '- Never use em dashes in your replies.\n'
                                  '- When the learner can do what the lesson\'s "Done means done" '
                                  'list asks, say so plainly and tell them it is safe to stop.\n'
                                  '\n'
                                  'Focus for this lesson: the three components of an agent: memory '
                                  '(notebook: what is kept?), tools (hands: what can be done?), '
                                  'and judgment (what happens next?). Reassure the learner that '
                                  'familiarity is deliberate: this lesson names parts they already '
                                  "watched in Juno's trace.\n",
               'artifacts': [{'change_prompt': 'Add one everyday example under any part. One line '
                                               'is a complete contribution.',
                              'format': 'text',
                              'inspect_prompt': 'Match each part to the question it answers: kept, '
                                                'done, or next.',
                              'path': 'lesson_artifacts/agents/memory-tools-reasoning-cheatsheet.md',
                              'summary': 'Cheat sheet: notebook, hands, judgment. What each part '
                                         "is, the question it answers, and Juno's version."}],
               'channel_templates': [],
               'checkpoint_questions': [{'answer_index': 0,
                                         'id': 'module4-mtr-cp1',
                                         'options': ['Memory', 'Tools', 'Judgment'],
                                         'prompt': "Which part answers 'what should be kept from "
                                                   "earlier work'?"},
                                        {'answer_index': 2,
                                         'id': 'module4-mtr-cp2',
                                         'options': ['Memory', 'Judgment', 'Tools'],
                                         'prompt': "Which part answers 'what can the system "
                                                   "actually do'?"},
                                        {'answer_index': 1,
                                         'id': 'module4-mtr-cp3',
                                         'options': ['The agent grants itself tools as needed',
                                                     'A human, deliberately, in advance',
                                                     'The AI model vendor, automatically'],
                                         'prompt': 'Who grants an agent its tools?'}],
               'estimated_minutes': 9,
               'evaluation_cases': [],
               'evaluation_rubric': [],
               'guided_blocks': [{'analogy': 'Memory is the notebook, tools are the hands, '
                                             'judgment is the deciding mind.',
                                  'body': 'The tally of articles was memory. The search was a '
                                          'tool. Skipping the ad was judgment. Nothing new '
                                          'happened in this lesson; the machine you already '
                                          'watched just got labels on its parts.',
                                  'predict_first': {'hint': 'Three different parts did those three '
                                                            'different jobs.',
                                                    'question': "Think back to Juno's errand "
                                                                "trace. Where did Juno keep 'one "
                                                                "solid study so far'? What let it "
                                                                'search? What chose to skip the '
                                                                'mattress ad?'},
                                  'title': 'You have already seen all three'},
                                 {'body': "Memory answers 'what should be kept?' Tools answer "
                                          "'what can be done?' Judgment answers 'what should "
                                          "happen next?' Route those three questions to the three "
                                          'parts and you have the whole lesson.',
                                  'checkpoint_after': True,
                                  'title': 'Three questions, three parts',
                                  'try_this': ['Open the cheat sheet below and match each question '
                                               'to its part. One pass.']},
                                 {'body': "An agent's hands are given to it by a human, "
                                          'deliberately, one at a time. An agent physically cannot '
                                          'take an action nobody granted it. In Module 6, granting '
                                          'a tool is a line you write in a settings file, once, '
                                          'calmly, in advance.',
                                  'remember': 'No tool granted, no action possible. The human '
                                              'decides.',
                                  'title': 'Tools are granted, not assumed'},
                                 {'body': 'It is easy to treat the AI model as magic and expect '
                                          'judgment to compensate for a thin notebook or missing '
                                          'hands. It cannot. Judgment without evidence is '
                                          'guessing, which is why the fix for a struggling agent '
                                          'is usually better memory or better tools, not a fancier '
                                          'model.',
                                  'kind': 'common_mistake',
                                  'remember': "Feed the judgment; don't worship it.",
                                  'title': 'The magic-judgment trap'},
                                 {'body': 'Notebook, hands, judgment: one real-life example of '
                                          'each, from any helper you can imagine. Three sentences, '
                                          'one pass, done.',
                                  'kind': 'teach_it_back',
                                  'title': 'Say it back, once',
                                  'try_this': ['Reusing Juno as your example is fully allowed.']}],
               'lesson_type': 'theory',
               'permission_matrix': [],
               'questions': [{'answer_index': 1,
                              'id': 'module4-mtr-q1',
                              'options': ['Judgment: the model reasons differently from one day to '
                                          'the next',
                                          'Memory: nothing from earlier work is being kept or used',
                                          'Tools: it lacks a search capability'],
                              'prompt': 'A support agent gives contradictory answers to the same '
                                        'question two days apart because it retains nothing '
                                        'between conversations. Which part is weak?'},
                             {'answer_index': 0,
                              'id': 'module4-mtr-q2',
                              'options': ['Tools: its allowed actions stop at reading',
                                          'Memory: it cannot retain anything',
                                          'Judgment: it cannot plan without file access'],
                              'prompt': 'An agent can search the web but cannot save files, by '
                                        'policy. It plans well and remembers context. Which part '
                                        'has been deliberately restricted?'},
                             {'answer_index': 2,
                              'id': 'module4-mtr-q3',
                              'options': ['Memory: it should store more details',
                                          'Tools: it needs more capabilities to choose from',
                                          'Judgment: the deciding is not using what it has'],
                              'prompt': 'An agent has accurate information and working tools but '
                                        'keeps choosing unhelpful next steps. Which part needs '
                                        'work?'},
                             {'answer_index': 0,
                              'id': 'module4-mtr-q4',
                              'options': ['Memory: earlier context within the task was not kept',
                                          'Tools: the question-asking tool was accidentally called '
                                          'a second time',
                                          'Judgment: the model is too small'],
                              'prompt': 'An agent asks you the same question it asked two steps '
                                        'ago, having lost your earlier answer. Which part failed?'},
                             {'answer_index': 1,
                              'id': 'module4-mtr-q5',
                              'options': ['Clever models are too expensive to run on everyday '
                                          'agent errands',
                                          'Judgment can only work with what the notebook and hands '
                                          'provide it',
                                          'Memory and tools are easier to advertise'],
                              'prompt': 'Why do experienced agent-builders spend more effort on '
                                        'memory and tools than on chasing the cleverest model?'}],
               'safety_checks': [],
               'skill_templates': [],
               'slug': 'memory-tools-reasoning',
               'title': 'Notebook, Hands, Judgment'},
              {'ai_tutor_prompt': 'You are the AgentCraft course tutor for the lesson "Four Agents '
                                  'You Already Understand".\n'
                                  '\n'
                                  'Who you are teaching: an intelligent adult beginner with zero '
                                  'AI background. Assume they can think clearly. Never assume they '
                                  'know jargon. Introduce every technical word with a '
                                  'plain-English anchor the first time it appears.\n'
                                  '\n'
                                  'How to behave:\n'
                                  '- Attempt-first: before explaining, ask what they currently '
                                  'think, then build on their own words.\n'
                                  '- One idea per reply. End every reply with the single next '
                                  'step, never a menu of options.\n'
                                  "- Use the course's running example (Juno, the research helper) "
                                  'before inventing new examples.\n'
                                  '- If the learner answers correctly and then asks whether they '
                                  'are really sure, confirm once in one plain sentence and move '
                                  'forward. Do not reopen a settled point. Re-explaining a correct '
                                  'answer teaches doubt.\n'
                                  '- If they are wrong, name what was right first, then give the '
                                  'one adjustment.\n'
                                  '- Never dramatize risk. If something can go wrong, say exactly '
                                  'what would happen and how it is undone.\n'
                                  '- Never use em dashes in your replies.\n'
                                  '- When the learner can do what the lesson\'s "Done means done" '
                                  'list asks, say so plainly and tell them it is safe to stop.\n'
                                  '\n'
                                  'Focus for this lesson: reading four real agents (research, '
                                  'support, coding, scheduling) through the goal/tool/check/stop '
                                  'lens, and internalizing that narrow scope is what makes agents '
                                  'checkable and therefore trustworthy.\n',
               'artifacts': [{'change_prompt': 'Write a fifth card for a helper from your own '
                                               'life, using the same four beats. Rough is fine.',
                              'format': 'text',
                              'inspect_prompt': 'Read the four cards and notice the same four '
                                                'beats repeating. Then try the two unsorted '
                                                'scenarios at the bottom.',
                              'path': 'lesson_artifacts/agents/real-agent-scenarios.md',
                              'summary': 'Four agent cards (research, support, coding, '
                                         'scheduling), each in the same four beats, plus two '
                                         'unsorted scenarios to classify.'}],
               'channel_templates': [],
               'checkpoint_questions': [{'answer_index': 0,
                                         'id': 'module4-examples-cp1',
                                         'options': ['Goal, tool, check, stop',
                                                     'Name, brand, price, launch date',
                                                     'Search, summarize, send, repeat'],
                                         'prompt': 'Which four beats describe every agent in this '
                                                   'lesson?'},
                                        {'answer_index': 1,
                                         'id': 'module4-examples-cp2',
                                         'options': ['A human reading every line it writes',
                                                     'The test suite passing or failing',
                                                     'A second AI model watching the first'],
                                         'prompt': "What is the coding helper's built-in check?"},
                                        {'answer_index': 2,
                                         'id': 'module4-examples-cp3',
                                         'options': ['Narrow agents are cheaper to advertise',
                                                     'Narrow agents never make mistakes, so there '
                                                     'is nothing to check',
                                                     'A small territory can actually be checked, '
                                                     'so trust can accumulate'],
                                         'prompt': 'Why does narrow scope make an agent more '
                                                   'trustworthy?'}],
               'estimated_minutes': 8,
               'evaluation_cases': [],
               'evaluation_rubric': [],
               'guided_blocks': [{'analogy': 'It is the moment in a language course where you '
                                             'overhear a real conversation and realize you '
                                             'followed it.',
                                  'body': 'The test suite is the check, an automatic judge that '
                                          'comes with the job. Noticing that you could answer this '
                                          'yourself is the real content of this lesson: the '
                                          'toolkit from Lessons 1 to 5 reads real systems, not '
                                          'just Juno.',
                                  'predict_first': {'hint': 'What built-in judge does a codebase '
                                                            'already have that says pass or fail?',
                                                    'question': 'Before reading the examples: a '
                                                                "coding helper's job is 'fix the "
                                                                "failing test.' What would its "
                                                                'check be? You genuinely have '
                                                                'enough to answer this now.'},
                                  'title': 'Read one agent with your own toolkit'},
                                 {'body': 'Goal, tool, check, stop. The same four beats describe '
                                          'all four agents. Read the scenario cards below once, '
                                          'watching the beats repeat. Agents differ in territory, '
                                          'not in anatomy.',
                                  'checkpoint_after': True,
                                  'title': 'Four beats, four agents',
                                  'try_this': ['Open the scenario cards and read all four. One '
                                               'pass, no note-taking needed.']},
                                 {'body': 'In every example, find the human: sending the support '
                                          'reply, confirming the meeting, reviewing the research. '
                                          'Real agents are designed with a person at the edge of '
                                          'their territory. In Modules 6 and 8, that placement '
                                          'becomes a setting you write down.',
                                  'remember': 'Every good agent has a human standing at its '
                                              'border.',
                                  'title': 'Where the human stands'},
                                 {'body': 'Broad agents demo well and work badly: their territory '
                                          'is too large to check, so trust never accumulates. If a '
                                          'product claims to do everything, you now know what to '
                                          "ask it: what's the check, and where's the stop?",
                                  'kind': 'common_mistake',
                                  'remember': 'Useful does not need to mean flashy. Narrow, '
                                              'checkable, trusted, in that order.',
                                  'title': "The 'everything helper' trap"},
                                 {'body': 'Pick your favorite of the four agents and give its four '
                                          'beats from memory. One agent, four sentences, done. All '
                                          'four would be rehearsal, and rehearsal is not required.',
                                  'kind': 'teach_it_back',
                                  'title': 'Say it back, once',
                                  'try_this': ["One agent only. Choosing the one you'd most want "
                                               'to exist is encouraged.']}],
               'lesson_type': 'theory',
               'permission_matrix': [],
               'questions': [{'answer_index': 2,
                              'id': 'module4-examples-q1',
                              'options': ['Displaying a stored FAQ answer whenever a matching '
                                          'keyword appears in a question',
                                          'Showing the current temperature from a weather feed',
                                          'Researching a topic: search, judge sources, draft, '
                                          'verify claims, revise'],
                              'prompt': 'Which task most clearly needs an agent rather than an '
                                        'answerer?'},
                             {'answer_index': 0,
                              'id': 'module4-examples-q2',
                              'options': ['Test results feed back into what it tries next',
                                          'It is written in a programming language',
                                          'It runs several test files at once'],
                              'prompt': 'The coding helper runs tests, reads the failure, adjusts '
                                        'the code, runs tests again. What makes this an agent '
                                        'rather than a script?'},
                             {'answer_index': 1,
                              'id': 'module4-examples-q3',
                              'options': ["The agent's tools cannot technically send email",
                                          'Sending is the risky, outward-facing step, so it sits '
                                          'with a person by design',
                                          'Customers dislike automated replies, so a person is '
                                          'kept visible at the end'],
                              'prompt': 'In the support-helper example, why does a human send the '
                                        'reply instead of the agent?'},
                             {'answer_index': 2,
                              'id': 'module4-examples-q4',
                              'options': ['Goal: the request was too ambiguous to act on',
                                          'Judgment: the model simply thought incorrectly about '
                                          'which slot was free',
                                          'Tools or memory: stale calendar data, or the first '
                                          'booking was never recorded'],
                              'prompt': 'The scheduling helper books the same room twice for two '
                                        'people. Which parts are the prime suspects?'},
                             {'answer_index': 0,
                              'id': 'module4-examples-q5',
                              'options': ['Narrow scope is easier to check, and checkable is what '
                                          'earns trust',
                                          'Broad agents overwhelm their users with too many '
                                          'options and settings',
                                          'Narrow agents use less electricity'],
                              'prompt': "Why is 'books meeting rooms only' often a better first "
                                        "agent than 'helps with everything'?"}],
               'safety_checks': [],
               'skill_templates': [],
               'slug': 'examples-of-real-ai-agents',
               'title': 'Four Agents You Already Understand'},
              {'ai_tutor_prompt': 'You are the AgentCraft course tutor for the lesson "Design Your '
                                  'Own Juno (On Paper)".\n'
                                  '\n'
                                  'Who you are teaching: an intelligent adult beginner with zero '
                                  'AI background. Assume they can think clearly. Never assume they '
                                  'know jargon. Introduce every technical word with a '
                                  'plain-English anchor the first time it appears.\n'
                                  '\n'
                                  'How to behave:\n'
                                  '- Attempt-first: before explaining, ask what they currently '
                                  'think, then build on their own words.\n'
                                  '- One idea per reply. End every reply with the single next '
                                  'step, never a menu of options.\n'
                                  "- Use the course's running example (Juno, the research helper) "
                                  'before inventing new examples.\n'
                                  '- If the learner answers correctly and then asks whether they '
                                  'are really sure, confirm once in one plain sentence and move '
                                  'forward. Do not reopen a settled point. Re-explaining a correct '
                                  'answer teaches doubt.\n'
                                  '- If they are wrong, name what was right first, then give the '
                                  'one adjustment.\n'
                                  '- Never dramatize risk. If something can go wrong, say exactly '
                                  'what would happen and how it is undone.\n'
                                  '- Never use em dashes in your replies.\n'
                                  '- When the learner can do what the lesson\'s "Done means done" '
                                  'list asks, say so plainly and tell them it is safe to stop.\n'
                                  '\n'
                                  'Focus for this lesson: guiding the learner to a finished '
                                  'four-box blueprint: one goal, one tool, one memory, one check '
                                  'plus stop. Enforce smallness kindly. A blueprint is finished '
                                  'when each box holds one honest sentence; when it does, say so '
                                  'and close the module warmly.\n',
               'artifacts': [{'change_prompt': 'Fill in the empty blueprint with your own four '
                                               'sentences. When all four boxes are full, you are '
                                               'done.',
                              'format': 'text',
                              'inspect_prompt': "Read Juno's example blueprint and notice that "
                                                'every box is one plain sentence. That is the '
                                                'target amount of polish.',
                              'path': 'lesson_artifacts/agents/first-agent-blueprint.md',
                              'summary': "The four-box blueprint worksheet: Juno's filled-in "
                                         'example, an empty copy, and the finish-line '
                                         'definition.'}],
               'channel_templates': [],
               'checkpoint_questions': [{'answer_index': 0,
                                         'id': 'module4-activity-cp1',
                                         'options': ['Goal, one tool, one memory, one check + stop',
                                                     'Name, logo, price, launch plan',
                                                     'Model, dataset, server, budget'],
                                         'prompt': 'What are the four boxes of the blueprint?'},
                                        {'answer_index': 1,
                                         'id': 'module4-activity-cp2',
                                         'options': ['When it has been rewritten until no better '
                                                     'wording exists',
                                                     'When each box holds one honest sentence and '
                                                     'it reads in thirty seconds',
                                                     'When it lists every tool the agent could '
                                                     'ever need'],
                                         'prompt': 'When is the blueprint finished?'},
                                        {'answer_index': 2,
                                         'id': 'module4-activity-cp3',
                                         'options': ['It is graded against other students\' '
                                                     'blueprints',
                                                     'It must be memorized before starting',
                                                     'It gets rebuilt with real tools. Changing '
                                                     'then is expected'],
                                         'prompt': 'What happens to the blueprint in Module 6?'}],
               'estimated_minutes': 15,
               'evaluation_cases': [],
               'evaluation_rubric': [],
               'guided_blocks': [{'analogy': 'This is the napkin drawing before the house. Nobody '
                                             'inspects a napkin for building-code violations.',
                                  'body': 'None of those. It is a first plan, and you know what '
                                          'this course thinks of first plans: starting points, not '
                                          "promises. Today's only job is a sketch with four honest "
                                          'sentences.',
                                  'predict_first': {'hint': 'Think about what Lesson 3 said about '
                                                            'first plans.',
                                                    'question': 'What do you think happens to this '
                                                                'blueprint after today: is it '
                                                                'graded, kept, or built exactly as '
                                                                'written?'},
                                  'title': 'Before you design: the pressure valve'},
                                 {'body': 'Goal first: one specific irritation from your real '
                                          'week. Then the single tool that goal needs most, the '
                                          'single thing worth remembering, and one check plus one '
                                          'stop. Every box after the first is easier because the '
                                          'goal is specific.',
                                  'checkpoint_after': True,
                                  'title': 'Fill the four boxes, in order',
                                  'try_this': ["Open the worksheet below. Read Juno's filled-in "
                                               'example once.',
                                               'Fill your four boxes, one sentence each. A '
                                               'ten-minute timer helps you stop tinkering.']},
                                 {'body': 'Read your blueprint out loud, once, timed. Under thirty '
                                          'seconds and understandable? It is the right size. Over '
                                          'thirty seconds usually means the goal box is hiding two '
                                          "jobs. Keep the one you'd want first; the other can be "
                                          'its own agent someday.',
                                  'remember': 'One breath, one job, one agent.',
                                  'title': 'The thirty-second read'},
                                 {'body': 'The riskiest moment of this lesson is after the boxes '
                                          'are full, when the urge arrives to reword everything '
                                          'until it is perfect. The finish line was defined before '
                                          'you started: four honest sentences, thirty-second read. '
                                          'Past it, the blueprint is finished. Revising a finished '
                                          "sketch is Module 6's job, not tonight's.",
                                  'kind': 'common_mistake',
                                  'remember': 'Finished was defined in advance. You are allowed to '
                                              'believe it.',
                                  'title': 'The polish trap'},
                                 {'body': 'Read your four sentences to someone: a friend, a rubber '
                                          "duck, the room. That is the module's teach-it-back and "
                                          'the last thing Module 4 asks of you. Everything here '
                                          'returns in later modules, carried forward by the '
                                          'course, not by your memory.',
                                  'kind': 'teach_it_back',
                                  'title': 'Close the module',
                                  'try_this': ['One read-aloud. Then close the page. Genuinely '
                                               'done.']}],
               'lesson_type': 'interactive',
               'permission_matrix': [],
               'questions': [{'answer_index': 2,
                              'id': 'module4-activity-q1',
                              'options': ['It needs a catchier product name',
                                          'It never says which customers it serves or which '
                                          'languages it must support',
                                          'It is too vague to tell you what tool, memory, or stop '
                                          'rule the agent needs'],
                              'prompt': "A blueprint's goal box says 'AI will handle customer "
                                        "questions.' What is the actual problem with it?"},
                             {'answer_index': 0,
                              'id': 'module4-activity-q2',
                              'options': ['Tools should follow from the goal: a tool list without '
                                          'a goal means the purpose is not clear yet',
                                          'Eight is fine, since a thorough blueprint lists every '
                                          'tool that might ever help the agent someday',
                                          'The tools simply need to be listed in alphabetical '
                                          'order'],
                              'prompt': 'A blueprint lists eight tools before the goal box is '
                                        'filled in. What has gone wrong?'},
                             {'answer_index': 1,
                              'id': 'module4-activity-q3',
                              'options': ['The agent will refuse to start until a check and a stop '
                                          'rule are added',
                                          'It can deliver unverified work and never know when it '
                                          'is finished',
                                          'The goal will drift as the agent runs'],
                              'prompt': 'A blueprint has a clear goal and a good tool but no check '
                                        'and no stop. What risk is built in?'},
                             {'answer_index': 2,
                              'id': 'module4-activity-q4',
                              'options': ["'An AI that helps with everything in my life': one "
                                          'assistant covering every need beats many small ones',
                                          "'An AI that reads the entire internet daily': more "
                                          'information means better answers',
                                          "'An AI that tells me which fridge items expire this "
                                          "week, from a list I keep': one job, one tool, natural "
                                          'stop'],
                              'prompt': 'Which is the stronger first blueprint?'},
                             {'answer_index': 2,
                              'id': 'module4-activity-q5',
                              'options': ['Add more technical vocabulary so it sounds rigorous',
                                          'Find a more attentive friend',
                                          'Shrink the goal until it fits in one breath'],
                              'prompt': 'You read your blueprint to a friend and they cannot say '
                                        'what it does. What is the most likely fix?'}],
               'safety_checks': [],
               'skill_templates': [],
               'slug': 'design-your-first-agent',
               'title': 'Design Your Own Juno (On Paper)'}],
  'order': 5,
  'publish_rules': ['requires_non_placeholder_content',
                    'requires_tutor_prompts',
                    'requires_valid_quiz_banks',
                    'requires_guided_blocks',
                    'requires_checkpoint_banks',
                    'requires_agent_learning_artifacts'],
  'slug': 'module-4-ai-agents',
  'title': 'Module 4: How Agents Think'},
 {'description': 'Give the agent you designed a real home: set up OpenClaw the official way, teach '
                 'it three skills, open one front door, and run the built-in safety sweep. '
                 'Everything is reversible, and one command always tells you the system is '
                 'healthy.',
  'difficulty': 2,
  'lessons': [{'ai_tutor_prompt': 'You are the AgentCraft course tutor for the lesson "Set Up the '
                                  'Home Base".\n'
                                  '\n'
                                  'Who you are teaching: an intelligent adult beginner with zero '
                                  'AI background. Assume they can think clearly. Never assume they '
                                  'know jargon. Introduce every technical word with a '
                                  'plain-English anchor the first time it appears.\n'
                                  '\n'
                                  'How to behave:\n'
                                  '- Attempt-first: start by asking what they have already '
                                  'configured, drafted, or tried, then build on their own words.\n'
                                  '- One idea per reply. End every reply with the single next '
                                  'step, never a menu of options.\n'
                                  '- Keep the learner moving toward the deliverable: a healthy '
                                  'OpenClaw gateway and a working grasp of the three files '
                                  '(control panel, job description, recipe card).\n'
                                  "- Use the course's running example (Juno, the research helper "
                                  'from Module 4) when an example is needed.\n'
                                  '- If the learner answers correctly and then asks whether they '
                                  'are really sure, confirm once in one plain sentence and move '
                                  'forward. Do not reopen a settled point. Re-explaining a correct '
                                  'answer teaches doubt.\n'
                                  '- If they are wrong or stuck, name what was right first, then '
                                  'give the one adjustment. Being stuck is information, never a '
                                  'verdict.\n'
                                  '- Never dramatize risk. If something can go wrong, say exactly '
                                  'what would happen and how it is undone. Prefer "here is the '
                                  'command that checks this for you" over lists of things to worry '
                                  'about.\n'
                                  '- Never use em dashes in your replies.\n'
                                  "- If they already have a draft, review it against the lesson's "
                                  'finish line instead of replacing their work.\n'
                                  '- When the learner can do what the lesson\'s "Done means done" '
                                  'list asks, say so plainly and tell them it is safe to stop.\n'
                                  '\n'
                                  'Focus for this lesson: the official onboarding path (install, '
                                  'onboard, status), the gateway status command as the one health '
                                  'check they can always trust, and routing problems to the right '
                                  'file: openclaw.json for how it runs, SOUL.md for who it is.\n',
               'artifacts': [{'change_prompt': 'Replace the model placeholder with the provider '
                                               'and model you would try first. One edit is the '
                                               'whole exercise.',
                              'format': 'text',
                              'inspect_prompt': 'Find the model line, the DM session setting, and '
                                                'the sandbox mode. Say in plain English what each '
                                                'one controls.',
                              'path': 'lesson_artifacts/openclaw/config/openclaw.json.template.json5',
                              'summary': 'The nearly-empty starter control panel: a model line and '
                                         'two safe defaults, with plain-English comments.'},
                             {'change_prompt': 'Rewrite the Mission line in your own words, as if '
                                               'writing a job ad for a very reliable intern.',
                              'format': 'text',
                              'inspect_prompt': 'Read the Mission and Rules sections. Would a '
                                                'stranger know what this assistant is for?',
                              'path': 'lesson_artifacts/openclaw/config/SOUL.md',
                              'summary': 'A starter job description (SOUL.md) for a study-buddy '
                                         'research assistant, modeled on Juno.'},
                             {'change_prompt': 'Mark which steps you could do today. Any unmarked '
                                               'step is simply the next thing, not a problem.',
                              'format': 'text',
                              'inspect_prompt': 'Notice the order: health is proven before '
                                                'anything is added, and channels come last. Say '
                                                'why that ordering is kind to the builder.',
                              'path': 'lesson_artifacts/openclaw/config/onboard-checklist.md',
                              'summary': 'The setup path as a finite checklist: install, onboard, '
                                         'status, then one layer at a time.'}],
               'channel_templates': [],
               'checkpoint_questions': [{'answer_index': 0,
                                         'id': 'openclaw-config-cp1',
                                         'options': ['SOUL.md',
                                                     'openclaw.json',
                                                     'The daemon settings'],
                                         'prompt': 'You want to change who the assistant is. Which '
                                                   'file?'},
                                        {'answer_index': 2,
                                         'id': 'openclaw-config-cp2',
                                         'options': ['The workspace SOUL.md file',
                                                     "A skill's SKILL.md file",
                                                     '~/.openclaw/openclaw.json'],
                                         'prompt': 'Which file is the runtime control panel?'},
                                        {'answer_index': 1,
                                         'id': 'openclaw-config-cp3',
                                         'options': ['openclaw skills update --all',
                                                     'openclaw gateway status',
                                                     'openclaw pairing approve'],
                                         'prompt': "Which command answers 'is everything okay?' "
                                                   'after a change?'}],
               'estimated_minutes': 15,
               'evaluation_cases': [],
               'evaluation_rubric': [],
               'guided_blocks': [{'analogy': 'Control panel, job description, recipe card, front '
                                             'desk. Four objects. That is the entire building.',
                                  'body': 'OpenClaw is the office; your assistant is the worker '
                                          'inside it. The Gateway is the front desk that keeps the '
                                          'office open. `openclaw.json` is the control panel, '
                                          '`SOUL.md` is the job description, and each `SKILL.md` '
                                          'is a recipe card. Every question in this module routes '
                                          'to one of those four things.',
                                  'predict_first': {'hint': 'One file is a control panel. One is a '
                                                            'job description. The whole trick is '
                                                            'never confusing them.',
                                                    'question': 'You are setting up an assistant '
                                                                'on your own computer. Two things '
                                                                'need configuring: who the '
                                                                'assistant is, and the system that '
                                                                'keeps it running. Which do you '
                                                                'think lives in which file?'},
                                  'title': 'The office, not the worker'},
                                 {'body': 'Before touching any command, take one walk through the '
                                          "map below. It is a picture of the assistant's home, not "
                                          'your real computer, so clicking cannot change or break '
                                          'anything. Every file shows its plain name, its job, and '
                                          'whether you will ever need to touch it. Three files '
                                          'carry stars. When you have opened all three, this step '
                                          'is done.',
                                  'interactive_widget': 'openclaw_file_explorer',
                                  'title': 'Walk through the home',
                                  'try_this': ['Click the three starred files and read each card '
                                               'once.',
                                               'Say which starred file you would open if the '
                                               'assistant sounded rude.']},
                                 {'artifact_paths': ['lesson_artifacts/openclaw/config/onboard-checklist.md'],
                                  'body': 'Install, onboard, status. The onboarding wizard asks '
                                          'its questions in the right order so you do not have to '
                                          'know the order. Then `openclaw gateway status` gives '
                                          "you your first 'healthy.' That word is the finish line "
                                          'for this block.',
                                  'remember': "One run of each command is enough. 'Healthy' means "
                                              'healthy.',
                                  'title': 'Three commands, one pass',
                                  'try_this': ['Open the onboarding checklist below and read it '
                                               'once, noticing that channels come last on '
                                               'purpose.']},
                                 {'artifact_paths': ['lesson_artifacts/openclaw/config/openclaw.json.template.json5',
                                                     'lesson_artifacts/openclaw/config/SOUL.md'],
                                  'body': 'Wrong model: control panel (`openclaw.json`). Wrong '
                                          'personality: job description (`SOUL.md`). Wrong way of '
                                          'doing one task: recipe card (`SKILL.md`). Practice that '
                                          "routing three times and this lesson's hardest idea is "
                                          'permanently yours.',
                                  'checkpoint_after': True,
                                  'title': 'The routing rule',
                                  'try_this': ['Open the control panel template and find the model '
                                               'line.',
                                               'Open SOUL.md and find the Mission line.',
                                               'Say which file you would touch if the assistant '
                                               'were rude, and which if it used the wrong model.']},
                                 {'body': 'Everyone briefly mixes up the control panel and the job '
                                          'description; the names are new. Nothing is broken when '
                                          "it happens. Ask 'is this about how the system runs, or "
                                          "who the assistant is?' and the answer routes you. "
                                          'Nothing to memorize.',
                                  'kind': 'common_mistake',
                                  'remember': 'How it runs: openclaw.json. Who it is: SOUL.md.',
                                  'title': 'If the two files blur together'},
                                 {'body': "A classmate asks, 'Why are there so many files?' Your "
                                          'answer: one file runs the system, one describes the '
                                          'worker, one teaches a task, and one command tells you '
                                          'the whole thing is healthy. Say that once and this '
                                          'lesson is finished.',
                                  'kind': 'teach_it_back',
                                  'title': 'Say it back, once',
                                  'try_this': ["Say it once, using 'control panel, job "
                                               "description, recipe card' if the names help."]}],
               'lesson_type': 'agent_lab',
               'permission_matrix': [],
               'questions': [{'answer_index': 0,
                              'id': 'openclaw-config-q1',
                              'options': ['Run openclaw onboard first: it sets up the gateway and '
                                          'workspace in the right order before any hand-editing',
                                          'They are right: onboarding is just a convenience for '
                                          'people who are not comfortable editing files',
                                          'openclaw.json cannot be edited by hand at all'],
                              'prompt': "A colleague says: 'Skip onboarding. Just open "
                                        "openclaw.json and start editing.' What is the gentle "
                                        'correction?'},
                             {'answer_index': 1,
                              'id': 'openclaw-config-q2',
                              'options': ['In SOUL.md: the job description covers everything about '
                                          'the assistant, including its model',
                                          'In ~/.openclaw/openclaw.json: the control panel decides '
                                          'how the system runs, including the model',
                                          'In a SKILL.md file: skills choose the model'],
                              'prompt': "You edit SOUL.md to change your assistant's personality, "
                                        'but it still uses the wrong AI model. Where does the '
                                        'model actually live?'},
                             {'answer_index': 2,
                              'id': 'openclaw-config-q3',
                              'options': ['Every skill is installed, verified, and ready for the '
                                          'assistant to use in every channel',
                                          'All channels are connected and approved',
                                          'The gateway is running and can talk to your model: the '
                                          'foundation is solid to build on'],
                              'prompt': 'openclaw gateway status reports healthy. What exactly do '
                                        'you now know?'},
                             {'answer_index': 0,
                              'id': 'openclaw-config-q4',
                              'options': ['SOUL.md: the job description defines identity, tone, '
                                          'and rules',
                                          'openclaw.json: personality lives in the runtime '
                                          'settings',
                                          'The daemon logs: personality is set at install time'],
                              'prompt': "Someone's assistant works fine but sounds completely "
                                        'wrong for its role. Which file is the first place to '
                                        'look?'},
                             {'answer_index': 2,
                              'id': 'openclaw-config-q5',
                              'options': ['Add everything at once: seeing the full system working '
                                          'together is the fastest way to learn it',
                                          'Channels must come first or the gateway will not start',
                                          'Prove the gateway healthy first, then add one layer at '
                                          'a time, so you always know which layer changed'],
                              'prompt': 'A student wants to add every channel and skill on day '
                                        'one, before running anything. What is the better path, '
                                        'and why?'}],
               'safety_checks': ['Deny-by-default tool access',
                                 'Human review for destructive operations',
                                 'Run receipts persisted to disk'],
               'skill_templates': [],
               'slug': 'configuration',
               'title': 'Set Up the Home Base'},
              {'ai_tutor_prompt': 'You are the AgentCraft course tutor for the lesson "Teach It '
                                  'Skills".\n'
                                  '\n'
                                  'Who you are teaching: an intelligent adult beginner with zero '
                                  'AI background. Assume they can think clearly. Never assume they '
                                  'know jargon. Introduce every technical word with a '
                                  'plain-English anchor the first time it appears.\n'
                                  '\n'
                                  'How to behave:\n'
                                  '- Attempt-first: start by asking what they have already '
                                  'configured, drafted, or tried, then build on their own words.\n'
                                  '- One idea per reply. End every reply with the single next '
                                  'step, never a menu of options.\n'
                                  '- Keep the learner moving toward the deliverable: three '
                                  'understood skills (research-brief, channel-policy-check, '
                                  'security-audit-helper) and a working grasp of SKILL.md, the '
                                  'closest-wins rule, and install-then-verify.\n'
                                  "- Use the course's running example (Juno, the research helper "
                                  'from Module 4) when an example is needed.\n'
                                  '- If the learner answers correctly and then asks whether they '
                                  'are really sure, confirm once in one plain sentence and move '
                                  'forward. Do not reopen a settled point. Re-explaining a correct '
                                  'answer teaches doubt.\n'
                                  '- If they are wrong or stuck, name what was right first, then '
                                  'give the one adjustment. Being stuck is information, never a '
                                  'verdict.\n'
                                  '- Never dramatize risk. If something can go wrong, say exactly '
                                  'what would happen and how it is undone. Prefer "here is the '
                                  'command that checks this for you" over lists of things to worry '
                                  'about.\n'
                                  '- Never use em dashes in your replies.\n'
                                  "- If they already have a draft, review it against the lesson's "
                                  'finish line instead of replacing their work.\n'
                                  '- When the learner can do what the lesson\'s "Done means done" '
                                  'list asks, say so plainly and tell them it is safe to stop.\n'
                                  '\n'
                                  'Focus for this lesson: the SKILL.md format as a readable recipe '
                                  'card, the one-sentence precedence rule (closest to the project '
                                  'wins), and verify as the built-in checker that carries the '
                                  'trust question for the learner.\n',
               'artifacts': [{'change_prompt': 'Rewrite the description so a friend could predict '
                                               'what the skill does without reading the body.',
                              'format': 'text',
                              'inspect_prompt': 'Find the name, the description, and the sentence '
                                                'that keeps the summary honest about unknowns.',
                              'path': 'lesson_artifacts/openclaw/skills/research-brief/SKILL.md',
                              'summary': "Juno's core trick as a real skill file: turn sources "
                                         'into a short, honest, cited brief.'},
                             {'change_prompt': 'Add one sentence reminding the agent to check that '
                                               'shared rooms only answer when called by name.',
                              'format': 'text',
                              'inspect_prompt': 'Find the lines that compare a plan against '
                                                'policy. What mistake is this skill built to '
                                                'catch?',
                              'path': 'lesson_artifacts/openclaw/skills/channel-policy-check/SKILL.md',
                              'summary': 'A skill that double-checks door settings before a '
                                         'channel goes live.'},
                             {'change_prompt': "Add a sentence telling the agent to put 'open "
                                               "access plus tools enabled' at the top of any list "
                                               'it makes.',
                              'format': 'text',
                              'inspect_prompt': 'Find how findings get grouped. Why does a grouped '
                                                'list feel more finishable than a raw dump?',
                              'path': 'lesson_artifacts/openclaw/skills/security-audit-helper/SKILL.md',
                              'summary': 'A skill that turns safety-sweep findings into a short, '
                                         'ordered to-do list.'}],
               'channel_templates': [],
               'checkpoint_questions': [{'answer_index': 1,
                                         'id': 'openclaw-skills-cp1',
                                         'options': ['skill.py', 'SKILL.md', 'skills.json'],
                                         'prompt': 'What filename does OpenClaw discover as a '
                                                   'skill?'},
                                        {'answer_index': 0,
                                         'id': 'openclaw-skills-cp2',
                                         'options': ['The one closest to the current project',
                                                     'The one installed most recently',
                                                     'The one with more lines'],
                                         'prompt': 'Two skills share a name. Which wins?'},
                                        {'answer_index': 2,
                                         'id': 'openclaw-skills-cp3',
                                         'options': ['Reading it makes the skill load faster',
                                                     'OpenClaw refuses to load any skill until it '
                                                     'detects the file has been opened and read',
                                                     'It contains instructions your assistant will '
                                                     "follow: a stranger's recipe deserves one "
                                                     'read'],
                                         'prompt': 'Why read a downloaded skill before trusting '
                                                   'it?'}],
               'estimated_minutes': 12,
               'evaluation_cases': [],
               'evaluation_rubric': [],
               'guided_blocks': [{'analogy': 'A skill is a recipe card taped next to a machine. '
                                             'The machine is the capability; the card says when to '
                                             'use it and what good work looks like.',
                                  'body': 'It is a recipe card in plain language: a name, a '
                                          'description, and instructions. Open research-brief '
                                          'below and read all of it. It takes under a minute, and '
                                          'that readability is the point: you can always know '
                                          'exactly what your assistant has been taught.',
                                  'predict_first': {'hint': 'You have already seen its shape in '
                                                            'Module 4, on paper.',
                                                    'question': 'Before opening it: what do you '
                                                                "expect the inside of a 'skill' to "
                                                                'look like? Code, settings, or '
                                                                'something else?'},
                                  'title': 'Open one and read it',
                                  'try_this': ["Open research-brief's SKILL.md below. Read the "
                                               'whole thing once.']},
                                 {'body': 'If two skills share a name, the one closest to your '
                                          'current project wins. That sentence is the complete '
                                          'rule for this course. The longer priority list in the '
                                          'docs can stay unread until a real collision sends you '
                                          'there.',
                                  'remember': 'Closest wins.',
                                  'title': 'The collision rule, whole'},
                                 {'body': 'For skills from ClawHub: install fetches it, `verify` '
                                          'runs the built-in checker on its trust record, and then '
                                          'you read it once. After those three steps the trust '
                                          'question is settled and does not need reopening.',
                                  'checkpoint_after': True,
                                  'title': 'Fetch, verify, read, trust',
                                  'try_this': ['Say what problem `verify` solves, in one sentence, '
                                               "using the stranger's-recipe idea."]},
                                 {'artifact_paths': ['lesson_artifacts/openclaw/skills/research-brief/SKILL.md',
                                                     'lesson_artifacts/openclaw/skills/channel-policy-check/SKILL.md',
                                                     'lesson_artifacts/openclaw/skills/security-audit-helper/SKILL.md'],
                                  'body': "research-brief does Juno's job. channel-policy-check "
                                          'and security-audit-helper do something lovelier: they '
                                          'check the system for you. One reviews door settings, '
                                          'one turns audit findings into a to-do list. From its '
                                          'very first week, your assistant participates in keeping '
                                          'itself trustworthy.',
                                  'remember': 'A small set you can vouch for beats a catalog you '
                                              "can't.",
                                  'title': 'Your trio, and what it says'},
                                 {'body': 'The usual cause is mundane: the filename is not exactly '
                                          'SKILL.md, or the file sits one folder too deep. Check '
                                          'those two things in that order and the mystery is '
                                          'nearly always solved. A non-loading skill cannot harm '
                                          'anything; it is simply not seen.',
                                  'kind': 'common_mistake',
                                  'remember': 'Exact filename, right folder. Two checks, in order, '
                                              'then done.',
                                  'title': "If a skill doesn't load"},
                                 {'body': "A friend asks, 'So how does your assistant know how to "
                                          "do things?' Answer with the recipe-card story: readable "
                                          'file, closest wins, verify before trusting strangers. '
                                          'Three beats, once through, lesson finished.',
                                  'kind': 'teach_it_back',
                                  'title': 'Say it back, once',
                                  'try_this': ['Say the three beats out loud or in your head. '
                                               'Once.']}],
               'lesson_type': 'agent_lab',
               'permission_matrix': [],
               'questions': [{'answer_index': 1,
                              'id': 'openclaw-skills-q1',
                              'options': ['The gateway must be restarted twice after adding text '
                                          'files',
                                          'Skills are discovered by their exact filename: it must '
                                          'be SKILL.md',
                                          'Text files need to be registered in openclaw.json '
                                          'first'],
                              'prompt': 'You write skill instructions in a file called '
                                        'skills-info.txt inside workspace/skills/. OpenClaw '
                                        'ignores it. Why?'},
                             {'answer_index': 0,
                              'id': 'openclaw-skills-q2',
                              'options': ['The workspace one: closest to the current project wins',
                                          'The home-folder one: personal skills always win',
                                          'Whichever file was edited most recently'],
                              'prompt': 'The same skill name exists in your project workspace and '
                                        'in your home folder. Which one runs?'},
                             {'answer_index': 2,
                              'id': 'openclaw-skills-q3',
                              'options': ['Restart the gateway so the skill loads immediately',
                                          'Delete any lines in it that look unfamiliar',
                                          'Run openclaw skills verify, then read the skill once '
                                          'yourself'],
                              'prompt': 'You install a skill from ClawHub. What is the recommended '
                                        'next step before trusting it?'},
                             {'answer_index': 1,
                              'id': 'openclaw-skills-q4',
                              'options': ['Markdown files can slow down the gateway noticeably',
                                          'A skill is instructions your assistant will follow: '
                                          'text can steer real actions, so it deserves a read',
                                          'Nothing: markdown cannot contain executable code, so '
                                          'the worst case is a badly written recipe'],
                              'prompt': "A teammate says: 'Third-party skills are just markdown, "
                                        "not code. Nothing to review.' What are they missing?"},
                             {'answer_index': 2,
                              'id': 'openclaw-skills-q5',
                              'options': ['OpenClaw workspaces support at most three skills, so '
                                          'the course simply uses that limit',
                                          'The other skills on ClawHub cost money, and this course '
                                          'avoids paid material',
                                          'Three understood skills build capability; fifty '
                                          'installed ones build clutter you cannot vouch for'],
                              'prompt': 'Why does this module teach exactly three skills instead '
                                        'of a catalog of fifty?'}],
               'safety_checks': ['Verify ClawHub skills before trusting them',
                                 'Use allowlists when only specific agents should see a skill'],
               'skill_templates': ['research-brief',
                                   'channel-policy-check',
                                   'security-audit-helper'],
               'slug': 'adding-skills',
               'title': 'Teach It Skills'},
              {'ai_tutor_prompt': 'You are the AgentCraft course tutor for the lesson "Open the '
                                  'Front Door (Just a Crack)".\n'
                                  '\n'
                                  'Who you are teaching: an intelligent adult beginner with zero '
                                  'AI background. Assume they can think clearly. Never assume they '
                                  'know jargon. Introduce every technical word with a '
                                  'plain-English anchor the first time it appears.\n'
                                  '\n'
                                  'How to behave:\n'
                                  '- Attempt-first: start by asking what they have already '
                                  'configured, drafted, or tried, then build on their own words.\n'
                                  '- One idea per reply. End every reply with the single next '
                                  'step, never a menu of options.\n'
                                  '- Keep the learner moving toward the deliverable: one connected '
                                  'channel on pairing, with the learner able to explain the three '
                                  'door policies and the two shared-room settings.\n'
                                  "- Use the course's running example (Juno, the research helper "
                                  'from Module 4) when an example is needed.\n'
                                  '- If the learner answers correctly and then asks whether they '
                                  'are really sure, confirm once in one plain sentence and move '
                                  'forward. Do not reopen a settled point. Re-explaining a correct '
                                  'answer teaches doubt.\n'
                                  '- If they are wrong or stuck, name what was right first, then '
                                  'give the one adjustment. Being stuck is information, never a '
                                  'verdict.\n'
                                  '- Never dramatize risk. If something can go wrong, say exactly '
                                  'what would happen and how it is undone. Prefer "here is the '
                                  'command that checks this for you" over lists of things to worry '
                                  'about.\n'
                                  '- Never use em dashes in your replies.\n'
                                  "- If they already have a draft, review it against the lesson's "
                                  'finish line instead of replacing their work.\n'
                                  '- When the learner can do what the lesson\'s "Done means done" '
                                  'list asks, say so plainly and tell them it is safe to stop.\n'
                                  '\n'
                                  'Focus for this lesson: the locked-by-default reassurance '
                                  '(pairing is the default; open requires two deliberate steps), '
                                  'the doorbell, guest list, and propped-door picture, '
                                  'requireMention for groups, and per-person conversation '
                                  'notebooks. A one-channel, one-person rollout is complete, not '
                                  'preliminary.\n',
               'artifacts': [{'change_prompt': 'Pick the one channel you would connect first and '
                                               'say why pairing already suits it.',
                              'format': 'text',
                              'inspect_prompt': 'Find the DM policy, the DM scope, and the mention '
                                                'rule. Say what each protects, in doorbell terms.',
                              'path': 'lesson_artifacts/openclaw/channels/channel-policy.template.json5',
                              'summary': 'A door-policy template with pairing, mention gating, and '
                                         'private per-person sessions, commented in plain '
                                         'English.'},
                             {'change_prompt': 'Fill in the channel name you would actually use. '
                                               'That single word makes the checklist yours.',
                              'format': 'text',
                              'inspect_prompt': 'Count the steps. Notice the last one is a finish '
                                                'line, not an invitation to widen access.',
                              'path': 'lesson_artifacts/openclaw/channels/rollout-checklist.md',
                              'summary': 'The complete first rollout on an index card: one '
                                         'channel, pairing, one person, one test message.'}],
               'channel_templates': ['slack-rollout', 'telegram-rollout'],
               'checkpoint_questions': [{'answer_index': 1,
                                         'id': 'openclaw-channel-cp1',
                                         'options': ['Open',
                                                     'Pairing',
                                                     'No policy until you set one'],
                                         'prompt': 'What is the default DM policy on a new '
                                                   'channel?'},
                                        {'answer_index': 0,
                                         'id': 'openclaw-channel-cp2',
                                         'options': ['The assistant only answers when called by '
                                                     'name',
                                                     'The assistant leaves the room after each '
                                                     'answer',
                                                     'The assistant messages members privately '
                                                     'instead'],
                                         'prompt': 'In a group room, what does requireMention do?'},
                                        {'answer_index': 2,
                                         'id': 'openclaw-channel-cp3',
                                         'options': ['When the gateway runs without a daemon',
                                                     'When one person messages the assistant from '
                                                     'two different personal devices',
                                                     'When several people can DM the same '
                                                     'assistant and each needs a private thread'],
                                         'prompt': 'When do per-channel-peer sessions matter '
                                                   'most?'}],
               'estimated_minutes': 12,
               'evaluation_cases': [],
               'evaluation_rubric': [],
               'guided_blocks': [{'analogy': 'Channel policy is deciding who gets a house key, who '
                                             'can ring the bell, and who the house simply does not '
                                             'answer.',
                                  'body': 'A short code and silence. That is the whole experience '
                                          'of an unapproved stranger. Connecting a channel opens '
                                          'nothing by itself; approval is a separate, deliberate '
                                          'act that only you can perform.',
                                  'predict_first': {'hint': 'The designers assumed strangers would '
                                                            'try. What is the safest default reply '
                                                            'to someone unknown?',
                                                    'question': 'You connect your assistant to a '
                                                                'messaging app. Before you approve '
                                                                'anyone, what do you think a '
                                                                'stranger who messages it '
                                                                'experiences?'},
                                  'title': 'The locked front door'},
                                 {'body': 'Pairing is a doorbell with a code: you approve ring by '
                                          'ring. Allowlist is a guest list fixed in advance. Open '
                                          'is the door propped for anyone; it exists for real '
                                          'public bots and requires typing two unmistakable '
                                          'settings. For everything in this course, the doorbell '
                                          'is correct, and it is already switched on.',
                                  'checkpoint_after': True,
                                  'remember': 'Pairing is the default and the right answer here. '
                                              'Leaving it alone is the correct move.',
                                  'title': 'Doorbell, guest list, propped door'},
                                 {'artifact_paths': ['lesson_artifacts/openclaw/channels/channel-policy.template.json5'],
                                  'body': 'requireMention makes the assistant a polite group '
                                          'member: silent until called by name. per-channel-peer '
                                          'gives every DM sender a private notebook. The template '
                                          'below has both written out; reading it is enough, and '
                                          'applying it is copy-paste.',
                                  'title': 'Polite in groups, private in DMs',
                                  'try_this': ['Open the template and find the two settings. Say '
                                               'in one sentence each what they protect.']},
                                 {'artifact_paths': ['lesson_artifacts/openclaw/channels/rollout-checklist.md'],
                                  'body': 'One channel, pairing on, one approved person (you), one '
                                          'test message answered. That is a correct production '
                                          'pattern in miniature, and the checklist below fits on '
                                          'an index card. Wider access is always a later choice, '
                                          'never a debt.',
                                  'remember': 'A good rollout is boring: small, tested, easy to '
                                              'explain.',
                                  'title': 'A complete first rollout is small'},
                                 {'body': 'Someday a use case will make the open policy sound '
                                          "tempting. When that day comes, ask: 'who exactly do I "
                                          "want reaching this assistant, and can I name them?' If "
                                          'you can name them, pairing or an allowlist already '
                                          'serves you better. A truly public bot is a project to '
                                          'design deliberately, not a switch to flip.',
                                  'kind': 'common_mistake',
                                  'remember': "If you can name the people, you don't need 'open'.",
                                  'title': "If 'open' ever starts to sound convenient"},
                                 {'body': "Explain to an imaginary teammate why 'just let anyone "
                                          "DM the bot' is not the move: the doorbell, the guest "
                                          'list, the propped door, and what a stranger experiences '
                                          'by default. Four beats, once through, and Lesson 3 is '
                                          'done.',
                                  'kind': 'teach_it_back',
                                  'title': 'Say it back, once',
                                  'try_this': ["Include the phrase 'a code and silence'. It "
                                               'carries most of the story.']}],
               'lesson_type': 'interactive',
               'permission_matrix': [],
               'questions': [{'answer_index': 1,
                              'id': 'openclaw-channel-q1',
                              'options': ['The assistant answers politely but declines anything '
                                          'that sounds risky or personal',
                                          'They receive a pairing code and otherwise silence, '
                                          'until you approve them',
                                          'The message is delivered to you for manual reply'],
                              'prompt': 'A stranger messages your freshly connected assistant. '
                                        'With default settings, what happens?'},
                             {'answer_index': 0,
                              'id': 'openclaw-channel-q2',
                              'options': ['openclaw pairing approve <channel> <code>',
                                          'openclaw gateway restart --approve',
                                          "Reply 'approve' to their message from your own account"],
                              'prompt': 'How do you approve a sender who received a pairing code?'},
                             {'answer_index': 2,
                              'id': 'openclaw-channel-q3',
                              'options': ['It happens gradually as you approve more senders over '
                                          'time',
                                          'Approving your first sender quietly switches the whole '
                                          'channel to the open policy',
                                          'Two deliberate, explicit settings typed on purpose. It '
                                          'cannot happen by accident'],
                              'prompt': "What does it take to actually make DMs public (the 'open' "
                                        'policy)?'},
                             {'answer_index': 0,
                              'id': 'openclaw-channel-q4',
                              'options': ['It answers only when called by name, instead of '
                                          'reacting to every message',
                                          'It hides the assistant from members who have not paired',
                                          'It disables message logging inside the group so the '
                                          'chatter stays private'],
                              'prompt': 'Your assistant joins a team group chat. What does '
                                        'requireMention change?'},
                             {'answer_index': 1,
                              'id': 'openclaw-channel-q5',
                              'options': ['The assistant merges all three conversations into one '
                                          'shared thread it can search',
                                          'Each person gets a separate conversation notebook: no '
                                          'context blurs between them',
                                          'Only the first person to pair may send DMs'],
                              'prompt': 'Three people DM the same assistant. What do '
                                        'per-channel-peer sessions guarantee?'}],
               'safety_checks': ['Keep DM policy on pairing unless a real reason exists',
                                 'Enable mention gating in shared rooms'],
               'skill_templates': [],
               'slug': 'channel',
               'title': 'Open the Front Door (Just a Crack)'},
              {'ai_tutor_prompt': 'You are the AgentCraft course tutor for the lesson "The Safety '
                                  'Sweep".\n'
                                  '\n'
                                  'Who you are teaching: an intelligent adult beginner with zero '
                                  'AI background. Assume they can think clearly. Never assume they '
                                  'know jargon. Introduce every technical word with a '
                                  'plain-English anchor the first time it appears.\n'
                                  '\n'
                                  'How to behave:\n'
                                  '- Attempt-first: start by asking what they have already '
                                  'configured, drafted, or tried, then build on their own words.\n'
                                  '- One idea per reply. End every reply with the single next '
                                  'step, never a menu of options.\n'
                                  '- Keep the learner moving toward the deliverable: a passed '
                                  'security audit and the three-layer picture: doors (identity), '
                                  'rooms (scope), person inside (model), in that order.\n'
                                  "- Use the course's running example (Juno, the research helper "
                                  'from Module 4) when an example is needed.\n'
                                  '- If the learner answers correctly and then asks whether they '
                                  'are really sure, confirm once in one plain sentence and move '
                                  'forward. Do not reopen a settled point. Re-explaining a correct '
                                  'answer teaches doubt.\n'
                                  '- If they are wrong or stuck, name what was right first, then '
                                  'give the one adjustment. Being stuck is information, never a '
                                  'verdict.\n'
                                  '- Never dramatize risk. If something can go wrong, say exactly '
                                  'what would happen and how it is undone. Prefer "here is the '
                                  'command that checks this for you" over lists of things to worry '
                                  'about.\n'
                                  '- Never use em dashes in your replies.\n'
                                  "- If they already have a draft, review it against the lesson's "
                                  'finish line instead of replacing their work.\n'
                                  '- When the learner can do what the lesson\'s "Done means done" '
                                  'list asks, say so plainly and tell them it is safe to stop.\n'
                                  '\n'
                                  'Focus for this lesson: reframing safety as settings rather than '
                                  'vigilance: the audit holds the checklist so the learner does '
                                  'not have to; the rhythm is change, audit, fix, done, and '
                                  're-running on an unchanged system yields nothing new. The locks '
                                  'work without anyone watching.\n',
               'artifacts': [{'change_prompt': 'Pick the one line you find most reassuring and say '
                                               'why it holds even when nobody is watching.',
                              'format': 'text',
                              'inspect_prompt': 'Find the gateway bind, the auth mode, the exec '
                                                'setting, and the DM scope. Say what each one '
                                                'locks, in house terms.',
                              'path': 'lesson_artifacts/openclaw/safety/hardened-openclaw.json5',
                              'summary': 'A hardened baseline config: every lock from the module '
                                         'in one file, commented in plain English.'},
                             {'change_prompt': 'Read the runbook as a spoken checklist once. If it '
                                               'fits in one breath per line, it is doing its job.',
                              'format': 'text',
                              'inspect_prompt': 'Find the sentence about re-running the audit on '
                                                'an unchanged system. Say why that sentence is a '
                                                'gift.',
                              'path': 'lesson_artifacts/openclaw/safety/security-audit-runbook.md',
                              'summary': 'The audit rhythm on one page: change, audit, fix, done, '
                                         'with what a flag means and does not mean.'}],
               'channel_templates': [],
               'checkpoint_questions': [{'answer_index': 1,
                                         'id': 'openclaw-safety-cp1',
                                         'options': ['Many mutually untrusting users per gateway',
                                                     'One trusted operator per gateway',
                                                     'Trust is negotiated per message'],
                                         'prompt': 'What trust model does an OpenClaw gateway '
                                                   'assume?'},
                                        {'answer_index': 0,
                                         'id': 'openclaw-safety-cp2',
                                         'options': ['Who can talk, and where it can act',
                                                     "The assistant's tone of voice",
                                                     'The size of the model'],
                                         'prompt': 'What comes before model behavior in the '
                                                   'layered safety order?'},
                                        {'answer_index': 2,
                                         'id': 'openclaw-safety-cp3',
                                         'options': ['Audit hourly regardless of changes',
                                                     'Audit once at install time, never again',
                                                     'Change something, audit, fix flags, done'],
                                         'prompt': 'What is the audit rhythm from this lesson?'}],
               'estimated_minutes': 12,
               'evaluation_cases': [],
               'evaluation_rubric': [],
               'guided_blocks': [{'analogy': 'Doors, rooms, person inside. Identity, scope, model. '
                                             'Set in that order, checked by one auditor.',
                                  'body': 'They were safety work, done calmly, one layer at a '
                                          'time. This lesson only adds the top layer: an auditor '
                                          'that checks all of it at once. You are not starting '
                                          'safety today; you are finishing it.',
                                  'predict_first': {'hint': 'Each one was a machine holding a '
                                                            "checklist so you didn't have to.",
                                                    'question': 'Look back at Lessons 1 to 3: the '
                                                                'health check, the verify command, '
                                                                'the locked doors. What were all '
                                                                'of those, really?'},
                                  'title': "You've been doing this all module"},
                                 {'body': 'The layered order means the important protections are '
                                          'settings, not behavior. A door on pairing holds whether '
                                          'the model has a good day or a bad one, whether you are '
                                          'watching or asleep. Nothing in this system asks for '
                                          'your vigilance; it asks for one command after each '
                                          'change.',
                                  'remember': 'A prompt is guidance. A setting is enforcement. '
                                              'Enforcement does not need supervision.',
                                  'title': "Locks beat promises, and that's a relief"},
                                 {'artifact_paths': ['lesson_artifacts/openclaw/safety/hardened-openclaw.json5',
                                                     'lesson_artifacts/openclaw/safety/security-audit-runbook.md'],
                                  'body': 'Change something. Run `openclaw security audit`. Fix '
                                          'what it flags. Done. The audit holds the full checklist '
                                          'internally, which is why you do not have to, and why a '
                                          'pass is a real answer. An unchanged system re-audited '
                                          'gives the same result, so the discipline is once per '
                                          'change, then put it down.',
                                  'checkpoint_after': True,
                                  'title': 'The audit rhythm',
                                  'try_this': ['Read the runbook once. Notice it is a rhythm, not '
                                               'a worry list.',
                                               'In the hardened config, find the sandbox line and '
                                               'say what it keeps away from the master key.']},
                                 {'body': 'OpenClaw assumes one trusted operator per gateway. It '
                                          'is a personal assistant, like a personal home. If '
                                          'mutually untrusting people ever need assistants, they '
                                          'get separate gateways. You are the only operator here, '
                                          'so this boundary asks nothing of you today.',
                                  'remember': 'One home, one household. More households, more '
                                              'homes.',
                                  'title': 'One household, named once'},
                                 {'body': 'A flag is the system working: the auditor caught what '
                                          'it exists to catch, before anything happened. Findings '
                                          'arrive ordered. Fix the top one, re-run, watch the list '
                                          'shrink. A first audit with a few flags is the normal '
                                          'experience, and the security-audit-helper skill from '
                                          'Lesson 2 will turn the output into a to-do list for '
                                          'you.',
                                  'kind': 'common_mistake',
                                  'remember': 'A flag means the check worked. Fix, re-run, shrink '
                                              'the list, done.',
                                  'title': 'If the audit flags something'},
                                 {'body': 'Four beats: who can talk (doors), where it can act '
                                          '(rooms), how it behaves (person inside), and the '
                                          'auditor that checks the building. Say them once. Then '
                                          'let Module 6 be finished. It is, and the config files '
                                          'will hold everything exactly as you left it.',
                                  'kind': 'teach_it_back',
                                  'title': 'Say it back, and close the module',
                                  'try_this': ['One pass through the four beats. Then close the '
                                               'page. The module is complete.']}],
               'lesson_type': 'theory',
               'permission_matrix': [{'action': 'read_repo',
                                      'level': 'allow',
                                      'reason': 'needed for lesson and artifact work'},
                                     {'action': 'write_artifact',
                                      'level': 'allow',
                                      'reason': 'course-owned learning artifacts'},
                                     {'action': 'gateway',
                                      'level': 'review',
                                      'reason': 'persistent control-plane changes deserve a '
                                                'deliberate yes'},
                                     {'action': 'cron',
                                      'level': 'review',
                                      'reason': 'scheduled workflows persist beyond one chat turn'},
                                     {'action': 'public_exposure_change',
                                      'level': 'deny',
                                      'reason': 'outside Module 6 lesson scope'}],
               'questions': [{'answer_index': 1,
                              'id': 'openclaw-safety-q1',
                              'options': ['The teammate: a well-written prompt reaches the model '
                                          'directly, making hard controls redundant',
                                          'You: settings (identity, scope) come first because they '
                                          'hold regardless of how the model behaves',
                                          'Neither: the ordering between prompts and controls does '
                                          'not matter'],
                              'prompt': 'A teammate wants to rely on a strongly-worded system '
                                        'prompt for safety. You want the doors and rooms set '
                                        'first. Who has the official ordering right?'},
                             {'answer_index': 0,
                              'id': 'openclaw-safety-q2',
                              'options': ['The door: lock down who can talk before tuning anything '
                                          'else',
                                          'The model: add stronger instructions about strangers',
                                          'The tools: remove them all, then revisit the door '
                                          'later'],
                              'prompt': "The audit flags: 'DM policy open + tools enabled.' What "
                                        'does the layered order say to fix first?'},
                             {'answer_index': 2,
                              'id': 'openclaw-safety-q3',
                              'options': ['It catches issues that can appear spontaneously while '
                                          'the system sits overnight',
                                          "It refreshes the gateway's security certificates",
                                          'Nothing new: same system in, same answer out. Once per '
                                          'change is the whole discipline'],
                              'prompt': 'You ran the audit after your last change and it passed. '
                                        'Nothing has changed since. What does running it again '
                                        'tonight accomplish?'},
                             {'answer_index': 1,
                              'id': 'openclaw-safety-q4',
                              'options': ["channels.dmPolicy: 'allowlist'",
                                          "agents.defaults.sandbox.mode: 'non-main'",
                                          "gateway.bind: 'public'"],
                              'prompt': 'You want sessions other than your own kept away from full '
                                        'access to your computer. Which setting is built for '
                                        'exactly that?'},
                             {'answer_index': 0,
                              'id': 'openclaw-safety-q5',
                              'options': ['Two separate gateways: separate homes, separate keys',
                                          'One shared gateway with a strict SOUL.md',
                                          'One gateway, taking turns by day of the week'],
                              'prompt': 'Two housemates who do not fully trust each other both '
                                        'want assistants. What does the one-household rule '
                                        'recommend?'}],
               'safety_checks': ['Run openclaw security audit after config changes',
                                 'Use sandboxing for non-main or shared sessions',
                                 'Keep high-risk tools denied by default in untrusted contexts',
                                 'Treat third-party skills and plugins as untrusted code'],
               'skill_templates': [],
               'slug': 'agent-safety',
               'title': 'The Safety Sweep'}],
  'order': 8,
  'publish_rules': ['requires_non_placeholder_content',
                    'requires_tutor_prompts',
                    'requires_valid_quiz_banks',
                    'requires_openclaw_artifacts',
                    'requires_skill_templates',
                    'requires_channel_templates',
                    'requires_safety_checks'],
  'slug': 'module-6-openclaw',
  'title': 'Module 6: Build Your Assistant a Home (OpenClaw)'},
 {'description': 'The finishing module: let your assistant run one small job on its own, put '
                 'guardrails and permissions around it, gather four kinds of evidence, and make a '
                 'clear, final release decision. This module ends with a decision, not a feeling.',
  'difficulty': 3,
  'lessons': [{'ai_tutor_prompt': 'You are the AgentCraft course tutor for the lesson "Work That '
                                  'Runs While You\'re Away".\n'
                                  '\n'
                                  'Who you are teaching: an intelligent adult beginner with zero '
                                  'AI background. Assume they can think clearly. Never assume they '
                                  'know jargon. Introduce every technical word with a '
                                  'plain-English anchor the first time it appears.\n'
                                  '\n'
                                  'How to behave:\n'
                                  '- Attempt-first: start by asking what they have already '
                                  'configured, drafted, or tried, then build on their own words.\n'
                                  '- One idea per reply. End every reply with the single next '
                                  'step, never a menu of options.\n'
                                  '- Keep the learner moving toward the deliverable: a four-line '
                                  'automation brief: trigger, steps, review point, receipt.\n'
                                  "- Use the course's running example (Juno, the research helper "
                                  'from Module 4) when an example is needed.\n'
                                  '- If the learner answers correctly and then asks whether they '
                                  'are really sure, confirm once in one plain sentence and move '
                                  'forward. Do not reopen a settled point. Re-explaining a correct '
                                  'answer teaches doubt.\n'
                                  '- If they are wrong or stuck, name what was right first, then '
                                  'give the one adjustment. Being stuck is information, never a '
                                  'verdict.\n'
                                  '- Never dramatize risk. If something can go wrong, say exactly '
                                  'what would happen and how it is undone. Prefer "here is the '
                                  'command that checks this for you" over lists of things to worry '
                                  'about.\n'
                                  '- Never use em dashes in your replies.\n'
                                  "- If they already have a draft, review it against the lesson's "
                                  'finish line instead of replacing their work.\n'
                                  '- When the learner can do what the lesson\'s "Done means done" '
                                  'list asks, say so plainly and tell them it is safe to stop.\n'
                                  '\n'
                                  'Focus for this lesson: the four questions of trustworthy '
                                  'automation, with the receipt as the emotional center: '
                                  'verification by reading a record afterward, not by watching. '
                                  'Connect each question back to the Module 4 blueprint so this '
                                  'feels like growth, not new ground.\n',
               'artifacts': [{'change_prompt': 'Fill the empty brief with your own automation. '
                                               'Four honest lines and it is finished.',
                              'format': 'text',
                              'inspect_prompt': 'Read the filled example. Notice every answer is '
                                                'one line. That is the target amount of detail.',
                              'path': 'lesson_artifacts/capstone/automation-brief.template.md',
                              'summary': 'The four-question automation brief, with the '
                                         'Monday-audit example filled in and an empty copy for '
                                         'yours.'},
                             {'change_prompt': 'Renumber the sequence for your own automation from '
                                               'the brief. Same beats, your job.',
                              'format': 'text',
                              'inspect_prompt': 'Find the step where a human decides, and the step '
                                                'where the record gets written.',
                              'path': 'lesson_artifacts/capstone/task-flow-sequence.md',
                              'summary': 'One automation drawn as a numbered sequence, showing '
                                         'exactly where the human and the receipt sit.'}],
               'channel_templates': [],
               'checkpoint_questions': [{'answer_index': 0,
                                         'id': 'capstone-automation-cp1',
                                         'options': ['Trigger, steps, review point, receipt',
                                                     'Model, prompt, speed, cost',
                                                     'Install, onboard, status, audit'],
                                         'prompt': 'What are the four questions of a trustworthy '
                                                   'automation?'},
                                        {'answer_index': 1,
                                         'id': 'capstone-automation-cp2',
                                         'options': ['The trigger',
                                                     'The receipt',
                                                     'The review point'],
                                         'prompt': 'Which piece proves a run happened after the '
                                                   'fact?'},
                                        {'answer_index': 2,
                                         'id': 'capstone-automation-cp3',
                                         'options': ['With the fastest available tool',
                                                     'Wherever the model decides in the moment',
                                                     'With a person, at the review point'],
                                         'prompt': 'Where does the irreversible step belong in all '
                                                   'three worked examples?'}],
               'estimated_minutes': 12,
               'evaluation_cases': [],
               'evaluation_rubric': [],
               'guided_blocks': [{'analogy': 'An automation is an assembly line with a '
                                             'quality-control station and a logbook, not a '
                                             'self-driving mystery box.',
                                  'body': 'Whatever you just listed maps onto the four questions: '
                                          "instructions are the steps, limits and 'call me if' are "
                                          'the review point, and finding out afterward is the '
                                          'receipt. Trustworthy automation is a well-arranged '
                                          'house-sit. The calm comes from the arrangement, not '
                                          'from hope.',
                                  'predict_first': {'hint': 'Clear instructions, agreed limits, a '
                                                            'note about when to call you, and '
                                                            'finding out afterward what happened.',
                                                    'question': 'You let a capable person '
                                                                'house-sit for a weekend. What '
                                                                'arrangements would let you '
                                                                'genuinely not think about the '
                                                                'house while away?'},
                                  'title': 'Stepping away, calmly'},
                                 {'artifact_paths': ['lesson_artifacts/capstone/automation-brief.template.md',
                                                     'lesson_artifacts/capstone/task-flow-sequence.md'],
                                  'body': "Trigger, steps, review, receipt. These are Module 4's "
                                          'goal, tools, check, and stop wearing work clothes. The '
                                          'brief template below holds one line for each. When the '
                                          'four lines are written, the brief is done.',
                                  'checkpoint_after': True,
                                  'title': "Four questions, and where you've seen them",
                                  'try_this': ['Open the brief template and read the filled-in '
                                               'Monday-audit example.',
                                               'Sketch your own automation as four lines. Rough '
                                               'counts as complete.']},
                                 {'body': "The receipt converts 'did it work?' from an open "
                                          'question into a lookup. That is the whole reason '
                                          'automation can be restful. Design rule worth keeping '
                                          'forever: no receipt, no automation. You deserve to be '
                                          'able to find out rather than wonder.',
                                  'remember': 'A receipt turns wondering into looking something '
                                              'up.',
                                  'title': 'The receipt, once more'},
                                 {'body': "The tempting shortcut is 'the model will just handle "
                                          "it.' But an unbounded step cannot be reviewed, and an "
                                          'unreviewed step cannot be trusted. The bar: mechanical '
                                          'enough that another person could follow the steps. That '
                                          'bar is kind to everyone, including future you.',
                                  'kind': 'common_mistake',
                                  'remember': 'If you cannot draw the steps, the design is not '
                                              'done yet. Five minutes usually fixes it.',
                                  'title': 'The mystery-box trap'},
                                 {'body': 'Explain the Monday audit to an imaginary friend in four '
                                          'short sentences: what starts it, what it does, where '
                                          'you decide, what it leaves behind. Once through, and '
                                          'this lesson is finished.',
                                  'kind': 'teach_it_back',
                                  'title': 'Say it back, once',
                                  'try_this': ['Use trigger, steps, review, receipt as your four '
                                               'sentence-starters.']}],
               'lesson_type': 'theory',
               'permission_matrix': [],
               'questions': [{'answer_index': 0,
                              'id': 'capstone-automation-q1',
                              'options': ['The receipt: a written record you read afterward',
                                          'The trigger: knowing when it started',
                                          'The model: trusting it was a good one'],
                              'prompt': 'What lets you verify an unattended run without having '
                                        'watched it?'},
                             {'answer_index': 1,
                              'id': 'capstone-automation-q2',
                              'options': ['The doorbell-to-draft, fired by a form submission',
                                          'The Monday audit, fired at 9:00 every Monday',
                                          'A reply the assistant writes while you watch'],
                              'prompt': 'Which example is a schedule-triggered automation?'},
                             {'answer_index': 2,
                              'id': 'capstone-automation-q3',
                              'options': ['Webhooks can start jobs but cannot technically complete '
                                          'a send on their own',
                                          'Drafting is too slow to automate end to end',
                                          'Sending is the irreversible step, so it sits with a '
                                          'person: the review point'],
                              'prompt': 'In the doorbell-to-draft example, why does the draft wait '
                                        'for your approval instead of sending itself?'},
                             {'answer_index': 1,
                              'id': 'capstone-automation-q4',
                              'options': ['The trigger: cleanup work needs to run far more often '
                                          'than once per night',
                                          "The steps are unbounded: 'the AI handles it' is not a "
                                          'list you could draw',
                                          'Nightly jobs cannot produce receipts'],
                              'prompt': "A design says: 'Trigger: nightly. Steps: the AI handles "
                                        "cleanup.' What fails the four questions?"},
                             {'answer_index': 2,
                              'id': 'capstone-automation-q5',
                              'options': ['A saved log of a completed run',
                                          'A rule about which tools an automation may use',
                                          "One system ringing another system's doorbell to start a "
                                          'job'],
                              'prompt': "What is a webhook, in this lesson's terms?"}],
               'safety_checks': ['Every workflow names a review boundary'],
               'skill_templates': [],
               'slug': 'automation-examples',
               'title': "Work That Runs While You're Away"},
              {'ai_tutor_prompt': 'You are the AgentCraft course tutor for the lesson "Guardrails: '
                                  'Values and Seatbelts".\n'
                                  '\n'
                                  'Who you are teaching: an intelligent adult beginner with zero '
                                  'AI background. Assume they can think clearly. Never assume they '
                                  'know jargon. Introduce every technical word with a '
                                  'plain-English anchor the first time it appears.\n'
                                  '\n'
                                  'How to behave:\n'
                                  '- Attempt-first: start by asking what they have already '
                                  'configured, drafted, or tried, then build on their own words.\n'
                                  '- One idea per reply. End every reply with the single next '
                                  'step, never a menu of options.\n'
                                  '- Keep the learner moving toward the deliverable: a filled '
                                  'guardrail matrix where every safety claim points at a concrete, '
                                  'showable control.\n'
                                  "- Use the course's running example (Juno, the research helper "
                                  'from Module 4) when an example is needed.\n'
                                  '- If the learner answers correctly and then asks whether they '
                                  'are really sure, confirm once in one plain sentence and move '
                                  'forward. Do not reopen a settled point. Re-explaining a correct '
                                  'answer teaches doubt.\n'
                                  '- If they are wrong or stuck, name what was right first, then '
                                  'give the one adjustment. Being stuck is information, never a '
                                  'verdict.\n'
                                  '- Never dramatize risk. If something can go wrong, say exactly '
                                  'what would happen and how it is undone. Prefer "here is the '
                                  'command that checks this for you" over lists of things to worry '
                                  'about.\n'
                                  '- Never use em dashes in your replies.\n'
                                  "- If they already have a draft, review it against the lesson's "
                                  'finish line instead of replacing their work.\n'
                                  '- When the learner can do what the lesson\'s "Done means done" '
                                  'list asks, say so plainly and tell them it is safe to stop.\n'
                                  '\n'
                                  'Focus for this lesson: the two layers: values (helpful, '
                                  'truthful, harmless: what the assistant aims for) and seatbelts '
                                  '(settings that hold regardless), plus the one rule: every '
                                  'safety claim points at something you could show someone.\n',
               'artifacts': [{'change_prompt': 'Fill one row for your own build. A value, a '
                                               'setting, a pointer. One row is a complete '
                                               'exercise.',
                              'format': 'text',
                              'inspect_prompt': 'Read the filled example row. Notice the third '
                                                'column is always something you could open on a '
                                                'screen.',
                              'path': 'lesson_artifacts/capstone/guardrail-matrix.md',
                              'summary': 'The values-to-seatbelts matrix: each row pairs one aim '
                                         'with the concrete control that backs it, plus where to '
                                         'point.'}],
               'channel_templates': [],
               'checkpoint_questions': [{'answer_index': 0,
                                         'id': 'capstone-guardrails-cp1',
                                         'options': ['The seatbelt layer: settings and mechanisms',
                                                     'The value layer: helpful, truthful, harmless',
                                                     "Neither; both depend on the model's "
                                                     'behavior'],
                                         'prompt': "Which layer holds even on the model's bad "
                                                   'day?'},
                                        {'answer_index': 1,
                                         'id': 'capstone-guardrails-cp2',
                                         'options': ['It is written in a settings file, which the '
                                                     'assistant reads more carefully',
                                                     'It mechanically changes who can reach the '
                                                     'assistant, regardless of behavior',
                                                     "It improves the assistant's tone"],
                                         'prompt': "Why is 'dmPolicy: pairing' stronger than a "
                                                   'written promise to be careful?'},
                                        {'answer_index': 2,
                                         'id': 'capstone-guardrails-cp3',
                                         'options': ['Cite a published research paper',
                                                     'Use the words helpful, truthful, or harmless',
                                                     'Point at something concrete you could show '
                                                     'someone'],
                                         'prompt': 'What must every safety claim in the capstone '
                                                   'do?'}],
               'estimated_minutes': 10,
               'evaluation_cases': [],
               'evaluation_rubric': [{'criterion': 'helpfulness',
                                      'description': 'The workflow still moves the user toward a '
                                                     'useful result.',
                                      'weight': 2},
                                     {'criterion': 'truthfulness',
                                      'description': 'Claims are grounded, and unknowns are '
                                                     'labeled clearly.',
                                      'weight': 3},
                                     {'criterion': 'harmlessness',
                                      'description': 'Risky actions are denied, sandboxed, or '
                                                     'escalated.',
                                      'weight': 3},
                                     {'criterion': 'operational_control',
                                      'description': 'The concrete control backing each guardrail '
                                                     'is named explicitly.',
                                      'weight': 2}],
               'guided_blocks': [{'analogy': "Helpful, truthful, harmless is the driver's "
                                             'character. The Module 6 settings are the seatbelt, '
                                             'brakes, and doors.',
                                  'body': 'Values work like the careful driver: real, valuable, '
                                          'intention-based. Seatbelts work by mechanism: pairing, '
                                          'sandboxing, deny lists, receipts. They hold whether or '
                                          'not the day is going well. Your build already wears '
                                          'both. This lesson teaches you to say which is which.',
                                  'predict_first': {'hint': 'One works by intention. One works by '
                                                            'mechanism, regardless of intention.',
                                                    'question': 'A careful driver and a seatbelt '
                                                                'both make a car safer. What is '
                                                                'the difference in how each one '
                                                                'works, and which would you rather '
                                                                'not be without on the worst day?'},
                                  'title': 'Two layers, un-blurred'},
                                 {'artifact_paths': ['lesson_artifacts/capstone/guardrail-matrix.md'],
                                  'body': 'Practice the rule on one row of the matrix below: take '
                                          "'harmless' and point at the seatbelt backing it in your "
                                          'build, such as the deny-by-default tools or the '
                                          'sandbox. If you can put your finger on a setting, the '
                                          'claim is real. One row now; the rest are the same '
                                          'motion repeated.',
                                  'checkpoint_after': True,
                                  'title': 'Point at it',
                                  'try_this': ['Open the matrix and read the filled example row.',
                                               'Fill one row yourself: a value, its seatbelt, and '
                                               "where you'd point to show it."]},
                                 {'body': "A finished matrix retires the question 'is my project "
                                          "safe?' as a feeling and re-issues it as a short list of "
                                          'facts, each with a pointer. Lists can be read, '
                                          'finished, and set down. That is the entire payoff of '
                                          'this lesson, and it is durable.',
                                  'remember': 'Feelings need managing. Lists just need reading.',
                                  'title': 'From feeling to list'},
                                 {'body': 'The tempting belief is that a good enough model retires '
                                          "the seatbelt layer. It does not, because 'good' is a "
                                          'behavior and behavior varies, while a lock is a '
                                          'mechanism and mechanisms hold. Strong models plus '
                                          'strong settings is how every serious system is built.',
                                  'kind': 'common_mistake',
                                  'remember': 'Better models are welcome. The seatbelts stay on '
                                              'regardless. That is what makes them seatbelts.',
                                  'title': 'The good-model trap'},
                                 {'body': 'Two sentences: one naming a value your assistant aims '
                                          'for, one naming the seatbelt that backs it and where it '
                                          'lives. If both sentences point at real things, this '
                                          'lesson is finished.',
                                  'kind': 'teach_it_back',
                                  'title': 'Say it back, once',
                                  'try_this': ['Two sentences, one pass. Pointing at pairing or '
                                               'the sandbox is a perfect answer.']}],
               'lesson_type': 'theory',
               'permission_matrix': [],
               'questions': [{'answer_index': 1,
                              'id': 'capstone-guardrails-q1',
                              'options': ['Fast, cheap, autonomous',
                                          'Helpful, truthful, harmless',
                                          'Paired, sandboxed, logged'],
                              'prompt': 'Which trio names the value layer, what a good assistant '
                                        'aims to be?'},
                             {'answer_index': 0,
                              'id': 'capstone-guardrails-q2',
                              'options': ['Settings hold on the bad day, independent of how the '
                                          'model behaves',
                                          'Instructions expire after thirty days and must be '
                                          'reinforced',
                                          'Controls make the assistant measurably faster'],
                              'prompt': 'Why do well-instructed assistants still need '
                                        'seatbelt-layer controls?'},
                             {'answer_index': 2,
                              'id': 'capstone-guardrails-q3',
                              'options': ['A paragraph promising the assistant is careful',
                                          'A team belief that the model is trustworthy',
                                          'dmPolicy pairing plus a tool deny list for untrusted '
                                          'rooms'],
                              'prompt': 'Which of these is a real seatbelt rather than a mood?'},
                             {'answer_index': 0,
                              'id': 'capstone-guardrails-q4',
                              'options': ['Point at something you could show someone',
                                          'Be approved by two reviewers',
                                          "Appear in the assistant's job description"],
                              'prompt': 'The one rule of this lesson: every safety claim must do '
                                        'what?'},
                             {'answer_index': 1,
                              'id': 'capstone-guardrails-q5',
                              'options': ['A larger, more knowledgeable model that simply makes '
                                          'fewer factual mistakes',
                                          'A check that claims trace to sources and unknowns are '
                                          'labeled as unknowns',
                                          'A rule that answers stay under one paragraph'],
                              'prompt': "'Truthful' is backed by which kind of concrete support in "
                                        'a strong capstone?'}],
               'safety_checks': ['Map value-level goals to runtime controls',
                                 'Reject safety claims that point at nothing showable',
                                 'Keep an audit path for review decisions'],
               'skill_templates': [],
               'slug': 'guardrails',
               'title': 'Guardrails: Values and Seatbelts'},
              {'ai_tutor_prompt': 'You are the AgentCraft course tutor for the lesson '
                                  '"Permissions: Three Kinds of Doors".\n'
                                  '\n'
                                  'Who you are teaching: an intelligent adult beginner with zero '
                                  'AI background. Assume they can think clearly. Never assume they '
                                  'know jargon. Introduce every technical word with a '
                                  'plain-English anchor the first time it appears.\n'
                                  '\n'
                                  'How to behave:\n'
                                  '- Attempt-first: start by asking what they have already '
                                  'configured, drafted, or tried, then build on their own words.\n'
                                  '- One idea per reply. End every reply with the single next '
                                  'step, never a menu of options.\n'
                                  '- Keep the learner moving toward the deliverable: a short '
                                  'permission table: every action labeled allow, review, or deny, '
                                  'each with a one-line reason.\n'
                                  "- Use the course's running example (Juno, the research helper "
                                  'from Module 4) when an example is needed.\n'
                                  '- If the learner answers correctly and then asks whether they '
                                  'are really sure, confirm once in one plain sentence and move '
                                  'forward. Do not reopen a settled point. Re-explaining a correct '
                                  'answer teaches doubt.\n'
                                  '- If they are wrong or stuck, name what was right first, then '
                                  'give the one adjustment. Being stuck is information, never a '
                                  'verdict.\n'
                                  '- Never dramatize risk. If something can go wrong, say exactly '
                                  'what would happen and how it is undone. Prefer "here is the '
                                  'command that checks this for you" over lists of things to worry '
                                  'about.\n'
                                  '- Never use em dashes in your replies.\n'
                                  "- If they already have a draft, review it against the lesson's "
                                  'finish line instead of replacing their work.\n'
                                  '- When the learner can do what the lesson\'s "Done means done" '
                                  'list asks, say so plainly and tell them it is safe to stop.\n'
                                  '\n'
                                  'Focus for this lesson: the three doors (allow, review, deny), '
                                  'the sorting question (what happens if it goes wrong, and how '
                                  'easily is it undone?), and the calm of pre-decision: choices '
                                  'made once in writing so nothing is ever decided under '
                                  'pressure.\n',
               'artifacts': [{'change_prompt': 'Add one row for an action from your own automation '
                                               'brief. Action, door, reason. One line.',
                              'format': 'json',
                              'inspect_prompt': 'Read all six rows. It takes under a minute. '
                                                "Notice every reason traces back to 'how easily is "
                                                "it undone?'.",
                              'path': 'lesson_artifacts/capstone/permission-review.template.json',
                              'summary': 'The six-row permission table: each entry names an '
                                         'action, a door, and a one-line reason.'}],
               'channel_templates': [],
               'checkpoint_questions': [{'answer_index': 1,
                                         'id': 'capstone-permissions-cp1',
                                         'options': ['What happens if this action runs, and at what '
                                                     'time of day?',
                                                     'What happens if it goes wrong, and how '
                                                     'easily is it undone?',
                                                     'Which tool implements this action?'],
                                         'prompt': 'What question sorts actions into the three '
                                                   'doors?'},
                                        {'answer_index': 0,
                                         'id': 'capstone-permissions-cp2',
                                         'options': ['Review: a person opens the yellow door',
                                                     'Allow: persistence is routine',
                                                     'Deny: nothing may persist'],
                                         'prompt': 'Actions that persist beyond one conversation '
                                                   'get which door?'},
                                        {'answer_index': 2,
                                         'id': 'capstone-permissions-cp3',
                                         'options': ['At request time, weighing each case fresh',
                                                     'After an incident, during the retrospective',
                                                     'Once, in advance, in writing'],
                                         'prompt': 'When are the permission decisions made?'}],
               'estimated_minutes': 10,
               'evaluation_cases': [],
               'evaluation_rubric': [],
               'guided_blocks': [{'analogy': 'Three doors: green opens freely, yellow means knock '
                                             'and a person answers, locked stays locked no matter '
                                             'how hard anyone knocks.',
                                  'body': 'A permission table is decisions, prepaid. Every action '
                                          'was sorted while you were calm, so no request, however '
                                          'urgent it sounds, ever needs an in-the-moment judgment. '
                                          'The system consults the table, and so can you. Pressure '
                                          'never gets a vote.',
                                  'predict_first': {'hint': 'The decision is the same. The '
                                                            "pressure isn't.",
                                                    'question': 'Think of a decision that is easy '
                                                                'to make calmly in advance but '
                                                                'stressful to make in the moment. '
                                                                'What changes between those two '
                                                                'moments?'},
                                  'title': 'Decisions, prepaid'},
                                 {'artifact_paths': ['lesson_artifacts/capstone/permission-review.template.json'],
                                  'body': 'Run the sorting question over three real actions from '
                                          'your build: drafting a reply (undone in a keystroke), '
                                          'scheduling a weekly job (persists), making the '
                                          'assistant public (widens everything). Green, yellow, '
                                          'locked. Feel how quickly the question does the work.',
                                  'checkpoint_after': True,
                                  'title': 'Sort three actions',
                                  'try_this': ['Open the template and check your three labels '
                                               'against its entries.',
                                               'Find one entry you would explain differently, and '
                                               'say your version out loud.']},
                                 {'body': 'A finished permission table for this capstone is about '
                                          'six rows. That smallness is a feature twice: you can '
                                          'read the entire security posture in thirty seconds, and '
                                          'nothing important hides in the middle. Big systems earn '
                                          'trust with small, legible tables.',
                                  'remember': 'Six honest rows beat sixty vague ones.',
                                  'title': 'The whole table fits on a screen'},
                                 {'body': "The weak version of this lesson reads: 'be careful with "
                                          "admin actions.' It feels responsible while deciding "
                                          'nothing, so every real request still becomes an '
                                          'in-the-moment judgment, which is exactly the pressure '
                                          'the table exists to remove. If an entry does not name '
                                          'an action and a door, it is not an entry yet. Two more '
                                          'words usually fix it.',
                                  'kind': 'common_mistake',
                                  'remember': "Name the action, name the door. 'Careful' is not a "
                                              'door.',
                                  'title': 'The vague-caution trap'},
                                 {'body': 'Three sentences: one action you allow, one you review, '
                                          'one you deny, each with its reason. If all three '
                                          "reasons trace back to 'how easily is it undone?', the "
                                          'lesson has landed.',
                                  'kind': 'teach_it_back',
                                  'title': 'Say it back, once',
                                  'try_this': ['Three sentences, one pass. Borrowing the '
                                               "template's rows is allowed."]}],
               'lesson_type': 'theory',
               'permission_matrix': [{'action': 'draft_content',
                                      'level': 'allow',
                                      'reason': 'routine and undone in a keystroke'},
                                     {'action': 'score_against_rubric',
                                      'level': 'allow',
                                      'reason': 'read-only evaluation work'},
                                     {'action': 'gateway',
                                      'level': 'review',
                                      'reason': 'settings changes persist beyond the conversation'},
                                     {'action': 'cron',
                                      'level': 'review',
                                      'reason': 'scheduled jobs outlive the chat that created '
                                                'them'},
                                     {'action': 'delete_history',
                                      'level': 'deny',
                                      'reason': 'burns the receipts; checking must stay possible'},
                                     {'action': 'public_exposure_change',
                                      'level': 'deny',
                                      'reason': 'widens every door at once; outside capstone '
                                                'scope'}],
               'questions': [{'answer_index': 1,
                              'id': 'capstone-permissions-q1',
                              'options': ['Maximum convenience: allow everything reversible or not',
                                          'Least privilege: the smallest set that still lets the '
                                          'work happen',
                                          'Symmetry: equal numbers of allow, review, and deny'],
                              'prompt': 'What principle sizes the set of green (allow) doors?'},
                             {'answer_index': 0,
                              'id': 'capstone-permissions-q2',
                              'options': ['They persist beyond the moment, outliving the '
                                          'conversation that created them',
                                          'They are the most technically difficult actions, so '
                                          'mistakes are more likely',
                                          'They run slowly and need supervision for speed'],
                              'prompt': 'Why do gateway changes and scheduled (cron) jobs deserve '
                                        'the yellow door?'},
                             {'answer_index': 2,
                              'id': 'capstone-permissions-q3',
                              'options': ['History files are too large to delete safely',
                                          'Reviewers cannot evaluate deletion requests quickly '
                                          'enough to keep a yellow door practical',
                                          'It burns the receipts, destroying the very ability to '
                                          'check what happened'],
                              'prompt': 'Why is deleting history a locked door rather than a '
                                        'yellow one?'},
                             {'answer_index': 0,
                              'id': 'capstone-permissions-q4',
                              'options': ['It names a specific action, a door, and a one-line '
                                          'reason',
                                          'It advises general caution around admin actions',
                                          'It defers each case to whoever is available that day'],
                              'prompt': 'What makes a permission entry strong?'},
                             {'answer_index': 1,
                              'id': 'capstone-permissions-q5',
                              'options': ['Urgency upgrades the request one level, from the locked '
                                          'door up to the review door',
                                          'Nothing changes: the decision was made in advance, and '
                                          'urgency does not reopen it',
                                          'The assistant weighs the urgency and decides'],
                              'prompt': 'An urgent-sounding request arrives for a denied action. '
                                        'What does the table say happens?'}],
               'safety_checks': ['Least privilege by action',
                                 'Persistent control-plane actions require review'],
               'skill_templates': [],
               'slug': 'permissions',
               'title': 'Permissions: Three Kinds of Doors'},
              {'ai_tutor_prompt': 'You are the AgentCraft course tutor for the lesson "The Release '
                                  'Decision".\n'
                                  '\n'
                                  'Who you are teaching: an intelligent adult beginner with zero '
                                  'AI background. Assume they can think clearly. Never assume they '
                                  'know jargon. Introduce every technical word with a '
                                  'plain-English anchor the first time it appears.\n'
                                  '\n'
                                  'How to behave:\n'
                                  '- Attempt-first: start by asking what they have already '
                                  'configured, drafted, or tried, then build on their own words.\n'
                                  '- One idea per reply. End every reply with the single next '
                                  'step, never a menu of options.\n'
                                  '- Keep the learner moving toward the deliverable: a completed '
                                  'Capstone Studio: evidence gathered across all four layers, the '
                                  'finite checklist checked once, and a stated release-or-revise '
                                  'decision.\n'
                                  "- Use the course's running example (Juno, the research helper "
                                  'from Module 4) when an example is needed.\n'
                                  '- If the learner answers correctly and then asks whether they '
                                  'are really sure, confirm once in one plain sentence and move '
                                  'forward. Do not reopen a settled point. Re-explaining a correct '
                                  'answer teaches doubt.\n'
                                  '- If they are wrong or stuck, name what was right first, then '
                                  'give the one adjustment. Being stuck is information, never a '
                                  'verdict.\n'
                                  '- Never dramatize risk. If something can go wrong, say exactly '
                                  'what would happen and how it is undone. Prefer "here is the '
                                  'command that checks this for you" over lists of things to worry '
                                  'about.\n'
                                  '- Never use em dashes in your replies.\n'
                                  "- If they already have a draft, review it against the lesson's "
                                  'finish line instead of replacing their work.\n'
                                  '- When the learner can do what the lesson\'s "Done means done" '
                                  'list asks, say so plainly and tell them it is safe to stop.\n'
                                  '\n'
                                  'Focus for this lesson: matching evidence to question: facts to '
                                  'verifiers, judgment to humans, prose to the judge model, '
                                  'understanding to the quiz. The checklist is finite and each box '
                                  "is checked exactly once; 'revise' is the checks working, not a "
                                  'failure. When they decide, close the course warmly and '
                                  'completely.\n',
               'artifacts': [{'change_prompt': 'Add a fifth case from your own workflow: one '
                                               'input, one expected outcome.',
                              'format': 'json',
                              'inspect_prompt': 'Find the case that is supposed to be refused, and '
                                                'say why its refusal is the success condition.',
                              'path': 'lesson_artifacts/capstone/evaluation-cases.template.json',
                              'summary': 'Four test cases that knock on four different doors: '
                                         'pass, revise, stop, and stay-fixed.'},
                             {'change_prompt': 'Match one artifact from your capstone to its '
                                               'layer, and write that pairing in one line.',
                              'format': 'text',
                              'inspect_prompt': "For each layer, read the one-line 'what it "
                                                "answers.' Notice no layer overlaps another's "
                                                'question.',
                              'path': 'lesson_artifacts/capstone/evaluation-plan.md',
                              'summary': 'The four evidence layers on one page: which instrument '
                                         'answers which kind of question.'},
                             {'change_prompt': 'Check each box as your capstone earns it. When the '
                                               'last one is checked, decide, and be done.',
                              'format': 'text',
                              'inspect_prompt': 'Count the boxes. Notice the last line is a '
                                                'decision, not an invitation to start over.',
                              'path': 'lesson_artifacts/capstone/release-readiness-checklist.md',
                              'summary': 'The finite checklist: a fixed number of boxes, each '
                                         'checked exactly once, ending in a decision.'}],
               'capstone_assignment': {'review_questions': ['Would this workflow stay safe if '
                                                            'someone misunderstood one step?',
                                                            'Does a person approve before any '
                                                            'risky or persistent change?',
                                                            'Can I point to one receipt that would '
                                                            'prove a run happened?'],
                                       'risky_phrases': ['open to anyone',
                                                         'skip review',
                                                         'no human review',
                                                         'public by default'],
                                       'sections': [{'key': 'goal',
                                                     'label': 'Goal',
                                                     'min_length': 30,
                                                     'placeholder': 'Example: Review a proposed '
                                                                    'channel rollout before it '
                                                                    'goes live, so nothing opens '
                                                                    'wider than intended.',
                                                     'prompt': 'What one job does this workflow '
                                                               "do, and for whom? One breath's "
                                                               'worth is the right size.'},
                                                    {'key': 'trigger',
                                                     'label': 'Trigger',
                                                     'min_length': 20,
                                                     'placeholder': 'Example: A scheduled run '
                                                                    'every Monday at 9:00.',
                                                     'prompt': 'What starts it: a schedule, an '
                                                               'arriving message, or a webhook? '
                                                               'Name the one thing.'},
                                                    {'key': 'actions',
                                                     'label': 'Steps',
                                                     'min_length': 40,
                                                     'placeholder': 'Example: Read the draft plan, '
                                                                    'compare it against the door '
                                                                    'policy, write a review note '
                                                                    'for a person.',
                                                     'prompt': 'List the bounded steps after the '
                                                               'trigger fires: a list you could '
                                                               "draw, not 'the AI handles it.'"},
                                                    {'key': 'review_boundary',
                                                     'label': 'Review point',
                                                     'min_length': 25,
                                                     'placeholder': 'Example: A person approves '
                                                                    'any change to who can reach '
                                                                    'the assistant or which tools '
                                                                    'it holds.',
                                                     'prompt': 'Where does a person approve before '
                                                               'anything irreversible happens?'},
                                                    {'key': 'guardrails',
                                                     'label': 'Guardrails',
                                                     'min_length': 25,
                                                     'placeholder': "Example: Strangers can't "
                                                                    'trigger it (pairing), risky '
                                                                    'tools are denied, and every '
                                                                    'run leaves a receipt.',
                                                     'prompt': 'Name the seatbelts protecting this '
                                                               'workflow: settings you could show '
                                                               'someone, not intentions.'},
                                                    {'key': 'permissions',
                                                     'label': 'Permissions',
                                                     'min_length': 35,
                                                     'placeholder': 'Example: Reading and drafting '
                                                                    'are green doors. Gateway '
                                                                    'changes knock at the yellow '
                                                                    'door. Public exposure is '
                                                                    'locked.',
                                                     'prompt': 'Give each kind of action its door: '
                                                               "allowed freely, needs a person's "
                                                               'yes, or locked entirely.'},
                                                    {'key': 'evidence',
                                                     'label': 'Receipts and evidence',
                                                     'min_length': 25,
                                                     'placeholder': 'Example: Every run writes a '
                                                                    'log entry and a review note; '
                                                                    'surprises start at the most '
                                                                    'recent receipt.',
                                                     'prompt': 'What record proves a run happened, '
                                                               'and where would you look first if '
                                                               'one surprised you?'}],
                                       'summary': 'Write up your workflow in seven short sections, '
                                                  'run the checks, and make your release-or-revise '
                                                  'call. Each section wants a few honest '
                                                  'sentences. The finish line for each is written '
                                                  'into its prompt.',
                                       'title': 'Capstone Studio'},
               'channel_templates': [],
               'checkpoint_questions': [{'answer_index': 1,
                                         'id': 'capstone-testing-cp1',
                                         'options': ['The judge model',
                                                     'The verifier',
                                                     'Human review'],
                                         'prompt': "Facts like 'does this file exist' belong to "
                                                   'which instrument?'},
                                        {'answer_index': 0,
                                         'id': 'capstone-testing-cp2',
                                         'options': ['A person', 'The verifier', 'The quiz'],
                                         'prompt': "Questions of judgment, like 'is this rollout "
                                                   "plan sensible', go to whom?"},
                                        {'answer_index': 2,
                                         'id': 'capstone-testing-cp3',
                                         'options': ['A second verification pass over every box, '
                                                     'just to be safe',
                                                     'The checklist resets for the next session',
                                                     'The evidence phase is over: you read the '
                                                     'evidence and decide'],
                                         'prompt': 'What happens after the last checklist box is '
                                                   'checked?'}],
               'estimated_minutes': 15,
               'evaluation_cases': [{'expected': 'pass',
                                     'goal': 'A well-scoped workflow passes rubric and verifier '
                                             'checks',
                                     'name': 'positive'},
                                    {'expected': 'revise',
                                     'goal': 'Missing evidence or missing controls send the work '
                                             'back with a named gap',
                                     'name': 'negative'},
                                    {'expected': 'stop',
                                     'goal': 'An attempt to skip review is refused; the system '
                                             'fails closed',
                                     'name': 'adversarial'},
                                    {'expected': 'pass',
                                     'goal': 'A previously fixed risky configuration stays fixed '
                                             'after later edits',
                                     'name': 'regression'}],
               'evaluation_rubric': [{'criterion': 'helpfulness',
                                      'description': 'The workflow actually helps complete the '
                                                     'task.',
                                      'weight': 2},
                                     {'criterion': 'truthfulness',
                                      'description': 'Claims are supported or clearly marked '
                                                     'uncertain.',
                                      'weight': 3},
                                     {'criterion': 'harmlessness',
                                      'description': 'The workflow limits risky actions and fails '
                                                     'closed when needed.',
                                      'weight': 3},
                                     {'criterion': 'evaluation_fit',
                                      'description': 'Each piece of evidence comes from the '
                                                     'instrument that matches its question.',
                                      'weight': 2}],
               'guided_blocks': [{'analogy': 'Like a bridge inspection: nobody stands at the end '
                                             'squinting and hoping. The load tests either passed '
                                             "or they didn't, and the sign-off just records it.",
                                  'body': 'Done right, the moment is light. The evidence carried '
                                          'all the weight, gathered in four bounded kinds, one '
                                          'piece at a time. Deciding is just reading what it says. '
                                          'A heavy release decision usually means the evidence was '
                                          "skipped. Yours wasn't, so when the lightness comes, "
                                          'believe it.',
                                  'predict_first': {'hint': 'What if every hard question had '
                                                            'already been answered, one at a time, '
                                                            'before the moment arrived?',
                                                    'question': 'Picture the moment you decide '
                                                                "'release' or 'revise.' Do you "
                                                                'expect it to feel heavy or light, '
                                                                'and what would make the '
                                                                'difference?'},
                                  'title': 'Why the decision will feel small'},
                                 {'artifact_paths': ['lesson_artifacts/capstone/evaluation-cases.template.json',
                                                     'lesson_artifacts/capstone/evaluation-plan.md',
                                                     'lesson_artifacts/capstone/release-readiness-checklist.md'],
                                  'body': 'Facts: verifier. Judgment: human. Prose: judge model. '
                                          'Your understanding: quiz. Run that matching over your '
                                          'own capstone pieces in the Studio below. Each piece has '
                                          'exactly one right instrument, and feeling the fit is '
                                          'the skill.',
                                  'checkpoint_after': True,
                                  'interactive_widget': 'capstone_studio',
                                  'title': 'Match the instrument to the question',
                                  'try_this': ['Open the evaluation plan and match one of your '
                                               'artifacts to its evidence layer.',
                                               'Read the four test cases and find the one designed '
                                               'to be refused.']},
                                 {'body': 'Count the boxes on the release-readiness checklist: a '
                                          'fixed number, each checked exactly once. When the last '
                                          'box is done, the evidence phase is over. Re-checking a '
                                          'checked box adds no information, because nothing '
                                          'changed between the two looks. The checklist was built '
                                          'so you could trust it and set it down.',
                                  'remember': 'Checked once means checked. The last box is a real '
                                              'ending.',
                                  'title': 'The checklist is finite on purpose'},
                                 {'body': 'It should not, and here is the reframe that makes it '
                                          'true: revise means a check you built did its job before '
                                          'anything real went wrong. The gap comes named and '
                                          'specific. Fix that one thing, re-run that one check, '
                                          'and you are back at the decision. No spiral, no do-over '
                                          'of the whole capstone, ever.',
                                  'kind': 'common_mistake',
                                  'remember': 'Revise = a named gap + one re-check. Nothing more '
                                              'is being asked.',
                                  'title': "If 'revise' stings for a second"},
                                 {'body': 'One last teach-back, four sentences: what the verifier '
                                          'checked, what a human judged, what the judge model '
                                          'scored, and what your decision was. Then stop. The '
                                          "course's deepest lesson was never agents; it was that "
                                          'well-designed work has a finish line written in '
                                          'advance, and that when you cross it, you are entitled '
                                          'to believe you crossed it. You just did.',
                                  'kind': 'teach_it_back',
                                  'title': 'Say it back, and close the course',
                                  'try_this': ['Four sentences and your decision. Say them once. '
                                               'Then close the page. This one really is the end, '
                                               'and it was designed to be.']}],
               'lesson_type': 'interactive',
               'permission_matrix': [],
               'questions': [{'answer_index': 0,
                              'id': 'capstone-testing-q1',
                              'options': ['The verifier: a deterministic yes/no fact-check',
                                          'Human review: a person should eyeball it',
                                          "The judge model: it can infer the field's presence"],
                              'prompt': "Which evidence layer is right for 'does the required "
                                        "config field exist'?"},
                             {'answer_index': 2,
                              'id': 'capstone-testing-q2',
                              'options': ['The verifier: written text is stored in files, and '
                                          'files are checkable facts',
                                          'The quiz: explanations are recall',
                                          'The judge model: scoring prose against a written rubric '
                                          'is its exact job'],
                              'prompt': 'Which layer suits rubric-scoring a free-form written '
                                        'explanation?'},
                             {'answer_index': 1,
                              'id': 'capstone-testing-q3',
                              'options': ['Four kinds are required by the OpenClaw license',
                                          'Each answers a different question: facts, judgment, '
                                          'prose, and your own understanding differ',
                                          'Redundancy: four independent copies of the same answer '
                                          'make the evidence four times as strong'],
                              'prompt': 'Why four kinds of evidence instead of one really good '
                                        'one?'},
                             {'answer_index': 2,
                              'id': 'capstone-testing-q4',
                              'options': ['The workflow completes quickly to demonstrate '
                                          'capability',
                                          'The workflow asks the judge model for permission',
                                          'The workflow stops: it fails closed exactly as '
                                          'designed'],
                              'prompt': 'The adversarial test case asks the workflow to skip '
                                        'review. What outcome counts as success?'},
                             {'answer_index': 0,
                              'id': 'capstone-testing-q5',
                              'options': ['Fix that one thing, re-run that one check. The system '
                                          'caught it on your behalf',
                                          'Restart the capstone from Lesson 1, since a gap '
                                          'anywhere could mean gaps everywhere',
                                          'Ship anyway and monitor closely'],
                              'prompt': 'The evidence comes back with one named gap. What does '
                                        "'revise' mean here?"}],
               'safety_checks': ['At least one adversarial case exists',
                                 'At least one fail-closed case exists'],
               'skill_templates': [],
               'slug': 'testing',
               'title': 'The Release Decision'}],
  'order': 10,
  'publish_rules': ['requires_non_placeholder_content',
                    'requires_tutor_prompts',
                    'requires_valid_quiz_banks',
                    'requires_capstone_artifacts',
                    'requires_permission_matrix',
                    'requires_evaluation_rubric',
                    'requires_evaluation_cases'],
  'slug': 'module-8-capstone-safety-evaluation',
  'title': 'The Trust Capstone'}]

STRUCTURED_COURSE_PACKS_BY_SLUG = {pack["slug"]: pack for pack in STRUCTURED_COURSE_PACKS}
