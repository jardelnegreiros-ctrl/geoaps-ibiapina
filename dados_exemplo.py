import pandas as pd

from calculos import aplicar_calculos
from banco import salvar_localidades, carregar_localidades


def criar_dados_exemplo():
    """
    Cria dados fictícios/didáticos de localidades de Ibiapina.
    Esses dados servem para testar o painel GeoAPS.
    """

    dados = [
        {
            "localidade": "Centro",
            "tipo_area": "Urbana",
            "populacao": 5200,
            "distancia_ubs_km": 0.5,
            "saneamento_adequado": "Sim",
            "risco_alagamento": "Médio",
            "risco_queimadas": "Baixo",
            "casos_dengue": 18,
            "familias_vulneraveis": 35,
            "latitude": -3.9234,
            "longitude": -40.8898
        },
        {
            "localidade": "Pedrinhas",
            "tipo_area": "Urbana",
            "populacao": 1800,
            "distancia_ubs_km": 2.0,
            "saneamento_adequado": "Parcial",
            "risco_alagamento": "Médio",
            "risco_queimadas": "Baixo",
            "casos_dengue": 12,
            "familias_vulneraveis": 28,
            "latitude": -3.9185,
            "longitude": -40.8955
        },
        {
            "localidade": "Alto Lindo",
            "tipo_area": "Urbana",
            "populacao": 1500,
            "distancia_ubs_km": 2.8,
            "saneamento_adequado": "Parcial",
            "risco_alagamento": "Baixo",
            "risco_queimadas": "Médio",
            "casos_dengue": 8,
            "familias_vulneraveis": 22,
            "latitude": -3.9290,
            "longitude": -40.8840
        },
        {
            "localidade": "São José",
            "tipo_area": "Urbana",
            "populacao": 1200,
            "distancia_ubs_km": 3.5,
            "saneamento_adequado": "Parcial",
            "risco_alagamento": "Baixo",
            "risco_queimadas": "Médio",
            "casos_dengue": 6,
            "familias_vulneraveis": 18,
            "latitude": -3.9260,
            "longitude": -40.8780
        },
        {
            "localidade": "Pindoba",
            "tipo_area": "Rural",
            "populacao": 850,
            "distancia_ubs_km": 7.2,
            "saneamento_adequado": "Não",
            "risco_alagamento": "Médio",
            "risco_queimadas": "Alto",
            "casos_dengue": 5,
            "familias_vulneraveis": 26,
            "latitude": -3.9500,
            "longitude": -40.9100
        },
        {
            "localidade": "Sítio Santa Tereza",
            "tipo_area": "Rural",
            "populacao": 700,
            "distancia_ubs_km": 9.5,
            "saneamento_adequado": "Não",
            "risco_alagamento": "Baixo",
            "risco_queimadas": "Alto",
            "casos_dengue": 4,
            "familias_vulneraveis": 32,
            "latitude": -3.9650,
            "longitude": -40.9050
        },
        {
            "localidade": "Sítio Vereda",
            "tipo_area": "Rural",
            "populacao": 620,
            "distancia_ubs_km": 10.8,
            "saneamento_adequado": "Não",
            "risco_alagamento": "Médio",
            "risco_queimadas": "Alto",
            "casos_dengue": 7,
            "familias_vulneraveis": 34,
            "latitude": -3.9750,
            "longitude": -40.9200
        },
        {
            "localidade": "Sítio Boa Vista",
            "tipo_area": "Rural",
            "populacao": 540,
            "distancia_ubs_km": 8.3,
            "saneamento_adequado": "Não",
            "risco_alagamento": "Baixo",
            "risco_queimadas": "Médio",
            "casos_dengue": 3,
            "familias_vulneraveis": 21,
            "latitude": -3.9400,
            "longitude": -40.9300
        },
        {
            "localidade": "Sítio Laranjeiras",
            "tipo_area": "Rural",
            "populacao": 480,
            "distancia_ubs_km": 11.6,
            "saneamento_adequado": "Não",
            "risco_alagamento": "Alto",
            "risco_queimadas": "Alto",
            "casos_dengue": 11,
            "familias_vulneraveis": 38,
            "latitude": -3.9850,
            "longitude": -40.9000
        },
        {
            "localidade": "Sítio Cajueiro",
            "tipo_area": "Rural",
            "populacao": 390,
            "distancia_ubs_km": 12.4,
            "saneamento_adequado": "Não",
            "risco_alagamento": "Médio",
            "risco_queimadas": "Alto",
            "casos_dengue": 9,
            "familias_vulneraveis": 29,
            "latitude": -3.9900,
            "longitude": -40.9150
        }
    ]

    df = pd.DataFrame(dados)

    df = aplicar_calculos(df)

    return df


if __name__ == "__main__":
    df = criar_dados_exemplo()

    salvar_localidades(df)

    print("Dados de exemplo criados e salvos com sucesso.")
    print("\nLocalidades cadastradas:")
    print(df[[
        "localidade",
        "tipo_area",
        "populacao",
        "indice_vulnerabilidade",
        "classificacao_risco",
        "prioridade_intervencao"
    ]])

    print("\nDados salvos no banco:")
    df_banco = carregar_localidades()
    print(df_banco.head())