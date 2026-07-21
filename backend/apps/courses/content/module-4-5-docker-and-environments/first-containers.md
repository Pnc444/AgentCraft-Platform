# Your First Containers

Time to actually run something. Two containers: one that just says hello, and one that's a real web server.

## 1. Hello, world

In your terminal:

```bash
docker run hello-world
```

What just happened, in order:

1. Docker looked for the `hello-world` **image** locally — didn't find it
2. Downloaded (pulled) it from **Docker Hub**
3. Created a **container** from the image and ran it
4. The container printed its message and exited

That's the whole Docker loop in one command.

## 2. A real web server

```bash
docker run -d -p 8080:80 nginx
```

Breaking that down:

- `-d` — **detached**: run in the background instead of taking over your terminal
- `-p 8080:80` — **port mapping**: port 8080 on your machine → port 80 inside the container
- `nginx` — the image: a popular web server

Now open **http://localhost:8080** in your browser. That "Welcome to nginx!" page is being served from inside the container.

![nginx welcome page](/images/lessons/first-containers/nginx-welcome.png)

## 3. Now delete it — no consequences

This is the point of containers: they're disposable. In Docker Desktop, go to the **Containers** tab, find the nginx container, hit **Stop**, then **Delete**. Or from the terminal:

```bash
docker ps                 # find the container ID
docker stop <id>
docker rm <id>
```

Refresh localhost:8080 — gone. Your machine is exactly as it was before. Nothing was installed, nothing to clean up. **Containers are removable with zero consequences.** Run the `docker run` command again and it's back in seconds (the image is still cached locally).

<details>
<summary><strong>🛠️ Common issues — click to expand</strong></summary>

**"Cannot connect to the Docker daemon"**
Docker Desktop isn't running. Launch it and wait for the green "Engine running" indicator.

**"port is already allocated"**
Something else is using 8080. Use a different port: `docker run -d -p 8081:80 nginx` and visit localhost:8081.

**localhost:8080 won't load**
Check the container is actually running with `docker ps`. If it's not listed, re-run the run command without `-d` to see the error.

</details>

## ✅ Handoff: leave Docker running

**Before you finish this module:** keep Docker Desktop open with the engine running — you'll need it immediately in Module 5.

![Docker Desktop with engine running highlighted](/images/lessons/first-containers/engine-running-highlight.png)

Look for the **green bar / "Engine running"** in the bottom-left of Docker Desktop. If it's green, you're ready.

## Takeaway
You pulled images, ran containers, mapped a port, and deleted everything with no trace. In Module 5 this becomes the backend for your first agent build.
