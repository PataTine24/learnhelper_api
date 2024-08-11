# -*- coding: utf-8 -*-
"""
This module will be used to create all
different menu views.

All menus that send stuff to database should have a submit form,
which reads out all vars from fields that can be changed

"""
import random

from abc import abstractmethod, ABC
import mysqlmodule as db
import ttkbootstrap as tb
import ttkbootstrap.constants as tbc
import tkinter as tk
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


# # # # creation fo classes for each "View" (Frame) to show # # # #

# TODO: All Frame widgets need to be changed, so they can be restyled
#  seems like some options used make it impossible to change the looks. Only settings so far works.
class ExFrame(tb.Frame, ABC):
    def __init__(self, master):
        super().__init__(master)
        self._master = master

    @abstractmethod
    def load_me(self, *xargs):
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

        self._save_button = tb.Button(self, text="SAVE", command=self._continue_to_main)
        self._save_button.pack(padx=20, pady=5)


    def _continue_to_main(self, *xargs):
        # TODO: Check if entry exists from DB before setting it in local data (anti hack)
        ind_drop = self.dropdown.current()
        set_man.set_settings_key("person_data", "id", self.index_to_id_list[ind_drop])
        set_man.set_settings_key("person_data", "name", self.person_list[ind_drop])
        ViewManager.get_instance().get_view("MainMenuFrame").load_me()

    def load_me(self, *xargs):
        # no use, because this frame will only be loaded if no person is set, so only once at first start of app
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
        menu_list = [["Start Test", "Check Tests",  "Questions Menu", "Person Menu", "Settings"],
                     ["StartTestFrame", "CheckTestFrame",  "QuestionMenuFrame", "PersonMenuFrame", "SettingsFrame"]]
        button_width = max(max(len(item) for item in menu_list[0])+2, 25)

        for i in range(len(menu_list[0])):
            button = tb.Button(self, text=menu_list[0][i], bootstyle="success, outline",
                               command=lambda x=i: self.load_frame(menu_list[1][x]))
            button.place(relx=0.5, rely=start_y + i * button_height, anchor='n', bordermode='outside')
            button.configure(width=button_width)

    def load_frame(self, frameName:str):
        ViewManager.get_instance().get_view(frameName).load_me()

    def load_me(self, *xargs):
        person_name = set_man.get_settings("person_data", "name")
        self.login_label.config(text=f"Eingeloggt als {person_name}")
        self.tkraise()


# TODO: StartTestFrame
class StartTestFrame(ExFrame):
    """
        choose test type (from all types and if there is a parent (question)type show child types)
    choose number of questions (text field)
    Main Menu (Back link)
    """
    def __init__(self, master):
        super().__init__(master)

        self._start_button = tb.Button(self, text="Start Test", command=self._start_test)
        self._start_button.pack()

        self._cancel_button = tb.Button(self, text="CANCEL", command=self._cancel)
        self._cancel_button.pack()

    def _start_test(self):
        new_test_id = 999
        ViewManager.get_instance().get_view("TestResultFrame").load_me(new_test_id)
    def _cancel(self):
        ViewManager.get_instance().get_view("MainMenuFrame").load_me()

    def load_me(self, *xargs):
        self.tkraise()



# TODO:  class TestQuestionFrame
class TestQuestionFrame(ExFrame):
    """    Shows one question with answers
    and makes it possible to choose
    the answer and go on to next."""
    def __init__(self, master):
        super().__init__(master)
        # TODO: remove this temp stuff:
        self._question_infos_label = tb.Label(self, text="Test Infos")
        self._question_infos_label.grid(row=0, column=0, sticky=tbc.NSEW)

        # end
        self._is_singlechoice = True
        self._question_text = ["popp", "bjkdjkawkdwada", "dhdusuidsuauhdn uidhauiui :duah w WDn  !!:;Jkd", "hdjdjd122"]
        self._answer_text_a = ["bananas", "sting", "lastline"]
        self._answer_text_b = ["!hdhdh", "stong"]
        self._answer_text_c = ["hepp", "-", "space"]
        self._answer_text_d = ["boop", "doop", ]
        self._answer_value_a = 123
        self._answer_value_b = 121
        self._answer_value_c = 124
        self._answer_value_d = 122

        # Configure rows and columns in the main frame
        self.grid_rowconfigure(0, weight=1)  # Upper div
        self.grid_rowconfigure(1, weight=1)  # Middle div
        self.grid_rowconfigure(2, weight=0)  # Bottom div
        self.grid_columnconfigure(0, weight=1)  # Full width

        # Upper div - 50% of the screen height
        upper_frame = tb.Frame(self, padding="10")
        upper_frame.grid(row=0, column=0, sticky=tbc.NSEW)

        # Large read-only text area in the upper div
        self.question_area = tb.Text(upper_frame, wrap=tbc.WORD, height=10, state='disabled')
        self.question_area.pack(fill=tbc.BOTH, expand=True)



        # Middle div - 30% of the screen height
        middle_frame = tb.Frame(self, padding="10")
        middle_frame.grid(row=1, column=0, sticky=tbc.NSEW)

        # Configure rows in the middle frame
        for i in range(4):
            middle_frame.grid_rowconfigure(i, weight=1)

        # Create four boxes with radio buttons and text areas
        self.radio_var = tk.StringVar()  # Variable to hold the selected radio button
        win_width = set_man.get_settings("visual_data", "resolution")[0]
        answer_width = win_width//7

        for i in range(4):
            row_frame = tb.Frame(middle_frame, padding="5")
            row_frame.grid(row=i, column=0, sticky=tbc.NSEW)

            if self._is_singlechoice:
                # Radio button
                radio_button = tb.Radiobutton(row_frame, variable=self.radio_var,
                                               value=None)
                # TODO: Set value for answers
                radio_button.pack(side=tbc.LEFT, padx=(0, 10))
            else:
                checkbox = tb.Checkbutton(row_frame)
                checkbox.pack(side=tbc.LEFT, padx=(0, 10))
            # Read-only text area
            text_area = tb.Text(row_frame, height=2, width=answer_width, state='disabled', wrap=tbc.WORD)
            text_area.pack(side=tbc.LEFT, fill=tbc.BOTH, expand=True)

        # Bottom div - 20% of the screen height
        bottom_frame = tb.Frame(self, padding="10")
        bottom_frame.grid(row=2, column=0, sticky=tbc.EW)

        # Add buttons to the bottom frame
        left_button = tb.Button(bottom_frame, text="Left Button")
        left_button.pack(side=tbc.LEFT, padx=(0, 10))

        right_button = tb.Button(bottom_frame, text="Right Button")
        right_button.pack(side=tbc.RIGHT)

    def _add_radio_buttons(self):
        pass

    def _add_checkboxes(self):
        pass

    def load_me(self, question_id: int = None, *xargs):
        if question_id is None:
            raise ValueError("TestQuestionFrame allways needs a question id")
        else:
            self._question_infos_label.config(text=f"question id: {question_id}")


# TODO: class CheckTestFrame
class CheckTestFrame(ExFrame):
    """Choose a test to look into
    Only the persons own,
    later people can have pupils, where they can also check into"""
    def __init__(self, master):
        super().__init__(master)

        self.dropdown = tb.Combobox(self)
        self.dropdown.pack(pady=20, side='top', padx=10)
        self.dropdown.config(state="readonly")
        self.dropdown['values'] = ["empty"]
        self.dropdown.current(0)
        self._dropdown_indexes = []
        self._dropdown_values = []

        self._check_button = tb.Button(self, text="CHECK", command=self._check)
        self._check_button.pack()
        self._cancel_button = tb.Button(self, text="CANCEL", command=self._cancel)
        self._cancel_button.pack()

    def _cancel(self):
        ViewManager.get_instance().get_view("MainMenuFrame").load_me()

    def _check(self):
        test_id = self._dropdown_indexes[self.dropdown.current()]
        ViewManager.get_instance().get_view("TestResultFrame").load_me(test_id)
        pass

    def load_me(self, *xargs):
        set_id: int = set_man.get_settings("person_data", "id")
        taken_test = db.get_tests_by_person_id(set_id)
        self._dropdown_indexes = []
        self._dropdown_values = []
        for t_id, _, _, num_questions, start_time, _, test_type_name, _ in taken_test:
            self._dropdown_indexes.append(t_id)
            self._dropdown_values.append(f"{test_type_name} ({num_questions}Q) | {start_time}")
        dropdown_width = max(max(len(item) for item in self._dropdown_values) + 2, 35)
        self.dropdown.config(width=dropdown_width)
        self.dropdown['values'] = self._dropdown_values
        self.dropdown.current(0)
        self.tkraise()


# TODO: class TestResultFrame
class TestResultFrame(ExFrame):
    """
    Shows all questions & answers from one test
    Will be called after a test is finished and shows that test only
    Needs to have a collection for each question + answers belonging to it
    and mark the answers given and show point result on the side.
    """
    def __init__(self, master):
        super().__init__(master)
        self._test_infos_label = tb.Label(self, text="Test Infos")
        self._test_infos_label.pack()
        self._cancel_button = tb.Button(self, text="CANCEL", command=self._cancel)
        self._cancel_button.pack()

    def _cancel(self):
        ViewManager.get_instance().get_view("MainMenuFrame").load_me()

    def load_me(self, test_id: int = None, *xargs):
        if test_id is None:
            raise ValueError("The TestResultFrame can only be loaded with a test id!")
        else:
            self._test_infos_label.config(text=f"TEST ID: {test_id}")
            self.tkraise()



# TODO: class QuestionMenuFrame
class QuestionMenuFrame(ExFrame):
    """choose between adding/checkin(updating) or deleting a question."""
    def __init__(self, master):
        super().__init__(master)

        self._cancel_button = tb.Button(self, text="CANCEL", command=self._cancel)
        self._cancel_button.pack()

    def _cancel(self):
        ViewManager.get_instance().get_view("MainMenuFrame").load_me()

    def load_me(self, *xargs):
        self.tkraise()


# TODO: format the widgets / align them properly
#  ??? Should also be able to set the login
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

        self._gen_themes = self._master.style.theme_names()
        self._dropdown_themes = tb.Combobox(self, values=self._gen_themes, state="readonly")
        self._dropdown_themes.set(self._master.style.theme_use())
        self._dropdown_themes.pack()
        # TODO: Add example widgets to show the visual change
        self._d_res_values = [f"{key}: {value[0]}x{value[1]}"for key, value in self._dict_resolution.items()]
        self._dropdown_resolution = tb.Combobox(self, values=self._d_res_values, state="readonly")
        self._dropdown_resolution.current(0)
        self._dropdown_resolution.pack()

        self._apply_button = tb.Button(self, text="APPLY", command=self._apply_changes)
        self._apply_button.pack()

        self._save_button = tb.Button(self, text="SAVE CHANGES", command=self._save_changes)
        self._save_button.pack()

        self._cancel_button = tb.Button(self, text="CANCEL", command=self._drop_changes)
        self._cancel_button.pack()

    def _apply_changes(self):
        self._master.style.theme_use(self._dropdown_themes.get())
        ind = self._dropdown_resolution.current()

        selected_key = list(self._dict_resolution.keys())[ind]
        x_y = self._dict_resolution[selected_key]

        screen_width = self._master.winfo_screenwidth()
        screen_height = self._master.winfo_screenheight()
        position_right = int(screen_width / 2 - x_y[0] / 2)
        position_down = int(screen_height / 2 - x_y[1] / 2)

        self._master.geometry(f"{x_y[0]}x{x_y[1]}+{position_right}+{position_down}")


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


# TODO: format the widgets / align them properly
#  choose between adding/checkin or deleting a person.
#  Add a recheck before updating/deleteing/adding with quotes: "Anna Banana" trim spaces end/start
#  maybe with radio buttons the 3 options choosing? Using another frame build up based on button set
class PersonMenuFrame(ExFrame):
    def __init__(self, master):
        super().__init__(master)
        tmp = db.get_person_list()

        set_id = set_man.get_settings("person_data", "id")
        self.person_list = []
        self.index_to_id_list = []
        for p_id, person in tmp:
            self.person_list.append(person)
            self.index_to_id_list.append(p_id)

        self.label = tb.Label(self, text="Wählen sie einen Login aus:")
        self.label.pack(pady=10, padx=30)

        dropdown_width = max(max(len(item) for item in self.person_list) + 2, 25)
        self.dropdown = tb.Combobox(self, width=dropdown_width)
        self.dropdown.pack(pady=20, side='top', padx=10)
        self.dropdown.config(state="readonly")
        self.dropdown['values'] = self.person_list
        if set_id == 0:
            self.dropdown.current(0)
        else:
            self.dropdown.current(self.index_to_id_list.index(set_id))

        self._save_button = tb.Button(self, text="SAVE CHANGES", command=self._save_changes)
        self._save_button.pack()

        self._cancel_button = tb.Button(self, text="CANCEL", command=self._drop_changes)
        self._cancel_button.pack()

    def _save_changes(self):

        set_man.set_settings_key("person_data", "id", self.index_to_id_list[self.dropdown.current()])
        set_man.set_settings_key("person_data", "name", self.person_list[self.dropdown.current()])
        ViewManager.get_instance().get_view("MainMenuFrame").load_me()

    def _drop_changes(self):
        ViewManager.get_instance().get_view("MainMenuFrame").load_me()

    def load_me(self, *xargs):
        set_id = set_man.get_settings("person_data", "id")
        tmp = db.get_person_list()
        self.person_list = []
        self.index_to_id_list = []
        for p_id, person in tmp:
            self.person_list.append(person)
            self.index_to_id_list.append(p_id)
        self.dropdown['values'] = self.person_list
        self.dropdown.current(self.index_to_id_list.index(set_id))
        self.tkraise()



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
    root_window.resizable(width=False, height=False)

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
    vm.add_view("StartTestFrame", StartTestFrame(base))
    vm.add_view("TestQuestionFrame", TestQuestionFrame(base))
    vm.add_view("CheckTestFrame", CheckTestFrame(base))
    vm.add_view("TestResultFrame", TestResultFrame(base))
    vm.add_view("QuestionMenuFrame", QuestionMenuFrame(base))
    vm.add_view("SettingsFrame", SettingsFrame(base))
    vm.add_view("PersonMenuFrame", PersonMenuFrame(base))
    vm.add_view("TestResultFrame", TestResultFrame(base))

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
       #vm.get_view("TestQuestionFrame").tkraise()

    base.mainloop()



if __name__ == "__main__":
    test()

