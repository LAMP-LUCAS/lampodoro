import time
import winsound

class PomodoroTimer:
    def __init__(self, work_time, short_break_time, long_break_time, cycles):
        self.work_time = work_time * 60  # Convertendo para segundos
        self.short_break_time = short_break_time * 60  # Convertendo para segundos
        self.long_break_time = long_break_time * 60  # Convertendo para segundos
        self.cycles = cycles
        self.current_cycle = 0

    def run(self):
        while self.current_cycle < self.cycles:
            self.current_cycle += 1
            print(f'Iniciando ciclo {self.current_cycle} de trabalho.')
            self.play_default_sound('inicio')  # Emitir alerta sonoro ao inicio do período
            self.run_timer(self.work_time, 'Tempo de trabalho encerrado!')

            if self.current_cycle < self.cycles:
                if self.current_cycle % 4 == 0:
                    self.play_default_sound('inicio')  # Emitir alerta sonoro ao inicio do período
                    print(f'Iniciando pausa longa após ciclo {self.current_cycle}.')
                    self.run_timer(self.long_break_time, 'Pausa longa encerrada.')
                else:
                    self.play_default_sound('inicio')  # Emitir alerta sonoro ao inicio do período
                    print(f'Iniciando pausa curta após ciclo {self.current_cycle}.')
                    self.run_timer(self.short_break_time, 'Pausa curta encerrada.')
                    self.play_default_sound()  # Emitir alerta sonoro de início de próximo ciclo

    def run_timer(self, duration, message):
        start_time = time.time()
        while time.time() - start_time < duration:
            remaining_time = duration - (time.time() - start_time)
            self.print_remaining_time(remaining_time)
            time.sleep(1)
        print(message)
        self.play_default_sound()  # Emitir alerta sonoro ao final do período

    def print_remaining_time(self, seconds):
        minutes, seconds = divmod(int(seconds), 60)
        print(f'Tempo restante: {minutes:02d}:{seconds:02d}')

    def play_default_sound(self, signal_type='fim'):
        try:
            if signal_type == 'inicio':
                winsound.Beep(540, 500)  # Frequência de 540 Hz e duração de 500 ms
                print('Sinal Sonoro - Início do período')
            else:
                winsound.Beep(440, 750)  # Frequência de 440 Hz e duração de 750 ms
                print('Sinal Sonoro - Fim do período')

        except Exception as e:
            print(f"Erro ao reproduzir o som padrão: {e}")

if __name__ == "__main__":
    work_time = float(input("Digite o tempo de trabalho (em minutos): "))
    short_break_time = float(input("Digite o tempo de pausa curta (em minutos): "))
    long_break_time = float(input("Digite o tempo de pausa longa (em minutos): "))
    cycles = int(input("Digite o número de ciclos Pomodoro: "))

    if cycles < 1:
        print("O número de ciclos deve ser pelo menos 1.")
    else:
        pomodoro = PomodoroTimer(work_time, short_break_time, long_break_time, cycles)
        pomodoro.run()
