"""
Data App - Análise de Performance de Ações da B3 (2021-2023)
"""

# Bibliotecas
from pathlib import Path
import pandas as pd
import streamlit as st

# Configurações da página
st.set_page_config(page_title="Anélise B3 2021-2023", page_icon="📈", layout="wide")

# Caminho dos arquivos
raiz = Path(__file__).resolve().parent
arquivo_contingencia = raiz / "data" / "processed" / "cotacoes_metricas.csv"


# Carrega os dados do Supabase ou do CSV local (em caso de contingência)
@st.cache_data(ttl=3600, show_spinner="Carregando Dados...")
def carregar_dados():
    """Lê o Supabase; se o banco estiver indisponível, lê o CSV local."""

    try:  # Tenta ler do Supabase
        conn = st.connection("postgresql", type="sql")
        df = conn.query("SELECT * FROM cotacoes", ttl=3600)
        origem = "Supabase (PostgreSQL)"
    except:  # Se houver erro, lê o CSV local
        df = pd.read_csv(arquivo_contingencia)
        origem = "CSV local (Contingência)"

    # Converte a coluna "data" para datetime
    df["data"] = pd.to_datetime(df["data"])
    return df, origem


# Desempacota o DataFrame e a origem dos dados
df, origem = carregar_dados()

# Título e legenda do app
st.title("📈 Performance de Ações da B3 (2021-2023)")
st.caption(f"Fonte dos dados: {origem} - {len(df):,} registros".replace(",", "."))

# Mostra os primeiros registros do DataFrame
st.dataframe(df.head(20))
