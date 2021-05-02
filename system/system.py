# Third party libraries
import psutil

# Internal imports
from util import util


class System:
    """
    Class that will provide information regarding process, memory and capacity in the server.
    """
    # Object from package Utils that allows usage all functions
    # from Utility class
    utility = util.Util()

    # Object for assign previous log obj instance -> avoid loss the path of the log
    log_obj = None

    # Keep Log object instance -> Assign it in the moment of object creation
    def __init__(self, obj):
        self.log_obj = obj

    # Object that will contain the list of process of the iteration
    list_all_process = list()
    # Object that will contain the list of process of the iteration order by cpu usage
    list_order_cpu = list()
    # Object that will contain the list of process of the iteration order by memory usage
    list_order_memory = list()

    # Attributes of the processes that it will be retrieved
    proc_attr = ['pid', 'name', 'username', 'create_time', 'cpu_percent', 'memory_percent']

    def getallprocesses(self):
        """
        Get all current running process in the system.
        Using utility class, format the values for more legible human way and storage
        in a list
        """
        format_info = {}

        # psutil.process_iter(attrs=[]) provide all the current processes in the server
        # it can receive attributes and return the information specified
        # https://psutil.readthedocs.io/en/latest/#processes
        #   If attrs is specified Process.as_dict() result will be stored as a info attribute attached to the
        #   returned Process instances. If attrs is an empty list it will retrieve all process info.

        # Iterate over all running processes
        for process in psutil.process_iter():
            try:
                # get all process info in one shot
                with process.oneshot():
                    # Get process detail as dictionary
                    # Example of a output:
                    # {'create_time': 1618860268.144381, 'pid': 0, 'name': 'kernel_task', 'username': 'root',
                    #   'cpu_percent': None, 'memory_percent': None}

                    # Contains "pure" info
                    procpureinfo = process.as_dict(attrs=self.proc_attr)

                    # Calls method to format data
                    format_info = self.utility.processdata(procpureinfo)

                    # Add format dictionary to the current list of process and avoid override the list in a next
                    # iteration
                    # Avoid include empty data
                    if format_info is not None:
                        self.list_all_process.append(format_info)
            except KeyError:
                print(f"Error trying to access to a key or value in a dictionary: {KeyError}")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                print(f"Cannot retrieve process info, skipping ... ")

        # >>>>> PROCESS DATA AND SEPARATE IT IN TWO LISTS
        # Sort process by memory usage
        # Sort list of dict by key vms i.e. memory usage
        self.list_order_memory = sorted(self.list_all_process, key=lambda processobj: processobj['memory_percent'],
                                        reverse=True)
        # Sort process by cpu usage
        # Sort list of dict by key vms i.e. memory usage
        self.list_order_cpu = sorted(self.list_all_process, key=lambda processobj: processobj['cpu_percent'],
                                     reverse=True)

        # Write results in the log
        # Write full list
        self.log_obj.writelog(f">" * 10 + "List of all process" + "<" * 10)
        self.log_obj.writelog(self.utility.returnlist(self.list_all_process, len(self.list_all_process), False))

        # Write 3 top process memory usage
        self.log_obj.writelog(f">" * 10 + "List of top 3 memory usage process" + "<" * 10)
        self.log_obj.writelog(self.utility.returnlist(self.list_order_memory, 3, True))

        # Write 3 top process CPU usage
        self.log_obj.writelog(f">" * 10 + "List of top 3 CPU usage process" + "<" * 10)
        self.log_obj.writelog(self.utility.returnlist(self.list_order_cpu, 3, True))

    def getdiskcapacity(self):
        """
       Return all mounted disk partitions as a list of named tuples including device, mount point and filesystem type,
       similarly to “df” command on UNIX. If all parameter is False it tries to distinguish and return physical devices
       only (e.g. hard disks, cd-rom drives, USB keys) and ignore all others (e.g. pseudo, memory, duplicate,
       inaccessible filesystems)
       :return: Information about all disk partition
       """
        partitions = psutil.disk_partitions()

        # Iterate in all disk partitions and retrieve information
        self.log_obj.writelog(f">" * 10 + "Disk information" + "<" * 10)

        for partition in partitions:
            self.log_obj.writelog(f"=== Device: {partition.device} ===")
            self.log_obj.writelog(f"  Mount point: {partition.mountpoint}")
            self.log_obj.writelog(f"  File system type: {partition.fstype}")
            #  a comma-separated string indicating different mount options for the drive/partition
            self.log_obj.writelog(f"  Partition Mount options: {partition.opts}")
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
            except PermissionError:
                # this can be catched due to the disk that
                # isn't ready
                print("f Partition is busy, cannot retrieve size and usage's size")
                continue
            self.log_obj.writelog(f"  Total Size: {self.utility.measuresequivalent(partition_usage.total)}")
            self.log_obj.writelog(f"  Used: {self.utility.measuresequivalent(partition_usage.used)}")
            self.log_obj.writelog(f"  Free: {self.utility.measuresequivalent(partition_usage.free)}")
            self.log_obj.writelog(f"  Percentage: {partition_usage.percent:.2f}%")