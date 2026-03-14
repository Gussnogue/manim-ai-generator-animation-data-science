import streamlit as st
import os
import subprocess
import sys
from pathlib import Path
import tempfile
import shutil

# Configuração da página
st.set_page_config(
    page_title="Assistente Manim com Groq",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Assistente de Animações Manim com Groq")
st.markdown(
    "Converse com um especialista em Manim. Descreva a animação que deseja e ele gerará o código. "
    "Depois, clique em **Renderizar** para ver o vídeo."
)

# Sidebar para configurações
with st.sidebar:
    st.header("🔧 Configurações")

    groq_api_key = st.text_input(
        "Chave da API Groq",
        type="password",
        help="Insira sua chave da Groq (ex: gsk_...). Obtenha em console.groq.com"
    )

    modelo_groq = st.selectbox(
        "Modelo",
        options=[
            "llama-3.3-70b-versatile",
            "llama3-70b-8192",
            "llama3-8b-8192",
            "gemma2-9b-it"
        ],
        index=0,
        help="Escolha o modelo da Groq. Recomendado: llama-3.3-70b-versatile"
    )

    qualidade = st.selectbox(
        "Qualidade da animação",
        options=["480p15", "720p30", "1080p60"],
        index=0,
        help="Qualidade do vídeo gerado (480p é mais rápido)"
    )

    st.divider()
    st.caption("Powered by Groq + Manim + Streamlit")

if not groq_api_key:
    st.warning("⚠️ Por favor, insira sua chave da API Groq na barra lateral.")
    st.stop()

from groq import Groq

@st.cache_resource
def get_groq_client(api_key):
    return Groq(api_key=api_key)

client = get_groq_client(groq_api_key)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Olá! Sou seu assistente Manim. Descreva a animação que você quer criar."}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Descreva sua animação..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Gerando código..."):
            system_prompt = """
Você é um especialista em Manim (biblioteca de animações matemáticas em Python).
Gere apenas código Python executável que crie uma cena chamada 'MyScene' (exatamente com esse nome).
O código deve importar tudo de manim (`from manim import *`) e também importar `math` e `numpy as np` se necessário.
Certifique-se de que todas as funções e módulos usados estejam importados.
O código não deve conter erros de sintaxe e deve ser executável.
Use as classes corretas do Manim (por exemplo, para gráficos use `axes.plot`, para atualizações use `always_redraw` com cuidado).
Gere apenas o código, sem explicações.
"""
            try:
                response = client.chat.completions.create(
                    model=modelo_groq,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-5:]]
                    ],
                    temperature=0.2,
                    max_tokens=2000
                )
                codigo = response.choices[0].message.content
                codigo = codigo.replace("```python", "").replace("```", "").strip()
                st.code(codigo, language="python")
                st.session_state["ultimo_codigo"] = codigo
                resposta_texto = "Código gerado! Use o botão abaixo para renderizar."
            except Exception as e:
                st.error(f"Erro na chamada da Groq: {e}")
                st.stop()

    st.session_state.messages.append({"role": "assistant", "content": resposta_texto})

if "ultimo_codigo" in st.session_state:
    st.divider()
    col1, col2 = st.columns([1, 5])
    with col1:
        renderizar = st.button("🎥 Renderizar Animação")

    if renderizar:
        with st.spinner("Renderizando (pode levar alguns segundos)..."):
            with tempfile.TemporaryDirectory() as tmpdir:
                arquivo_py = Path(tmpdir) / "animacao.py"
                arquivo_py.write_text(st.session_state["ultimo_codigo"], encoding="utf-8")

                # Mapeamento correto da qualidade para flag do Manim
                flag_map = {
                    "480p15": "-pql",
                    "720p30": "-pqm",
                    "1080p60": "-pqh",
                }
                flag = flag_map.get(qualidade, "-pql")

                cmd = [
                    sys.executable, "-m", "manim",
                    flag,
                    str(arquivo_py),
                    "MyScene"
                ]

                try:
                    resultado = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

                    if resultado.returncode != 0:
                        st.error(f"Erro na renderização:\n{resultado.stderr}")
                        with st.expander("Ver código enviado"):
                            st.code(st.session_state["ultimo_codigo"], language="python")
                    else:
                        video_path = None
                        possiveis_caminhos = [
                            Path(tmpdir) / "media" / "videos" / "animacao" / qualidade / "MyScene.mp4",
                            Path(tmpdir) / "media" / "videos" / "animacao" / "480p15" / "MyScene.mp4",
                            Path(tmpdir) / "media" / "videos" / "animacao" / "720p30" / "MyScene.mp4",
                            Path(tmpdir) / "media" / "videos" / "animacao" / "1080p60" / "MyScene.mp4"
                        ]

                        for caminho in possiveis_caminhos:
                            if caminho.exists():
                                video_path = caminho
                                break

                        if not video_path:
                            st.error("Vídeo não encontrado após renderização.")
                            st.stop()

                        destino = Path("media") / "ultimo_video.mp4"
                        destino.parent.mkdir(exist_ok=True)
                        shutil.copy(video_path, destino)

                        st.success("Renderização concluída!")
                        st.video(str(destino))

                except subprocess.TimeoutExpired:
                    st.error("Tempo limite excedido (10000s). A animação pode ser muito complexa.")
                except Exception as e:
                    st.error(f"Erro inesperado: {e}")

    with col2:
        st.download_button(
            label="📥 Download do código (.py)",
            data=st.session_state["ultimo_codigo"],
            file_name="animacao_manim.py",
            mime="text/plain"
        )

        