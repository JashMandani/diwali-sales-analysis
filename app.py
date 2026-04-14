import streamlit as st
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Diwali Sales Analysis",
    page_icon="🪔",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Hide default streamlit chrome */
#MainMenu, footer { visibility: hidden; }
header {
    visibility: visible;
    height: 0px;
}

header * {
    display: none;
}

/* Page background */
.stApp { background: #0F0E17; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: #1A1825 !important;
    border-right: 1px solid #2D2B3D;
}
[data-testid="stSidebar"] * { color: #C8C5E0 !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label { color: #9D9AB8 !important; font-size: 12px !important; letter-spacing: 0.08em; text-transform: uppercase; }

/* Metric cards */
.kpi-card {
    background: linear-gradient(135deg, #1E1B2E 0%, #252236 100%);
    border: 1px solid #3D3A54;
    border-radius: 16px;
    padding: 24px 20px;
    text-align: center;
    transition: transform 0.2s, border-color 0.2s;
}
.kpi-card:hover { transform: translateY(-2px); border-color: #E8650A; }
.kpi-number { font-family: 'Syne', sans-serif; font-size: 2rem; font-weight: 800; color: #F5A623; line-height: 1; margin-bottom: 6px; }
.kpi-label { font-size: 0.78rem; color: #7B78A0; letter-spacing: 0.1em; text-transform: uppercase; }
.kpi-sub { font-size: 0.85rem; color: #A09DC0; margin-top: 4px; }

/* Section headings */
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: #F0EEF8;
    border-left: 4px solid #E8650A;
    padding-left: 12px;
    margin: 32px 0 16px;
}

/* Hero title */
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.6rem;
    font-weight: 800;
    color: #F0EEF8;
    line-height: 1.1;
}
.hero-subtitle {
    font-size: 1rem;
    color: #7B78A0;
    margin-top: 6px;
}
.hero-accent { color: #E8650A; }

/* Insight boxes */
.insight-box {
    background: #1E1B2E;
    border: 1px solid #3D3A54;
    border-left: 4px solid #F5A623;
    border-radius: 12px;
    padding: 16px 20px;
    font-size: 0.9rem;
    color: #C8C5E0;
    margin-top: 10px;
    line-height: 1.7;
}
.insight-box b { color: #F5A623; }

/* Chart containers */
[data-testid="stPlotlyChart"], .stPyplot { border-radius: 12px; overflow: hidden; }

/* Divider */
.fancy-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #3D3A54, transparent);
    margin: 32px 0;
}
</style>
""", unsafe_allow_html=True)

# ── Palette ───────────────────────────────────────────────────────────────────
ORANGE   = "#E8650A"
GOLD     = "#F5A623"
DARK_BG  = "#0F0E17"
CARD_BG  = "#1A1825"
CHART_BG = "#15131F"
TEXT     = "#C8C5E0"
MUTED    = "#7B78A0"
COLORS   = [ORANGE, GOLD, "#E74C3C", "#3498DB", "#2ECC71",
            "#9B59B6", "#1ABC9C", "#F39C12", "#E67E22", "#16A085"]
AGE_ORDER = ['0-17', '18-25', '26-35', '36-45', '46-50', '51-55', '55+']

# ── Chart theme ───────────────────────────────────────────────────────────────
def chart_style():
    plt.rcParams.update({
        'figure.facecolor':  CHART_BG,
        'axes.facecolor':    CHART_BG,
        'axes.edgecolor':    '#2D2B3D',
        'axes.labelcolor':   MUTED,
        'xtick.color':       MUTED,
        'ytick.color':       MUTED,
        'text.color':        TEXT,
        'grid.color':        '#2D2B3D',
        'grid.linestyle':    '--',
        'grid.alpha':        0.5,
        'font.family':       'DejaVu Sans',
    })

def inr_fmt(ax, axis='y'):
    fmt = mticker.FuncFormatter(lambda x, _: f"₹{x/1e6:.1f}M" if x >= 1e6 else f"₹{x/1e3:.0f}K")
    if axis == 'y': ax.yaxis.set_major_formatter(fmt)
    else:           ax.xaxis.set_major_formatter(fmt)

def polish(ax, title=""):
    ax.set_title(title, fontsize=13, fontweight='bold', color=TEXT, pad=10)
    ax.spines[['top', 'right', 'left', 'bottom']].set_visible(False)
    ax.tick_params(colors=MUTED, length=0)
    ax.grid(axis='y', alpha=0.3)

def save_fig(fig):
    fig.tight_layout()
    return fig

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('data/Diwali_Sales_Data.csv', encoding='latin1')
    except FileNotFoundError:
        df = pd.read_csv('Diwali_Sales_Data.csv', encoding='latin1')
    df = df.drop(columns=['Status', 'unnamed1'], errors='ignore').dropna(subset=['Amount'])
    df['Amount']               = df['Amount'].astype(int)
    df['User_ID']              = df['User_ID'].astype(str)
    df['Gender_Label']         = df['Gender'].map({'F': 'Female', 'M': 'Male'})
    df['Marital_Status_Label'] = df['Marital_Status'].map({0: 'Single', 1: 'Married'})
    df['Age Group']            = pd.Categorical(df['Age Group'], categories=AGE_ORDER, ordered=True)
    df['State']                = df['State'].str.strip()
    return df

df_full = load_data()

# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR — Filters
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 20px 0 12px;'>
      <span style='font-size:2.4rem'>🪔</span>
      <div style='font-family:Syne,sans-serif; font-size:1.2rem; font-weight:700; color:#F0EEF8; margin-top:6px;'>Diwali Sales</div>
      <div style='font-size:0.75rem; color:#7B78A0; letter-spacing:0.08em;'>ANALYSIS DASHBOARD</div>
    </div>
    <hr style='border-color:#2D2B3D; margin:0 0 20px;'>
    """, unsafe_allow_html=True)

    st.markdown("**Filters**")

    gender_opts  = ['All'] + sorted(df_full['Gender_Label'].dropna().unique().tolist())
    zone_opts    = ['All'] + sorted(df_full['Zone'].dropna().unique().tolist())
    marital_opts = ['All'] + sorted(df_full['Marital_Status_Label'].dropna().unique().tolist())

    sel_gender  = st.selectbox("Gender",         gender_opts)
    sel_zone    = st.selectbox("Zone",            zone_opts)
    sel_marital = st.selectbox("Marital status",  marital_opts)
    sel_ages    = st.multiselect("Age groups",    AGE_ORDER, default=AGE_ORDER)
    sel_states  = st.multiselect("States",
                                 sorted(df_full['State'].unique().tolist()),
                                 default=sorted(df_full['State'].unique().tolist()))

    st.markdown("<hr style='border-color:#2D2B3D; margin:20px 0 12px;'>", unsafe_allow_html=True)
    st.caption("Data: 11,239 transactions · 16 states · 18 categories")

# ── Apply filters ─────────────────────────────────────────────────────────────
df = df_full.copy()
if sel_gender  != 'All':  df = df[df['Gender_Label']         == sel_gender]
if sel_zone    != 'All':  df = df[df['Zone']                 == sel_zone]
if sel_marital != 'All':  df = df[df['Marital_Status_Label'] == sel_marital]
if sel_ages:              df = df[df['Age Group'].isin(sel_ages)]
if sel_states:            df = df[df['State'].isin(sel_states)]

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN CONTENT
# ═══════════════════════════════════════════════════════════════════════════════

# Hero header
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown("""
    <div class='hero-title'>🪔 Diwali Sales <span class='hero-accent'>Analysis</span></div>
    <div class='hero-subtitle'>Customer behavior &amp; revenue insights across demographics, geographies &amp; categories</div>
    """, unsafe_allow_html=True)
with col_h2:
    st.markdown(f"""
    <div style='text-align:right; padding-top:12px;'>
      <div style='font-size:0.75rem; color:{MUTED}; letter-spacing:0.08em; text-transform:uppercase;'>Filtered records</div>
      <div style='font-family:Syne,sans-serif; font-size:2rem; font-weight:800; color:{GOLD};'>{len(df):,}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)

# ── KPI cards ─────────────────────────────────────────────────────────────────
total_rev    = df['Amount'].sum()
total_orders = df['Orders'].sum()
total_cust   = df['User_ID'].nunique()
avg_order    = total_rev / total_orders if total_orders > 0 else 0
female_pct   = df[df['Gender'] == 'F']['Amount'].sum() / total_rev * 100 if total_rev > 0 else 0

k1, k2, k3, k4, k5 = st.columns(5)
kpis = [
    (k1, f"₹{total_rev/1e7:.2f} Cr",  "Total Revenue",    "Festive season"),
    (k2, f"{total_orders:,}",          "Total Orders",     "Placed"),
    (k3, f"{total_cust:,}",            "Customers",        "Unique buyers"),
    (k4, f"₹{avg_order:,.0f}",         "Avg Order Value",  "Per order"),
    (k5, f"{female_pct:.1f}%",         "Female Share",     "Of revenue"),
]
for col, num, lbl, sub in kpis:
    with col:
        st.markdown(f"""
        <div class='kpi-card'>
          <div class='kpi-number'>{num}</div>
          <div class='kpi-label'>{lbl}</div>
          <div class='kpi-sub'>{sub}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)
chart_style()

# ═══════════════════════════════════════════════════════════════════════════════
# ROW 1 — Gender + Age
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("<div class='section-title'>Demographics</div>", unsafe_allow_html=True)
c1, c2 = st.columns([1, 1.6])

with c1:
    g_rev = df.groupby('Gender_Label')['Amount'].sum()
    if not g_rev.empty:
        fig, ax = plt.subplots(figsize=(5, 4), facecolor=CHART_BG)
        wedges, texts, autotexts = ax.pie(
            g_rev.values, labels=g_rev.index, autopct='%1.1f%%',
            colors=[ORANGE, GOLD], startangle=90,
            wedgeprops=dict(edgecolor=CHART_BG, linewidth=2.5),
        )
        for t in texts:   t.set_color(TEXT);  t.set_fontsize(11)
        for a in autotexts: a.set_color(DARK_BG); a.set_fontweight('bold'); a.set_fontsize(10)
        ax.set_title("Revenue by Gender", color=TEXT, fontsize=12, fontweight='bold', pad=12)
        st.pyplot(fig, use_container_width=True)
        plt.close()
    st.markdown(f"""<div class='insight-box'>
      Female buyers drive <b>{female_pct:.1f}%</b> of total revenue —
      they shop more frequently and in higher volumes during Diwali.
    </div>""", unsafe_allow_html=True)

with c2:
    age_data = df.groupby('Age Group', observed=True)['Amount'].sum().reindex(AGE_ORDER).dropna()
    if not age_data.empty:
        fig, ax = plt.subplots(figsize=(7, 4), facecolor=CHART_BG)
        bars = ax.bar(age_data.index, age_data.values, color=COLORS[:len(age_data)],
                      edgecolor=CHART_BG, linewidth=1.5, width=0.7)
        for bar, val in zip(bars, age_data.values):
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+100000,
                    f"₹{val/1e6:.1f}M", ha='center', fontsize=8, color=MUTED)
        polish(ax, "Revenue by Age Group")
        inr_fmt(ax)
        st.pyplot(fig, use_container_width=True)
        plt.close()
    top_age = age_data.idxmax() if not age_data.empty else "26-35"
    st.markdown(f"""<div class='insight-box'>
      The <b>{top_age}</b> age group dominates — young professionals with
      disposable income and high Diwali gifting activity.
    </div>""", unsafe_allow_html=True)

st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# ROW 2 — State + Zone
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("<div class='section-title'>Geography</div>", unsafe_allow_html=True)
c3, c4 = st.columns([1.5, 1])

with c3:
    state_data = df.groupby('State')['Amount'].sum().sort_values(ascending=False).head(10)
    if not state_data.empty:
        fig, ax = plt.subplots(figsize=(7, 5), facecolor=CHART_BG)
        colors_h = [ORANGE if i == 0 else GOLD if i == 1 else "#3D3A54" for i in range(len(state_data))]
        bars = ax.barh(state_data.index[::-1], state_data.values[::-1],
                       color=colors_h[::-1], edgecolor=CHART_BG, linewidth=1, height=0.65)
        for bar, val in zip(ax.patches, state_data.values[::-1]):
            ax.text(bar.get_width()+200000, bar.get_y()+bar.get_height()/2,
                    f"₹{val/1e6:.1f}M", va='center', fontsize=8.5, color=MUTED)
        ax.set_title("Top 10 States by Revenue", color=TEXT, fontsize=12, fontweight='bold', pad=10)
        ax.spines[['top', 'right', 'left', 'bottom']].set_visible(False)
        ax.tick_params(colors=MUTED, length=0)
        inr_fmt(ax, 'x')
        ax.grid(axis='x', alpha=0.3)
        st.pyplot(fig, use_container_width=True)
        plt.close()

with c4:
    zone_data = df.groupby('Zone').agg(Amount=('Amount','sum'), Orders=('Orders','sum')) \
                  .sort_values('Amount', ascending=False).reset_index()
    if not zone_data.empty:
        fig, ax = plt.subplots(figsize=(5, 5), facecolor=CHART_BG)
        zone_colors = [ORANGE if i==0 else GOLD if i==1 else "#3D3A54" for i in range(len(zone_data))]
        bars = ax.bar(zone_data['Zone'], zone_data['Amount'],
                      color=zone_colors, edgecolor=CHART_BG, linewidth=1.5, width=0.65)
        polish(ax, "Revenue by Zone")
        inr_fmt(ax)
        ax.set_xticklabels(zone_data['Zone'], rotation=15, ha='right', fontsize=9)
        st.pyplot(fig, use_container_width=True)
        plt.close()
    top_zone = zone_data.iloc[0]['Zone'] if not zone_data.empty else "Central"
    top_state = state_data.index[0] if not state_data.empty else "Uttar Pradesh"
    st.markdown(f"""<div class='insight-box'>
      <b>{top_state}</b> leads all states. The <b>{top_zone}</b> zone
      dominates regionally — concentrate logistics and inventory here.
    </div>""", unsafe_allow_html=True)

st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# ROW 3 — Occupation + Product Category
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("<div class='section-title'>Occupation &amp; Products</div>", unsafe_allow_html=True)
c5, c6 = st.columns(2)

with c5:
    occ_data = df.groupby('Occupation')['Amount'].sum().sort_values(ascending=False)
    if not occ_data.empty:
        fig, ax = plt.subplots(figsize=(6, 4.5), facecolor=CHART_BG)
        bar_colors = [ORANGE if i==0 else GOLD if i==1 else "#3D3A54" for i in range(len(occ_data))]
        ax.bar(occ_data.index, occ_data.values, color=bar_colors, edgecolor=CHART_BG, linewidth=1, width=0.7)
        polish(ax, "Revenue by Occupation")
        inr_fmt(ax)
        ax.set_xticklabels(occ_data.index, rotation=40, ha='right', fontsize=8)
        st.pyplot(fig, use_container_width=True)
        plt.close()
    top_occ = occ_data.index[0] if not occ_data.empty else "IT Sector"
    st.markdown(f"""<div class='insight-box'>
      <b>{top_occ}</b> professionals are the top spenders — high salaries
      and tech-savvy shopping habits drive festive purchases.
    </div>""", unsafe_allow_html=True)

with c6:
    cat_data = df.groupby('Product_Category')['Amount'].sum().sort_values(ascending=False).head(10)
    if not cat_data.empty:
        fig, ax = plt.subplots(figsize=(6, 4.5), facecolor=CHART_BG)
        cat_colors = [ORANGE if i==0 else GOLD if i==1 else "#3D3A54" for i in range(len(cat_data))]
        ax.barh(cat_data.index[::-1], cat_data.values[::-1],
                color=cat_colors[::-1], edgecolor=CHART_BG, linewidth=1, height=0.7)
        ax.set_title("Top 10 Product Categories", color=TEXT, fontsize=12, fontweight='bold', pad=10)
        ax.spines[['top','right','left','bottom']].set_visible(False)
        ax.tick_params(colors=MUTED, length=0)
        inr_fmt(ax, 'x')
        ax.grid(axis='x', alpha=0.3)
        st.pyplot(fig, use_container_width=True)
        plt.close()
    top_cat = cat_data.index[0] if not cat_data.empty else "Food"
    st.markdown(f"""<div class='insight-box'>
      <b>{top_cat}</b> is the best-selling category. Feature it prominently
      in Diwali campaigns and ensure ample inventory.
    </div>""", unsafe_allow_html=True)

st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# ROW 4 — Marital Status + Correlation
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("<div class='section-title'>Marital Status &amp; Correlation</div>", unsafe_allow_html=True)
c7, c8 = st.columns(2)

with c7:
    mar = df.groupby(['Marital_Status_Label', 'Gender_Label'])['Amount'].sum().unstack(fill_value=0)
    if not mar.empty and mar.shape[1] > 0:
        fig, ax = plt.subplots(figsize=(6, 4), facecolor=CHART_BG)
        x = range(len(mar.index))
        w = 0.35
        cols_list = mar.columns.tolist()
        bar_c = [ORANGE, GOLD]
        for i, (col, bc) in enumerate(zip(cols_list, bar_c)):
            offset = [xi + (i - len(cols_list)/2 + 0.5)*w for xi in x]
            ax.bar(offset, mar[col].values, width=w, label=col, color=bc, edgecolor=CHART_BG, linewidth=1)
        ax.set_xticks(list(x))
        ax.set_xticklabels(mar.index, fontsize=10)
        ax.legend(fontsize=9, facecolor=CARD_BG, labelcolor=TEXT, framealpha=0.8)
        polish(ax, "Revenue by Marital Status & Gender")
        inr_fmt(ax)
        st.pyplot(fig, use_container_width=True)
        plt.close()
    st.markdown(f"""<div class='insight-box'>
      <b>Married women</b> are the single highest-value segment — ideal
      target for family bundle offers and gifting campaigns.
    </div>""", unsafe_allow_html=True)

with c8:
    corr = df[['Age', 'Marital_Status', 'Orders', 'Amount']].corr()
    fig, ax = plt.subplots(figsize=(6, 4), facecolor=CHART_BG)
    sns.heatmap(corr, annot=True, fmt='.2f',
                cmap=sns.diverging_palette(220, 20, as_cmap=True),
                linewidths=0.5, linecolor=CHART_BG, ax=ax,
                annot_kws={'size': 11, 'color': TEXT})
    ax.set_title("Correlation Heatmap", color=TEXT, fontsize=12, fontweight='bold', pad=10)
    ax.tick_params(colors=MUTED, length=0)
    for spine in ax.spines.values(): spine.set_visible(False)
    st.pyplot(fig, use_container_width=True)
    plt.close()
    st.markdown("""<div class='insight-box'>
      <b>Orders ↔ Amount</b> shows the strongest correlation — more orders
      directly drive higher revenue per customer.
    </div>""", unsafe_allow_html=True)

st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# RAW DATA TABLE (collapsible)
# ═══════════════════════════════════════════════════════════════════════════════
with st.expander("📋 View filtered raw data"):
    display_cols = ['User_ID','Gender_Label','Age Group','Marital_Status_Label',
                    'State','Zone','Occupation','Product_Category','Orders','Amount']
    st.dataframe(
        df[display_cols].rename(columns={
            'Gender_Label':'Gender', 'Marital_Status_Label':'Marital Status',
            'Age Group':'Age Group', 'Product_Category':'Category'
        }).reset_index(drop=True),
        use_container_width=True,
        height=320,
    )
    st.caption(f"{len(df):,} rows shown after filters")

# Footer
st.markdown(f"""
<div style='text-align:center; padding:40px 0 20px; color:{MUTED}; font-size:0.8rem;'>
  🪔 Diwali Sales Analysis &nbsp;·&nbsp; Built with Python &amp; Streamlit
</div>
""", unsafe_allow_html=True)
