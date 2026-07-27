# Knight's Academy

A hands-on course platform that takes someone with no AI background and gets
them building real AI agents. Ten modules, 57 lessons, three agent builds
(Hermes, OpenClaw, Claude Code) and a capstone on safety and evaluation.

Django + DRF on Postgres, Next.js 14 on the front, everything in Docker.

---

## Quickstart

You need **Docker Desktop** (with the engine running) and nothing else — no
local Python, no local Node.

```bash
git clone git@github.com:Pnc444/AgentCraft-Platform.git
cd AgentCraft-Platform
cp .env.example .env          # then edit — see Environment below
docker compose up -d          # builds, migrates, seeds, serves
```

First run takes a few minutes to build the images. When it settles:

| | URL | Credentials |
|---|---|---|
| App | http://localhost:3000 | see below |
| API | http://localhost:8000/api/v1/ | JWT |
| API docs | http://localhost:8000/api/docs/ | — |
| Django admin | http://localhost:8000/admin/ | superuser you create |

Create a student and an admin:

```bash
# demo student (also seeds badges and progress)
docker compose exec backend python manage.py seed_demo
# -> login demo_student / demo1234

# staff/superuser review account (idempotent; re-run to reset the password)
docker compose exec backend python manage.py create_admin
# -> login admin / admin1234 — pass --password for anything not localhost

# or Django's own interactive prompt
docker compose exec backend python manage.py createsuperuser
```

Then open http://localhost:3000, log in, and start Module 1.

### Staff accounts skip the lesson gates

Students move through the course gated: a module stays locked until the one
before it is complete, an assessment stays locked until the lesson video has
been watched to the end, and the player makes you answer each check before
moving on. Any account with Django's **`is_staff`** flag skips all of it —
module locks, video gates, per-beat gating, the certificate lock, and the
locked rows in the module overview's step dropdowns. That's what makes
reviewing Module 7 possible without playing Modules 1–6 first.

Who has the flag: anyone from `createsuperuser` (Django sets `is_staff`
alongside `is_superuser`), anyone from `create_admin` (use `--staff-only` to
grant the bypass without superuser), and anyone an existing admin ticks
"Staff status" for in `/admin/`. The **`ai_instructor` role does not bypass
anything** — only `is_staff` is consulted.

Two caveats worth knowing. Students can't grant themselves the flag:
`is_staff` is served read-only by `/api/v1/auth/me/`, and a test pins that a
PATCH is silently ignored. And the bypass is a review convenience, not a
security boundary — the API has never enforced lesson progression for
anyone, so gating that must hold against a hostile client belongs
server-side (see `frontend/lib/gates.ts`).

Stop with `docker compose down`. Your database survives — only `down -v`
destroys it.

---

## Environment

`.env` is gitignored; `.env.example` is the template. The values that matter:

| Variable | What it does |
|---|---|
| `SECRET_KEY` | Django secret. Change it for anything non-local. |
| `DATABASE_URL` | Points at the compose Postgres by service name (`db`). |
| `POSTGRES_PORT` / `BACKEND_PORT` / `FRONTEND_PORT` | Host ports. Defaults 5433 / 8000 / 3000. Alternates are commented in the file if another stack owns those. |
| `OPENROUTER_API_KEY` | Powers the AI tutor. Without it the tutor says so plainly instead of pretending. |
| `OPENROUTER_TUTOR_MODELS` | Comma-separated fallback chain, best first. Free models rate-limit, so the tutor walks the list until one answers. |

`DATABASE_URL` uses the Docker service name, so it only resolves inside
compose. Running the backend in a local venv? Point it at
`postgresql://postgres:postgres@localhost:5433/agentcraft` or comment it out to
fall back to SQLite.

---

## How the course is put together

### Content lives in Markdown

```text
backend/apps/courses/
├── content/<course-slug>/<lesson-slug>.md   the lesson prose
├── curriculum.py                            the spec: modules, lessons, quizzes
├── structured_course_packs.py               modules 4, 6, 8 (artifacts, rubrics)
├── sandbox_specs.py                          practice-terminal task specs
└── beats.py                                 how a lesson becomes screens
```

Write or edit a `.md` file, register the lesson in `curriculum.py`, then:

```bash
docker compose exec backend python manage.py sync_content
```

`sync_content` is production-safe: it upserts by slug and never touches users,
badges, or progress on kept lessons. Add `--course <slug>` to scope it,
`--prune` to delete lessons no longer in the spec (this *does* drop their
progress), and `--strict` to fail the run on content-validation problems — use
that one in CI.

The backend container runs `migrate` and `sync_content` on every start, so a
`docker compose up` always reflects the current content.

### A lesson is a sequence of beats

Lessons render in one zero-scroll player. Each screen is a **beat**, and there
are five kinds:

| Beat | Purpose |
|---|---|
| `explain` | one idea, with an optional analogy |
| `predict` | ask before telling — the learner commits a guess first |
| `check` | one question, instant feedback, free retries |
| `do` | a real action: `video`, `terminal`, `workbench`, `studio`, `tutor_try` |
| `recap` | what you now know |

Beats come from one of three sources, in priority order: an authored `beats`
list in the lesson config, the guided blocks that modules 4/6/8 ship, or a
mechanical conversion of the Markdown. That last one is why every lesson —
including ones nobody has converted — renders in the player.

Two rules the validator enforces on sync: no two `explain` beats in a row
(passive streaks are where attention dies), and a `do` beat must name an action
that actually exists.

### The interactive pieces

- **Workbench** — opens a lesson's real practice files (`SOUL.md`,
  `openclaw.json`, skill templates) in an editable pane. Edits go to a scratch
  buffer and Reset restores the shipped text; nothing reaches the server.
- **Practice terminal** — the learner types real commands and gets realistic
  output, with per-task hints. Used by the Docker and Hermes labs.
- **Capstone studio** — the Module 8 deliverable, with its rubric and
  evaluation cases.
- **AI tutor** — streams from OpenRouter with the whole curriculum, the current
  lesson, and the learner's progress in context. It refuses to hand over quiz
  answers.

### Assessment

Every published module ends with an exam. Exam items must combine at least two
lessons or apply one to a new scenario, and **no exam question may repeat a
recap question** — `sync_content` checks that and complains if it does. Pass at
80%, retries are free and unlimited, and a passed assessment opens on its
standing result rather than a blank attempt.

---

## Working on it

```bash
# tests
docker compose run --rm --no-deps --entrypoint "" backend \
  sh -c "pip install -q pytest pytest-django && python -m pytest -q"
docker compose run --rm --no-deps --entrypoint "" frontend npm run test

# types and lint
docker compose run --rm --no-deps --entrypoint "" frontend npx tsc --noEmit
docker compose run --rm --no-deps --entrypoint "" frontend npm run lint

# logs / shell
docker compose logs -f backend
docker compose exec backend python manage.py shell
docker compose exec db psql -U postgres -d agentcraft
```

Both services hot-reload from bind mounts, so edits land without a rebuild.
Rebuild only when dependencies change:

```bash
docker compose up -d --build
```

### Layout

```text
backend/
  apps/accounts    users and JWT auth
  apps/courses     modules, lessons, content sync, beats
  apps/learning    progress, badges, interaction log
  apps/tutor       OpenRouter client, lesson context, streaming endpoint
  config/          settings, urls
frontend/
  app/(dashboard)  the authenticated app
  components/lessons  the player and its beat widgets
  lib/             API client, beat helpers, progress cache
infra/docker/      Dockerfiles
```

---

## API

Every response is a `{ data, meta, errors }` envelope. Auth is JWT — 15-minute
access, 7-day refresh.

```text
POST   /api/v1/auth/register/
POST   /api/v1/auth/token/               and /token/refresh/
GET    /api/v1/auth/me/                  PATCH to update

GET    /api/v1/courses/                  with per-user progress
GET    /api/v1/courses/{slug}/
GET    /api/v1/courses/{course}/lessons/{lesson}/    includes derived beats
POST   /api/v1/lessons/{id}/progress/    status, score, video_watched, interaction_event

POST   /api/v1/tutor/ask/                SSE stream
GET    /api/v1/tutor/suggestions/

GET    /api/v1/recommendations/
GET    /api/v1/dashboard/stats/
```

---

## Troubleshooting

**Port already allocated.** Something owns 3000, 8000, or 5433. Change the
`*_PORT` values in `.env` (alternates are commented there) and
`docker compose up -d` again.

**`could not translate host name "db"`.** The backend is running outside
compose, or `docker compose up` was never run. `DATABASE_URL` uses the compose
service name.

**Frontend can't reach the API.** `NEXT_PUBLIC_API_URL` is read by the browser
and must be a host URL (`http://localhost:8000/api/v1`), while
`INTERNAL_API_URL` is used server-side and points at `http://backend:8000`.

**The tutor says every model is busy.** Expected on OpenRouter's free tier —
it walks a five-model fallback chain first. There is also a per-user limit of
20 questions every 5 minutes.

**Lesson edits aren't showing.** Run `sync_content`. Content is synced into
Postgres, not read from disk at request time.

**Node modules owned by root.** The frontend container writes them. Either work
through `docker compose run` (as above) or
`sudo chown -R $USER frontend/node_modules`.
