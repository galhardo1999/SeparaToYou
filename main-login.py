import face_recognition
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import separaFotosMulti
import fazerRelatorio
import requests
import sys
import ttkbootstrap as ttk
#pyinstaller --onefile --windowed --add-data "C:\Users\Apolo\AppData\Roaming\Python\Python313\site-packages\face_recognition_models\models;face_recognition_models/models" main-login.py
API_URL = "http://127.0.0.1:5000/api/verificar-premium-login"

class LoginWindow:
    def __init__(self, root, callback):
        self.root = root
        self.root.title("Login - SeparaToYou")
        self.root.geometry("350x300")
        self.root.resizable(False, False)
        self.callback = callback

        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 11), padding=10)
        style.configure("TLabel", background="#f5f6f5", font=("Helvetica", 11))
        style.configure("Accent.TButton", background="#0288D1", foreground="white")
        style.configure("Transparent.TFrame", background="#f5f6f5")

        frame = ttk.Frame(self.root, padding=20, style="Transparent.TFrame")
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Login", font=("Helvetica", 18, "bold"), foreground="#0288D1").pack(pady=10)

        ttk.Label(frame, text="E-mail:").pack(anchor="w")
        self.email_entry = ttk.Entry(frame, width=35)
        self.email_entry.pack(pady=5)

        ttk.Label(frame, text="Senha:").pack(anchor="w")
        self.senha_entry = ttk.Entry(frame, width=35, show="*")
        self.senha_entry.pack(pady=5)

        self.login_button = ttk.Button(frame, text="Entrar", style="Accent.TButton", command=self.verificar_login)
        self.login_button.pack(pady=15)

        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def verificar_login(self):
        email = self.email_entry.get()
        senha = self.senha_entry.get()
        if not email or not senha:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
            return

        try:
            response = requests.post(API_URL, json={"email": email, "senha": senha}, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get("premium"):
                    self.root.destroy()
                    self.callback()
                else:
                    messagebox.showerror("Erro", "Acesso negado. Você precisa de um plano premium.")
                    sys.exit(1)
            else:
                messagebox.showerror("Erro", "Credenciais inválidas. Verifique seu e-mail e senha.")
        except requests.RequestException as e:
            messagebox.showerror("Erro", f"Erro ao conectar ao servidor: {e}")
            sys.exit(1)

class DashboardWindow:
    def __init__(self):
        self.janela_dashboard = tk.Tk()
        self.janela_dashboard.title("SeparaToYou")
        self.janela_dashboard.geometry("480x350")
        self.janela_dashboard.configure(bg="#f5f6f5")
        self.janela_dashboard.resizable(False, False)

        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 11), padding=10)
        style.configure("TLabel", background="#f5f6f5", font=("Helvetica", 11))
        style.configure("Accent.TButton", background="#ADD8E6", foreground="black")
        style.configure("Transparent.TFrame", background="#f5f6f5")

        frame_principal = ttk.Frame(self.janela_dashboard, padding="20", style="Transparent.TFrame")
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

        self.janela_dashboard.update_idletasks()
        width = self.janela_dashboard.winfo_width()
        height = self.janela_dashboard.winfo_height()
        x = (self.janela_dashboard.winfo_screenwidth() // 2) - (width // 2)
        y = (self.janela_dashboard.winfo_screenheight() // 2) - (height // 2)
        self.janela_dashboard.geometry(f"{width}x{height}+{x}+{y}")

        self.janela_dashboard.protocol("WM_DELETE_WINDOW", self.janela_dashboard.quit)

    def abrir_fazer_relatorio(self):
        try:
            janela_relatorio = tk.Toplevel(self.janela_dashboard)
            app = fazerRelatorio.GeradorRelatorioComparativo(janela_relatorio)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao abrir o gerador de relatórios: {str(e)}")

    def abrir_separar_fotos_multi(self):
        try:
            separaFotosMulti.janela_separador_fotos_multi(self.janela_dashboard)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao abrir separador de fotos: {str(e)}")

    def run(self):
        self.janela_dashboard.mainloop()

def main():
    root = tk.Tk()
    login_app = LoginWindow(root, lambda: DashboardWindow().run())
    root.mainloop()

if __name__ == "__main__":
    main()