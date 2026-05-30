import sqlite3
import pandas as pd
from pathlib import Path


PASTA_PROJETO = Path(__file__).resolve().parent
PASTA_DADOS = PASTA_PROJETO / "dados"
PASTA_DADOS.mkdir(exist_ok=True)

CAMINHO_BANCO = PASTA_DADOS / "geoaps.db"


def conectar():
    return sqlite3.connect(CAMINHO_BANCO)


def criar_tabela():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS localidades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            localidade TEXT UNIQUE,
            tipo_area TEXT,
            populacao INTEGER,
            distancia_ubs_km REAL,
            saneamento_adequado TEXT,
            risco_alagamento TEXT,
            risco_queimadas TEXT,
            casos_dengue INTEGER,
            familias_vulneraveis INTEGER,
            latitude REAL,
            longitude REAL,
            indice_vulnerabilidade INTEGER,
            classificacao_risco TEXT,
            prioridade_intervencao TEXT,
            atualizado_em TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conexao.commit()
    conexao.close()


def salvar_localidades(df):
    criar_tabela()
    conexao = conectar()

    for _, linha in df.iterrows():
        conexao.execute("""
            INSERT OR REPLACE INTO localidades (
                localidade,
                tipo_area,
                populacao,
                distancia_ubs_km,
                saneamento_adequado,
                risco_alagamento,
                risco_queimadas,
                casos_dengue,
                familias_vulneraveis,
                latitude,
                longitude,
                indice_vulnerabilidade,
                classificacao_risco,
                prioridade_intervencao
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            linha["localidade"],
            linha["tipo_area"],
            int(linha["populacao"]),
            float(linha["distancia_ubs_km"]),
            linha["saneamento_adequado"],
            linha["risco_alagamento"],
            linha["risco_queimadas"],
            int(linha["casos_dengue"]),
            int(linha["familias_vulneraveis"]),
            float(linha["latitude"]),
            float(linha["longitude"]),
            int(linha["indice_vulnerabilidade"]),
            linha["classificacao_risco"],
            linha["prioridade_intervencao"]
        ))

    conexao.commit()
    conexao.close()


def carregar_localidades():
    criar_tabela()
    conexao = conectar()

    df = pd.read_sql_query("""
        SELECT
            id,
            localidade,
            tipo_area,
            populacao,
            distancia_ubs_km,
            saneamento_adequado,
            risco_alagamento,
            risco_queimadas,
            casos_dengue,
            familias_vulneraveis,
            latitude,
            longitude,
            indice_vulnerabilidade,
            classificacao_risco,
            prioridade_intervencao,
            atualizado_em
        FROM localidades
        ORDER BY indice_vulnerabilidade DESC, populacao DESC
    """, conexao)

    conexao.close()
    return df


if __name__ == "__main__":
    criar_tabela()
    print("Banco GeoAPS criado/verificado com sucesso.")
    print("Banco usado:", CAMINHO_BANCO)