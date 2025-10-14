import webbrowser as web 
from time import sleep
import json
import cv2
import pyautogui as pd
import numpy as np
import time


class DetectorMovimentoFacialAvancado:
    def __init__(self):
        # Carrega o classificador Haar Cascade (modelo pré-treinado para rostos)
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        # Variáveis de controle
        self.face_anterior = None
        self.movimentos = []
        self.comandos_ativos = True
        self.contador_movimentos = 0
        self.ultimo_comando = ""
        
        # Controle para detecção de 5 segundos
        self.tempo_inicio_direita = None
        self.comando_executado = False

    # ------------------------------------------------------------
    # Calcula diferença entre posição do rosto atual e anterior
    # ------------------------------------------------------------
    def calcular_movimentos(self, face_atual, face_anterior):
        if face_anterior is None:
            return 0, 0, 0
        
        x_ant, y_ant, w_ant, h_ant = face_anterior
        x_atual, y_atual, w_atual, h_atual = face_atual

        dx = x_atual - x_ant  # movimento horizontal
        dy = y_atual - y_ant  # movimento vertical
        dz = w_atual - w_ant  # diferença de tamanho (zoom)

        return dx, dy, dz

    # ------------------------------------------------------------
    # Salva os movimentos detectados em um arquivo JSON
    # ------------------------------------------------------------
    def salvar_movimentos(self):
        dados = {
            "total_movimentos": self.contador_movimentos,
            "ultimos_movimentos": self.movimentos[-10:],
            "ultimo_comando": self.ultimo_comando
        }
        with open("movimentos_faciais.json", "w") as f:
            json.dump(dados, f, indent=4)
        print("Movimentos salvos em movimentos_faciais.json")

    # ---------------------------------------------------------------
    # Detecta se a cabeça está inclinada para direita por 5 segundos
    # ---------------------------------------------------------------
    def detectar_inclinacao_direita(self, movimento, dx):
        """
        Detecta se a cabeça está inclinada para direita por 5 segundos consecutivos
        e executa o comando do YouTube Shorts
        """
        if not self.comandos_ativos:
            self.tempo_inicio_direita = None
            return
            
        # Se detectou movimento para direita
        if "Direita" in movimento and dx > 10:
            # Inicia o temporizador se não estava contando
            if self.tempo_inicio_direita is None:
                self.tempo_inicio_direita = time.time()
                self.comando_executado = False
                print("Iniciando contagem para YouTube Shorts...")
            
            # Calcula quanto tempo já passou
            tempo_decorrido = time.time() - self.tempo_inicio_direita
            
            # Se passaram 5 segundos e o comando ainda não foi executado
            if tempo_decorrido >= 5 and not self.comando_executado:
                print("5 segundos detectados! Executando comando YouTube Shorts...")
                
                # Abre o YouTube Shorts
                web.open('https://www.youtube.com/shorts')
                sleep(3)  # Espera a página carregar
                
                # Faz o scroll
                pd.scroll(-100)
                print("YouTube Shorts aberto e scroll realizado!")
                
                # Marca que o comando foi executado
                self.comando_executado = True
                
            return tempo_decorrido
            
        else:
            # Reseta o temporizador se não está mais inclinado para direita
            self.tempo_inicio_direita = None
            self.comando_executado = False
            return 0

    # ------------------------------------------------------------
    # Função principal - captura da câmera e detecção de movimentos
    # ------------------------------------------------------------
    def detectar_movimentos(self):
        cap = cv2.VideoCapture(0)

        # Define resolução da câmera
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Verifica se o classificador foi carregado corretamente
        if self.face_cascade.empty():
            print("ERRO: Não foi possível carregar o classificador Haar Cascade.")
            return

        print("=== SISTEMA DE DETECÇÃO FACIAL ATIVADO ===")
        print("INCLINE A CABEÇA PARA DIREITA POR 5 SEGUNDOS PARA ABRIR YOUTUBE SHORTS")
        print("Teclas:")
        print("q - sair | s - salvar | c - ativar/desativar detecção | r - resetar contador")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Erro ao capturar frame. Verifique a câmera.")
                break
            
            # 🔄🔁🔄 INVERTE A CÂMERA AQUI 🔄🔁🔄
            frame = cv2.flip(frame, 1)  # 1 = espelhar horizontalmente
            
            # Converte para tons de cinza (aumenta a performance)
            cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detecta rostos (ajustes para melhorar precisão)
            faces = self.face_cascade.detectMultiScale(
                cinza,
                scaleFactor=1.1,     # sensibilidade
                minNeighbors=4,      # reduz falsos positivos
                minSize=(80, 80)     # ignora rostos muito pequenos
            )
        
            if len(faces) > 0:
                # Pega o primeiro rosto detectado
                x, y, w, h = faces[0]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                  
                # Se havia um rosto anterior, calcula o movimento
                if self.face_anterior is not None:
                    dx, dy, dz = self.calcular_movimentos(faces[0], self.face_anterior)
                    movimento = ""
                    cor = (0, 255, 0) if self.comandos_ativos else (100, 100, 100)

                    # Movimento horizontal
                    if abs(dx) > 5:
                        movimento += "Direita" if dx > 0 else "Esquerda"
                    
                    # Movimento vertical
                    if abs(dy) > 5:
                        movimento += " Baixo" if dy > 0 else " Cima"
                    
                    # Movimento de profundidade (zoom)
                    if abs(dz) > 3:
                        movimento += " Frente" if dz > 0 else " Trás"
                    
                    # Se algum movimento foi detectado
                    if movimento.strip():
                        movimento_limpo = movimento.strip()
                        self.movimentos.append(movimento_limpo)
                        self.contador_movimentos += 1
                        if len(self.movimentos) > 10:
                            self.movimentos.pop(0)

                        self.ultimo_comando = movimento_limpo

                        # Detecta inclinação prolongada para direita
                        tempo_decorrido = self.detectar_inclinacao_direita(movimento_limpo, dx)

                        # Mostra o movimento detectado na tela
                        cv2.putText(frame, f"Movimento: {movimento_limpo}", (10, 30),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, cor, 2)
                        
                        # Mostra contagem regressiva se estiver contando
                        if self.tempo_inicio_direita is not None and tempo_decorrido > 0:
                            tempo_restante = max(0, 5 - tempo_decorrido)
                            cv2.putText(frame, f"YouTube Shorts em: {tempo_restante:.1f}s", 
                                       (10, frame.shape[0] - 50), cv2.FONT_HERSHEY_SIMPLEX, 
                                       0.8, (0, 255, 255), 2)

                        # Desenha setas visuais indicando direção
                        centro_x, centro_y = x + w//2, y + h//2
                        arrow_color = (0, 255, 255) if self.comandos_ativos else (100, 100, 100)
                        
                        if "Esquerda" in movimento:
                            cv2.arrowedLine(frame, (centro_x, centro_y), (centro_x - 50, centro_y), arrow_color, 3)
                        if "Direita" in movimento:
                            cv2.arrowedLine(frame, (centro_x, centro_y), (centro_x + 50, centro_y), arrow_color, 3)
                            # Destaca a seta direita quando contando tempo
                            if self.tempo_inicio_direita is not None:
                                cv2.arrowedLine(frame, (centro_x, centro_y), (centro_x + 70, centro_y), (0, 0, 255), 5)
                        if "Cima" in movimento:
                            cv2.arrowedLine(frame, (centro_x, centro_y), (centro_x, centro_y - 50), arrow_color, 3)
                        if "Baixo" in movimento:
                            cv2.arrowedLine(frame, (centro_x, centro_y), (centro_x, centro_y + 50), arrow_color, 3)
                
                # Atualiza o rosto anterior
                self.face_anterior = faces[0]
            else:
                self.face_anterior = None
                self.tempo_inicio_direita = None
                self.comando_executado = False
            
            # --------------------------------------------------------
            # Exibição de status e informações na tela
            # --------------------------------------------------------
            y_pos = 60
            
            # Status dos comandos
            status = "ATIVO" if self.comandos_ativos else "INATIVO"
            cor_status = (0, 255, 0) if self.comandos_ativos else (0, 0, 255)
            cv2.putText(frame, f"Detecção: {status}", (10, y_pos),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, cor_status, 2)
            y_pos += 30
            
            # Último comando
            if self.ultimo_comando:
                cv2.putText(frame, f"Ultimo movimento: {self.ultimo_comando}", (10, y_pos),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
                y_pos += 25
            
            # Contador total
            cv2.putText(frame, f"Total de movimentos: {self.contador_movimentos}", (10, y_pos),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            y_pos += 25
            
            # Instrução principal
            cv2.putText(frame, "INCLINE DIREITA 5s -> YOUTUBE SHORTS", 
                       (frame.shape[1] - 350, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.6, (0, 255, 255), 2)
            
            # Mostra o vídeo com as marcações
            cv2.imshow('Detecção Facial - YouTube Shorts', frame)

            # Controles via teclado
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):   # sair
                break
            elif key == ord('s'): # salvar
                self.salvar_movimentos()
            elif key == ord('c'): # ativar/desativar detecção
                self.comandos_ativos = not self.comandos_ativos
                self.tempo_inicio_direita = None
                print(f"Detecção {'ativada' if self.comandos_ativos else 'desativada'}!")
            elif key == ord('r'): # resetar contador
                self.contador_movimentos = 0
                self.movimentos = []
                self.tempo_inicio_direita = None
                self.comando_executado = False
                print("Contadores resetados!")
                
        # Libera recursos
        cap.release()
        cv2.destroyAllWindows()
        print("Sistema finalizado.")


# ------------------------------------------------------------
# Execução principal
# ------------------------------------------------------------
if __name__ == "__main__":
    detector = DetectorMovimentoFacialAvancado()
    detector.detectar_movimentos()