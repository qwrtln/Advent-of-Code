from enum import Enum
from common import read_file


class Symbol(str, Enum):
    ROCK = "ROCK"
    PAPER = "PAPER"
    SCISSORS = "SCISSORS"


class Result(str, Enum):
    WIN = "WIN"
    LOSE = "LOSE"
    DRAW = "DRAW"


OPPONENT = {
    "A": Symbol.ROCK,
    "B": Symbol.PAPER,
    "C": Symbol.SCISSORS,
}

YOU = {
    "X": Result.LOSE,
    "Y": Result.DRAW,
    "Z": Result.WIN,
}

SYMBOL_SCORE = {
    Symbol.ROCK: 1,
    Symbol.PAPER: 2,
    Symbol.SCISSORS: 3,
}

WIN_SCORE = {
    Result.WIN: 6,
    Result.DRAW: 3,
    Result.LOSE: 0,
}

WINNING_MOVES = [
    (Symbol.PAPER, Symbol.SCISSORS),
    (Symbol.SCISSORS, Symbol.ROCK),
    (Symbol.ROCK, Symbol.PAPER),
]

WINNING_MAPPING = {
    Symbol.PAPER: Symbol.SCISSORS,
    Symbol.SCISSORS: Symbol.ROCK,
    Symbol.ROCK: Symbol.PAPER,
}

LOSING_MAPPING = {v: k for k, v in WINNING_MAPPING.items()}


def find_result(opp_symbol: Symbol, your_symbol: Symbol) -> Result:
    if opp_symbol == your_symbol:
        return Result.DRAW
    if (opp_symbol, your_symbol) in WINNING_MOVES:
        return Result.WIN
    return Result.LOSE


def find_right_move(opp_symbol: Symbol, result: Result) -> Symbol:
    if result == Result.DRAW:
        return opp_symbol
    if result == Result.WIN:
        return WINNING_MAPPING[opp_symbol]
    return LOSING_MAPPING[opp_symbol]


def find_score(opp_move: str, your_move: str) -> int:
    opp_symbol = OPPONENT[opp_move]
    result = YOU[your_move]
    your_symbol = find_right_move(opp_symbol, result)
    score = SYMBOL_SCORE[your_symbol]
    result = find_result(opp_symbol, your_symbol)
    score += WIN_SCORE[result]
    return score


if __name__ == "__main__":
    puzzle_lines = read_file("02").split("\n")[:-1]
    score = 0
    for line in puzzle_lines:
        score += find_score(*line.split(" "))
    print(score)
