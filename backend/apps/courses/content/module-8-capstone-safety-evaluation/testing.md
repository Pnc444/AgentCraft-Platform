# The Release Decision

*Lesson 4 of 4 · about 15 minutes · the last lesson of the capstone. It ends with a decision, not a feeling.*

Everything is built: an automation with a shape, guardrails that point at real things, doors labeled in advance. One question remains: *should this ship?* This lesson makes that question answerable with evidence instead of nerves.

## Four kinds of evidence

No single test can vouch for a whole system, so the capstone gathers four kinds. Each answers a different question, so together they leave no question standing:

1. **The quiz**: do *you* understand the system? (The recap quizzes have quietly been this all along.)
2. **The verifier**: are the facts in place? A deterministic yes/no machine: files exist, required settings present, audit passes. Same answer every time, which is exactly its charm.
3. **Human review**: is it *good*? Judgment questions ("is this rollout plan sensible?") go to a person.
4. **The judge model**: is the free-form work sound? An AI scoring drafts against a written rubric: clarity, groundedness, safety reasoning.

The matching matters more than the machinery: facts go to verifiers, judgment goes to humans, prose goes to the judge, and your own understanding shows up in the quiz. Evidence of the wrong kind is just noise. A file-exists check cannot tell you an explanation is clear, and a judge model should not be asked whether a file exists.

## The test cases: four doors, deliberately knocked on

Your evaluation set below tries four things on purpose: a good workflow (should **pass**), a flawed one missing evidence (should come back marked **revise**), a sneaky one that tries to skip review (should be **stopped**), and a re-test of something fixed before (should **stay fixed**). The third case deserves a smile: you *want* the system tested by a bad actor on your schedule, in the safety of a test. A system that fails closed under a sneaky test has earned something hoping cannot buy.

## The finite checklist, and the decision

The release-readiness checklist below is **finite on purpose**: a fixed number of boxes, each checked exactly once. When the last box is checked, the evidence phase is over. Then you decide. Two outcomes, both honorable:

- **Release**: the evidence supports trust. Ship it.
- **Revise**: the evidence named a specific gap. Fix that one thing and re-run that one check. Revise is the checks working on your behalf, never a verdict on you.

Notice how the moment of deciding feels: small. The evidence carried all the weight, gathered one bounded piece at a time. Deciding is just reading what the evidence already says.

## Done means done: lesson, module, and course

Complete the Capstone Studio below, check the finite list, make your call. Then pause on this: **you are done.** Not "done for now." Done, by criteria written down before you started, which has been this course's promise since Juno's first stop rule. The stop rule fires. The work ends. That, as much as any technical skill, is what this course most hoped you would take with you.