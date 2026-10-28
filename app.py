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
    """<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
}

.main {
    background-color: #f8fafc;
}

.hero-card {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
    border-radius: 18px;
    padding: 2.2rem 2.4rem;
    color: #ffffff;
    margin-bottom: 2rem;
    box-shadow: 0 12px 30px -10px rgba(15, 23, 42, 0.25);
    border: 1px solid rgba(255, 255, 255, 0.08);
}

.hero-title {
    font-size: 2.2rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: #ffffff;
    margin-bottom: 0.3rem;
}

.hero-subtitle {
    font-size: 1.1rem;
    color: #38bdf8;
    font-weight: 600;
    margin-bottom: 1rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

.hero-bio {
    font-size: 0.98rem;
    color: #cbd5e1;
    max-width: 980px;
    line-height: 1.7;
}

.content-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 1.6rem 1.8rem;
    margin-bottom: 1.4rem;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.03);
}

.card-header-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    flex-wrap: wrap;
    margin-bottom: 0.7rem;
    gap: 0.5rem;
}

.role-title {
    font-size: 1.18rem;
    font-weight: 700;
    color: #0f172a;
}

.company-name {
    font-size: 1.02rem;
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
</style>""",
    unsafe_allow_html=True,
)


def find_profile_photo():
  possible_names = [
      "imagem.png",
      "imagem.jpg",
      "imagem.jpeg",
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


def extract_pdf_full_text(pdf_path):
  text_content = ""
  try:
    with pdfplumber.open(pdf_path) as pdf:
      for page in pdf.pages:
        txt = page.extract_text()
        if txt:
          text_content += "\n" + txt
  except Exception:
    return ""
  return text_content


def parse_pdf_data(raw_text):
  data = {
      "resumo": "",
      "ellenco_bullets": [],
      "brasilseg_bullets": [],
      "mapfre_sinistros_bullets": [],
      "mapfre_obras_bullets": [],
      "competencias_tecnicas": [],
      "ferramentas": [],
      "metodologias": [],
      "comportamentais": [],
      "cursos": [],
      "idiomas": [],
  }

  if not raw_text.strip():
    return data

  lines = [l.strip() for l in raw_text.splitlines() if l.strip()]

  # 1. Resumo Profissional
  resumo_lines = []
  capture_resumo = False
  for l in lines:
    if re.search(r"(?i)^resumo(\s+profissional)?$", l):
      capture_resumo = True
      continue
    if capture_resumo:
      if re.search(r"(?i)^(compet[êe]ncias|experi[êe]ncia|forma[çc][ãa]o)", l):
        break
      resumo_lines.append(l)
  data["resumo"] = " ".join(resumo_lines)

  # 2. Experiências por Empresa
  current_company = None
  for l in lines:
    lower = l.lower()
    if "ellenco" in lower:
      current_company = "ellenco"
      continue
    elif "brasilseg" in lower:
      current_company = "brasilseg"
      continue
    elif "mapfre" in lower:
      current_company = "mapfre_sinistros"
      continue
    elif "analista de obras e layout" in lower:
      current_company = "mapfre_obras"
      continue
    elif re.search(
        r"(?i)^(forma[çc][ãa]o|cursos?|idiomas?|compet[êe]ncias)", l
    ):
      current_company = None

    if current_company and (
        l.startswith("-")
        or l.startswith("•")
        or l.startswith("*")
        or l.startswith(".")
    ):
      bullet = re.sub(r"^[\-•\*\.]\s*", "", l).strip()
      if bullet:
        if current_company == "ellenco":
          data["ellenco_bullets"].append(bullet)
        elif current_company == "brasilseg":
          data["brasilseg_bullets"].append(bullet)
        elif current_company == "mapfre_sinistros":
          data["mapfre_sinistros_bullets"].append(bullet)
        elif current_company == "mapfre_obras":
          data["mapfre_obras_bullets"].append(bullet)

  # 3. Competências Técnicas
  comp_lines = []
  capture_comp = False
  for l in lines:
    if re.search(r"(?i)^compet[êe]ncias\s+t[ée]cnicas$", l):
      capture_comp = True
      continue
    if capture_comp:
      if re.search(r"(?i)^(experi[êe]ncia|forma[çc][ãa]o|cursos|idiomas)", l):
        break
      comp_lines.append(l)

  for l in comp_lines:
    for item in re.split(r"[/•|,;]", l):
      it = item.strip()
      if it and len(it) > 1:
        data["competencias_tecnicas"].append(it)

  # 4. Ferramentas, Metodologias e Comportamentais
  for l in lines:
    if re.search(r"(?i)^ferramentas\b", l):
      parts = re.split(
          r"[:\-–|,/]", re.sub(r"(?i)^ferramentas\s*[:\-–]?\s*", "", l)
      )
      data["ferramentas"] = [p.strip() for p in parts if p.strip()]
    if re.search(r"(?i)^metodologias\b", l):
      parts = re.split(
          r"[:\-–|,/]", re.sub(r"(?i)^metodologias\s*[:\-–]?\s*", "", l)
      )
      data["metodologias"] = [p.strip() for p in parts if p.strip()]
    if re.search(r"(?i)^compet[êe]ncias\s+comportamentais\b", l):
      parts = re.split(
          r"[:\-–|,/]",
          re.sub(r"(?i)^compet[êe]ncias\s+comportamentais\s*[:\-–]?\s*", "", l),
      )
      data["comportamentais"] = [p.strip() for p in parts if p.strip()]

  # 5. Cursos
  capture_cursos = False
  for l in lines:
    if re.search(r"(?i)^cursos?(\s+complementares)?$", l):
      capture_cursos = True
      continue
    if capture_cursos:
      if re.search(
          r"(?i)^(idiomas?|ferramentas?|metodologias?|compet[êe]ncias?)", l
      ):
        break
      c = re.sub(r"^[\-•\*\.]\s*", "", l).strip()
      if c:
        data["cursos"].append(c)

  # 6. Idiomas
  for l in lines:
    if re.search(r"(?i)^ingl[êe]s\b", l):
      data["idiomas"].append(l)

  return data


pdf_path = get_latest_pdf()
photo_path = find_profile_photo()
pdf_text = extract_pdf_full_text(pdf_path) if pdf_path else ""
cv = parse_pdf_data(pdf_text)

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
      """<a class="contact-button" href="https://www.linkedin.com/in/brunapcoriolano/" target="_blank">
        <svg width="18" height="18" fill="#0a66c2" viewBox="0 0 24 24"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/></svg>
        Perfil no LinkedIn
    </a>
    <a class="contact-button" href="mailto:brunapcoriolano@gmail.com">
        <svg width="18" height="18" fill="#e11d48" viewBox="0 0 24 24"><path d="M12 12.713l-11.985-8.713h23.97l-11.985 8.713zm0 2.574l-12-8.725v13.438h24v-13.438l-12 8.725z"/></svg>
        brunapcoriolano@gmail.com
    </a>""",
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
    st.info("Suba seu PDF para ativar o download.")

# Área Principal - Hero Banner
resumo_exibicao = (
    cv["resumo"]
    if cv["resumo"]
    else (
        "Engenheira Civil com MBA em Gestão de Projetos e mais de 10 anos de"
        " sólida trajetória no mercado segurador, com atuação destacada em"
        " grandes seguradoras e na gestão direta no segurado corporativo."
        " Experiência de ponta em mitigação de riscos, governança securitária,"
        " análise e regulação de sinistros e desenvolvimento de soluções"
        " digitais orientadas à eficiência e dados."
    )
)

st.markdown(
    f"""<div class="hero-card">
    <div class="hero-title">Bruna Prado Coriolano</div>
    <div class="hero-subtitle">SEGUROS | SINISTROS | GESTÃO DE RISCOS | CORPORATE INSURANCE</div>
    <div class="hero-bio">{resumo_exibicao}</div>
</div>""",
    unsafe_allow_html=True,
)

# Apresentação em Vídeo
st.markdown("### 🎥 Vídeo de Apresentação")
col_vid, col_vid_txt = st.columns([1.5, 1], gap="medium")

video_source = "https://youtu.be/oItvfiUpsO4?is=BPv046PG3ejMbH0i"

with col_vid:
  if video_source:
    try:
      st.video(video_source)
    except Exception:
      st.warning("Não foi possível carregar o vídeo.")
  else:
    st.markdown(
        """<div style="background: #ffffff; border: 2px dashed #cbd5e1; border-radius: 12px; padding: 2.5rem; text-align: center; color: #64748b;">
            <p style="font-size: 1.8rem; margin: 0;">🎬</p>
            <p style="font-weight: 600; margin: 0.5rem 0 0 0;">Espaço Reservado para Pitch Pessoal</p>
        </div>""",
        unsafe_allow_html=True,
    )

with col_vid_txt:
  st.markdown(
      """<div class="content-card" style="margin-bottom:0; height: 100%;">
        <div style="font-weight: 700; color: #0f172a; margin-bottom: 0.5rem; font-size: 1rem;">💼 Proposta de Valor</div>
        <ul style="color: #475569; font-size: 0.92rem; line-height: 1.7; padding-left: 1.2rem; margin: 0;">
            <li>Domínio completo de <b>Property, RC, Obras, Garantia e D&O</b>.</li>
            <li>Histórico comprovado em <b>redução de custos</b> em renovações e negociações.</li>
            <li>Interface estratégica entre <b>Diretoria, Jurídico, Engenharia e Operações</b>.</li>
            <li>Inovação aplicada a sinistros com <b>IA e automação analítica</b>.</li>
        </ul>
    </div>""",
      unsafe_allow_html=True,
  )

st.markdown("<br>", unsafe_allow_html=True)

# Abas Principais
tab_exp, tab_form, tab_comp, tab_cur_idi = st.tabs([
    "🏢 Experiência Profissional",
    "🎓 Formação Acadêmica",
    "⚡ Competências & Tecnologias",
    "📚 Cursos & Idiomas",
])

# ----------------- ABA 1: EXPERIÊNCIA PROFISSIONAL -----------------
with tab_exp:
  st.markdown("<br>", unsafe_allow_html=True)

  # 1. ELLENCO
  ellenco_items = (
      cv["ellenco_bullets"]
      if cv["ellenco_bullets"]
      else [
          (
              "Responsável pela gestão da carteira corporativa de seguros da"
              " companhia, conduzindo processos de contratação, renovação,"
              " análise técnica, negociação e gestão de riscos."
          ),
          "Administração de aproximadamente 100 apólices ativas.",
          (
              "Gestão de programas envolvendo Property, RC Geral, RC Obras, D&O,"
              " Frota, Equipamentos, Riscos de Engenharia e Garantias."
          ),
          (
              "Negociação com aproximadamente 22 corretoras e mais de 30"
              " Seguradoras."
          ),
          (
              "Economia aproximada de R$ 476 mil em renovações e negociações em"
              " 2026."
          ),
          (
              "Economia aproximada de R$ 380 mil em renovações e negociações em"
              " 2025."
          ),
          (
              "Gestão de riscos contratuais, compliance securitário e"
              " governança das apólices corporativas."
          ),
          (
              "Análise técnica de aproximadamente 77 editais e 257 cotações no"
              " último ano."
          ),
          "Análise mensal de cerca de seis licitações públicas.",
          (
              "Implantação do processo estruturado de gestão de sinistros da"
              " empresa."
          ),
          (
              "Interface direta com Diretoria, Jurídico, Engenharia, Financeiro"
              " e Operações para suporte à tomada de decisão."
          ),
      ]
  )
  ellenco_li = "".join([f"<li>{b}</li>" for b in ellenco_items])
  st.markdown(
      f"""<div class="content-card">
        <div class="card-header-row">
            <div>
                <span class="role-title">Analista de Seguros</span>
                <span style="color: #94a3b8; margin: 0 0.4rem;">•</span>
                <span class="company-name">ELLENCO CONSTRUÇÕES LTDA</span>
            </div>
            <span class="period-badge">Jan/2025 – Atual</span>
        </div>
        <ul style="color: #334155; font-size: 0.92rem; line-height: 1.75; padding-left: 1.3rem; margin: 0.5rem 0 0 0;">
            {ellenco_li}
        </ul>
    </div>""",
      unsafe_allow_html=True,
  )

  # 2. BRASILSEG
  brasilseg_items = (
      cv["brasilseg_bullets"]
      if cv["brasilseg_bullets"]
      else [
          (
              "Análise média de aproximadamente 200 processos de sinistro por"
              " mês."
          ),
          "Referência técnica em sinistros habitacionais.",
          "Treinamento e orientação técnica de reguladores.",
          (
              "Liderança do projeto de revisão das cartas de negativa de"
              " sinistros."
          ),
          (
              "Atuação junto às áreas de Produto, Subscrição, Jurídico,"
              " Ouvidoria e Rede Comercial."
          ),
          (
              "Desenvolvimento de estudos técnicos para melhoria de produtos e"
              " oportunidades de mitigação de perdas."
          ),
          (
              "Gestão de indicadores operacionais e acompanhamento contínuo de"
              " projetos."
          ),
          (
              "Envolvimento em grandes sinistros como subsidência em Maceió"
              " devido extração do sal-gema pela Braskem e enchentes no Rio"
              " Grande do Sul."
          ),
          (
              "1º Lugar no projeto Inovalab com IA voltada ao sinistro,"
              " projetos de redução de ressarcimento e comunicação com"
              " segurados."
          ),
      ]
  )
  brasilseg_li = "".join([f"<li>{b}</li>" for b in brasilseg_items])
  st.markdown(
      f"""<div class="content-card">
        <div class="card-header-row">
            <div>
                <span class="role-title">Analista de Sinistros Pleno</span>
                <span style="color: #94a3b8; margin: 0 0.4rem;">•</span>
                <span class="company-name">BRASILSEG</span>
            </div>
            <span class="period-badge">Jan/2018 – Nov/2024</span>
        </div>
        <ul style="color: #334155; font-size: 0.92rem; line-height: 1.75; padding-left: 1.3rem; margin: 0.5rem 0 0 0;">
            {brasilseg_li}
        </ul>
    </div>""",
      unsafe_allow_html=True,
  )

  # 3. GRUPO SEGURADOR BANCO DO BRASIL MAPFRE
  mapfre_sinistros = (
      cv["mapfre_sinistros_bullets"]
      if cv["mapfre_sinistros_bullets"]
      else [
          "Análise técnica de cobertura.",
          "Gestão de indicadores e monitoramento rigoroso de SLA.",
          (
              "Priorização operacional e participação em projetos de melhoria"
              " contínua."
          ),
      ]
  )
  mapfre_obras = (
      cv["mapfre_obras_bullets"]
      if cv["mapfre_obras_bullets"]
      else [
          "Coordenação de fornecedores e equipes de obra.",
          (
              "Gestão de orçamento, cronograma físico-financeiro e"
              " infraestrutura predial."
          ),
          "Implantação de unidades corporativas em âmbito nacional.",
          (
              "Condução de reuniões de projetos, planejamento de mudanças"
              " corporativas e gestão de contratos."
          ),
      ]
  )
  sinistros_li = "".join([f"<li>{b}</li>" for b in mapfre_sinistros])
  obras_li = "".join([f"<li>{b}</li>" for b in mapfre_obras])

  st.markdown(
      f"""<div class="content-card">
        <div class="card-header-row">
            <div>
                <span class="role-title">Analista de Sinistros Jr</span>
                <span style="color: #94a3b8; margin: 0 0.4rem;">•</span>
                <span class="company-name">GRUPO SEGURADOR BANCO DO BRASIL MAPFRE</span>
            </div>
            <span class="period-badge">Set/2015 – Dez/2017</span>
        </div>
        <ul style="color: #334155; font-size: 0.92rem; line-height: 1.75; padding-left: 1.3rem; margin: 0.5rem 0 1rem 0;">
            {sinistros_li}
        </ul>
        <hr style="border: 0; border-top: 1px solid #f1f5f9; margin: 1.1rem 0 1rem 0;">
        <div class="card-header-row">
            <div>
                <span class="role-title">Analista de Obras e Layout Jr</span>
                <span style="color: #94a3b8; margin: 0 0.4rem;">•</span>
                <span class="company-name">GRUPO SEGURADOR BANCO DO BRASIL MAPFRE</span>
            </div>
            <span class="period-badge">Abr/2012 – Ago/2015</span>
        </div>
        <ul style="color: #334155; font-size: 0.92rem; line-height: 1.75; padding-left: 1.3rem; margin: 0.5rem 0 0 0;">
            {obras_li}
        </ul>
    </div>""",
      unsafe_allow_html=True,
  )

# ----------------- ABA 2: FORMAÇÃO ACADÊMICA -----------------
with tab_form:
  st.markdown("<br>", unsafe_allow_html=True)
  col_f1, col_f2, col_f3 = st.columns(3)

  with col_f1:
    st.markdown(
        """<div class="content-card" style="height: 100%;">
            <div style="font-size: 1.6rem; margin-bottom: 0.5rem;">🎓</div>
            <div class="role-title">MBA em Gestão de Projetos</div>
            <div style="color: #0284c7; font-weight: 600; margin: 0.3rem 0;">USP / ESALQ</div>
            <span class="period-badge">Conclusão: 2023</span>
            <p style="color: #64748b; font-size: 0.88rem; margin-top: 0.8rem;">
                Foco em planejamento estratégico, metodologias preditivas e ágeis, mitigação de riscos e governança corporativa.
            </p>
        </div>""",
        unsafe_allow_html=True,
    )

  with col_f2:
    st.markdown(
        """<div class="content-card" style="height: 100%;">
            <div style="font-size: 1.6rem; margin-bottom: 0.5rem;">📐</div>
            <div class="role-title">Bacharelado em Engenharia Civil</div>
            <div style="color: #0284c7; font-weight: 600; margin: 0.3rem 0;">Universidade Mogi das Cruzes</div>
            <span class="period-badge">Conclusão: 2015</span>
            <p style="color: #64748b; font-size: 0.88rem; margin-top: 0.8rem;">
                Base técnica sólida para avaliação pericial, análise de sinistros de engenharia, infraestrutura e riscos estruturais.
            </p>
        </div>""",
        unsafe_allow_html=True,
    )

  with col_f3:
    st.markdown(
        """<div class="content-card" style="height: 100%;">
            <div style="font-size: 1.6rem; margin-bottom: 0.5rem;">🏗️</div>
            <div class="role-title">Tecnologia em Construção Civil</div>
            <div style="color: #0284c7; font-weight: 600; margin: 0.3rem 0;">FATEC SP</div>
            <span class="period-badge">Conclusão: 2012</span>
            <p style="color: #64748b; font-size: 0.88rem; margin-top: 0.8rem;">
                Formação com ênfase em processos construtivos, orçamento, cronograma e acompanhamento operacional de obras.
            </p>
        </div>""",
        unsafe_allow_html=True,
    )

# ----------------- ABA 3: COMPETÊNCIAS & TECNOLOGIAS -----------------
with tab_comp:
  st.markdown("<br>", unsafe_allow_html=True)
  col_c1, col_c2 = st.columns(2)

  tech_skills = (
      cv["competencias_tecnicas"]
      if cv["competencias_tecnicas"]
      else [
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
  )
  methods = (
      cv["metodologias"]
      if cv["metodologias"]
      else [
          "Scrum",
          "Kanban",
          "Agile",
          "Melhoria Contínua",
          "Gestão de Projetos",
          "Lean Six Sigma",
      ]
  )
  tools = (
      cv["ferramentas"]
      if cv["ferramentas"]
      else [
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
  )
  soft = (
      cv["comportamentais"]
      if cv["comportamentais"]
      else [
          "Pensamento Analítico",
          "Negociação Estratégica",
          "Gestão de Stakeholders",
          "Resolução de Problemas",
          "Tomada de Decisão",
          "Gestão de Mudanças",
          "Influência Técnica",
          "Planejamento e Organização",
      ]
  )

  with col_c1:
    badges_tech = "".join(
        [f'<span class="tag-pill tag-blue">{s}</span>' for s in tech_skills]
    )
    st.markdown(
        f"""<div class="content-card">
            <div style="font-weight: 700; color: #0f172a; font-size: 1.05rem; margin-bottom: 0.8rem;">
                🛡️ Seguros & Gestão de Riscos (Core Expertise)
            </div>
            <div>{badges_tech}</div>
        </div>""",
        unsafe_allow_html=True,
    )

    badges_m = "".join(
        [f'<span class="tag-pill tag-purple">{m}</span>' for m in methods]
    )
    st.markdown(
        f"""<div class="content-card">
            <div style="font-weight: 700; color: #0f172a; font-size: 1.05rem; margin-bottom: 0.8rem;">
                🎯 Metodologias & Práticas de Gestão
            </div>
            <div>{badges_m}</div>
        </div>""",
        unsafe_allow_html=True,
    )

  with col_c2:
    badges_t = "".join(
        [f'<span class="tag-pill tag-emerald">{t}</span>' for t in tools]
    )
    st.markdown(
        f"""<div class="content-card">
            <div style="font-weight: 700; color: #0f172a; font-size: 1.05rem; margin-bottom: 0.8rem;">
                💻 Ferramentas & Análise de Dados
            </div>
            <div>{badges_t}</div>
        </div>""",
        unsafe_allow_html=True,
    )

    badges_s = "".join(
        [f'<span class="tag-pill tag-slate">{s}</span>' for s in soft]
    )
    st.markdown(
        f"""<div class="content-card">
            <div style="font-weight: 700; color: #0f172a; font-size: 1.05rem; margin-bottom: 0.8rem;">
                🤝 Competências Comportamentais
            </div>
            <div>{badges_s}</div>
        </div>""",
        unsafe_allow_html=True,
    )

# ----------------- ABA 4: CURSOS & IDIOMAS -----------------
with tab_cur_idi:
  st.markdown("<br>", unsafe_allow_html=True)
  col_cur, col_idi = st.columns([1.2, 1])

  cursos_items = (
      cv["cursos"]
      if cv["cursos"]
      else [
          (
              "Yellow Belt Lean – Otimização de processos e eliminação de"
              " desperdícios"
          ),
          "Gerenciamento de Obras – Controle de escopo, custo e prazos",
          "Orçamento de Obras – Levantamento quantitativo e estimativas",
          "Acessibilidade – Normas técnicas e conformidade predial",
          "Sustentabilidade – Eficiência e boas práticas corporativas",
      ]
  )
  cursos_li = "".join([f"<li><b>{c}</b></li>" for c in cursos_items])

  with col_cur:
    st.markdown(
        f"""<div class="content-card">
            <div style="font-weight: 700; color: #0f172a; font-size: 1.1rem; margin-bottom: 1rem;">
                📜 Certificações & Cursos Complementares
            </div>
            <ul style="color: #334155; font-size: 0.95rem; line-height: 2; padding-left: 1.3rem; margin: 0;">
                {cursos_li}
            </ul>
        </div>""",
        unsafe_allow_html=True,
    )

  with col_idi:
    st.markdown(
        """<div class="content-card">
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
        </div>""",
        unsafe_allow_html=True,
    )
