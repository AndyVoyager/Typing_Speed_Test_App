__author__ = "AndyVoyager"

import data
import re
import Levenshtein


def destroy_widgets(root):
    """
    Destroy all widgets in the given root window.
    :param root: The root window containing the widgets to be destroyed.
    """
    root.frame.destroy()
    for widget in root.winfo_children():
        widget.destroy()


def round_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    """
    Generates a rounded rectangle shape on a canvas widget.

    :param canvas: canvas widget to draw the rounded rectangle on.
    :param x1: The x-coordinate of the top-left corner of the rounded rectangle.
    :type x1: int
    :param y1: The y-coordinate of the top-left corner of the rounded rectangle.
    :type y1: int
    :param x2: The x-coordinate of the bottom-right corner of the rounded rectangle.
    :type x2: int
    :param y2: The y-coordinate of the bottom-right corner of the rounded rectangle.
    :type y2: int
    :param radius: The radius of the rounded corners of the rounded rectangle. Defaults to 25.
    :type radius: int
    :return: The ID of the created rounded rectangle shape.
    :rtype: int
    """
    points = [x1 + radius, y1,
              x1 + radius, y1,
              x2 - radius, y1,
              x2 - radius, y1,
              x2, y1,
              x2, y1 + radius,
              x2, y1 + radius,
              x2, y2 - radius,
              x2, y2 - radius,
              x2, y2,
              x2 - radius, y2,
              x2 - radius, y2,
              x1 + radius, y2,
              x1 + radius, y2,
              x1, y2,
              x1, y2 - radius,
              x1, y2 - radius,
              x1, y1 + radius,
              x1, y1 + radius,
              x1, y1]

    return canvas.create_polygon(points, **kwargs, smooth=True, stipple='gray12')


class Brain:

    def __init__(self):
        self.total_words_in_sentence = 0
        self.input_text = None
        self.counter = 0
        self.cpm = 0
        self.accuracy = 0
        self.wpm = 0
        self.text_parts = None
        self.actual_part = None
        self.count = 0
        self.total_time_in_sec = None
        self.count_minute = 0
        self.total_correct_words = 0
        self.total_correct_chars = 0

    @staticmethod
    def start_countdown(label, minutes, func):
        """
        This function starts a countdown timer, updating the label with the remaining time in HH:MM format.

        Parameters:
            label: The label widget where the countdown time will be displayed.
            minutes: The total number of minutes for the countdown.
            func: The function to be executed once the countdown reaches zero.
        """

        def count_down():
            """
            Updates the countdown timer displayed on the label widget.

            This function is called recursively to update the countdown timer every second.
            It calculates the remaining time in hours and minutes based on the given minutes parameter.
            The label widget is then updated with the formatted time in HH:MM format.
            """
            nonlocal minutes

            if minutes >= 0:
                hour = minutes // 60
                minute = minutes % 60
                label.configure(text=f"{hour:02d}:{minute:02d}")
                if minutes > 0:
                    minutes -= 1
                    label.after(1000, count_down)
                else:
                    func()
            else:
                label.config(text="00:00")

        count_down()

    def calculate_speed(self, time_taken, canvas, cpm_label, wpm_label, accuracy_label):
        """
        Calculates the speed metrics (CPM, WPM, Accuracy) based on the given time taken and updates the corresponding
        labels.

        Parameters:
            time_taken (str): The time taken in the format "HH:MM".
            canvas (tkinter.Canvas): The canvas object used to update the labels.
            cpm_label (int): The canvas item ID for the CPM label.
            wpm_label (int): The canvas item ID for the WPM label.
            accuracy_label (int): The canvas item ID for the Accuracy label.
        """

        # Convert time taken to time format:
        minutes, seconds = map(int, time_taken.split(':'))
        total_taken_time = self.total_time_in_sec - (minutes * 60 + seconds)
        self.total_time_in_sec -= total_taken_time

        # print(f"total time taken: {total_taken_time}")
        # Compare input text with actual part:
        distance = Levenshtein.distance(self.input_text, self.actual_part)
        correct_chars = len(self.input_text) - distance
        self.total_correct_chars += correct_chars

        # Split input text and actual part into words:
        input_words = self.input_text.split()
        actual_words = self.actual_part.split()

        # Count number of correctly typed words:
        correct_words = 0
        for input_word, actual_word in zip(input_words, actual_words):
            if input_word == actual_word:
                correct_words += 1

        # Sum correctly typed words and total words in a sentence:
        self.total_correct_words += correct_words
        self.total_words_in_sentence += len(actual_words)

        #______________Calculate CPM, WPM, ACCURACY_____________________________________________________________________
        self.count_minute += total_taken_time
        if self.count_minute < 60:
            # Calculate CPM if time taken is less than 1 minute:
            predicted_cpm = (correct_chars / total_taken_time) * 60
            cpm = predicted_cpm

            # Calculate WPM if time taken is less than 1 minute:
            predicted_wpm = (correct_words / total_taken_time) * 60
            wpm = predicted_wpm
        else:
            minutes_taken = self.count_minute / 60

            # Calculate CPM if time taken is more than 1 minute:
            cpm = self.total_correct_chars / minutes_taken

            # Calculate WPM if time taken is more than 1 minute:
            wpm = self.total_correct_words / minutes_taken

        # Calculate ACCURACY:
        accuracy = (self.total_correct_words / self.total_words_in_sentence) * 100
        #_______________________________________________________________________________________________________________

        # Update CPM, WPM, ACCURACY:
        if self.cpm == 0:
            self.cpm = cpm
        else:
            self.cpm = (self.cpm + cpm) / 2

        if self.wpm == 0:
            self.wpm = wpm
        else:
            self.wpm = (self.wpm + wpm) / 2

        if self.accuracy == 0:
            self.accuracy = accuracy
        else:
            self.accuracy = (self.accuracy + accuracy) / 2

        # Update CPM and WPM labels:
        canvas.itemconfig(cpm_label, text=f"{round(self.cpm)}")
        canvas.itemconfig(wpm_label, text=f"{round(self.wpm)}")
        canvas.itemconfig(accuracy_label, text=f"{round(self.accuracy)}")

    def compare_text_with_canvas_text(self, input_text, canvas_text):
        self.input_text = input_text
        self.actual_part = canvas_text
        if input_text in canvas_text:
            # print("correct")
            pass
        else:
            # print("incorrect")
            pass

    def generate_text(self, theme):
        """
        Generates text based on the given theme and splits it into parts.

        Parameters:
            theme (str): The theme to generate the text from.
        """
        if not self.text_parts:
            self.text_parts = None
        generated_text = data.get_data(theme)
        # Split text into parts:
        self.text_parts = re.findall(r'.{1,65}(?:\s|$)', generated_text)

    def get_text_parts(self):
        """
        Retrieves the text parts from the instance variable `text_parts` and returns the part at the index specified by
        `count`.

        Returns:
            str: The text part at the index specified by `count`.
        """
        # Choose actual part:
        for i, part in enumerate(self.text_parts):
            if i == self.count:
                # print(part)
                return part

    def clear_scores(self):
        """
        Clears the scores by resetting the count, cpm, wpm, and accuracy attributes to their initial values.

        Parameters:
            self (object): The instance of the class.
        """
        self.count = 0
        self.cpm = 0
        self.wpm = 0
        self.accuracy = 0
