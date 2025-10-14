import webbrowser as web 
from time import sleep
import json
import cv2
import pyautogui as pd
import numpy as np
import time
import mediapipe as mp


class DetectorGestosMaosAvancado:
    def __init__(self):
        # Inicializa MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,  # Detecta apenas uma mão
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        # Variáveis de controle
        self.movimentos = []
        self.comandos_ativos = True
        self.contador_movimentos = 0
        self.ultimo_comando = ""
        
        # Controle para scroll automático
        self.scroll_ativo = False
        self.em_scroll = False
        
        # Posição anterior da mão para calcular movimento
        self.mao_anterior = None

    # ------------------------------------------------------------
    # NOVA FUNÇÃO: Move o mouse para o centro da tela
    # ------------------------------------------------------------
    def mover_mouse_centro(self):
        """
        Move o mouse para o centro da tela
        """
        # Obtém o tamanho da tela
        screen_width, screen_height = pd.size()
        
        # Calcula o centro
        centro_x = screen_width // 2
        centro_y = screen_height // 2
        
        # Move o mouse para o centro
        pd.moveTo(centro_x, centro_y, duration=0.5)
        print(f"🖱️ Mouse movido para o centro: ({centro_x}, {centro_y})")
        
        return centro_x, centro_y

    # ------------------------------------------------------------
    # Detecta gestos específicos da mão
    # ------------------------------------------------------------
    def detectar_gesto(self, landmarks):
        """
        Detecta gestos específicos: 
        - Apenas dedo indicador levantado
        - Mão fechada
        - Outros gestos
        """
        # Pontos dos dedos (ponta de cada dedo)
        pontas_dedos = [8, 12, 16, 20]  # indicador, médio, anelar, mindinho
        ponta_polegar = 4
        
        # Verifica se os dedos estão estendidos
        dedos_estendidos = []
        
        for ponta in pontas_dedos:
            # Se a ponta do dedo está acima da junta média
            if landmarks[ponta].y < landmarks[ponta-2].y:
                dedos_estendidos.append(True)
            else:
                dedos_estendidos.append(False)
        
        # Verifica polegar (lógica diferente)
        if landmarks[ponta_polegar].x < landmarks[ponta_polegar-1].x:
            dedos_estendidos.append(True)
        else:
            dedos_estendidos.append(False)
        
        # Conta quantos dedos estão estendidos
        dedos_contagem = sum(dedos_estendidos)
        
        # Detecta gestos específicos
        if dedos_contagem == 1 and dedos_estendidos[0]:  # Apenas indicador
            return "DEDO_INDICADOR"
        elif dedos_contagem == 0:  # Nenhum dedo = mão fechada
            return "MAO_FECHADA"
        else:
            return "OUTRO_GESTO"

    # ------------------------------------------------------------
    # Executa scroll automático
    # ------------------------------------------------------------
    def executar_scroll_automatico(self):
        """
        Executa scroll automático até detectar mão fechada
        """
        print("🎬 Iniciando scroll automático no YouTube Shorts...")
        
        # 🆕 Move o mouse para o centro antes de começar o scroll
        self.mover_mouse_centro()
        
        self.scroll_ativo = True
        scroll_count = 0
        max_scrolls = 50  # Limite de segurança
        
        while self.scroll_ativo and scroll_count < max_scrolls:
            pd.scroll(-100)
            scroll_count += 1
            print(f"📜 Scroll executado: {scroll_count}")
            sleep(10)
            
            # Pequena pausa entre scrolls
            time.sleep(0.8)
            
            # Verifica se deve parar (será controlado pela detecção de mão fechada)
            if not self.scroll_ativo:
                break
        
        print("🛑 Scroll automático finalizado")
        self.em_scroll = False

    # ------------------------------------------------------------
    # Controla ações baseado nos gestos
    # ------------------------------------------------------------
    def controlar_por_gestos(self, gesto, landmarks, frame):
        """
        Controla ações baseado nos gestos detectados
        """
        if not self.comandos_ativos:
            return
        
        # GESTO: APENAS DEDO INDICADOR - Abre YouTube e inicia scroll
        if gesto == "DEDO_INDICADOR" and not self.em_scroll:
            print("📗 Dedo indicador detectado! Abrindo YouTube Shorts...")
            
            # 🆕 Move o mouse para o centro antes de abrir o YouTube
            self.mover_mouse_centro()
            
            # Abre o YouTube Shorts
            web.open('https://www.youtube.com/shorts')
            sleep(2)
            
            # Inicia scroll automático
            self.em_scroll = True
            
            # Inicia thread de scroll em segundo plano
            import threading
            scroll_thread = threading.Thread(target=self.executar_scroll_automatico)
            scroll_thread.daemon = True
            scroll_thread.start()
            
            return "YouTube Aberto + Scroll"
        
        # GESTO: MAO FECHADA - Para tudo
        elif gesto == "MAO_FECHADA":
            if self.em_scroll or self.scroll_ativo:
                print("✊ Mão fechada detectada! Parando scroll...")
                self.scroll_ativo = False
                self.em_scroll = False
                
                # 🆕 Move o mouse para o centro ao parar o scroll
                self.mover_mouse_centro()
                
                pd.hotkey('ctrl', 'w')
                return "Scroll Parado"
            
            return "Mão Fechada"
        
        return ""

    # ------------------------------------------------------------
    # Salva os movimentos detectados em um arquivo JSON
    # ------------------------------------------------------------
    def salvar_movimentos(self):
        dados = {
            "total_movimentos": self.contador_movimentos,
            "ultimos_movimentos": self.movimentos[-10:],
            "ultimo_comando": self.ultimo_comando,
            "estado_atual": "SCROLL_ATIVO" if self.em_scroll else "AGUARDANDO"
        }
        with open("movimentos_maos.json", "w") as f:
            json.dump(dados, f, indent=4)
        print("Movimentos salvos em movimentos_maos.json")

    # ------------------------------------------------------------
    # Função principal - captura da câmera e detecção de mãos
    # ------------------------------------------------------------
    def detectar_movimentos(self):
        cap = cv2.VideoCapture(0)

        # Define resolução da câmera
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        print("=== 🎮 SISTEMA DE CONTROLE POR GESTOS ===")
        print("📗 GESTOS:")
        print("  - APENAS DEDO INDICADOR → Abre YouTube Shorts + Scroll Automático")
        print("  - MÃO FECHADA (✊) → Para o scroll")
        print("")
        print("🎯 INSTRUÇÕES:")
        print("  1. Mostre APENAS o DEDO INDICADOR para abrir YouTube")
        print("  2. Feche a MÃO (✊) para parar o scroll")
        print("  3. Mouse será movido para o CENTRO automaticamente")
        print("")
        print("⌨️  TECLAS:")
        print("  q - Sair | s - Salvar | c - Ativar/Desativar | r - Reset")
        print("  m - Mover mouse para o centro (manual)")
        
        # 🆕 Move o mouse para o centro ao iniciar o programa
        self.mover_mouse_centro()
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Erro ao capturar frame. Verifique a câmera.")
                break
            
            # Espelha a câmera para ficar mais intuitivo
            frame = cv2.flip(frame, 1)
            
            # Converte BGR para RGB (MediaPipe usa RGB)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Processa o frame para detectar mãos
            resultados = self.hands.process(rgb_frame)
            
            acao_executada = ""
            
            if resultados.multi_hand_landmarks:
                for hand_landmarks in resultados.multi_hand_landmarks:
                    # Desenha os landmarks da mão
                    self.mp_draw.draw_landmarks(
                        frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                    
                    # Converte landmarks para array numpy
                    landmarks = hand_landmarks.landmark
                    
                    # Detecta gesto
                    gesto = self.detectar_gesto(landmarks)
                    
                    # Controla por gestos
                    acao = self.controlar_por_gestos(gesto, landmarks, frame)
                    if acao:
                        acao_executada = acao
                        self.movimentos.append(acao)
                        self.contador_movimentos += 1
                        if len(self.movimentos) > 10:
                            self.movimentos.pop(0)
                        self.ultimo_comando = acao
                    
                    # Mostra gesto detectado
                    cv2.putText(frame, f'Gesto: {gesto}', 
                               (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    
                    # Destaca o dedo indicador em amarelo
                    h, w, c = frame.shape
                    cx, cy = int(landmarks[8].x * w), int(landmarks[8].y * h)
                    cv2.circle(frame, (cx, cy), 12, (0, 255, 255), -1)
                    
                    # Se é apenas dedo indicador, destaca ainda mais
                    if gesto == "DEDO_INDICADOR":
                        cv2.circle(frame, (cx, cy), 15, (0, 255, 0), 3)
            
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
            
            # Estado do scroll
            scroll_status = "SCROLL ATIVO 🎬" if self.em_scroll else "AGUARDANDO GESTO ⏸️"
            cor_scroll = (0, 0, 255) if self.em_scroll else (0, 255, 255)
            cv2.putText(frame, f"Estado: {scroll_status}", (10, y_pos),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, cor_scroll, 2)
            y_pos += 30
            
            # Posição atual do mouse
            mouse_x, mouse_y = pd.position()
            cv2.putText(frame, f"Mouse: ({mouse_x}, {mouse_y})", (10, y_pos),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 255), 1)
            y_pos += 25
            
            # Última ação
            if acao_executada:
                cv2.putText(frame, f"Ultima acao: {acao_executada}", (10, y_pos),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
                y_pos += 25
            
            # Contador total
            cv2.putText(frame, f"Total de acoes: {self.contador_movimentos}", (10, y_pos),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            y_pos += 25
            
            # Instruções na tela
            instrucoes = [
                "INSTRUCOES:",
                "📗 APENAS DEDO INDICADOR -> Abre YouTube + Scroll",
                "✊ MAO FECHADA -> Para scroll + Fecha aba",
                "🖱️ Mouse vai para CENTRO automaticamente",
                "⌨️  TECLAS: q-sair, m-centro mouse"
            ]
            
            for i, instrucao in enumerate(instrucoes):
                cv2.putText(frame, instrucao, (frame.shape[1] - 400, 30 + i*25),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
            
            # Mostra o vídeo com as marcações
            cv2.imshow('🎮 Controle por Gestos - YouTube Shorts', frame)

            # Controles via teclado
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):   # sair
                self.scroll_ativo = False
                break
            elif key == ord('s'): # salvar
                self.salvar_movimentos()
            elif key == ord('c'): # ativar/desativar detecção
                self.comandos_ativos = not self.comandos_ativos
                print(f"Detecção {'ativada' if self.comandos_ativos else 'desativada'}!")
            elif key == ord('r'): # resetar contador
                self.contador_movimentos = 0
                self.movimentos = []
                self.scroll_ativo = False
                self.em_scroll = False
                print("Sistema resetado!")
            elif key == ord('m'): # 🆕 Mover mouse para centro (manual)
                self.mover_mouse_centro()
                
        # Libera recursos
        cap.release()
        cv2.destroyAllWindows()
        self.hands.close()
        self.scroll_ativo = False
        print("Sistema finalizado.")


# ------------------------------------------------------------
# Execução principal
# ------------------------------------------------------------
if __name__ == "__main__":
    detector = DetectorGestosMaosAvancado()
    detector.detectar_movimentos()