# метод вычисления процента правильности:
# число правильных ответов / максимальное количество правильных ответов * 100

import random


file_name = "test.txt"   # файл, из которого читаются вопросы
questions_count = 20     # количество вопросов в тесте
random_questions = True  # перемешать вопросы
random_answers = True    # перемешать варианты ответов

# статистика проходящего тест
user = {
    "right": 0,
    "wrong": 0
}

# максимально число очков за тест, используется в подсчёте результатов
max_points = 0


def get_questions(file_name):
    """Читает вопросы из файла."""

    global questions_count
    global random_questions
    global random_answers

    questions = []

    with open(file_name, encoding="utf-8") as f:
        text = f.read()

    objects = text.split("\n\n")

    for object in objects:
        lines = object.split("\n")

        answers = []
        for line in lines[1:]:
            answer = {
                "text": line[2:],
                "right": True if int(line[0]) == 1 else False
            }
            answers.append(answer)

        if random_answers is True:
            random.shuffle(answers)

        question = {
            "text": lines[0][lines[0].find(")") + 1:],
            "answers": answers
        }

        questions.append(question)

    if random_questions is True:
        random.shuffle(questions)

    questions = questions[:questions_count]

    return questions


def print_question(question, number):
    """Выводит на экран вопрос и варианты ответов."""

    # + 1 чтобы нумерация шла не с нуля, в дальнейшем это учтено
    print("{}. {}".format(number + 1, question["text"]))

    for i in range(len(question["answers"])):
        print("{}) {}".format(i + 1, question["answers"][i]["text"]))


def answering(question, user_answer, user):
    """Обработка ответа на вопрос."""

    global max_points

    # собираем список правильных ответов
    right_answers = []
    for i in range(len(question["answers"])):
        if question["answers"][i]["right"] is True:
            right_answers.append(i + 1)

    max_points += len(right_answers)

    user_answer = user_answer.split()

    if len(user_answer) == 0:
        # если пользователь ничего не ответил
        user["wrong"] += len(right_answers)
    else:
        user_answer = [int(num) for num in user_answer]

        if len(set(right_answers) & set(user_answer)) == len(right_answers):
            # все ответы верные
            print("Всё верно!")
        else:
            # некоторые или все неверные
            print("Правильные ответы: " + " ".join([str(item) for item in right_answers]))

        user["right"] += len(set(right_answers) & set(user_answer))
        user["wrong"] += len(set(user_answer) - set(right_answers))


def print_result(user, max_points):
    """Выводит на экран результаты теста."""

    print("""_____РЕЗУЛЬТАТЫ_____
Правильных ответов: {}
Неправильных ответов: {}
Процент правильности: {:.2f}""".format(user["right"], user["wrong"],
                                   user["right"] / max_points * 100))


questions = get_questions(file_name)

for i in range(len(questions)):
    print_question(questions[i], i)

    user_answer = input("Ваш ответ: ")

    if user_answer == "стоп":
        break

    answering(questions[i], user_answer, user)

    print()
else:
    # тест пройден, выводим результаты
    print_result(user, max_points)
