import tkinter as tk
from tkinter import messagebox
import ctypes
import datetime
import os

class SYSTEMTIME(ctypes.Structure):
    _fields_ = [("wYear", ctypes.c_ushort),
                ("wMonth", ctypes.c_ushort),
                ("wDayOfWeek", ctypes.c_ushort),
                ("wDay", ctypes.c_ushort),
                ("wHour", ctypes.c_ushort),
                ("wMinute", ctypes.c_ushort),
                ("wSecond", ctypes.c_ushort),
                ("wMilliseconds", ctypes.c_ushort)]

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def createSystemTime(year, month, day):
    now = datetime.datetime.now()
    local_time = datetime.datetime(year, month, day, now.hour, now.minute, now.second, now.microsecond)
    utc_time = local_time.astimezone(datetime.timezone.utc)

    system_time = SYSTEMTIME()
    system_time.wYear = utc_time.year
    system_time.wMonth = utc_time.month
    system_time.wDay = utc_time.day
    system_time.wHour = utc_time.hour
    system_time.wMinute = utc_time.minute
    system_time.wSecond = utc_time.second
    system_time.wMilliseconds = int(utc_time.microsecond / 1000)

    return system_time

def setFixDate():
    year, month, day = 2024, 6, 11
    system_time = createSystemTime(year, month, day)
    ret = ctypes.windll.kernel32.SetSystemTime(ctypes.byref(system_time))
    if ret == 0:
        logInsert("Failed to set system date","red")
        return False
    else:
        logInsert(f"Date successfully set to {month}/{day}/{year}","green")
        return True

def syncWinDate():
    command = 'w32tm /resync'
    result = os.popen(command).read()
    logInsert(result,"green")

def logInsert(msg,color):
    log_text.config(state=tk.NORMAL)
    log_text.insert(tk.END, msg + "\n",color)
    log_text.config(state=tk.DISABLED)
    log_text.see(tk.END)

def fixdate():
    if is_admin():
        setFixDate()
    else:
        messagebox.showwarning("Warning","Script is not running as admin")

def curdate():
    if is_admin():
        syncWinDate()
    else:
        messagebox.showwarning("Warning","Script is not running as admin")



r = tk.Tk()
r.title('DCS World F15E A/A RDR FIX')

log_text = tk.Text(r, wrap='word', height=10, width=50)
log_text.pack(padx=10, pady=10)
log_text.config(state=tk.DISABLED)  # Disable editing

button = tk.Button(r, text='Fix radar', width=25, command=fixdate)
button2 = tk.Button(r, text='Sync current date', width=25, command=curdate)
button.pack()
button2.pack()
r.mainloop()