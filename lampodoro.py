import tkinter as tk
from tkinter import messagebox
import time
import configparser
import gettext
import os

class Lampodoro:
    def __init__(self, root):
        """
        Inicializa o Lampodoro.

        Args:
            root (tk.Tk): O objeto root da interface gráfica Tkinter.
        """
        self.root = root
        self.root.title(_("Lampodoro"))
        self.work_time = tk.StringVar()
        self.break_time = tk.StringVar()
        self.cycles = tk.IntVar()
        self.current_cycle = tk.IntVar(value=0)
        self.running = False
        self.start_time = 0

        self.load_settings()
        self.create_widgets()

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

    def load_settings(self):
        """
        Carrega as configurações salvas do arquivo lampodoro_settings.ini.
        Caso o arquivo não exista ou não possa ser lido, valores padrão serão utilizados.
        """
        config = configparser.ConfigParser()
        try:
            config.read("lampodoro_settings.ini")
            self.work_time.set(config.get("Settings", "work_time"))
            self.break_time.set(config.get("Settings", "break_time"))
            self.cycles.set(config.getint("Settings", "cycles"))
        except:
            self.work_time.set("25")
            self.break_time.set("5")
            self.cycles.set(4)

    def save_settings(self):
        """
        Salva as configurações personalizadas do usuário no arquivo lampodoro_settings.ini.
        """
        config = configparser.ConfigParser()
        config["Settings"] = {
            "work_time": self.work_time.get(),
            "break_time": self.break_time.get(),
            "cycles": self.cycles.get()
        }
        with open("lampodoro_settings.ini", "w") as config_file:
            config.write(config_file)

    def start_pomodoro(self):
        """
        Inicia os ciclos de trabalho e pausa do Pomodoro.
        """
        if not self.running:
            self.save_settings()
            self.current_cycle.set(0)
            self.update_cycle_label()
            work_time = int(self.work_time.get()) * 60
            break_time = int(self.break_time.get()) * 60
            cycles = self.cycles.get()
            work_message = _("Tempo de trabalho encerrado!")
            break_message = _("Pausa encerrada!")
            for i in range(cycles):
                self.current_cycle.set(self.current_cycle.get() + 1)
                self.update_cycle_label()
                self.run_timer(work_time, work_message)
                self.run_timer(break_time, break_message)
            self.current_cycle.set(0)
            self.update_cycle_label()

    def format_time(self, seconds):
        """
        Formata o tempo em segundos para o formato 'MM:SS'.

        Args:
            seconds (int): O tempo em segundos.

        Returns:
            str: O tempo formatado no formato 'MM:SS'.
        """
        m, s = divmod(int(seconds), 60)
        return '{:02d}:{:02d}'.format(m, s)
 
    def run_timer(self, seconds, message):
        """
        Executa o timer para o tempo especificado.

        Args:
            seconds (int): O tempo em segundos.
            message (str): A mensagem a ser exibida quando o tempo se esgotar.
        """
        self.running = True
        self.start_time = time.time()
        while seconds > 0:
            if not self.running:
                break
            elapsed_time = time.time() - self.start_time
            seconds_left = max(0, seconds - elapsed_time)
            time_format = self.format_time(seconds_left)
            self.timer_label.config(text=_("Tempo restante: ") + time_format)
            self.root.update()
            time.sleep(1)
        self.running = False
        self.root.title(_("Lampodoro"))
        self.timer_label.config(text=_("Tempo restante: "))
        messagebox.showinfo(_("Lampodoro"), message)

    def stop_pomodoro(self):
        """
        Para a execução dos ciclos de trabalho e pausa.
        """
        self.running = False

    def update_cycle_label(self):
        """
        Atualiza o label do ciclo atual.
        """
        current_cycle = self.current_cycle.get()
        total_cycles = self.cycles.get()
        self.current_cycle_label.config(text=_("Ciclo atual: {}/{}").format(current_cycle, total_cycles))

if __name__ == "__main__":
    # Configuração de internacionalização
    locale_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "locale"))
    lang = gettext.translation("lampodoro", localedir=locale_dir, languages=["pt_BR", "en_US", "es_ES"])
    lang.install()
    
    root = tk.Tk()
    lampodoro = Lampodoro(root)
    root.mainloop()
