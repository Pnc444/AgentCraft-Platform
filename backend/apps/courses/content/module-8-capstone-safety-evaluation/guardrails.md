# Guardrails: Values and Seatbelts

*Lesson 2 of 4 · about 10 minutes · what your assistant tries to be, and what the system guarantees anyway.*

Your automation from Lesson 1 has a shape. This lesson wraps it in guardrails, which come in two layers people constantly blur. You are about to un-blur them permanently.

## Layer one: values (what the assistant tries to be)

AI research names three qualities a good assistant aims for: **helpful, truthful, harmless**.

- **Helpful**: it moves your task forward instead of dead-ending.
- **Truthful**: it separates what it knows from what it guesses, and says which is which.
- **Harmless**: it declines to cause damage, even when asked carelessly.

These are real and they matter. They are also *aims*: the driver's good intentions.

## Layer two: seatbelts (what the system guarantees)

A careful driver still wears a seatbelt, because the seatbelt works on the bad day. Your Module 6 build is already full of seatbelts: pairing on the doors, sandboxing on the rooms, tools granted one at a time, receipts on every run. **Settings, not intentions. They hold no matter what kind of day the model is having.**

The two layers are a pairing, not rivals. Values make the assistant good to work with. Seatbelts make the outcome safe even if values slip. You want both, and you already have both.

## The one rule this lesson installs

> **Every safety claim must point at something you could show someone.**

"Our assistant is safe": points at nothing. It is a mood.
"Strangers can't reach it (pairing), it can't touch files outside its workspace (sandbox), and every run leaves a receipt": points at three settings you could open on screen in ten seconds.

The guardrail matrix below runs this rule across your whole capstone: each row takes one value and names the concrete seatbelt behind it. When the matrix is full, "is my project safe?" has stopped being a feeling and become a short list of checkable facts. Feelings need managing. Lists just need reading.

## Done means done

You are done when you can:

- name the three values with a one-line meaning for each
- give one seatbelt from your own build and say which value it backs
- state the one rule