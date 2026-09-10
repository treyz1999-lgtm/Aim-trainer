# Aim Trainer

A desktop aim trainer built with Python and Pygame. Targets spawn over time, shrink after reaching their max size, and count as misses if they disappear before being clicked.

![Aim Trainer gameplay](assets/md_images/aim%20trainer%201.gif)

## Features

- Timed target spawning
- Hit, miss, lives, elapsed time, and hits-per-second tracking
- Game over screen when lives reach zero
- Restart with `Esc` or `Space`
- Settings panel for colors, spawn speed, target size, lives, and audio volume
- Random hit sound effects
- Hit marker image effect

![Aim Trainer settings](assets/md_images/aim%20trainer%202.gif)

## Requirements

- Python 3.14 or newer, OR
- Docker / Docker Desktop
- `pygame-ce`

## Setup

### Option 1: Local Python Setup

Clone the repository:

```powershell
git clone https://github.com/treyz1999-lgtm/Aim-trainer.git
cd Aim-trainer
```

Create a virtual environment:

```powershell
python -m venv .venv
```

Install dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Run the game:

```powershell
.\.venv\Scripts\python.exe main.py
```

### Option 2: Docker Setup

#### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop) installed and running

#### Build the Image

```bash
git clone https://github.com/treyz1999-lgtm/Aim-trainer.git
cd Aim-trainer
docker build -t aim-trainer:latest .
```

#### Run with Docker Compose (Recommended)

```bash
docker compose up
```

To run in the background:

```bash
docker compose up -d
```

To stop the container:

```bash
docker compose down
```

#### Run with Docker CLI

```bash
docker run --rm -it \
  -e DISPLAY=:0 \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  aim-trainer:latest
```

**Note on Display:** The default Docker setup uses `SDL_VIDEODRIVER=dummy` for headless operation. To display the game GUI:

- **Linux:** Pass your `DISPLAY` variable and X11 socket as shown above
- **macOS:** Install [XQuartz](https://www.xquartz.org/) and configure X11 forwarding
- **Windows:** Use WSL2 with a display server like [VcXsrv](https://sourceforge.net/projects/vcxsrv/) or [Xming](http://www.straightrunning.com/XmingNotes/)

## Controls

- Click targets to score hits.
- Press `Esc` or `Space` to restart.
- Click `Settings` in the info bar to customize the game.

## Assets

Hit sound effects are loaded from:

```text
assets/audio/hits/
```

The hit marker image is loaded from:

```text
assets/images/Hitmarker.png
```

Optional background music can be added locally at:

```text
assets/audio/background.mp3
```

That background music file is ignored by Git because it may not be licensed for redistribution.
