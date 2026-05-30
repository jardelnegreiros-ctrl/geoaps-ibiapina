def calcular_indice_vulnerabilidade(linha):
    """
    Calcula uma pontuação simples de vulnerabilidade territorial.

    Critérios usados:
    - Distância da UBS
    - Saneamento
    - Risco de alagamento
    - Risco de queimadas
    - Casos de dengue
    - Famílias vulneráveis
    - População
    """

    pontos = 0

    # Distância maior que 5 km aumenta vulnerabilidade
    if linha["distancia_ubs_km"] > 5:
        pontos += 2

    # Saneamento inadequado aumenta vulnerabilidade
    if linha["saneamento_adequado"] == "Não":
        pontos += 2

    # Risco alto de alagamento
    if linha["risco_alagamento"] == "Alto":
        pontos += 2
    elif linha["risco_alagamento"] == "Médio":
        pontos += 1

    # Risco alto de queimadas
    if linha["risco_queimadas"] == "Alto":
        pontos += 1

    # Muitos casos de dengue
    if linha["casos_dengue"] > 10:
        pontos += 2
    elif linha["casos_dengue"] >= 5:
        pontos += 1

    # Muitas famílias vulneráveis
    if linha["familias_vulneraveis"] > 30:
        pontos += 2
    elif linha["familias_vulneraveis"] >= 15:
        pontos += 1

    # População elevada
    if linha["populacao"] > 1000:
        pontos += 1

    return pontos


def classificar_risco(indice):
    """
    Classifica o risco a partir do índice calculado.
    """

    if indice >= 7:
        return "Alta"
    elif indice >= 4:
        return "Média"
    else:
        return "Baixa"


def definir_prioridade(classificacao):
    """
    Define prioridade de intervenção para a APS.
    """

    if classificacao == "Alta":
        return "Prioridade 1 - Intervenção imediata"
    elif classificacao == "Média":
        return "Prioridade 2 - Monitoramento intensivo"
    else:
        return "Prioridade 3 - Acompanhamento regular"


def aplicar_calculos(df):
    """
    Aplica os cálculos de vulnerabilidade em todo o DataFrame.
    """

    df = df.copy()

    df["indice_vulnerabilidade"] = df.apply(
        calcular_indice_vulnerabilidade,
        axis=1
    )

    df["classificacao_risco"] = df["indice_vulnerabilidade"].apply(
        classificar_risco
    )

    df["prioridade_intervencao"] = df["classificacao_risco"].apply(
        definir_prioridade
    )

    return df


if __name__ == "__main__":
    import pandas as pd

    dados_teste = pd.DataFrame([
        {
            "localidade": "Teste",
            "tipo_area": "Rural",
            "populacao": 1200,
            "distancia_ubs_km": 8.5,
            "saneamento_adequado": "Não",
            "risco_alagamento": "Alto",
            "risco_queimadas": "Alto",
            "casos_dengue": 15,
            "familias_vulneraveis": 40,
            "latitude": -3.923,
            "longitude": -40.889
        }
    ])

    resultado = aplicar_calculos(dados_teste)

    print(resultado[[
        "localidade",
        "indice_vulnerabilidade",
        "classificacao_risco",
        "prioridade_intervencao"
    ]])