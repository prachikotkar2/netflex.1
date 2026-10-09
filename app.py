from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Netflix | Viewing Insights",
    page_icon="N",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BACKGROUND = "#0b0b0b"
PANEL = "#141414"
RED = "#e50914"
WHITE = "#f5f5f1"
MUTED = "#a5a5a5"

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@400;500;600;700&display=swap');
    :root {{
        color-scheme: dark;
        --netflix-red: {RED};
        --ink: {BACKGROUND};
        --paper: {WHITE};
    }}
    [data-testid="stAppViewContainer"] {{
        background: radial-gradient(ellipse at 50% -30%, #292020 0%, {BACKGROUND} 54%);
        color: {WHITE};
        font-family: 'DM Sans', sans-serif;
    }}
    [data-testid="stHeader"] {{ background: transparent; }}
    .block-container {{ max-width: 1440px; padding-top: 2.2rem; padding-bottom: 3rem; }}
    [data-testid="stMarkdownContainer"] {{ color: {WHITE}; }}
    .brandline {{
        display: flex; align-items: center; gap: 12px;
        color: #c9c9c9; font-size: 0.78rem; font-weight: 700;
        letter-spacing: 0.12em; text-transform: uppercase;
    }}
    .brandmark {{ color: {RED}; font-family: 'Bebas Neue', Impact, sans-serif; font-size: 1.8rem; line-height: 1; }}
    .hero-title {{
        margin: 1rem 0 0; color: {WHITE};
        font-family: 'Bebas Neue', Impact, sans-serif;
        font-size: clamp(3.4rem, 5rem, 5rem); line-height: 0.95;
    }}
    .hero-copy {{ color: #b7b7b7; font-size: 0.98rem; margin: 0.65rem 0 1.7rem; }}
    .red-rule {{ height: 3px; width: 100%; background: linear-gradient(90deg, {RED} 0 115px, #353535 115px 100%); margin: 1.35rem 0 1.8rem; }}
    .chart-heading {{
        display: flex; align-items: baseline; gap: 11px;
        padding-bottom: 0.65rem; margin-bottom: 0.35rem;
        border-bottom: 1px solid #303030;
    }}
    .chart-number {{ color: {RED}; font-size: 0.72rem; font-weight: 700; letter-spacing: 0.1em; }}
    .chart-title {{ color: {WHITE}; font-size: 1.15rem; font-weight: 600; }}
    .chart-note {{ color: {MUTED}; font-size: 0.8rem; margin: 0.2rem 0 0.5rem; }}
    div[data-testid="stVerticalBlock"] > div:has(> .element-container .chart-heading) {{ padding-top: 0.3rem; }}
    @media (max-width: 700px) {{
        .block-container {{ padding: 1.25rem 1rem 2rem; }}
        .hero-title {{ font-size: 3.4rem; }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(show_spinner=False)
def load_data(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)


data_path = Path(__file__).resolve().parent / "netflix database file.xls"
if not data_path.exists():
    st.error(f"Dataset not found: {data_path.name}")
    st.stop()

try:
    netflix = load_data(str(data_path))
except Exception as error:
    st.error(f"Could not read {data_path.name}: {error}")
    st.stop()

required_columns = {"Region", "Monthly_Revenue", "Subscription_Plan", "Rating", "Category"}
missing_columns = required_columns.difference(netflix.columns)
if missing_columns:
    st.error(f"Dataset is missing chart columns: {', '.join(sorted(missing_columns))}")
    st.stop()


st.markdown(
    """
    <div class="brandline"><span class="brandmark">N</span><span>Netflix data analysis</span></div>
    <h1 class="hero-title">Viewing insights</h1>
    <p class="hero-copy">Revenue and rating patterns across the supplied customer dataset.</p>
    <div class="red-rule"></div>
    """,
    unsafe_allow_html=True,
)


def style_chart(fig: plt.Figure, ax: plt.Axes) -> None:
    fig.patch.set_facecolor(PANEL)
    ax.set_facecolor(PANEL)
    ax.tick_params(colors=WHITE, labelsize=9)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.grid(axis="y", color="#3a3a3a", linewidth=0.7, alpha=0.7)
    ax.set_axisbelow(True)
    ax.yaxis.label.set_color(MUTED)
    ax.xaxis.label.set_color(MUTED)


def chart_heading(number: str, title: str, note: str) -> None:
    st.markdown(
        f'<div class="chart-heading"><span class="chart-number">{number}</span>'
        f'<span class="chart-title">{title}</span></div><p class="chart-note">{note}</p>',
        unsafe_allow_html=True,
    )


left_top, right_top = st.columns(2, gap="large")
with left_top:
    chart_heading("01", "Revenue by region", "Total monthly revenue")
    revenue_by_region = netflix.groupby("Region")["Monthly_Revenue"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(6.2, 3.7), layout="constrained")
    style_chart(fig, ax)
    bars = ax.bar(revenue_by_region.index, revenue_by_region.values, color=RED, width=0.58)
    ax.set_ylabel("Monthly revenue")
    ax.bar_label(bars, labels=[f"{value:,.0f}" for value in revenue_by_region.values], color=WHITE, padding=4, fontsize=9)
    ax.set_ylim(0, max(revenue_by_region.values) * 1.18)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

with right_top:
    chart_heading("02", "Rating by subscription plan", "Sum of ratings")
    rating_by_plan = netflix.groupby("Subscription_Plan")["Rating"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(6.2, 3.7), layout="constrained")
    fig.patch.set_facecolor(PANEL)
    pie_colors = [RED, "#777777", "#3a3a3a"]
    wedges, _, _ = ax.pie(
        rating_by_plan.values,
        colors=pie_colors[: len(rating_by_plan)],
        startangle=90,
        counterclock=False,
        autopct="%1.0f%%",
        pctdistance=0.72,
        wedgeprops={"edgecolor": PANEL, "linewidth": 2},
        textprops={"color": WHITE, "fontsize": 10, "weight": "bold"},
    )
    ax.legend(
        wedges,
        rating_by_plan.index,
        loc="center left",
        bbox_to_anchor=(0.92, 0.5),
        frameon=False,
        labelcolor=WHITE,
        fontsize=9,
    )
    ax.set_aspect("equal")
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

st.markdown('<div class="red-rule"></div>', unsafe_allow_html=True)

left_bottom, right_bottom = st.columns(2, gap="large")
with left_bottom:
    chart_heading("03", "Rating distribution", "Number of records at each rating")
    rating_counts = netflix["Rating"].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(6.2, 3.7), layout="constrained")
    style_chart(fig, ax)
    bars = ax.bar(rating_counts.index.astype(str), rating_counts.values, color=RED, width=0.58)
    ax.set_xlabel("Rating")
    ax.set_ylabel("Count")
    ax.bar_label(bars, color=WHITE, padding=4, fontsize=9)
    ax.set_ylim(0, max(rating_counts.values) * 1.18)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

with right_bottom:
    chart_heading("04", "Revenue by category", "Share of total monthly revenue")
    revenue_by_category = netflix.groupby("Category")["Monthly_Revenue"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(6.2, 3.7), layout="constrained")
    fig.patch.set_facecolor(PANEL)
    category_colors = [RED, "#b20710", "#720f14", "#666666", "#444444", "#cf3037", "#911c22", "#303030"]
    wedges, _, _ = ax.pie(
        revenue_by_category.values,
        colors=category_colors[: len(revenue_by_category)],
        startangle=90,
        counterclock=False,
        autopct=lambda percentage: f"{percentage:.0f}%" if percentage >= 5 else "",
        pctdistance=0.72,
        wedgeprops={"edgecolor": PANEL, "linewidth": 1.5},
        textprops={"color": WHITE, "fontsize": 8, "weight": "bold"},
    )
    ax.legend(
        wedges,
        revenue_by_category.index,
        loc="center left",
        bbox_to_anchor=(0.91, 0.5),
        frameon=False,
        labelcolor=WHITE,
        fontsize=8,
    )
    ax.set_aspect("equal")
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)