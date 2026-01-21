# Distributing BERA with Docker

## What is Docker?
Think of Docker like a **shipping container** for code.
- **Without Docker**: To run your code, someone needs to install Python, then `pip install requirements.txt`, ensure they have the right version of libraries, set up paths, etc. It works on your machine but might break on theirs ("It works on my machine" syndrome).
- **With Docker**: You pack your code, Python, and all dependencies into a sealed box (Container Image). You ship this box to your users. They just run the box. They don't need Python installed. They just need Docker.

## Step 1: Publish Your Agent (For You/Developer)
To distribute this, you usually upload the "box" to a central warehouse called **Docker Hub** (like GitHub but for containers).

1.  **Create an account** on [Docker Hub](https://hub.docker.com/).
2.  **Login** in your terminal:
    ```bash
    docker login
    ```
3.  **Build & Tag** the image:
    Replace `yourusername` with your Docker Hub username.
    ```bash
    docker build -t yourusername/bera:latest .
    ```
4.  **Push** it to the cloud:
    ```bash
    docker push yourusername/bera:latest
    ```

## Step 2: Run the Agent (For the User)
Now, anyone in the world can run your agent without installing Python or cloning the repo. They just need Docker.

**The Command:**
```bash
docker run --rm \
  -e GROQ_API_KEY="their_key_here" \
  -v "/path/to/their/local/extensions:/data/extensions:ro" \
  -v "$(pwd)/output:/app/output" \
  yourusername/bera:latest
```

### What happens?
1.  Docker downloads (`pulls`) your agent from the cloud.
2.  It starts the container.
3.  It mounts their local extension folder into the container so the agent can see it.
4.  The agent runs, generates `report_<id>.json`, and saves it to their output folder.
5.  The container shuts down (`--rm` cleans it up).

## Updating the Agent
Because the image is cached on your computer, if a new version is released, you need to pull it manually:
```bash
docker pull yourusername/bera:latest
```
Then run the agent again.
