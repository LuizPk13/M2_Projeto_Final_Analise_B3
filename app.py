"""
Data App - Análise de Performance de Ações da B3 (2021-2023)
"""

# Bibliotecas
from pathlib import Path
import pandas as pd
import streamlit as st

# Configurações da página
st.set_page_config(page_title="Análise B3 2021-2023", page_icon="📈", layout="wide")

# Caminho dos arquivos
raiz = Path(__file__).resolve().parent
arquivo_contingencia = raiz / "data" / "processed" / "cotacoes_metricas.csv"


# ----------------------------------------------------------------------------------------
# Carga de dados (Supabase com contingência em CSV)
# ----------------------------------------------------------------------------------------
@st.cache_data(ttl=3600, show_spinner="Carregando Dados...")
def carregar_dados():
    """Lê o Supabase; se o banco estiver indisponível, lê o CSV local."""

    try:  # Tenta ler do Supabase
        conn = st.connection("postgresql", type="sql")
        df = conn.query("SELECT * FROM cotacoes", ttl=3600)
        origem = "Supabase (PostgreSQL)"

    except Exception:  # Se houver erro, lê o CSV local
        df = pd.read_csv(arquivo_contingencia)
        origem = "CSV local (Contingência)"

    # Converte a coluna "data" para datetime
    df["data"] = pd.to_datetime(df["data"])
    return df, origem


@st.cache_data(show_spinner=False)
def recalcular_periodo(df):
    """Recalcula a Base 100, retorno acumulado e drawdown a partir da 1º data do filtro"""
    df = df.sort_values(["nome_acao", "data"]).copy()
    preco = df.groupby("nome_acao")["fechamento_ajustado"]
    df["base_100"] = df["fechamento_ajustado"] / preco.transform("first") * 100
    df["retorno_acumulado"] = df["base_100"] / 100 - 1
    df["drawdown"] = df["fechamento_ajustado"] / preco.cummax() - 1
    return df


# Desempacota o DataFrame e a origem dos dados
df, origem = carregar_dados()


# ------------------------------------------------------------------------------
# Filtros: valores padrão guardados no session_state
# ------------------------------------------------------------------------------
setores_todos = sorted(df["setor"].unique())
data_min = df["data"].min().date()
data_max = df["data"].max().date()


def acoes_dos_setores(setores):
    """Lista as ações que pertencem aos setores escolhidos"""
    return sorted(df.loc[df["setor"].isin(setores), "nome_acao"].unique())


padroes = {
    "filtro_setores": setores_todos,
    "filtro_acoes": acoes_dos_setores(setores_todos),
    "filtro_periodo": (data_min, data_max),
}

# Na primeira execução, grava os padrões, mantém o que o usuário escolheu
for chave, valor in padroes.items():
    if chave not in st.session_state:
        st.session_state[chave] = valor


def ao_mudar_setor():
    """Filtro cruzado: ao trocar os setores, a lista de ações acompanha"""
    st.session_state["filtro_acoes"] = acoes_dos_setores(
        st.session_state["filtro_setores"]
    )


def resetar_filtros():
    """Volta todos os filtros para o padrão"""
    for chave, valor in padroes.items():
        st.session_state[chave] = valor


with st.sidebar:
    st.header("🔎 Filtros")
    st.multiselect(
        "Setores", setores_todos, key="filtro_setores", on_change=ao_mudar_setor
    )
    st.multiselect(
        "Ações",
        acoes_dos_setores(st.session_state["filtro_setores"]),
        key="filtro_acoes",
    )
    st.date_input(
        "Período",
        min_value=data_min,
        max_value=data_max,
        key="filtro_periodo",
        format="DD/MM/YYYY",
    )
    st.button("🔄 Resetar filtros", on_click=resetar_filtros)


# --------------------------------------------------------------------------------------------------
# Aplicação dos filtros
# --------------------------------------------------------------------------------------------------
periodo = st.session_state["filtro_periodo"]
if len(periodo) != 2:
    st.info("Selecione a data inicial e a data final do período.")
    st.stop()

inicio, fim = pd.Timestamp(periodo[0]), pd.Timestamp(periodo[1])
filtro = df["nome_acao"].isin(st.session_state["filtro_acoes"]) & df["data"].between(
    inicio, fim
)
df_filtrado = df[filtro]

if df_filtrado.empty:
    st.warning(
        "Nenhum dado para os filtros selecionados. Ajuste os filtros ou clique em (Resetar filtros)"
    )
    st.stop()

df_filtrado = recalcular_periodo(df_filtrado)

# ------------------------------------------------------------------
# Conteúdo
# ------------------------------------------------------------------
st.title("📈 Performance de Ações da B3 (2021-2023)")
st.caption(
    f"Fonte dos dados: {origem} - {len(df_filtrado):,} registros - "
    f"{inicio:%d/%m/%Y} a {fim:%d/%m/%Y}".replace(",", ".")
)

# Mostra os primeiros registros do DataFrame
st.dataframe(df_filtrado.head(20))
