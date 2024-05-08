__author__ = "AndyVoyager"


class Values:
    def __init__(self):

        self.time = None
        self.time_text = None
        self.level = None

    def set_time(self, time):
        """
        Set the time and time text based on the given time.

        Parameters:
            time (str): The time in the format "X minutes".
        """
        time = int(time.split(" ")[0])
        self.time = time * 60
        self.time_text = f"0{str(time)}:00"

    def set_level(self, level):
        self.level = level


def choose_time():
    times = ["1 minute", "2 minutes", "3 minutes", "4 minutes", "5 minutes"]
    return times


def choose_level():
    levels = ["History", "Movies", "Science", "Sports", "General"]
    return levels
