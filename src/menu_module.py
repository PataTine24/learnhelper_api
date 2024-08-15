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
from mysqlmodule import NoQuestionError
import ttkbootstrap as tb
import ttkbootstrap.constants as tbc
import tkinter as tk
from settings_class import SettingsManager
from tkinter import messagebox
from ttkbootstrap.dialogs import Messagebox as MBox

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

def change_entry(element_entry, text: str) -> None:
    element_entry.config(state="normal")
    element_entry.delete(0, tbc.END)
    element_entry.insert(0, text)
    element_entry.config(state="readonly")

def change_text(element_text, text: str) -> None:
    element_text.config(state="normal")
    element_text.delete("1.0", tbc.END)
    element_text.insert("1.0", text)
    element_text.config(state="disabled")

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


# TODO: StartTestFrame formatting
class StartTestFrame(ExFrame):
    """
        choose test type (from all types and if there is a parent (question)type show child types)
    choose number of questions (text field)
    Main Menu (Back link)
    """
    def __init__(self, master):
        super().__init__(master)

        self._test_type_list = []
        self._dropdown_test_types = tb.Combobox(self, values=[""], state="readonly")
        self._dropdown_test_types.bind("<<ComboboxSelected>>", self._change_dropdown)
        self._dropdown_test_types.current(0)
        self._dropdown_test_types.pack()
        self._extra_var = tb.StringVar()
        self._extra_var.set("")

        self._dropdown_extra = tb.Entry(self, textvariable=self._extra_var, state="readonly")
        self._dropdown_extra.pack()

        # FIXME: if you wrote one number you cant delete teh one number anymore
        check_num = self.register(self._check_num)
        self._number_field = tb.Entry(self, width=2, validate="key", validatecommand=(check_num, "%P"))
        self._number_field.pack()

        self._start_button = tb.Button(self, text="Start Test", command=self._start_test)
        self._start_button.pack()

        self._cancel_button = tb.Button(self, text="CANCEL", command=self._cancel)
        self._cancel_button.pack()

    def _check_num(self, in_value):
        # Allow empty input (when deleting)
        if in_value == "":
            return True

        if len(in_value) <= 2 and in_value.isnumeric():
            return True
        return False

    def _change_dropdown(self, *xargs):
        self._extra_var.set(self._test_type_list[self._dropdown_test_types.current()][3])

    def _start_test(self):
        t_type_id = self._test_type_list[self._dropdown_test_types.current()][0]

        try:
            num_questions = int(self._number_field.get())
            person_id = set_man.get_settings("person_data", "id")
            person_id = int(str(person_id))
        except ValueError as err:
            print(err)
        else:
            self._new_test_id = db.add_taken_test(person_id, t_type_id, num_questions)
            self._load_test_question(num_questions)

    def _load_test_question(self, num_questions):
        try:
            question_id = db.add_new_random_question_to_test(self._new_test_id)
        except NoQuestionError as err:
            # TODO: alert there are no questions in that type
            #  delete taken_test_id from DB
            conf_win = MBox.show_warning(message=f"Sorry! No Questions Available for\n{self._test_type_list[
                self._dropdown_test_types.current()][1]}", title="NoQuestionError")
            db.delete_taken_test(self._new_test_id)
            ViewManager.get_instance().get_view("MainMenuFrame").load_me()

        else:
            ViewManager.get_instance().get_view("TestQuestionFrame").load_me(question_id, self._new_test_id, num_questions)

    def _cancel(self):
        ViewManager.get_instance().get_view("MainMenuFrame").load_me()

    def load_me(self, *xargs):
        self._number_field.delete(0, "end")
        self._test_type_list = db.get_test_type_list()
        self._dropdown_test_types.configure(values=[entry[1] for entry in self._test_type_list])
        self._dropdown_test_types.current(0)
        self._extra_var.set(self._test_type_list[self._dropdown_test_types.current()][3])
        self.tkraise()



# TODO:  class TestQuestionFrame
#  Add usability friendliness, click in frame of answer = click on radio button or checkbox (no small click areas)
class TestQuestionFrame(ExFrame):
    """    Shows one question with answers
    and makes it possible to choose
    the answer and go on to next."""
    def __init__(self, master):
        super().__init__(master)
        #test values, otherwise None
        self._question_id = 5
        self._test_id = 30 # TODO: needs to be set to 0 at start
        self._test_type_name = "Empty"

        tmp_q = db.get_question_by_id(self._question_id)
        self._question_value = tmp_q[2]
        self._number_of_questions = 0
        self._finished_questions = 0
        self._is_single_choice = bool(tmp_q[3])

        tmp_answer = db.get_answers_by_question_id(self._question_id)
        self._answer_text_value_list = []
        self._answer_value_list = []

        self._radio_var = tb.IntVar()
        self._checkbox_values = [tb.BooleanVar(), tb.BooleanVar(), tb.BooleanVar(), tb.BooleanVar()]

        for a_id, _, a_value,_ in tmp_answer:
            self._answer_text_value_list.append(a_value)
            self._answer_value_list.append(a_id)

        # all widgets init, no packing!

        self._upper_frame = tb.Frame(self, padding="5")
        self._upper_frame.grid(row=0, column=0, sticky="nsew")
        self._middle_frame = tb.Frame(self, padding="5")
        self._middle_frame.grid(row=1, column=0, sticky="nsew")
        self._bottom_frame = tb.Frame(self, padding="5")
        self._bottom_frame.grid(row=2, column=0, sticky="nsew")

        self._question_infos_label = tb.Label(self._upper_frame, text="Test Infos")
        self._question_text_widget = tb.Text(self._upper_frame, state="disabled", width=100, height=13)

       # # # #  add each element for answers # # # #
        self._add_answer_elements()

        self._cancel_test_button = tb.Button(self._bottom_frame, text="Cancel Test", command=self._cancel)
        self._next_button = tb.Button(self._bottom_frame, text="Next Question", command=self._submit_answers)

        # packing /layouting
        self._question_infos_label.pack()
        self._question_text_widget.pack()
        self._cancel_test_button.pack(side="left")
        self._next_button.pack(side="right")

        # # # # set values AFTER packing only! # # # #
        change_text(self._question_text_widget, self._question_value)


    def _add_answer_elements(self):
        self._answer_frames = []
        self._answer_boxes = []
        self._answer_text_widgets = []


        for index in range(4):
            self._answer_frames.append(tb.Frame(self._middle_frame, padding="2"))
            if self._is_single_choice:
                self._answer_boxes.append(
                    tb.Radiobutton(self._answer_frames[index], variable=self._radio_var,
                                   value=self._answer_value_list[index]))
            else:
                self._answer_boxes.append(tb.Checkbutton(
                    self._answer_frames[index], variable=self._checkbox_values[index]))
            self._answer_text_widgets.append(tb.Text(self._answer_frames[index], state="disabled", width=96, height=2))
            self._answer_frames[index].grid(row=index)
            self._answer_boxes[index].grid(row=index, column=0)
            self._answer_text_widgets[index].grid(row=index, column=1)
            # TODO: Could be list of strings, proper check is needed here for multiline answers and inline code
            text_tmp = "".join(self._answer_text_value_list[index])
            change_text(self._answer_text_widgets[index], text_tmp)

    def _cancel(self):
        self._finished_questions = 0
        ViewManager.get_instance().get_view("MainMenuFrame").load_me()

    # TODO: If max numbers of questions, dont try to grab new question!
    def _submit_answers(self):
        if self._is_single_choice:  # radio buttons
            db.add_test_answer(self._test_id, self._question_id, self._radio_var.get())

        else: #checkboxes
            for index, boxes in enumerate(self._checkbox_values):
                if boxes.get():
                    print(self._test_id, self._question_id, self._answer_value_list[index])
                    print(type(self._test_id), type(self._question_id), type(self._answer_value_list[index]))
                    db.add_test_answer(self._test_id, self._question_id, self._answer_value_list[index])

        # check if any more questions are available
        try:
            n_question_id = db.add_new_random_question_to_test(self._test_id)
        except NoQuestionError as err:
            self._finished_questions = 0
            ViewManager.get_instance().get_view("MainMenuFrame").load_me()

        else:
            self._finished_questions += 1
            self.load_me(question_id=n_question_id, test_id=self._test_id)

    def load_me(self, question_id: int = None, test_id: int = None, num_questions: int = None, *xargs):
        if question_id is None:
            raise ValueError("TestQuestionFrame allways needs a question_id")
        elif test_id is None:
            raise ValueError("TestQuestionFrame allways needs a test_id")
        else:
            self._question_id = question_id

            if not self._test_id == test_id:  # if new test
                if num_questions is None:
                    raise ValueError("TestQuestionFrame allways needs a num_questions var")
                else:
                    self._number_of_questions = num_questions

            self._test_id = test_id

            q_entry = db.get_question_by_id(question_id)
            self._is_single_choice = bool(q_entry[3])
            self._question_infos_label.config(text=f"{self._finished_questions}/{self._number_of_questions}             "
                                                   f"       {self._test_type_name}            Question Starttime: {q_entry[4]}")
            question_text = q_entry[2]
            change_text(self._question_text_widget, question_text)

            tmp_answer = db.get_answers_by_question_id(self._question_id)
            self._answer_text_value_list = []
            self._answer_value_list = []
            self._radio_var.set(0)
            for box in self._checkbox_values:
                box.set(False)
            for a_id, _, a_value, _ in tmp_answer:
                self._answer_text_value_list.append(a_value)
                self._answer_value_list.append(a_id)


            for index, answer in enumerate(tmp_answer):
                change_text(self._answer_text_widgets[index], answer[2])

                if self._is_single_choice:
                    self._answer_boxes.append(
                        tb.Radiobutton(self._answer_frames[index], variable=self._radio_var,
                                       value=self._answer_value_list[index]))
                else:
                    self._answer_boxes.append(tb.Checkbutton(
                        self._answer_frames[index], variable=self._checkbox_values[index]))

                self._answer_boxes[index].grid(row=index, column=0)

                # TODO: Could be list of strings, proper check is needed here for multiline answers and inline code
                text_tmp = "".join(self._answer_text_value_list[index])
                change_text(self._answer_text_widgets[index], text_tmp)

            # for index in range(4):
            #     self._answer_frames.append(tb.Frame(self._middle_frame, padding="2"))
            #     if self._is_single_choice:
            #         self._answer_boxes.append(
            #             tb.Radiobutton(self._answer_frames[index], variable=self._radio_var,
            #                            value=self._answer_value_list[index]))
            #     else:
            #         self._answer_boxes.append(tb.Checkbutton(
            #             self._answer_frames[index], variable=self._checkbox_values[index]))
            #     self._answer_text_widgets.append(
            #         tb.Text(self._answer_frames[index], state="disabled", width=96, height=2))
            #     self._answer_frames[index].grid(row=index)
            #     self._answer_boxes[index].grid(row=index, column=0)
            #     self._answer_text_widgets[index].grid(row=index, column=1)
            #     # TODO: Could be list of strings, proper check is needed here for multiline answers and inline code
            #     text_tmp = "".join(self._answer_text_value_list[index])
            #     change_text(self._answer_text_widgets[index], text_tmp)

            # self._question_id = 5
            # self._test_id = 30  # TODO: needs to be set to 0 at start
            # self._test_type_name = "Empty"
            #
            # tmp_q = db.get_question_by_id(self._question_id)
            # self._question_value = tmp_q[2]
            # self._number_of_questions = 0
            # self._finished_questions = 0
            # self._is_single_choice = bool(tmp_q[3])
            #
            # tmp_answer = db.get_answers_by_question_id(self._question_id)
            # self._answer_text_value_list = []
            # self._answer_value_list = []
            # for a_id, _, a_value, _ in tmp_answer:
            #     self._answer_text_value_list.append(a_value)
            #     self._answer_value_list.append(a_id)

            # answer 0-3 values
            # radio or checkbox
            # daher löschen der elemente
            #
            #



            # TODO: change all values in the view
            self.tkraise()


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
#  Add a recheck before updating/deleting/adding with quotes: "Anna Banana" trim spaces end/start
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


# TODO: change to the proper area in code



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
    db.end()


if __name__ == "__main__":
    test()

