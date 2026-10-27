import os
import glob
import streamlit as st
import pdfplumber

st.set_page_config(
    page_title="Currículo Interativo",
    page_icon="📄",
    layout="wide"
)

# Custom Styling
st.markdown("""
<style>
    .main {
        background-color: #f8fafc;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.07);
        border: 1px solid #e2e8f0;
        margin-bottom: 1rem;
    }
    .badge {
        display: inline-block;
        padding: 0.25rem 0.65rem;
        margin: 0.2rem;
        font-size: 0.85rem;
        font-weight: 500;
        border-radius: 9999px;
        background-color: #e0f2fe;
        color: #0369a1;
    }
</style>
""", unsafe_allow_html=True)

def get_latest_pdf(search_dirs=["./data", "."]):
    pdf_files = []
    for directory in search_dirs:
        if os.path.exists(directory):
            pdf_files.extend(glob.glob(os.path.join(directory, "*.pdf")))
    if not pdf_files:
        return None
    return max(pdf_files, key=os.path.getmtime)

def extract_pdf_data(pdf_path):
    extracted_text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                extracted_text.append(text)
    return "\n\n".join(extracted_text)

# Localizar PDF
pdf_path = get_latest_pdf()

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/180", caption="Foto de Perfil", width=180)
    st.title("Seu Nome")
    st.caption("Especialista / Analista | Localização")
    
    st.markdown("---")
    st.subheader("🌐 Contato & Redes")
    st.markdown("[🔗 LinkedIn](https://www.linkedin.com)", unsafe_allow_html=True)
    st.markdown("[💻 GitHub](https://github.com)", unsafe_allow_html=True)
    st.markdown("✉️ contato@email.com")

    st.markdown("---")
    st.subheader("🛠️ Principais Competências")
    skills = ["Python", "Streamlit", "Pandas", "Automação", "Processamento de Dados", "Gestão de Processos"]
    badge_html = "".join([f'<span class="badge">{s}</span>' for s in skills])
    st.markdown(badge_html, unsafe_allow_html=True)

    st.markdown("---")
    if pdf_path and os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="📥 Baixar PDF Original",
                data=f.read(),
                file_name=os.path.basename(pdf_path),
                mime="application/pdf",
                use_container_width=True
            )
    else:
        st.info("Nenhum arquivo PDF detectado para download.")

# Área Principal
col_title, col_status = st.columns([3, 1])
with col_title:
    st.title("Apresentação Profissional")
with col_status:
    if pdf_path:
        st.success(f"Arquivo carregado: `{os.path.basename(pdf_path)}`")
    else:
        st.warning("Aguardando PDF em `./data`")

# Seção de Vídeo
st.subheader("🎬 Pitch de Apresentação")
video_source = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Insira a URL do YouTube/Drive ou './media/video.mp4'

if video_source:
    try:
        st.video(video_source)
    except Exception as e:
        st.info("Vídeo de apresentação temporariamente indisponível.")
else:
    st.info("Adicione o link ou arquivo do seu vídeo de apresentação no código.")

st.markdown("---")

# Conteúdo do Currículo Dinâmico
st.subheader("📑 Conteúdo do Currículo")

if pdf_path:
    pdf_text = extract_pdf_data(pdf_path)
    if pdf_text.strip():
        # Exibe em um container estruturado
        with st.container():
            st.markdown(f"""
            <div class="metric-card">
                <pre style="white-space: pre-wrap; font-family: inherit; font-size: 0.95rem; line-height: 1.6; color: #1e293b; margin: 0;">
{pdf_text}
                </pre>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("O PDF carregado não possui texto selecionável/legível.")
else:
    st.info("Para visualizar as informações, envie seu currículo em formato PDF para a pasta `./data` no GitHub.")
