# Internal imports
from util import util


class Log:
    """
    Class that will handled the log management with some basic functions as write and read
    """
    # Object of util class that will handled format information
    utility = util.Util()

    # path will keep the value of the file for current log
    path = ""

    def createlog(self, base_path, log_name):
        """
        Create a log in LOG_PATH env path of the application
        :param base_path: string, base path of the application
        :param String, log_name: name of the log
        """
        # Generate log path
        report_path = base_path + "/log_files/" + log_name + ".txt"
        print(report_path)

        # Storage value in the attribute class
        self.path = report_path
        try:
            # Create the file in the specified path
            with open(self.path, 'w') as writer:
                writer.close()
        except FileNotFoundError:
            print("Could not create the log: " + log_name)
            raise SystemExit

    def writelog(self, text):
        """
        Write a specific text in a log
        :param text: String, text to be write in the report
        """
        try:
            with open(self.path, "a") as writer:
                writer.write(text + "\n")
        except FileNotFoundError:
            print("File not found! " + self.path)
            raise SystemExit
