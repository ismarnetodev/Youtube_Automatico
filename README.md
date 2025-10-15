# 🔥 Youtube Automático

Sistema inteligente de automação que utiliza visão computacional e gestos manuais para controlar o computador de forma hands-free. Desenvolvido para facilitar a navegação e interação com aplicativos através de comandos gestuais.

## 🎯 Sobre o Projeto

O **Youtube Automático** é uma aplicação Python que combina **OpenCV** e **MediaPipe** para detectar gestos manuais em tempo real e executar ações automatizadas no sistema. O foco principal é proporcionar uma experiência de navegação intuitiva e acessível.

### ⚡ Funcionalidade Principal
- **Controle por gestos** para automação do YouTube Shorts
- **Scroll automático** inteligente
- **Interface visual** em tempo real com feedback dos gestos

## 🚀 Características

### 🤖 Automações Implementadas
- ✅ **Abertura automática** do YouTube Shorts
- ✅ **Scroll contínuo** hands-free
- ✅ **Controle gestual** preciso
- ✅ **Interface visual** intuitiva
- ✅ **Feedback em tempo real**

### 🎮 Gestos Suportados
| Gestos | Ação | Descrição |
|--------|------|-----------|
| 👆 **Dedo Indicador** | Abre YouTube + Scroll | Apenas o dedo indicador levantado |
| ✊ **Mão Fechada** | Para Scroll + Fecha Aba | Todos os dedos fechados |
| 🖱️ **Tecla M** | Centraliza Mouse | Controle manual do mouse |

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**
- **OpenCV** - Processamento de imagem em tempo real
- **MediaPipe** - Detecção avançada de mãos e gestos
- **PyAutoGUI** - Automação de interface e controle do sistema
- **NumPy** - Processamento numérico eficiente
- **WebBrowser** - Integração com navegador web

## 📦 Instalação Rápida

### Instalação de Todas as Dependências
```bash
pip install opencv-python mediapipe pyautogui numpy
```

### Pré-requisitos
```bash
# Python 3.8 ou superior
python --version

# Gerenciador de pacotes pip
pip --version
```

### Configuração do Projeto
```bash
# Clone o repositório
git clone https://github.com/ismarnetodev/foguinho_automatico.git
cd foguinho_automatico

# Instale todas as dependências de uma vez
pip install opencv-python mediapipe pyautogui numpy
```

## 🎯 Como Usar

### Execução do Sistema
```bash
python app.py
```

### Fluxo de Uso
1. **Inicie o programa**
2. **Posicione sua mão** frente à câmera
3. **Mostre apenas o dedo indicador** 👆 para:
   - Abrir YouTube Shorts automaticamente
   - Iniciar scroll automático

4. **Feche a mão** ✊ para:
   - Parar o scroll
   - Fechar a aba do YouTube

### Controles por Teclado
| Tecla | Ação |
|-------|------|
| `Q` | Sair do programa |
| `S` | Salvar dados de movimento |
| `C` | Ativar/Desativar detecção |
| `R` | Resetar contadores |
| `M` | Centralizar mouse |

## 🏗️ Estrutura do Projeto

```
foguinho_automatico/
├── app.py                 # Aplicação principal
├── movimentos_maos.json   # Dados salvos dos gestos
└── README.md             # Documentação
```

## 🔧 Configuração

### Ajustes de Sensibilidade
No código, você pode ajustar:

```python
# Sensibilidade da detecção de gestos
min_detection_confidence=0.7
min_tracking_confidence=0.5

# Velocidade do scroll
pd.scroll(-100)  # Ajuste o valor para mais/menos velocidade
```

### Resolução da Câmera
```python
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
```

## 🎨 Personalização

### Adicionar Novos Gestos
```python
def detectar_novo_gesto(self, landmarks):
    # Implemente sua lógica de detecção aqui
    if novo_gesto_condicao:
        return "NOVO_GESTO"
```

### Novas Ações Automatizadas
```python
def executar_nova_acao(self):
    # Adicione novas funcionalidades
    pd.hotkey('ctrl', 't')  # Exemplo: nova aba
```

## 📊 Funcionalidades Técnicas

### Detecção de Gestos
- **21 pontos de referência** por mão
- **Precisão em tempo real**
- **Robusto a variações de iluminação**

### Sistema de Controle
- **Threading** para operações paralelas
- **Gestão de estado** eficiente
- **Tratamento de erros** robusto

## 🤝 Contribuição

Contribuições são bem-vindas! Siga estos passos:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👨‍💻 Desenvolvedor

**Ismarneto Dev**
- GitHub: [@ismarnetodev](https://github.com/ismarnetodev)
- Projeto: [Youtube Automático](https://github.com/ismarnetodev/foguinho_automatico)

## 🆘 Suporte

Encontrou problemas? 
1. Verifique se todas as dependências estão instaladas
2. Confirme que sua câmera está funcionando
3. Teste em ambiente com boa iluminação
4. Abra uma [issue](https://github.com/ismarnetodev/foguinho_automatico/issues) no GitHub

---

**⭐ Se este projeto foi útil, deixe uma estrela no repositório!**

**🔥 Automatize seu fluxo com Youtube Automático!**
