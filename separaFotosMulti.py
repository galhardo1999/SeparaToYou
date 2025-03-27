import face_recognition
import os
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import threading
import queue
import time

class PhotoSeparator:
    def __init__(self, root):
        self.root = root
        self.root.title("Separador de Fotos - Alternativo")
        self.root.geometry("600x400")
        self.root.configure(bg="#e8ecef")

        # Variáveis
        self.photos_folder = tk.StringVar()
        self.identify_folder = tk.StringVar()
        self.output_folder = tk.StringVar()
        self.running = False
        self.tolerance = 0.55  # Tolerância fixa para simplificar
        self.task_queue = queue.Queue()
        self.processed_count = 0

        # Interface
        tk.Label(root, text="Separador de Fotos", font=("Arial", 16, "bold"), bg="#e8ecef").pack(pady=10)

        tk.Label(root, text="Pasta com Fotos:", bg="#e8ecef").pack()
        tk.Entry(root, textvariable=self.photos_folder, width=50).pack()
        tk.Button(root, text="Selecionar", command=self.select_photos_folder).pack(pady=5)

        tk.Label(root, text="Pasta de Identificação:", bg="#e8ecef").pack()
        tk.Entry(root, textvariable=self.identify_folder, width=50).pack()
        tk.Button(root, text="Selecionar", command=self.select_identify_folder).pack(pady=5)

        tk.Label(root, text="Pasta de Saída:", bg="#e8ecef").pack()
        tk.Entry(root, textvariable=self.output_folder, width=50).pack()
        tk.Button(root, text="Selecionar", command=self.select_output_folder).pack(pady=5)

        self.start_button = tk.Button(root, text="Iniciar", command=self.start_processing)
        self.start_button.pack(pady=10)

        self.cancel_button = tk.Button(root, text="Cancelar", command=self.cancel_processing, state=tk.DISABLED)
        self.cancel_button.pack(pady=5)

        self.status_label = tk.Label(root, text="Pronto", bg="#e8ecef")
        self.status_label.pack(pady=10)

        # Centralizar janela
        self.root.update_idletasks()
        width, height = self.root.winfo_width(), self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def select_photos_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.photos_folder.set(folder)

    def select_identify_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.identify_folder.set(folder)

    def select_output_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_folder.set(folder)

    def update_status(self, message):
        self.status_label.config(text=message)
        self.root.update_idletasks()

    def on_closing(self):
        self.running = False
        self.root.destroy()

    def load_identifications(self, folder):
        """Carrega as codificações faciais das imagens de identificação."""
        identifications = {}
        for file in os.listdir(folder):
            if not file.lower().endswith(('.jpg', '.jpeg', '.png')):
                continue
            path = os.path.join(folder, file)
            try:
                image = face_recognition.load_image_file(path)
                encodings = face_recognition.face_encodings(image, model="small")
                if encodings:
                    name = os.path.splitext(file)[0]
                    identifications[name] = encodings[0]  # Usa apenas a primeira codificação por simplicidade
                    self.update_status(f"Carregado: {name}")
                else:
                    self.update_status(f"Sem rosto em: {file}")
            except Exception as e:
                self.update_status(f"Erro em {file}: {str(e)}")
        return identifications

    def process_photo(self, photo_path, output_folder, identifications):
        """Processa uma única foto e a move para a pasta apropriada."""
        try:
            with Image.open(photo_path) as img:
                img.verify()  # Verifica se a imagem é válida
            image = face_recognition.load_image_file(photo_path)
            encodings = face_recognition.face_encodings(image, model="small")

            if not encodings:
                self.move_to_unidentified(photo_path, output_folder)
                return f"Nenhum rosto em {os.path.basename(photo_path)}"

            encoding = encodings[0]  # Usa o primeiro rosto detectado
            best_match = None
            best_distance = float('inf')

            for name, known_encoding in identifications.items():
                distance = face_recognition.face_distance([known_encoding], encoding)[0]
                if distance < best_distance:
                    best_distance = distance
                    best_match = name

            if best_distance <= self.tolerance:
                self.move_to_person_folder(photo_path, output_folder, best_match)
                return f"Identificado {best_match} em {os.path.basename(photo_path)} (distância: {best_distance:.2f})"
            else:
                self.move_to_unidentified(photo_path, output_folder)
                return f"Não identificado: {os.path.basename(photo_path)}"
        except Exception as e:
            self.move_to_corrupted(photo_path, output_folder)
            return f"Foto corrompida: {os.path.basename(photo_path)} - {str(e)}"

    def move_to_person_folder(self, photo_path, output_folder, person_name):
        """Move a foto para a pasta da pessoa identificada."""
        person_dir = os.path.join(output_folder, person_name)
        Path(person_dir).mkdir(parents=True, exist_ok=True)
        shutil.copy(photo_path, os.path.join(person_dir, os.path.basename(photo_path)))

    def move_to_unidentified(self, photo_path, output_folder):
        """Move a foto para a pasta de não identificados."""
        unidentified_dir = os.path.join(output_folder, "Não Identificados")
        Path(unidentified_dir).mkdir(parents=True, exist_ok=True)
        shutil.copy(photo_path, os.path.join(unidentified_dir, os.path.basename(photo_path)))

    def move_to_corrupted(self, photo_path, output_folder):
        """Move a foto para a pasta de corrompidos."""
        corrupted_dir = os.path.join(output_folder, "Corrompidos")
        Path(corrupted_dir).mkdir(parents=True, exist_ok=True)
        shutil.copy(photo_path, os.path.join(corrupted_dir, os.path.basename(photo_path)))

    def process_photos(self):
        """Processa todas as fotos em uma thread separada usando uma fila de tarefas."""
        photos_folder = self.photos_folder.get()
        identify_folder = self.identify_folder.get()
        output_folder = self.output_folder.get()

        if not (photos_folder and identify_folder and output_folder):
            messagebox.showerror("Erro", "Selecione todas as pastas!")
            return

        self.running = True
        self.start_button.config(state=tk.DISABLED)
        self.cancel_button.config(state=tk.NORMAL)

        # Carrega identificações
        self.update_status("Carregando identificações...")
        identifications = self.load_identifications(identify_folder)
        if not identifications:
            messagebox.showerror("Erro", "Nenhuma identificação válida encontrada!")
            self.reset_ui()
            return

        # Coleta todas as fotos
        photos = [os.path.join(root, file) for root, _, files in os.walk(photos_folder)
                  for file in files if file.lower().endswith(('.jpg', '.jpeg', '.png'))]
        total_photos = len(photos)
        self.processed_count = 0

        if total_photos == 0:
            messagebox.showinfo("Aviso", "Nenhuma foto encontrada!")
            self.reset_ui()
            return

        # Adiciona tarefas à fila
        for photo in photos:
            self.task_queue.put((photo, output_folder, identifications))

        start_time = time.time()
        self.update_status(f"Processando 0/{total_photos} fotos...")

        def worker():
            while self.running and not self.task_queue.empty():
                try:
                    photo, out_folder, ids = self.task_queue.get(timeout=1)
                    result = self.process_photo(photo, out_folder, ids)
                    self.processed_count += 1
                    elapsed = time.time() - start_time
                    avg_time = elapsed / self.processed_count if self.processed_count > 0 else 0
                    remaining = (total_photos - self.processed_count) * avg_time
                    self.update_status(
                        f"Processando {self.processed_count}/{total_photos} - {result} - Restante: {int(remaining)}s"
                    )
                except queue.Empty:
                    break
                finally:
                    self.task_queue.task_done()

            if self.running:
                total_time = time.time() - start_time
                self.update_status(f"Concluído! Processadas {self.processed_count}/{total_photos} fotos em {int(total_time)}s")
                messagebox.showinfo("Sucesso", "Processamento concluído!")
            else:
                self.update_status("Processamento cancelado.")
                messagebox.showinfo("Cancelado", "Processamento foi interrompido.")
            self.reset_ui()

        # Inicia o processamento em uma thread
        threading.Thread(target=worker, daemon=True).start()

    def start_processing(self):
        if not self.running:
            threading.Thread(target=self.process_photos, daemon=True).start()

    def cancel_processing(self):
        self.running = False
        self.cancel_button.config(state=tk.DISABLED)

    def reset_ui(self):
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.cancel_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoSeparator(root)
    root.mainloop()