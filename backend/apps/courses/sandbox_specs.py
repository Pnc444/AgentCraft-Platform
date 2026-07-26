"""Practice-terminal specs for `sandbox` lessons.

A sandbox lesson used to render a button that fired `alert("coming soon")`.
This replaces it with something that actually teaches: the learner types the
real commands from the lesson and gets realistic output back.

It is a *simulator*, and the UI says so plainly ("Simulated · nothing runs on
your machine"). That is the honest framing — the commands are byte-identical to
the real ones, so the muscle memory transfers, but nothing can break and no
Docker install is required to practise.

Keyed by ``(course_slug, lesson_slug)``. A lesson with no entry renders no
sandbox at all rather than a fake affordance.

Each task's ``accept`` entries are case-insensitive regex sources.
"""

from __future__ import annotations

SANDBOX_SPECS: dict[tuple[str, str], dict] = {
    ("module-4-5-docker-and-environments", "first-containers"): {
        "intro": (
            "Work through the same commands from the lesson. Type them here first, "
            "then run them for real in your own terminal."
        ),
        "tasks": [
            {
                "id": "m45-hello-world",
                "goal": "Run the hello-world container",
                "detail": "Ask Docker to run the hello-world image.",
                "hint": "docker run hello-world",
                "accept": [r"^docker\s+run\s+hello-world$"],
                "output": (
                    "Unable to find image 'hello-world:latest' locally\n"
                    "latest: Pulling from library/hello-world\n"
                    "c1ec31eb5944: Pull complete\n"
                    "Digest: sha256:d211f485f2dd1dee407a80973c8f129f00d54604d2c90732e8e320e5038a0348\n"
                    "Status: Downloaded newer image for hello-world:latest\n\n"
                    "Hello from Docker!\n"
                    "This message shows that your installation appears to be working correctly."
                ),
                "success": "Docker pulled the image, made a container, ran it, and it exited.",
            },
            {
                "id": "m45-run-nginx",
                "goal": "Run nginx in the background on port 8080",
                "detail": "Detached, mapping your port 8080 to port 80 inside the container.",
                "hint": "docker run -d -p 8080:80 nginx",
                "accept": [
                    r"^docker\s+run\s+(-d\s+-p\s+8080:80|-p\s+8080:80\s+-d|-dp\s+8080:80)\s+nginx$"
                ],
                "output": (
                    "Unable to find image 'nginx:latest' locally\n"
                    "latest: Pulling from library/nginx\n"
                    "Status: Downloaded newer image for nginx:latest\n"
                    "9f4e3a2b7c11d0e5a8b3c6f2019d4e7a5b8c1d2e3f4a5b6c7d8e9f0a1b2c3d4e"
                ),
                "success": "It's running in the background. localhost:8080 would serve the nginx page.",
            },
            {
                "id": "m45-docker-ps",
                "goal": "List what's running",
                "detail": "You need the container ID before you can stop it.",
                "hint": "docker ps",
                "accept": [r"^docker\s+ps$"],
                "output": (
                    "CONTAINER ID   IMAGE   COMMAND                  STATUS         PORTS                  NAMES\n"
                    "9f4e3a2b7c11   nginx   \"/docker-entrypoint.…\"   Up 2 minutes   0.0.0.0:8080->80/tcp   nginx-demo"
                ),
                "success": "There it is — container 9f4e3a2b7c11.",
            },
            {
                "id": "m45-stop",
                "goal": "Stop the nginx container",
                "detail": "Use the ID from the list above (9f4e3a2b7c11).",
                "hint": "docker stop 9f4e3a2b7c11",
                "accept": [r"^docker\s+stop\s+(9f4e3a2b7c11|nginx-demo)$"],
                "output": "9f4e3a2b7c11",
                "success": "Stopped. localhost:8080 would stop responding now.",
            },
            {
                "id": "m45-rm",
                "goal": "Delete the container",
                "detail": "This is the payoff — removal with zero consequences.",
                "hint": "docker rm 9f4e3a2b7c11",
                "accept": [r"^docker\s+rm\s+(-f\s+)?(9f4e3a2b7c11|nginx-demo)$"],
                "output": "9f4e3a2b7c11",
                "success": "Gone. Your machine is exactly as it was before you started.",
            },
        ],
        "misfires": [
            {
                "match": [r"^docker\s+run\s+nginx$"],
                "message": (
                    "That starts nginx but takes over your terminal, and nothing maps to "
                    "a port you can visit. Add -d to detach and -p 8080:80 to map the port."
                ),
            },
            {
                "match": [r"^docker\s+run\s+-d\s+nginx$"],
                "message": (
                    "Running, but unreachable — no port mapping. Without -p 8080:80, port 80 "
                    "stays sealed inside the container."
                ),
            },
            {
                "match": [r"^docker\s+rm\s+.*", r"^docker\s+stop\s+.*"],
                "message": "Close — but check the container ID against `docker ps` output.",
            },
            {
                "match": [r"^docker\s+run\s+.*-p\s+80:8080.*"],
                "message": (
                    "Ports are the wrong way round. It's -p <your-machine>:<inside-container>, "
                    "so -p 8080:80."
                ),
            },
            {
                "match": [r"^sudo\s+.*"],
                "message": "No sudo needed here — Docker Desktop runs as your user.",
            },
        ],
        "extras": [
            {
                "match": [r"^docker\s+images$"],
                "output": (
                    "REPOSITORY    TAG       IMAGE ID       SIZE\n"
                    "nginx         latest    a72860cb95fd   188MB\n"
                    "hello-world   latest    d2c94e258dcb   13.3kB"
                ),
            },
            {
                "match": [r"^docker\s+ps\s+-a$"],
                "output": (
                    "CONTAINER ID   IMAGE         STATUS                     NAMES\n"
                    "9f4e3a2b7c11   nginx         Up 2 minutes               nginx-demo\n"
                    "3b1a5c8d2e04   hello-world   Exited (0) 5 minutes ago   zen_mirzakhani"
                ),
            },
            {
                "match": [r"^docker\s+(-v|--version|version)$"],
                "output": "Docker version 27.1.1, build 6312585",
            },
            {
                "match": [r"^help$", r"^\?$"],
                "output": (
                    "Practice terminal. Recognised here: docker run, docker ps, docker stop,\n"
                    "docker rm, docker images, docker version. Type 'clear' to reset."
                ),
            },
        ],
        "completion": {
            "title": "That's the whole Docker loop.",
            "body": (
                "Pull, run, map a port, stop, delete. Now run the exact same commands in "
                "your own terminal — leave Docker Desktop running, Module 5 needs it."
            ),
        },
    },
    ("module-5-hermes", "first-conversation-and-container"): {
        "intro": (
            "The Docker backend is lazy — the container appears the first time the "
            "agent runs a command. Practise the sequence that creates it."
        ),
        "tasks": [
            {
                "id": "m5c-config-view",
                "goal": "Print your whole Hermes configuration",
                "detail": "Worth seeing once so you know everything your agent is set up to do.",
                "hint": "hermes config",
                "accept": [r"^hermes\s+config$"],
                "output": (
                    "config.yaml   ~/.hermes/config.yaml\n"
                    ".env          ~/.hermes/.env\n"
                    "model         openrouter/auto\n"
                    "terminal.backend   docker\n"
                    "OPENROUTER_API_KEY sk-or-v1-****************  (set)"
                ),
                "success": "Backend is docker and the key is set — ready to run.",
            },
            {
                "id": "m5c-set-cpu",
                "goal": "Cap the agent at 1 CPU core",
                "detail": "Dotted keys reach nested sections in config.yaml.",
                "hint": "hermes config set terminal.container_cpu 1",
                "accept": [r"^hermes\s+config\s+set\s+terminal\.container_cpu\s+1$"],
                "output": "updated config.yaml: terminal.container_cpu = 1",
                "success": "A runaway loop now hits a ceiling instead of your whole machine.",
            },
            {
                "id": "m5c-set-memory",
                "goal": "Cap the agent's memory at 2048 MB",
                "hint": "hermes config set terminal.container_memory 2048",
                "accept": [r"^hermes\s+config\s+set\s+terminal\.container_memory\s+2048$"],
                "output": "updated config.yaml: terminal.container_memory = 2048",
                "success": "Both resource caps in place.",
            },
            {
                "id": "m5c-whoami",
                "goal": "Ask the agent to run whoami",
                "detail": (
                    "This is the moment the container gets created. Type the request "
                    "you'd send the agent."
                ),
                "hint": "run whoami and tell me what it says",
                "accept": [r"^(?!docker\b).*\bwhoami\b"],
                "output": (
                    "[hermes] creating sandbox container… done (hermes-sandbox)\n"
                    "[hermes] $ whoami\n"
                    "hermes\n\n"
                    "It says `hermes` — that's the unprivileged user inside the container,\n"
                    "not your machine's username."
                ),
                "success": (
                    "The container was created on demand, and the answer proves the "
                    "command ran inside it — not on your laptop."
                ),
            },
        ],
        "misfires": [
            {
                "match": [r"^hermes\s+config\s+set\s+container_cpu.*"],
                "message": (
                    "Nearly — the key is nested under terminal, so it needs the dotted "
                    "form: terminal.container_cpu"
                ),
            },
            {
                "match": [r"^docker\s+.*"],
                "message": (
                    "You don't drive the container directly here. Hermes creates and "
                    "manages it for you — talk to Hermes instead."
                ),
            },
        ],
        "extras": [
            {
                "match": [r"^hermes$", r"^hermes\s+start$"],
                "output": "[hermes] ready. Type a message, or /exit to quit.",
            },
        ],
        "completion": {
            "title": "You made the box appear.",
            "body": (
                "Config caps set, container created on first command, and you proved the "
                "command ran inside it. Next lesson you'll try to break out of it."
            ),
        },
    },
    ("module-5-hermes", "sandbox-verification-lab"): {
        "intro": (
            "Prove the sandbox actually contains the agent. Each command tests one "
            "boundary — run them here, then repeat against your real container."
        ),
        "tasks": [
            {
                "id": "m5-ps-running",
                "goal": "Confirm the Hermes container is running",
                "hint": "docker ps",
                "accept": [r"^docker\s+ps$"],
                "output": (
                    "CONTAINER ID   IMAGE            STATUS         NAMES\n"
                    "4d7c2a9e1b83   hermes:0.18.2    Up 6 minutes   hermes-sandbox"
                ),
                "success": "Running and isolated as hermes-sandbox.",
            },
            {
                "id": "m5-whoami",
                "goal": "Check which user the agent runs as inside the container",
                "detail": "An agent running as root inside its box is a weaker boundary.",
                "hint": "docker exec hermes-sandbox whoami",
                "accept": [r"^docker\s+exec\s+(-it\s+)?hermes-sandbox\s+whoami$"],
                "output": "hermes",
                "success": "Unprivileged user, not root. That's what you want.",
            },
            {
                "id": "m5-filesystem",
                "goal": "Show the agent cannot see your home directory",
                "detail": "List /host inside the container — it should not exist.",
                "hint": "docker exec hermes-sandbox ls /host",
                "accept": [r"^docker\s+exec\s+(-it\s+)?hermes-sandbox\s+ls\s+/host$"],
                "output": "ls: /host: No such file or directory",
                "success": "The boundary holds — your files are not reachable from inside.",
            },
            {
                "id": "m5-escape",
                "goal": "Attempt to read a file outside the sandbox",
                "detail": "This is supposed to fail. Watch it fail.",
                "hint": "docker exec hermes-sandbox cat /etc/hostname",
                "accept": [
                    r"^docker\s+exec\s+(-it\s+)?hermes-sandbox\s+cat\s+/(etc/hostname|host/.*)$"
                ],
                "output": "4d7c2a9e1b83",
                "success": (
                    "It read the container's own hostname, not your machine's. "
                    "The agent's whole world is that container."
                ),
            },
        ],
        "misfires": [
            {
                "match": [r"^docker\s+exec\s+.*\s+(rm|sudo|chmod)\s+.*"],
                "message": (
                    "Don't practise destructive commands here. The lab is about proving "
                    "the boundary exists, not testing what breaks."
                ),
            },
            {
                "match": [r"^whoami$", r"^ls\s.*"],
                "message": (
                    "That runs on your machine, not in the container. Prefix it with "
                    "`docker exec hermes-sandbox` to run it inside."
                ),
            },
        ],
        "extras": [
            {
                "match": [r"^docker\s+logs\s+hermes-sandbox$"],
                "output": (
                    "[hermes] backend=docker model=openrouter/auto\n"
                    "[hermes] sandbox ready, awaiting messages"
                ),
            },
        ],
        "completion": {
            "title": "You verified the boundary yourself.",
            "body": (
                "You did not take our word for it — you checked the user, the filesystem, "
                "and an escape attempt. Do this every time you give an agent new powers."
            ),
        },
    },
}


def sandbox_spec_for(course_slug: str, lesson_slug: str) -> dict | None:
    return SANDBOX_SPECS.get((course_slug, lesson_slug))
