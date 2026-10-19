"""
ETL -  Etapa 1: Extração

Cotações diárias de 12 ações da B3 via yfinance.
Período: 01/01/2021 a (31/12/2023 | 01/01/2024)
Local de armazenamento: data/raw/cotacoes_brutas.csv
"""

# Bibliotecas:
from pathlib import Path
import pandas as pd
import yfinance as yf

# Pasta RAIZ do projeto:
raiz = Path(__file__).resolve().parent.parent
# Local de armazenamento da consulta (Arquivo RAW):
pasta_raw = raiz / "data" / "raw"

# Nome das ações a serem extraídas:
lista_acao = [
    "WEGE3",
    "EMBJ3",  # Tive que trocar de (EMBR3 para EMBJ3) pois a Embraer mudou de código na B3: desde 3 de novembro de 2025
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

# Periodos de busca:
data_inicio = "2021-01-01"
data_final = "2024-01-01"  # 31/12/2023. Joguei um dia a mais para garantir que o intervalo seja total


def baixar_cotacoes(nome_acao):
    """Baixa o histórico dos ativos e devolve uma tabela"""
    df = yf.download(
        f"{nome_acao}.SA",  # .SA Indicativo da B3
        start=data_inicio,  # Data de início da busca
        end=data_final,  # Data de término da busca
        auto_adjust=False,  # Mantém os preços originais e traz a coluna "Adj Close" (fechamento ajustado por dividendos e desdobramentos)
        progress=False,  # Desliga a barra de progresso no terminal.
    )

    # Tratamento das colunas: se retornar as colunas agrupadas em dois níveis, achata as colunas para o formato padrão de um nível
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df = df.reset_index()  # transforma a data (que vem como índice) em coluna
    df["nome_acao"] = nome_acao
    return df  # Retorna um dataframe da consulta de cotações


def main():
    pasta_raw.mkdir(
        parents=True, exist_ok=True
    )  # Cria a pasta de destino se não existir
    tabelas = []  # Guarda as tabelas de cada ação

    for nome_acao in lista_acao:  # Loop para baixar cada uma das ações
        print(f"Baixando {nome_acao}...")  # Imprime o nome da ação
        df = baixar_cotacoes(nome_acao)  # Chama a função para baixar a cotação
        if df.empty:  # Verifica se a tabela está vazia
            print(
                f"  ATENÇÃO: nenhum dado retornado para {nome_acao}"
            )  # Imprime uma mensagem de aviso
            continue
        print(f"{len(df)} linhas")  # Imprime a quantidade de linhas da tabela
        tabelas.append(df)  # Adiciona a tabela à lista para concatenar no final

    base = pd.concat(tabelas, ignore_index=True)  # junta as 12 tabelas em uma só
    caminho = pasta_raw / "cotacoes_brutas.csv"  # Caminho para guardar o arquivo
    base.to_csv(caminho, index=False)  # Salva o arquivo no destino (sem index)

    print(
        f"\nArquivo salvo em: {caminho}"
    )  # Imprime o caminho onde o arquivo foi salvo
    print(
        f"Total: {len(base)} linhas | {base['nome_acao'].nunique()} ativos"
    )  # Imprime a quantidade de linhas e a quantidade de ativos


if __name__ == "__main__":
    main()
