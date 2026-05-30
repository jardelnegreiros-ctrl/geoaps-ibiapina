import pandas as pd
from pathlib import Path


PASTA_PROJETO = Path(__file__).resolve().parent
PASTA_EXPORTS = PASTA_PROJETO / "exports"
PASTA_EXPORTS.mkdir(exist_ok=True)


def criar_modelo():
    dados = [
        {
            "localidade": "Exemplo Centro",
            "tipo_area": "Urbana",
            "populacao": 1000,
            "distancia_ubs_km": 1.2,
            "saneamento_adequado": "Sim",
            "risco_alagamento": "Baixo",
            "risco_queimadas": "Baixo",
            "casos_dengue": 2,
            "familias_vulneraveis": 10,
            "latitude": -3.9234,
            "longitude": -40.8898
        },
        {
            "localidade": "Exemplo Rural",
            "tipo_area": "Rural",
            "populacao": 500,
            "distancia_ubs_km": 8.5,
            "saneamento_adequado": "Não",
            "risco_alagamento": "Médio",
            "risco_queimadas": "Alto",
            "casos_dengue": 8,
            "familias_vulneraveis": 30,
            "latitude": -3.9650,
            "longitude": -40.9050
        }
    ]

    df = pd.DataFrame(dados)

    caminho_excel = PASTA_EXPORTS / "modelo_importacao_geoaps.xlsx"
    caminho_csv = PASTA_EXPORTS / "modelo_importacao_geoaps.csv"

    df.to_excel(caminho_excel, index=False)
    df.to_csv(caminho_csv, index=False, encoding="utf-8-sig")

    print("Modelos criados com sucesso:")
    print(caminho_excel)
    print(caminho_csv)


if __name__ == "__main__":
    criar_modelo()