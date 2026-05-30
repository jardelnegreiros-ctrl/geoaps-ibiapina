from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px
import pydeck as pdk

from banco import carregar_localidades, salvar_localidades, CAMINHO_BANCO
from dados_exemplo import criar_dados_exemplo
from importador import importar_planilha, COLUNAS_OBRIGATORIAS


PASTA_PROJETO = Path(__file__).resolve().parent
PASTA_EXPORTS = PASTA_PROJETO / "exports"
PASTA_EXPORTS.mkdir(exist_ok=True)


st.set_page_config(
    page_title="GeoAPS Ibiapina",
    page_icon="🗺️",
    layout="wide"
)


st.title("🗺️ GeoAPS Ibiapina")
st.write(
    "Painel de territorialização, vulnerabilidade ambiental e inteligência geográfica "
    "para apoio à Atenção Primária à Saúde."
)

st.info(f"Banco usado: {CAMINHO_BANCO}")


with st.sidebar:
    st.header("Controles")

    carregar_exemplo = st.button(
        "Carregar dados de exemplo",
        use_container_width=True
    )

    st.divider()

    st.subheader("Importar planilha")

    arquivo_importado = st.file_uploader(
        "Envie um arquivo CSV ou Excel",
        type=["csv", "xlsx", "xls"]
    )

    importar = st.button(
        "Importar planilha",
        use_container_width=True
    )

    with st.expander("Ver colunas obrigatórias"):
        st.write(COLUNAS_OBRIGATORIAS)

    modelo_path = PASTA_EXPORTS / "modelo_importacao_geoaps.xlsx"

    if modelo_path.exists():
        with open(modelo_path, "rb") as modelo:
            st.download_button(
                label="Baixar modelo Excel",
                data=modelo,
                file_name="modelo_importacao_geoaps.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
    else:
        st.info("Rode python modelo_planilha.py para gerar o modelo Excel.")

    st.divider()

    st.subheader("Sobre o projeto")
    st.write("Município: Ibiapina - Ceará")
    st.write("Tema: Territorialização em Saúde")
    st.write("Aplicação: Atenção Primária à Saúde")


if carregar_exemplo:
    df_exemplo = criar_dados_exemplo()
    salvar_localidades(df_exemplo)
    st.success("Dados de exemplo carregados com sucesso!")


if importar:
    if arquivo_importado is None:
        st.warning("Envie uma planilha antes de clicar em importar.")
    else:
        try:
            df_importado = importar_planilha(arquivo_importado)
            st.success(
                f"Planilha importada com sucesso! "
                f"{len(df_importado)} localidades foram processadas."
            )
        except ValueError as erro:
            st.error(str(erro))
        except Exception as erro:
            st.error(f"Erro inesperado ao importar a planilha: {erro}")


df = carregar_localidades()


if df.empty:
    st.warning(
        "Nenhuma localidade cadastrada ainda. "
        "Clique em 'Carregar dados de exemplo' na barra lateral."
    )
    st.stop()


# =========================
# FILTROS
# =========================

st.sidebar.subheader("Filtros")

tipos_area = sorted(df["tipo_area"].dropna().unique())
riscos = sorted(df["classificacao_risco"].dropna().unique())

tipos_selecionados = st.sidebar.multiselect(
    "Tipo de área",
    tipos_area,
    default=tipos_area
)

riscos_selecionados = st.sidebar.multiselect(
    "Classificação de risco",
    riscos,
    default=riscos
)


df_filtrado = df[
    (df["tipo_area"].isin(tipos_selecionados)) &
    (df["classificacao_risco"].isin(riscos_selecionados))
].copy()


if df_filtrado.empty:
    st.warning("Nenhuma localidade encontrada com os filtros selecionados.")
    st.stop()


# =========================
# CARDS PRINCIPAIS
# =========================

total_localidades = len(df_filtrado)
populacao_total = int(df_filtrado["populacao"].sum())
alta_vulnerabilidade = len(df_filtrado[df_filtrado["classificacao_risco"] == "Alta"])
casos_dengue = int(df_filtrado["casos_dengue"].sum())


col1, col2, col3, col4 = st.columns(4)

col1.metric("Localidades analisadas", total_localidades)
col2.metric("População estimada", f"{populacao_total:,}".replace(",", "."))
col3.metric("Áreas de alta vulnerabilidade", alta_vulnerabilidade)
col4.metric("Casos de dengue informados", casos_dengue)


st.divider()


# =========================
# RANKING
# =========================

st.subheader("Ranking de vulnerabilidade territorial")

ranking = df_filtrado.sort_values(
    ["indice_vulnerabilidade", "populacao"],
    ascending=[False, False]
)

st.dataframe(
    ranking[[
        "localidade",
        "tipo_area",
        "populacao",
        "distancia_ubs_km",
        "casos_dengue",
        "familias_vulneraveis",
        "indice_vulnerabilidade",
        "classificacao_risco",
        "prioridade_intervencao"
    ]],
    use_container_width=True
)


# =========================
# GRÁFICOS
# =========================

col_g1, col_g2 = st.columns(2)

with col_g1:
    st.subheader("Localidades por classificação de risco")

    risco_contagem = (
        df_filtrado.groupby("classificacao_risco")
        .size()
        .reset_index(name="quantidade")
    )

    fig_risco = px.bar(
        risco_contagem,
        x="classificacao_risco",
        y="quantidade",
        text="quantidade",
        title="Quantidade de localidades por risco"
    )

    st.plotly_chart(fig_risco, use_container_width=True)


with col_g2:
    st.subheader("População por tipo de área")

    pop_tipo = (
        df_filtrado.groupby("tipo_area")["populacao"]
        .sum()
        .reset_index()
    )

    fig_tipo = px.pie(
        pop_tipo,
        names="tipo_area",
        values="populacao",
        title="Distribuição populacional por tipo de área"
    )

    st.plotly_chart(fig_tipo, use_container_width=True)


st.subheader("Top localidades por índice de vulnerabilidade")

top_vulnerabilidade = ranking.head(10)

fig_top = px.bar(
    top_vulnerabilidade,
    x="indice_vulnerabilidade",
    y="localidade",
    orientation="h",
    text="indice_vulnerabilidade",
    title="Ranking das localidades mais vulneráveis"
)

fig_top.update_layout(yaxis={"categoryorder": "total ascending"})

st.plotly_chart(fig_top, use_container_width=True)


# =========================
# MAPA
# =========================

st.subheader("Mapa territorial das localidades")

mapa_df = df_filtrado.dropna(subset=["latitude", "longitude"]).copy()

if mapa_df.empty:
    st.warning("Não há coordenadas disponíveis para exibir o mapa.")
else:
    mapa_df["cor_r"] = mapa_df["classificacao_risco"].map({
        "Alta": 220,
        "Média": 255,
        "Baixa": 60
    }).fillna(120)

    mapa_df["cor_g"] = mapa_df["classificacao_risco"].map({
        "Alta": 60,
        "Média": 180,
        "Baixa": 180
    }).fillna(120)

    mapa_df["cor_b"] = mapa_df["classificacao_risco"].map({
        "Alta": 60,
        "Média": 60,
        "Baixa": 90
    }).fillna(120)

    mapa_df["raio"] = mapa_df["populacao"].apply(
        lambda x: max(80, min(x * 0.8, 1000))
    )

    view_state = pdk.ViewState(
        latitude=float(mapa_df["latitude"].mean()),
        longitude=float(mapa_df["longitude"].mean()),
        zoom=11,
        pitch=0
    )

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=mapa_df,
        get_position="[longitude, latitude]",
        get_radius="raio",
        get_fill_color="[cor_r, cor_g, cor_b, 180]",
        pickable=True,
        auto_highlight=True
    )

    tooltip = {
        "html": """
        <b>{localidade}</b><br/>
        Tipo: {tipo_area}<br/>
        População: {populacao}<br/>
        Índice: {indice_vulnerabilidade}<br/>
        Risco: {classificacao_risco}<br/>
        Prioridade: {prioridade_intervencao}
        """,
        "style": {
            "backgroundColor": "steelblue",
            "color": "white"
        }
    }

    deck = pdk.Deck(
        map_style=None,
        initial_view_state=view_state,
        layers=[layer],
        tooltip=tooltip
    )

    st.pydeck_chart(deck)

    st.caption(
        "Cores do mapa: vermelho = alta vulnerabilidade, amarelo/laranja = média, verde = baixa."
    )


# =========================
# TABELA COMPLETA
# =========================

st.subheader("Base territorial completa")

st.dataframe(df_filtrado, use_container_width=True)


# =========================
# EXPORTAÇÃO
# =========================

st.subheader("Exportar dados")

excel_path = PASTA_EXPORTS / "geoaps_ibiapina.xlsx"
df_filtrado.to_excel(excel_path, index=False)

with open(excel_path, "rb") as arquivo:
    st.download_button(
        label="Baixar Excel",
        data=arquivo,
        file_name="geoaps_ibiapina.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

csv = df_filtrado.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Baixar CSV",
    data=csv,
    file_name="geoaps_ibiapina.csv",
    mime="text/csv"
)


# =========================
# INTERPRETAÇÃO
# =========================

st.divider()

st.subheader("Interpretação para a gestão em saúde")

st.write(
    """
    Este painel permite identificar localidades com maior vulnerabilidade territorial,
    considerando fatores ambientais, sociais e assistenciais. As áreas classificadas
    como alta vulnerabilidade podem ser priorizadas para ações da Atenção Primária,
    vigilância em saúde, visitas domiciliares, educação em saúde e planejamento
    intersetorial.
    """
)