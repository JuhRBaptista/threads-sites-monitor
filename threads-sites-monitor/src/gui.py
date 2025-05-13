import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import threading
from .verification import monothreading_verification, multithreading_verification, monitor_system_usage
from .plot import plot_all

class ThreadMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Thread Monitor - Comparador de Desempenho")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        self.sites = []
        self.filename = None
        self.results = {
            "mono": {"time": None, "cpu": None, "mem": None},
            "multi": {"time": None, "cpu": None, "mem": None}
        }

        self.show_buttom = False

        self.create_widgets()

    def create_widgets(self):
        # Título
        title = tk.Label(self.root, text="Monitoramento de Sites com Threads", font=("Helvetica", 16, "bold"))
        title.pack(pady=10)

        # Botão para carregar arquivo
        self.load_button = ttk.Button(self.root, text="Selecionar Arquivo de Sites", command=self.load_file)
        self.load_button.pack(pady=10)

        self.file_label = tk.Label(self.root, text="Nenhum arquivo selecionado", fg="gray")
        self.file_label.pack()

        # Botões de execução
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=15)

        self.mono_button = ttk.Button(button_frame, text="Executar Monothread", command=lambda: self.run_monitoring(monothreading_verification))
        self.mono_button.grid(row=0, column=0, padx=10)

        self.multi_button = ttk.Button(button_frame, text="Executar Multithread", command=lambda: self.run_monitoring(multithreading_verification))
        self.multi_button.grid(row=0, column=1, padx=10)

        self.show_performance = ttk.Button(button_frame, text="Comparar Resultados", command=lambda: plot_all(self.results))
        self.show_performance.grid(row=1, column=0, columnspan=2, pady=15)
        self.show_performance.grid_remove()

        # Indicador de status
        self.status_label = tk.Label(self.root, text="", font=("Helvetica", 11, "italic"))
        self.status_label.pack(pady=10)
        
        # Área de resultado
        self.result_label = tk.Label(self.root, text="", font=("Helvetica", 12))
        self.result_label.pack(pady=10)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            self.filename = file_path
            try:
                with open(file_path, "r") as f:
                    self.sites = [line.strip() for line in f if line.strip()]
                self.file_label.config(text=f"{len(self.sites)} sites carregados.")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao ler o arquivo: {e}")
        else:
            self.file_label.config(text="Nenhum arquivo selecionado")

    def run_monitoring(self, verification_func):
        if not self.sites:
            messagebox.showwarning("Aviso", "Carregue um arquivo de sites primeiro!")
            return

        self.status_label.config(text="Executando, por favor aguarde...")
        self.result_label.config(text="")
        self.mono_button["state"] = "disabled"
        self.multi_button["state"] = "disabled"

        threading.Thread(target=self._execute_with_monitoring, args=(verification_func,)).start()

    def _execute_with_monitoring(self, func):

        mode = "multi" if func == multithreading_verification else "mono"
        stop_event = threading.Event()
        data = {}
        monitor_thread = threading.Thread(target=monitor_system_usage, args=(stop_event, data))
        monitor_thread.start()

        time_taken = func(self.sites)
        print(time_taken)
        stop_event.set()
        monitor_thread.join()

        self.results[mode]["time"] = time_taken
        self.results[mode]["cpu"] = data["cpu"]
        self.results[mode]["mem"] = data["memory"]
        
        self.root.after(0, lambda: self.on_monitoring_complete(mode))

    def on_monitoring_complete(self, mode):
        method_name = "Multithread" if mode == "multi" else "Monothread"
        tempo = self.results[mode]["time"]

        self.status_label.config(text=f"Execução {method_name} finalizada.")
        self.result_label.config(text=f"[{method_name}] Tempo total: {round(tempo, 2)}s")

        self.mono_button["state"] = "normal"
        self.multi_button["state"] = "normal"

        # Se os dois testes foram feitos, exibe os gráficos
        if self.results["mono"]["time"] and self.results["multi"]["time"]:
            self.show_performance.grid()
 


def start_app():
    root = tk.Tk()
    app = ThreadMonitorApp(root)
    root.mainloop()
