# Standard library imports
import datetime
import socket
import sys

# Internal imports
from system import system
from logs import logs


def main():

    try:
        # Bash script will pass a base path where folder of the application will be
        base_path_proj = (sys.argv[1])
    except IndexError:
        print("Value in argv position 1 does not exist")
        raise SystemExit

    # 2- Call main function
    # 2.1 -> create log file
    obj_time = datetime.datetime.now()
    obj_host = socket.gethostname()

    obj_log = logs.Log()
    obj_log.createlog(base_path_proj, "assigment_log_" + str(obj_time) + "_" + str(obj_host))

    # 2.2 -> call system functions to get all data
    obj_sys = system.System(obj_log)
    obj_sys.getallprocesses()
    obj_sys.getdiskcapacity()


if __name__ == "__main__":
    main()
