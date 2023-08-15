import time
import winsound

class PomodoroTimer:
    """
    Uma classe que implementa um temporizador Pomodoro.
    
    ...

    Attributes
    ----------
    work_time : float
        Tempo de trabalho em minutos.
    short_break_time : float
        Tempo de pausa curta em minutos.
    long_break_time : float
        Tempo de pausa longa em minutos.
    cycles : int
        Número de ciclos Pomodoro a serem executados.

    Methods
    -------
    run()
        Executa os ciclos Pomodoro.
    run_timer(duration, message)
        Executa um temporizador com duração e mensagem específicas.
    print_remaining_time(seconds)
        Imprime o tempo restante no formato MM:SS.
    play_default_sound(signal_type='fim')
        Emite um sinal sonoro padrão.
    """

    def __init__(self, work_time, short_break_time, long_break_time, cycles):     
        self.work_time = work_time * 60  # Convertendo para segundos
        self.short_break_time = short_break_time * 60  # Convertendo para segundos
        self.long_break_time = long_break_time * 60  # Convertendo para segundos
        self.cycles = cycles
        self.current_cycle = 0
        self.cycle_records = []

    def run(self):
        while self.current_cycle < self.cycles:
            self.current_cycle += 1
            print(f'\nIniciando ciclo {self.current_cycle} de trabalho.\n')
            self.play_default_sound('inicio')  # Emitir alerta sonoro ao inicio do período
            work_duration = self.run_timer(self.work_time, '\nTempo de trabalho encerrado!')

            if self.current_cycle < self.cycles:
                if self.current_cycle % 4 == 0:
                    self.play_default_sound('inicio')  # Emitir alerta sonoro ao inicio do período
                    print(f'\nIniciando pausa longa após ciclo {self.current_cycle}.\n')
                    break_duration = self.run_timer(self.long_break_time, '\nPausa longa encerrada.')
                else:
                    self.play_default_sound('inicio')  # Emitir alerta sonoro ao inicio do período
                    print(f'\nIniciando pausa curta após ciclo {self.current_cycle}.')
                    break_duration = self.run_timer(self.short_break_time, '\nPausa curta encerrada.')
                    self.play_default_sound()  # Emitir alerta sonoro de início de próximo ciclo

                self.cycle_records.append({
                    'cycle_number': self.current_cycle,
                    'work_duration': work_duration,
                    'break_duration': break_duration,
                    'break_type': 'longa' if self.current_cycle % 4 == 0 else 'curta',
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                })

        print("\nCiclos concluídos. Aqui estão os registros:")
        for record in self.cycle_records:
            registro = f'''
            Ciclo {record['cycle_number']}:
            Duração de trabalho: {record['work_duration'] / 60:.2f} minutos
            Duração de pausa: {record['break_duration'] / 60:.2f} minutos ({record['break_type']})
            Concluído em: {record['timestamp']}
            \n
            '''
            print(registro)

    def run_timer(self, duration, message):
        start_time = time.time()
        while time.time() - start_time < duration:
            remaining_time = duration - (time.time() - start_time)
            self.print_remaining_time(remaining_time)
            time.sleep(1)
        print(message)
        self.play_default_sound()  # Emitir alerta sonoro ao final do período
        return duration

    def print_remaining_time(self, seconds):
        minutes, seconds = divmod(int(seconds), 60)
        #print(f'Tempo restante: {minutes:02d}:{seconds:02d}')
        return minutes

    def play_default_sound(self, signal_type='fim'):
        try:
            if signal_type == 'inicio':
                winsound.Beep(500, 500)  # Frequência de 540 Hz e duração de 500 ms
                winsound.Beep(550, 750)
                winsound.Beep(750, 1000)
                print('\nSinal Sonoro - Início do período')
            else:
                winsound.Beep(440, 1000)  # Frequência de 440 Hz e duração de 750 ms
                winsound.Beep(220, 750)
                winsound.Beep(100, 500)
                print('\nSinal Sonoro - Fim do período')

        except Exception as e:
            print(f"\nErro ao reproduzir o som padrão: {e}")

def obter_numero(mensagem):
    while True:
        try:
            valor = float(input(mensagem))
            return valor
        except ValueError:
            print("\nDigite um valor numérico válido.")

def obter_inteiro(mensagem):
    while True:
        try:
            valor = int(input(mensagem))
            return valor
        except ValueError:
            print("\nDigite um valor inteiro válido.")

def main():
    mensagem_inicial = '''
    
    Bem-vindo ao Pomodoro Timer!
    
    O método Pomodoro é uma técnica de gerenciamento de tempo que envolve a divisão do trabalho em períodos focados seguidos de pausas curtas.
    Isso pode ajudar a melhorar a produtividade e o foco, reduzindo o cansaço mental.
    Durante o ciclo de trabalho, se concentre em uma tarefa específica. Quando o tempo acabar, faça uma pausa para descansar um pouco antes de iniciar o próximo ciclo.
    Lembre-se de ajustar os tempos de trabalho e pausa de acordo com suas preferências e necessidades.
    
    Aqui estão as melhores práticas para uma alta eficiência ao usar o método Pomodoro:
        - Escolha uma tarefa específica para cada ciclo de trabalho.
        - Elimine distrações durante o ciclo de trabalho.
        - Faça pausas curtas e ativas durante as pausas.
        - Mantenha-se hidratado e alongue-se durante as pausas.
        - Revise seu progresso e ajuste os tempos conforme necessário.

    Revise seu progresso e ajuste os tempos conforme necessário.
        \n
    '''
    print(mensagem_inicial)

    while True:
        input("Pressione Enter para iniciar...")
        
        work_time = obter_numero("Digite o tempo de trabalho (em minutos): ")
        short_break_time = obter_numero("Digite o tempo de pausa curta (em minutos): ")
        long_break_time = obter_numero("Digite o tempo de pausa longa (em minutos): ")
        cycles = obter_inteiro("Digite o número de ciclos Pomodoro: ")
        
        if cycles < 1:
            print("O número de ciclos deve ser pelo menos 1.")
        else:
            pomodoro = PomodoroTimer(work_time, short_break_time, long_break_time, cycles)
            pomodoro.run()
            
        program = input('Deseja iniciar um novo pomodoro? (Y/N): ').lower()
        if program == 'n':
            print('\nFim do Programa\n')
            break

if __name__ == "__main__":
    main()
