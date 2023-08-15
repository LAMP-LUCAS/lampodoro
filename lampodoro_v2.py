import time
import threading
import lampodoro_lib
import sys
from plyer import notification

def draw_progress_bar(progress):
    bar_length = 40
    block = int(round(bar_length * progress))
    progress_bar = "[" + "#" * block + "-" * (bar_length - block) + "]"
    return progress_bar

def update_progress_bar(duration, notification_event):
    start_time = time.time()
    while time.time() - start_time < duration:
        elapsed_time = time.time() - start_time
        progress = 1 - (elapsed_time / duration)
        progress_bar = draw_progress_bar(progress)
        time_remaining = int(duration - elapsed_time)
        sys.stdout.write(f"\r{progress_bar} {time_remaining // 60:02d}:{time_remaining % 60:02d} ")
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\r" + " " * 60 + "\r" )  # Limpa a linha
    sys.stdout.flush()
    notification_event.set()

def main():
    print("Bem-vindo ao Pomodoro Timer com Gráfico de Barras!\n")
    
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
        print("Pressione Enter para iniciar o Pomodoro ou Esc para sair...")
        start_key = input()

        if start_key.lower() == "esc":
            print("\nSaindo do Pomodoro Timer...")
            break
        
        work_time = lampodoro_lib.obter_numero("Digite o tempo de trabalho (em minutos): ")
        short_break_time = lampodoro_lib.obter_numero("Digite o tempo de pausa curta (em minutos): ")
        long_break_time = lampodoro_lib.obter_numero("Digite o tempo de pausa longa (em minutos): ")
        cycles = lampodoro_lib.obter_inteiro("Digite o número de ciclos Pomodoro: ")

        if cycles < 1:
            print("O número de ciclos deve ser pelo menos 1.")
        else:
            pomodoro_timer = lampodoro_lib.PomodoroTimer(work_time, short_break_time, long_break_time, cycles)

            for _ in range(cycles):
                print(f'\nIniciando ciclo {_ + 1} de trabalho.\n')
                notification_event = threading.Event()
                update_thread = threading.Thread(target=update_progress_bar, args=(work_time * 60, notification_event))
                update_thread.start()
                pomodoro_timer.run_timer(work_time * 60, 'Tempo de trabalho encerrado!')
                update_thread.join()
                notification_event.wait()  # Aguarda a notificação antes de continuar
                notification.notify(
                        title="Pomodoro - Tempo de trabalho encerrado",
                        message=f"Ciclo {_ + 1}. Tempo de desncanso começando.",
                        app_name="Pomodoro Timer"
                    )

                if _ + 1 < cycles:
                    if (_ + 1) % 4 == 0:
                        print(f'\nIniciando pausa longa após ciclo {_ + 1}.\n')
                        notification_event = threading.Event()
                        update_thread = threading.Thread(target=update_progress_bar, args=(long_break_time * 60, notification_event))
                        update_thread.start()
                        pomodoro_timer.run_timer(long_break_time * 60, 'Pausa longa encerrada.')
                        update_thread.join()
                        notification_event.wait()  # Aguarda a notificação antes de continuar
                    else:
                        print(f'Iniciando pausa curta após ciclo {_ + 1}.')
                        notification_event = threading.Event()
                        update_thread = threading.Thread(target=update_progress_bar, args=(short_break_time * 60, notification_event))
                        update_thread.start()
                        pomodoro_timer.run_timer(short_break_time * 60, 'Pausa curta encerrada.')
                        update_thread.join()
                        notification_event.wait()  # Aguarda a notificação antes de continuar
                        notification.notify(
                        title="Pomodoro - Tempo de pausa encerrado",
                        message=f"Ciclo {_ + 1}. Tempo de trabalho começando.",
                        app_name="Pomodoro Timer"
                    )

                    pomodoro_timer.play_default_sound()
                    '''
                    notification.notify(
                        title="Pomodoro Concluído",
                        message=f"Ciclo {_ + 1} concluído. Próximo ciclo começando.",
                        app_name="Pomodoro Timer"
                    )
                    '''

            print("\nCiclos concluídos. Aqui estão os registros:")
            for record in pomodoro_timer.cycle_records:
                registro = f'''
                Ciclo {record['cycle_number']}:
                Duração de trabalho: {record['work_duration'] / 60:.2f} minutos
                Duração de pausa: {record['break_duration'] / 60:.2f} minutos ({record['break_type']})
                Concluído em: {record['timestamp']}
                \n
                '''
                print(registro)

if __name__ == "__main__":
    main()
