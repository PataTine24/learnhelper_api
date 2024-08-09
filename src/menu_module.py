# -*- coding: utf-8 -*-
"""
This module will be used to create all
different menu views.

All menus that send stuff to database should have a submit form,
which reads out all vars from fields that can be changed

"""
import random
from tkinter import ttk

import mysqlmodule as db
import ttkbootstrap as tb
from ttkbootstrap import Window
from settings_class import SettingsManager
from tkinter import messagebox

set_man = SettingsManager()
class ViewManager:
    _instance = None

    def __init__(self):
        if ViewManager._instance is not None:
            raise Exception("This class is a singleton!")
        self._views: dict = {}
        ViewManager._instance = self

    @staticmethod
    def get_instance():
        if ViewManager._instance is None:
            ViewManager()
        return ViewManager._instance

    def add_view(self, view_name, view):
        self._views[view_name] = view

    def get_view_names(self):
        return self._views.keys()

    def get_view(self, view_name):
        return self._views[view_name]

    def get_views(self):
        return self._views.values()

    def get_view_list(self):
        return self._views



def menu_wrapper(*xargs):
    """
    Close program
    Settings Menu
    on specified positions for all views
    :return:
    """
    pass


def start_screen(*xargs):
    """
    Basically the first view/menu/screen shown at the start of the application where you have to choose
    a person for the config/ if not self exists add a new person to DB and save it to personal settings
    if person is set allready in config ( not 0)  then greet the person(or show directly main menu)
    :return:
    """


    pass


def main_menu(*xargs):
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


def start_test_frame(*xargs):
    """
    choose test type (from all types and if there is a parent (question)type show child types)
    choose number of questions (text field)
    Main Menu (Back link)
    opened in menu_wrapper
    :return:
    """
    pass


def test_result_menu(*xargs):
    """
    Shows all questions & answers from one test
    Needs to have a collection for each question + answers belonging to it
    and mark the answers given and show point result on the side.
    opened in menu_wrapper
    :return:
    """
    pass


def test_question_menu(*xargs):
    """
    Shows one question with answers
    and makes it possible to choose
    the answer and go on to next.
    opened in menu_wrapper
    :return:
    """
    pass



def check_test_frame(*xargs):
    """
    Choose a test to look into
    opened in menu_wrapper
    :return:
    """
    pass


def person_menu_frame(*xargs):
    """
    choose between adding/checkin or deleting a person.
    opened in menu_wrapper
    :return:
    """
    pass


def questions_menu_frame(*xargs):
    """
    choose between adding/checkin(updating) or deleting a question.
    opened in menu_wrapper
    :return:
    """
    pass


def settings_menu_frame(*xargs):
    """
    Return to main menu for navigating only
    Change person/login, menu looks and maybe more later
    :return:
    """
    pass
class StartFrame(tb.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        tmp = db.get_person_list()
        self.person_list = []
        self.index_to_id_list = []
        for p_id, person in tmp:
            self.person_list.append(person)
            self.index_to_id_list.append(p_id)

        dropdown_width = max(max(len(item) for item in self.person_list) + 2, 25)

        self.label1 = tb.Label(self, text="Settings sind leer.", font=("Arial", 18), bootstyle="success")
        self.label1.pack(pady=5, padx=30)
        self.label2 = tb.Label(self, text="Wählen sie einen Login aus:", font=("Arial", 18), bootstyle="success")
        self.label2.pack(pady=10, padx=30)

        self.dropdown = tb.Combobox(self, width=25)
        self.dropdown.pack(pady=20, side='top', padx=10)#fill="both", expand=True, pady=20)
        self.dropdown.config(state="readonly")
        self.dropdown['values'] = self.person_list
        self.dropdown.current(0)

        self.forward_button = tb.Button(self, bootstyle="success", text="weiter")
        self.forward_button.pack(padx=20, pady=5)
        self.forward_button.bind("<ButtonRelease-1>", self.continue_to_main)

    def continue_to_main(self, *xargs):
        ind_drop = self.dropdown.current()
        set_man.set_settings_key("person_data", "id", self.index_to_id_list[ind_drop])
        set_man.set_settings_key("person_data", "name", self.person_list[ind_drop])
        ViewManager.get_instance().get_view("main_menu_frame").tkraise()

class MainMenuFrame(tb.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        person_name = set_man.get_settings("person_data", "name")

        lab = tb.Label(self, text=f"Eingeloggt als {person_name}", font=("Consolas", 20), bootstyle="success")
        lab.place(relx=0.5, rely=0.1, anchor='n', bordermode='outside')

        # Dynamische Button-Platzierung
        button_height = 0.1  # Höhe, die jeder Button in Anspruch nimmt (10% des Fensters)
        start_y = 0.3  # Start-Y-Position

        menu_list = [["Start Test", "Check Tests", "Person Menu", "Questions Menu", "Settings"],
                     [start_test_frame, check_test_frame, person_menu_frame, questions_menu_frame, settings_menu_frame]]
        button_width = max(max(len(item) for item in menu_list[0])+2, 25)

        for i in range(len(menu_list[0])):
            link_func = menu_list[1][i]
            button = tb.Button(self, text=menu_list[0][i], bootstyle="success, outline", command=link_func)
            button.place(relx=0.5, rely=start_y + i * button_height, anchor='n', bordermode='outside')
            button.configure(width=button_width)


def on_closing():
    base = ViewManager.get_instance().get_view("base")
    if messagebox.askokcancel("Beenden", "Möchten Sie die Anwendung wirklich schließen?"):
        base.destroy()  # Schließt das Fenster


def test():

    set_man.import_settings()

# # # # # Infos to window and init of window # # # #
    #set_man.set_settings_key("visual_data", "color_scheme", "cosmo")

    scheme = str(set_man.get_settings("visual_data", "color_scheme"))
    if scheme == "default":
        base = tb.Window(themename="litera")
    else:
        base = tb.Window(themename=scheme)

    #set_man.set_settings_key("visual_data", "size", "800x500")

    size = str(set_man.get_settings("visual_data", "size"))
    if size == "default":
        base.geometry("500x350")
    else:
        base.geometry(size)

    base.protocol("WM_DELETE_WINDOW", on_closing)
    base.title("Learnhelper")
    base.grid_rowconfigure(0, weight=1)
    base.grid_columnconfigure(0, weight=1)


# # # # # adding all views to the viewmanager # # # # #

    vm = ViewManager.get_instance()
    vm.add_view("base", base)
    vm.add_view("start_frame", StartFrame(base))

    vm.add_view("main_menu_frame", MainMenuFrame(base))
    vm.add_view("test_start_frame", tb.Frame(base))
    vm.add_view("test_question_frame", tb.Frame(base))
    vm.add_view("test_result_choice_frame", tb.Frame(base))
    vm.add_view("test_result_frame", tb.Frame(base))
    vm.add_view("question_frame", tb.Frame(base))
    vm.add_view("settings_frame", tb.Frame(base))

    liste: dict = vm.get_view_list()
    for key, fr in liste.items():
        if key == "base":
            continue
        else:
            fr.grid(row=0, column=0, sticky='nsew')

    # check if settings already exist, if no we have default of ID 0, then the start frame needs to be called
    if set_man.get_settings("person_data", "id") == 0:
        # need to open the init screen for setting user
        vm.get_view("start_frame").tkraise()
    else:
        vm.get_view("main_menu_frame").tkraise()

    base.mainloop()



if __name__ == "__main__":
    test()

