import pandas as pd

from calculos import aplicar_calculos
from banco import salvar_localidades


COLUNAS_OBRIGATORIAS = [
    "localidade",
    "tipo_area",
    "populacao",
    "distancia_ubs_km",
    "saneamento_adequado",
    "risco_alagamento",
    "risco_queimadas",
    "casos_dengue",
    "familias_vulneraveis",
    "latitude",
    "longitude"
]


def ler_planilha(arquivo):
    """
    Lê arquivo CSV ou Excel enviado pelo usuário.
    """

    nome_arquivo = arquivo.name.lower()

    if nome_arquivo.endswith(".csv"):
        df = pd.read_csv(arquivo)
    elif nome_arquivo.endswith(".xlsx") or nome_arquivo.endswith(".xls"):
        df = pd.read_excel(arquivo)
    else:
        raise ValueError("Formato inválido. Envie um arquivo CSV ou Excel.")

    return df


def validar_colunas(df):
    """
    Verifica se a planilha possui todas as colunas obrigatórias.
    """

    colunas_arquivo = list(df.columns)

    colunas_faltando = [
        coluna for coluna in COLUNAS_OBRIGATORIAS
        if coluna not in colunas_arquivo
    ]

    if colunas_faltando:
        raise ValueError(
            "A planilha está sem as seguintes colunas obrigatórias: "
            + ", ".join(colunas_faltando)
        )


def tratar_dados(df):
    """
    Padroniza os dados da planilha antes de calcular o índice.
    """

    df = df.copy()

    validar_colunas(df)

    # Mantém somente as colunas necessárias
    df = df[COLUNAS_OBRIGATORIAS]

    # Remove linhas sem localidade
    df = df.dropna(subset=["localidade"])

    # Padroniza textos
    colunas_texto = [
        "localidade",
        "tipo_area",
        "saneamento_adequado",
        "risco_alagamento",
        "risco_queimadas"
    ]

    for coluna in colunas_texto:
        df[coluna] = df[coluna].astype(str).str.strip()

    # Converte números
    colunas_numericas = [
        "populacao",
        "distancia_ubs_km",
        "casos_dengue",
        "familias_vulneraveis",
        "latitude",
        "longitude"
    ]

    for coluna in colunas_numericas:
        df[coluna] = pd.to_numeric(df[coluna], errors="coerce")

    # Remove linhas com números essenciais ausentes
    df = df.dropna(subset=colunas_numericas)

    # Ajusta tipos
    df["populacao"] = df["populacao"].astype(int)
    df["casos_dengue"] = df["casos_dengue"].astype(int)
    df["familias_vulneraveis"] = df["familias_vulneraveis"].astype(int)

    return df


def importar_planilha(arquivo):
    """
    Processo completo:
    lê arquivo,
    valida colunas,
    trata dados,
    calcula vulnerabilidade,
    salva no banco.
    """

    df = ler_planilha(arquivo)
    df = tratar_dados(df)
    df = aplicar_calculos(df)

    salvar_localidades(df)

    return df