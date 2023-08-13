import tkinter as tk
import time
import configparser
import gettext
import os
import winsound
import threading
from tkinter import messagebox
import logging


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Lampodoro:

    def __init__(self, root):
        self.pomodoro_started = False
        self.root = root
        self.root.title(_("Lampodoro"))
        self.work_time = tk.StringVar(value=".1")
        self.break_time = tk.StringVar(value=".1")
        self.cycles = tk.IntVar(value=1)
        self.current_cycle = tk.IntVar(value=0)
        self.running = False
        self.start_time = 0
        self.sound_file = ""

        reset_button = tk.Button(self.root, text=_("Redefinir"), command=self.reset_pomodoro)
        reset_button.pack()

        self.load_last_sound()
        self.load_settings()
        self.create_widgets()

    def reset_pomodoro(self):
        self.pomodoro_started = False
        self.stop_pomodoro()

    def create_widgets(self):
        """
        Cria os widgets da interface gráfica.
        """
        label_work = tk.Label(self.root, text=_("Tempo de trabalho (minutos):"))
        label_work.pack()
        entry_work = tk.Entry(self.root, textvariable=self.work_time)
        entry_work.pack()

        label_break = tk.Label(self.root, text=_("Tempo de pausa (minutos):"))
        label_break.pack()
        entry_break = tk.Entry(self.root, textvariable=self.break_time)
        entry_break.pack()

        label_cycles = tk.Label(self.root, text=_("Quantos ciclos Pomodoro:"))
        label_cycles.pack()
        entry_cycles = tk.Entry(self.root, textvariable=self.cycles)
        entry_cycles.pack()

        start_button = tk.Button(self.root, text=_("Iniciar"), command=self.start_pomodoro)
        start_button.pack()

        stop_button = tk.Button(self.root, text=_("Parar"), command=self.stop_pomodoro)
        stop_button.pack()

        self.current_cycle_label = tk.Label(self.root, text=_("Ciclo atual: 0"))
        self.current_cycle_label.pack()

        self.timer_label = tk.Label(self.root, text=_("Tempo restante:"))
        self.timer_label.pack()

        select_sound_button = tk.Button(self.root, text=_("Selecionar Som"), command=self.save_last_sound)
        select_sound_button.pack()

        self.message_label = tk.Label(self.root, text="")
        self.message_label.pack()

        self.sound_file = ""

    def load_settings(self):
        config = configparser.ConfigParser()
        try:
            config.read("Lampodoro_settings.ini")
            self.work_time.set(config.get("Settings", "work_time"))
            self.break_time.set(config.get("Settings", "break_time"))
            self.cycles.set(config.getint("Settings", "cycles"))
            self.sound_file = config.get("Settings", "sound_file")
        except:
            self.save_settings()

    def save_settings(self):
        config = configparser.ConfigParser()
        config["Settings"] = {
            "work_time": self.work_time.get(),
            "break_time": self.break_time.get(),
            "cycles": self.cycles.get(),
            #"sound_file": self.sound_file
        }
        with open("Lampodoro_settings.ini", "w") as config_file:
            config.write(config_file)

        self.save_last_sound()

    def load_last_sound(self):
        """
        Carrega o caminho do último som utilizado do arquivo de configurações.
        """
        config = configparser.ConfigParser()
        try:
            config.read("Lampodoro_settings.ini")
            self.sound_file = config.get("Settings", "sound_file")
        except:
            self.sound_file = ""

    def save_last_sound(self):
        """
        Salva o caminho do último som utilizado no arquivo de configurações.
        """
        config = configparser.ConfigParser()
        config["Settings"] = {
            "last_sound": self.sound_file
        }
        with open("Lampodoro_settings.ini", "w") as config_file:
            config.write(config_file)

    def start_pomodoro(self):
        logging.debug("start_pomodoro called")

        if not self.pomodoro_started:
            logging.debug("Starting a new pomodoro session")
            self.pomodoro_started = True
            self.save_settings()
            self.current_cycle.set(0)
            self.update_cycle_label()
            work_time = float(self.work_time.get()) * 60
            break_time = float(self.break_time.get()) * 60
            cycles = int(self.cycles.get())

            threading.Thread(target=self.run_pomodoro_thread, args=(work_time, break_time, cycles)).start()

    def run_pomodoro_thread(self, work_time, break_time, cycles):
        logging.debug("Running pomodoro thread")
        for i in range(cycles):
            if not self.pomodoro_started:
                logging.debug("Pomodoro session stopped")
                break

            self.current_cycle.set(i + 1)
            self.update_cycle_label()

            logging.debug("Running pomodoro cycle")
            self.run_pomodoro_cycle(work_time, break_time) 

            if i < cycles - 1:
                self.root.after(int(work_time) * 1000, self.run_break, break_time)

        logging.debug("Pomodoro session completed")
        self.current_cycle.set(0)
        self.update_cycle_label()
        self.pomodoro_started = False
        self.running = False

    def run_break(self, break_time):
        logging.debug("Running break")
        self.run_sleep_timer(break_time, _("Tempo de pausa encerrado!"))

    def run_pomodoro_cycle(self, work_time, break_time):
        logging.debug("Running pomodoro cycle")
        self.run_sleep_timer(work_time, _("Tempo de trabalho encerrado!"))

    def update_timer(self, seconds_left):
        print("update_timer called with seconds_left =", seconds_left)
        logging.debug("update_timer called with seconds_left = %s", seconds_left)
        if self.running:
            elapsed_time = time.time() - self.start_time
            seconds_left = max(0, self.remaining_time - elapsed_time)
            logging.debug("Elapsed Time: %s, Remaining Time: %s, Seconds Left: %s", elapsed_time, self.remaining_time, seconds_left)
            self.timer_label.config(text=_("Tempo restante: ") + self.format_time(seconds_left))

    def run_sleep_timer(self, seconds, message):
        logging.debug("run_sleep_timer called with seconds = %s", seconds)
        self.running = True
        self.start_time = time.time()
        self.remaining_time = seconds
        self.current_message = message

        self.update_timer(self.remaining_time)
        threading.Timer(1, self.update_timer_thread, args=[self.remaining_time - 1]).start()

    def update_timer_thread(self, seconds_left):
        if self.running and seconds_left >= 0:
            self.update_timer(seconds_left)
            threading.Timer(1, self.update_timer_thread, args=[seconds_left - 1]).start()

    def stop_pomodoro(self):
        logging.debug("Stopping pomodoro session")
        self.running = False

    def update_cycle_label(self):
        current_cycle = self.current_cycle.get()
        total_cycles = self.cycles.get()
        self.current_cycle_label.config(text=_("Ciclo atual: {}/{}").format(current_cycle, total_cycles))

    def format_time(self, seconds):
        m, s = divmod(int(seconds), 60)
        return '{:02d}:{:02d}'.format(m, s)

    def play_custom_sound(self, sound_file):
        try:
            winsound.PlaySound(sound_file, winsound.SND_FILENAME)
        except Exception as e:
            self.message_label.config(text=_("Erro ao reproduzir som"), bg="red")
            print(f"Erro ao reproduzir o som: {e}")

    def play_default_sound(self):
        try:
            winsound.Beep(440, 500)  # Frequência de 440 Hz e duração de 500 ms
        except Exception as e:
            self.message_label.config(text=_("Erro ao reproduzir som padrão"), bg="red")
            print(f"Erro ao reproduzir o som padrão: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    
    locale_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "locale"))
    lang = gettext.translation("Lampodoro", localedir=locale_dir, languages=["pt_BR", "en_US", "es_ES"])
    lang.install()

    root = tk.Tk()
    app = Lampodoro(root)
    root.mainloop()
    