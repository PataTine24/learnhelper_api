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


# # # # creation fo classes for each "View" (Frame) to show # # # #

# TODO: All Frame widgets need to be changed, so they can be restyled
#  seems like some options used make it impossible to change the looks. Only settings so far works.
class ExFrame(tb.Frame):
    def __init__(self, master):
        super().__init__(master)
        self._master = master

    def load_me(self, *xargs):
        self.tkraise()
        pass

class StartFrame(ExFrame):
    def __init__(self, master):
        super().__init__(master)
        tmp = db.get_person_list()

        self.person_list = []
        self.index_to_id_list = []
        for p_id, person in tmp:
            self.person_list.append(person)
            self.index_to_id_list.append(p_id)



        self.label1 = tb.Label(self, text="Settings sind leer.", font=("Arial", 18), bootstyle="success")
        self.label1.pack(pady=5, padx=30)
        self.label2 = tb.Label(self, text="Wählen sie einen Login aus:", font=("Arial", 18), bootstyle="success")
        self.label2.pack(pady=10, padx=30)

        dropdown_width = max(max(len(item) for item in self.person_list) + 2, 25)
        self.dropdown = tb.Combobox(self, width=dropdown_width)
        self.dropdown.pack(pady=20, side='top', padx=10)#fill="both", expand=True, pady=20)
        self.dropdown.config(state="readonly")
        self.dropdown['values'] = self.person_list
        self.dropdown.current(0)

        self.forward_button = tb.Button(self, bootstyle="success", text="weiter")
        self.forward_button.pack(padx=20, pady=5)
        self.forward_button.bind("<ButtonRelease-1>", self.continue_to_main)

    def continue_to_main(self, *xargs):
        # TODO: Check if entry exists from DB before setting it in local data (anti hack)
        ind_drop = self.dropdown.current()
        set_man.set_settings_key("person_data", "id", self.index_to_id_list[ind_drop])
        set_man.set_settings_key("person_data", "name", self.person_list[ind_drop])
        ViewManager.get_instance().get_view("MainMenuFrame").load_me()

    def load_me(self, *xargs):

        pass


class MainMenuFrame(ExFrame):
    def __init__(self, master):
        super().__init__(master)

        person_name = set_man.get_settings("person_data", "name")
        self.login_label = tb.Label(self, text=f"Eingeloggt als {person_name}", font=("Consolas", 20), bootstyle="success")
        self.login_label.place(relx=0.5, rely=0.1, anchor='n', bordermode='outside')

        # Dynamische Button-Platzierung
        button_height = 0.1  # Höhe, die jeder Button in Anspruch nimmt (10% des Fensters)
        start_y = 0.3  # Start-Y-Position
        # TODO: Later do all text things with a language file, based on user language and default in english
        #  so we can change per language what you see (Only menus, but not questions & answers)
        menu_list = [["Start Test", "Check Tests", "Person Menu", "Questions Menu", "Settings"],
                     ["TestStartFrame", "CheckTestFrame", "PersonMenuFrame", "QuestionMenuFrame", "SettingsFrame"]]
        button_width = max(max(len(item) for item in menu_list[0])+2, 25)

        # FIXME: seems like the lambda is allways calling the SettingsFrame or better the button event allways calls it
        for i in range(len(menu_list[0])):
            button = tb.Button(self, text=menu_list[0][i], bootstyle="success, outline",
                               command=lambda: self.load_frame(menu_list[1][i]))
            button.place(relx=0.5, rely=start_y + i * button_height, anchor='n', bordermode='outside')
            button.configure(width=button_width)

    def load_frame(self, frameName:str):
        print(frameName)
        ViewManager.get_instance().get_view(frameName).load_me()

    def load_me(self, *xargs):
        person_name = set_man.get_settings("person_data", "name")
        self.login_label.config(text=f"Eingeloggt als {person_name}")
        self.tkraise()


# TODO: TestStartFrame
class TestStartFrame(ExFrame):
    def __init__(self, master):
        super().__init__(master)

    def load_me(self, *xargs):
        pass


# TODO:  class TestQuestionFrame
class TestQuestionFrame(ExFrame):
    def __init__(self, master):
        super().__init__(master)

    def load_me(self, *xargs):
        pass


# TODO: class CheckTestFrame
class CheckTestFrame(ExFrame):
    def __init__(self, master):
        super().__init__(master)

    def load_me(self, *xargs):
        pass


# TODO: class TestResultFrame
class TestResultFrame(ExFrame):
    def __init__(self, master):
        super().__init__(master)

    def load_me(self, *xargs):
        pass


# TODO: class QuestionMenuFrame
class QuestionMenuFrame(ExFrame):
    def __init__(self, master):
        super().__init__(master)

    def load_me(self, *xargs):
        pass


# TODO: class SettingsFrame
class SettingsFrame(ExFrame):
    def __init__(self, master):
        super().__init__(master)
        self._dict_resolution: dict[str, tuple[int, int]] = {
            "VGA(4:3)": (640, 480),
            "SVGA(4:3)": (800, 600),
            "XGA(4:3)": (1024, 768),
            "HD(16:9)": (1280, 720),
            "WXGA(16:10)": (1280, 800),
            "HD(16:9)": (1366, 768),
            "WXGA+(16:10)": (1440, 900),
            "HD+(16:9)": (1600, 900),
            "WSXGA+(16:10)": (1680, 1050),
            "FULL HD (16:9)": (1920, 1080),
            "WUXGA(16:10)": (1920, 1200),
            "QHD/2K(16:9)": (2560, 1440),
            "WQXGA(16:10)": (2560, 1600),
            "4K UHD(16:9)": (3840, 2160),
            "5K(16:9)": (5120, 2880),
            "8K(16:9)": (7680, 4320)}
        self._theme_list = [
            "litera",
            "cerulean",
            "cosmo",
            "cyborg",
            "darkly",
            "flatly",
            "journal",
            "lumen",
            "lux",
            "minty",
            "morph",
            "pulse",
            "sandstone",
            "simplex",
            "sketchy",
            "slate",
            "solar",
            "spacelab",
            "superhero",
            "united",
            "yeti"]
        self._gen_themes = self._master.style.theme_names()
        self._dropdown_themes = tb.Combobox(self, values=self._gen_themes, state="readonly")
        self._dropdown_themes.set(self._master.style.theme_use())
        self._dropdown_themes.pack(pady=20, padx=50)

        self._d_res_values = [f"{key}: {value[0]}x{value[1]}"for key, value in self._dict_resolution.items()]
        self._dropdown_resolution = tb.Combobox(self, values=self._d_res_values, state="readonly")
        self._dropdown_resolution.current(0)
        self._dropdown_resolution.pack(pady=20, padx=10)

        self._apply_button = tb.Button(self, text="APPLY", command=self._apply_changes)
        self._apply_button.pack(pady=60, padx=10)

        self._save_button = tb.Button(self, text="SAVE CHANGES", command=self._save_changes)
        self._save_button.pack(pady=60, padx=50)

        self._cancel_button = tb.Button(self, text="CANCEL", command=self._drop_changes)
        self._cancel_button.pack(pady=60, padx=100)

    def _apply_changes(self):
        self._master.style.theme_use(self._dropdown_themes.get())
        ind = self._dropdown_resolution.current()

        selected_key = list(self._dict_resolution.keys())[ind]
        entry = self._dict_resolution[selected_key]

        new_res = f"{entry[0]}x{entry[1]}"
        self._master.geometry(new_res)

    def _save_changes(self):
        new_theme = self._dropdown_themes.get()
        ind = self._dropdown_resolution.current()

        selected_key = list(self._dict_resolution.keys())[ind]
        reso = self._dict_resolution[selected_key]

        set_man.set_settings_key("visual_data", "resolution", reso)
        set_man.set_settings_key("visual_data", "theme", new_theme)
        ViewManager.get_instance().get_view("MainMenuFrame").load_me()

    def _drop_changes(self):
        ViewManager.get_instance().get_view("MainMenuFrame").load_me()

    def load_me(self, *xargs):
        self._dropdown_themes.set(self._master.style.theme_use())
        self._dropdown_resolution.current(0)
        self.tkraise()


# TODO: class PersonSettingsFrame
class PersonSettingsFrame(ExFrame):
    def __init__(self, master):
        super().__init__(master)

    def load_me(self, *xargs):
        pass


# TODO: class PersonMenuFrame
class PersonMenuFrame(ExFrame):
    def __init__(self, master):
        super().__init__(master)

    def load_me(self, *xargs):
        pass


# # # #  Function for changing what is happening on window close # # # #
def on_closing():
    base = ViewManager.get_instance().get_view("base")
    if messagebox.askokcancel("Beenden", "Möchten Sie die Anwendung wirklich schließen?"):
        # TODO: Save stuff based on position the person is on (like in a test)
        base.destroy()  # Schließt das Fenster


# TODO: change to proper area in code



def set_window_properties():
    """
    Here we configure how the window will be looking
    We also check for settings here and implement these here
    """
    #set_man.set_settings_key("visual_data", "color_scheme", "cyborg")

    theme = str(set_man.get_settings("visual_data", "theme"))
    # FIXME: Seems like this has a problem with different themes?
    #  Maybe they are changing different things we dont see in our project so far
    root_window = tb.Window(themename=theme)

    #set_man.set_settings_key("visual_data", "size", (800, 600))
    # size now returns a tuple (x,y) which is getting unpacked here
    window_width, window_height = set_man.get_settings("visual_data", "resolution")

    root_window.protocol("WM_DELETE_WINDOW", on_closing)
    root_window.title("Learnhelper")

    screen_width = root_window.winfo_screenwidth()
    screen_height = root_window.winfo_screenheight()
    # use this t position the window in the middle of the screen
    position_right = int(screen_width / 2 - window_width / 2)
    position_down = int(screen_height / 2 - window_height / 2)

    root_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")
    root_window.minsize(640, 480)
    root_window.maxsize(width=screen_width, height=screen_height)
    root_window.resizable(width=True, height=True)

    # add grinds, only if needed
    root_window.grid_rowconfigure(0, weight=1)
    root_window.grid_columnconfigure(0, weight=1)

    return root_window
def test():
    # TODO: Change this to the mainfile. In this file should only be the init of frames
    set_man.import_settings()

# # # # # Infos to window and init of window # # # #

    base = set_window_properties()

# # # # # adding all views to the viewmanager # # # # #

    vm = ViewManager.get_instance()
    vm.add_view("base", base)
    vm.add_view("StartFrame", StartFrame(base))

    vm.add_view("MainMenuFrame", MainMenuFrame(base))
    vm.add_view("TestStartFrame", TestStartFrame(base))
    vm.add_view("TestQuestionFrame", TestQuestionFrame(base))
    vm.add_view("CheckTestFrame", CheckTestFrame(base))
    vm.add_view("TestResultFrame", TestResultFrame(base))
    vm.add_view("QuestionMenuFrame", QuestionMenuFrame(base))
    vm.add_view("SettingsFrame", SettingsFrame(base))
    vm.add_view("PersonSettingsFrame", PersonSettingsFrame(base))
    vm.add_view("PersonMenuFrame", PersonMenuFrame(base))

    list_views: dict = vm.get_view_list()
    for key, fr in list_views.items():
        if key == "base":
            continue
        else:
            fr.grid(row=0, column=0, sticky='nsew')

    # check if settings already exist, if no we have default of ID 0, then the start frame needs to be called
    # FIXME: We need to load the view new(init it new) to get the right infos in it , like person data
    if set_man.get_settings("person_data", "id") == 0:
        # need to open the init screen for setting user
        vm.get_view("StartFrame").tkraise()
    else:
        vm.get_view("MainMenuFrame").tkraise()

    base.mainloop()



if __name__ == "__main__":
    test()

