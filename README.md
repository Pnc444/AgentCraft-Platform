# AgentCraft

Learn AI agents from zero, one step at a time. Django REST API backend + Next.js (React) frontend, run with Docker Compose.

## Repository Structure

```
agentcraft-platform/
├── backend/                  # Django 5 + Django REST Framework API
│   ├── config/               # Settings (base/development/production), URLs, WSGI/ASGI
│   ├── apps/
│   │   ├── accounts/         # Custom User model, JWT auth, register, profile
│   │   ├── courses/          # Skill, Course, Lesson + seed_demo command
│   │   └── learning/         # Progress tracking, recommendations, dashboard stats
│   ├── shared/               # Envelope renderer, pagination
│   └── requirements/         # base / development / production
├── frontend/                 # Next.js 14 (App Router) + TypeScript + Tailwind
│   ├── app/                  # Pages: landing, (auth), (dashboard)
│   ├── components/           # landing/, dashboard/, auth/, shared/
│   ├── lib/api/              # Fetch client with JWT refresh + API modules
│   ├── stores/               # Zustand auth store
│   └── types/                # Shared TypeScript types
├── infra/docker/             # Dockerfiles
└── docker-compose.yml        # Postgres 16, Redis 7, backend, frontend
```

## Quick Start (Docker)

```bash
cp .env.example .env          # fill in SECRET_KEY at minimum
docker-compose up --build
# CHECK BUG FIXES AT THE BOTTOM OF THE PAGE
```

| Service | URL |
|---|---|
| Frontend | http://localhost:3000 |
| Django API | http://localhost:8000/api/v1/ |
| API docs (Swagger) | http://localhost:8000/api/docs/ |
| Django admin | http://localhost:8000/admin/ |

Seed demo data (courses, lessons, a demo student):

```bash
docker-compose exec backend python manage.py seed_demo
# Login: demo_student / demo1234
```

## Local Development (without Docker)

Backend (uses SQLite automatically when DATABASE_URL is unset):

```bash
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1        # Windows
pip install -r requirements/development.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver        # http://localhost:8000
```

Frontend:

```bash
cd frontend
npm install
npm run dev                       # http://localhost:3000
```

## API Overview

All endpoints return a `{ data, meta, errors }` envelope. Auth is JWT (15-min access, 7-day refresh).

```
POST   /api/v1/auth/register/
POST   /api/v1/auth/token/
POST   /api/v1/auth/token/refresh/
GET    /api/v1/auth/me/               PATCH to update profile
POST   /api/v1/auth/password/change/

GET    /api/v1/courses/               with per-user progress annotations
GET    /api/v1/courses/{slug}/
GET    /api/v1/courses/{course_slug}/lessons/{lesson_slug}/
POST   /api/v1/lessons/{id}/progress/ { "status": "in_progress" | "completed" }

GET    /api/v1/recommendations/
GET    /api/v1/dashboard/stats/       profile stats + badges
```

## Adding Lesson Content

Lesson content is plain Markdown, synced into the database by slug.

1. **Write the lesson file.** Drop a `.md` file at
   `backend/apps/courses/content/<course-slug>/<lesson-slug>.md`
   (e.g. `content/module-5-hermes/what-hermes-is.md`). Standard Markdown works;
   code blocks get a copy-to-clipboard button automatically.

2. **Register it in the curriculum.** In `backend/apps/courses/curriculum.py`, find (or add)
   the module entry and make sure the lesson is listed:
   `("Lesson Title", "lesson-slug", "theory" | "interactive" | "sandbox" | "agent_lab", minutes)`.
   The lesson slug must match the filename. A course only shows in the app when its
   `"published"` flag is `True`.

3. **Load it into the app.** This syncs ALL modules under `courses/` into the database:

   ```bash
   docker compose exec backend python manage.py sync_content
   ```

   To sync just one course, add `--course <course-slug>`. Add `--prune` to delete DB lessons
   that are no longer in the curriculum spec (warning: student progress on pruned lessons is lost).
   `sync_content` is production-safe: it upserts by slug and never touches users, badges,
   progress, admin-set video URLs, or admin-edited quiz questions.

4. **Quiz questions** live in the lesson's sandbox config. Every lesson gets filler recap
   questions by default; write real ones in Django admin (lesson → quiz/sandbox config) or
   in the lesson spec in `curriculum.py`.

For a full dev reset with demo data instead, use `seed_demo` (destructive, dev only).

## Conventions

- Python: PEP 8, Black, isort
- TypeScript: strict mode, no `any`
- Client state: Zustand · Server state: TanStack Query
- Commits: Conventional commits (`feat:`, `fix:`, `chore:`, `docs:`)

## Coming Soon

- AI Tutor chat (Anthropic API) — panel UI is in place, backend integration pending
- Sandbox lessons (Docker-in-Docker practice environments)

## Docker Bug Fixes

### "Module not found" after pulling new frontend dependencies

`docker compose up` builds fine but the frontend errors with something like
`Module not found: Can't resolve 'some-package'`, even though the package is listed in
`frontend/package.json`.

```bash
docker compose down
docker compose up --build -V
```
## more aggressive reset

```bash
docker compose down -v
docker compose up --build
```

