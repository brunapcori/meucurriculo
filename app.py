import glob
import os
import re
import pdfplumber
import streamlit as st

st.set_page_config(
    page_title="Bruna Prado Coriolano | Currículo Profissional",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Estilização Moderna, Limpa e Elegante
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .main {
        background-color: #fcfcfd;
    }

    /* Card Principal */
    .hero-card {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        border-radius: 16px;
        padding: 2.2rem;
        color: #ffffff;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.15);
    }

    .hero-title {
        font-size: 2.1rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
        color: #f8fafc;
    }

    .hero-subtitle {
        font-size: 1.1rem;
        color: #94a3b8;
        font-weight: 400;
        margin-bottom: 0.8rem;
    }

    /* Container de Seções */
    .section-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 1.5rem 1.8rem;
        margin-bottom: 1.4rem;
        box-shadow: 0 4px 6px -2px rgba(0, 0, 0, 0.03);
    }

    .section-header {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        font-size: 1.15rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 1rem;
        border-bottom: 2px solid #f1f5f9;
        padding-bottom: 0.6rem;
    }

    /* Badges */
    .skill-badge {
        display: inline-block;
        padding: 0.35rem 0.75rem;
        margin: 0.2rem;
        font-size: 0.82rem;
        font-weight: 600;
        border-radius: 8px;
        background-color: #f1f5f9;
        color: #334155;
        border: 1px solid #e2e8f0;
    }

    /* Links e Botões */
    .contact-link {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        padding: 0.6rem 0.9rem;
        background-color: #ffffff;
        border: 1px solid #cbd5e1;
        border-radius: 10px;
        color: #1e293b !important;
        text-decoration: none;
        font-weight: 500;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
        transition: all 0.2s ease;
    }

    .contact-link:hover {
        border-color: #0284c7;
        background-color: #f0f9ff;
    }
</style>
""",
    unsafe_allow_html=True,
)


def find_profile_photo():
  possible_names = [
      "profile.png",
      "profile.jpg",
      "profile.jpeg",
      "foto.png",
      "foto.jpg",
  ]
  for path in possible_names:
    if os.path.exists(path):
      return path
    subpath = os.path.join("media", path)
    if os.path.exists(subpath):
      return subpath
  return None


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
  try:
    with pdfplumber.open(pdf_path) as pdf:
      for page in pdf.pages:
        text = page.extract_text()
        if text:
          extracted_text.append(text)
  except Exception:
    return ""
  return "\n".join(extracted_text)


def parse_curriculum_sections(raw_text):
  """Segmenta o texto do PDF por tópicos conhecidos ou por blocos estruturados."""
  if not raw_text.strip():
    return {}

  keywords = [
      "Resumo",
      "Sobre",
      "Perfil Profissional",
      "Experiência",
      "Experiência Profissional",
      "Histórico Profissional",
      "Formação",
      "Formação Acadêmica",
      "Educação",
      "Competências",
      "Habilidades",
      "Certificações",
      "Cursos",
      "Idiomas",
      "Projetos",
  ]
  pattern = r"(?i)^\s*(" + "|".join(keywords) + r")\s*[:\-]?\s*$"

  sections = {}
  current_section = "Informações Gerais"
  sections[current_section] = []

  for line in raw_text.splitlines():
    clean_line = line.strip()
    if not clean_line:
      continue
    if re.match(pattern, clean_line):
      current_section = clean_line.title()
      if current_section not in sections:
        sections[current_section] = []
    else:
      sections[current_section].append(clean_line)

  return {k: "\n".join(v) for k, v in sections.items() if v}


pdf_path = get_latest_pdf()
photo_path = find_profile_photo()

# Sidebar
with st.sidebar:
  if photo_path:
    st.image(photo_path, use_container_width=True)
  else:
    st.image(
        "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?q=80&w=400&auto=format&fit=crop",
        use_container_width=True,
    )

  st.markdown("### **Bruna Prado Coriolano**")
  st.caption(
      "Gestão de Riscos & Análise de Seguros Corporativos | Automação Python"
  )

  st.markdown("---")
  st.markdown("#### **Conecte-se comigo**")
  st.markdown(
      """
        <a class="contact-link" href="https://www.linkedin.com/in/brunapcoriolano/" target="_blank">
            <svg width="18" height="18" fill="#0a66c2" viewBox="0 0 24 24"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/></svg>
            Perfil no LinkedIn
        </a>
        <a class="contact-link" href="https://github.com/brunapcori" target="_blank">
            <svg width="18" height="18" fill="#24292f" viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
            Repositório GitHub
        </a>
    """,
      unsafe_allow_html=True,
  )

  st.markdown("---")
  st.markdown("#### **Competências Centrais**")
  skills = [
      "Gestão de Riscos",
      "Seguros Corporativos",
      "Regulação de Sinistros",
      "Python",
      "Streamlit",
      "Pandas",
      "Automação de Processos",
      "Power BI",
  ]
  badge_html = "".join([f'<span class="skill-badge">{s}</span>' for s in skills])
  st.markdown(badge_html, unsafe_allow_html=True)

  st.markdown("---")
  if pdf_path and os.path.exists(pdf_path):
    with open(pdf_path, "rb") as f:
      st.download_button(
          label="📄 Baixar PDF do Currículo",
          data=f.read(),
          file_name=os.path.basename(pdf_path),
          mime="application/pdf",
          use_container_width=True,
      )
  else:
    st.info("Adicione o arquivo `.pdf` na pasta `./data` para liberar o download.")

# Área Principal
st.markdown(
    """
<div class="hero-card">
    <div class="hero-title">Bruna Prado Coriolano</div>
    <div class="hero-subtitle">Especialista em Riscos Corporativos & Soluções com Dados e Automação</div>
    <div style="font-size: 0.95rem; color: #cbd5e1; max-width: 800px; line-height: 1.6;">
        Profissional dedicada à otimização de fluxos operacionais, análise estratégica de coberturas securitárias e desenvolvimento de ferramentas interativas orientadas à eficiência analítica.
    </div>
</div>
""",
    unsafe_allow_html=True,
)

col_video, col_info = st.columns([1.2, 1], gap="large")

with col_video:
  st.markdown(
      """
    <div class="section-header">
        <span>🎥</span> Vídeo de Apresentação
    </div>
    """,
      unsafe_allow_html=True,
  )

  # Adicione o link do seu vídeo do YouTube, Vimeo ou arquivo local (ex: ./media/apresentacao.mp4)
  video_source = ""

  if video_source:
    try:
      st.video(video_source)
    except Exception:
      st.warning("Não foi possível carregar o vídeo.")
  else:
    st.info(
        "Espaço reservado para o seu vídeo de apresentação. Insira a URL do"
        " YouTube/Vimeo ou arquivo na variável `video_source`."
    )

with col_info:
  st.markdown(
      """
    <div class="section-header">
        <span>📌</span> Destaques & Status
    </div>
    """,
      unsafe_allow_html=True,
  )

  if pdf_path:
    st.success(f"**Documento Ativo:** `{os.path.basename(pdf_path)}`")
    st.caption(
        "As informações abaixo são sincronizadas em tempo real a partir do"
        " repositório."
    )
  else:
    st.warning("Nenhum arquivo PDF encontrado na pasta `./data`.")
    st.caption("Suba o arquivo PDF no repositório para visualização automática.")

  st.markdown("""
    * **Foco:** Análise técnica, mitigação de riscos e automações.
    * **Tecnologias:** Python, Pandas, Streamlit, Integrações com LLMs / APIs.
    * **Disponibilidade:** Projetos estratégicos e oportunidades corporativas.
    """)

st.markdown("<br>", unsafe_allow_html=True)

# Tópicos do Currículo
st.markdown(
    """
<div class="section-header">
    <span>📋</span> Trajetória Profissional & Estrutura
</div>
""",
    unsafe_allow_html=True,
)

if pdf_path:
  raw_text = extract_pdf_data(pdf_path)
  sections = parse_curriculum_sections(raw_text)

  if sections:
    for title, content in sections.items():
      with st.expander(
          f"🔹 {title}",
          expanded=(
              title in ["Resumo", "Sobre", "Informações Gerais", "Experiência"]
          ),
      ):
        st.markdown(
            f"""
                <div style="background-color: #f8fafc; padding: 1.2rem; border-radius: 8px; border: 1px solid #edf2f7; line-height: 1.6; color: #1e293b; font-size: 0.95rem; white-space: pre-wrap;">
{content}
                </div>
                """,
            unsafe_allow_html=True,
        )
  else:
    st.warning(
        "O PDF carregado não possui texto selecionável ou estruturado legível."
    )
else:
  st.info(
      "Assim que você fizer o upload do seu currículo em PDF na pasta"
      " `./data/`, as seções serão montadas automaticamente aqui."
  )
