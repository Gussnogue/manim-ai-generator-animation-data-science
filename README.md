# 🎬 Manim AI Generator – Animações Matemáticas com Groq

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-red)](https://streamlit.io)
[![Manim](https://img.shields.io/badge/Manim-0.18%2B-purple)](https://www.manim.community)
[![Groq](https://img.shields.io/badge/Groq-Llama%203.3%2070B-orange)](https://groq.com)

Aplicação **Streamlit** que conecta a API da **Groq** (modelo `llama-3.3-70b-versatile`) para gerar animações matemáticas com a biblioteca **Manim**.  O usuário descreve a cena em linguagem natural, a IA retorna o código Python executável e o sistema renderiza localmente o vídeo com qualidade ajustável (480p a 4K).

* * *

## ✨ Funcionalidades

* ✅ **Geração por IA:** Descreva a animação em português ou inglês – o modelo Llama 3.3 70B gera o código Manim.
* ✅ **Renderização local:** O Manim é executado no seu computador, com suporte a preview automático.
* ✅ **Qualidade ajustável:** Escolha entre `480p`, `720p`, `1080p` ou `4K` diretamente na interface.
* ✅ **Privacidade:** Apenas a descrição é enviada para a Groq; todo o processamento e geração de vídeo são locais.
* ✅ **Download do código:** Salve o script `.py` gerado para reúso ou ajustes manuais.
* ✅ **Histórico da conversa:** O chat mantém contexto das últimas mensagens para refinamentos.

* * *

## 🚀 Como Executar

### Pré-requisitos

* **Python 3.10+**
* **Conta na Groq** e uma chave de API ([console.groq.com](https://console.groq.com))
* **Manim** instalado e funcionando ([guia oficial](https://docs.manim.community))

### Passo a Passo

1. **Clone o repositório**

   ```bash
   git clone https://github.com/Gussnogue/manim-ai-generator-animation-data-science.git
   cd manim-ai-generator-animation-data-science

2. **Crie e ative um ambiente virtual**

   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt

4. **Configure sua chave da Groq**
   ```bash
   GROQ_API_KEY=sua_chave_aqui
   
5. **Execute o aplicativo**
   ```bash
   streamlit run app.py

### 🧠 Como Usar

Na barra lateral, insira sua chave da API Groq (se não estiver no .env).

Selecione a qualidade da animação desejada.

No chat, digite a descrição da cena (ex.: "Crie um círculo se transformando em um quadrado").

A IA responderá com o código Manim gerado.

Clique em "Renderizar" para executar o Manim e gerar o vídeo.

O vídeo será exibido na tela e você poderá baixar o código-fonte.


### 📄 Licença
Este projeto está licenciado sob a MIT License – veja o arquivo LICENSE para mais detalhes.
