"""
ETL -  Etapa 1: Extração

Cotações diárias de 12 ações da B3 via yfinance.
Período: 01/01/2021 a (31/12/2023 | 01/01/2024)
Local de armazenamento: data/raw/cotacoes_brutas.csv
"""

from pathlib import Path
import pandas as pd
import yfinance as yf

# Pasta RAIZ do projeto:
raiz = Path(__file__).resolve().parent.parent
# Pasta PASTA_RAW do projeto:
pasta_raw = raiz / "data" / "raw"

# Nome das ações a serem extraídas:
lista_acao = [
    "WEGE3",
    "EMBR3",
    "VALE3",
    "GGBR4",
    "KLBN11",
    "PETR4",
    "PRIO3",
    "EGIE3",
    "ITUB4",
    "BBDC4",
    "ABEV3",
    "RENT3",
]

# Periodo da busca:
data_inicio = "2021-01-01"
data_final = "2024-01-01"


def baixar_cotacoes(nome_acao):
    """Baixa o histórico de um ativo e devolve uma tabela com a coluna nome_acao."""
    df = yf.download(
        f"{nome_acao}.SA",
        start=data_inicio,
        end=data_final,
        auto_adjust=False,
        progress=False,
    )

    # Em algumas versões o yfinance devolve colunas em dois níveis; aqui deixamos em um só
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df = df.reset_index()  # transforma a data (que vem como índice) em coluna
    df["nome_acao"] = nome_acao
    return df


def main():
    pasta_raw.mkdir(parents=True, exist_ok=True)
    tabelas = []

    for nome_acao in lista_acao:
        print(f"Baixando {nome_acao}...")
        df = baixar_cotacoes(nome_acao)
        if df.empty:
            print(f"  ATENÇÃO: nenhum dado retornado para {nome_acao}")
            continue
        print(f"  {len(df)} linhas")
        tabelas.append(df)

    base = pd.concat(tabelas, ignore_index=True)  # junta as 12 tabelas em uma só
    caminho = pasta_raw / "cotacoes_brutas.csv"
    base.to_csv(caminho, index=False)

    print(f"\nArquivo salvo em: {caminho}")
    print(f"Total: {len(base)} linhas | {base['nome_acao'].nunique()} ativos")


if __name__ == "__main__":
    main()
