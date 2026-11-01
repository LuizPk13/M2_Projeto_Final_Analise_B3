"""
ETL - Etapa 3: Métricas
Aplica os cálculos validados em notebooks/02_metricas.ipynb.
Entrada: data/processed/cotacoes_limpas.csv
Saída: data/processed/cotacoes_metricas.csv
"""
from pathlib import Path

import pandas as pd

raiz = Path(__file__).resolve().parent.parent
arquivo_limpo = raiz / "data" / "processed" / "cotacoes_limpas.csv"
arquivo_metricas = raiz / "data" / "processed" / "cotacoes_metricas.csv"

setores = {
    "WEGE3": "Bens Industriais",
    "EMBJ3": "Bens Industriais",
    "ABEV3": "Consumo",
    "RENT3": "Consumo",
    "BBDC4": "Financeiro",
    "ITUB4": "Financeiro",
    "GGBR4": "Material Basico",
    "KLBN11": "Material Basico",
    "VALE3": "Material Basico",
    "EGIE3": "Petroleo Energia",
    "PETR4": "Petroleo Energia",
    "PRIO3": "Petroleo Energia",
}


def calcular_metricas(df):
    """Adiciona setor e métricas financeiras diárias a cada ação."""
    df = df.sort_values(["nome_acao", "data"]).reset_index(drop=True)
    preco = df.groupby("nome_acao")["fechamento_ajustado"]

    df["setor"] = df["nome_acao"].map(setores)
    df["volume_financeiro"] = df["volume"] * df["fechamento"]
    df["retorno_diario"] = preco.pct_change()
    df["base_100"] = df["fechamento_ajustado"] / preco.transform("first") * 100
    df["retorno_acumulado"] = df["base_100"] / 100 - 1
    df["drawdown"] = df["fechamento_ajustado"] / preco.cummax() - 1
    df["sma_21"] = preco.transform(lambda s: s.rolling(21).mean())
    df["sma_50"] = preco.transform(lambda s: s.rolling(50).mean())
    return df


def main():
    df = pd.read_csv(arquivo_limpo)
    df["data"] = pd.to_datetime(df["data"])

    df = calcular_metricas(df)

    # Conferências rápidas
    print(f"Linhas: {len(df)} | Colunas: {len(df.columns)}")
    print(f"Ações sem setor: {df['setor'].isna().sum()}")
    print(f"Maior drawdown (deve ser 0): {df['drawdown'].max()}")

    df.to_csv(arquivo_metricas, index=False)
    print(f"Arquivo salvo em: {arquivo_metricas}")


# Executa o main() apenas quando o arquivo é rodado diretamente
if __name__ == "__main__":
    main()