"""
ETL - Etapa 4: Carga
Envia a base com métricas para o PostgreSQL do Supabase
Entrada: data/processed/contacoes_metricas.csv
Destino: tabela "cotacoes" no Supabase
Credenciais: .streamlit/secrets.toml (fora do Github)
"""

import tomllib
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

raiz = Path(__file__).resolve().parent.parent
arquivo_metricas = raiz / "data" / "processed" / "cotacoes_metricas.csv"
arquivo_secrets = raiz / ".streamlit" / "secrets.toml"


def main():
    # Lê o endereço do banco direto do secrets.toml

    with open(arquivo_secrets, "rb") as f:
        url = tomllib.load(f)["connections"]["postgresql"]["url"]
    engine = create_engine(url)

    # 1. Teste de conexão
    with engine.connect() as conexao:
        conexao.execute(text("SELECT 1"))
    print("Conexão com o Supabase: OK")

    # 2. Envio da base (Substitui a tabela se ela já existir)
    df = pd.read_csv(arquivo_metricas, parse_dates=["data"])
    df.to_sql(
        "cotacoes",
        engine,
        if_exists="replace",
        index=False,
        chunksize=1000,
        method="multi",
    )

    # 3. Conferência: conta as linhas que chegaram no banco
    with engine.connect() as conexao:
        total = conexao.execute(text("SELECT COUNT(*) FROM cotacoes")).scalar()
    print(f"Linhas no CSV: {len(df)} | Linhas no banco: {total}")


# Executa o main() apenas quando o arquivo é rodado diretamente
if __name__ == "__main__":
    main()
