# Legal Fee Optimizer
# v0.8.7 — UX institucional refinado: cabeçalho premium alinhado, subtítulo e layout final de deploy

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from datetime import datetime

# ---------- Funções utilitárias ----------
def brl(v: float) -> str:
    s = f"R$ {v:,.2f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")

def nowrap_html(text: str) -> str:
    return f"<span class='nowrap'>{text}</span>"

# ---------- Layout base ----------
logo_path = Path("assets/logo_gui2.jpg")

st.markdown(f"""
<style>
body {{
  font-family: 'Inter', sans-serif;
  background-color: #F9FAFB;
  color: #1F2937;
}}
[data-testid="stSidebar"] {{
  width: 400px !important;
  background-color: #F3F4F6;
  padding: 1rem;
  border-right: 1px solid #E5E7EB;
}}
div[data-testid="stExpander"] {{
  border: 1px solid #E5E7EB;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  margin-bottom: 1rem;
}}
div[data-testid="stExpander"] > div:first-child {{
  background-color: #F3F4F6;
  color: #0E4DA4;
  font-weight: 600;
  border-radius: 12px 12px 0 0;
}}
.footer {{
  margin-top: 2rem;
  text-align: center;
  font-size: 0.85rem;
  color: #6B7280;
  border-top: 1px solid #E5E7EB;
  padding-top: 0.5rem;
}}
</style>
""", unsafe_allow_html=True)

# ---------- Cabeçalho premium institucional ----------
with st.container():
    if logo_path.exists():
        logo_url = str(logo_path).replace("\\", "/")
        st.markdown(
            f"""
            <div style="
                display: flex;
                align-items: center;
                justify-content: space-between;
                background: linear-gradient(90deg, #0E4DA4 0%, #0A325E 100%);
                padding: 1.2rem 1.8rem;
                border-radius: 14px;
                box-shadow: 0 3px 8px rgba(0,0,0,0.1);
            ">
                <div style="display: flex; flex-direction: column; justify-content: center;">
                    <h1 style="font-size:1.35rem; font-weight:700; color:white; margin:0;">
                        ⚖️ Legal Fee Optimizer — Simulação Financeira Jurídica
                    </h1>
                    <p style="font-size:0.9rem; color:#E5E7EB; margin-top:4px;">
                        Precificação jurídica orientada por margens, custos e risco.
                    </p>
                </div>
                <div style="flex-shrink: 0; margin-left: 30px;">
                    <img src="{logo_url}" alt="Logo" style="height:65px; border-radius:10px;">
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <div style="
                background: linear-gradient(90deg, #0E4DA4 0%, #0A325E 100%);
                padding: 1.2rem 1.8rem;
                border-radius: 14px;
                box-shadow: 0 3px 8px rgba(0,0,0,0.1);
            ">
                <h1 style="font-size:1.35rem; font-weight:700; color:white; margin:0;">
                    ⚖️ Legal Fee Optimizer — Simulação Financeira Jurídica
                </h1>
                <p style="font-size:0.9rem; color:#E5E7EB; margin-top:4px;">
                    Precificação jurídica orientada por margens, custos e risco.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

# ---------- Entradas ----------
with st.sidebar:
    st.header("Parâmetros da Simulação")
    honorario = st.number_input("Honorário Bruto (R$)", min_value=0.0, step=100.0, format="%.2f")
    horas_estimadas = st.number_input("Horas Estimadas de Trabalho", min_value=0.0, step=1.0)
    custo_fixo = st.number_input("Custos Fixos (R$)", min_value=0.0, step=100.0, format="%.2f")
    custo_variavel = st.number_input("Custos Variáveis (R$)", min_value=0.0, step=50.0, format="%.2f")
    desconto = st.slider("Desconto (%)", 0, 100, 0)
    complexidade = st.slider("Complexidade do Caso", 1, 5, 3)
    sucesso = st.slider("Probabilidade de Sucesso (%)", 0, 100, 80)
    st.caption("Preencha os campos para visualizar margens, custos e rentabilidade.")

# ---------- Cálculos ----------
if horas_estimadas > 0 and honorario > 0:
    desconto_valor = honorario * (desconto / 100)
    honorario_liquido = honorario - desconto_valor
    fator_complexidade = {1: 0.9, 2: 1.0, 3: 1.1, 4: 1.25, 5: 1.5}.get(complexidade, 1.0)
    custo_fixo_ajustado = custo_fixo * fator_complexidade
    custo_variavel_ajustado = custo_variavel * fator_complexidade
    custo_total = custo_fixo_ajustado + custo_variavel_ajustado
    custo_hora = custo_total / horas_estimadas if horas_estimadas > 0 else 0.0
    lucro_liquido = honorario_liquido - custo_total
    margem_contribuicao = (lucro_liquido / honorario_liquido) * 100 if honorario_liquido > 0 else 0.0
    rentabilidade_ajustada = margem_contribuicao * (sucesso / 100)
    ponto_equilibrio = custo_total / (margem_contribuicao / 100) if margem_contribuicao > 0 else 0.0

    st.subheader("📈 Resultados Financeiros da Simulação")
    if desconto > 0:
        st.warning(f"🔻 Desconto de {desconto}% aplicado — Honorário líquido: {brl(honorario_liquido)}")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💰 Margem de Contribuição", f"{margem_contribuicao:.2f}%")
        st.metric("📊 Rentabilidade Ajustada", f"{rentabilidade_ajustada:.2f}%")
    with col2:
        st.metric("⚙️ Custo Total", brl(custo_total))
        st.metric("⏱️ Custo-Hora Real", brl(custo_hora))
    with col3:
        st.metric("💵 Lucro Líquido", brl(lucro_liquido))
        st.metric("🎯 Ponto de Equilíbrio", brl(ponto_equilibrio))

    with st.expander("🧠 Análise Detalhada e Recomendações", expanded=False):
        if margem_contribuicao < 30:
            st.error("🔻 Margem crítica: o caso é financeiramente inviável.")
        elif 30 <= margem_contribuicao < 45:
            st.warning("⚠️ Margem abaixo do mínimo aceitável (45%). Reavalie precificação ou reduza custos.")
        elif 45 <= margem_contribuicao < 60:
            st.info("ℹ️ Margem razoável, mas sensível a oscilações. Monitore execução e produtividade.")
        else:
            st.success("✅ Margem saudável e sustentável. Estrutura financeira sólida e competitiva.")

        if desconto > 0:
            linha_desconto_html = (
                "Desconto de <b>{}%</b> ({}{}) reduziu o honorário bruto de {} para {}."
                .format(
                    desconto,
                    "",
                    nowrap_html(brl(desconto_valor)),
                    nowrap_html(brl(honorario)),
                    nowrap_html(brl(honorario_liquido)),
                )
            )
        else:
            linha_desconto_html = (
                "Nenhum desconto aplicado. Honorário líquido igual ao honorário bruto ({})."
                .format(nowrap_html(brl(honorario)))
            )

        st.markdown(f"""
        <h3>⚙️ Complexidade, Desconto e Risco</h3>
        <ul style="margin-left:1rem;">
            <li>Complexidade <b>Nível {complexidade}</b> → fator de <b>{fator_complexidade:.2f}x</b> aplicado aos custos.</li>
            <li>{linha_desconto_html}</li>
        </ul>
        """, unsafe_allow_html=True)

        st.markdown("### 📈 Resumo Executivo")
        if margem_contribuicao < 30:
            resumo = (f"O caso apresenta margem de apenas {margem_contribuicao:.1f}%. "
                      "Financeiramente inviável — o valor não cobre custos diretos e indiretos. "
                      "Recomenda-se revisão imediata do honorário.")
        elif 30 <= margem_contribuicao < 45:
            resumo = (f"A margem de {margem_contribuicao:.1f}% indica risco elevado. "
                      "Embora haja possibilidade de lucro, o retorno é limitado. "
                      "Considere ajustar custos ou renegociar valores.")
        elif 45 <= margem_contribuicao < 60:
            resumo = (f"Margem de {margem_contribuicao:.1f}% e probabilidade de sucesso de {sucesso}%. "
                      f"Rentabilidade esperada: {rentabilidade_ajustada:.1f}%. "
                      "Cenário viável, mas sujeito a variações operacionais.")
        else:
            resumo = (f"Margem de {margem_contribuicao:.1f}% e rentabilidade esperada de {rentabilidade_ajustada:.1f}%. "
                      f"Custo total de {brl(custo_total)}. Estrutura enxuta e sustentável — excelente desempenho.")
        st.markdown(resumo)

    with st.expander("📊 Estrutura Financeira — Gráfico Waterfall", expanded=False):
        etapas = ["Honorário Bruto"]
        valores = [honorario]
        if desconto_valor > 0:
            etapas.append("Desconto")
            valores.append(-desconto_valor)
        etapas += ["Custos Fixos", "Custos Variáveis"]
        valores += [-custo_fixo_ajustado, -custo_variavel_ajustado]
        cumul = np.cumsum([0] + valores[:-1])
        cores = ["#3A3A3A"] + (["#6B7280"] if desconto_valor > 0 else []) + ["#D97706", "#EAB308"]
        cor_lucro = "#22C55E"
        fig, ax = plt.subplots(figsize=(8, 4))
        for i, (val, base, cor) in enumerate(zip(valores, cumul, cores)):
            ax.bar(etapas[i], val, bottom=base, color=cor, edgecolor="black", linewidth=0.8)
            ax.text(i, base + (val / 2), brl(val), ha='center', va='center', color='white', fontweight='bold')
        ax.bar("Lucro Líquido", lucro_liquido, bottom=0, color=cor_lucro, edgecolor="black", linewidth=0.8)
        ax.text(len(etapas), lucro_liquido / 2, brl(lucro_liquido), ha='center', va='center', color='white', fontweight='bold')
        ax.axhline(0, color='black', linewidth=1)
        ax.set_ylabel("Valor (R$)", fontsize=10)
        ax.set_title("Composição do Resultado Financeiro", color="#0E4DA4", fontsize=12, fontweight="bold")
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.tick_params(colors="#333333")
        plt.tight_layout()
        st.pyplot(fig)
        st.caption("Evolução: Honorário Bruto → (Desconto) → Custos Fixos e Variáveis → Lucro Líquido.")

else:
    st.info("💤 Aguardando dados para gerar a análise. Insira valores para iniciar a simulação.")

# ---------- Rodapé institucional ----------
st.markdown(
    f"<div class='footer'>© {datetime.now().year} Guilherme de Paula | Legal Data Analytics — Todos os direitos reservados.</div>",
    unsafe_allow_html=True
)
