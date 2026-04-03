"""
eda_analysis.py
---------------
Generates all EDA visualizations from the clean Diwali Sales dataset.
Run data_cleaning.py first to produce Diwali_Sales_Clean.csv.

Charts saved to: ../charts/
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os, warnings
warnings.filterwarnings('ignore')

# ── Paths ────────────────────────────────────────────────────────────────────
BASE       = os.path.join(os.path.dirname(__file__), '..')
DATA_PATH  = os.path.join(BASE, 'data', 'Diwali_Sales_Clean.csv')
CHART_DIR  = os.path.join(BASE, 'charts')
os.makedirs(CHART_DIR, exist_ok=True)

# ── Palette ──────────────────────────────────────────────────────────────────
ORANGE  = "#E8650A"
GOLD    = "#F5A623"
DARK    = "#1A1A2E"
ACCENT  = "#FF6B35"
COLORS  = [ORANGE, GOLD, "#E74C3C", "#3498DB", "#2ECC71",
           "#9B59B6", "#1ABC9C", "#F39C12", "#E67E22", "#16A085"]

AGE_ORDER = ['0-17', '18-25', '26-35', '36-45', '46-50', '51-55', '55+']


# ── Helpers ──────────────────────────────────────────────────────────────────
def save(fig, name: str) -> str:
    path = os.path.join(CHART_DIR, f"{name}.png")
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  Saved: {name}.png")
    return path


def fmt_inr(ax, axis='y'):
    fmt = plt.FuncFormatter(lambda x, _: f"₹{x/1e6:.1f}M" if x >= 1e6 else f"₹{x/1e3:.0f}K")
    if axis == 'y':
        ax.yaxis.set_major_formatter(fmt)
    else:
        ax.xaxis.set_major_formatter(fmt)


def polish(ax, title="", xlabel="", ylabel=""):
    ax.set_title(title, fontsize=13, fontweight='bold', color=DARK, pad=10)
    ax.set_xlabel(xlabel, fontsize=10, color='#555')
    ax.set_ylabel(ylabel, fontsize=10, color='#555')
    ax.spines[['top', 'right']].set_visible(False)
    ax.tick_params(colors='#333')
    ax.grid(axis='y', alpha=0.25, linestyle='--')


# ══════════════════════════════════════════════════════════════════════════════
# 1. GENDER ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
def plot_gender(df):
    g_rev = df.groupby('Gender_Label')['Amount'].sum()
    g_ord = df.groupby('Gender_Label')['Orders'].sum()

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))
    for ax, data, title, clr in zip(
        axes,
        [g_rev, g_ord],
        ['Revenue Share by Gender', 'Order Share by Gender'],
        [[ORANGE, GOLD], [ACCENT, '#3498DB']]
    ):
        ax.pie(data.values, labels=data.index, autopct='%1.1f%%',
               colors=clr, startangle=90,
               wedgeprops=dict(edgecolor='white', linewidth=2),
               textprops={'fontsize': 11})
        ax.set_title(title, fontsize=13, fontweight='bold', color=DARK)

    fig.suptitle("Gender Analysis", fontsize=15, fontweight='bold', color=DARK, y=1.02)
    fig.tight_layout()
    return save(fig, "01_gender")


# ══════════════════════════════════════════════════════════════════════════════
# 2. AGE GROUP ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
def plot_age(df):
    age = df.groupby('Age Group', observed=True).agg(
        Amount=('Amount', 'sum'),
        Orders=('Orders', 'sum'),
        Customers=('User_ID', 'nunique')
    ).reindex(AGE_ORDER).reset_index()

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    # Revenue
    bars = axes[0].bar(age['Age Group'], age['Amount'], color=COLORS[:len(age)], edgecolor='white')
    polish(axes[0], "Revenue by Age Group", "Age Group", "Revenue (₹)")
    fmt_inr(axes[0])
    for bar, val in zip(bars, age['Amount']):
        axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 200000,
                     f"₹{val/1e6:.1f}M", ha='center', va='bottom', fontsize=8, color=DARK, fontweight='bold')

    # Orders
    axes[1].bar(age['Age Group'], age['Orders'], color=COLORS[:len(age)], edgecolor='white')
    polish(axes[1], "Orders by Age Group", "Age Group", "Total Orders")
    axes[1].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x):,}"))

    fig.suptitle("Age Group Analysis", fontsize=15, fontweight='bold', color=DARK)
    fig.tight_layout()
    return save(fig, "02_age_group")


# ══════════════════════════════════════════════════════════════════════════════
# 3. STATE ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
def plot_state(df):
    state = df.groupby('State')['Amount'].sum().sort_values(ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(11, 5))
    bars = ax.barh(state.index[::-1], state.values[::-1], color=COLORS[:10], edgecolor='white')
    ax.set_title("Top 10 States by Revenue", fontsize=13, fontweight='bold', color=DARK, pad=10)
    ax.set_xlabel("Revenue (₹)", fontsize=10)
    ax.spines[['top', 'right']].set_visible(False)
    fmt_inr(ax, axis='x')
    ax.grid(axis='x', alpha=0.25, linestyle='--')
    for bar, val in zip(ax.patches, state.values[::-1]):
        ax.text(bar.get_width() + 100000, bar.get_y() + bar.get_height()/2,
                f"₹{val/1e6:.1f}M", va='center', fontsize=9, fontweight='bold', color=DARK)
    fig.tight_layout()
    return save(fig, "03_state")


# ══════════════════════════════════════════════════════════════════════════════
# 4. ZONE ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
def plot_zone(df):
    zone = df.groupby('Zone').agg(Amount=('Amount', 'sum'), Orders=('Orders', 'sum')) \
             .sort_values('Amount', ascending=False).reset_index()

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    axes[0].bar(zone['Zone'], zone['Amount'], color=COLORS[:5], edgecolor='white')
    polish(axes[0], "Revenue by Zone", "Zone", "Revenue (₹)")
    fmt_inr(axes[0])

    axes[1].bar(zone['Zone'], zone['Orders'], color=[GOLD, ORANGE, ACCENT, '#3498DB', '#2ECC71'], edgecolor='white')
    polish(axes[1], "Orders by Zone", "Zone", "Total Orders")

    fig.suptitle("Zone / Regional Analysis", fontsize=15, fontweight='bold', color=DARK)
    fig.tight_layout()
    return save(fig, "04_zone")


# ══════════════════════════════════════════════════════════════════════════════
# 5. OCCUPATION ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
def plot_occupation(df):
    occ = df.groupby('Occupation')['Amount'].sum().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(12, 5))
    bars = ax.bar(occ.index, occ.values, color=COLORS[:len(occ)], edgecolor='white')
    polish(ax, "Revenue by Occupation", "Occupation", "Revenue (₹)")
    fmt_inr(ax)
    ax.set_xticklabels(occ.index, rotation=35, ha='right', fontsize=9)
    fig.tight_layout()
    return save(fig, "05_occupation")


# ══════════════════════════════════════════════════════════════════════════════
# 6. PRODUCT CATEGORY ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
def plot_category(df):
    cat = df.groupby('Product_Category')['Amount'].sum().sort_values(ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(11, 5))
    ax.barh(cat.index[::-1], cat.values[::-1], color=COLORS[:10], edgecolor='white')
    ax.set_title("Top 10 Product Categories by Revenue", fontsize=13, fontweight='bold', color=DARK)
    ax.set_xlabel("Revenue (₹)", fontsize=10)
    ax.spines[['top', 'right']].set_visible(False)
    fmt_inr(ax, axis='x')
    ax.grid(axis='x', alpha=0.25, linestyle='--')
    for bar, val in zip(ax.patches, cat.values[::-1]):
        ax.text(bar.get_width() + 100000, bar.get_y() + bar.get_height()/2,
                f"₹{val/1e6:.1f}M", va='center', fontsize=9, fontweight='bold', color=DARK)
    fig.tight_layout()
    return save(fig, "06_product_category")


# ══════════════════════════════════════════════════════════════════════════════
# 7. MARITAL STATUS × GENDER
# ══════════════════════════════════════════════════════════════════════════════
def plot_marital(df):
    mar = df.groupby(['Marital_Status_Label', 'Gender_Label'])['Amount'].sum().unstack()

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    mar.plot(kind='bar', ax=axes[0], color=[ORANGE, GOLD], edgecolor='white', width=0.6)
    polish(axes[0], "Revenue by Marital Status & Gender", "", "Revenue (₹)")
    fmt_inr(axes[0])
    axes[0].set_xticklabels(mar.index, rotation=0)
    axes[0].legend(title='Gender')

    # Count of customers
    mar_count = df.groupby(['Marital_Status_Label', 'Gender_Label'])['User_ID'].nunique().unstack()
    mar_count.plot(kind='bar', ax=axes[1], color=[ACCENT, '#3498DB'], edgecolor='white', width=0.6)
    polish(axes[1], "Customer Count by Marital Status & Gender", "", "Customers")
    axes[1].set_xticklabels(mar_count.index, rotation=0)
    axes[1].legend(title='Gender')

    fig.suptitle("Marital Status Analysis", fontsize=15, fontweight='bold', color=DARK)
    fig.tight_layout()
    return save(fig, "07_marital_status")


# ══════════════════════════════════════════════════════════════════════════════
# 8. CORRELATION HEATMAP
# ══════════════════════════════════════════════════════════════════════════════
def plot_correlation(df):
    num_cols = df[['Age', 'Marital_Status', 'Orders', 'Amount']].copy()
    corr = num_cols.corr()

    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='YlOrRd',
                linewidths=0.5, ax=ax, annot_kws={'size': 11})
    ax.set_title("Correlation Heatmap (Numerical Features)", fontsize=13,
                 fontweight='bold', color=DARK, pad=10)
    fig.tight_layout()
    return save(fig, "08_correlation")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════
def main():
    # Load clean data (fall back to raw if clean not found)
    try:
        df = pd.read_csv(DATA_PATH)
        print(f"✅ Loaded clean data: {df.shape[0]:,} rows")
    except FileNotFoundError:
        raw = os.path.join(BASE, 'data', 'Diwali_Sales_Data.csv')
        df  = pd.read_csv(raw, encoding='latin1')
        df  = df.drop(columns=['Status', 'unnamed1'], errors='ignore').dropna(subset=['Amount'])
        df['Amount']              = df['Amount'].astype(int)
        df['Gender_Label']        = df['Gender'].map({'F': 'Female', 'M': 'Male'})
        df['Marital_Status_Label']= df['Marital_Status'].map({0: 'Single', 1: 'Married'})
        df['Age Group']           = pd.Categorical(df['Age Group'],
                                                   categories=AGE_ORDER, ordered=True)
        print(f"⚠️  Clean CSV not found — loaded raw directly: {df.shape[0]:,} rows")

    print("\n📊 Generating charts...")
    plot_gender(df)
    plot_age(df)
    plot_state(df)
    plot_zone(df)
    plot_occupation(df)
    plot_category(df)
    plot_marital(df)
    plot_correlation(df)

    print(f"\n✅ All 8 charts saved to: {CHART_DIR}")


if __name__ == '__main__':
    main()
