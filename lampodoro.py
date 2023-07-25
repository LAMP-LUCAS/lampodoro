import tkinter as tk
from tkinter import messagebox
import time
import configparser

class Lampodoro:
    def __init__(self, root):
        self.root = root
        self.root.title("Lampodoro")
        self.work_time = tk.StringVar()
        self.break_time = tk.StringVar()
        self.cycles = tk.IntVar()
        self.running = False

        self.load_settings()
        self.create_widgets()

    def create_widgets(self):
        label_work = tk.Label(self.root, text="Tempo de trabalho (minutos):")
        label_work.pack()
        entry_work = tk.Entry(self.root, textvariable=self.work_time)
        entry_work.pack()

        label_break = tk.Label(self.root, text="Tempo de pausa (minutos):")
        label_break.pack()
        entry_break = tk.Entry(self.root, textvariable=self.break_time)
        entry_break.pack()

        label_cycles = tk.Label(self.root, text="Quantos ciclos Pomodoro:")
        label_cycles.pack()
        entry_cycles = tk.Entry(self.root, textvariable=self.cycles)
        entry_cycles.pack()

        start_button = tk.Button(self.root, text="Iniciar", command=self.start_pomodoro)
        start_button.pack()

        stop_button = tk.Button(self.root, text="Parar", command=self.stop_pomodoro)
        stop_button.pack()

    def load_settings(self):
        config = configparser.ConfigParser()
        try:
            config.read("lampodoro_settings.ini")
            self.work_time.set(config.get("Settings", "work_time"))
            self.break_time.set(config.get("Settings", "break_time"))
            self.cycles.set(config.getint("Settings", "cycles"))
        except:
            # Caso o arquivo de configuração não exista ou não possa ser lido, 
            # valores padrão serão utilizados.
            self.work_time.set("25")
            self.break_time.set("5")
            self.cycles.set(4)

    def save_settings(self):
        config = configparser.ConfigParser()
        config["Settings"] = {
            "work_time": self.work_time.get(),
            "break_time": self.break_time.get(),
            "cycles": self.cycles.get()
        }
        with open("lampodoro_settings.ini", "w") as config_file:
            config.write(config_file)

    def start_pomodoro(self):
        if not self.running:
            self.save_settings()
            work_time = int(self.work_time.get()) * 60
            break_time = int(self.break_time.get()) * 60
            cycles = self.cycles.get()
            for _ in range(cycles):
                self.run_timer(work_time, "Tempo de trabalho encerrado!")
                self.run_timer(break_time, "Pausa encerrada!")

    def run_timer(self, seconds, message):
        self.running = True
        while seconds > 0:
            m, s = divmod(seconds, 60)
            time_format = '{:02d}:{:02d}'.format(m, s)
            self.root.title("Lampodoro - " + time_format)
            self.root.update()
            time.sleep(1)
            seconds -= 1
        self.running = False
        self.root.title("Lampodoro")
        messagebox.showinfo("Lampodoro", message)

    def stop_pomodoro(self):
        self.running = False

if __name__ == "__main__":
    root = tk.Tk()
    lampodoro = Lampodoro(root)
    root.mainloop()
