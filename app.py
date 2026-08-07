import streamlit as st
import pandas as pd

# ============ CONFIGURAÇÃO DA PÁGINA ============
st.set_page_config(
    page_title="Assistente de Impostos - Security Services",
    page_icon="🇧🇷",
    layout="wide"
)

# ============ DADOS ============
DADOS_IMPOSTOS = {
    "Cyber Strategy": [
        {
            "offering": "IBM Cyber Strategy and Risk",
            "occ": "6955-AX2",
            "natop": "3347 - CONSULTORIA de SW",
            "iss_sp": 0.029, "iss_hf": 0.02, "iss_rj": 0.05,
            "pis_cofins": 0.0365
        },
        {
            "offering": "Cyber Risk, Resilience and Compliance",
            "occ": "6955-AX3",
            "natop": "3347 - CONSULTORIA de SW",
            "iss_sp": 0.029, "iss_hf": 0.02, "iss_rj": 0.05,
            "pis_cofins": 0.0365
        },
        {
            "offering": "BV Assets for IBM Cyber Strategy and Risk",
            "occ": "6941-20Y",
            "natop": "⚠️ Não disponível",
            "iss_sp": None, "iss_hf": None, "iss_rj": None,
            "pis_cofins": None
        },
    ],
    "Data and AI Security": [
        {
            "offering": "IBM CyberDefend",
            "occ": "6955-AX4",
            "natop": "3347 - CONSULTORIA de SW",
            "iss_sp": 0.029, "iss_hf": 0.02, "iss_rj": 0.05,
            "pis_cofins": 0.0365
        },
        {
            "offering": "Identity and Access Management",
            "occ": "6955-AX5",
            "natop": "2212 - INSTALAÇÃO, CONFIGURAÇÃO E MANUTENÇÃO",
            "iss_sp": 0.029, "iss_hf": 0.02, "iss_rj": 0.05,
            "pis_cofins": 0.0365
        },
        {
            "offering": "Application Security",
            "occ": "6955-AX6",
            "natop": "⚠️ Não disponível",
            "iss_sp": None, "iss_hf": None, "iss_rj": None,
            "pis_cofins": None
        },
        {
            "offering": "Cloud and Infrastructure Security",
            "occ": "6955-AX7",
            "natop": "3347 - CONSULTORIA de SW",
            "iss_sp": 0.029, "iss_hf": 0.02, "iss_rj": 0.05,
            "pis_cofins": 0.0365
        },
        {
            "offering": "BV Assets for IBM CyberDefend",
            "occ": "6941-20X",
            "natop": "⚠️ Não disponível",
            "iss_sp": None, "iss_hf": None, "iss_rj": None,
            "pis_cofins": None
        },
    ],
    "Threat Management Advisory": [
        {
            "offering": "IBM Cyber Threat Management",
            "occ": "6955-AX8",
            "natop": "3347 - CONSULTORIA de SW",
            "iss_sp": 0.029, "iss_hf": 0.02, "iss_rj": 0.05,
            "pis_cofins": 0.0365
        },
        {
            "offering": "X-Force Red Testing",
            "occ": "6955-AX9",
            "natop": "3347 - CONSULTORIA de SW",
            "iss_sp": 0.029, "iss_hf": 0.02, "iss_rj": 0.05,
            "pis_cofins": 0.0365
        },
        {
            "offering": "Exposure Management",
            "occ": "6955-AY0",
            "natop": "3347 - CONSULTORIA de SW",
            "iss_sp": 0.029, "iss_hf": 0.02, "iss_rj": 0.05,
            "pis_cofins": 0.0365
        },
        {
            "offering": "Threat Detection and Response",
            "occ": "6955-AY1",
            "natop": "3347 - CONSULTORIA de SW / 2212 - INSTALAÇÃO",
            "iss_sp": 0.029, "iss_hf": 0.02, "iss_rj": 0.05,
            "pis_cofins": 0.0365
        },
        {
            "offering": "X-Force Incident Response",
            "occ": "6955-AY2",
            "natop": "2212 - INSTALAÇÃO, CONFIGURAÇÃO E MANUTENÇÃO",
            "iss_sp": 0.029, "iss_hf": 0.02, "iss_rj": 0.05,
            "pis_cofins": 0.0365
        },
        {
            "offering": "BV Assets for IBM Cyber Threat Management",
            "occ": "6941-20P",
            "natop": "⚠️ Não disponível",
            "iss_sp": None, "iss_hf": None, "iss_rj": None,
            "pis_cofins": None
        },
    ],
    "Revenda de OEM": [
        {
            "offering": "Revenda de OEM",
            "occ": "---",
            "natop": "Revenda",
            "iss_sp": 0.029, "iss_hf": 0.02, "iss_rj": 0.05,
            "pis_cofins": 0.0925
        },
    ]
}

LOCALIDADES = {
    "São Paulo": "iss_sp",
    "Hortolandia": "iss_hf",
    "Rio de Janeiro": "iss_rj"
}

def formatar_brl(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# ============ ESTILO ============
st.markdown("""
    <style>
        /* Fundo geral */
        .stApp { background-color: #f4f6fb; }

        /* Header */
        .main-header {
            background: linear-gradient(135deg, #1a1a2e 0%, #0f3460 100%);
            padding: 35px 40px;
            border-radius: 16px;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 8px 32px rgba(15,52,96,0.18);
        }
        .main-header h1 {
            color: #00d4ff;
            font-size: 2.3rem;
            margin-bottom: 6px;
            letter-spacing: 1px;
        }
        .main-header p { color: #b0bec5; font-size: 1rem; }

        /* Cards */
        .card {
            background: white;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.07);
            margin-bottom: 20px;
        }

        /* Gross box */
        .gross-box {
            background: linear-gradient(135deg, #1a1a2e 0%, #0f3460 100%);
            border-radius: 12px;
            padding: 28px;
            text-align: center;
            margin-top: 20px;
            box-shadow: 0 4px 20px rgba(15,52,96,0.25);
        }
        .gross-box .label {
            color: #b0bec5;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        .gross-box .valor {
            color: #00d4ff;
            font-size: 2.6rem;
            font-weight: 800;
            margin: 10px 0 6px;
        }
        .gross-box .pct {
            color: #80cbc4;
            font-size: 0.9rem;
        }

        /* Pilar badge */
        .pilar-badge {
            display: inline-block;
            background: #e3f2fd;
            color: #0f3460;
            padding: 5px 14px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            margin-bottom: 16px;
            border: 1px solid #90caf9;
        }

        /* Linha de imposto */
        .imposto-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 0;
            border-bottom: 1px solid #f0f0f0;
        }
        .imposto-row:last-child { border-bottom: none; }
        .imposto-label { color: #546e7a; font-size: 0.95rem; }
        .imposto-valor { color: #0f3460; font-weight: 700; font-size: 1rem; }

        /* Divider */
        hr { border-color: #e0e0e0 !important; }

        /* Botão */
        .stButton > button {
            background: linear-gradient(135deg, #0f3460, #00d4ff) !important;
            color: white !important;
            font-weight: 700 !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 12px !important;
            font-size: 1rem !important;
            transition: all 0.3s !important;
        }
        .stButton > button:hover {
            opacity: 0.9 !important;
            transform: translateY(-1px) !important;
        }

        /* Selectbox e inputs */
        .stSelectbox > div > div,
        .stNumberInput > div > div > input {
            border-radius: 8px !important;
            border: 1.5px solid #cfd8dc !important;
        }

        /* Dataframe */
        .stDataFrame { border-radius: 10px; overflow: hidden; }
    </style>
""", unsafe_allow_html=True)

# ============ HEADER ============
st.markdown("""
    <div class="main-header">
        <h1>🇧🇷 Assistente de Impostos</h1>
        <p>Security Services IBM &nbsp;·&nbsp; Cálculo NET × GROSS</p>
    </div>
""", unsafe_allow_html=True)

# ============ LAYOUT PRINCIPAL ============
col1, col2 = st.columns([1, 1], gap="large")

# ---------- COLUNA 1: INPUTS ----------
with col1:
    st.markdown("### ⚙️ Parâmetros")

    pilar = st.selectbox(
        "🔐 Pilar",
        options=[""] + list(DADOS_IMPOSTOS.keys()),
        format_func=lambda x: "— Selecione um pilar —" if x == "" else x
    )

    localidade = st.selectbox(
        "📍 Localidade",
        options=["", "São Paulo", "Hortolandia", "Rio de Janeiro"],
        format_func=lambda x: "— Selecione uma localidade —" if x == "" else x
    )

    valor_net = st.number_input(
        "💵 Valor NET (R$)",
        min_value=0.0,
        step=1000.0,
        format="%.2f"
    )

    calcular = st.button("💰  Calcular Impostos", use_container_width=True, type="primary")

# ---------- COLUNA 2: RESULTADO ----------
with col2:
    st.markdown("### 📊 Resultado")

    if calcular:
        if not pilar or not localidade or valor_net <= 0:
            st.error("⚠️ Preencha todos os campos corretamente!")
        else:
            ofertas    = DADOS_IMPOSTOS[pilar]
            chave_iss  = LOCALIDADES[localidade]
            iss        = ofertas[0][chave_iss]
            pis_cofins = ofertas[0]["pis_cofins"]

            if iss is None or pis_cofins is None:
                st.warning("⚠️ Este pilar não possui alíquotas cadastradas.")
            else:
                imp_iss    = valor_net * iss
                imp_pis    = valor_net * pis_cofins
                total_imp  = imp_iss + imp_pis
                valor_gross = valor_net + total_imp
                pct_total  = (total_imp / valor_net) * 100

                st.markdown(
                    f'<div class="pilar-badge">🔐 {pilar} &nbsp;·&nbsp; 📍 {localidade}</div>',
                    unsafe_allow_html=True
                )

                # Métricas principais
                m1, m2, m3 = st.columns(3)
                m1.metric("Valor NET",       formatar_brl(valor_net))
                m2.metric("Total Impostos",  formatar_brl(total_imp))
                m3.metric("% Imposto",       f"{pct_total:.2f}%")

                st.divider()

                # Detalhamento
                st.markdown(f"""
                    <div class="imposto-row">
                        <span class="imposto-label">🏛️ ISS ({iss*100:.1f}%)</span>
                        <span class="imposto-valor">{formatar_brl(imp_iss)}</span>
                    </div>
                    <div class="imposto-row">
                        <span class="imposto-label">📋 PIS/COFINS ({pis_cofins*100:.2f}%)</span>
                        <span class="imposto-valor">{formatar_brl(imp_pis)}</span>
                    </div>
                """, unsafe_allow_html=True)

                # GROSS
                st.markdown(f"""
                    <div class="gross-box">
                        <div class="label">Valor GROSS (Total com Impostos)</div>
                        <div class="valor">{formatar_brl(valor_gross)}</div>
                        <div class="pct">Impostos representam {pct_total:.2f}% do valor NET</div>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.info("👈 Preencha os campos ao lado e clique em **Calcular Impostos**")

# ============ TABELA DE OFERTAS ============
st.divider()
st.markdown("### 📑 Ofertas do Pilar Selecionado")

if pilar:
    ofertas = DADOS_IMPOSTOS[pilar]
    tabela  = []
    for o in ofertas:
        tabela.append({
            "Offering":   o["offering"],
            "OCC":        o["occ"],
            "NATOP":      o["natop"],
            "ISS SP":     f"{o['iss_sp']*100:.1f}%"    if o["iss_sp"]     else "—",
            "ISS HF":     f"{o['iss_hf']*100:.1f}%"    if o["iss_hf"]     else "—",
            "ISS RJ":     f"{o['iss_rj']*100:.1f}%"    if o["iss_rj"]     else "—",
            "PIS/COFINS": f"{o['pis_cofins']*100:.2f}%" if o["pis_cofins"] else "—",
        })
    df = pd.DataFrame(tabela)
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("Selecione um pilar acima para ver as ofertas disponíveis.")
