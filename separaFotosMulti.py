import face_recognition
import os
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import time
from PIL import Image
from multiprocessing import Pool, cpu_count
import threading
import pickle

class SeparadorFotos:
    def __init__(self, root):
        self.root = root
        self.root.title("Separador de Fotos por Reconhecimento Facial")
        self.root.geometry("740x700")
        self.root.configure(bg="#f5f6f5")

        self.pasta_fotos = tk.StringVar()
        self.pasta_identificacao = tk.StringVar()
        self.pasta_saida = tk.StringVar()
        self.cancelar = False
        self.processamento_ativo = False
        self.modo_multi = tk.BooleanVar(value=False)
        self.tolerancia = tk.DoubleVar(value=0.55)

        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 11), padding=10)
        style.configure("TLabel", background="#f5f6f5", font=("Helvetica", 11))
        style.configure("Accent.TButton", background="#ADD8E6", foreground="black", font=("Helvetica", 11), padding=(10, 2))
        style.configure("Transparent.TFrame", background="#f5f6f5")
        style.configure("TProgressbar", thickness=20)

        frame_principal = ttk.Frame(self.root, padding="20", style="Transparent.TFrame")
        frame_principal.grid(row=0, column=0, sticky="nsew")

        ttk.Label(frame_principal, text="Separador de Fotos", font=("Helvetica", 20, "bold"), foreground="#0288D1").grid(row=0, column=0, columnspan=3, pady=(0, 2))
        ttk.Label(frame_principal, text="Version Alpha 1.0.1 - Single/Multi Processing", font=("Helvetica", 10, "italic"), foreground="#666").grid(row=1, column=0, columnspan=3, pady=(0, 8))

        ttk.Label(frame_principal, text="Pasta com Todas as Fotos:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(frame_principal, textvariable=self.pasta_fotos, width=50).grid(row=2, column=1, padx=5, pady=3)
        ttk.Button(frame_principal, text="Selecionar", command=self.selecionar_pasta_fotos, style="Accent.TButton").grid(row=2, column=2, padx=5, pady=5)

        ttk.Label(frame_principal, text="Pasta de Identificação dos Alunos:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(frame_principal, textvariable=self.pasta_identificacao, width=50).grid(row=3, column=1, padx=5, pady=3)
        ttk.Button(frame_principal, text="Selecionar", command=self.selecionar_pasta_identificacao, style="Accent.TButton").grid(row=3, column=2, padx=5, pady=5)

        ttk.Label(frame_principal, text="Pasta de Saída:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(frame_principal, textvariable=self.pasta_saida, width=50).grid(row=4, column=1, padx=5, pady=3)
        ttk.Button(frame_principal, text="Selecionar", command=self.selecionar_pasta_saida, style="Accent.TButton").grid(row=4, column=2, padx=5, pady=5)

        ttk.Label(frame_principal, text="Tolerância de Reconhecimento (0.4-0.6):").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(frame_principal, textvariable=self.tolerancia, width=10).grid(row=5, column=1, padx=5, pady=5, sticky="w")

        ttk.Checkbutton(frame_principal, text=" Multi-Processing (Usar se o computador tiver mais de 2 núcleos)", variable=self.modo_multi).grid(row=6, column=0, columnspan=3, pady=5, padx=2, sticky="w")

        texto_frame = ttk.Frame(frame_principal)
        texto_frame.grid(row=7, column=0, columnspan=3, padx=5, pady=10, sticky="nsew")

        self.log_texto = tk.Text(texto_frame, height=15, width=97, font=("Helvetica", 10))
        self.log_texto.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(texto_frame, orient="vertical", command=self.log_texto.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_texto.configure(yscrollcommand=scrollbar.set)

        self.progresso = ttk.Progressbar(frame_principal, length=650, mode='determinate')
        self.progresso.grid(row=8, column=0, columnspan=3, padx=5, pady=5)

        self.label_progresso = ttk.Label(frame_principal, text="Progresso: 0% | Tempo estimado: --")
        self.label_progresso.grid(row=9, column=0, columnspan=3, pady=8)

        frame_botoes = ttk.Frame(frame_principal, style="Transparent.TFrame")
        frame_botoes.grid(row=10, column=0, columnspan=3, pady=10)

        self.botao_iniciar = ttk.Button(frame_botoes, text="Iniciar Processamento", command=self.iniciar_processamento, style="Accent.TButton", width=25)
        self.botao_iniciar.grid(row=0, column=0, padx=5, pady=8)

        self.botao_cancelar = ttk.Button(frame_botoes, text="Cancelar", command=self.cancelar_processamento, style="Accent.TButton", width=25, state=tk.DISABLED)
        self.botao_cancelar.grid(row=0, column=1, padx=5, pady=8)

        ttk.Label(frame_principal, text="© 2025 - Desenvolvido por Alexandre Galhardo", font=("Helvetica", 8), foreground="#999").grid(row=11, column=0, columnspan=3, pady=10)

        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        self.root.protocol("WM_DELETE_WINDOW", self.fechar_janela)

    def fechar_janela(self):
        self.cancelar = True
        self.root.destroy()

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
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        self.log_texto.insert(tk.END, f"[{timestamp}] {mensagem}\n")
        self.log_texto.see(tk.END)
        if atualizar_imediatamente:
            self.root.update_idletasks()

    def atualizar_progresso(self, percentual, tempo_str):
        self.progresso.configure(value=percentual)
        self.label_progresso.config(text=f"Progresso: {percentual:.1f}% | Tempo estimado: {tempo_str}")

    def cancelar_processamento(self):
        self.cancelar = True
        self.log("Cancelamento solicitado...")

    @staticmethod
    def preprocessar_imagem(caminho):
        try:
            imagem = Image.open(caminho).convert('RGB')
            largura_max = 500
            if imagem.width > largura_max:
                proporcao = largura_max / imagem.width
                nova_altura = int(imagem.height * proporcao)
                imagem = imagem.resize((largura_max, nova_altura), Image.Resampling.LANCZOS)
            caminho_temp = caminho + "_temp.jpg"
            imagem.save(caminho_temp, quality=95)
            imagem_processada = face_recognition.load_image_file(caminho_temp)
            os.remove(caminho_temp)
            return imagem_processada, None
        except Exception as e:
            return face_recognition.load_image_file(caminho), f"Erro ao pré-processar {caminho}: {str(e)} - Tipo: {type(e).__name__}"

    @staticmethod
    def processar_uma_foto(args):
        foto, pasta_saida, identificacoes, tolerancia, cancelar = args
        if cancelar:
            return f"Cancelado: {foto}"

        pasta_nao_identificadas = os.path.join(pasta_saida, "Fotos Não Identificadas")
        pasta_corrompidas = os.path.join(pasta_saida, "Fotos Corrompidas")
        Path(pasta_corrompidas).mkdir(parents=True, exist_ok=True)
        Path(pasta_nao_identificadas).mkdir(parents=True, exist_ok=True)

        try:
            with Image.open(foto) as img:
                img.verify()
        except Exception as e:
            destino = os.path.join(pasta_corrompidas, os.path.basename(foto))
            try:
                shutil.move(foto, destino)
                return f"Arquivo corrompido: {foto} movido para Fotos Corrompidas"
            except Exception as move_error:
                return f"Erro ao mover arquivo corrompido {foto}: {str(move_error)}"

        try:
            imagem_desconhecida, erro = SeparadorFotos.preprocessar_imagem(foto)
            if erro:
                destino = os.path.join(pasta_nao_identificadas, os.path.basename(foto))
                shutil.copy(foto, destino)
                return erro

            codificacoes_desconhecidas = face_recognition.face_encodings(imagem_desconhecida, model="small", num_jitters=1)

            if len(codificacoes_desconhecidas) == 0:
                destino = os.path.join(pasta_nao_identificadas, os.path.basename(foto))
                shutil.copy(foto, destino)
                return f"Nenhum rosto encontrado em {foto}"

            identificados = []
            foto_copiada = False

            for j, codificacao_desconhecida in enumerate(codificacoes_desconhecidas):
                melhor_distancia = float('inf')
                melhor_aluno = None

                for nome_aluno, codificacoes_aluno in identificacoes.items():
                    distancias = face_recognition.face_distance(codificacoes_aluno, codificacao_desconhecida)
                    menor_distancia = min(distancias) if distancias.size > 0 else float('inf')
                    if menor_distancia < melhor_distancia:
                        melhor_distancia = menor_distancia
                        melhor_aluno = nome_aluno

                if melhor_distancia <= tolerancia:
                    pasta_aluno = os.path.join(pasta_saida, melhor_aluno)
                    Path(pasta_aluno).mkdir(parents=True, exist_ok=True)
                    destino = os.path.join(pasta_aluno, os.path.basename(foto))
                    try:
                        shutil.copy(foto, destino)
                        foto_copiada = True
                        identificados.append(f"Rosto {j+1} identificado como {melhor_aluno} (distância: {melhor_distancia:.2f})")
                    except Exception as e:
                        return f"Erro ao copiar {foto} para {destino}: {str(e)}"

            if not identificados:
                destino = os.path.join(pasta_nao_identificadas, os.path.basename(foto))
                shutil.copy(foto, destino)
                return f"Foto {foto} movida para Não Identificadas"

            return "; ".join(identificados)

        except Exception as e:
            destino = os.path.join(pasta_nao_identificadas, os.path.basename(foto))
            try:
                shutil.copy(foto, destino)
            except Exception as copy_error:
                return f"Erro ao processar e copiar {foto}: {str(e)}, erro na cópia: {str(copy_error)}"
            return f"Erro ao processar {foto}: {str(e)}"

    def carregar_identificacoes(self, pasta_identificacao):
        identificacoes = {}
        for arquivo in os.listdir(pasta_identificacao):
            if self.cancelar:
                break
            caminho = os.path.join(pasta_identificacao, arquivo)
            if not os.path.isfile(caminho) or not arquivo.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff')):
                continue
            try:
                Image.open(caminho).verify()
                imagem, erro = self.preprocessar_imagem(caminho)
                if erro:
                    self.log(erro)
                    continue
                codificacoes = face_recognition.face_encodings(imagem, model="large", num_jitters=5)
                if not codificacoes:
                    self.log(f"Nenhum rosto encontrado em {arquivo}")
                    continue
                nome_aluno = os.path.splitext(arquivo)[0]
                identificacoes[nome_aluno] = codificacoes
                self.log(f"Carregada identificação de {nome_aluno}")
            except Exception as e:
                self.log(f"Erro ao carregar {arquivo}: {str(e)}")
        return identificacoes

    def processar_fotos_single(self):
        pasta_fotos = self.pasta_fotos.get()
        pasta_identificacao = self.pasta_identificacao.get()
        pasta_saida = self.pasta_saida.get()
        tolerancia = self.tolerancia.get()

        if not (pasta_fotos and pasta_identificacao and pasta_saida):
            self.root.after(0, lambda: messagebox.showerror("Erro", "Por favor, selecione todas as pastas!"))
            return

        self.cancelar = False
        self.processamento_ativo = True
        self.root.after(0, lambda: self.botao_iniciar.config(state=tk.DISABLED))
        self.root.after(0, lambda: self.botao_cancelar.config(state=tk.NORMAL))
        Path(pasta_saida).mkdir(parents=True, exist_ok=True)
        Path(os.path.join(pasta_saida, "Fotos Não Identificadas")).mkdir(parents=True, exist_ok=True)

        self.log("Iniciando processamento (Single-Processing)...", atualizar_imediatamente=True)

        identificacoes = self.carregar_identificacoes(pasta_identificacao)
        fotos = [os.path.join(raiz, arquivo) for raiz, _, arquivos in os.walk(pasta_fotos) 
                 for arquivo in arquivos if arquivo.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff'))]
        total_fotos = len(fotos)
        self.log(f"Total de fotos a processar: {total_fotos}")
        fotos_processadas = 0
        tempo_inicio = time.time()

        for i, foto in enumerate(fotos):
            if self.cancelar:
                break
            resultado = self.processar_uma_foto((foto, pasta_saida, identificacoes, tolerancia, self.cancelar))
            self.log(resultado)

            fotos_processadas += 1
            percentual = (fotos_processadas / total_fotos) * 100
            tempo_decorrido = time.time() - tempo_inicio
            tempo_medio = tempo_decorrido / fotos_processadas if fotos_processadas > 0 else 0
            fotos_restantes = total_fotos - fotos_processadas
            tempo_estimado = tempo_medio * fotos_restantes
            minutos = int(tempo_estimado // 60)
            segundos = int(tempo_estimado % 60)
            tempo_str = f"{minutos}m {segundos}s"
            if fotos_processadas % 10 == 0 or i == total_fotos - 1:
                self.root.after(0, self.atualizar_progresso, percentual, tempo_str)
                self.root.update_idletasks()

        self.finalizar_processamento(total_fotos, fotos_processadas, tempo_inicio)

    @staticmethod
    def processar_lote(args):
        batch, pasta_saida, identificacoes, tolerancia, cancelar = args
        resultados = []
        for foto in batch:
            if cancelar:
                break
            resultados.append(SeparadorFotos.processar_uma_foto((foto, pasta_saida, identificacoes, tolerancia, cancelar)))
        return resultados

    def processar_fotos_multi(self):
        pasta_fotos = self.pasta_fotos.get()
        pasta_identificacao = self.pasta_identificacao.get()
        pasta_saida = self.pasta_saida.get()
        tolerancia = self.tolerancia.get()

        if not (pasta_fotos and pasta_identificacao and pasta_saida):
            self.root.after(0, lambda: messagebox.showerror("Erro", "Por favor, selecione todas as pastas!"))
            return

        self.cancelar = False
        self.processamento_ativo = True
        self.root.after(0, lambda: self.botao_iniciar.config(state=tk.DISABLED))
        self.root.after(0, lambda: self.botao_cancelar.config(state=tk.NORMAL))
        Path(pasta_saida).mkdir(parents=True, exist_ok=True)
        Path(os.path.join(pasta_saida, "Fotos Não Identificadas")).mkdir(parents=True, exist_ok=True)

        self.log("Iniciando processamento (Multi-Processing)...", atualizar_imediatamente=True)

        identificacoes = self.carregar_identificacoes(pasta_identificacao)
        fotos = [os.path.join(raiz, arquivo) for raiz, _, arquivos in os.walk(pasta_fotos) 
                 for arquivo in arquivos if arquivo.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff'))]
        total_fotos = len(fotos)
        self.log(f"Total de fotos a processar: {total_fotos}")

        num_processes = min(int(cpu_count() * 0.8), max(1, total_fotos // 10))
        tempo_inicio = time.time()
        fotos_processadas = 0
        batch_size = 10

        try:
            with Pool(processes=num_processes) as pool:
                self.log(f"Pool de processos iniciado com {num_processes} processos.", atualizar_imediatamente=True)
                batches = [fotos[i:i + batch_size] for i in range(0, len(fotos), batch_size)]
                args = [(batch, pasta_saida, identificacoes, tolerancia, self.cancelar) for batch in batches]
                resultados = pool.imap(self.processar_lote, args)

                for i, resultado_batch in enumerate(resultados):
                    if self.cancelar:
                        pool.terminate()
                        pool.close()
                        pool.join()
                        break
                    for resultado in resultado_batch:
                        self.log(resultado)
                        fotos_processadas += 1
                    percentual = (fotos_processadas / total_fotos) * 100
                    tempo_decorrido = time.time() - tempo_inicio
                    tempo_medio = tempo_decorrido / fotos_processadas if fotos_processadas > 0 else 0
                    fotos_restantes = total_fotos - fotos_processadas
                    tempo_estimado = tempo_medio * fotos_restantes
                    minutos = int(tempo_estimado // 60)
                    segundos = int(tempo_estimado % 60)
                    tempo_str = f"{minutos}m {segundos}s"
                    if fotos_processadas % 10 == 0 or i == len(batches) - 1:
                        self.root.after(0, self.atualizar_progresso, percentual, tempo_str)
                        self.root.update_idletasks()
        except Exception as e:
            self.log(f"Erro no Pool: {str(e)}", atualizar_imediatamente=True)

        self.finalizar_processamento(total_fotos, fotos_processadas, tempo_inicio)

    def finalizar_processamento(self, total_fotos, fotos_processadas, tempo_inicio):
        self.processamento_ativo = False
        if self.cancelar:
            self.log("Processamento cancelado.", atualizar_imediatamente=True)
            self.root.after(0, lambda: messagebox.showinfo("Cancelado", "O processamento foi interrompido."))
        else:
            tempo_total = time.time() - tempo_inicio
            minutos = int(tempo_total // 60)
            segundos = int(tempo_total % 60)
            self.log(f"Processamento concluído! Total de fotos processadas: {fotos_processadas}/{total_fotos}", atualizar_imediatamente=True)
            self.log(f"Tempo total: {minutos}m {segundos}s", atualizar_imediatamente=True)
            self.root.after(0, lambda: messagebox.showinfo("Concluído", "O processamento das fotos foi finalizado."))

        self.root.after(0, lambda: self.botao_iniciar.config(state=tk.NORMAL))
        self.root.after(0, lambda: self.botao_cancelar.config(state=tk.DISABLED))
        self.root.after(0, lambda: self.progresso.configure(value=0))
        self.root.after(0, lambda: self.label_progresso.config(text="Progresso: 0% | Tempo estimado: --"))

    def iniciar_processamento(self):
        if not self.processamento_ativo:
            try:
                thread = threading.Thread(target=self.processar_fotos_multi if self.modo_multi.get() else self.processar_fotos_single)
                thread.start()
            except Exception as e:
                self.log(f"Erro ao iniciar processamento: {str(e)}", atualizar_imediatamente=True)
                self.root.after(0, lambda: messagebox.showerror("Erro", f"Falha ao iniciar: {str(e)}"))

def janela_separador_fotos_multi(parent):
    root = tk.Toplevel(parent)  # Cria uma nova janela como filha do dashboard
    app = SeparadorFotos(root)
    return app

if __name__ == "__main__":
    root = tk.Tk()
    app = SeparadorFotos(root)
    root.mainloop()