# TP1

## Description

In this TP, students are required to solve a problem using any of the RL algorithms studied in class, more details on
[document](resources/enunciado.pdf). In my solution, I've solved a Tic Tac Toe game bot using both Monte Carlo ES and
Q-Learning, and then I've compared the results. A [report](resources/TP1_RL1_Maximiliano_Torti.pdf) with the analysis
and conclusions of the work done is available.

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
python src/main.py play --games=<number_of_games> [--bot] [--model-file=<model-file>] [--human]
```

The game starts between two of the three options: human player, a bot and a trained model. The human player can
enter the position where they want to place their symbol. The bot selects a random position on the board and the trained
model plays according to the strategies it learnt. The game continues until there is a winner or the board is
full. Multiple consecutive games can be played using the `--games` option.

## Training a Model

To train a model, run the following command:

```sh
python src/main.py train --model=<model_type> --episodes=<number_of_episodes>
```

The model can be either `q-learning` or `monte-carlo`. The training process will run for the specified number of
episodes, and the model will be saved to a file.

Already trained models are available in the `resources` folder. To play against them, run the following commands:

```sh
python src/main.py play --games=5 --model-file=resources/monte-carlo.pkl
```

```sh
python src/main.py play --games=5 --model-file=resources/q-learning.pkl
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

All code contains documentation. No vulnerabilities or code smells were detected by SonarQube analysis.

