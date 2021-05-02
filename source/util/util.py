# Standard library imports
from datetime import date
import socket

# Third party imports
import dotenv


class Util:
    """
    Class that will 'help' the rest of application class with different methods that could include
    process, check or print data.
    """
    """
    Dictionary that will support different functions through all application (Disk conversions)
    Examples
    {'PB': '0.0', 'TB': '0.081', 'GB': '83.304', 'MB': '85302.874', 'KB': '87350143.082', 'bytes': '89446546516.0'}
    """
    # UNITS_MAPPING is a dict with all convert values
    # taking as base a number of bytes
    UNITS_MAPPING = [
        (1 << 50, 'PB'),
        (1 << 40, 'TB'),
        (1 << 30, 'GB'),
        (1 << 20, 'MB'),
        (1 << 10, 'KB'),
        (1, ('byte', 'bytes')),
    ]

    def processdata(self, proc_info):
        """
        Return in a format way the data according with the type
        :param proc_info: information of the process as a dictionary
        :return: the format information in a dictionary
        """
        format_info = {}

        try:
            # if all values are different of None, be will take in account for process, otherwise, ignore
            if all(item is not None for item in proc_info.values()):
                for key, value in proc_info.items():
                    str_key = str(key)
                    # if value contains information, do the format process appropriately
                    # PID, name and username will keep the same data
                    if str_key == "pid" or str_key == "name" or str_key == "username":
                        format_info[key] = value
                    # Convert milisec data to format one
                    if str_key == "create_time":
                        format_info[key] = self.formatdate(proc_info[key])
                    # Memory and CPU %
                    if str_key == "memory_percent" or str_key == "cpu_percent":
                        format_info[key] = f"{proc_info[key]:.2f} %"

                return format_info

        except KeyError as e:
            print(f"Error trying to access value in a dictionary: {e}")
            raise SystemExit

    def formatdate(self, millisec_date):
        """
        Convert a millisecond value to a string format date
        :param millisec_date: date value in milliseconds
        :return: format string date of millisecond value
        """
        try:
            return date.fromtimestamp(millisec_date).strftime("%m/%d/%Y, %H:%M:%S")
        except Exception as e:
            print(f"Error trying to parse date: {e}")
            raise SystemExit

    def measuresequivalent(self, num_bytes):
        """
        Returns human-readable sizes
        as a dictionary according with measures dictionaries
        previously defined
        :param memory: Boolean, indicates if we want to use memory dictionary without PB measure
        :param num_bytes, Float, number of bytes to be converted
        :return a dictionary with conversions based of number of bytes
        """
        table_convert = {}

        # Iterate in units and convert values
        for factor, suffix in self.UNITS_MAPPING:
            amount = round(float(num_bytes / factor), 3)
            if isinstance(suffix, tuple):
                singular, multiple = suffix
                if amount == 1:
                    suffix = singular
                else:
                    suffix = multiple
            table_convert[suffix] = str(amount)
        return table_convert

    def returnttitle(self):
        """
        Return a title list for the current processes
        :return: String, a title for a better lecture of the list process
        """
        return str(f" PID " + "\t" * 3 + "Name" + "\t" * 4 + "Username" + "\t" * 3 + "Creation datetime" + "\t" * 3
                   + "CPU %" + "\t" * 3 + "Memory %")

    def returnlist(self, listofprocess, amount, limit):
        """
        Return a list of object with their respective format to be printed
        :param listofprocess: list of process to be write
        :param amount: quantity of process to be write
        :param limit: if we want a limit, set this to true
        :return: the list format to string
        """
        tittle = self.returnttitle() + "\n"
        line = ""
        i = 0

        if limit:
            for item in listofprocess:
                if i < amount:
                    line = line + str(f"{item['pid']}" + "\t" * 3 +
                                      f"{item['name']}" + "\t" * 4 +
                                      f"{item['username']}" + "\t" * 3 +
                                      f"{item['create_time']}" + "\t" * 4 +
                                      f"{item['cpu_percent']}" + "\t" * 3 +
                                      f"{item['memory_percent']}" + "\n")
                    i = i + 1
        else:
            for item in listofprocess:
                line = line + str(f"{item['pid']}" + "\t" * 3 +
                                  f"{item['name']}" + "\t" * 4 +
                                  f"{item['username']}" + "\t" * 3 +
                                  f"{item['create_time']}" + "\t" * 3 +
                                  f"{item['cpu_percent']}" + "\t" * 3 +
                                  f"{item['memory_percent']}" + "\n")

        return tittle + line
