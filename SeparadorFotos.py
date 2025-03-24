import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import separaFotos
import fazerRelatorio

def abrir_fazer_relatorio():
    try:
        # Criar uma nova janela para o relatório
        janela_relatorio = tk.Toplevel(janela_dashboard)
        app = fazerRelatorio.GeradorRelatorioComparativo(janela_relatorio)
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao abrir o gerador de relatórios: {str(e)}")

def abrir_separar_fotos():
    try:
        separaFotos.janela_separador_fotos(janela_dashboard)
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao abrir separador de fotos: {str(e)}")

# Configuração da janela principal
janela_dashboard = tk.Tk()
janela_dashboard.title("SeparooU")
janela_dashboard.geometry("500x350")
janela_dashboard.configure(bg="#f5f6f5")
janela_dashboard.resizable(False, False)

# Estilo ttk
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 11), padding=10)
style.configure("TLabel", background="#f5f6f5", font=("Helvetica", 11))
style.configure("Accent.TButton", background="#ADD8E6", foreground="black")
style.configure("Transparent.TFrame", background="#f5f6f5")

# Frame principal
frame_principal = ttk.Frame(janela_dashboard, padding="20", style="Transparent.TFrame")
frame_principal.pack(fill="both", expand=True)

# Título e subtítulo
titulo = ttk.Label(frame_principal, text="SeparooU", font=("Helvetica", 20, "bold"), foreground="#0288D1")
titulo.pack(pady=(20, 0))
subtitulo = ttk.Label(frame_principal, text="Ferramenta de Separação de Fotos", font=("Helvetica", 10, "italic"), foreground="#666")
subtitulo.pack(pady=(2, 30))

# Frame para botões
frame_botoes = ttk.Frame(frame_principal, style="Transparent.TFrame")
frame_botoes.pack()

# Botões
botao_separar_fotos = ttk.Button(frame_botoes, text="Separar Fotos de Alunos", command=abrir_separar_fotos, style="Accent.TButton", width=30)
botao_separar_fotos.pack(pady=10)

botao_relatorio = ttk.Button(frame_botoes, text="Relatório de Alunos", command=abrir_fazer_relatorio, style="Accent.TButton", width=30)
botao_relatorio.pack(pady=10)

# Rodapé
rodape = ttk.Label(frame_principal, text="© 2025 - Desenvolvido por Alexandre Galhardo", font=("Helvetica", 8), foreground="#999")
rodape.pack(side="bottom", pady=10)

# Centralizar janela
janela_dashboard.update_idletasks()
width = janela_dashboard.winfo_width()
height = janela_dashboard.winfo_height()
x = (janela_dashboard.winfo_screenwidth() // 2) - (width // 2)
y = (janela_dashboard.winfo_screenheight() // 2) - (height // 2)
janela_dashboard.geometry(f"{width}x{height}+{x}+{y}")

# Protocolo de fechamento
janela_dashboard.protocol("WM_DELETE_WINDOW", janela_dashboard.quit)

# Iniciar o dashboard
janela_dashboard.mainloop()