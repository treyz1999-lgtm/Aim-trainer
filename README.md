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

- Python 3.14 or newer
- `pygame-ce`

## Setup

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
