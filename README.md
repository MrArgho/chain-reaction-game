# chain-reaction-game
A strategy game for 2 players. Here your opponent is an AI agent. AI opponent is build using Minimax algorithm with alpha-pruning. The objective of Chain Reaction is to take control of the board by eliminating your opponents' orbs.
## rules
here are the rules of the Chain Reaction game presented:
* **Objective:** Eliminate your opponents' orbs by creating chain reactions.
* **Setup:** Distribute orbs, place them on the board.
* **Gameplay:**
  * Add orbs to empty cells.
  * Trigger chain reactions using active orbs.
  * When a cell reaches its specific critical mass (usually 1, 2, or 3 orbs), it explodes, causing a chain reaction.
  * **Critical mass:**
    * For corner cell is 1
    * For edge except corners is 2
    * For other cell is 3
* **Winning:** Eliminate all opponents' orbs.
## Prerequisites
This project required a C compiler (gcc prefered) and libraries like SDL2, SDL2_ttf installed on device. Make sure you have them. Clone this repo and open the folder in VS code, then simply run.
## User Interface
### Dash Board
![Screenshot 2023-10-26 190124](https://github.com/MrArgho/chain-reaction-game/assets/103327602/bcce6bc8-6b6c-4cc1-9636-07f2e4ce8ffc)
### Game Play
![Screenshot 2023-10-26 190154](https://github.com/MrArgho/chain-reaction-game/assets/103327602/ad2c718f-5216-4566-894a-9c54bfcb2730)
## Contributors
1. [Argho Deb Das](https://github.com/MrArgho)
2. [Md Hefzul Hossain Papon](https://github.com/RedRiotPapon)

