# Terminal Space Shooter

A fun, fast-paced space shooter game that runs entirely in your terminal!

## Features
- Smooth terminal animations using the `blessed` library.
- Parallax starfield background.
- Increasing difficulty as your score grows.
- Explosions and colorful emoji graphics.

## How to Play

### Prerequisites
- Python 3.x
- `blessed` library

### Installation
1. Navigate to the game directory:
   ```bash
   cd space_invaders_terminal
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Game
Run the game using Python:
```bash
python3 game.py
```

### Controls
- **A** or **Left Arrow**: Move Left
- **D** or **Right Arrow**: Move Right
- **Space**: Shoot
- **Q** or **ESC**: Quit Game

## Objective
Shoot the incoming alien invaders (`👾`) before they reach the bottom of the screen or hit your ship (`🚀`). You have 3 lives. Each enemy destroyed gives you 10 points!
