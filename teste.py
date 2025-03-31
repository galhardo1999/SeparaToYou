import os
import cv2
from PIL import Image
import numpy as np

pasta_identificacao = r"C:\Users\Apolo\Desktop\CRESCER\1 - IDENTIFICACAO\PLAQUINHAS"

print(f"Verificando pasta: {pasta_identificacao}")
if not os.path.exists(pasta_identificacao):
    print("Pasta não existe!")
else:
    arquivos = os.listdir(pasta_identificacao)
    print(f"Arquivos encontrados: {arquivos}")

    for arquivo in arquivos:
        caminho = os.path.join(pasta_identificacao, arquivo)
        print(f"\nTestando {arquivo} ({caminho}):")
        if not os.path.isfile(caminho):
            print("Não é um arquivo")
            continue
        if not arquivo.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff')):
            print("Não é uma imagem válida")
            continue

        # Teste com PIL
        try:
            with Image.open(caminho) as img:
                img.verify()
            print("PIL: Imagem válida")
        except Exception as e:
            print(f"PIL: Erro ao carregar - {str(e)}")

        # Teste com Open