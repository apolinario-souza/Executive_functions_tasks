#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 10 12:20:02 2025

@author: tercio
"""

import cv2
import tkinter as tk
from constants import CAMERA,WIDTH, HEIGHT




def visualizar_camera_tela_cheia(camera_index=CAMERA):
    cap = cv2.VideoCapture(camera_index)
    
    if not cap.isOpened():
        print("Erro: Não foi possível abrir a câmera.")
        return
    
    # Configura a janela para tela cheia (funciona em sistemas Windows/Linux)
    cv2.namedWindow("Câmera (Tela Cheia)", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Câmera (Tela Cheia)", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    
    print("Pressione ESC para sair do modo tela cheia...")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erro ao capturar o frame.")
            break
        
        # Redimensiona o frame para ocupar toda a tela (opcional)
        altura_tela = HEIGHT   # Altere conforme sua resolução
        largura_tela = WIDTH  # Altere conforme sua resolução
        frame_redimensionado = cv2.resize(frame, (largura_tela, altura_tela))
        
        cv2.imshow("Câmera (Tela Cheia)", frame_redimensionado)
        
        if cv2.waitKey(1) == 27:  # ESC para sair
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("Visualização encerrada.")

# Use a constante CAMERA do seu código original ou 0 para câmera padrão
visualizar_camera_tela_cheia(CAMERA)  # Ou substitua CAMERA por 0 se necessário