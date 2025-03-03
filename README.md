# Advanced Chess Bot

This project implements an advanced chess bot in Python. The bot utilizes the [python‑chess](https://python-chess.readthedocs.io/en/latest/) library and incorporates several advanced techniques to improve decision-making and performance.

## Features

- **Enhanced Evaluation Function:**  
  Combines material count with piece‑square tables to evaluate board positions, with different heuristics for midgame and endgame.

- **Alpha‑Beta Pruning with Transposition Tables:**  
  Optimizes the search process by pruning branches that cannot affect the final decision and caching evaluated positions.

- **Quiescence Search:**  
  Extends search at leaf nodes by considering capture moves to reduce the horizon effect in tactical sequences.

- **Iterative Deepening:**  
  Searches with increasing depth until reaching a maximum depth or time limit, improving move ordering and ensuring a timely response.

- **Adjustable Parameters:**  
  Easily configurable maximum search depth and time limits to balance strength and speed.

## Requirements

- **Python 3.x**  
- **python‑chess** library

You can install the required library using pip:

```bash
pip install python-chess
```

## Usage

1. Clone or download the repository containing the bot's code.
2. Run the bot by executing the Python script:

   ```bash
   python advanced_chess_bot.py
   ```

3. Follow the on-screen instructions:
   - The bot prompts you to enter moves in UCI format (e.g., `e2e4`).
   - Play as White; the bot will respond as Black.

## Code Overview

- **advanced_chess_bot.py:**  
  The main script that implements the chess bot, including:
  - **Board Evaluation:** Uses a combination of material values and positional bonuses from piece‑square tables.
  - **Alpha‑Beta Search with Transposition Table:** Optimizes decision-making by pruning unnecessary branches.
  - **Quiescence Search:** Extends search in tactical positions.
  - **Iterative Deepening:** Ensures the bot finds the best move within a given time limit.

## Future Improvements

- Integrate a graphical user interface (GUI) for enhanced interaction.
- Further refine evaluation heuristics with additional positional analysis.
- Improve move ordering heuristics and add multi-threading for performance gains.

## Contributing

Contributions and suggestions are welcome! Feel free to fork the repository and submit pull requests with improvements or additional features.

Happy coding and enjoy playing with the Advanced Chess Bot!
