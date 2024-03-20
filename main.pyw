import time
import datetime
import tkinter as tk
import os
import chime

"""
Keeps track of the amount of hours I worked

"""

chime.theme("chime")

class App:
    def __init__(self,root: tk.Tk) -> None:
        self.root = root
        self.root.title("Hour's worked tracker")

        self.WIDTH,self.HEIGHT = 500,300
        self.root.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.root.resizable(False,False)

        self.time_started = False
        self.paused = False
        self.time_paused = 0
        self.start_time = 0
        self.time_elapsed = 0

        self.begin_button = tk.Button(self.root, text='Begin Time', width=10,height=5,command=self.begin_click, font='courier')
        self.pause_button = tk.Button(self.root, text="Pause", width=10,height=5, command=self.pause_click,font='courier' )
        self.timer = tk.Label(text="00:00:00", font=('courier',25))


        self.begin_button.place(relx=0.3, rely=0.2, anchor=tk.CENTER)
        self.pause_button.place(relx=0.7, rely=0.2, anchor=tk.CENTER)
        self.timer.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

    
    def pause_click(self):
        self.paused = not self.paused

        if self.paused:
            self.time_paused = time.time()
            self.pause_button.config(text="Resume")
        else:
            self.start_time += (time.time() - self.time_paused)
            self.pause_button.config(text="Pause")

    def begin_click(self):

        if  self.time_started == False:           
            self.time_started = True
            self.begin_button.config(text="End Time")
            self.start_time = (time.time())
            self.update_time()
        else:
            self.pop_window()
            self.begin_button.config(text="Begin Time")
            self.time_started = False
    
    def pop_window(self):
        top = tk.Toplevel(self.root)
        self.top = top
        top.geometry("250x200")
        top.resizable(False,False)

        l1 = tk.Label(top, text="Hours spent not working: ").place(relx=0.35, rely=0.1, anchor=tk.CENTER)
        self.hours_not_worked = tk.Text(top, height=1, width=5)
        self.hours_not_worked.place(relx=0.8, rely=0.1, anchor=tk.CENTER)

        l2 = tk.Label(top, text='Notes:').place(relx=0.1,rely=0.3, anchor=tk.CENTER)

        self.notes = tk.Text(top, width=20 , height=4)
        self.notes.place(relx=0.1, rely=0.35)

        submit = tk.Button(top, text="Submit",command=self.info_submit, width=7,height=2).place(relx=0.5,rely=0.85, anchor=tk.CENTER)

    # submit information about the hours worked
    def info_submit(self):
        hours_not_worked = (self.hours_not_worked.get("1.0", tk.END).strip())

        if not hours_not_worked.replace(".","0").isdigit():
            hours_not_worked = 0    

        notes = (self.notes.get("1.0", tk.END).strip())

        self.time_elapsed = int(time.time() - self.start_time)
        hours_worked = round((self.time_elapsed)/(60*60) - (float(hours_not_worked)),2)
        
        mypath = os.path.join(os.getcwd(), "hours")
        files =  [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]

        now = datetime.datetime.fromtimestamp(int(time.time()))

        dates = []
        # get all files
        if files:
            for i in files:
                dates.append(self.date_str_to_datetime(i))
        else: # no files create one
            self.create_file(f"{str(now.year)[2:]}-{str(now.month).zfill(2)}-{str(now.day).zfill(2)}.txt", f"Hours worked: {hours_worked}\nNotes:\n{notes}")
            self.top.destroy()
            self.timer.config(text="00:00:00")
            return 0

        date:datetime.datetime = max(dates)  # most recent date
        bi_weekly = date + datetime.timedelta(days=14)
        
        if now >= bi_weekly:
            self.create_file(f"{str(now.year)[2:]}-{str(now.month).zfill(2)}-{str(now.day).zfill(2)}.txt", f"Hours worked: {hours_worked}\nNotes:\n{notes}")
        else: # append to existing file
            with open(os.path.join(os.getcwd(),"hours", self.date_to_str(date)+".txt"),"r+") as f:
                contents = f.read().splitlines()
                current_hours = float((contents[0][14:].strip()))
                current_notes = "\n".join([x for x in contents[2:]])
                f.truncate(0)
                f.seek(0)
                f.write(f"Hours worked: {current_hours + hours_worked}\nNotes:\n{current_notes}\n{notes}")
                f.close()

        self.top.destroy()
        self.timer.config(text="00:00:00")

    def create_file(self, file_name, contents):
        chime.info()
        with open(os.path.join(os.getcwd(),"hours", file_name), 'w')as f:
            f.write(contents)
            f.close()

    def date_to_str(self,date):
        return f"{str(date.year)[2:]}-{str(date.month).zfill(2)}-{str(date.day).zfill(2)}"
    # converts date string from file name to datetime object
    def date_str_to_datetime(self, date):
        date = date.split("-")
        year = "20" + date[0]

        month = date[1]
        day = date[2].replace(".txt", "")

        if month[0] == 0:
            month = month[1]
        if day[0] == 0:
            day = day[1]

        return datetime.datetime(year=int(year), month=int(month),day=int(day))

    def update_time(self):
        if self.time_started and not self.paused:       
            self.time_elapsed = int(time.time() - self.start_time)
            self.timer.config(text=self.time_to_str(self.time_elapsed))

        if self.time_started:
            self.root.after(1000,self.update_time)

    def time_to_str(self,t):
        m,s = divmod(t, 60)
        h,m, = divmod(m,60)
        
        s = round(s,0)
        return f"{str(h).zfill(2)}:{str(m).zfill(2)}:{str(s).zfill(2)}"

root = tk.Tk()

window = App(root)

root.mainloop()

