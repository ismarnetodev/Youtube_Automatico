# 🔥 Foguinho Automático

O **Foguinho Automático** é um projeto em desenvolvimento que utiliza **visão computacional** para **reconhecer movimentos faciais** e realizar **ações automatizadas no computador**.  
Atualmente, o sistema identifica quando o usuário **baixa o rosto por cinco segundos**, e em resposta, executa um comando **Alt + Tab** para alternar de janela, abrir o **YouTube Shorts** e **rolar automaticamente os vídeos**.

---

## 🧠 Objetivo

O projeto tem como propósito explorar o uso de **reconhecimento facial aplicado à automação**, abrindo caminho para novas formas de **interação sem o uso das mãos** — especialmente útil em contextos de acessibilidade e automação pessoal.

---

## ⚙️ Tecnologias utilizadas

- **Python 3**
- **OpenCV** – Captura e processamento de vídeo
- **Mediapipe** (ou biblioteca similar) – Detecção de rosto e pontos faciais
- **PyAutoGUI** – Execução de comandos automáticos no sistema

---

## 🚀 Funcionamento atual

1. O sistema inicia a captura de vídeo pela webcam.  
2. Monitora continuamente a posição do rosto do usuário.  
3. Quando o rosto permanece abaixado por **5 segundos**, o programa:
   - Executa o comando **Alt + Tab**;
   - Abre o **YouTube Shorts**;
   - E começa a **rolar automaticamente os vídeos**.

---

## 📦 Estrutura do projeto

