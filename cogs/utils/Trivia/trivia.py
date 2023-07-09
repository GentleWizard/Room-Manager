import cogs.utils.Trivia.Trivia_API as Trivia_API
import random
import html


def get_trivia(category: int = None, difficulty: str = None, type: str = None):
    return Trivia_API.get_question(Category=category, Difficulty=difficulty, Type=type)


def question(trivia):
    # turn the html encocding into a string
    trivia[0]["question"] = html.unescape(trivia[0]["question"])
    return trivia[0]["question"]


def answer(trivia):
    return trivia[0]["correct_answer"]


def incorrect_answers(trivia):
    return trivia[0]["incorrect_answers"]


def all_answers(trivia):
    answers = incorrect_answers(trivia)
    answers.append(answer(trivia))
    return answers


def all_answers_shuffled(trivia):
    answers = all_answers(trivia)
    random.shuffle(answers)
    return answers


def category(trivia):
    return trivia[0]["category"]


def difficulty(trivia):
    return trivia[0]["difficulty"]


def type(trivia):
    return trivia[0]["type"]