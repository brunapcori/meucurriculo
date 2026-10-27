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

# Estilização CSS Moderna, Executiva e Elegante
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
    }

    .main {
        background-color: #f8fafc;
    }

    /* Hero Banner Executivo */
    .hero-card {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
        border-radius: 18px;
        padding: 2.4rem;
        color: #ffffff;
        margin-bottom: 2rem;
        box-shadow: 0 12px 30px -10px rgba(15, 23, 42, 0.25);
        border: 1px solid rgba(255, 255, 255, 0.08);
    }

    .hero-title {
        font-size: 2.3rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: #ffffff;
        margin-bottom: 0.3rem;
    }

    .hero-subtitle {
        font-size: 1.15rem;
        color: #38bdf8;
        font-weight: 600;
        margin-bottom: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    .hero-bio {
        font-size: 0.98rem;
        color: #cbd5e1;
        max-width: 950px;
        line-height: 1.7;
    }

    /* Cards Estruturados */
    .content-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 1.6rem;
        margin-bottom: 1.3rem;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.03);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }

    .content-card:hover {
        box-shadow: 0 8px 20px rgba(15, 23, 42, 0.06);
        border-color: #cbd5e1;
    }

    .card-header-row {
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        flex-wrap: wrap;
        margin-bottom: 0.6rem;
    }

    .role-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #0f172a;
    }

    .company-name {
        font-size: 1rem;
        font-weight: 600;
        color: #0284c7;
    }

    .period-badge {
        background-color: #f1f5f9;
        color: #475569;
        font-size: 0.82rem;
        font-weight: 600;
        padding: 0.25rem 0.65rem;
        border-radius: 9999px;
        border: 1px solid #e2e8f0;
    }

    /* Badges Técnicas e Comportamentais */
    .tag-pill {
        display: inline-block;
        padding: 0.35rem 0.75rem;
        margin: 0.25rem 0.25rem;
        font-size: 0.85rem;
        font-weight: 600;
        border-radius: 8px;
        border: 1px solid transparent;
    }

    .tag-blue {
        background-color: #e0f2fe;
        color: #0369a1;
        border-color: #bae6fd;
    }

    .tag-purple {
        background-color: #f3e8ff;
        color: #7e22ce;
        border-color: #e9d5ff;
    }

    .tag-emerald {
        background-color: #d1fae5;
        color: #047857;
        border-color: #a7f3d0;
    }

    .tag-slate {
        background-color: #f1f5f9;
        color: #334155;
        border-color: #e2e8f0;
    }

    /* Links de Contato */
    .contact-button {
        display: flex;
        align-items: center;
        gap: 0.7rem;
        padding: 0.65rem 1rem;
        background-color: #ffffff;
        border: 1px solid #cbd5e1;
        border-radius: 10px;
        color: #0f172a !important;
        text-decoration: none;
        font-weight: 600;
        font-size: 0.88rem;
        margin-bottom: 0.6rem;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    }

    .contact-button:hover {
        border-color: #0284c7;
        background-color: #f8fafc;
        color: #0284c7 !important;
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


pdf_path = get_latest_pdf()
photo_path = find_profile_photo()

# Barra Lateral (Sidebar)
with st.sidebar:
  if photo_path:
    st.image(photo_path, use_container_width=True)
  else:
    st.image(
        "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?q=80&w=400&auto=format&fit=crop",
        use_container_width=True,
    )

  st.markdown("### **Bruna Prado Coriolano**")
  st.markdown(
      "<p style='color: #64748b; font-size: 0.9rem; margin-top:-10px;'>Seguros"
      " • Sinistros • Gestão de Riscos • Corporate Insurance</p>",
      unsafe_allow_html=True,
  )
  st.caption("📍 Sorocaba - SP | Brasil")

  st.markdown("---")
  st.markdown("#### **Canais de Contato**")
  st.markdown(
      """
        <a class="contact-button" href="https://www.linkedin.com/in/brunapcoriolano/" target="_blank">
            <svg width="18" height="18" fill="#0a66c2" viewBox="0 0 24 24"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/></svg>
            Perfil no LinkedIn
        </a>
        <a class="contact-button" href="mailto:brunapcoriolano@gmail.com">
            <svg width="18" height="18" fill="#e11d48" viewBox="0 0 24 24"><path d="M12 12.713l-11.985-8.713h23.97l-11.985 8.713zm0 2.574l-12-8.725v13.438h24v-13.438l-12 8.725z"/></svg>
            brunapcoriolano@gmail.com
        </a>
        <a class="contact-button" href="https://github.com/brunapcori" target="_blank">
            <svg width="18" height="18" fill="#24292f" viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
            GitHub Projects
        </a>
    """,
      unsafe_allow_html=True,
  )

  st.markdown("---")
  st.markdown("#### **Download do Currículo**")
  if pdf_path and os.path.exists(pdf_path):
    with open(pdf_path, "rb") as f:
      st.download_button(
          label="📥 Baixar Versão em PDF",
          data=f.read(),
          file_name=os.path.basename(pdf_path),
          mime="application/pdf",
          use_container_width=True,
      )
    st.caption(f"Sincronizado: `{os.path.basename(pdf_path)}`")
  else:
    st.info("Suba seu PDF na pasta `./data` para ativar o download.")

# Área Principal - Hero Banner
st.markdown(
    """
<div class="hero-card">
    <div class="hero-title">Bruna Prado Coriolano</div>
    <div class="hero-subtitle">Engenheira Civil • MBA Gestão de Projetos • Especialista em Riscos e Seguros Corporativos</div>
    <div class="hero-bio">
        Mais de 10 anos de sólida trajetória no mercado segurador, com atuação destacada em seguradoras de grande porte e gestão direta no segurado corporativo. Experiência de ponta em mitigação de riscos, governança securitária, análise e regulação de sinistros e desenvolvimento de soluções digitais orientadas à eficiência e dados.
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# Apresentação em Vídeo
st.markdown("### 🎥 Vídeo de Apresentação")
col_vid, col_vid_txt = st.columns([1.5, 1], gap="medium")

# Cole a URL do YouTube, Vimeo ou link direto para seu vídeo na variável abaixo:
video_source = ""

with col_vid:
  if video_source:
    try:
      st.video(video_source)
    except Exception:
      st.warning("Não foi possível carregar o vídeo.")
  else:
    st.markdown(
        """
        <div style="background: #ffffff; border: 2px dashed #cbd5e1; border-radius: 12px; padding: 2.5rem; text-align: center; color: #64748b;">
            <p style="font-size: 1.8rem; margin: 0;">🎬</p>
            <p style="font-weight: 600; margin: 0.5rem 0 0 0;">Espaço Reservado para Pitch Pessoal</p>
            <p style="font-size: 0.85rem; margin: 0;">Adicione o link do seu vídeo na variável <code>video_source</code> no arquivo <code>app.py</code>.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_vid_txt:
  st.markdown(
      """
    <div class="content-card" style="margin-bottom:0; height: 100%;">
        <div style="font-weight: 700; color: #0f172a; margin-bottom: 0.5rem; font-size: 1rem;">💼 Proposta de Valor</div>
        <ul style="color: #475569; font-size: 0.92rem; line-height: 1.7; padding-left: 1.2rem; margin: 0;">
            <li>Domínio completo de <b>Property, RC, Obras, Garantia e D&O</b>.</li>
            <li>Histórico comprovado em <b>redução de custos</b> em renovações e cotações.</li>
            <li>Interface estratégica entre <b>Diretoria, Jurídico, Engenharia e Operações</b>.</li>
            <li>Automação analítica com <b>Python, Streamlit e BI</b>.</li>
        </ul>
    </div>
    """,
      unsafe_allow_html=True,
  )

st.markdown("<br>", unsafe_allow_html=True)

# Seções em Abas Elegantes
tab_exp, tab_form, tab_comp, tab_cur_idi = st.tabs([
    "🏢 Experiência Profissional",
    "🎓 Formação Acadêmica",
    "⚡ Competências & Tecnologias",
    "📚 Cursos & Idiomas",
])

# ----------------- ABA 1: EXPERIÊNCIA PROFISSIONAL -----------------
with tab_exp:
  st.markdown("<br>", unsafe_allow_html=True)

  # Empresa 1: Ellenco
  st.markdown(
      """
    <div class="content-card">
        <div class="card-header-row">
            <div>
                <span class="role-title">Analista de Seguros</span>
                <span style="color: #94a3b8; margin: 0 0.4rem;">•</span>
                <span class="company-name">ELLENCO CONSTRUÇÕES LTDA</span>
            </div>
            <span class="period-badge">Jan/2025 – Atual</span>
        </div>
        <p style="color: #475569; font-size: 0.94rem; margin-bottom: 0.8rem; font-weight: 500;">
            Responsável pela gestão da carteira corporativa de seguros da companhia, conduzindo processos de contratação, renovação, análise técnica, negociação e gestão de riscos.
        </p>
        <ul style="color: #334155; font-size: 0.92rem; line-height: 1.75; padding-left: 1.3rem; margin: 0;">
            <li><b>Administração de cerca de 100 apólices ativas:</b> Programas de Property, RC Geral, RC Obras, D&O, Frota, Equipamentos, Riscos de Engenharia e Garantias.</li>
            <li><b>Negociação e Otimização de Custos:</b> Relacionamento direto com aprox. 10 corretoras e mais de 30 seguradoras, gerando economia aproximada de <b>R$ 380 mil</b> em renovações e negociações.</li>
            <li><b>Governança e Editais:</b> Gestão de riscos contratuais, compliance securitário e análise técnica de <b>77 editais e 257 cotações</b> no último ano (média de 6 licitações/mês).</li>
            <li><b>Estruturação Operacional:</b> Implantação do processo estruturado de gestão de sinistros da empresa.</li>
            <li><b>Interface Executiva:</b> Atuação direta com Diretoria, Jurídico, Engenharia, Financeiro e Operações no suporte à tomada de decisão.</li>
        </ul>
    </div>
    """,
      unsafe_allow_html=True,
  )

  # Empresa 2: Brasilseg
  st.markdown(
      """
    <div class="content-card">
        <div class="card-header-row">
            <div>
                <span class="role-title">Analista de Sinistros Pleno</span>
                <span style="color: #94a3b8; margin: 0 0.4rem;">•</span>
                <span class="company-name">BRASILSEG</span>
            </div>
            <span class="period-badge">Jan/2018 – Nov/2024</span>
        </div>
        <ul style="color: #334155; font-size: 0.92rem; line-height: 1.75; padding-left: 1.3rem; margin: 0;">
            <li><b>Volume Analítico:</b> Análise média de aproximadamente 200 processos de sinistro por mês, sendo referência técnica em ramos habitacionais.</li>
            <li><b>Capacitação & Processos:</b> Treinamento e orientação técnica de reguladores e liderança no projeto de revisão das cartas de negativa de sinistros.</li>
            <li><b>Melhoria de Produtos:</b> Atuação multidisciplinar com áreas de Produto, Subscrição, Jurídico, Ouvidoria e Rede Comercial no desenvolvimento de estudos técnicos para mitigação de perdas.</li>
            <li><b>Controle e Indicadores:</b> Gestão de indicadores operacionais e acompanhamento contínuo de projetos.</li>
        </ul>
    </div>
    """,
      unsafe_allow_html=True,
  )

  # Empresa 3: Mapfre
  st.markdown(
      """
    <div class="content-card">
        <div class="card-header-row">
            <div>
                <span class="role-title">Analista de Sinistros Jr</span>
                <span style="color: #94a3b8; margin: 0 0.4rem;">•</span>
                <span class="company-name">GRUPO SEGURADOR BANCO DO BRASIL MAPFRE</span>
            </div>
            <span class="period-badge">Set/2015 – Dez/2017</span>
        </div>
        <ul style="color: #334155; font-size: 0.92rem; line-height: 1.75; padding-left: 1.3rem; margin: 0;">
            <li>Análise técnica de cobertura securitária, gestão de indicadores de desempenho e monitoramento rigoroso de SLAs.</li>
            <li>Priorização operacional e participação em iniciativas voltadas à melhoria contínua dos processos de regulação.</li>
        </ul>
        <hr style="border: 0; border-top: 1px solid #f1f5f9; margin: 1.1rem 0 0.9rem 0;">
        <div class="card-header-row">
            <div>
                <span class="role-title">Analista de Obras e Layout Jr</span>
                <span style="color: #94a3b8; margin: 0 0.4rem;">•</span>
                <span class="company-name">GRUPO SEGURADOR BANCO DO BRASIL MAPFRE</span>
            </div>
            <span class="period-badge">Abr/2012 – Ago/2015</span>
        </div>
        <ul style="color: #334155; font-size: 0.92rem; line-height: 1.75; padding-left: 1.3rem; margin: 0;">
            <li>Coordenação de fornecedores e equipes de obras civis; gestão de orçamento, cronograma físico-financeiro e infraestrutura predial.</li>
            <li>Implantação de unidades corporativas em âmbito nacional, planejamento de mudanças corporativas e gestão de contratos.</li>
        </ul>
    </div>
    """,
      unsafe_allow_html=True,
  )

# ----------------- ABA 2: FORMAÇÃO ACADÊMICA -----------------
with tab_form:
  st.markdown("<br>", unsafe_allow_html=True)
  col_f1, col_f2, col_f3 = st.columns(3)

  with col_f1:
    st.markdown(
        """
        <div class="content-card" style="height: 100%;">
            <div style="font-size: 1.6rem; margin-bottom: 0.5rem;">🎓</div>
            <div class="role-title">MBA em Gestão de Projetos</div>
            <div class="company-name" style="margin: 0.3rem 0;">USP / ESALQ</div>
            <span class="period-badge">Conclusão: 2023</span>
            <p style="color: #64748b; font-size: 0.88rem; margin-top: 0.8rem;">
                Foco em planejamento estratégico, metodologias preditivas e ágeis, mitigação de riscos e governança de projetos corporativos.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

  with col_f2:
    st.markdown(
        """
        <div class="content-card" style="height: 100%;">
            <div style="font-size: 1.6rem; margin-bottom: 0.5rem;">📐</div>
            <div class="role-title">Bacharelado em Engenharia Civil</div>
            <div class="company-name" style="margin: 0.3rem 0;">Universidade Mogi das Cruzes</div>
            <span class="period-badge">Conclusão: 2015</span>
            <p style="color: #64748b; font-size: 0.88rem; margin-top: 0.8rem;">
                Base técnica sólida para avaliação pericial, análise de sinistros de engenharia, infraestrutura e riscos estruturais.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

  with col_f3:
    st.markdown(
        """
        <div class="content-card" style="height: 100%;">
            <div style="font-size: 1.6rem; margin-bottom: 0.5rem;">🏗️</div>
            <div class="role-title">Tecnologia em Construção Civil</div>
            <div class="company-name" style="margin: 0.3rem 0;">FATEC SP</div>
            <span class="period-badge">Conclusão: 2012</span>
            <p style="color: #64748b; font-size: 0.88rem; margin-top: 0.8rem;">
                Formação com ênfase em processos construtivos, orçamento, cronograma e acompanhamento operacional de obras.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ----------------- ABA 3: COMPETÊNCIAS & TECNOLOGIAS -----------------
with tab_comp:
  st.markdown("<br>", unsafe_allow_html=True)
  col_c1, col_c2 = st.columns(2)

  with col_c1:
    st.markdown(
        """
        <div class="content-card">
            <div style="font-weight: 700; color: #0f172a; font-size: 1.05rem; margin-bottom: 0.8rem;">
                🛡️ Seguros & Gestão de Riscos (Core Expertise)
            </div>
            <div>
        """,
        unsafe_allow_html=True,
    )
    tech_skills = [
        "Corporate Insurance",
        "Risk Management",
        "Property",
        "Seguro Garantia",
        "Responsabilidade Civil",
        "Riscos de Engenharia",
        "Claims Management",
        "Gestão de Sinistros",
        "Gestão de Apólices",
        "Governança Securitária",
        "Análise Contratual",
        "Insurance Placement",
        "Broker Management",
        "Renovações (Renewals)",
        "Policy Administration",
    ]
    badge_html = "".join(
        [f'<span class="tag-pill tag-blue">{s}</span>' for s in tech_skills]
    )
    st.markdown(badge_html + "</div></div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="content-card">
            <div style="font-weight: 700; color: #0f172a; font-size: 1.05rem; margin-bottom: 0.8rem;">
                🎯 Metodologias & Práticas de Gestão
            </div>
            <div>
        """,
        unsafe_allow_html=True,
    )
    methods = [
        "Scrum",
        "Kanban",
        "Agile",
        "Melhoria Contínua",
        "Gestão de Projetos",
        "Lean Six Sigma",
    ]
    badge_m = "".join(
        [f'<span class="tag-pill tag-purple">{m}</span>' for m in methods]
    )
    st.markdown(badge_m + "</div></div>", unsafe_allow_html=True)

  with col_c2:
    st.markdown(
        """
        <div class="content-card">
            <div style="font-weight: 700; color: #0f172a; font-size: 1.05rem; margin-bottom: 0.8rem;">
                💻 Ferramentas & Análise de Dados
            </div>
            <div>
        """,
        unsafe_allow_html=True,
    )
    tools = [
        "SAP",
        "Excel Avançado",
        "Access",
        "Power BI",
        "Python",
        "Streamlit",
        "Pandas",
        "AutoCAD",
        "MS Project",
        "Word",
        "PowerPoint",
    ]
    badge_t = "".join(
        [f'<span class="tag-pill tag-emerald">{t}</span>' for t in tools]
    )
    st.markdown(badge_t + "</div></div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="content-card">
            <div style="font-weight: 700; color: #0f172a; font-size: 1.05rem; margin-bottom: 0.8rem;">
                🤝 Competências Comportamentais
            </div>
            <div>
        """,
        unsafe_allow_html=True,
    )
    soft_skills = [
        "Pensamento Analítico",
        "Negociação Estratégica",
        "Gestão de Stakeholders",
        "Resolução de Problemas",
        "Tomada de Decisão",
        "Gestão de Mudanças",
        "Influência Técnica",
        "Planejamento e Organização",
    ]
    badge_s = "".join(
        [f'<span class="tag-pill tag-slate">{s}</span>' for s in soft_skills]
    )
    st.markdown(badge_s + "</div></div>", unsafe_allow_html=True)

# ----------------- ABA 4: CURSOS & IDIOMAS -----------------
with tab_cur_idi:
  st.markdown("<br>", unsafe_allow_html=True)
  col_cur, col_idi = st.columns([1.2, 1])

  with col_cur:
    st.markdown(
        """
        <div class="content-card">
            <div style="font-weight: 700; color: #0f172a; font-size: 1.1rem; margin-bottom: 1rem;">
                📜 Certificações & Cursos Complementares
            </div>
            <ul style="color: #334155; font-size: 0.95rem; line-height: 2; padding-left: 1.3rem; margin: 0;">
                <li><b>Yellow Belt Lean</b> – Otimização de processos e eliminação de desperdícios</li>
                <li><b>Gerenciamento de Obras</b> – Controle de escopo, custo e prazos</li>
                <li><b>Orçamento de Obras</b> – Levantamento quantitativo e estimativas</li>
                <li><b>Acessibilidade</b> – Normas técnicas e conformidade predial</li>
                <li><b>Sustentabilidade</b> – Eficiência e boas práticas corporativas</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

  with col_idi:
    st.markdown(
        """
        <div class="content-card">
            <div style="font-weight: 700; color: #0f172a; font-size: 1.1rem; margin-bottom: 1rem;">
                🌐 Idiomas
            </div>
            <div style="margin-bottom: 1rem;">
                <div style="font-weight: 600; color: #0f172a; font-size: 0.95rem;">🇬🇧 Inglês</div>
                <div style="color: #475569; font-size: 0.88rem; margin-top: 0.2rem;">
                    Nível <b>Intermediário</b> voltado para leitura técnica e escrita. Conversação em desenvolvimento ativo.
                </div>
            </div>
            <div>
                <div style="font-weight: 600; color: #0f172a; font-size: 0.95rem;">🇧🇷 Português</div>
                <div style="color: #475569; font-size: 0.88rem; margin-top: 0.2rem;">
                    Nativo / Fluente.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
