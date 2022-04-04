import psutil


def read_preferences():
    contents = []
    proc_int_dict = dict()

    # Put contents of preferences file line by line into list
    with open('preferences') as f:
        contents = f.readlines()

    # Split each line at the "|" and put into dictionary where the key is before "|" and its value is after "|"
    for line in contents:
        for i in range(len(line)):
            if line[i:i+1] == '|':
                proc_int_dict.update({line[0:i]: int(line[i+1])})

    return proc_int_dict


def append_preferences(process, intensity):

    with open("preferences", "a") as f:
        f.write("\n" + process + "|" + str(intensity))


def restore_default_preferences():
    with open("preferences", "w") as f:
        f.write("chrome.exe|1\npycharm64.exe|3")

    print("\nRestored default settings successfully.")


def curr_process(show_output=False):
    processes = []

    # Collect processes into list of dictionaries
    for proc in psutil.process_iter():
        try:
            process_info = proc.as_dict(attrs=["pid", "name"])
            process_info["vms"] = proc.memory_info().vms / (1024 * 1024)  # conversion from bytes to MB
            #                                                               (computers use powers of 2 for things)
            processes.append(process_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    if show_output:
        print("\nBefore filtering\n")
        for proc in processes[:10]:
            print(proc)

# ----------------------------------------------------------------------------------------------------------------------

    # Exclude pycharm & others (mostly windows background stuff) from the list of current processes
    to_be_removed = []
    filter_procs = ["pycharm64.exe", "SupportAssistAgent.exe", "MsMpEng.exe", "KillerNetworkService.exe", "svchost.exe",
                    "SearchApp.exe", "dwm.exe", "Dsapi.exe", "YourPhoneServer.exe", "ServiceShell.exe",
                    "IAStorDataMgrSvc.exe"]

    # Remove duplicate processes, adding their vms aka ram usage, and listing their pids in one process dictionary
    consolidated_dupes = []
    for proc in processes:
        name = proc["name"]
        count = 0
        dupes = []

        # Don't even bother checking for duplicates of stuff that is going to be filtered out later
        if name in filter_procs:
            continue

        # Count instances of process
        for proc2 in processes:
            if name == proc2["name"]:
                dupes.append(proc2)
                count += 1

        # If there are no duplicates, continue to next proc in processes
        if count < 2:
            continue

        # If already consolidated the duplicates, continue to next proc in process
        already_done = False
        for dupe in consolidated_dupes:
            if name == dupe["name"]:
                already_done = True
                break

        if already_done:
            continue

        total_vms = 0
        pids = []

        # For each duplicate, add its vms aka ram usage to the total and append its pid to a list of pids
        for dupe in dupes:
            total_vms += dupe["vms"]
            pids.append(dupe["pid"])

        consolidated_dupe = {"name": name, "pid": pids, "vms": total_vms}
        filter_procs.append(name)
        consolidated_dupes.append(consolidated_dupe)

    if show_output:
        print("\nConsolidated duplicate processes\n")
        for dupe in consolidated_dupes:
            print(dupe)

    # Filtering w/previously defined filter procs
    for proc in processes:
        if proc["name"] in filter_procs:
            to_be_removed.append(proc)

    # Removing things caught in filter
    for proc in to_be_removed:
        processes.remove(proc)

    # Adding consolidated duplicate processes to the list of processes in place of the removed duplicates
    for cons_dupe in consolidated_dupes:
        processes.append(cons_dupe)

    if show_output:
        print("\nAfter removing target processes and adding in consolidated duplicates\n")
        for proc in processes[:10]:
            print(proc)

# ----------------------------------------------------------------------------------------------------------------------

    # Sort list by memory usage in order of highest to lowest
    processes = sorted(processes, key=lambda proc: proc["vms"], reverse=True)

    # To see what the output looks like
    if show_output:
        print("\nAfter sorted by memory\n")
        for proc in processes[:10]:
            print(proc)

    return processes[:10]


def intensity_num(processes, show_output=False):
    first = processes[0]
    curr_preferences = read_preferences()

    # If nothing significant is running return 0 out of 5
    if first.get("vms") < 500:
        if show_output:
            print(0)
        return 0

    # If the current process is not in the preferences file
    if curr_preferences.get((first.get("name")), "DNE") == "DNE":
        # Print names of processes for user to see
        for proc in processes:
            print(proc.get("name"))

        # User input for process name
        real_process = input("Please type the name of which process you would like to use exactly as it appears: ")

        # Check if it is in the top 10 memory using processes
        for proc in processes:
            # If it is, check the preferences file for the process
            if proc.get("name") == real_process:
                # If it's not in the preferences file ask for an intensity, append to preferences, and return intensity
                if curr_preferences.get(real_process, "DNE") == "DNE":
                    new_pref = input("Type an integer from 0 (least) to 5 (most) inclusive which represents the "
                                     + "process's intensity: ")
                    append_preferences(real_process, new_pref)

                    if show_output:
                        print(new_pref)

                    return new_pref

                # If it is in the preferences file then return associated intensity
                if show_output:
                    print(curr_preferences.get(real_process))

                return curr_preferences.get(real_process)

        # If the user input is not in the top 10 memory using processes, assume medium intensity
        if show_output:
            print(2)

        return 2

    # If it is in the preferences file, then return associated intensity
    if show_output:
        print(curr_preferences.get(first.get("name")))

    return curr_preferences.get(first.get("name"))


def get_intensity():
    return intensity_num(curr_process())
