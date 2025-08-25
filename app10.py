
import streamlit as st
import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
import io

st.set_page_config(page_title="Avaliação ATM's - DOF", layout="wide")

st.title("🧠 Avaliação ATM's - DOF [Dor Orofacial]")

# ======================================================
# 📋 Dados do paciente
# ======================================================
st.header("📋 Dados do Paciente")
nome = st.text_input("Nome completo")
qp = st.text_area("Queixa Principal (Q.P.)")
tempo = st.text_input("Tempo de dor")
tipo_dor = st.radio("Tipo de dor", ["Aguda", "Crônica","Leve", "Moderada", "Severa"])
comorbidades = st.multiselect("Condições de saúde", ["Diabetes", "HAS", "Câncer", "Tumor", "Marca-passo", "Outros", "Nenhuma"])
cirurgias = st.text_area("Cirurgias realizadas")
tratamentos_previos = st.text_area("Tratamentos já realizados")

# ======================================================
# 🤕 Dor de cabeça - Migrânea
# ======================================================
st.header("🤕 Dor de Cabeça - Migrânea")
migranea = st.checkbox("Marque para avaliar sintomas de Migrânea")
sintomas_migranea = []
if migranea:
    sintomas_migranea = st.multiselect("Sintomas", [
        "Migrânea (Enxaqueca)","Unilateral", "Pulsada", "Sensibilidade ao cheiro", "Sensibilidade auditiva",
        "Aura presente", "Sensibilidade à claridade", "Náuseas", "Vômitos",
        "Precisa se trancar no quarto escuro"
    ])

# ======================================================
# 🤕 Dor de cabeça - Tensional
# ======================================================
st.header("🤕 Dor de Cabeça - Tensional")
tensional = st.checkbox("Marque para avaliar sintomas de Cefaleia Tensional")
sintomas_tensional = []
if tensional:
    sintomas_tensional = st.multiselect("Sintomas e músculos envolvidos", [
        "Tipo Tensional","MM trapézio", "MM temporal", "MM ECOM", "MM escalenos", "Dor leve/moderada",
        "Melhora com exercício", "Não se agrava com esforço físico", "Dor bilateral não pulsátil", "Outros MM"
    ])

# ======================================================
# 🦷 Bloco Único - Dor, Zumbido, Hábitos, Respiração, Postura, Movimento
# ======================================================
st.header("🦷 Dor, Zumbido e Hábitos Parafuncionais")
sintomas_dor = st.multiselect("Sintomas", ["ATM D", "ATM E", "Falar", "Mastigar", "Ouvido", "Bruxismo", "Briquismo"])
mastigacao = st.multiselect("Mastigação", ["D", "E"])
habitos = st.multiselect("Hábitos Parafuncionais", [
    "Apertar os dentes", "Roer unhas", "Apoiar mão ao dormir", "Uso de celular do lado sintomático",
    "Apoio mão no queixo", "Morder lábio", "Morder bochecha", "Mascar chiclete",
    "Apertamento durante atividade física", "Apertamento durante atividade profissional"
])
zumbido = st.radio("Zumbido", ["Sim", "Não"])
tensao_muscular = st.checkbox("Zumbido relacionado à tensão muscular (Masseter + Temporal)")

# 🌬️ Padrão respiratório
st.header("🌬️ Padrão Respiratório")
respiracao = st.radio("Respiração", ["Pela boca", "Pelo nariz"])
if respiracao == "Pela boca":
    st.warning("⚠️ Respiração bucal pode levar à hiperativação dos músculos ECOM e Escalenos.")

# 🧍 Postura e movimento funcional
st.header("🧍 Postura e Movimento Funcional")
postura = st.multiselect("Alterações posturais", ["Anteriorização da cabeça", "Hipercifose torácica"])
movimentos_cervicais = st.multiselect("Movimentos que exacerbam a dor", [
    "Flexão", "Extensão", "Inclinação D", "Inclinação E", "Rotação D", "Rotação E"
])
with st.expander("Ver Músculos Envolvidos"):
    st.write("ECOM, Escalenos, Pterigoideo lateral, Hióides supra e infra, digástricos e Platisma.")

# 📏 Amplitude de movimento
st.header("📏 Amplitude de Movimento")
abertura = st.radio("Abertura bucal", ["Hipomobilidade", "Hipermobilidade", "Normobilidade"])
lateral_d = st.slider("Lateralização Direita (cm)", 0.0, 3.0, 1.0)
lateral_e = st.slider("Lateralização Esquerda (cm)", 0.0, 3.0, 1.0)
lateralidade = st.radio("Classificação da lateralização", ["Hipomobilidade", "Normobilidade", "Hipermobilidade"])

amplitude = {}
for movimento in ["Flexão", "Extensão", "Inclinação D", "Inclinação E", "Rotação D", "Rotação E"]:
    valor = st.slider(f"{movimento} cervical (graus)", 0, 90, 45)
    amplitude[movimento] = valor

# ======================================================
# 📄 QUADRO RESUMO (RIGOROSAMENTE AJUSTADO)
# ======================================================
st.header("📋 Resumo da Avaliação")
st.subheader("Observações e Sintomas Coletados")

# Mapeia os tratamentos para cada sintoma/diagnóstico
tratamentos_map = {
    "Sintomas de Migrânea": [
        "Hábitos alimentares", "Evitar saída de sua rotina diária", "Sono reparador", 
        "Respiração", "Repouso", "Tratamento medicamentoso [crise]"
    ],
    "Sintomas de Cefaleia Tensional": [
        "Liberação miofascial", "Digitopressão (Trigger points)", "Pompage", 
        "Atividade física", "Alongamentos"
    ],
    "Sintomas de Dor ATM": [
        "Liberação miofascial", "Digitopressão (Trigger Points)",
        "Alongamento muscular", "Orientação para evitar hábitos parafuncionais",
        "Mobilização articular ATM (Maitland)"
    ],
    "Hábitos Parafuncionais": [
        "Orientação para evitar hábitos parafuncionais"
    ],
    "Respiração": [
        "Exercícios respiratórios + Encaminhamento Fonoaudiologia/Otorrino"
    ],
    "Postura": [
        "Exercícios posturais e mobilização articular (RPG, Pilates, Fisioterapia postural)"
    ],
    "Abertura Bucal": [
        "Mobilização articular ATM (Maitland)"
    ],
    "Classificação da Lateralização": [
        "Mobilização articular ATM (Maitland)"
    ],
    "Zumbido": [
        "Encaminhamento Otorrinolaringologia"
    ]
}

# Constrói a tabela com 3 colunas, incluindo o tratamento mapeado
resumo_data = [["Diagnóstico", "Sintomas", "Tratamento Sugerido"]]

resumo_data.append(["Sintomas de Migrânea", ", ".join(sintomas_migranea) if migranea else "Não avaliado", ", ".join(tratamentos_map["Sintomas de Migrânea"]) if migranea else ""])
resumo_data.append(["Sintomas de Cefaleia Tensional", ", ".join(sintomas_tensional) if tensional else "Não avaliado", ", ".join(tratamentos_map["Sintomas de Cefaleia Tensional"]) if tensional else ""])
resumo_data.append(["Sintomas de Dor ATM", ", ".join(sintomas_dor) if sintomas_dor else "Nenhum", ", ".join(tratamentos_map["Sintomas de Dor ATM"]) if sintomas_dor else ""])
resumo_data.append(["Hábitos Parafuncionais", ", ".join(habitos) if habitos else "Nenhum", ", ".join(tratamentos_map["Hábitos Parafuncionais"]) if habitos else ""])
resumo_data.append(["Respiração", respiracao, ", ".join(tratamentos_map["Respiração"]) if respiracao == "Pela boca" else ""])
resumo_data.append(["Postura", ", ".join(postura) if postura else "Nenhuma", ", ".join(tratamentos_map["Postura"]) if postura else ""])
resumo_data.append(["Movimentos que exacerbam a dor", ", ".join(movimentos_cervicais) if movimentos_cervicais else "Nenhum", "Nenhum tratamento direto."])
resumo_data.append(["Abertura Bucal", abertura, ", ".join(tratamentos_map["Abertura Bucal"]) if abertura != "Normobilidade" else ""])
resumo_data.append(["Classificação da Lateralização", lateralidade, ", ".join(tratamentos_map["Classificação da Lateralização"]) if lateralidade != "Normobilidade" else ""])
resumo_data.append(["Zumbido", zumbido, ", ".join(tratamentos_map["Zumbido"]) if zumbido == "Sim" and not tensao_muscular else ""])
resumo_data.append(["Zumbido com tensão muscular", "Sim" if tensao_muscular else "Não", ", ".join(tratamentos_map["Sintomas de Dor ATM"]) if tensao_muscular else ""])


st.table(resumo_data)

# ======================================================
# 🩺 Diagnóstico e Tratamento (Preenchido automaticamente)
# ======================================================
st.header("🩺 Diagnóstico e Tratamento")
diagnostico = []
tratamento = []

# Grupo Migrânea
if migranea:
    diagnostico.append("Migrânea")
    tratamento += [
        "Hábitos alimentares","Evitar saída de sua rotina diária", "Sono reparador", "Respiração",
        "Repouso", "Tratamento medicamentoso [crise]"
    ]

# Grupo Cefaleia Tensional
if tensional:
    diagnostico.append("Cefaleia Tensional")
    tratamento += [
        "Liberação miofascial", "Digitopressão (Trigger points)", "Pompage", "Atividade física", "Alongamentos"
    ]

# Grupo 1 - Dor, ATM, hábitos, zumbido muscular
if sintomas_dor or habitos or (zumbido == "Sim" and tensao_muscular):
    diagnostico.append("Disfunção Temporomandibular de origem muscular/articular")
    tratamento += [
        "Liberação miofascial", "Digitopressão (Trigger Points)",
        "Alongamento muscular", "Orientação para evitar hábitos parafuncionais",
        "Mobilização articular ATM (Maitland)"
    ]

# Grupo 2 - Respiração/Postura/Zumbido não muscular
if respiracao == "Pela boca":
    diagnostico.append("Alteração do padrão respiratório (respiração bucal)")
    tratamento.append("Exercícios respiratórios + Encaminhamento Fonoaudiologia/Otorrino")

if postura:
    diagnostico.append("Alteração postural cervical/torácica")
    tratamento.append("Exercícios posturais e mobilização articular (RPG, Pilates, Fisioterapia postural)")

if zumbido == "Sim" and not tensao_muscular:
    diagnostico.append("Zumbido não relacionado a tensão muscular")
    tratamento.append("Encaminhamento Otorrinolaringologia")

# Grupo 3 - Amplitude de movimento
if abertura != "Normobilidade" or lateralidade != "Normobilidade":
    if "Disfunção Temporomandibular de origem articular" not in diagnostico:
        diagnostico.append("Disfunção Temporomandibular de origem articular")
    if "Mobilização articular ATM (Maitland)" not in tratamento:
        tratamento.append("Mobilização articular ATM (Maitland)")

# ======================================================
# 📋 NOVO RESUMO DE DIAGNÓSTICO E TRATAMENTO
# ======================================================
st.subheader("Resumo do Diagnóstico e Tratamento Gerados")
# Exibe o diagnóstico gerado
if diagnostico:
    st.markdown("**Diagnóstico(s):** " + ", ".join(diagnostico))
else:
    st.markdown("**Diagnóstico(s):** Sem alterações significativas.")

# Exibe o tratamento gerado
if tratamento:
    st.markdown("**Tratamento(s) Recomendado(s):** " + ", ".join(set(tratamento)))
else:
    st.markdown("**Tratamento(s) Recomendado(s):** Sem necessidade de intervenção específica no momento.")

# ======================================================
# 📅 Plano terapêutico semanal
# ======================================================
st.header("📅 Plano Terapêutico Semanal")
dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
plano = {}
for dia in dias:
    plano[dia] = st.multiselect(f"Técnicas para {dia}", list(set(tratamento)), key=dia)

# ======================================================
# 📄 Relatório final
# ======================================================
st.header("📄 Relatório Final")
if st.button("Gerar Relatório"):
    st.subheader("🧾 Dados do Paciente")
    st.write(f"**Nome:** {nome}")
    st.write(f"**Q.P.:** {qp}")
    st.write(f"**Tempo:** {tempo}")
    st.write(f"**Tipo de dor:** {tipo_dor}")
    st.write(f"**Comorbidades:** {', '.join(comorbidades)}")
    st.write(f"**Cirurgias:** {cirurgias}")
    st.write(f"**Tratamentos prévios:** {tratamentos_previos}")

    st.subheader("🩺 Diagnóstico")
    st.write(", ".join(diagnostico))

    st.subheader("💊 Tratamentos Recomendados")
    st.write(", ".join(set(tratamento)))

    st.subheader("📅 Plano Semanal")
    for dia, tecnicas in plano.items():
        st.write(f"**{dia}:** {', '.join(tecnicas)}")

    # ======================
    # 📝 Resumo interpretativo automático
    # ======================
    resumo = "O paciente apresenta quadro clínico compatível com "
    if len(diagnostico) == 1:
        resumo += f"**{diagnostico[0]}**."
    elif len(diagnostico) > 1:
        resumo += "**" + " + ".join(diagnostico) + "**."
    else:
        resumo += "**sem alterações significativas detectadas**."

    resumo += " O tratamento recomendado envolve: "
    if tratamento:
        resumo += ", ".join(set(tratamento)) + "."
    else:
        resumo += "sem necessidade de intervenção específica no momento."

    st.subheader("📝 Resumo Clínico")
    st.info(resumo)

    st.success("✅ Relatório gerado com sucesso!")

# ======================================================
# 📄 Exportar Relatório em PDF
# ======================================================
if st.button("Exportar PDF"):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Titulo", fontSize=16, leading=20, textColor=colors.HexColor("#003366"), spaceAfter=12, alignment=1, bold=True))
    styles.add(ParagraphStyle(name="Subtitulo", fontSize=13, leading=16, textColor=colors.HexColor("#006699"), spaceBefore=12, spaceAfter=6, bold=True))
    styles.add(ParagraphStyle(name="TextoPadrao", fontSize=11, leading=14))
    styles.add(ParagraphStyle(name="Resumo", fontSize=12, leading=16, textColor=colors.black, backColor=colors.HexColor("#f2f2f2"), spaceBefore=10, spaceAfter=10, leftIndent=6, rightIndent=6))

    elementos = []

    # Título
    elementos.append(Paragraph("🧠 Avaliação ATM's - DOF [Dor Orofacial]", styles["Titulo"]))
    elementos.append(Spacer(1, 12))

    # Dados do paciente em tabela
    dados_paciente = [
        ["Nome", nome],
        ["Queixa Principal (Q.P.)", qp],
        ["Tempo de Dor", tempo],
        ["Tipo de Dor", tipo_dor],
        ["Comorbidades", ", ".join(comorbidades)],
        ["Cirurgias", cirurgias],
        ["Tratamentos Prévios", tratamentos_previos]
    ]
    tabela_paciente = Table(dados_paciente, colWidths=[5*cm, 10*cm])
    tabela_paciente.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#d9e6f2")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.black),
        ("ALIGN", (0,0), (-1,-1), "LEFT"),
        ("FONTNAME", (0,0), (-1,-1), "Helvetica"),
        ("FONTSIZE", (0,0), (-1,-1), 10),
        ("GRID", (0,0), (-1,-1), 0.25, colors.grey),
        ("VALIGN", (0,0), (-1,-1), "TOP")
    ]))
    elementos.append(Paragraph("📋 Dados do Paciente", styles["Subtitulo"]))
    elementos.append(tabela_paciente)
    elementos.append(Spacer(1, 12))

    # Adiciona o resumo da avaliação no PDF
    resumo_data_pdf = [["Diagnóstico", "Sintomas", "Tratamento Sugerido"]]
    resumo_data_pdf.append([
        Paragraph("Sintomas de Migrânea", styles["TextoPadrao"]),
        Paragraph(", ".join(sintomas_migranea) if migranea else "Não avaliado", styles["TextoPadrao"]),
        Paragraph(", ".join(tratamentos_map["Sintomas de Migrânea"]) if migranea else "", styles["TextoPadrao"])
    ])
    resumo_data_pdf.append([
        Paragraph("Sintomas de Cefaleia Tensional", styles["TextoPadrao"]),
        Paragraph(", ".join(sintomas_tensional) if tensional else "Não avaliado", styles["TextoPadrao"]),
        Paragraph(", ".join(tratamentos_map["Sintomas de Cefaleia Tensional"]) if tensional else "", styles["TextoPadrao"])
    ])
    resumo_data_pdf.append([
        Paragraph("Sintomas de Dor ATM", styles["TextoPadrao"]),
        Paragraph(", ".join(sintomas_dor) if sintomas_dor else "Nenhum", styles["TextoPadrao"]),
        Paragraph(", ".join(tratamentos_map["Sintomas de Dor ATM"]) if sintomas_dor else "", styles["TextoPadrao"])
    ])
    resumo_data_pdf.append([
        Paragraph("Hábitos Parafuncionais", styles["TextoPadrao"]),
        Paragraph(", ".join(habitos) if habitos else "Nenhum", styles["TextoPadrao"]),
        Paragraph(", ".join(tratamentos_map["Hábitos Parafuncionais"]) if habitos else "", styles["TextoPadrao"])
    ])
    resumo_data_pdf.append([
        Paragraph("Respiração", styles["TextoPadrao"]),
        Paragraph(respiracao, styles["TextoPadrao"]),
        Paragraph(", ".join(tratamentos_map["Respiração"]) if respiracao == "Pela boca" else "", styles["TextoPadrao"])
    ])
    resumo_data_pdf.append([
        Paragraph("Postura", styles["TextoPadrao"]),
        Paragraph(", ".join(postura) if postura else "Nenhuma", styles["TextoPadrao"]),
        Paragraph(", ".join(tratamentos_map["Postura"]) if postura else "", styles["TextoPadrao"])
    ])
    resumo_data_pdf.append([
        Paragraph("Movimentos que exacerbam a dor", styles["TextoPadrao"]),
        Paragraph(", ".join(movimentos_cervicais) if movimentos_cervicais else "Nenhum", styles["TextoPadrao"]),
        Paragraph("Nenhum tratamento direto.", styles["TextoPadrao"])
    ])
    resumo_data_pdf.append([
        Paragraph("Abertura Bucal", styles["TextoPadrao"]),
        Paragraph(abertura, styles["TextoPadrao"]),
        Paragraph(", ".join(tratamentos_map["Abertura Bucal"]) if abertura != "Normobilidade" else "", styles["TextoPadrao"])
    ])
    resumo_data_pdf.append([
        Paragraph("Classificação da Lateralização", styles["TextoPadrao"]),
        Paragraph(lateralidade, styles["TextoPadrao"]),
        Paragraph(", ".join(tratamentos_map["Classificação da Lateralização"]) if lateralidade != "Normobilidade" else "", styles["TextoPadrao"])
    ])
    resumo_data_pdf.append([
        Paragraph("Zumbido", styles["TextoPadrao"]),
        Paragraph(zumbido, styles["TextoPadrao"]),
        Paragraph(", ".join(tratamentos_map["Zumbido"]) if zumbido == "Sim" and not tensao_muscular else "", styles["TextoPadrao"])
    ])
    resumo_data_pdf.append([
        Paragraph("Zumbido com tensão muscular", styles["TextoPadrao"]),
        Paragraph("Sim" if tensao_muscular else "Não", styles["TextoPadrao"]),
        Paragraph(", ".join(tratamentos_map["Sintomas de Dor ATM"]) if tensao_muscular else "", styles["TextoPadrao"])
    ])

    tabela_resumo_sintomas = Table(resumo_data_pdf, colWidths=[5*cm, 5*cm, 5*cm])
    tabela_resumo_sintomas.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#d9e6f2")),
        ("GRID", (0,0), (-1,-1), 0.25, colors.grey),
        ("VALIGN", (0,0), (-1,-1), "TOP")
    ]))
    elementos.append(Paragraph("📋 Resumo da Avaliação", styles["Subtitulo"]))
    elementos.append(tabela_resumo_sintomas)
    elementos.append(Spacer(1, 12))

    # Adiciona o diagnóstico e tratamento gerados no PDF
    elementos.append(Paragraph("🩺 Diagnóstico e Tratamento", styles["Subtitulo"]))
    elementos.append(Paragraph("<b>Diagnóstico(s):</b> " + ", ".join(diagnostico), styles["TextoPadrao"]))
    elementos.append(Paragraph("<b>Tratamento(s) Recomendado(s):</b> " + ", ".join(set(tratamento)), styles["TextoPadrao"]))
    elementos.append(Spacer(1, 12))
    
    # Plano semanal em tabela
    elementos.append(Paragraph("📅 Plano Terapêutico Semanal", styles["Subtitulo"]))
    plano_dados = [[Paragraph(dia, styles["TextoPadrao"]), Paragraph(", ".join(tecnicas), styles["TextoPadrao"])] for dia, tecnicas in plano.items()]
    plano_dados.insert(0, ["**Dia**", "**Técnicas**"])

    tabela_plano = Table(plano_dados, colWidths=[4*cm, 11*cm])
    tabela_plano.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#d9e6f2")),
        ("GRID", (0,0), (-1,-1), 0.25, colors.grey),
        ("VALIGN", (0,0), (-1,-1), "TOP")
    ]))
    elementos.append(tabela_plano)

    # === CORREÇÃO AQUI: Novo formato para o resumo da Regra de Ouro ===
    elementos.append(Paragraph("⭐ Regra de Ouro", styles["Subtitulo"]))
    
    # Parágrafo de introdução
    elementos.append(Paragraph(f"O paciente <b>{nome}</b> apresenta quadro clínico compatível com:", styles["TextoPadrao"]))

    # Lista de diagnósticos
    diagnosticos_list = [f"<li>{d}</li>" for d in diagnostico]
    diagnosticos_html = f"<ul>{''.join(diagnosticos_list)}</ul>"
    elementos.append(Paragraph(f"<b>Diagnósticos:</b> {diagnosticos_html}", styles["TextoPadrao"]))

    # Lista de tratamentos
    tratamentos_list = [f"<li>{t}</li>" for t in sorted(list(set(tratamento)))]
    tratamentos_html = f"<ul>{''.join(tratamentos_list)}</ul>"
    elementos.append(Paragraph(f"<b>Tratamentos:</b> {tratamentos_html}", styles["TextoPadrao"]))

    # Parágrafo final
    elementos.append(Paragraph("O plano terapêutico semanal foi estruturado conforme a tabela acima.", styles["TextoPadrao"]))

    doc.build(elementos)
    buffer.seek(0)

    st.download_button(
        label="📥 Baixar Relatório em PDF",
        data=buffer,
        file_name=f"Relatorio_{nome}.pdf",
        mime="application/pdf"
    )