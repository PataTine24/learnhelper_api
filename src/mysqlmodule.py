# -*- coding: utf-8 -*-
"""
mysqlModule description:
This module adds the functionality to set,get, update and delete data from
the learnhelper database.

Starter problems:
Pycharm uses a virtual environment, which is NOT LOADING automatically
the packages installed on windows.
So you should add the packages via pyCharms package manger or via pyCharms console with pip install
Every project maybe needs to have the librarys installed each time, because each project is one virtual area.


"""

import mysql.connector
from os import path
import traceback


class NoQuestionError(Exception):
    def __init__(self, message: str = None, error_code=None):
        if message is None:
            message = f"There is no more Questions for that test type with that test_id."
        else:
            self.message = message
        super().__init__(message)
        self.error_code = error_code
        self.traceback = ''.join(traceback.format_stack())

learnhelper = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="learnhelper"
)

# need to be called in the main program if the program gets closed
def end():
    learnhelper.close()

def no_commit(proc_name, *xproc_args) -> None | list[list]:
    """
    Runs a procedure with *xproc_args and commits the results.\n
    if the procedure returns smth. its also returned.
    :param proc_name: string
    :return: list[list[]]
    """

    mycursor = learnhelper.cursor()

    for x in xproc_args:
        if type(x) is str:
            x = string_to_sql_string(x)
    mycursor.callproc(proc_name, args=(xproc_args))
    result: list = []
    for s in mycursor.stored_results():
        rows = s.fetchall()
    for row in rows:
        result.append(list(row))

    mycursor.close()
    return result


def with_commit(proc_name, *xproc_args) -> None | list[list]:
    """
    Runs a procedure with *xproc_args and commits the results.\n
    if the procedure returns smth. its also returned.
    :param proc_name: string
    :return: list[list[]]
    """
    mycursor = learnhelper.cursor()
    for x in xproc_args:
        if type(x) is str:
            x = string_to_sql_string(x)

    mycursor.callproc(proc_name, args=(xproc_args))
    learnhelper.commit()
    result: list = []
    # TODO:  Handle this better with if and checks instead of try! Or catch the right exception only
    try:
        for s in mycursor.stored_results():
            rows = s.fetchall()

        for row in rows:
            result.append(list(row))
    except Exception:
        # catches all exceptions, not wanted, imagine timeout exception happens....
        result = None

    mycursor.close()
    return result


def string_to_sql_string(in_string: str) -> str:
    """
    This function will check a string for special sings needed for \n
    questions & answers. to MD readable and in SQL savable.\n
    returns the changed string
    :param in_string: str
    :return: str
    """
    out_string = in_string
    return "\"" + out_string + "\""


# GET from DB
def get_person_infos_by_id(p_id: int) -> list[str, object, int]:
    """
    Returns person data:\n
    ['ZERO', datetime.datetime(2024, 7, 11, 9, 15, 45), 0]\n
    [name, timestamp, no. of tests]
    :param p_id: int
    :return: list
    """
    return no_commit("get_person_infos_by_id", p_id)[0]


def get_test_type_list() -> list[list[int, str, int | None, str]]:
    """
    Returns a list of test types formated like this:\n
    [[1, 'Python All Topics', None, 'NO PARENT'],[...]...]
    :return: list
    """
    return no_commit("get_test_types_with_main_type")

def get_tests_by_person_id(person_id: int):
    """
    Returns a list of test taken tests:\n
    [[25, 1, 2, 20, datetime.datetime(2024, 7, 12, 17, 12, 48), 2, 'Python Basics', 1],[...], ...]
    [[test_id, person_id, test_type_id, number_of_questions, start_timestamp,
    test_type_id, test_type_name, parent_test_type],[...],...]
    :return: list
    """
    return no_commit("get_tests_by_person_id", person_id)


def get_test_answer_and_question_ids_by_test_id(test_id: int) -> list[int]:
    """
    Returns a list of test answer and question ids formated like this:\n
    [[12, 6], [11, 6], [7, 8], [6, 8]]\n
    [[answer_id, question_id],[...],...]
    :param test_id:
    :return: list
    """
    return no_commit("get_test_answer_and_question_ids_by_test_id", test_id)


def get_answers_by_question_id(question_id: int) -> list[list[int, int, str, int]]:
    """
    Returns a list of answers formated like this:\n
    [[29, 8, '.txt', 1], [30, 8, '.csv', 1], [32, 8, '.masterblaster', 1], [31, 8, '.jpg', 1]]\n
    [[answer_id, question_id, answer, is_correct],[...],...]\n
    is_correct is a boolean value, but returns 0 or 1 for it.
    :param question_id:
    :return: list
    """
    return no_commit("get_answers_by_question_id", question_id)


def get_question_by_id(question_id: int) -> list[list]:
    """
    Returns a question formated like this:\n
    [3, 2, 'How do you convert another primitive datatype into a string?', 0, datetime.datetime(2024, 7, 10, 16, 36, 48)]
    [question_id, test_type_id, question_content, singlechoice, timestamp]\n
    singlechoice is a boolean value, but returns 0 or 1 for it.
    :param question_id:
    :return: list
    """
    return no_commit("get_question_by_id", question_id)[0]


def get_question_infos_by_test_id(test_id: int) -> list[list]:
    """
    returns a list of question info formated like this:\n
    [[1, datetime.datetime(2024, 8, 15, 19, 4, 8), datetime.datetime(2024, 8, 15, 19, 4, 10)], [...],...]
    [[id, startime, endtime],[...],...]
    :param test_id: int
    :return: list[list[int, datetime, datetime]]
    """
    result = no_commit("get_question_infos_by_test_id", test_id)
    return result


def get_person_list():
    # TODO: docstring
    return no_commit("get_person_list")


# ADD to DB
def add_single_choice_question(question: str, question_type: int, correct_answer: str,
                               wrong_answer1: str, wrong_answer2: str, wrong_answer3: str) -> None:
    """
    Adds a single choice question to the database.\n
    Needs all these parameters to be valid.
    :param question: str(2000)
    :param question_type: int
    :param correct_answer: str(255)
    :param wrong_answer1: str(255)
    :param wrong_answer2: str(255)
    :param wrong_answer3: str(255)
    :return: None
    """
    with_commit("add_single_choice_question", question, question_type,
                correct_answer, wrong_answer1, wrong_answer2, wrong_answer3)


def add_multiple_choice_question(question: str, question_type: int, answer1: str, answer2: str, answer3: str,
                                 answer4: str, answer1_correct: bool, answer2_correct: bool,
                                 answer3_correct: bool, answer4_correct: bool) -> None:
    """
    Adds a multiple choice question to the database.\n
    Needs all these parameters to be valid.
    :param question: str(2000)
    :param question_type: int
    :param answer1: str(255)
    :param answer2: str(255)
    :param answer3: str(255)
    :param answer4: str(255)
    :param answer1_correct: bool
    :param answer2_correct: bool
    :param answer3_correct: bool
    :param answer4_correct: bool
    :return: None
    """

    with_commit("add_question", question, question_type, False, answer1, answer2, answer3, answer4,
                answer1_correct, answer2_correct, answer3_correct, answer4_correct)


def add_taken_test(person_id: int, test_type_id: int, number_of_questions: int) -> int:
    """
    Starts a new test and returns its id.
    :param person_id: int
    :param test_type_id: int
    :param number_of_questions: int
    :return: int
    """
    result = with_commit("add_taken_test", person_id, test_type_id, number_of_questions)

    return result[0][0]


def add_test_answer(test_id: int, question_id: int, answer_id: int) -> None:
    """
    Adds to a answer to a test. Needs test, question and answer_id
    :param test_id: int
    :param question_id: int
    :param answer_id: int
    :return: None
    """
    with_commit("add_test_answer", test_id, question_id, answer_id)


def add_new_random_question_to_test(test_id: int) -> int:
    """
    Returns new question id or 0 if testype not found(test_id wrong) or if NO new question available.\n
    WARNING! Under specific conditions this could duplicate questions asked.\n
    This conditions are unknown and need further testing!\n
    Or no new question is added.\n
    Raises a "NoQuestionError" if there is no question left, so you need to catch that.
    :param test_id: int
    :return: int
    """
    result = with_commit("add_new_random_question_to_test", test_id)
    if result[0][0] == 0:
        raise NoQuestionError
    return result[0][0]


def add_test_type(test_type_content: str, main_type_id: int | None) -> None:
    """
    Adds a new test type to the database.\n
    Choose the None type (Not "None" as string!) if its a new main type
    :param test_type_content: str(63)
    :param main_type_id: int
    :return: None
    """
    with_commit("add_test_type", test_type_content, main_type_id)


def add_end_time_by_test_id_and_question_id(test_id: int, question_id: int) -> None:
    with_commit("add_end_time_by_test_id_and_question_id", test_id, question_id)
def add_person(user_name: str, email:str, password_clean:str):

    password_hash = password_clean
    with_commit("add_person", user_name, email, password_hash)

# DELETE from DB
def delete_person_data(person_id: int) -> None:
    """
    Deletes person data from database based on person_id\n
    Including taken test and the answers to it.
    :param person_id: int
    :return: None
    """
    with_commit("delete_person_data", person_id)


def delete_taken_test(test_id: int) -> None:
    """
    Deletes taken test from the database.\n
    Including questions and the answer history.
    :param test_id: int
    :return: None
    """
    with_commit("delete_taken_test", test_id)


# # # # # Code to test # # # # #
# TODO: On release remove test block
def test():
    quest_id = 3
    # maybe you need to change the ID you give out for testing (database AUTO_INCREMENT can be a lil tricky sometimes)
    # to check use mysql workbench and show the questions table and take one ID form there
    print("Testing:")
    print(get_answers_by_question_id(quest_id))
    # better readable:
    for _, _, answer, correct in get_answers_by_question_id(quest_id):
        print("[CORRECT]" if correct == 1 else "[WRONG]", answer)
    # there can be line breaks if you print answers/questions! because they can contain line breaks in string

    # almost everything will be given out as 2d list like this
    # [[values, values], [otherValues, otherValues], ...]
    # so you need to format them properly.

if __name__ == "__main__":

    test()

