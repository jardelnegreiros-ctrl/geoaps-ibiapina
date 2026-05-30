# GeoAPS

Painel de Territorialização, Vulnerabilidade Ambiental e Inteligência Geográfica para apoio à Atenção Primária à Saúde no município de Ibiapina, Ceará.

## Objetivo

Este projeto tem como objetivo apoiar a territorialização em saúde no município de Ibiapina, integrando dados territoriais, ambientais e de saúde pública para identificar localidades com maior vulnerabilidade e auxiliar a tomada de decisão na Atenção Primária à Saúde.

O painel permite visualizar localidades, população, distância até UBS, saneamento, risco de alagamento, risco de queimadas, casos de dengue, famílias vulneráveis e classificação de risco territorial.

## Município de análise

- Município: Ibiapina
- Estado: Ceará
- País: Brasil
- Tema: Territorialização em saúde
- Aplicação: Atenção Primária à Saúde

## Tecnologias utilizadas

- Python
- Pandas
- SQLite
- Streamlit
- Plotly
- PyDeck
- OpenPyXL

## Funcionalidades

- Cadastro e leitura de localidades
- Geração de dados de exemplo
- Cálculo de índice de vulnerabilidade territorial
- Classificação de risco: baixa, média e alta
- Priorização de intervenção para APS
- Dashboard com indicadores principais
- Ranking de vulnerabilidade
- Gráficos por classificação de risco
- Gráficos por tipo de área
- Mapa interativo das localidades
- Tabela completa dos dados
- Exportação para Excel
- Exportação para CSV
- Execução local no Windows com arquivo .bat

## Índice de vulnerabilidade territorial

O índice considera fatores como:

- Distância até a UBS
- Saneamento inadequado
- Risco de alagamento
- Risco de queimadas
- Casos de dengue
- Famílias vulneráveis
- População da localidade

Classificação utilizada:

```text
0 a 3 pontos   → Baixa vulnerabilidade
4 a 6 pontos   → Média vulnerabilidade
7 ou mais      → Alta vulnerabilidade
```

## Aplicação em saúde pública

O GeoAPS pode apoiar:

* Territorialização das equipes de Saúde da Família
* Identificação de áreas vulneráveis
* Planejamento de visitas domiciliares
* Priorização de ações da APS
* Monitoramento de riscos ambientais
* Vigilância de arboviroses
* Planejamento intersetorial
* Apoio à gestão municipal de saúde
