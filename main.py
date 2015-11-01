import wmi
from tkinter import *
import tkinter.messagebox as mb

class BattDisplay(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.conn = wmi.WMI(moniker="//./root/wmi")
        self.batts = self.conn.ExecQuery('Select * from BatteryFullChargedCapacity')
        self.full_cap = self.batts[0].FullChargedCapacity
        self.switch_status = False
        self.batt_percent = 0
        self.batt_show = StringVar()
        self.batt_label = Label(self, textvariable=self.batt_show)
        self.btn = Button(text="Battery Tracker", command=self.toggle_switch)
        self.batt_label.pack()
        self.btn.pack()
        self.update_me()

    def update_me(self):  
        if self.switch_status:
            self.update_batt_percent()
            if (self.batts[0].Charging and self.batt_percent > 80) or (not self.batts[0].Charging and self.batt_percent < 40):
                self.show_status()
        self.after(10000, self.update_me)


    def toggle_switch(self):
        if self.switch_status:
            self.switch_status = False
            self.btn.configure(relief=RAISED)
        else:
            self.switch_status = True
            self.btn.configure(relief=SUNKEN)
            self.update_batt_percent()
          
          
    def show_status(self):
        mb.showwarning("Battery Info", "Your battery is at %i percent" % self.batt_percent)
        
    def update_batt_percent(self):
        self.batts = self.conn.ExecQuery('Select * from BatteryStatus where Voltage > 0')
        rem_cap = self.batts[0].RemainingCapacity
        self.batt_percent = int(rem_cap / self.full_cap * 100)
        self.batt_show.set("Battery Level: %s percent" % str(self.batt_percent))

    


if __name__ == '__main__':
    tk = Tk()
    timer_frame = BattDisplay(tk)
    timer_frame.pack()
    tk.mainloop()
