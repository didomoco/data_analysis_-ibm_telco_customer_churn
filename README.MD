# Customer Churn Analytics

Projeto de análise de churn de clientes com Python, SQL, notebooks Jupyter e dashboard em Streamlit.

Este repositório combina análise exploratória, investigação com SQL e uma aplicação interativa para mostrar quais perfis de clientes apresentam maior propensão ao cancelamento em uma base de telecom (Dataset público Telco -IBM).

## Visão Geral

O projeto foi estruturado para responder perguntas como:

- Qual é a taxa geral de churn?
- Quais perfis de clientes apresentam maior risco de cancelamento?
- Como tipo de contrato, cobrança mensal e tempo de permanência se relacionam com churn?
- Como explorar esses padrões tanto em notebooks quanto em um dashboard interativo?

## Stack

- Python
- pandas
- numpy
- matplotlib
- seaborn
- plotly
- Streamlit
- Jupyter Notebook
- SQL
- sqlite3 para validação local das consultas

## Fonte dos Dados

- Arquivo local: `data/churn.csv`
- Fallback remoto usado pelos scripts de carga:
  `https://raw.githubusercontent.com/blastchar/telco-customer-churn/master/WA_Fn-UseC_-Telco-Customer-Churn.csv`

O arquivo local é a fonte principal das análises e do dashboard. O fallback remoto ajuda a manter o projeto executável caso o CSV não esteja disponível localmente.

## Estrutura do Repositório

- `app.py`: dashboard em Streamlit para análise interativa de churn
- `acesso_banco.py`: script simples de carga de dados com fallback local e remoto
- `data/churn.csv`: base de churn usada no projeto
- `notebooks/analysis.ipynb`: análise exploratória e visualizações
- `notebooks/sql_tests.ipynb`: validação das consultas SQL com `sqlite3`
- `sql/queries.sql`: consultas SQL principais da análise
- `requirements.txt`: dependências Python do projeto

## Funcionalidades do Dashboard

- KPIs com total de clientes, taxa de churn, média de cobrança mensal e média de permanência
- filtros por tipo de contrato, serviço de internet e método de pagamento
- comparativo de churn por contrato
- distribuição de cobrança mensal por churn
- distribuição de tenure por churn
- visualização tabular dos dados filtrados

## Como Executar

1. Crie e ative um ambiente virtual.
2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Execute o dashboard:

```bash
streamlit run app.py
```

4. Para explorar os notebooks, inicie o Jupyter:

```bash
jupyter notebook
```

## Observações Técnicas

- `sqlite3` não precisa ser instalado separadamente, pois faz parte da biblioteca padrão do Python.
- O dashboard usa a base local por padrão e tenta manter o fluxo utilizável com fallback remoto.
- O projeto pode ser expandido futuramente com modelagem preditiva, engenharia de atributos e automação de deploy.

## Valor do Projeto

Para recrutadores:
este repositório demonstra organização de projeto analítico, leitura de indicadores de negócio, exploração de dados, consultas SQL e tradução de insights em uma interface interativa.

Para devs e analistas:
o projeto serve como base para evolução com segmentação de clientes, previsão de churn, testes das consultas e melhorias de produto no dashboard.

---

## English Version

Customer churn analysis project built with Python, SQL, Jupyter notebooks, and a Streamlit dashboard.

This repository combines exploratory analysis, SQL-based investigation, and an interactive application to show which customer profiles are more likely to cancel a telecom service by IBM Telco public dataset.

## Project Overview

The project is structured to answer questions such as:

- What is the overall churn rate?
- Which customer profiles show higher cancellation risk?
- How do contract type, monthly charges, and tenure relate to churn?
- How can these patterns be explored through both notebooks and an interactive dashboard?

## Tech Stack

- Python
- pandas
- numpy
- matplotlib
- seaborn
- plotly
- Streamlit
- Jupyter Notebook
- SQL
- sqlite3 for local SQL query validation

## Data Source

- Local file: `data/churn.csv`
- Remote fallback used by the data loading scripts:
  `https://raw.githubusercontent.com/blastchar/telco-customer-churn/master/WA_Fn-UseC_-Telco-Customer-Churn.csv`

The local file is the main source for both the analysis and the dashboard. The remote fallback helps keep the project runnable if the CSV is not available locally.

## Repository Structure

- `app.py`: Streamlit dashboard for interactive churn analysis
- `acesso_banco.py`: simple data-loading script with local and remote fallback
- `data/churn.csv`: churn dataset used throughout the project
- `notebooks/analysis.ipynb`: exploratory analysis and visualizations
- `notebooks/sql_tests.ipynb`: SQL query validation with `sqlite3`
- `sql/queries.sql`: main SQL queries used in the analysis
- `requirements.txt`: Python dependencies

## Dashboard Features

- KPIs for total customers, churn rate, average monthly charges, and average tenure
- filters by contract type, internet service, and payment method
- churn comparison by contract
- monthly charges distribution by churn status
- tenure distribution by churn status
- tabular preview of the filtered dataset

## How to Run

1. Create and activate a virtual environment.
2. Install the dependencies:

```bash
pip install -r requirements.txt
```

3. Run the dashboard:

```bash
streamlit run app.py
```

4. To explore the notebooks, start Jupyter:

```bash
jupyter notebook
```

## Technical Notes

- `sqlite3` does not need a separate installation because it is part of Python's standard library.
- The dashboard uses the local dataset by default and tries to remain usable with a remote fallback.
- The project can be expanded in the future with predictive modeling, feature engineering, and deployment automation.

## Project Value

For recruiters:
this repository demonstrates analytics project organization, business metric interpretation, exploratory data analysis, SQL reasoning, and the translation of insights into an interactive interface.

For developers and analysts:
the project works as a base for future evolution with customer segmentation, churn prediction, query testing, and product improvements in the dashboard.
