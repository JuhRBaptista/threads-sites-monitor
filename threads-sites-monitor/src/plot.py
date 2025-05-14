import matplotlib.pyplot as plt

def plot_time_comparison(mono_time, multi_time):
  
    performance_gain = ((mono_time - multi_time) / mono_time) * 100

    plt.figure(figsize=(15, 10))

    # Gráfico de Tempo de Processamento
    plt.subplot(1, 2, 1)
    plt.bar("Monothread", mono_time, color=['blue'])
    plt.bar("Multithread", multi_time, color=['orange'])
    plt.ylabel('Tempo de Processamento (segundos)')
    plt.title('Comparação de Desempenho: Tempo de Processamento')
    plt.grid(axis='y')


    # Gráfico de Ganho de Desempenho (apenas valor)
    plt.subplot(1, 2, 2)
    plt.bar(['Ganho de Desempenho'], [performance_gain], color='green')
    plt.title(f"Ganho de Desempenho: {round(performance_gain, 2)}%")
    plt.ylabel('Ganho (%)')
    plt.ylim(0, 100)  # Ajuste para garantir que o gráfico tenha escala de 0 a 100%
    # Exibindo o valor no centro da barra
    plt.text(0, performance_gain + 5, f'{round(performance_gain, 2)}%', ha='center', color='white', fontsize=12)

    plt.tight_layout()
    plt.show()

def plot_cpu_comparison(cpu_usage_mono, cpu_usage_multi, mono_time):

    plt.figure(figsize=(15, 10))
    plt.plot(cpu_usage_mono, label='Monothread', color='blue')
    plt.plot(cpu_usage_multi, label='Multithreads', color='orange')
    plt.ylabel('Uso da CPU (%)')
    plt.title('Utilização da CPU')
    plt.xlabel('Tempo(s*10)')
    plt.xlim(0, int(mono_time*10))
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

def plot_memory_usage(memory_usage_mono, memory_usage_multi, mono_time):

    # Gráfico de Utilização da Memória
    plt.figure(figsize=(15, 10)) 
    plt.plot(memory_usage_mono, label='Monothread', color='blue')
    plt.plot(memory_usage_multi, label='Multithreads', color='orange')
    plt.ylabel('Uso da Memória (%)')
    plt.title('Utilização da Memória')
    plt.xlabel('Tempo(s*10)')
    plt.xlim(0, int(mono_time*10))
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

def plot_all(results):
    plot_time_comparison(results["mono"]["time"], results["multi"]["time"])
    plot_cpu_comparison(results["mono"]["cpu"], results["multi"]["cpu"], results["mono"]["time"])
    plot_memory_usage(results["mono"]["mem"], results["multi"]["mem"], results["mono"]["time"])


