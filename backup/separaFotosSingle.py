import face_recognition 
import os
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import time
from PIL import Image, ImageEnhance
import threading

class SeparadorFotos:
    def __init__(self, root):
        self.root = root
        self.root.title("Separador de Fotos por Reconhecimento Facial")
        self.root.geometry("740x650")
        self.root.configure(bg="#f5f6f5")

        self.pasta_fotos = tk.StringVar()
        self.pasta_identificacao = tk.StringVar()
        self.pasta_saida = tk.StringVar()
        self.cancelar = False
        self.processamento_ativo = False

        # Estilo ttk
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 11), padding=10)
        style.configure("TLabel", background="#f5f6f5", font=("Helvetica", 11))
        style.configure("Accent.TButton", background="#ADD8E6", foreground="black", font=("Helvetica", 11), padding=(10, 2))
        style.configure("Transparent.TFrame", background="#f5f6f5")
        style.configure("TProgressbar", thickness=20)

        # Frame principal
        frame_principal = ttk.Frame(self.root, padding="20", style="Transparent.TFrame")
        frame_principal.grid(row=0, column=0, sticky="nsew")

        # Título e subtítulo
        ttk.Label(frame_principal, text="Separador de Fotos", font=("Helvetica", 20, "bold"), foreground="#0288D1").grid(row=0, column=0, columnspan=3, pady=(0, 2))
        ttk.Label(frame_principal, text="Version Alpha 1.0.1 - Single-Processing", font=("Helvetica", 10, "italic"), foreground="#666").grid(row=1, column=0, columnspan=3, pady=(0, 8))

        # Interface
        ttk.Label(frame_principal, text="Pasta com Todas as Fotos:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(frame_principal, textvariable=self.pasta_fotos, width=50).grid(row=2, column=1, padx=5, pady=3)
        ttk.Button(frame_principal, text="Selecionar", command=self.selecionar_pasta_fotos, style="Accent.TButton").grid(row=2, column=2, padx=5, pady=5)

        ttk.Label(frame_principal, text="Pasta de Identificação dos Alunos:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(frame_principal, textvariable=self.pasta_identificacao, width=50).grid(row=3, column=1, padx=5, pady=3)
        ttk.Button(frame_principal, text="Selecionar", command=self.selecionar_pasta_identificacao, style="Accent.TButton").grid(row=3, column=2, padx=5, pady=5)

        ttk.Label(frame_principal, text="Pasta de Saída:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(frame_principal, textvariable=self.pasta_saida, width=50).grid(row=4, column=1, padx=5, pady=3)
        ttk.Button(frame_principal, text="Selecionar", command=self.selecionar_pasta_saida, style="Accent.TButton").grid(row=4, column=2, padx=5, pady=5)

        # Frame para o texto com barra de rolagem
        texto_frame = ttk.Frame(frame_principal)
        texto_frame.grid(row=5, column=0, columnspan=3, padx=5, pady=10, sticky="nsew")

        # Área de texto para o log com barra de rolagem
        self.log_texto = tk.Text(texto_frame, height=15, width=97, font=("Helvetica", 10))
        self.log_texto.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(texto_frame, orient="vertical", command=self.log_texto.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_texto.configure(yscrollcommand=scrollbar.set)

        self.progresso = ttk.Progressbar(frame_principal, length=650, mode='determinate')
        self.progresso.grid(row=6, column=0, columnspan=3, padx=5, pady=5)

        self.label_progresso = ttk.Label(frame_principal, text="Progresso: 0% | Tempo estimado: --")
        self.label_progresso.grid(row=7, column=0, columnspan=3, pady=8)

        # Frame para centralizar os botões
        frame_botoes = ttk.Frame(frame_principal, style="Transparent.TFrame")
        frame_botoes.grid(row=8, column=0, columnspan=3, pady=10)

        self.botao_iniciar = ttk.Button(frame_botoes, text="Iniciar Processamento", command=self.iniciar_processamento, style="Accent.TButton", width=25)
        self.botao_iniciar.grid(row=0, column=0, padx=5, pady=8)

        self.botao_cancelar = ttk.Button(frame_botoes, text="Cancelar", command=self.cancelar_processamento, style="Accent.TButton", width=25, state=tk.DISABLED)
        self.botao_cancelar.grid(row=0, column=1, padx=5, pady=8)

        # Rodapé
        ttk.Label(frame_principal, text="© 2025 - Desenvolvido por Alexandre Galhardo", font=("Helvetica", 8), foreground="#999").grid(row=9, column=0, columnspan=3, pady=10)

        # Centralizar janela
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)

    def selecionar_pasta_fotos(self):
        pasta = filedialog.askdirectory()
        if pasta:
            self.pasta_fotos.set(pasta)

    def selecionar_pasta_identificacao(self):
        pasta = filedialog.askdirectory()
        if pasta:
            self.pasta_identificacao.set(pasta)

    def selecionar_pasta_saida(self):
        pasta = filedialog.askdirectory()
        if pasta:
            self.pasta_saida.set(pasta)

    def log(self, mensagem, atualizar_imediatamente=False):
        self.log_texto.insert(tk.END, mensagem + "\n")
        self.log_texto.see(tk.END)
        if atualizar_imediatamente:
            self.root.update()

    def cancelar_processamento(self):
        self.cancelar = True
        self.log("Cancelamento solicitado...")

    def preprocessar_imagem(self, caminho):
        try:
            imagem = Image.open(caminho).convert('RGB')
            largura_max = 500  # Redimensionar para acelerar
            if imagem.width > largura_max:
                proporcao = largura_max / imagem.width
                nova_altura = int(imagem.height * proporcao)
                imagem = imagem.resize((largura_max, nova_altura), Image.Resampling.LANCZOS)
            caminho_temp = caminho + "_temp.jpg"
            imagem.save(caminho_temp)
            imagem_processada = face_recognition.load_image_file(caminho_temp)
            os.remove(caminho_temp)
            return imagem_processada
        except Exception as e:
            self.log(f"Erro ao pré-processar {caminho}: {str(e)}")
            return face_recognition.load_image_file(caminho)

    def processar_fotos(self):
        pasta_fotos = self.pasta_fotos.get()
        pasta_identificacao = self.pasta_identificacao.get()
        pasta_saida = self.pasta_saida.get()

        if not (pasta_fotos and pasta_identificacao and pasta_saida):
            self.root.after(0, lambda: messagebox.showerror("Erro", "Por favor, selecione todas as pastas!"))
            return

        self.cancelar = False
        self.processamento_ativo = True
        self.root.after(0, lambda: self.botao_iniciar.config(state=tk.DISABLED))
        self.root.after(0, lambda: self.botao_cancelar.config(state=tk.NORMAL))
        Path(pasta_saida).mkdir(parents=True, exist_ok=True)
        
        pasta_nao_identificadas = os.path.join(pasta_saida, "Fotos Não Identificadas")
        Path(pasta_nao_identificadas).mkdir(parents=True, exist_ok=True)
        
        self.log("Iniciando processamento...", atualizar_imediatamente=True)

        identificacoes = {}
        for arquivo in os.listdir(pasta_identificacao):
            if self.cancelar:
                break
            caminho = os.path.join(pasta_identificacao, arquivo)
            if not os.path.isfile(caminho) or not arquivo.lower().endswith(('.jpg', '.jpeg', '.png')):
                continue
            try:
                Image.open(caminho).verify()
                imagem = self.preprocessar_imagem(caminho)
                codificacoes = face_recognition.face_encodings(imagem, model="small", num_jitters=0)
                if not codificacoes:
                    self.log(f"Nenhum rosto encontrado em {arquivo}")
                    continue
                codificacao = codificacoes[0]
                nome_aluno = os.path.splitext(arquivo)[0]
                identificacoes[nome_aluno] = codificacao
                self.log(f"Carregada identificação de {nome_aluno}")
            except Exception as e:
                self.log(f"Erro ao carregar {arquivo}: {str(e)}")

        fotos = [os.path.join(raiz, arquivo) for raiz, _, arquivos in os.walk(pasta_fotos) for arquivo in arquivos if arquivo.lower().endswith(('.jpg', '.jpeg', '.png'))]
        total_fotos = len(fotos)
        fotos_processadas = 0
        tempo_inicio = time.time()

        for i, foto in enumerate(fotos):
            if self.cancelar:
                break
            try:
                Image.open(foto).verify()
                imagem_desconhecida = self.preprocessar_imagem(foto)
                codificacoes_desconhecidas = face_recognition.face_encodings(imagem_desconhecida, model="small", num_jitters=0)

                if len(codificacoes_desconhecidas) == 0:
                    destino = os.path.join(pasta_nao_identificadas, os.path.basename(foto))
                    shutil.copy(foto, destino)
                    self.log(f"Nenhum rosto encontrado em {foto}")
                else:
                    identificados = False
                    for j, codificacao_desconhecida in enumerate(codificacoes_desconhecidas):
                        distancias = face_recognition.face_distance(list(identificacoes.values()), codificacao_desconhecida)
                        tolerancia = 0.55
                        menor_distancia = min(distancias) if distancias.size > 0 else float('inf')

                        if menor_distancia <= tolerancia:
                            identificados = True
                            indice_melhor = distancias.argmin()
                            nome_aluno = list(identificacoes.keys())[indice_melhor]
                            pasta_aluno = os.path.join(pasta_saida, nome_aluno)
                            Path(pasta_aluno).mkdir(parents=True, exist_ok=True)
                            destino = os.path.join(pasta_aluno, os.path.basename(foto))
                            shutil.copy(foto, destino)
                            self.log(f"Rosto {j+1} em {foto} identificado como {nome_aluno} (distância: {menor_distancia:.2f})")
                        else:
                            self.log(f"Rosto {j+1} em {foto} não identificado (distância: {menor_distancia:.2f})")

                    if not identificados:
                        destino = os.path.join(pasta_nao_identificadas, os.path.basename(foto))
                        shutil.copy(foto, destino)

                fotos_processadas += 1
                percentual = (fotos_processadas / total_fotos) * 100
                self.root.after(0, lambda p=percentual: self.progresso.configure(value=p))

                tempo_decorrido = time.time() - tempo_inicio
                tempo_medio = tempo_decorrido / fotos_processadas if fotos_processadas > 0 else 0
                fotos_restantes = total_fotos - fotos_processadas
                tempo_estimado = tempo_medio * fotos_restantes
                minutos = int(tempo_estimado // 60)
                segundos = int(tempo_estimado % 60)
                tempo_str = f"{minutos}m {segundos}s"
                self.root.after(0, lambda t=tempo_str, p=percentual: self.label_progresso.config(text=f"Progresso: {p:.1f}% | Tempo estimado: {t}"))

                # Atualizar interface a cada 10 fotos
                if i % 10 == 0 or i == total_fotos - 1:
                    self.root.update()

            except Exception as e:
                self.log(f"Erro ao processar {foto}: {str(e)}")
                destino = os.path.join(pasta_nao_identificadas, os.path.basename(foto))
                shutil.copy(foto, destino)

        self.processamento_ativo = False
        if self.cancelar:
            self.log("Processamento cancelado.", atualizar_imediatamente=True)
            self.root.after(0, lambda: messagebox.showinfo("Cancelado", "O processamento foi interrompido."))
        else:
            self.log("Processamento concluído!", atualizar_imediatamente=True)
            self.root.after(0, lambda: messagebox.showinfo("Concluído", "O processamento das fotos foi finalizado."))

        self.root.after(0, lambda: self.botao_iniciar.config(state=tk.NORMAL))
        self.root.after(0, lambda: self.botao_cancelar.config(state=tk.DISABLED))
        self.root.after(0, lambda: self.progresso.configure(value=0))
        self.root.after(0, lambda: self.label_progresso.config(text="Progresso: 0% | Tempo estimado: --"))

    def iniciar_processamento(self):
        if not self.processamento_ativo:
            thread = threading.Thread(target=self.processar_fotos)
            thread.start()

def janela_separador_fotos(master=None):
    root = tk.Toplevel(master)
    app = SeparadorFotos(root)
    return root

if __name__ == "__main__":
    root = tk.Tk()
    app = SeparadorFotos(root)
    root.mainloop()