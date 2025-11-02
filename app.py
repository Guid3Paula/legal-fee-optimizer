# Legal Fee Optimizer
# v0.8.3 — correção definitiva: moedas e % com no-wrap + HTML limpo (sem **), fim das quebras

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# ---------- Funções utilitárias ----------
def brl(v: float) -> str:
    """Formata valor para Real (R$) com separadores brasileiros."""
    s = f"R$ {v:,.2f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")

def brl_html(v: float) -> str:
    """Valor BRL envolto em span nowrap para evitar quebras."""
    return f"<span class='nowrap'>{brl(v)}</span>"

def pct_html(v: float, casas: int = 1) -> str:
    """Percentual com span nowrap para evitar quebras (ex.: 61,5%)."""
    s = f"{v:.{casas}f}%"
    s = s.replace(".", ",")
    return f"<span class='nowrap'>{s}</span>"

# ---------- Layout e cabeçalho ----------
logo_path = Path("assets/logo_gui.jpg")

col1, col2 = st.columns([5, 1])
with col1:
    st.markdown(
        "<h1 style='font-size:1.5rem; color:#0E4DA4; font-weight:700;'>⚖️ Legal Fee Optimizer — Simulação Financeira para Precificação Jurídica Baseada em Margens e Riscos</h1>",
        unsafe_allow_html=True
    )
with col2:
    if logo_path.exists():
        st.image(str(logo_path), width=80, output_format="auto")

PRIMARY_COLOR = "#0E4DA4"
ACCENT_COLOR = "#00C2FF"

st.markdown(f"""
<style>
:root {{
  --primary: {PRIMARY_COLOR};
  --accent: {ACCENT_COLOR};
}}
[data-testid="stSidebar"] {{
    width: 400px !important;
}}
div[data-testid="stAppViewContainer"] {{
    padding-left: 0px !important;
}}
h1, h2, h3 {{
  color: var(--primary);
}}
/* Evita quebra de linha dentro de valores (R$ 100.000,00 | 61,5%) */
.nowrap {{ white-space: nowrap; }}
/* Parágrafos mais limpos nos blocos analíticos */
.block p {{ margin: 0 0 8px; line-height: 1.45; }}
</style>
""", unsafe_allow_html=True)

st.markdown("---")

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

    # ---------- Resultados ----------
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

    # ---------- Expander: Análises Detalhadas ----------
    with st.expander("🧠 Análise Detalhada e Recomendações", expanded=False):

        # Avaliação de desempenho
        if margem_contribuicao < 30:
            st.error("🔻 Margem crítica: o caso é financeiramente inviável.")
        elif 30 <= margem_contribuicao < 45:
            st.warning("⚠️ Margem abaixo do mínimo aceitável (45%). Reavalie precificação ou reduza custos.")
        elif 45 <= margem_contribuicao < 60:
            st.info("ℹ️ Margem razoável, mas sensível a oscilações. Monitore execução e produtividade.")
        else:
            st.success("✅ Margem saudável e sustentável. Estrutura financeira sólida e competitiva.")

        # ⚙️ Complexidade, Desconto e Risco — HTML limpo (sem **), com no-wrap
        st.markdown("### ⚙️ Complexidade, Desconto e Risco")
        st.markdown(
            f"<div class='block'>"
            f"<p>Complexidade <strong>Nível {complexidade}</strong> → fator de "
            f"<strong>{fator_complexidade:.2f}x</strong> aplicado aos custos.</p>"
            +
            (
                f"<p>Desconto de <strong>{desconto}%</strong> "
                f"({brl_html(desconto_valor)}) reduziu o honorário bruto de "
                f"{brl_html(honorario)} para <strong>{brl_html(honorario_liquido)}</strong>.</p>"
                if desconto > 0
                else
                f"<p>Nenhum desconto aplicado. Honorário líquido igual ao honorário bruto "
                f"({brl_html(honorario)}).</p>"
            )
            +
            f"<p>Probabilidade de sucesso de <strong>{sucesso}%</strong> ajusta a rentabilidade esperada.</p>"
            f"</div>",
            unsafe_allow_html=True
        )

        # 📘 Interpretação dos Indicadores
        st.markdown("### 📘 Interpretação dos Indicadores")
        st.markdown(f"""
        - **💰 Margem de Contribuição ({margem_contribuicao:.2f}%)** — percentual do honorário líquido que sobra após cobrir custos fixos e variáveis.  
          > Fórmula: `(Honorário Líquido - Custos Totais) ÷ Honorário Líquido × 100`

        - **💵 Lucro Líquido ({brl(lucro_liquido)})** — resultado final após desconto e custos.  
          > Fórmula: `Honorário Líquido - Custos Totais`

        - **⚙️ Custo Total ({brl(custo_total)})** — soma de custos fixos e variáveis ajustados pela complexidade.  
          > Fórmula: `(Custos Fixos + Custos Variáveis) × Fator de Complexidade`

        - **⏱️ Custo-Hora Real ({brl(custo_hora)})** — custo médio por hora trabalhada.  
          > Fórmula: `Custo Total ÷ Horas Estimadas`

        - **🎯 Ponto de Equilíbrio ({brl(ponto_equilibrio)})** — receita mínima para zerar o lucro.  
          > Fórmula: `Custo Total ÷ (Margem de Contribuição ÷ 100)`

        - **📊 Rentabilidade Ajustada ({rentabilidade_ajustada:.2f}%)** — lucro ponderado pelo risco de êxito.  
          > Fórmula: `Margem de Contribuição × (Probabilidade de Sucesso ÷ 100)`
        """)

        # 📈 Resumo Executivo — HTML limpo, com no-wrap para valores e %
        st.markdown("### 📈 Resumo Executivo")
        st.markdown(
            f"<div class='block'>"
            f"<p>Este caso apresenta {pct_html(margem_contribuicao)} de margem de contribuição e "
            f"{pct_html(rentabilidade_ajustada)} de rentabilidade ajustada ao risco.</p>"
            f"<p>O custo total estimado é de {brl_html(custo_total)}, enquanto o lucro líquido projetado alcança "
            f"{brl_html(lucro_liquido)}, considerando a estrutura de custos e o desconto aplicado.</p>"
            f"<p>O ponto de equilíbrio financeiro é atingido a partir de {brl_html(ponto_equilibrio)} em honorários, "
            f"indicando o nível mínimo de receita necessário para evitar prejuízo.</p>"
            f"<p>Esse cenário reflete uma operação "
            f"{'sólida e sustentável' if margem_contribuicao >= 60 else 'razoável, porém sensível a variações de custo'} "
            f"com "
            f"{'boa capacidade de absorver oscilações de mercado' if margem_contribuicao >= 60 else 'potencial de otimização via revisão de precificação ou eficiência operacional'}."
            f"</p>"
            f"</div>",
            unsafe_allow_html=True
        )

        st.markdown(
            "> 💡 **Recomendações Automáticas:**  \n"
            "> - Margem < 30% → Caso financeiramente inviável.  \n"
            "> - 30% ≤ Margem < 45% → Precificação inadequada.  \n"
            "> - 45% ≤ Margem < 60% → Faixa aceitável, monitorar execução.  \n"
            "> - Margem ≥ 60% → Estrutura sólida e competitiva."
        )

    # ---------- Expander: Gráfico Waterfall ----------
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
            y_pos = base + (val / 2)
            ax.text(i, y_pos, brl(val), ha='center', va='center', color='white', fontweight='bold')

        ax.bar("Lucro Líquido", lucro_liquido, bottom=0, color=cor_lucro, edgecolor="black", linewidth=0.8)
        ax.text(len(etapas), lucro_liquido / 2, brl(lucro_liquido), ha='center', va='center', color='white', fontweight='bold')

        ax.axhline(0, color='black', linewidth=1)
        ax.set_ylabel("Valor (R$)", fontsize=10)
        ax.set_title("Composição do Resultado Financeiro", color="#0E4DA4", fontsize=12, fontweight="bold")
        fig.patch.set_facecolor('none')
        ax.set_facecolor('none')
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.tick_params(colors="#333333")

        plt.tight_layout()
        st.pyplot(fig)
        st.caption("Evolução: Honorário Bruto → (Desconto) → Custos Fixos e Variáveis → Lucro Líquido (barra final partindo do zero).")

else:
    st.markdown("---")
    st.info("💤 Aguardando dados para gerar a análise. Insira valores de honorário, horas e custos para visualizar margens, rentabilidade e recomendações.")
