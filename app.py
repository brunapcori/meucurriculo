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

    /* Cards Estruturados */
    .content-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 1.5rem 1.6rem;
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
        gap: 0.5rem;
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


def extract_pdf_lines(pdf_path):
  all_lines = []
  try:
    with pdfplumber.open(pdf_path) as pdf:
      for page in pdf.pages:
        text = page.extract_text()
        if text:
          for line in text.splitlines():
            cleaned = line.strip()
            if cleaned:
              all_lines.append(cleaned)
  except Exception:
    return []
  return all_lines


def parse_pdf_resume(lines):
  """Segmenta dinamicamente as seções do PDF para preencher abas e cards automaticamente."""
  data = {
      "nome": "Bruna Prado Coriolano",
      "subtitulo": (
          "SEGUROS | SINISTROS | GESTÃO DE RISCOS | CORPORATE INSURANCE"
      ),
      "resumo": "",
      "experiencias": [],
      "formacoes": [],
      "competencias_tecnicas": [],
      "ferramentas": [],
      "metodologias": [],
      "competencias_comportamentais": [],
      "cursos": [],
      "idiomas": [],
  }

  if not lines:
    return data

  current_section = "topo"
  buffer = {
      "topo": [],
      "resumo": [],
      "competencias": [],
      "experiencias": [],
      "formacao": [],
      "cursos": [],
      "idiomas": [],
      "ferramentas": [],
      "metodologias": [],
      "comportamentais": [],
  }

  header_patterns = [
      (r"(?i)^resumo(\s+profissional)?$", "resumo"),
      (r"(?i)^compet[êe]ncias\s+t[ée]cnicas$", "competencias"),
      (r"(?i)^experi[êe]ncia(\s+profissional)?$", "experiencias"),
      (r"(?i)^forma[çc][ãa]o(\s+acad[êe]mica)?$", "formacao"),
      (r"(?i)^cursos?(\s+complementares)?$", "cursos"),
      (r"(?i)^idiomas?$", "idiomas"),
      (r"(?i)^ferramentas?$", "ferramentas"),
      (r"(?i)^metodologias?$", "metodologias"),
      (r"(?i)^compet[êe]ncias\s+comportamentais$", "comportamentais"),
  ]

  for line in lines:
    matched = False
    for pat, sec_name in header_patterns:
      if re.match(pat, line):
        current_section = sec_name
        matched = True
        break
    if not matched:
      buffer[current_section].append(line)

  # Resumo
  if buffer["resumo"]:
    data["resumo"] = " ".join(buffer["resumo"])

  # Competências Técnicas
  if buffer["competencias"]:
    items = []
    for l in buffer["competencias"]:
      for item in re.split(r"[/•|,;]", l):
        it = item.strip()
        if it:
          items.append(it)
    data["competencias_tecnicas"] = items

  # Ferramentas
  if buffer["ferramentas"]:
    items = []
    for l in buffer["ferramentas"]:
      for item in re.split(r"[/•\-|,;]", l):
        it = item.strip()
        if it:
          items.append(it)
    data["ferramentas"] = items

  # Metodologias
  if buffer["metodologias"]:
    items = []
    for l in buffer["metodologias"]:
      for item in re.split(r"[/•\-|,;]", l):
        it = item.strip()
        if it:
          items.append(it)
    data["metodologias"] = items

  # Comportamentais
  if buffer["comportamentais"]:
    items = []
    for l in buffer["comportamentais"]:
      for item in re.split(r"[/•|,;]", l):
        it = item.strip()
        if it:
          items.append(it)
    data["competencias_comportamentais"] = items

  # Experiências
  exp_lines = buffer["experiencias"]
  if exp_lines:
    current_exp = None
    date_pattern = r"(?i)^(jan|fev|mar|abr|mai|jun|jul|ago|set|out|nov|dez|\d{2}/\d{4}|\d{4})"

    for l in exp_lines:
      if re.search(date_pattern, l) or (
          "|" in l and not l.startswith("-") and not l.startswith("•")
      ):
        if current_exp:
          data["experiencias"].append(current_exp)

        period = ""
        headline = l
        date_match = re.search(
            r"(?i)((jan|fev|mar|abr|mai|jun|jul|ago|set|out|nov|dez|\d{4})[^\-|•\n]*[\-–][^\n]+)",
            l,
        )
        if date_match and len(date_match.group(1)) < 35:
          period = date_match.group(1).strip()
          headline = l.replace(period, "").strip(" -|")

        current_exp = {
            "header": headline if headline else l,
            "period": period,
            "desc": [],
            "bullets": [],
        }
      elif current_exp:
        if (
            l.startswith("-")
            or l.startswith("•")
            or l.startswith("*")
            or l.startswith(".")
        ):
          clean_b = re.sub(r"^[\-•\*\.]\s*", "", l)
          current_exp["bullets"].append(clean_b)
        else:
          current_exp["desc"].append(l)
      else:
        current_exp = {"header": l, "period": "", "desc": [], "bullets": []}

    if current_exp:
      data["experiencias"].append(current_exp)

  # Formações
  form_lines = buffer["formacao"]
  if form_lines:
    i = 0
    while i < len(form_lines):
      title = form_lines[i]
      inst = (
          form_lines[i + 1]
          if i + 1 < len(form_lines) and not re.match(r"^\d{4}$", form_lines[i + 1])
          else ""
      )
      year = ""

      offset = 2 if inst else 1
      if i + offset < len(form_lines) and re.match(
          r"^\d{4}$", form_lines[i + offset]
      ):
        year = form_lines[i + offset]
        i += offset + 1
      elif inst and re.match(r"^\d{4}$", form_lines[i + 1]):
        year = form_lines[i + 1]
        inst = ""
        i += 2
      else:
        i += 2 if inst else 1

      data["formacoes"].append(
          {"titulo": title, "instituicao": inst, "ano": year}
      )

  # Cursos
  if buffer["cursos"]:
    data["cursos"] = [
        re.sub(r"^[\-•\*\.]\s*", "", c) for c in buffer["cursos"]
    ]

  # Idiomas
  if buffer["idiomas"]:
    data["idiomas"] = buffer["idiomas"]

  return data


pdf_path = get_latest_pdf()
photo_path = find_profile_photo()
pdf_lines = extract_pdf_lines(pdf_path) if pdf_path else []
cv = parse_pdf_resume(pdf_lines)

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
    st.info("Suba seu PDF para ativar o download.")

# Área Principal - Hero Banner
st.markdown(
    f"""
<div class="hero-card">
    <div class="hero-title">{cv["nome"]}</div>
    <div class="hero-subtitle">{cv["subtitulo"]}</div>
    <div class="hero-bio">
        {cv["resumo"] if cv["resumo"] else "Mais de 10 anos de sólida trajetória no mercado segurador, com atuação destacada em grandes seguradoras e na gestão direta no segurado corporativo."}
    </div>
</div>
""",
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
        """
        <div style="background: #ffffff; border: 2px dashed #cbd5e1; border-radius: 12px; padding: 2.5rem; text-align: center; color: #64748b;">
            <p style="font-size: 1.8rem; margin: 0;">🎬</p>
            <p style="font-weight: 600; margin: 0.5rem 0 0 0;">Espaço Reservado para Pitch Pessoal</p>
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

# Abas Dinâmicas
tab_exp, tab_form, tab_comp, tab_cur_idi = st.tabs([
    "🏢 Experiência Profissional",
    "🎓 Formação Acadêmica",
    "⚡ Competências & Tecnologias",
    "📚 Cursos & Idiomas",
])

# ----------------- ABA 1: EXPERIÊNCIA PROFISSIONAL (Dinâmico) -----------------
with tab_exp:
  st.markdown("<br>", unsafe_allow_html=True)
  if cv["experiencias"]:
    for exp in cv["experiencias"]:
      header_display = exp["header"]
      period_badge = (
          f'<span class="period-badge">{exp["period"]}</span>'
          if exp["period"]
          else ""
      )

      bullets_html = ""
      if exp["bullets"]:
        bullets_html = (
            "<ul style='color: #334155; font-size: 0.92rem; line-height: 1.75;"
            " padding-left: 1.3rem; margin: 0.5rem 0 0 0;'>"
        )
        for b in exp["bullets"]:
          bullets_html += f"<li>{b}</li>"
        bullets_html += "</ul>"

      desc_html = ""
      if exp["desc"]:
        desc_html = (
            "<p style='color: #475569; font-size: 0.93rem; margin-bottom:"
            " 0.6rem; font-weight: 500;'>{' '.join(exp['desc'])}</p>"
        )

      st.markdown(
          f"""
            <div class="content-card">
                <div class="card-header-row">
                    <span class="role-title">{header_display}</span>
                    {period_badge}
                </div>
                {desc_html}
                {bullets_html}
            </div>
            """,
          unsafe_allow_html=True,
      )
  else:
    st.info("Nenhuma experiência profissional detectada no arquivo PDF atual.")

# ----------------- ABA 2: FORMAÇÃO ACADÊMICA (Dinâmico) -----------------
with tab_form:
  st.markdown("<br>", unsafe_allow_html=True)
  if cv["formacoes"]:
    cols = st.columns(min(len(cv["formacoes"]), 3))
    for idx, form in enumerate(cv["formacoes"]):
      col_target = cols[idx % len(cols)]
      with col_target:
        year_badge = (
            f'<span class="period-badge">Conclusão: {form["ano"]}</span>'
            if form["ano"]
            else ""
        )
        inst_text = (
            '<div class="company-name" style="margin: 0.3rem'
            f' 0;">{form["instituicao"]}</div>'
            if form["instituicao"]
            else ""
        )

        st.markdown(
            f"""
                <div class="content-card" style="height: 100%;">
                    <div style="font-size: 1.6rem; margin-bottom: 0.5rem;">🎓</div>
                    <div class="role-title">{form["titulo"]}</div>
                    {inst_text}
                    {year_badge}
                </div>
                """,
            unsafe_allow_html=True,
        )
  else:
    st.info("Nenhuma formação acadêmica detectada no arquivo PDF atual.")

# ----------------- ABA 3: COMPETÊNCIAS & TECNOLOGIAS (Dinâmico) -----------------
with tab_comp:
  st.markdown("<br>", unsafe_allow_html=True)
  col_c1, col_c2 = st.columns(2)

  with col_c1:
    if cv["competencias_tecnicas"]:
      badges = "".join([
          f'<span class="tag-pill tag-blue">{s}</span>'
          for s in cv["competencias_tecnicas"]
      ])
      st.markdown(
          f"""
            <div class="content-card">
                <div style="font-weight: 700; color: #0f172a; font-size: 1.05rem; margin-bottom: 0.8rem;">
                    🛡️ Seguros & Gestão de Riscos (Core Expertise)
                </div>
                <div>{badges}</div>
            </div>
            """,
          unsafe_allow_html=True,
      )

    if cv["metodologias"]:
      badges_m = "".join([
          f'<span class="tag-pill tag-purple">{m}</span>'
          for m in cv["metodologias"]
      ])
      st.markdown(
          f"""
            <div class="content-card">
                <div style="font-weight: 700; color: #0f172a; font-size: 1.05rem; margin-bottom: 0.8rem;">
                    🎯 Metodologias & Práticas de Gestão
                </div>
                <div>{badges_m}</div>
            </div>
            """,
          unsafe_allow_html=True,
      )

  with col_c2:
    if cv["ferramentas"]:
      badges_t = "".join([
          f'<span class="tag-pill tag-emerald">{t}</span>'
          for t in cv["ferramentas"]
      ])
      st.markdown(
          f"""
            <div class="content-card">
                <div style="font-weight: 700; color: #0f172a; font-size: 1.05rem; margin-bottom: 0.8rem;">
                    💻 Ferramentas & Análise de Dados
                </div>
                <div>{badges_t}</div>
            </div>
            """,
          unsafe_allow_html=True,
      )

    if cv["competencias_comportamentais"]:
      badges_s = "".join([
          f'<span class="tag-pill tag-slate">{s}</span>'
          for s in cv["competencias_comportamentais"]
      ])
      st.markdown(
          f"""
            <div class="content-card">
                <div style="font-weight: 700; color: #0f172a; font-size: 1.05rem; margin-bottom: 0.8rem;">
                    🤝 Competências Comportamentais
                </div>
                <div>{badges_s}</div>
            </div>
            """,
          unsafe_allow_html=True,
      )

# ----------------- ABA 4: CURSOS & IDIOMAS (Dinâmico) -----------------
with tab_cur_idi:
  st.markdown("<br>", unsafe_allow_html=True)
  col_cur, col_idi = st.columns([1.2, 1])

  with col_cur:
    if cv["cursos"]:
      items_c = "".join([f"<li><b>{c}</b></li>" for c in cv["cursos"]])
      st.markdown(
          f"""
            <div class="content-card">
                <div style="font-weight: 700; color: #0f172a; font-size: 1.1rem; margin-bottom: 1rem;">
                    📜 Certificações & Cursos Complementares
                </div>
                <ul style="color: #334155; font-size: 0.95rem; line-height: 2; padding-left: 1.3rem; margin: 0;">
                    {items_c}
                </ul>
            </div>
            """,
          unsafe_allow_html=True,
      )
    else:
      st.info("Nenhum curso complementar listado.")

  with col_idi:
    if cv["idiomas"]:
      idiomas_html = ""
      for item in cv["idiomas"]:
        parts = item.split("-", 1)
        title = parts[0].strip()
        desc = parts[1].strip() if len(parts) > 1 else ""
        idiomas_html += f"""
                <div style="margin-bottom: 1rem;">
                    <div style="font-weight: 600; color: #0f172a; font-size: 0.95rem;">🌐 {title}</div>
                    <div style="color: #475569; font-size: 0.88rem; margin-top: 0.2rem;">{desc}</div>
                </div>
                """
      st.markdown(
          f"""
            <div class="content-card">
                <div style="font-weight: 700; color: #0f172a; font-size: 1.1rem; margin-bottom: 1rem;">
                    🌐 Idiomas
                </div>
                {idiomas_html}
            </div>
            """,
          unsafe_allow_html=True,
      )
    else:
      st.info("Nenhum idioma listado.")
