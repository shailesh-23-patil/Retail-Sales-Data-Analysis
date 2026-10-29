import base64
import html
import json
from datetime import timedelta
from pathlib import Path
from typing import Any

import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components

# --------------------------------------------------
# 1. PAGE CONFIGURATION (must be the first Streamlit call)
# --------------------------------------------------
st.set_page_config(
    page_title="Retail Sales Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------
# 2. DESIGN TOKENS
# --------------------------------------------------
TEXT = "#F3EEFF"        # main text
MUTED = "#C9B8EA"       # secondary text
PRIMARY = "#B77CFF"     # main data colour (matches the arrows)
HIGHLIGHT = "#FFC857"   # the highest value
SERIES = [PRIMARY, HIGHLIGHT, "#5EEAD4", "#FF7AD9", "#7C9CFF", "#E9D5FF"]
GLASS_EDGE = "rgba(255,255,255,0.12)"

REQUIRED_COLUMNS = [
    "Transaction ID", "Date", "Customer ID", "Gender",
    "Age", "Product Category", "Quantity",
    "Price per Unit", "Total Amount",
]
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday",
            "Friday", "Saturday", "Sunday"]
AGE_BINS = [0, 20, 30, 40, 50, 60, float("inf")]
AGE_LABELS = ["Up to 20", "21-30", "31-40", "41-50", "51-60", "Over 60"]
CSV_NAME = "retail_sales_dataset.csv"
BASE_DIR = Path(__file__).resolve().parent
BACKGROUND_FILES = ["background.jpg", "background.jpeg",
                    "background.png", "background.webp"]

PLOT_CONFIG = {"displayModeBar": False}

# How soft the background image is, in pixels. 0 = sharp, 3 = slight, 8 = very soft.
BACKGROUND_BLUR_PX = 3


def _streamlit_at_least(major: int, minor: int) -> bool:
    try:
        parts = st.__version__.split(".")
        return (int(parts[0]), int(parts[1])) >= (major, minor)
    except (ValueError, IndexError):
        return False


# Newer Streamlit versions replace use_container_width with width="stretch".
STRETCH: dict[str, Any] = (
    {"width": "stretch"} if _streamlit_at_least(1, 50)
    else {"use_container_width": True}
)

# --------------------------------------------------
# 3. STYLES (dark glass panels over the animated background)
# --------------------------------------------------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');

html { background: #0b0618 !important; }
body { background: transparent !important; }
html, body, .stApp, .stMarkdown, p, h1, h2, h3, h4, label, button, input, textarea,
[data-testid="stMetric"] {
    font-family: 'Manrope', 'Segoe UI', sans-serif;
}

/* Let the animated background show through */
.stApp { background: transparent !important; }
[data-testid="stAppViewContainer"], [data-testid="stMain"],
[data-testid="stHeader"], .main { background: transparent !important; }

.block-container { padding-top: 1.8rem; padding-bottom: 3rem; max-width: 1360px; }
#MainMenu, footer { visibility: hidden; }

/* Hide the zero-height frame that loads the background script */
[data-testid="stElementContainer"]:has(iframe[height="0"]),
.element-container:has(iframe[height="0"]) {
    position: absolute; height: 0; margin: 0; overflow: hidden;
}

/* Text colours that stay readable on the dark background */
.stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
.stMarkdown h5, [data-testid="stWidgetLabel"] p,
[data-testid="stCaptionContainer"] { color: #F3EEFF; }
[data-testid="stCaptionContainer"] { color: #C9B8EA; }

.hero {
    background: rgba(20, 10, 42, 0.55);
    -webkit-backdrop-filter: blur(12px);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.12);
    border-left: 6px solid #FFC857;
    border-radius: 14px;
    padding: 1.4rem 1.7rem;
    margin-bottom: 0.6rem;
}
.hero-title { color: #FFFFFF; font-size: 1.9rem; font-weight: 800; letter-spacing: -0.02em; line-height: 1.2; }
.hero-sub { color: #D5C8F0; font-size: 1rem; margin-top: 0.3rem; }

[data-testid="stMetric"] {
    background: rgba(20, 10, 42, 0.55);
    -webkit-backdrop-filter: blur(12px);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 12px;
    padding: 14px 16px;
}
[data-testid="stMetricLabel"] p { color: #C9B8EA; font-weight: 600; font-size: 0.85rem; }
[data-testid="stMetricValue"] { color: #FFFFFF; font-weight: 800; font-size: 1.55rem; }

[data-testid="stPlotlyChart"] {
    background: rgba(20, 10, 42, 0.55);
    -webkit-backdrop-filter: blur(12px);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 12px;
    padding: 6px 8px;
}
[data-testid="stDataFrame"] {
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 12px;
    overflow: hidden;
}

[role="tablist"] { gap: 6px; border-bottom: 1px solid rgba(255,255,255,0.14); }
[role="tab"], [role="tab"] p, [role="tab"] div { color: #C9B8EA !important; font-weight: 700; }
[role="tab"][aria-selected="true"], [role="tab"][aria-selected="true"] p,
[role="tab"][aria-selected="true"] div { color: #FFFFFF !important; }
[role="tab"][aria-selected="true"] { box-shadow: inset 0 -3px 0 #B77CFF; }
[role="tab"][aria-selected="true"]::after, [data-baseweb="tab-highlight"] {
    background-color: #B77CFF !important;
}

.insight-card {
    background: rgba(20, 10, 42, 0.55);
    -webkit-backdrop-filter: blur(12px);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.12);
    border-left: 5px solid #FFC857;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    color: #F3EEFF;
}
.insight-card h4 { margin: 0 0 0.5rem 0; font-size: 1.05rem; font-weight: 800; color: #FFFFFF; }
.insight-card ul { margin: 0; padding-left: 1.1rem; }
.insight-card li { margin-bottom: 0.45rem; line-height: 1.5; color: #F3EEFF; }

[data-testid="stSidebar"] {
    background: rgba(14, 7, 30, 0.72) !important;
    -webkit-backdrop-filter: blur(14px);
    backdrop-filter: blur(14px);
    border-right: 1px solid rgba(255,255,255,0.10);
}
[data-testid="stSidebar"] > div:first-child { background: transparent; }
[data-testid="stSidebar"] h3 { margin-top: 0; }
[data-testid="stDownloadButton"] button { font-weight: 700; }
</style>
""",
    unsafe_allow_html=True,
)

# --------------------------------------------------
# 4. 3D SCROLLING BACKGROUND
#    Runs once per browser page and lives behind the whole app:
#    - the image tilts, zooms and shifts as you scroll
#    - it also follows the mouse a little
#    - glowing arrows and sparkles at different depths move at different
#      speeds when you scroll, which gives the parallax depth
# --------------------------------------------------
BACKGROUND_JS = r"""
(function () {
  if (window.__bg3d) return;
  window.__bg3d = true;
  var doc = document;

  var css = `
    #bg3d-root{position:fixed;top:0;right:0;bottom:0;left:0;z-index:-1;overflow:hidden;
      pointer-events:none;background:#0b0618;perspective:900px;perspective-origin:50% 60%}
    #bg3d-img{position:absolute;top:-14%;right:-14%;bottom:-14%;left:-14%;
      background:#0b0618 url("__IMG__") center bottom/cover no-repeat;
      transform-origin:50% 100%;will-change:transform;filter:blur(__BLUR__px)}
    #bg3d-canvas{position:absolute;top:0;left:0;width:100%;height:100%}
    #bg3d-scrim{position:absolute;top:0;right:0;bottom:0;left:0;
      background:radial-gradient(ellipse at 50% 35%,rgba(11,6,24,.28) 0%,rgba(11,6,24,.70) 100%)}
    html{background:#0b0618 !important}
    body{background:transparent !important}
    .stApp{background:transparent !important}
    [data-testid="stAppViewContainer"],[data-testid="stMain"],[data-testid="stHeader"],.main{
      background:transparent !important}
  `;
  var style = doc.createElement('style');
  style.id = 'bg3d-style';
  style.textContent = css;
  doc.head.appendChild(style);

  var root = doc.createElement('div');
  root.id = 'bg3d-root';
  root.innerHTML = '<div id="bg3d-img"></div><canvas id="bg3d-canvas"></canvas><div id="bg3d-scrim"></div>';
  doc.body.insertBefore(root, doc.body.firstChild);

  var img = doc.getElementById('bg3d-img');
  var canvas = doc.getElementById('bg3d-canvas');
  var ctx = canvas.getContext('2d');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var W = 0, H = 0, lastW = 0, dpr = 1, arrows = [], dots = [];
  var curY = 0, targetY = 0, maxY = 0, mx = 0, my = 0, tx = 0, ty = 0;
  var scroller = null, frame = 0;

  function rnd(a, b) { return a + Math.random() * (b - a); }

  function build() {
    var n = W < 700 ? 10 : 18;
    arrows = [];
    for (var i = 0; i < n; i++) {
      var d = Math.pow(Math.random(), 1.5) * 0.85 + 0.15;
      arrows.push({ x: Math.random(), d: d, phase: Math.random() * 5000,
                    speed: 14 + d * 60, k: 0.25 + d * 0.9 });
    }
    arrows.sort(function (a, b) { return a.d - b.d; });
    dots = [];
    var m = W < 700 ? 60 : 120;
    for (var j = 0; j < m; j++) {
      dots.push({ x: Math.random(), y: Math.random(), r: rnd(0.5, 1.7),
                  d: rnd(0.2, 1), tw: rnd(0, 6.28) });
    }
  }

  function resize() {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    W = window.innerWidth;
    H = window.innerHeight;
    canvas.width = Math.round(W * dpr);
    canvas.height = Math.round(H * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    if (!arrows.length || Math.abs(W - lastW) > 80) { build(); lastW = W; }
  }

  function findScroller() {
    if (scroller && scroller.isConnected) return scroller;
    scroller = doc.querySelector('[data-testid="stMain"]') ||
               doc.querySelector('section.main') ||
               doc.scrollingElement;
    return scroller;
  }

  function draw(now) {
    var t = now * 0.001;
    ctx.clearRect(0, 0, W, H);

    // sparkles
    for (var i = 0; i < dots.length; i++) {
      var s = dots[i];
      var span = H + 20;
      var yy = ((s.y * span - curY * 0.12 * s.d - t * 5 * s.d) % span + span) % span - 10;
      var a = (0.3 + 0.7 * Math.abs(Math.sin(t * 1.3 + s.tw))) * s.d;
      ctx.fillStyle = 'rgba(235,215,255,' + a.toFixed(3) + ')';
      ctx.beginPath();
      ctx.arc(s.x * W, yy, s.r * (0.6 + s.d), 0, 6.2832);
      ctx.fill();
    }

    // arrows (far ones first, so near ones overlap them)
    var u = H / 800;
    for (var k = 0; k < arrows.length; k++) {
      var r = arrows[k];
      var L = (110 + 300 * r.d) * u;
      var sp = H + L * 2;
      var off = ((r.phase + t * r.speed + curY * r.k) % sp + sp) % sp;
      var yTip = H + L - off;
      var x = r.x * W;
      var w = 1.5 + 6.5 * r.d;
      var hw = (6 + 26 * r.d) * u;

      ctx.globalAlpha = 0.22 + 0.58 * r.d;
      ctx.shadowColor = 'rgba(190,120,255,0.9)';
      ctx.shadowBlur = 6 + 18 * r.d;
      var g = ctx.createLinearGradient(0, yTip, 0, yTip + L);
      g.addColorStop(0, 'rgba(245,215,255,1)');
      g.addColorStop(0.35, 'rgba(200,130,255,0.85)');
      g.addColorStop(1, 'rgba(120,60,220,0)');
      ctx.strokeStyle = g;
      ctx.lineWidth = w;
      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';
      ctx.beginPath();
      ctx.moveTo(x, yTip + hw * 0.3);
      ctx.lineTo(x, yTip + L);
      ctx.stroke();
      ctx.strokeStyle = 'rgba(250,225,255,1)';
      ctx.lineWidth = w * 0.9;
      ctx.beginPath();
      ctx.moveTo(x - hw, yTip + hw * 1.05);
      ctx.lineTo(x, yTip);
      ctx.lineTo(x + hw, yTip + hw * 1.05);
      ctx.stroke();
    }
    ctx.globalAlpha = 1;
    ctx.shadowBlur = 0;
  }

  function loop(now) {
    var sc = findScroller();
    if (sc) {
      targetY = Math.max(sc.scrollTop || 0, window.scrollY || 0);
      if (frame % 30 === 0) {
        maxY = Math.max(0, (sc.scrollHeight || 0) - (sc.clientHeight || 0));
      }
    }
    frame++;

    curY += (targetY - curY) * 0.09;
    mx += (tx - mx) * 0.05;
    my += (ty - my) * 0.05;

    var p = maxY > 1 ? Math.min(1, Math.max(0, curY / maxY)) : 0;
    img.style.transform =
      'translate3d(' + (-mx * 1.2) + '%,' + (-p * 5 - my * 0.8) + '%,0) ' +
      'rotateX(' + (p * 9 - my * 1.5) + 'deg) ' +
      'rotateY(' + (mx * 2) + 'deg) ' +
      'scale(' + (1 + p * 0.22) + ')';

    draw(now);
    if (!reduce) window.requestAnimationFrame(loop);
  }

  doc.addEventListener('mousemove', function (e) {
    tx = (e.clientX / window.innerWidth) * 2 - 1;
    ty = (e.clientY / window.innerHeight) * 2 - 1;
  }, { passive: true });
  window.addEventListener('resize', resize);

  resize();
  window.requestAnimationFrame(loop);
})();
"""


@st.cache_resource(show_spinner=False)
def background_data_uri() -> str:
    """Return the background image as a data URI, or '' if none is found."""
    for folder in (BASE_DIR / "assets", BASE_DIR):
        for name in BACKGROUND_FILES:
            path = folder / name
            if path.exists():
                mime = {
                    ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
                    ".png": "image/png", ".webp": "image/webp",
                }[path.suffix.lower()]
                encoded = base64.b64encode(path.read_bytes()).decode("ascii")
                return f"data:{mime};base64,{encoded}"
    return ""


def inject_background() -> None:
    script = BACKGROUND_JS.replace("__IMG__", background_data_uri()).replace(
        "__BLUR__", str(int(BACKGROUND_BLUR_PX))
    )
    loader = (
        "<script>(function(){"
        "var P=window.parent,d=P.document;"
        "if(d.getElementById('bg3d-script'))return;"
        "var s=d.createElement('script');s.id='bg3d-script';"
        f"s.textContent={json.dumps(script)};"
        "d.head.appendChild(s);})();</script>"
    )
    components.html(loader, height=0)


inject_background()


# --------------------------------------------------
# 5. HELPERS
# --------------------------------------------------
class DataError(Exception):
    """Raised when the dataset is missing columns or has no usable rows."""


def inr(value) -> str:
    """Format a number as rupees with Indian digit grouping (₹4,56,000)."""
    try:
        n = int(round(float(value)))
    except (TypeError, ValueError):
        return "₹0"
    sign = "-" if n < 0 else ""
    digits = str(abs(n))
    if len(digits) > 3:
        head, tail = digits[:-3], digits[-3:]
        groups = []
        while len(head) > 2:
            groups.insert(0, head[-2:])
            head = head[:-2]
        if head:
            groups.insert(0, head)
        digits = ",".join(groups + [tail])
    return f"₹{sign}{digits}"


def prepare(raw: pd.DataFrame) -> pd.DataFrame:
    """Validate and clean the raw dataset."""
    df = raw.copy()
    df.columns = [str(c).strip() for c in df.columns]

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise DataError(
            "The file is missing these columns: " + ", ".join(missing)
        )

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    for col in ["Age", "Quantity", "Price per Unit", "Total Amount"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(
        subset=["Date", "Gender", "Product Category", "Total Amount"]
    ).copy()
    if df.empty:
        raise DataError("The file has no rows with a valid date, gender, "
                        "category and amount.")

    for col in ["Gender", "Product Category", "Transaction ID", "Customer ID"]:
        df[col] = df[col].astype(str).str.strip()

    df["Day"] = df["Date"].dt.date
    return df


@st.cache_data(show_spinner="Loading data...")
def load_csv(path: str, modified: float) -> pd.DataFrame:
    # `modified` makes the cache refresh when the CSV file changes.
    return prepare(pd.read_csv(path))


def get_data():
    """Return the cleaned dataset, or None while waiting for an upload."""
    for candidate in (BASE_DIR / "data" / CSV_NAME, BASE_DIR / CSV_NAME):
        if candidate.exists():
            return load_csv(str(candidate), candidate.stat().st_mtime)

    st.info(
        f"Could not find `data/{CSV_NAME}`. Upload the CSV to continue, "
        "or add it to the data folder next to app.py."
    )
    uploaded = st.file_uploader("Upload the retail sales CSV", type="csv")
    if uploaded is None:
        return None
    return prepare(pd.read_csv(uploaded))


def show(fig):
    st.plotly_chart(fig, config=PLOT_CONFIG, **STRETCH)


def show_table(data, column_config=None):
    st.dataframe(data, hide_index=True, column_config=column_config, **STRETCH)


def style(fig, height=380, legend=False):
    fig.update_layout(
        template="plotly_dark",
        height=height,
        margin=dict(l=10, r=10, t=55, b=10),
        font=dict(family="Manrope, Segoe UI, sans-serif", color=TEXT, size=13),
        title=dict(font=dict(size=16, color=TEXT), x=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=legend,
        hoverlabel=dict(font_family="Manrope, Segoe UI, sans-serif"),
    )
    if legend:
        fig.update_layout(
            legend=dict(orientation="h", y=1.12, x=0, title_text="")
        )
    fig.update_xaxes(showgrid=False, linecolor=GLASS_EDGE, title=None)
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.08)", zeroline=False,
                     title=None)
    return fig


def highlight_colors(values):
    """Violet bars, with the highest value in gold."""
    top = max(values) if len(values) else None
    return [HIGHLIGHT if v == top else PRIMARY for v in values]


def top_row(data: pd.DataFrame, column: str) -> pd.Series:
    """Return the row with the highest value in `column`."""
    return data.iloc[int(data[column].to_numpy().argmax())]


def kpis(d: pd.DataFrame) -> dict:
    revenue = d["Total Amount"].sum()
    transactions = d["Transaction ID"].nunique()
    return {
        "revenue": revenue,
        "transactions": transactions,
        "customers": d["Customer ID"].nunique(),
        "units": d["Quantity"].sum(),
        "average": revenue / transactions if transactions else 0,
    }


def pct_change(current: dict, previous, key: str):
    if previous is None or not previous[key]:
        return None
    return f"{(current[key] - previous[key]) / previous[key] * 100:+.1f}%"


# --------------------------------------------------
# 6. HEADER AND DATA LOADING
# --------------------------------------------------
st.markdown(
    """
<div class="hero">
  <div class="hero-title">Retail sales dashboard</div>
  <div class="hero-sub">See what sells, who buys, and when revenue peaks.</div>
</div>
""",
    unsafe_allow_html=True,
)

try:
    df = get_data()
except DataError as error:
    st.error(str(error))
    st.stop()
except Exception as error:  # unreadable or malformed file
    st.error(f"Could not read the dataset: {error}")
    st.stop()

if df is None:
    st.stop()

# --------------------------------------------------
# 7. SIDEBAR FILTERS
# --------------------------------------------------
min_date = df["Day"].min()
max_date = df["Day"].max()
all_genders = sorted(df["Gender"].unique())
all_categories = sorted(df["Product Category"].unique())

with st.sidebar:
    st.markdown("### Filters")

    date_range = st.date_input(
        "Date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )
    selected_genders = st.multiselect(
        "Gender", options=all_genders, default=all_genders
    )
    selected_categories = st.multiselect(
        "Product category", options=all_categories, default=all_categories
    )

    age_range = None
    if df["Age"].notna().any():
        age_lo, age_hi = int(df["Age"].min()), int(df["Age"].max())
        if age_lo < age_hi:
            age_range = st.slider(
                "Customer age", age_lo, age_hi, (age_lo, age_hi)
            )

if isinstance(date_range, (tuple, list)):
    if len(date_range) == 2:
        start_date, end_date = date_range
    elif len(date_range) == 1:
        start_date = end_date = date_range[0]
        st.sidebar.caption("Pick an end date to complete the range.")
    else:
        start_date, end_date = min_date, max_date
else:
    start_date = end_date = date_range


def apply_filters(data: pd.DataFrame, start, end) -> pd.DataFrame:
    mask = (
        data["Day"].between(start, end)
        & data["Gender"].isin(selected_genders)
        & data["Product Category"].isin(selected_categories)
    )
    if age_range is not None:
        mask &= data["Age"].between(age_range[0], age_range[1]) | data["Age"].isna()
    return data.loc[mask].copy()


filtered = apply_filters(df, start_date, end_date)

if filtered.empty:
    st.warning(
        "No transactions match these filters. Widen the date range or "
        "select more genders or categories."
    )
    st.stop()

st.caption(
    f"Showing {len(filtered):,} transactions from "
    f"{start_date.strftime('%d %b %Y')} to {end_date.strftime('%d %b %Y')}."
)

# --------------------------------------------------
# 8. KEY PERFORMANCE INDICATORS
# --------------------------------------------------
current = kpis(filtered)

# Compare with the previous period of the same length, but only when the
# whole previous period lies inside the data.
previous = None
span_days = (end_date - start_date).days + 1
prev_start = start_date - timedelta(days=span_days)
prev_end = start_date - timedelta(days=1)
if prev_start >= min_date:
    prev_df = apply_filters(df, prev_start, prev_end)
    if not prev_df.empty:
        previous = kpis(prev_df)
compare_help = f"Change versus the previous {span_days} days."

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total revenue", inr(current["revenue"]),
          pct_change(current, previous, "revenue"), help=compare_help)
c2.metric("Transactions", f"{current['transactions']:,}",
          pct_change(current, previous, "transactions"), help=compare_help)
c3.metric("Unique customers", f"{current['customers']:,}",
          pct_change(current, previous, "customers"), help=compare_help)
c4.metric("Units sold", f"{current['units']:,.0f}",
          pct_change(current, previous, "units"), help=compare_help)
c5.metric("Avg. transaction", inr(current["average"]),
          pct_change(current, previous, "average"), help=compare_help)

st.write("")

# --------------------------------------------------
# 9. PREPARED TABLES
# --------------------------------------------------
total_revenue = current["revenue"]

category_sales = (
    filtered.groupby("Product Category", as_index=False)
    .agg(
        Revenue=("Total Amount", "sum"),
        Units=("Quantity", "sum"),
        Transactions=("Transaction ID", "nunique"),
    )
    .sort_values("Revenue", ascending=False)
    .reset_index(drop=True)
)
category_sales["Share (%)"] = (
    category_sales["Revenue"] / total_revenue * 100 if total_revenue else 0
)
category_sales["Avg. transaction"] = (
    category_sales["Revenue"] / category_sales["Transactions"]
).round(0)

filtered["Month"] = filtered["Date"].dt.to_period("M").dt.to_timestamp()
monthly_sales = (
    filtered.groupby("Month", as_index=False)
    .agg(Revenue=("Total Amount", "sum"))
    .sort_values("Month")
)

weekday_sales = (
    filtered.groupby(filtered["Date"].dt.day_name())["Total Amount"]
    .sum()
    .reindex(WEEKDAYS)
    .fillna(0)
    .rename_axis("Weekday")
    .reset_index(name="Revenue")
)

gender_sales = (
    filtered.groupby("Gender", as_index=False)
    .agg(
        Revenue=("Total Amount", "sum"),
        Transactions=("Transaction ID", "nunique"),
        Average_Spending=("Total Amount", "mean"),
    )
    .round(2)
)

filtered["Age Group"] = pd.cut(
    filtered["Age"], bins=AGE_BINS, labels=AGE_LABELS, include_lowest=True
)
age_sales = (
    filtered.dropna(subset=["Age Group"])
    .groupby("Age Group", observed=False, as_index=False)
    .agg(
        Revenue=("Total Amount", "sum"),
        Transactions=("Transaction ID", "nunique"),
    )
)

category_gender = (
    filtered.groupby(["Product Category", "Gender"], as_index=False)
    .agg(Revenue=("Total Amount", "sum"))
)

# --------------------------------------------------
# 10. TABS
# --------------------------------------------------
tab_overview, tab_products, tab_customers, tab_transactions = st.tabs(
    ["Overview", "Products", "Customers", "Transactions"]
)

# ---------- Overview ----------
with tab_overview:
    best_month = top_row(monthly_sales, "Revenue")

    fig = px.area(
        monthly_sales, x="Month", y="Revenue", title="Monthly revenue"
    )
    fig.update_traces(
        line=dict(color=PRIMARY, width=3),
        fillcolor="rgba(183,124,255,0.18)",
        mode="lines+markers",
        marker=dict(size=7, color=PRIMARY),
        hovertemplate="%{x|%B %Y}<br>₹%{y:,.0f}<extra></extra>",
    )
    fig.add_scatter(
        x=[best_month["Month"]],
        y=[best_month["Revenue"]],
        mode="markers",
        marker=dict(size=13, color=HIGHLIGHT, line=dict(color="#1A0F33", width=2)),
        hoverinfo="skip",
        showlegend=False,
    )
    style(fig, height=360)
    fig.update_yaxes(tickprefix="₹", tickformat="~s")
    fig.update_xaxes(
        tickformat="%b %Y",
        dtick="M1" if len(monthly_sales) <= 12 else None,
    )
    fig.update_layout(hovermode="x unified")
    show(fig)
    st.caption("The gold dot marks the best month.")

    left, right = st.columns([3, 2], gap="large")

    with left:
        fig = px.bar(weekday_sales, x="Weekday", y="Revenue",
                     title="Revenue by day of the week")
        fig.update_traces(
            marker_color=highlight_colors(list(weekday_sales["Revenue"])),
            texttemplate="₹%{y:.3~s}",
            textposition="outside",
            cliponaxis=False,
            hovertemplate="%{x}<br>₹%{y:,.0f}<extra></extra>",
        )
        style(fig, height=340)
        fig.update_yaxes(visible=False)
        show(fig)

    with right:
        top_cat = category_sales.iloc[0]
        top_gender = top_row(gender_sales, "Revenue")
        best_basket = top_row(category_sales, "Avg. transaction")

        items = [
            f"<li><b>{html.escape(str(top_cat['Product Category']))}</b> earns the "
            f"most: {inr(top_cat['Revenue'])}, {top_cat['Share (%)']:.1f}% of revenue.</li>",
            f"<li><b>{best_month['Month'].strftime('%B %Y')}</b> is the best month "
            f"with {inr(best_month['Revenue'])}.</li>",
            f"<li><b>{html.escape(str(top_gender['Gender']))}</b> customers bring in "
            f"the most revenue: {inr(top_gender['Revenue'])}.</li>",
            f"<li><b>{html.escape(str(best_basket['Product Category']))}</b> has the "
            f"largest average transaction at {inr(best_basket['Avg. transaction'])}.</li>",
        ]
        if not age_sales.empty and age_sales["Revenue"].max() > 0:
            top_age = top_row(age_sales, "Revenue")
            items.append(
                f"<li>Customers aged <b>{top_age['Age Group']}</b> spend the "
                f"most: {inr(top_age['Revenue'])}.</li>"
            )

        st.markdown(
            "<div class='insight-card'><h4>What stands out</h4><ul>"
            + "".join(items)
            + "</ul></div>",
            unsafe_allow_html=True,
        )
        st.caption("Revenue is what customers paid, not profit.")

# ---------- Products ----------
with tab_products:
    left, right = st.columns(2, gap="large")

    with left:
        fig = px.bar(category_sales, x="Revenue", y="Product Category",
                     orientation="h", title="Revenue by category")
        fig.update_traces(
            marker_color=highlight_colors(list(category_sales["Revenue"])),
            texttemplate="₹%{x:.3~s}",
            textposition="outside",
            cliponaxis=False,
            hovertemplate="%{y}<br>₹%{x:,.0f}<extra></extra>",
        )
        style(fig, height=340)
        fig.update_xaxes(visible=False)
        fig.update_yaxes(autorange="reversed", showgrid=False)
        fig.update_layout(margin=dict(l=10, r=50, t=55, b=10))
        show(fig)

    with right:
        units_sorted = category_sales.sort_values("Units", ascending=False)
        fig = px.bar(units_sorted, x="Units", y="Product Category",
                     orientation="h", title="Units sold by category")
        fig.update_traces(
            marker_color=highlight_colors(list(units_sorted["Units"])),
            texttemplate="%{x:,.0f}",
            textposition="outside",
            cliponaxis=False,
            hovertemplate="%{y}<br>%{x:,.0f} units<extra></extra>",
        )
        style(fig, height=340)
        fig.update_xaxes(visible=False)
        fig.update_yaxes(autorange="reversed", showgrid=False)
        fig.update_layout(margin=dict(l=10, r=50, t=55, b=10))
        show(fig)

    st.markdown("##### Category summary")
    show_table(
        category_sales[["Product Category", "Revenue", "Share (%)", "Units",
                        "Transactions", "Avg. transaction"]],
        column_config={
            "Revenue": st.column_config.NumberColumn(format="₹%.0f"),
            "Share (%)": st.column_config.ProgressColumn(
                format="%.1f%%", min_value=0, max_value=100
            ),
            "Units": st.column_config.NumberColumn(format="%d"),
            "Transactions": st.column_config.NumberColumn(format="%d"),
            "Avg. transaction": st.column_config.NumberColumn(format="₹%.0f"),
        },
    )

# ---------- Customers ----------
with tab_customers:
    left, right = st.columns(2, gap="large")

    with left:
        fig = px.pie(
            gender_sales, names="Gender", values="Revenue", hole=0.55,
            title="Revenue share by gender",
            color_discrete_sequence=SERIES,
        )
        fig.update_traces(
            textinfo="percent+label",
            textposition="outside",
            marker=dict(line=dict(color="#1A0F33", width=2)),
            hovertemplate="%{label}<br>₹%{value:,.0f}<extra></extra>",
        )
        style(fig, height=360)
        show(fig)

    with right:
        if age_sales.empty:
            st.info("Age data is not available for the selected transactions.")
        else:
            fig = px.bar(age_sales, x="Age Group", y="Revenue",
                         title="Revenue by age group")
            fig.update_traces(
                marker_color=highlight_colors(list(age_sales["Revenue"])),
                texttemplate="₹%{y:.3~s}",
                textposition="outside",
                cliponaxis=False,
                hovertemplate="%{x}<br>₹%{y:,.0f}<extra></extra>",
            )
            style(fig, height=360)
            fig.update_yaxes(visible=False)
            show(fig)

    fig = px.bar(
        category_gender, x="Product Category", y="Revenue", color="Gender",
        barmode="group", title="Category revenue by gender",
        color_discrete_sequence=SERIES,
    )
    fig.update_traces(hovertemplate="%{x}<br>₹%{y:,.0f}<extra></extra>")
    style(fig, height=360, legend=True)
    fig.update_yaxes(tickprefix="₹", tickformat="~s")
    show(fig)

    st.markdown("##### Spending by gender")
    show_table(
        gender_sales.rename(columns={"Average_Spending": "Avg. spending"}),
        column_config={
            "Revenue": st.column_config.NumberColumn(format="₹%.0f"),
            "Transactions": st.column_config.NumberColumn(format="%d"),
            "Avg. spending": st.column_config.NumberColumn(format="₹%.0f"),
        },
    )

# ---------- Transactions ----------
with tab_transactions:
    search_text = st.text_input(
        "Search transactions",
        placeholder="Customer ID, transaction ID or category, e.g. CUST001 or Beauty",
    )

    display_df = filtered.sort_values("Date", ascending=False)
    query = search_text.strip()
    if query:
        mask = pd.Series(False, index=display_df.index)
        for col in ["Customer ID", "Transaction ID", "Product Category"]:
            mask |= display_df[col].str.contains(
                query, case=False, regex=False, na=False
            )
        display_df = display_df[mask]

    table = display_df[REQUIRED_COLUMNS]
    st.write(f"{len(table):,} matching transactions")

    if table.empty:
        st.info("No transactions match that search. Try a shorter term.")
    else:
        show_table(
            table,
            column_config={
                "Date": st.column_config.DateColumn(format="DD MMM YYYY"),
                "Price per Unit": st.column_config.NumberColumn(format="₹%.0f"),
                "Total Amount": st.column_config.NumberColumn(format="₹%.0f"),
            },
        )

        export = table.copy()
        export["Date"] = export["Date"].dt.strftime("%Y-%m-%d")
        st.download_button(
            "Download these transactions as CSV",
            data=export.to_csv(index=False).encode("utf-8"),
            file_name=f"retail_sales_{start_date}_{end_date}.csv",
            mime="text/csv",
        )

st.divider()
st.caption("Retail Sales Analytics, built with Python, Pandas, Plotly and Streamlit.")