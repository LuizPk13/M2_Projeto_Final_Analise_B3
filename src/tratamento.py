"""
ETL - Etapa 2: Tratamento
Aplica as decições investigadas em notebook/01_tratamento.ipynb
Entrada: data/raw/cotacoes_brutas.csv
Saída: data/processed/cotacoes_limpas.csv
"""

# Bibliotecas
from pathlib import Path
import pandas as pd

# Pasta RAIZ do projeto:
raiz = Path(__file__).resolve().parent.parent
# Local do arquivo bruto:
arquivo_bruto = raiz / "data" / "raw" / "cotacoes_brutas.csv"
# Local do arquivo tratado:
pasta_processed = raiz / "data" / "processed"

# Para renomear as colunas:
nome_colunas = {
    "Date": "data",
    "Adj Close": "fechamento_ajustado",
    "Close": "fechamento",
    "High": "maxima",
    "Low": "minima",
    "Open": "abertura",
    "Volume": "volume",
}

# Para corrigir casas decimais:
colunas_precos = [
    "fechamento",
    "maxima",
    "minima",
    "abertura",
]


# Motrando linhas duplicadas, nulas e volumes zerados da base:
def diagnostico(df, titulo):
    print(f"\n===== {titulo} =====")
    print(f"Linhas: {len(df)} | Ativos: {df["nome_acao"].nunique()}")
    print(
        f"Duplicados (data + nome_acao): {df.duplicated(subset=["data", "nome_acao"]).sum()}"
    )
    print(f"Nulos no total: {df.isna().sum().sum()}")
    print(f"Dias com volume zero: {(df["volume"] == 0).sum()}")


# Aplicando as etapas de tratamento e devolvendo a base limpa:
def tratar(df):
    # 1. Nome das colunas para português:
    df.rename(columns=nome_colunas, inplace=True)
    # 2. Corrigindo o tipo da coluna data str para datetime:
    df["data"] = pd.to_datetime(df["data"], errors="coerce")

    # 3. Garantido que todas as colunas numéricas continuem sendo numéricas:
    for colunas in colunas_precos + ["fechamento_ajustado", "volume"]:
        df[colunas] = pd.to_numeric(df[colunas], errors="coerce")

    # 4. Duplicados: mantem apenas um registro por ação por dia:
    df = df.drop_duplicates(subset=["data", "nome_acao"], keep="last")

    # 5. Nulos: sem data ou sem preço ajustado não servem para os cálculos:
    df = df.dropna(subset=["data", "fechamento_ajustado"])

    # 6. Preços invélidos: (zeros ou negativos)
    df = df[df["fechamento_ajustado"] > 0]

    # 7. Arredondando os para duas casas decimais:
    df[colunas_precos] = df[colunas_precos].round(2)

    # # 8. Volume nulo vira 0; os 3 dias com volume zero são MANTIDOS (ver notebook):
    df["volume"] = df["volume"].fillna(0).astype("int64")

    # 9. Ordena por ação e data e reseta o índice:
    return df.sort_values(["nome_acao", "data"]).reset_index(drop=True)


# Leitura do arquivo bruto e tratamento:
def main():
    # Leitura do arquivo bruto:
    df_raw = pd.read_csv(arquivo_bruto, sep=",", decimal=".", encoding="utf-8")
    # Aplicando diagnosticos:
    diagnostico(df_raw.rename(columns=nome_colunas), "ANTES")

    # Aplicando as etapas de tratamento:
    df = tratar(df_raw)
    diagnostico(df, "DEPOIS")

    # Salvando o arquivo tratado:
    pasta_processed.mkdir(parents=True, exist_ok=True)
    caminho = pasta_processed / "cotacoes_limpas.csv"
    df.to_csv(caminho, index=False)

    print(f"\nArquivo salvo em: {caminho}")


# Executa o main() apenas quando o arquivo é rodado diretamente
if __name__ == "__main__":
    main()
