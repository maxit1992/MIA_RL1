# TP1

## Description

In this TP, students are required to solve a problem using Monte Carlo. My implementation is based on Tic Tac Toe game.

## Requirements

- Python 3.8 or higher
- pytest to run the tests

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/maxit1992/MIA_RL1.git
    cd MIA_RL1/tp1
    ```

2. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Running the Game

To start the game, run the following command:

```sh
python src/main.py play --games=<number_of_games> [--bot] [--monte_carlo=<model_file>] [--human]
```

The game starts between two of the three options: human player, a bot and a Monte Carlo model. The human player can
enter the position where they want to place their symbol. The bot selects a random position on the board and the Monte
Carlo model plays according to the strategies it learnt. The game continues until there is a winner or the board is
full. Multiple consecutive games can be played using the `--games` option.

## Training the Monte Carlo Model

To train the Monte Carlo model, run the following command:

```sh
python src/main.py train --episodes=<number_of_episodes>
```

## Running Tests

To run the tests, use the following command:

```sh
pytest
```

## Running Coverage

To get the code coverage, use the following command:

```sh
coverage run -m pytest
coverage report
```

## Code Quality

No vulnerabilities or code smells were detected by SonarQube analysis.

