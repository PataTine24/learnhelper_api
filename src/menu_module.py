# -*- coding: utf-8 -*-
"""
This module will be used to create all
different menu views.

All menus that send stuff to database should have a submit form,
which reads out all vars from fields that can be changed

"""
import random
import mysqlmodule as db


def menu_wrapper():
    """
    Close program
    Settings Menu
    on specified positions for all views
    :return:
    """
    pass


def start_screen():
    """
    Basically the first view/menu/screen shown at the start of the application where you have to choose
    a person for the config/ if not self exists add a new person to DB and save it to personal settings
    if person is set allready in config ( not 0)  then greet the person(or show directly main menu)
    :return:
    """

    pass


def main_menu():
    """
    Needs to have  link to
    test_start_menu
    check_test_menu
    person_menu (add/delete/update)
    questions_menu (add/delete/update)
    opened in menu_wrapper
    :return:
    """
    pass


def test_start_menu():
    """
    choose test type (from all types and if there is a parent (question)type show child types)
    choose number of questions (text field)
    Main Menu (Back link)
    opened in menu_wrapper
    :return:
    """
    pass


def test_result_menu():
    """
    Shows all questions & answers from one test
    Needs to have a collection for each question + answers belonging to it
    and mark the answers given and show point result on the side.
    opened in menu_wrapper
    :return:
    """
    pass


def test_question_menu():
    """
    Shows one question with answers
    and makes it possible to choose
    the answer and go on to next.
    opened in menu_wrapper
    :return:
    """
    pass


def check_test_menu():
    """
    Choose a test to look into
    opened in menu_wrapper
    :return:
    """
    pass


def person_menu():
    """
    choose between adding/checkin or deleting a person.
    opened in menu_wrapper
    :return:
    """
    pass


def questions_menu():
    """
    choose between adding/checkin(updating) or deleting a question.
    opened in menu_wrapper
    :return:
    """
    pass


def settings_menu():
    """
    Return to main menu for navigating only
    Change person/login, menu looks and maybe more later
    :return:
    """
    pass


if __name__ == "__main__":
    print("This module is not working on its own so far")

