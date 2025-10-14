import pyautogui 
import webbrowser
from time import sleep
import json
import cv2
import pytesseract as tct
import subprocess
import os

class DetectorMovimentoFacialAvancado:
    def __init__(self):
        # Carrega o classificador Haar Cascade para detectar rostos
        # Esse arquivo faz parte do OpenCV e é um modelo pré-treinado
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Variáveis de controle
        self.face_anterior = None
        self.movimentos = []
        self.comandos_ativos = True
        self.contador_movimentos = 0
        self.ultimo_comando = ""
        
        # Configurações do PyAutoGUI (segurança e tempo entre ações)
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1

    # ------------------------------------------------------------
    # Calcula diferença entre a posição do rosto atual e anterior
    # ------------------------------------------------------------
    def calcular_movimentos(self, face_atual, face_anterior):
        if face_anterior is None:
            return 0, 0, 0
        
        x_ant, y_ant, w_ant, h_ant = face_anterior
        x_atual, y_atual, w_atual, h_atual = face_atual

        dx = x_atual - x_ant
        dy = y_atual - y_ant
        dz = w_atual - w_ant  # diferença de tamanho (zoom)

        return dx, dy, dz

    # ------------------------------------------------------------
    # Executa ações no PC com base no movimento facial
    # ------------------------------------------------------------
    def executar_comando(self, movimento):
        movimento = movimento.strip()
        self.ultimo_comando = movimento
        self.contador_movimentos += 1
        print(f"Comando executado: {movimento}")
        
        # Movimentos simples
        if movimento == "Direita":
            pyautogui.moveRel(50, 0, duration=0.1)
        elif movimento == "Esquerda":
            pyautogui.moveRel(-50, 0, duration=0.1)
        elif movimento == "Cima":
            pyautogui.moveRel(0, -50, duration=0.1)
        elif movimento == "Baixo":
            pyautogui.moveRel(0, 50, duration=0.1)
        elif movimento == "Frente":
            pyautogui.doubleClick()
        elif movimento == "Trás":
            pyautogui.rightClick()

        # Combinações de movimentos (atalhos)
        if self.contador_movimentos >= 3:
            ultimos = self.movimentos[-3:]
            if ultimos == ["Cima", "Cima", "Cima"]:
                self.abrir_navegador()
            elif ultimos == ["Baixo", "Baixo", "Baixo"]:
                self.fechar_janela()
            elif ultimos == ["Esquerda", "Direita", "Esquerda"]:
                self.alt_tab()

    # ------------------------------------------------------------
    # Funções de comando especiais
    # ------------------------------------------------------------
    def abrir_navegador(self):
        print("Abrindo navegador...")
        webbrowser.open("https://www.google.com")
        self.contador_movimentos = 0

    def fechar_janela(self):
        print("Fechando janela...")
        pyautogui.hotkey('alt', 'f4')
        self.contador_movimentos = 0

    def alt_tab(self):
        print("Alternando janelas...")
        pyautogui.hotkey('alt', 'tab')
        self.contador_movimentos = 0

    # ------------------------------------------------------------
    # Salva os movimentos em um arquivo JSON
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

    # ------------------------------------------------------------
    # Função principal - captura da câmera e detecção de movimentos
    # ------------------------------------------------------------
    def detectar_movimentos(self):
        cap = cv2.VideoCapture(0)

        # Define resolução da câmera (melhora detecção)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Verifica se o classificador foi carregado corretamente
        if self.face_cascade.empty():
            print("ERRO: Não foi possível carregar o classificador Haar Cascade.")
            return

        print("=== SISTEMA DE CONTROLE FACIAL ATIVADO ===")
        print("Movimentos: Esquerda | Direita | Cima | Baixo | Frente | Trás")
        print("Comandos especiais:")
        print("- 3x 'Cima': Abrir navegador")
        print("- 3x 'Baixo': Fechar janela")
        print("- 'Esquerda, Direita, Esquerda': Alternar janelas")
        print("Teclas:")
        print("q - sair | s - salvar | c - ativar/desativar comandos | r - resetar contador")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Erro ao capturar frame. Verifique a câmera.")
                break
            
            # Converte para escala de cinza (melhor desempenho)
            cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detecta rostos (ajustes otimizados para precisão)
            faces = self.face_cascade.detectMultiScale(
                cinza,
                scaleFactor=1.1,     # sensibilidade do detector
                minNeighbors=4,      # reduz falsos positivos
                minSize=(80, 80)     # ignora rostos muito pequenos
            )
        
            if len(faces) > 0:
                # Pega o primeiro rosto detectado
                x, y, w, h = faces[0]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                  
                # Se havia um rosto anterior, calcula movimento
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
                        if len(self.movimentos) > 10:
                            self.movimentos.pop(0)

                        # Executa o comando se estiver ativo
                        if self.comandos_ativos:
                            self.executar_comando(movimento_limpo)

                        # Exibe o movimento detectado
                        cv2.putText(frame, f"Movimento: {movimento_limpo}", (10, 30),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, cor, 2)

                        # Desenha setas visuais indicando a direção
                        centro_x, centro_y = x + w//2, y + h//2
                        arrow_color = (0, 255, 255) if self.comandos_ativos else (100, 100, 100)
                        
                        if "Esquerda" in movimento:
                            cv2.arrowedLine(frame, (centro_x, centro_y), (centro_x - 50, centro_y), arrow_color, 3)
                        if "Direita" in movimento:
                            cv2.arrowedLine(frame, (centro_x, centro_y), (centro_x + 50, centro_y), arrow_color, 3)
                        if "Cima" in movimento:
                            cv2.arrowedLine(frame, (centro_x, centro_y), (centro_x, centro_y - 50), arrow_color, 3)
                        if "Baixo" in movimento:
                            cv2.arrowedLine(frame, (centro_x, centro_y), (centro_x, centro_y + 50), arrow_color, 3)  
                
                # Atualiza o rosto anterior
                self.face_anterior = faces[0]
            else:
                self.face_anterior = None
            
            # --------------------------------------------------------
            # Interface na tela com informações de status
            # --------------------------------------------------------
            y_pos = 60
            
            # Status dos comandos
            status = "ATIVO" if self.comandos_ativos else "INATIVO"
            cor_status = (0, 255, 0) if self.comandos_ativos else (0, 0, 255)
            cv2.putText(frame, f"Comandos: {status}", (10, y_pos),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, cor_status, 2)
            y_pos += 30
            
            # Último comando
            if self.ultimo_comando:
                cv2.putText(frame, f"Ultimo: {self.ultimo_comando}", (10, y_pos),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
                y_pos += 25
            
            # Contador total
            cv2.putText(frame, f"Total movimentos: {self.contador_movimentos}", (10, y_pos),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            y_pos += 25
            
            # Últimos movimentos
            cv2.putText(frame, "Ultimos movimentos:", (10, y_pos),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            y_pos += 20
            
            for i, mov in enumerate(self.movimentos[-5:]):
                cv2.putText(frame, f"{i + 1}. {mov}", (10, y_pos),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
                y_pos += 15
            
            # Mostra o vídeo
            cv2.imshow('Controle Facial Avancado', frame)

            # Controles via teclado
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):   # sair
                break
            elif key == ord('s'): # salvar
                self.salvar_movimentos()
            elif key == ord('c'): # ativar/desativar comandos
                self.comandos_ativos = not self.comandos_ativos
                print(f"Comandos {'ativados' if self.comandos_ativos else 'desativados'}!")
            elif key == ord('r'): # resetar contador
                self.contador_movimentos = 0
                self.movimentos = []
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
