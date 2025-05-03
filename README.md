# 🧠 SOS Game with AI (Minimax + Alpha-Beta Pruning + Tkinter GUI)

This is a simple yet strategic **SOS game** built in Python using the **Tkinter GUI library**.  
The computer opponent is powered by the **Minimax algorithm with Alpha-Beta Pruning**, making smart decisions to never lose!


## 🎮 What is SOS?

SOS is a paper-and-pencil game played on a grid (3x3 in this project).  
Players take turns placing either the letter **S** or **O** in any empty cell.  
A player scores a point by forming the sequence **S-O-S** horizontally, vertically, or diagonally.

## 🤖 Features

- ✅ Interactive GUI with **Tkinter**
- 🧠 AI uses **Minimax algorithm** with **Alpha-Beta pruning**
- 🧩 Dynamic score calculation (each SOS gives a point)
- 🎯 Real-time turn-based play
- 💬 Visual indicators for player turn and scores
- 🏆 Game ends when the board is full, winner is announced

## 📸 Screenshot

> Insert a screenshot of your running game here.

```
![Screenshot](images/screenshot.png)
```

## ⚙️ How to Run

### 1. Clone the repository:

```bash
git clone https://github.com/your-username/sos-ai-game.git
cd sos-ai-game
```

### 2. Run the game:

```bash
python SOS_oyunu.py
```

✅ Make sure you have Python 3 installed.

## 📁 File Structure

```bash
sos-ai-game/
│
├── SOS_oyunu.py         # Main game script (GUI + AI logic)
├── README.md            # This file
├── images/
│   └── screenshot.png   # (Optional) Screenshot for display
└── ...                  # Other possible files
```

## 🧠 AI Algorithm Overview

- **Minimax** explores all possible future game states up to a given depth.
- **Alpha-Beta pruning** helps eliminate unnecessary branches for faster decision-making.
- Scores are calculated based on how many **SOS** sequences are formed per move.

## 📌 Dependencies

- Only standard Python libraries:
  - `tkinter` (for GUI)
  - `copy` (for deep copying game state)

No installation is needed. This game runs out-of-the-box on any Python 3 environment.

## 📜 License

MIT License.  
Feel free to use, modify, or share!

## 🙋‍♀️ Author
Developed with 💙 by **Yaren**  
For practice and learning purposes as part of an AI course project.

## 🌟 Star this repo if you like it!
