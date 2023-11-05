from tkinter import *
from tkinter import ttk
import time
import json
from tkinter.messagebox import showinfo, askyesno

main_window = Tk()
main_window.title("Keyboard trainer")

WINDOW_LENGTH = 1000  # main_window parametrs
WINDOW_HIGHT = 700
WINDOW_X_SHIFT = 250
WINDOW_Y_SHIFT = 50
WINDOW_X_MIN_SIZE = 600
WINDOW_Y_MIN_SIZE = 400
WINDOW_X_MAX_SIZE = 1200
WINDOW_Y_MAX_SIZE = 1000

main_window.geometry(f"{WINDOW_LENGTH}x{WINDOW_HIGHT}+{WINDOW_X_SHIFT}+{WINDOW_Y_SHIFT}")
main_window.minsize(WINDOW_X_MIN_SIZE, WINDOW_Y_MIN_SIZE)
main_window.maxsize(WINDOW_X_MAX_SIZE, WINDOW_Y_MAX_SIZE)


class Mistake:
    all_mst = 0
    all_chr = 0

    def __init__(self):
        self.count = 0


mistake_int = Mistake()


class Results:
    def __init__(self, name):
        self.name = name
        self.speed = 0
        self.mistake = 0
        self.acc = 0


name = "name"


# class fo checking time
class TimeSpeed:
    all_time = 0

    def __init__(self):
        self.start = 0
        self.end = 0


# file with previous statistics

with open('statistic.json') as start_f:
    my_old_stat = json.load(start_f)

print(my_old_stat)
speed_time = TimeSpeed()

speed_time.all_time = my_old_stat['time']
my_results = Results(my_old_stat['name'])

mistake_int.all_mst = my_old_stat['mistake']
mistake_int.all_chr = my_old_stat['all chr']

# file with example of task

with open('example_task.json') as file:
    new_task = json.load(file)

# after completing all tasks
def open_info():
    result = askyesno(title="Congratulations", message="You have compiled all tasks! Do you want to do it again?")
    if result:
        global key
        key = 1
        showinfo("Congratulations", "Restart")
    else:
        showinfo("Congratulations", "Goodbye!")
        main_window.destroy()


# def for Entry field
def typing_field():
    global key
    cur_task = new_task[str(key)]
    # label with text to type
    example_label_x = 61
    example_label_y = 30
    example_label = ttk.Label(main_window, text=cur_task, font=24)
    example_label.place(x=example_label_x, y=example_label_y)

    # is_valid is checking is the next letter suitable or not
    # also is_valid is changing the statistic and making new iteration of task

    def is_valid(newval, smb):
        global key
        # key is the int(key) of task in file with tasks
        # cur_task is task to write
        cur_task = new_task[str(key)]

        # start of timer
        if int(smb) == 0:
            speed_time.start = time.time()

        # if the end of task is reached
        if len(cur_task) - 1 == int(smb) and cur_task[int(smb)] == newval[int(smb)]:
            speed_time.end = time.time()
            # change os statistics
            speed_time.all_time += speed_time.end - speed_time.start

            mistake_int.all_chr += len(cur_task) + mistake_int.count
            mistake_int.all_mst += mistake_int.count

            mistake_int.count = 0
            my_results.mistake = mistake_int.all_mst

            my_results.speed = round(mistake_int.all_chr / speed_time.all_time * 60, 2)
            my_results.acc = round(((mistake_int.all_chr - mistake_int.all_mst) / mistake_int.all_chr * 100), 2)

            progr_pad = 10
            # show the statistics
            total_progress = ttk.Frame(main_window, borderwidth=1, relief=SOLID, padding=[progr_pad])

            user_name = ttk.Label(total_progress, text="UserName: " + my_results.name, font=24)
            user_name.pack(anchor=NW)

            total_speed = ttk.Label(total_progress, font=24)
            total_speed.pack(anchor=NW)

            total_mst = ttk.Label(total_progress, font=24)
            total_mst.pack(anchor=NW)

            total_acc = ttk.Label(total_progress, font=24)
            total_acc.pack(anchor=NW)

            total_speed["text"] = "Total Speed: " + str(my_results.speed) + " chr in min"
            total_mst["text"] = "Total Count of Mistakes: " + str(my_results.mistake)
            total_acc["text"] = "Total Accuracy: " + str(my_results.acc) + "%"

            total_progress.pack(anchor=NW, padx=5, pady=5)

            # hide the statistics if the task is ended
            def on_key(event):
                total_progress.destroy()

            main_window.bind("<KeyPress>", on_key)
            # clear the entry field for a new task
            entry_line.delete(0, len(cur_task))

            # changing key for a new task
            key = int(key) + 1

            # new iteration of tasks
            if key <= len(new_task):
                cur_task = new_task[str(key)]
                example_label["text"] = cur_task
            else:
                # if all tasks are ended
                example_label["text"] = new_task['1']
                open_info()

        else:
            # if typed letter is not suitable
            if cur_task[int(smb)] != newval[int(smb)]:
                mistake_int.count += 1

        # if we started typing more letters, then are in task
        if int(smb) >= len(cur_task):
            return False
        # check fof a typed letter
        return cur_task[int(smb)] == newval[int(smb)]

    # creating of entry field
    entry_check = (main_window.register(is_valid), "%P", "%i")

    entry_line = ttk.Entry(validate="key", validatecommand=entry_check, width=200, font=24)

    entry_line.pack(anchor=NW, padx=60, pady=60)


# start key is 1
key = 1
typing_field()


# button for clearing statistics
def ClearBtn():
    def clear():
        mistake_int.all_mst = 0
        mistake_int.all_chr = 0
        speed_time.all_time = 0

    restart_btn = ttk.Button(text="Clear all statistics", command=clear)
    restart_btn.pack()


ClearBtn()


# def for saving statistics after closing app
def close():
    my_statistics = {'name': name, 'mistake': mistake_int.all_mst, 'all chr': mistake_int.all_chr,
                     'time': speed_time.all_time}

    with open('statistic.json', 'w') as f:
        json.dump(my_statistics, f)

    print(my_statistics)

    main_window.destroy()


main_window.protocol("WM_DELETE_WINDOW", close)

main_window.mainloop()
