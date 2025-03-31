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
from deepface import DeepFace
import cv2
import numpy as np

class SeparadorFotos:
    def __init__(self, root):
        self.root = root
        self.root.title("Separador de Fotos por Reconhecimento Facial - DeepFace")
        self.root.geometry("740x700")
        self.root.configure(bg="#f5f6f5")

        self.pasta_fotos = tk.StringVar()
        self.pasta_identificacao = tk.StringVar()
        self.pasta_saida = tk.StringVar()
        self.cancelar = False
        self.processamento_ativo = False
        self.modo_multi = tk.BooleanVar(value=True)
        self.tolerancia = tk.DoubleVar(value=0.6)  # Tolerância ajustada para 0.6
        self.modelo = tk.StringVar(value="Facenet")

        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 11), padding=10)
        style.configure("TLabel", background="#f5f6f5", font=("Helvetica", 11))
        style.configure("Accent.TButton", background="#ADD8E6", foreground="black", font=("Helvetica", 11), padding=(10, 2))
        style.configure("Transparent.TFrame", background="#f5f6f5")
        style.configure("TProgressbar", thickness=20)

        frame_principal = ttk.Frame(self.root, padding="20", style="Transparent.TFrame")
        frame_principal.grid(row=0, column=0, sticky="nsew")

        ttk.Label(frame_principal, text="Separador de Fotos", font=("Helvetica", 20, "bold"), foreground="#0288D1").grid(row=0, column=0, columnspan=3, pady=(0, 2))
        ttk.Label(frame_principal, text="Version Alpha 1.0.4 - DeepFace Edition", font=("Helvetica", 10, "italic"), foreground="#666").grid(row=1, column=0, columnspan=3, pady=(0, 8))

        ttk.Label(frame_principal, text="Pasta com Todas as Fotos:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(frame_principal, textvariable=self.pasta_fotos, width=50).grid(row=2, column=1, padx=5, pady=3)
        ttk.Button(frame_principal, text="Selecionar", command=self.selecionar_pasta_fotos, style="Accent.TButton").grid(row=2, column=2, padx=5, pady=5)

        ttk.Label(frame_principal, text="Pasta de Identificação dos Alunos:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(frame_principal, textvariable=self.pasta_identificacao, width=50).grid(row=3, column=1, padx=5, pady=3)
        ttk.Button(frame_principal, text="Selecionar", command=self.selecionar_pasta_identificacao, style="Accent.TButton").grid(row=3, column=2, padx=5, pady=5)

        ttk.Label(frame_principal, text="Pasta de Saída:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(frame_principal, textvariable=self.pasta_saida, width=50).grid(row=4, column=1, padx=5, pady=3)
        ttk.Button(frame_principal, text="Selecionar", command=self.selecionar_pasta_saida, style="Accent.TButton").grid(row=4, column=2, padx=5, pady=5)

        ttk.Label(frame_principal, text="Tolerância de Reconhecimento (0.4-1.0):").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(frame_principal, textvariable=self.tolerancia, width=10).grid(row=5, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(frame_principal, text="Modelo de Reconhecimento:").grid(row=6, column=0, padx=5, pady=5, sticky="w")
        ttk.Combobox(frame_principal, textvariable=self.modelo, values=["Facenet", "VGG-Face", "ArcFace"], state="readonly").grid(row=6, column=1, padx=5, pady=5, sticky="w")

        ttk.Checkbutton(frame_principal, text=" Multi-Processing (Usar se o computador tiver mais de 2 núcleos)", variable=self.modo_multi).grid(row=7, column=0, columnspan=3, pady=5, padx=2, sticky="w")

        texto_frame = ttk.Frame(frame_principal)
        texto_frame.grid(row=8, column=0, columnspan=3, padx=5, pady=10, sticky="nsew")

        self.log_texto = tk.Text(texto_frame, height=15, width=97, font=("Helvetica", 10))
        self.log_texto.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(texto_frame, orient="vertical", command=self.log_texto.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_texto.configure(yscrollcommand=scrollbar.set)

        self.progresso = ttk.Progressbar(frame_principal, length=650, mode='determinate')
        self.progresso.grid(row=9, column=0, columnspan=3, padx=5, pady=5)

        self.label_progresso = ttk.Label(frame_principal, text="Progresso: 0% | Tempo estimado: --")
        self.label_progresso.grid(row=10, column=0, columnspan=3, pady=8)

        frame_botoes = ttk.Frame(frame_principal, style="Transparent.TFrame")
        frame_botoes.grid(row=11, column=0, columnspan=3, pady=10)

        self.botao_iniciar = ttk.Button(frame_botoes, text="Iniciar Processamento", command=self.iniciar_processamento, style="Accent.TButton", width=25)
        self.botao_iniciar.grid(row=0, column=0, padx=5, pady=8)

        self.botao_cancelar = ttk.Button(frame_botoes, text="Cancelar", command=self.cancelar_processamento, style="Accent.TButton", width=25, state=tk.DISABLED)
        self.botao_cancelar.grid(row=0, column=1, padx=5, pady=8)

        ttk.Label(frame_principal, text="© 2025 - Desenvolvido por Alexandre Galhardo", font=("Helvetica", 8), foreground="#999").grid(row=12, column=0, columnspan=3, pady=10)

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
            imagem_cv = cv2.cvtColor(np.array(imagem), cv2.COLOR_RGB2BGR)
            return imagem_cv, None
        except Exception as e:
            return None, f"Erro ao pré-processar {caminho}: {str(e)}"

    def processar_uma_foto(self, args):
        foto, pasta_saida, identificacoes, tolerancia, modelo, cancelar = args
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

        imagem_desconhecida, erro = SeparadorFotos.preprocessar_imagem(foto)
        if erro:
            destino = os.path.join(pasta_nao_identificadas, os.path.basename(foto))
            shutil.copy(foto, destino)
            return erro

        try:
            rostos = DeepFace.extract_faces(imagem_desconhecida, detector_backend='opencv', enforce_detection=False)
            if not rostos or len(rostos) == 0:
                destino = os.path.join(pasta_nao_identificadas, os.path.basename(foto))
                shutil.copy(foto, destino)
                return f"Nenhum rosto encontrado em {foto}"

            identificados = []
            foto_copiada = False

            for i, rosto in enumerate(rostos):
                rosto_img = rosto["face"]
                melhor_distancia = float('inf')
                melhor_aluno = None
                distancias = []

                for nome_aluno, caminho_referencia in identificacoes.items():
                    try:
                        ref_img = cv2.imread(caminho_referencia)
                        if ref_img is None:
                            try:
                                ref_img_pil = Image.open(caminho_referencia).convert('RGB')
                                ref_img = cv2.cvtColor(np.array(ref_img_pil), cv2.COLOR_RGB2BGR)
                            except Exception as e:
                                print(f"[DEBUG] Imagem de referência {caminho_referencia} inválida, pulando... {str(e)}")
                                continue

                        resultado = DeepFace.verify(
                            rosto_img,
                            ref_img,
                            model_name=modelo,
                            distance_metric="euclidean_l2",
                            enforce_detection=False
                        )
                        distancia = resultado["distance"]
                        distancias.append(f"{nome_aluno}: {distancia:.2f}")
                        if distancia < melhor_distancia:
                            melhor_distancia = distancia
                            melhor_aluno = nome_aluno

                    except Exception as e:
                        return f"Erro ao comparar {foto} com {nome_aluno} ({caminho_referencia}): {str(e)}"

                # Log das distâncias para depuração
                self.log(f"Foto {os.path.basename(foto)}, Rosto {i+1} - Distancias: {', '.join(distancias)}")

                if melhor_aluno and melhor_distancia <= tolerancia:
                    pasta_aluno = os.path.join(pasta_saida, melhor_aluno)
                    Path(pasta_aluno).mkdir(parents=True, exist_ok=True)
                    destino = os.path.join(pasta_aluno, os.path.basename(foto))
                    shutil.copy(foto, destino)
                    rosto_path = os.path.join(pasta_aluno, f"rosto_{i+1}_{os.path.basename(foto)}")
                    cv2.imwrite(rosto_path, cv2.cvtColor((rosto_img * 255).astype(np.uint8), cv2.COLOR_RGB2BGR))
                    identificados.append(f"Rosto {i+1} identificado como {melhor_aluno} (distância: {melhor_distancia:.2f})")
                    foto_copiada = True
                else:
                    self.log(f"Rosto {i+1} não identificado (melhor distância: {melhor_distancia:.2f}, tolerância: {tolerancia})")

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
        self.log(f"Verificando pasta de identificação: {pasta_identificacao}")
        if not os.path.exists(pasta_identificacao):
            self.log(f"Erro: A pasta {pasta_identificacao} não existe.")
            self.root.after(0, lambda: messagebox.showerror("Erro", f"A pasta de identificação {pasta_identificacao} não existe."))
            return {}

        cache_file = os.path.join(pasta_identificacao, "identificacoes_cache.pkl")
        if os.path.exists(cache_file) and os.path.getsize(cache_file) > 0:
            try:
                with open(cache_file, 'rb') as f:
                    identificacoes = pickle.load(f)
                self.log("Identificações carregadas do cache.")
                return identificacoes
            except Exception as e:
                self.log(f"Erro ao carregar cache: {str(e)}. Recalculando identificações...")

        identificacoes = {}
        invalidas = []
        arquivos_encontrados = os.listdir(pasta_identificacao)
        self.log(f"Arquivos encontrados na pasta: {', '.join(arquivos_encontrados) if arquivos_encontrados else 'Nenhum arquivo encontrado'}")

        for arquivo in arquivos_encontrados:
            if self.cancelar:
                break
            caminho = os.path.join(pasta_identificacao, arquivo)
            self.log(f"Processando arquivo: {arquivo} (caminho: {caminho})")
            if not os.path.isfile(caminho):
                self.log(f"Ignorando {arquivo}: não é um arquivo")
                continue
            if not arquivo.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff')):
                self.log(f"Ignorando {arquivo}: não é uma imagem válida")
                continue
            if not os.path.exists(caminho):
                self.log(f"Erro: Arquivo {arquivo} não existe no caminho {caminho}")
                invalidas.append(arquivo)
                continue
            try:
                with Image.open(caminho) as img:
                    img.verify()
                ref_img = cv2.imread(caminho)
                if ref_img is None:
                    self.log(f"OpenCV não conseguiu ler {arquivo}, tentando com PIL...")
                    try:
                        ref_img_pil = Image.open(caminho).convert('RGB')
                        ref_img = cv2.cvtColor(np.array(ref_img_pil), cv2.COLOR_RGB2BGR)
                        self.log(f"Carregada {arquivo} usando PIL como fallback")
                    except Exception as e:
                        self.log(f"Erro: Não foi possível ler {arquivo} com OpenCV ou PIL: {str(e)}")
                        invalidas.append(arquivo)
                        continue
                nome_aluno = os.path.splitext(arquivo)[0]
                identificacoes[nome_aluno] = caminho
                self.log(f"Carregada identificação de {nome_aluno} ({caminho})")
            except Exception as e:
                self.log(f"Erro ao carregar {arquivo}: {str(e)}")
                invalidas.append(arquivo)

        if invalidas:
            self.log(f"Imagens inválidas: {', '.join(invalidas)}")
            self.root.after(0, lambda: messagebox.showwarning("Atenção", f"Imagens inválidas detectadas: {', '.join(invalidas)}. Elas serão ignoradas."))

        if not identificacoes:
            self.log("Nenhuma imagem de referência válida encontrada. O processamento não pode continuar.")
            self.root.after(0, lambda: messagebox.showerror("Erro", "Nenhuma imagem de referência válida foi encontrada. Verifique a pasta de identificação e os arquivos."))
            return {}

        try:
            with open(cache_file, 'wb') as f:
                pickle.dump(identificacoes, f)
            self.log("Identificações salvas no cache.")
        except Exception as e:
            self.log(f"Erro ao salvar cache: {str(e)}")
        return identificacoes

    def processar_fotos_single(self):
        pasta_fotos = self.pasta_fotos.get()
        pasta_identificacao = self.pasta_identificacao.get()
        pasta_saida = self.pasta_saida.get()
        tolerancia = self.tolerancia.get()
        modelo = self.modelo.get()

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
        if not identificacoes:
            self.finalizar_processamento(0, 0, time.time())
            return

        fotos = [os.path.join(raiz, arquivo) for raiz, _, arquivos in os.walk(pasta_fotos) 
                 for arquivo in arquivos if arquivo.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff'))]
        total_fotos = len(fotos)
        self.log(f"Total de fotos a processar: {total_fotos}")
        fotos_processadas = 0
        tempo_inicio = time.time()

        for i, foto in enumerate(fotos):
            if self.cancelar:
                break
            resultado = self.processar_uma_foto((foto, pasta_saida, identificacoes, tolerancia, modelo, self.cancelar))
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
        batch, pasta_saida, identificacoes, tolerancia, modelo, cancelar = args
        resultados = []
        for foto in batch:
            if cancelar:
                break
            resultados.append(SeparadorFotos.processar_uma_foto((foto, pasta_saida, identificacoes, tolerancia, modelo, cancelar)))
        return resultados

    def processar_fotos_multi(self):
        pasta_fotos = self.pasta_fotos.get()
        pasta_identificacao = self.pasta_identificacao.get()
        pasta_saida = self.pasta_saida.get()
        tolerancia = self.tolerancia.get()
        modelo = self.modelo.get()

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
        if not identificacoes:
            self.finalizar_processamento(0, 0, time.time())
            return

        fotos = [os.path.join(raiz, arquivo) for raiz, _, arquivos in os.walk(pasta_fotos) 
                 for arquivo in arquivos if arquivo.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff'))]
        total_fotos = len(fotos)
        self.log(f"Total de fotos a processar: {total_fotos}")

        num_processes = max(1, cpu_count())
        tempo_inicio = time.time()
        fotos_processadas = 0
        batch_size = 10

        try:
            with Pool(processes=num_processes) as pool:
                self.log(f"Pool de processos iniciado com {num_processes} processos.", atualizar_imediatamente=True)
                batches = [fotos[i:i + batch_size] for i in range(0, len(fotos), batch_size)]
                args = [(batch, pasta_saida, identificacoes, tolerancia, modelo, self.cancelar) for batch in batches]
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
        tempo_total = time.time() - tempo_inicio
        minutos = int(tempo_total // 60)
        segundos = int(tempo_total % 60)

        pasta_saida = self.pasta_saida.get()
        relatorio = {"Não Identificadas": 0, "Corrompidas": 0}
        for pasta in os.listdir(pasta_saida):
            caminho = os.path.join(pasta_saida, pasta)
            if os.path.isdir(caminho):
                count = len([f for f in os.listdir(caminho) if os.path.isfile(os.path.join(caminho, f)) and not f.startswith("rosto_")])
                relatorio[pasta] = count

        with open(os.path.join(pasta_saida, "relatorio.txt"), "w") as f:
            f.write(f"Relatório de Processamento - {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total de fotos processadas: {fotos_processadas}/{total_fotos}\n")
            f.write(f"Tempo total: {minutos}m {segundos}s\n")
            f.write("Distribuição das fotos:\n")
            for chave, valor in relatorio.items():
                f.write(f"{chave}: {valor} fotos\n")

        if self.cancelar:
            self.log("Processamento cancelado.", atualizar_imediatamente=True)
            self.root.after(0, lambda: messagebox.showinfo("Cancelado", "O processamento foi interrompido."))
        else:
            self.log(f"Processamento concluído! Total de fotos processadas: {fotos_processadas}/{total_fotos}", atualizar_imediatamente=True)
            self.log(f"Tempo total: {minutos}m {segundos}s", atualizar_imediatamente=True)
            self.log("Relatório salvo em relatorio.txt", atualizar_imediatamente=True)
            self.root.after(0, lambda: messagebox.showinfo("Concluído", "O processamento das fotos foi finalizado. Veja o relatório em relatorio.txt"))

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
    root = tk.Toplevel(parent)
    app = SeparadorFotos(root)
    return app

if __name__ == "__main__":
    root = tk.Tk()
    app = SeparadorFotos(root)
    root.mainloop()