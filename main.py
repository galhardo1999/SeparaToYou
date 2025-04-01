import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import separaFotosMulti
import fazerRelatorio
import ttkbootstrap as ttk

class DashboardWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SeparaToYou")
        self.root.geometry("480x350")
        self.root.configure(bg="#f5f6f5")
        self.root.resizable(False, False)

        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 11), padding=10)
        style.configure("TLabel", background="#f5f6f5", font=("Helvetica", 11))
        style.configure("Accent.TButton", background="#ADD8E6", foreground="black")
        style.configure("Transparent.TFrame", background="#f5f6f5")

        frame_principal = ttk.Frame(self.root, padding="20", style="Transparent.TFrame")
        frame_principal.pack(fill="both", expand=True)

        titulo = ttk.Label(frame_principal, text="SeparaToYou", font=("Helvetica", 20, "bold"), foreground="#0288D1")
        titulo.pack(pady=(20, 0))
        subtitulo = ttk.Label(frame_principal, text="Ferramenta de Separação de Fotos", font=("Helvetica", 10, "italic"), foreground="#666")
        subtitulo.pack(pady=(2, 30))

        frame_botoes = ttk.Frame(frame_principal, style="Transparent.TFrame")
        frame_botoes.pack()

        botao_separar_fotos_multi = ttk.Button(frame_botoes, text="Separar Fotos de Alunos", command=self.abrir_separar_fotos_multi, style="Accent.TButton", width=30)
        botao_separar_fotos_multi.pack(pady=10)

        botao_relatorio = ttk.Button(frame_botoes, text="Relatório de Alunos", command=self.abrir_fazer_relatorio, style="Accent.TButton", width=30)
        botao_relatorio.pack(pady=10)

        rodape = ttk.Label(frame_principal, text="© 2025 - Desenvolvido por Alexandre Galhardo", font=("Helvetica", 8), foreground="#999")
        rodape.pack(side="bottom", pady=10)

        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)

    def abrir_fazer_relatorio(self):
        try:
            janela_relatorio = tk.Toplevel(self.root)
            app = fazerRelatorio.GeradorRelatorioComparativo(janela_relatorio)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao abrir o gerador de relatórios: {str(e)}")

    def abrir_separar_fotos_multi(self):
        try:
            separaFotosMulti.janela_separador_fotos_multi(self.root)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao abrir separador de fotos: {str(e)}")

    def run(self):
        self.root.mainloop()

def main():
    root = DashboardWindow()
    root.run()  # Chama o método run() da classe

if __name__ == "__main__":
    main()