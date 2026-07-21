# Open the Front Door (Just a Crack)

*Lesson 3 of 4 · about 12 minutes · your assistant gets a doorway to the outside world.*

So far your assistant only talks to you, on your machine. A **channel** connects it to a chat app you already use (WhatsApp, Telegram, Slack, Discord, and others) so you can message it from your phone like any other contact.

## Start with the reassurance

**Every door starts locked.** Out of the box, a stranger who messages your assistant gets a short pairing code and then silence. The assistant will not talk to them, act for them, or reveal anything until you deliberately approve that person. There is no accidental way to open your assistant to the world; the open setting requires two explicit steps you would have to type on purpose. Explore this whole lesson knowing that.

## Three door policies

- **Pairing** *(the default)*: a doorbell with a code. Unknown senders get a code; you approve the ones you choose with `openclaw pairing approve <channel> <code>`. Everyone else gets silence.
- **Allowlist**: a guest list. Only people you named in advance get through.
- **Open**: the door propped open for anyone. Exists for genuine public bots. Requires the two deliberate steps. Not for this course.

Pairing is the right answer for everything you will build here. It is not the timid option; it is the correct one.

## Two settings for shared spaces

- **`requireMention`**: in a group chat, the assistant only answers when called by name, like a polite person in a group conversation.
- **`per-channel-peer` sessions**: if several people message your assistant directly, each person gets a separate conversation notebook. Threads never blur together.

## The rollout, whole

1. Connect one channel, the app you actually use most.
2. Leave the policy on pairing. It already is.
3. Approve exactly one person: you.
4. Send yourself a message. Watch it answer.

That is a complete, correct first rollout. Widening it later (a second person, a group room) is a repeat of step 3 with a new code, whenever you choose. There is no pressure to widen anything today, or ever.

## Done means done

You are done when you can:

- explain pairing, allowlist, and open in doorbell terms
- say what `requireMention` prevents in a group room
- say who can reach a freshly connected channel before any approvals (answer: no one)