import pandas as pd
import plotly.express as px
import streamlit as st


DATA_PATH = "data/churn.csv"
FALLBACK_URL = (
    "https://raw.githubusercontent.com/blastchar/telco-customer-churn/master/"
    "WA_Fn-UseC_-Telco-Customer-Churn.csv"
)

TEXTS = {
    "pt-BR": {
        "language_label": "Idioma / Language",
        "language_section": "Preferências",
        "title": "Dashboard de Churn de Clientes",
        "subtitle": "Visão interativa dos padrões de churn da base de clientes Telco IBM.",
        "data_source": "Fonte dos dados",
        "filters": "Filtros",
        "filters_help": "Refine a visão do dashboard usando os campos abaixo.",
        "all_option": "Todos",
        "contract": "Contrato",
        "gender": "Gênero",
        "tenure_period": "Tempo de permanência (meses)",
        "internet_service": "Serviço de Internet",
        "payment_method": "Método de Pagamento",
        "load_error": "Não foi possível carregar a base de dados",
        "no_records": "Nenhum registro corresponde aos filtros selecionados.",
        "customers": "Clientes",
        "churn_rate": "Taxa de Churn",
        "avg_monthly": "Média de Cobrança Mensal",
        "avg_tenure": "Média de Permanência",
        "months": "meses",
        "quick_insight": "Insight rápido",
        "quick_insight_text": "{contract} apresenta a maior taxa de churn na visão atual: {rate}.",
        "insight_contract_title": "Maior risco por contrato",
        "insight_tenure_title": "Churn early-stage",
        "insight_price_title": "Sensibilidade a preço",
        "insight_payment_title": "Método de pagamento",
        "insight_contract_text": "{contract} lidera a taxa de churn neste recorte, com {rate}.",
        "insight_tenure_text": "A faixa {group} concentra o maior churn neste recorte, com {rate}.",
        "insight_price_text": "Clientes que cancelaram têm mensalidade média de {yes_value}, contra {no_value} entre os que permaneceram.",
        "insight_payment_text": "{method} concentra a maior taxa de churn neste recorte, com {rate}.",
        "contract_chart_title": "Taxa de churn por tipo de contrato",
        "contract_chart_y": "Percentual de clientes",
        "payment_chart_title": "Taxa de churn por método de pagamento",
        "monthly_chart_title": "Cobrança mensal por status de churn",
        "monthly_chart_y": "Cobrança mensal",
        "tenure_chart_title": "Distribuição de permanência por status de churn",
        "tenure_chart_x": "Tempo de permanência (meses)",
        "count_label": "Clientes",
        "preview": "Visualizar dados filtrados",
        "local_source": "Arquivo local",
        "remote_source": "Fallback remoto",
        "churn_label": "Churn",
        "yes": "Sim",
        "no": "Não",
    },
    "en": {
        "language_label": "Language / Idioma",
        "language_section": "Preferences",
        "title": "Customer Churn Dashboard",
        "subtitle": "Interactive view of churn patterns in the Telco IBM customer base.",
        "data_source": "Data source",
        "filters": "Filters",
        "filters_help": "Refine the dashboard view using the fields below.",
        "all_option": "All",
        "contract": "Contract",
        "gender": "Gender",
        "tenure_period": "Customer tenure (months)",
        "internet_service": "Internet Service",
        "payment_method": "Payment Method",
        "load_error": "Unable to load the dataset",
        "no_records": "No records match the selected filters.",
        "customers": "Customers",
        "churn_rate": "Churn Rate",
        "avg_monthly": "Avg. Monthly Charges",
        "avg_tenure": "Avg. Tenure",
        "months": "months",
        "quick_insight": "Quick insight",
        "quick_insight_text": "{contract} has the highest churn rate in the current view: {rate}.",
        "insight_contract_title": "Highest risk by contract",
        "insight_tenure_title": "Early-stage churn",
        "insight_price_title": "Price sensitivity",
        "insight_payment_title": "Payment method",
        "insight_contract_text": "{contract} leads the churn rate in this view at {rate}.",
        "insight_tenure_text": "The {group} range concentrates the highest churn in this view at {rate}.",
        "insight_price_text": "Customers who churned show an average monthly charge of {yes_value}, versus {no_value} for those who stayed.",
        "insight_payment_text": "{method} concentrates the highest churn rate in this view at {rate}.",
        "contract_chart_title": "Churn rate by contract type",
        "contract_chart_y": "Percentage of customers",
        "payment_chart_title": "Churn rate by payment method",
        "monthly_chart_title": "Monthly charges by churn status",
        "monthly_chart_y": "Monthly charges",
        "tenure_chart_title": "Tenure distribution by churn status",
        "tenure_chart_x": "Tenure (months)",
        "count_label": "Customers",
        "preview": "Preview filtered data",
        "local_source": "Local file",
        "remote_source": "Remote fallback",
        "churn_label": "Churn",
        "yes": "Yes",
        "no": "No",
    },
}


st.set_page_config(
    page_title="Customer Churn Dashboard",
    page_icon="chart_with_upwards_trend",
    layout="wide",
)


def inject_styles():
    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(circle at top left, rgba(64, 102, 156, 0.22), transparent 24%),
                radial-gradient(circle at top right, rgba(102, 148, 186, 0.16), transparent 22%),
                linear-gradient(180deg, #0d1b2a 0%, #14243a 100%);
        }

        [data-testid="stAppViewContainer"] {
            background: transparent;
        }

        [data-testid="stHeader"] {
            background: rgba(13, 27, 42, 0.78);
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #13263b 0%, #1b314a 100%);
            border-right: 1px solid rgba(201, 215, 232, 0.10);
        }

        [data-testid="stSidebar"] .block-container {
            padding-top: 1.2rem;
        }

        h1, h2, h3 {
            color: #ecf3fb;
            letter-spacing: -0.02em;
        }

        [data-testid="stMarkdownContainer"] p {
            color: #c9d7e8;
        }

        [data-testid="stCaptionContainer"] {
            color: #a9bfd6;
        }

        [data-testid="stHorizontalBlock"] {
            gap: 1rem;
        }

        [data-testid="stMetric"] {
            background:
                linear-gradient(180deg, rgba(21, 38, 58, 0.96), rgba(26, 47, 71, 0.96));
            border: 1px solid rgba(173, 198, 224, 0.14);
            border-radius: 22px;
            padding: 1rem 1.05rem;
            box-shadow: 0 16px 34px rgba(5, 12, 24, 0.26);
            position: relative;
            overflow: hidden;
        }

        [data-testid="stMetric"]::after {
            content: "";
            position: absolute;
            inset: 0 auto auto 0;
            width: 100%;
            height: 4px;
            background: linear-gradient(90deg, #4b86c5 0%, #78b8e6 52%, #9bd2c7 100%);
        }

        [data-testid="stMetricLabel"] {
            color: #9eb8d4;
            font-size: 0.82rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }

        [data-testid="stMetricValue"] {
            color: #eff6ff;
            letter-spacing: -0.03em;
        }

        [data-testid="stExpander"] {
            background: rgba(20, 37, 57, 0.96);
            border: 1px solid rgba(173, 198, 224, 0.14);
            border-radius: 20px;
            box-shadow: 0 14px 26px rgba(5, 12, 24, 0.18);
            overflow: hidden;
        }

        [data-testid="stExpander"] details summary {
            background: linear-gradient(90deg, #17304a 0%, #234566 100%);
            color: #eff6ff !important;
            border-radius: 16px;
            padding: 0.45rem 0.85rem;
        }

        [data-testid="stExpander"] details summary p {
            color: #eff6ff !important;
            font-weight: 600;
        }

        [data-testid="stExpanderDetails"] {
            background: linear-gradient(180deg, rgba(24, 45, 68, 0.98), rgba(18, 34, 52, 0.98));
            border-top: 1px solid rgba(173, 198, 224, 0.12);
            padding-top: 0.75rem;
        }

        [data-testid="stPlotlyChart"] {
            background: linear-gradient(180deg, rgba(21, 38, 58, 0.98), rgba(26, 47, 71, 0.98));
            border: 1px solid rgba(173, 198, 224, 0.14);
            border-radius: 24px;
            padding: 0.65rem 0.65rem 0.2rem 0.65rem;
            box-shadow: 0 16px 32px rgba(5, 12, 24, 0.20);
        }

        [data-testid="stDataFrame"] {
            border: 1px solid rgba(173, 198, 224, 0.14);
            border-radius: 18px;
            overflow: hidden;
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.08);
        }

        [data-testid="stDataFrame"] [role="grid"] {
            background: #f7fbff;
        }

        [data-testid="stDataFrame"] [role="columnheader"] {
            background: #dbe8f5 !important;
            color: #17304a !important;
            font-weight: 700 !important;
        }

        [data-testid="stDataFrame"] [role="gridcell"] {
            color: #203247 !important;
            background: #f7fbff !important;
        }

        .sidebar-panel {
            background: rgba(21, 38, 58, 0.84);
            border: 1px solid rgba(201, 215, 232, 0.10);
            border-radius: 18px;
            padding: 0.9rem 0.95rem 0.4rem 0.95rem;
            margin-bottom: 0.85rem;
            box-shadow: 0 14px 28px rgba(5, 12, 24, 0.18);
        }

        .sidebar-kicker {
            font-size: 0.72rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: #8fc3ff;
            margin-bottom: 0.25rem;
            font-weight: 700;
        }

        .sidebar-copy {
            font-size: 0.88rem;
            color: #d5e2f0;
            margin-bottom: 0.2rem;
        }

        [data-testid="stSidebar"] label {
            color: #edf5ff !important;
            font-weight: 600 !important;
        }

        [data-testid="stSidebar"] [data-baseweb="select"] > div {
            background-color: #223b56;
            border-radius: 14px;
            border: 1px solid rgba(173, 198, 224, 0.18);
            min-height: 3rem;
            box-shadow: none;
        }

        [data-testid="stSidebar"] [data-baseweb="select"] * {
            color: #edf5ff !important;
        }

        [data-testid="stSidebar"] svg {
            fill: #edf5ff !important;
        }

        .hero-panel {
            background:
                linear-gradient(135deg, rgba(23, 42, 64, 0.98), rgba(31, 56, 85, 0.98));
            border: 1px solid rgba(143, 171, 201, 0.16);
            border-radius: 28px;
            padding: 1.35rem 1.35rem 1.2rem 1.35rem;
            box-shadow: 0 20px 44px rgba(5, 12, 24, 0.28);
            margin-bottom: 1rem;
        }

        .hero-kicker {
            font-size: 0.74rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            color: #8fc3ff;
            font-weight: 700;
            margin-bottom: 0.35rem;
        }

        .hero-title {
            font-size: clamp(2.2rem, 4vw, 3.4rem);
            line-height: 0.95;
            letter-spacing: -0.045em;
            color: #f3f8fe;
            font-weight: 800;
            margin: 0 0 0.55rem 0;
        }

        .hero-copy {
            color: #d3e1ef;
            font-size: 1rem;
            line-height: 1.6;
            margin: 0;
        }

        .insight-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 1rem;
            margin: 1rem 0 1.2rem 0;
        }

        .insight-card {
            background: linear-gradient(180deg, rgba(21, 38, 58, 0.98), rgba(26, 47, 71, 0.98));
            border: 1px solid rgba(173, 198, 224, 0.14);
            border-radius: 22px;
            padding: 1rem 1rem 0.95rem 1rem;
            box-shadow: 0 16px 30px rgba(5, 12, 24, 0.18);
        }

        .insight-title {
            color: #8fc3ff;
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-weight: 700;
            margin-bottom: 0.45rem;
        }

        .insight-body {
            color: #eff6ff;
            font-size: 0.97rem;
            line-height: 1.55;
            margin: 0;
        }

        @media (max-width: 900px) {
            .insight-grid {
                grid-template-columns: 1fr;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data
def load_data() -> tuple[pd.DataFrame, str]:
    try:
        df = pd.read_csv(DATA_PATH)
        source = ("local", DATA_PATH)
    except FileNotFoundError:
        df = pd.read_csv(FALLBACK_URL)
        source = ("remote", FALLBACK_URL)

    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    return df, source


def get_language() -> str:
    st.sidebar.markdown(
        f"""
        <div class="sidebar-panel">
            <div class="sidebar-kicker">{TEXTS["pt-BR"]["language_section"]} / {TEXTS["en"]["language_section"]}</div>
            <div class="sidebar-copy">Escolha o idioma da interface do dashboard.</div>
            <div class="sidebar-copy">Choose the dashboard interface language.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    return st.sidebar.selectbox(
        TEXTS["pt-BR"]["language_label"],
        options=["pt-BR", "en"],
        format_func=lambda lang: "Português (Brasil)" if lang == "pt-BR" else "English",
    )


def localize_churn(df: pd.DataFrame, texts: dict[str, str]) -> pd.DataFrame:
    localized = df.copy()
    localized[texts["churn_label"]] = localized["Churn"].map(
        {"Yes": texts["yes"], "No": texts["no"]}
    )
    return localized


def format_integer(value: int, language: str) -> str:
    return f"{value:,}".replace(",", ".")


def format_currency(value: float, language: str) -> str:
    if language == "pt-BR":
        formatted = f"{value:,.2f}"
        formatted = formatted.replace(",", "X").replace(".", ",").replace("X", ".")
        return f"R$ {formatted}"
    return f"${value:,.2f}"


def format_decimal(value: float, language: str, places: int = 1) -> str:
    formatted = f"{value:,.{places}f}"
    if language == "pt-BR":
        return formatted.replace(",", "X").replace(".", ",").replace("X", ".")
    return formatted


def format_percentage(value: float, language: str, places: int = 2) -> str:
    formatted = f"{value:.{places}%}"
    if language == "pt-BR":
        return formatted.replace(".", ",")
    return formatted


def apply_filters(df: pd.DataFrame, texts: dict[str, str]) -> pd.DataFrame:
    st.sidebar.markdown(
        f"""
        <div class="sidebar-panel">
            <div class="sidebar-kicker">{texts["filters"]}</div>
            <div class="sidebar-copy">{texts["filters_help"]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    contract_options = [texts["all_option"], *sorted(df["Contract"].dropna().unique())]
    gender_options = [texts["all_option"], *sorted(df["gender"].dropna().unique())]
    internet_options = [texts["all_option"], *sorted(df["InternetService"].dropna().unique())]
    payment_options = [texts["all_option"], *sorted(df["PaymentMethod"].dropna().unique())]
    min_tenure = int(df["tenure"].min())
    max_tenure = int(df["tenure"].max())

    selected_contract = st.sidebar.selectbox(texts["contract"], options=contract_options)
    selected_gender = st.sidebar.selectbox(texts["gender"], options=gender_options)
    selected_tenure = st.sidebar.slider(
        texts["tenure_period"],
        min_value=min_tenure,
        max_value=max_tenure,
        value=(min_tenure, max_tenure),
    )
    selected_internet = st.sidebar.selectbox(
        texts["internet_service"], options=internet_options
    )
    selected_payment = st.sidebar.selectbox(
        texts["payment_method"], options=payment_options
    )

    filtered = df.copy()

    if selected_contract != texts["all_option"]:
        filtered = filtered[filtered["Contract"] == selected_contract]

    if selected_gender != texts["all_option"]:
        filtered = filtered[filtered["gender"] == selected_gender]

    filtered = filtered[
        (filtered["tenure"] >= selected_tenure[0]) & (filtered["tenure"] <= selected_tenure[1])
    ]

    if selected_internet != texts["all_option"]:
        filtered = filtered[filtered["InternetService"] == selected_internet]

    if selected_payment != texts["all_option"]:
        filtered = filtered[filtered["PaymentMethod"] == selected_payment]

    return filtered


def build_contract_chart(df: pd.DataFrame, texts: dict[str, str]):
    chart_df = (
        df.groupby(["Contract", "Churn"])
        .size()
        .reset_index(name="Customers")
    )
    totals = chart_df.groupby("Contract")["Customers"].transform("sum")
    chart_df["ChurnRatePct"] = (chart_df["Customers"] / totals * 100).round(2)
    chart_df[texts["churn_label"]] = chart_df["Churn"].map(
        {"Yes": texts["yes"], "No": texts["no"]}
    )

    fig = px.bar(
        chart_df,
        x="Contract",
        y="ChurnRatePct",
        color=texts["churn_label"],
        barmode="group",
        title=texts["contract_chart_title"],
        labels={
            "ChurnRatePct": texts["contract_chart_y"],
            "Contract": texts["contract"],
        },
        color_discrete_map={texts["yes"]: "#b86a3b", texts["no"]: "#405f4f"},
    )
    fig.update_traces(marker_line_width=0, opacity=0.92)
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#18314b",
        legend_title_text=texts["churn_label"],
        margin=dict(l=12, r=12, t=56, b=12),
        font=dict(color="#edf5ff"),
        title_font=dict(size=20, color="#8fc3ff"),
        xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(color="#edf5ff")),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(237,245,255,0.12)",
            zeroline=False,
            tickfont=dict(color="#edf5ff"),
        ),
        legend=dict(font=dict(color="#edf5ff")),
    )
    fig.update_xaxes(title_font=dict(color="#edf5ff"))
    fig.update_yaxes(title_font=dict(color="#edf5ff"))
    return fig


def build_tenure_chart(df: pd.DataFrame, texts: dict[str, str]):
    chart_df = localize_churn(df, texts)
    fig = px.histogram(
        chart_df,
        x="tenure",
        color=texts["churn_label"],
        nbins=30,
        barmode="overlay",
        title=texts["tenure_chart_title"],
        labels={"tenure": texts["tenure_chart_x"], "count": texts["count_label"]},
        opacity=0.75,
        color_discrete_map={texts["yes"]: "#b86a3b", texts["no"]: "#405f4f"},
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#18314b",
        legend_title_text=texts["churn_label"],
        margin=dict(l=12, r=12, t=56, b=12),
        font=dict(color="#edf5ff"),
        title_font=dict(size=20, color="#8fc3ff"),
        xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(color="#edf5ff")),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(237,245,255,0.12)",
            zeroline=False,
            tickfont=dict(color="#edf5ff"),
        ),
        legend=dict(font=dict(color="#edf5ff")),
    )
    fig.update_xaxes(title_font=dict(color="#edf5ff"))
    fig.update_yaxes(title_font=dict(color="#edf5ff"))
    return fig


def build_monthly_charges_chart(df: pd.DataFrame, texts: dict[str, str]):
    chart_df = localize_churn(df, texts)
    fig = px.box(
        chart_df,
        x=texts["churn_label"],
        y="MonthlyCharges",
        color=texts["churn_label"],
        title=texts["monthly_chart_title"],
        labels={
            "MonthlyCharges": texts["monthly_chart_y"],
            texts["churn_label"]: texts["churn_label"],
        },
        color_discrete_map={texts["yes"]: "#b86a3b", texts["no"]: "#405f4f"},
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#18314b",
        legend_title_text=texts["churn_label"],
        margin=dict(l=12, r=12, t=56, b=12),
        font=dict(color="#edf5ff"),
        showlegend=False,
        title_font=dict(size=20, color="#8fc3ff"),
        xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(color="#edf5ff")),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(237,245,255,0.12)",
            zeroline=False,
            tickfont=dict(color="#edf5ff"),
        ),
    )
    fig.update_xaxes(title_font=dict(color="#edf5ff"))
    fig.update_yaxes(title_font=dict(color="#edf5ff"))
    return fig


def build_payment_chart(df: pd.DataFrame, texts: dict[str, str]):
    chart_df = (
        df.groupby(["PaymentMethod", "Churn"])
        .size()
        .reset_index(name="Customers")
    )
    totals = chart_df.groupby("PaymentMethod")["Customers"].transform("sum")
    chart_df["ChurnRatePct"] = (chart_df["Customers"] / totals * 100).round(2)
    chart_df[texts["churn_label"]] = chart_df["Churn"].map(
        {"Yes": texts["yes"], "No": texts["no"]}
    )

    fig = px.bar(
        chart_df,
        x="PaymentMethod",
        y="ChurnRatePct",
        color=texts["churn_label"],
        barmode="group",
        title=texts["payment_chart_title"],
        labels={
            "ChurnRatePct": texts["contract_chart_y"],
            "PaymentMethod": texts["payment_method"],
        },
        color_discrete_map={texts["yes"]: "#b86a3b", texts["no"]: "#405f4f"},
    )
    fig.update_traces(marker_line_width=0, opacity=0.92)
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#18314b",
        legend_title_text=texts["churn_label"],
        margin=dict(l=12, r=12, t=56, b=12),
        font=dict(color="#edf5ff"),
        title_font=dict(size=20, color="#8fc3ff"),
        xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(color="#edf5ff")),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(237,245,255,0.12)",
            zeroline=False,
            tickfont=dict(color="#edf5ff"),
        ),
        legend=dict(font=dict(color="#edf5ff")),
    )
    fig.update_xaxes(title_font=dict(color="#edf5ff"))
    fig.update_yaxes(title_font=dict(color="#edf5ff"))
    return fig


def build_insights(df: pd.DataFrame, texts: dict[str, str], language: str) -> str:
    contract_rates = (
        df.groupby("Contract")["Churn"]
        .apply(lambda s: (s == "Yes").mean())
        .sort_values(ascending=False)
    )
    top_contract = contract_rates.index[0]
    top_contract_rate = format_percentage(contract_rates.iloc[0], language)

    working_df = df.copy()
    working_df["tenure_group"] = pd.cut(
        working_df["tenure"],
        bins=[0, 12, 24, 48, 72],
        include_lowest=True,
        labels=["0-12", "13-24", "25-48", "49-72"],
    )
    tenure_rates = (
        working_df.groupby("tenure_group", observed=False)["Churn"]
        .apply(lambda s: (s == "Yes").mean())
        .dropna()
        .sort_values(ascending=False)
    )
    top_tenure_group = tenure_rates.index[0]
    top_tenure_rate = format_percentage(tenure_rates.iloc[0], language)

    avg_monthly = working_df.groupby("Churn")["MonthlyCharges"].mean()
    churn_yes_value = format_currency(avg_monthly.get("Yes", 0), language)
    churn_no_value = format_currency(avg_monthly.get("No", 0), language)

    payment_rates = (
        working_df.groupby("PaymentMethod")["Churn"]
        .apply(lambda s: (s == "Yes").mean())
        .sort_values(ascending=False)
    )
    top_payment_method = payment_rates.index[0]
    top_payment_rate = format_percentage(payment_rates.iloc[0], language)

    return f"""
    <div class="insight-grid">
        <div class="insight-card">
            <div class="insight-title">{texts["insight_contract_title"]}</div>
            <p class="insight-body">
                {texts["insight_contract_text"].format(contract=top_contract, rate=top_contract_rate)}
            </p>
        </div>
        <div class="insight-card">
            <div class="insight-title">{texts["insight_tenure_title"]}</div>
            <p class="insight-body">
                {texts["insight_tenure_text"].format(group=top_tenure_group, rate=top_tenure_rate)}
            </p>
        </div>
        <div class="insight-card">
            <div class="insight-title">{texts["insight_price_title"]}</div>
            <p class="insight-body">
                {texts["insight_price_text"].format(yes_value=churn_yes_value, no_value=churn_no_value)}
            </p>
        </div>
        <div class="insight-card">
            <div class="insight-title">{texts["insight_payment_title"]}</div>
            <p class="insight-body">
                {texts["insight_payment_text"].format(method=top_payment_method, rate=top_payment_rate)}
            </p>
        </div>
    </div>
    """


def main():
    inject_styles()
    language = get_language()
    texts = TEXTS[language]

    st.markdown(
        f"""
        <div class="hero-panel">
            <div class="hero-kicker">Telecom Analytics</div>
            <h1 class="hero-title">{texts["title"]}</h1>
            <p class="hero-copy">{texts["subtitle"]}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    try:
        df, source = load_data()
    except Exception as exc:
        st.error(f"{texts['load_error']}: {exc}")
        st.stop()

    source_kind, source_value = source
    source_label = texts["local_source"] if source_kind == "local" else texts["remote_source"]
    st.caption(f"{texts['data_source']}: {source_label}: {source_value}")

    filtered_df = apply_filters(df, texts)

    if filtered_df.empty:
        st.warning(texts["no_records"])
        st.stop()

    churn_rate = (filtered_df["Churn"] == "Yes").mean()
    avg_monthly = filtered_df["MonthlyCharges"].mean()
    avg_tenure = filtered_df["tenure"].mean()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric(texts["customers"], format_integer(len(filtered_df), language))
    col2.metric(texts["churn_rate"], format_percentage(churn_rate, language))
    col3.metric(texts["avg_monthly"], format_currency(avg_monthly, language))
    col4.metric(
        texts["avg_tenure"],
        f"{format_decimal(avg_tenure, language, 1)} {texts['months']}",
    )

    insight = (
        filtered_df.groupby("Contract")["Churn"]
        .apply(lambda s: (s == "Yes").mean())
        .sort_values(ascending=False)
    )
    top_contract = insight.index[0]
    top_rate = insight.iloc[0]

    st.markdown(
        f"**{texts['quick_insight']}:** "
        f"`{texts['quick_insight_text'].format(contract=top_contract, rate=format_percentage(top_rate, language))}`"
    )

    st.markdown(build_insights(filtered_df, texts, language), unsafe_allow_html=True)

    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        st.plotly_chart(
            build_contract_chart(filtered_df, texts),
            use_container_width=True,
        )
    with chart_col2:
        st.plotly_chart(
            build_monthly_charges_chart(filtered_df, texts),
            use_container_width=True,
        )

    st.plotly_chart(
        build_tenure_chart(filtered_df, texts),
        use_container_width=True,
    )

    st.plotly_chart(
        build_payment_chart(filtered_df, texts),
        use_container_width=True,
    )

    preview_df = localize_churn(filtered_df, texts)

    with st.expander(texts["preview"]):
        st.dataframe(preview_df, use_container_width=True)


if __name__ == "__main__":
    main()
