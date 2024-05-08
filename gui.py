__author__ = "AndyVoyager"

from pathlib import Path
import tkinter
from tkinter import *
from tkinter import ttk, messagebox
import values as vl
import customtkinter as ctk
from PIL import Image
import brain
from db import read_top_3_scores, add_score

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH_FRAME0 = OUTPUT_PATH / Path(r"//Users/Luck777/Documents/Python/Python Proffesional Portfolio/"
                                        r"Typing_Speed_Test_App/build/assets/frame0")
ASSETS_PATH_FRAME1 = OUTPUT_PATH / Path(r"/Users/Luck777/Documents/Python/Python Proffesional "
                                        r"Portfolio/Typing_Speed_Test_App/build/assets/frame1")
ASSETS_PATH_FRAME2 = OUTPUT_PATH / Path(r"/Users/Luck777/Documents/Python/Python Proffesional Portfolio/"
                                        r"Typing_Speed_Test_App/build/assets/frame2")
WINDOW_POSITION = "1240x864+200+50"

# Set colors:
BACKGROUND_COLOR = "#FAFAF8"
RECTANGLE_COLOR = "#3776E8"
TEXT_COLOR = "#080016"

FONT_TYPE = "AppleBraille Outline8Dot"


def relative_to_assets(path: str, assets_path) -> Path:
    """
    Returns the absolute path of a file relative to the assets' directory.

    Parameters:
        path (str): The relative path of the file.
        assets_path (Path): The path to the assets' directory.

    Returns:
        Path: The absolute path of the file.
    """
    return assets_path / Path(path)


class App(tkinter.Tk):
    def __init__(self):
        super().__init__()

        self.title("Typing Speed Test App")
        self.geometry(WINDOW_POSITION)
        self.minsize(800, 600)
        self.configure(bg=BACKGROUND_COLOR)
        self.resizable(True, True)

        self.frame = None
        self.check_values = True

        self.values = vl.Values()
        self.brain = brain.Brain()

        self.start_over()

    def start_test(self):
        """
        Executes the test scenario by setting the values on the frame.
        Handles AttributeErrors gracefully.
        Clears the scores, destroys widgets, and initializes a new TestFrame.
        Returns the TestFrame object.
        """
        try:
            self.frame.set_values()
        except AttributeError:
            pass

        # Check if values are correct:
        if not self.check_values:
            return
        self.brain.clear_scores()
        brain.destroy_widgets(self)
        self.frame = TestFrame(self)
        return self.frame

    def finish_test(self):
        """
        This function finishes the test scenario by destroying widgets and creating a new ScoreFrame.
        Returns the ScoreFrame object.
        """
        brain.destroy_widgets(self)

        self.frame = ScoreFrame(self)

        return self.frame

    def start_over(self):
        """
        Clears the scores, destroys widgets, and initializes a new MainFrame object.
        """
        try:
            if self.frame:
                brain.destroy_widgets(self)
                self.frame.destroy()
        except AttributeError:
            print("no frame yet")
        finally:
            self.brain.clear_scores()
            self.frame = MainFrame(self)

        return self.frame


class MainFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Create MainFrame
        self.parent = parent
        self.parent.title("Typing Speed Test App")
        self.parent.geometry(WINDOW_POSITION)
        self.parent.minsize(800, 600)
        self.parent.resizable(False, False)

        # Variables:
        self.image_image_1 = None
        self.image_image_2 = None
        self.image_image_3 = None
        self.combobox_image_1 = None
        self.combobox_image_2 = None
        self.button_image_1 = None
        self.canvas = None
        self.combobox_1 = None
        self.combobox_2 = None
        self.top_3_scores = read_top_3_scores()

        self.create_widgets()

    def set_values(self):
        """
        Sets the values of the comboboxes in the GUI.

        This function takes the selected values from the comboboxes in the GUI and sets them in the corresponding
        attributes of the parent object. It also checks if the values are valid and displays error messages if
         necessary.
        """
        # Take data from comboboxes:
        time_value = self.combobox_1.get()
        level_value = self.combobox_2.get()
        self.parent.brain.generate_text(level_value)

        if time_value:
            # print(time_value)
            self.parent.values.set_time(time_value)
            self.parent.check_values = True
        else:
            messagebox.showwarning("Time Error", "Please select a time")
            self.parent.check_values = False
            return

        if level_value:
            # print(level_value)
            self.parent.values.set_level(level_value)
            self.parent.check_values = True
        else:
            messagebox.showwarning("Level Error", "Please select a level")
            self.parent.check_values = False

    def create_widgets(self):
        """
        Generate all the necessary widgets and elements for the user interface.
        Creates canvas with specific dimensions and styles, labels, buttons, comboboxes, icons, and text elements.
        """
        self.canvas = Canvas(
            self.parent,
            bg=BACKGROUND_COLOR,
            height=864,
            width=1240,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        # Create top right label with text:
        self.canvas.place(x=0, y=0)
        brain.round_rectangle(self.canvas, x1=635, y1=40, x2=1184, y2=176,
                              radius=40, fill=RECTANGLE_COLOR, outline="")
        self.canvas.create_text(
            720.0,
            103.0,
            anchor="w",
            text="TYPING SPEED TEST",
            fill=TEXT_COLOR,
            font=(FONT_TYPE, 40 * -1)
        )

        # Create bottom right label with text:
        brain.round_rectangle(self.canvas, x1=635, y1=376, x2=1184, y2=513,
                              fill=RECTANGLE_COLOR, outline="")
        self.canvas.create_text(
            725,
            403,
            anchor="nw",
            text="Check your typing skills in a minute.",
            fill=TEXT_COLOR,
            font=(FONT_TYPE, 24 * -1)
        )
        self.canvas.create_text(
            795,
            460,
            anchor="nw",
            text="SELECT YOUR TEST",
            fill=TEXT_COLOR,
            font=(FONT_TYPE, 24 * -1)
        )

        # Create Start Button:
        self.button_image_1 = ctk.CTkImage(
            light_image=Image.open(relative_to_assets("button_1.png", ASSETS_PATH_FRAME0)),
            dark_image=Image.open(relative_to_assets("button_1.png", ASSETS_PATH_FRAME0)),
            size=(102, 102))
        button_1 = ctk.CTkButton(
            self.parent,
            image=self.button_image_1,
            command=self.parent.start_test,
            hover_color=RECTANGLE_COLOR,
            text="",
            width=102,
            height=102,
            fg_color=BACKGROUND_COLOR, )
        button_1.place(
            x=1085.0,
            y=589.0
        )

        # Create Combobox choose time:
        self.combobox_1 = ctk.CTkComboBox(self.parent,
                                          values=vl.choose_time(),
                                          button_color=RECTANGLE_COLOR,
                                          fg_color=BACKGROUND_COLOR,
                                          text_color=TEXT_COLOR,
                                          font=(FONT_TYPE, 20 * -1),
                                          state="readonly",
                                          justify="center",
                                          cursor="watch",
                                          height=41, width=325,
                                          corner_radius=20)
        self.combobox_1.place(x=730, y=578)

        # Create Combobox 2 choose Level:
        self.combobox_2 = ctk.CTkComboBox(self.parent,
                                          values=vl.choose_level(),
                                          button_color=RECTANGLE_COLOR,
                                          fg_color=BACKGROUND_COLOR,
                                          text_color=TEXT_COLOR,
                                          font=(FONT_TYPE, 20 * -1),
                                          state="readonly",
                                          justify="center",
                                          cursor="watch",
                                          height=41, width=325,
                                          corner_radius=20)
        self.combobox_2.place(x=730, y=661)

        # Create level icon:
        self.image_image_1 = PhotoImage(
            file=relative_to_assets("image_1.png", ASSETS_PATH_FRAME0))
        image_1 = self.canvas.create_image(
            668, 681,
            image=self.image_image_1
        )

        # Create time icon:
        self.image_image_2 = PhotoImage(
            file=relative_to_assets("image_2.png", ASSETS_PATH_FRAME0))
        image_2 = self.canvas.create_image(
            668, 599,
            image=self.image_image_2
        )

        # Create top left text label:
        brain.round_rectangle(self.canvas, 55, 44, 394, 297,
                              radius=40,
                              fill=RECTANGLE_COLOR, outline="")
        # Text "Best Score":
        self.canvas.create_text(
            150, 60,
            anchor="nw",
            text="BEST SCORES",
            fill=TEXT_COLOR,
            font=(FONT_TYPE, 22 * -1)
        )
        # Inside round rectangle:
        brain.round_rectangle(self.canvas, 100, 105, 341, 270,
                              radius=40,
                              fill=BACKGROUND_COLOR, outline="")
        # First position:
        self.canvas.create_text(
            122,
            140,
            anchor="center",
            text="1",
            fill=RECTANGLE_COLOR,
            font=(FONT_TYPE, 36 * -1)
        )
        self.canvas.create_text(
            180,
            140,
            anchor="center",
            text=f"{self.top_3_scores[0][1]}",
            fill=TEXT_COLOR,
            font=(FONT_TYPE, 36 * -1)
        )

        # Second position:
        self.canvas.create_text(
            121,
            186,
            anchor="center",
            text="2",
            fill=RECTANGLE_COLOR,
            font=(FONT_TYPE, 36 * -1)
        )
        self.canvas.create_text(
            180,
            186,
            anchor="center",
            text=f"{self.top_3_scores[1][1]}",
            fill=TEXT_COLOR,
            font=(FONT_TYPE, 36 * -1)
        )

        # Third position:
        self.canvas.create_text(
            122,
            232,
            anchor="center",
            text="3",
            fill=RECTANGLE_COLOR,
            font=(FONT_TYPE, 36 * -1)
        )
        self.canvas.create_text(
            180,
            232,
            anchor="center",
            text=f"{self.top_3_scores[2][1]}",
            fill=TEXT_COLOR,
            font=(FONT_TYPE, 36 * -1)
        )

        # Copyright label:
        self.canvas.create_text(
            1190,
            800,
            anchor="e",
            text="© 2024 Andrii Yavorskyi",
            fill=TEXT_COLOR,
            font=(FONT_TYPE, 20 * -1)
        )

        self.image_image_3 = PhotoImage(
            file=relative_to_assets("image_3.png", ASSETS_PATH_FRAME0))
        image_3 = self.canvas.create_image(
            275.0,
            607,
            image=self.image_image_3
        )


class TestFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Create Test Frame
        self.button_image_2 = None
        self.button_1 = None
        self.accuracy_label = None
        self.wpm_label = None
        self.cpm_label = None
        self.entry_1 = None
        self.text_speed = None
        self.timer_label = None
        self.entry_image_1 = None
        self.image_image_2 = None
        self.image_image_1 = None
        self.canvas = None
        self.button_image_1 = None
        self.parent = parent

        parent.title("Typing Speed Test App")
        parent.geometry(WINDOW_POSITION)
        parent.minsize(800, 600)
        parent.resizable(False, False)

        self.create_widgets()
        self.create_timer_label()

    def enter_check(self, event):
        """
        A function that checks the input entry, compares it with the frame text, deletes the entry text, and gets the
        next part text.
        Calculates CPM, WPM, and Accuracy based on the timer label text and updates the corresponding labels.

        Parameters:
            event: The event trigger for the function.
        """
        if self.entry_1:
            self.parent.brain.count += 1

            # Compare entry text with frame text:
            self.parent.brain.compare_text_with_canvas_text(self.entry_1.get(),
                                                            self.canvas.itemcget(self.text_speed, "text"))
            # Delete entry text:
            self.entry_1.delete(0, 'end')
            # Get next part text:
            self.canvas.itemconfig(self.text_speed, text=self.parent.brain.get_text_parts())

        # Calculate CPM, WPM, ACCURACY:
        self.parent.brain.calculate_speed(self.timer_label.cget("text"), canvas=self.canvas,
                                          cpm_label=self.cpm_label,
                                          wpm_label=self.wpm_label,
                                          accuracy_label=self.accuracy_label)

    def start_timer(self):
        """
        Starts the timer for the test.

        This function initializes the total time in seconds for the test based on the value provided by the user.
         It then calls the `start_countdown` method of the `parent.brain` object to start the countdown timer.
         The timer is started with the specified number of minutes, and the `label` and `func` parameters are passed to
         update the timer label and execute the `finish_test` method of the `parent` object when the timer reaches zero.

        After starting the timer, the function shows the first part of the text on the canvas by calling the
        `itemconfig` method of the `canvas` object and passing the `text_speed` item and the result of
        the `get_text_parts` method of the `parent.brain` object.

        The function also updates the start button image and command to show the "Start Over" button and execute
        the `start_over` method of the `parent` object when clicked.

        Finally, the function places the entry text on the canvas and binds the `<Return>` key to trigger
         the `enter_check` method of the current object.
        """

        time = self.parent.values.time
        self.parent.brain.total_time_in_sec = time

        # Start timer:
        self.parent.brain.start_countdown(minutes=time,
                                          label=self.timer_label,
                                          func=self.parent.finish_test)

        # Show first part of text:
        self.entry_1.delete(0, 'end')
        self.canvas.itemconfig(self.text_speed, text=self.parent.brain.get_text_parts(), fill=BACKGROUND_COLOR)

        # Hide start button:
        self.button_image_2 = ctk.CTkImage(
            light_image=Image.open(relative_to_assets("button_2.png", ASSETS_PATH_FRAME1)),
            dark_image=Image.open(relative_to_assets("button_2.png", ASSETS_PATH_FRAME1)),
            size=(102, 102))
        self.button_1.configure(image=self.button_image_2, command=self.parent.start_over)

        # Show entry text when timer starts:
        self.entry_1.place(
            x=112,
            y=510,
        )
        self.entry_1.focus()
        self.entry_1.bind("<Return>", self.enter_check)

    def create_timer_label(self):
        """
        Creates a timer label on the canvas with the specified time text.

        This function initializes the timer label using the provided time_text and styling settings.
        The timer label is displayed on the canvas at the specified coordinates (x=130, y=95).
        """
        time_text = self.parent.values.time_text
        # Create Timer Label
        self.timer_label = ctk.CTkLabel(self.canvas, text=f"{time_text}",
                                        font=(FONT_TYPE, 24 * -1),
                                        fg_color=BACKGROUND_COLOR, text_color=RECTANGLE_COLOR, )
        self.timer_label.place(x=130, y=95)

    def create_widgets(self):
        """
        Creates and initializes all the widgets and elements for the GUI.

        This function creates and places all the widgets and elements required for the GUI, such as the canvas, images,
         text, buttons, and labels. It also initializes the necessary variables and sets up the layout of the GUI.

        Parameters:
            self (TestFrame): The instance of the TestFrame class.

        Returns:
            None
        """
        # Create Canvas:
        self.canvas = Canvas(
            self.parent,
            bg=BACKGROUND_COLOR,
            height=864,
            width=1240,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        # Create image background:
        self.image_image_1 = PhotoImage(
            file=relative_to_assets("image_1.png", ASSETS_PATH_FRAME1))
        image_1 = self.canvas.create_image(
            269.0,
            623.0,
            image=self.image_image_1
        )

        # Create Top Right Frame with text::
        brain.round_rectangle(self.canvas,
                              445, 40, 1185, 169,
                              fill=RECTANGLE_COLOR,
                              outline="")

        self.canvas.create_text(
            590, 50,
            anchor="nw",
            text="TYPING SPEED TEST\nTest your typing skills",
            fill=TEXT_COLOR,
            font=(FONT_TYPE, 48 * -1)
        )

        # Crate Bottom Test Frame:
        brain.round_rectangle(self.canvas,
                              75,
                              409,
                              1163,
                              616,
                              fill=RECTANGLE_COLOR,
                              outline="")
        self.text_speed = self.canvas.create_text(
            112,
            440,
            anchor="nw",
            text="Please, press START button to start the test.",
            fill=TEXT_COLOR,
            font=(FONT_TYPE, 36 * -1)
        )

        # Create Entry Frame:
        self.entry_image_1 = ctk.CTkImage(
            light_image=Image.open(relative_to_assets("entry_1.png", ASSETS_PATH_FRAME1)),
            dark_image=Image.open(relative_to_assets("entry_1.png", ASSETS_PATH_FRAME1)),
            size=(620, 512))
        self.entry_1 = ctk.CTkEntry(
            self.canvas,
            placeholder_text="Type here",
            width=1000,
            height=42,
            fg_color=BACKGROUND_COLOR,
            font=(FONT_TYPE, 36 * -1),
            text_color=RECTANGLE_COLOR
        )

        # Create Button Start:
        self.button_image_1 = ctk.CTkImage(
            light_image=Image.open(relative_to_assets("button_1.png", ASSETS_PATH_FRAME0)),
            dark_image=Image.open(relative_to_assets("button_1.png", ASSETS_PATH_FRAME0)),
            size=(102, 102))
        self.button_1 = ctk.CTkButton(
            self.canvas,
            image=self.button_image_1,
            hover_color=RECTANGLE_COLOR,
            width=102,
            height=102,
            text="",
            fg_color=BACKGROUND_COLOR,
            command=self.start_timer,
        )
        self.button_1.place(
            x=567.0,
            y=669.0,
        )

        # Create Time Frame on Top Left:
        brain.round_rectangle(self.canvas,
                              55,
                              40,
                              265,
                              168,
                              fill=RECTANGLE_COLOR,
                              outline="")
        self.canvas.create_text(
            130,
            50,
            anchor="nw",
            text="Time:",
            fill=TEXT_COLOR,
            font=(FONT_TYPE, 24 * -1)
        )
        brain.round_rectangle(self.canvas,
                              98,
                              83,
                              225,
                              136,
                              fill=BACKGROUND_COLOR,
                              outline="")

        # Create words/min Frame on Center:
        brain.round_rectangle(self.canvas,
                              290,
                              225,
                              455,
                              354,
                              fill=RECTANGLE_COLOR,
                              outline="")
        self.canvas.create_text(
            375,
            245,
            anchor="center",
            text="words/min",
            fill=TEXT_COLOR,
            font=(FONT_TYPE, 20 * -1)
        )
        brain.round_rectangle(self.canvas,
                              325,
                              269,
                              425,
                              321,
                              fill=BACKGROUND_COLOR,
                              outline="")
        self.wpm_label = self.canvas.create_text(
            375,
            295,
            anchor="center",
            text="0",
            fill=TEXT_COLOR,
            font=(FONT_TYPE, 32 * -1)
        )

        # Create accuracy % Frame on center:
        brain.round_rectangle(self.canvas,
                              782,
                              225,
                              947,
                              354,
                              fill=RECTANGLE_COLOR,
                              outline="")
        self.canvas.create_text(
            865,
            245,
            anchor="center",
            text="% accurancy",
            fill=TEXT_COLOR,
            font=(FONT_TYPE, 20 * -1)
        )
        brain.round_rectangle(self.canvas,
                              816,
                              269,
                              916,
                              321,
                              fill=BACKGROUND_COLOR,
                              outline="")
        self.accuracy_label = self.canvas.create_text(
            865,
            295,
            anchor="center",
            text="0",
            fill=TEXT_COLOR,
            font=(FONT_TYPE, 32 * -1)
        )

        # Create chars/min Frame on center:
        brain.round_rectangle(self.canvas,
                              537,
                              225,
                              701,
                              354,
                              fill=RECTANGLE_COLOR,
                              outline="")
        self.canvas.create_text(
            620,
            245,
            anchor="center",
            text="chars/min",
            fill=TEXT_COLOR,
            font=(FONT_TYPE, 20 * -1)
        )
        brain.round_rectangle(self.canvas,
                              570,
                              269,
                              670,
                              321,
                              fill=BACKGROUND_COLOR,
                              outline="")
        self.cpm_label = self.canvas.create_text(
            620,
            295,
            anchor="center",
            text="0",
            fill=TEXT_COLOR,
            font=(FONT_TYPE, 32 * -1)
        )

        # Create motivation png:
        self.image_image_2 = PhotoImage(
            file=relative_to_assets("image_2.png", ASSETS_PATH_FRAME1))
        image_2 = self.canvas.create_image(
            1120,
            347,
            image=self.image_image_2,
        )

        # Create Copyright text:
        self.canvas.create_text(
            1190,
            800,
            anchor="e",
            text="© 2024 Andrii Yavorskyi",
            fill=TEXT_COLOR,
            font=(FONT_TYPE, 20 * -1)
        )


class ScoreFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Create Score Frame:
        self.image_image_1 = None
        self.score_result = None
        self.parent = parent
        self.canvas = None

        parent.title("Typing Speed Test App")
        parent.geometry("600x800+400+50")
        parent.minsize(600, 800)
        parent.resizable(False, False)

        self.create_widgets()

    def show_results(self):
        """
        Determines the user's typing speed and assigns a corresponding animal image and result.

        This function calculates the user's typing speed based on the number of words per minute (WPM) and assigns
        a corresponding animal image and result. The animal image is determined based on the user's typing speed:
        - If the user's WPM is less than or equal to 20, the image is set to "panda-bear.png" and the result is
          set to "Pandas".
        - If the user's WPM is between 20 and 30, the image is set to "hippopotamus.png" and the result is set to
          "Hippopotamus".
        - If the user's WPM is between 30 and 40, the image is set to "zebra.png" and the result is set to "Zebra".
        - If the user's WPM is greater than 40, the image is set to "cheetah.png" and the result is set to "Cheetah".
        """

        if self.parent.brain.wpm <= 20:
            self.score_result = "Pandas"
            self.image_image_1 = PhotoImage(
                file=relative_to_assets("panda-bear.png", ASSETS_PATH_FRAME2))
        elif 20 < self.parent.brain.wpm <= 30:
            self.score_result = "Hippopotamus"
            self.image_image_1 = PhotoImage(
                file=relative_to_assets("hippopotamus.png", ASSETS_PATH_FRAME2))
        elif 30 < self.parent.brain.wpm <= 40:
            self.score_result = "Zebra"
            self.image_image_1 = PhotoImage(
                file=relative_to_assets("zebra.png", ASSETS_PATH_FRAME2))
        else:
            self.score_result = "Cheetah"
            self.image_image_1 = PhotoImage(
                file=relative_to_assets("cheetah.png", ASSETS_PATH_FRAME2))

    def safe_button(self):
        """
        Calculates the score based on the user's typing speed and accuracy, adds the score to the leaderboard, and
        starts the test over.
        """
        score = self.parent.brain.wpm * self.parent.brain.accuracy / 100
        add_score(int(self.parent.brain.wpm))
        self.parent.start_over()

    def create_widgets(self):
        """
        Creates the widgets for the GUI.

        This function creates the necessary widgets for the GUI, including the canvas, top frame, score image,
        WPM frame, ACC frame, CPM frame, and the "Try Again" and "Save" buttons.
        """
        # Create Canvas:
        self.canvas = Canvas(
            self.parent,
            bg=BACKGROUND_COLOR,
            height=800,
            width=600,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.show_results()

        # Create Top frame:
        brain.round_rectangle(self.canvas,
                              74,
                              30,
                              527,
                              195,
                              fill=RECTANGLE_COLOR,
                              outline="")
        self.canvas.create_text(
            485, 55,
            anchor="ne",
            text=f"Your Test Score is:\n{self.score_result}",
            justify="right",
            fill=TEXT_COLOR,
            font=(FONT_TYPE, 48 * -1)
        )

        # Create Score Image:
        image_1 = self.canvas.create_image(
            300.0,
            345.0,
            image=self.image_image_1
        )

        # Create WPM Frame:
        brain.round_rectangle(self.canvas,
                              64,
                              478,
                              194,
                              604,
                              fill=RECTANGLE_COLOR,
                              outline="")
        self.canvas.create_text(
            130, 500,
            anchor="center",
            text="wpm",
            fill=TEXT_COLOR,
            font=(FONT_TYPE, 20 * -1)
        )
        brain.round_rectangle(self.canvas,
                              91,
                              521,
                              170,
                              572,
                              fill="#D9D9D9",
                              outline="")
        self.canvas.create_text(
            130,
            545,
            anchor="center",
            text=round(self.parent.brain.wpm),
            fill=TEXT_COLOR,
            font=(FONT_TYPE, 32 * -1)
        )

        # Create ACC Frame:
        brain.round_rectangle(self.canvas,
                              394,
                              478,
                              524,
                              604,
                              fill=RECTANGLE_COLOR,
                              outline="")
        self.canvas.create_text(
            460, 500,
            anchor="center",
            text="% acc",
            fill=TEXT_COLOR,
            font=(FONT_TYPE, 20 * -1)
        )
        brain.round_rectangle(self.canvas,
                              420,
                              521,
                              498,
                              572,
                              fill="#D9D9D9",
                              outline="")

        self.canvas.create_text(
            460, 545,
            anchor="center",
            text=round(self.parent.brain.accuracy),
            fill=TEXT_COLOR,
            font=(FONT_TYPE, 32 * -1)
        )

        # Create CPM Frame:
        brain.round_rectangle(self.canvas,
                              229,
                              478,
                              359,
                              604,
                              fill=RECTANGLE_COLOR,
                              outline="")
        self.canvas.create_text(
            295, 500,
            anchor="center",
            text="cpm",
            fill=TEXT_COLOR,
            font=(FONT_TYPE, 20 * -1)
        )
        brain.round_rectangle(self.canvas,
                              256,
                              521,
                              335,
                              572,
                              fill="#D9D9D9",
                              outline="")

        self.canvas.create_text(
            295, 545,
            anchor="center",
            text=round(self.parent.brain.cpm),
            fill=TEXT_COLOR,
            font=(FONT_TYPE, 32 * -1)
        )

        # Create Try Again Bottom:
        button_1 = ctk.CTkButton(self.canvas,
                                 fg_color="#F789B5",
                                 command=self.parent.start_test,
                                 width=165, height=54,
                                 text="TRY AGAIN",
                                 font=(FONT_TYPE, 16 * -1),
                                 text_color=BACKGROUND_COLOR,
                                 hover_color=RECTANGLE_COLOR,
                                 corner_radius=25
                                 )
        button_1.place(
            x=64.0,
            y=666.0,
        )

        # Create Save Bottom:
        button_2 = ctk.CTkButton(self.canvas,
                                 fg_color=RECTANGLE_COLOR,
                                 command=self.safe_button,
                                 width=165, height=54,
                                 text="SAVE",
                                 font=(FONT_TYPE, 16 * -1),
                                 text_color=BACKGROUND_COLOR,
                                 hover_color="#F789B5",
                                 corner_radius=25
                                 )
        button_2.place(
            x=359.0,
            y=666.0,

        )
