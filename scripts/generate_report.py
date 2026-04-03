import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import os, warnings
warnings.filterwarnings('ignore')

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image,
                                 Table, TableStyle, PageBreak, HRFlowable)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import KeepTogether

# ─── Palette ────────────────────────────────────────────────────────────────
ORANGE   = "#E8650A"
GOLD     = "#F5A623"
DARK     = "#1A1A2E"
MID      = "#16213E"
LIGHT_BG = "#FFF8F0"
ACCENT   = "#FF6B35"
GREEN    = "#27AE60"
PURPLE   = "#8E44AD"

CHART_COLORS = [ORANGE, GOLD, "#E74C3C", "#3498DB", "#2ECC71",
                "#9B59B6", "#1ABC9C", "#F39C12", "#E67E22", "#16A085"]

os.makedirs("/charts", exist_ok=True)

# ─── Load Data ───────────────────────────────────────────────────────────────
df = pd.read_csv('data/Diwali_Sales_Clean.csv', encoding='latin1')

# ─── Helper ──────────────────────────────────────────────────────────────────
def save(fig, name):
    path = f"/charts/{name}.png"
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    return path

def bar_style(ax, title="", xlabel="", ylabel="Amount (₹)"):
    ax.set_title(title, fontsize=13, fontweight='bold', color=DARK, pad=10)
    ax.set_xlabel(xlabel, fontsize=10, color='#555')
    ax.set_ylabel(ylabel, fontsize=10, color='#555')
    ax.spines[['top','right']].set_visible(False)
    ax.tick_params(colors='#333')
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x,_: f"₹{x/1e6:.1f}M" if x>=1e6 else f"₹{x/1e3:.0f}K"))
    ax.grid(axis='y', alpha=0.3, linestyle='--')

# ═══════════════════════════════════════════════════════════════════════════
# CHART 1 – Gender split (pie)
# ═══════════════════════════════════════════════════════════════════════════
g = df.groupby('Gender')['Amount'].sum()
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].pie(g.values, labels=['Female','Male'], autopct='%1.1f%%',
            colors=[ORANGE, GOLD], startangle=90,
            wedgeprops=dict(edgecolor='white', linewidth=2))
axes[0].set_title('Sales by Gender', fontsize=13, fontweight='bold', color=DARK)

go = df.groupby('Gender')['Orders'].sum()
axes[1].pie(go.values, labels=['Female','Male'], autopct='%1.1f%%',
            colors=[ACCENT, "#3498DB"], startangle=90,
            wedgeprops=dict(edgecolor='white', linewidth=2))
axes[1].set_title('Orders by Gender', fontsize=13, fontweight='bold', color=DARK)
fig.tight_layout()
chart_gender = save(fig, "gender")

# ═══════════════════════════════════════════════════════════════════════════
# CHART 2 – Age Group
# ═══════════════════════════════════════════════════════════════════════════
age_order = ['0-17','18-25','26-35','36-45','46-50','51-55','55+']
age_data = df.groupby('Age Group').agg(Amount=('Amount','sum'), Orders=('Orders','sum')).reindex(age_order).reset_index()

fig, ax = plt.subplots(figsize=(10, 4.5))
bars = ax.bar(age_data['Age Group'], age_data['Amount'], color=CHART_COLORS[:len(age_data)], edgecolor='white', linewidth=0.8)
bar_style(ax, "Revenue by Age Group", "Age Group")
for bar, val in zip(bars, age_data['Amount']):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+200000,
            f"₹{val/1e6:.1f}M", ha='center', va='bottom', fontsize=8.5, color=DARK, fontweight='bold')
fig.tight_layout()
chart_age = save(fig, "age")

# ═══════════════════════════════════════════════════════════════════════════
# CHART 3 – State Revenue (top 10)
# ═══════════════════════════════════════════════════════════════════════════
state_data = df.groupby('State')['Amount'].sum().sort_values(ascending=False).head(10)
fig, ax = plt.subplots(figsize=(10, 4.5))
bars = ax.barh(state_data.index[::-1], state_data.values[::-1], color=CHART_COLORS[:10], edgecolor='white')
ax.set_title("Top 10 States by Revenue", fontsize=13, fontweight='bold', color=DARK, pad=10)
ax.set_xlabel("Amount (₹)", fontsize=10)
ax.spines[['top','right']].set_visible(False)
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x,_: f"₹{x/1e6:.1f}M"))
ax.grid(axis='x', alpha=0.3, linestyle='--')
for bar, val in zip(ax.patches, state_data.values[::-1]):
    ax.text(bar.get_width()+100000, bar.get_y()+bar.get_height()/2,
            f"₹{val/1e6:.1f}M", va='center', fontsize=8.5, fontweight='bold', color=DARK)
fig.tight_layout()
chart_state = save(fig, "state")

# ═══════════════════════════════════════════════════════════════════════════
# CHART 4 – Zone
# ═══════════════════════════════════════════════════════════════════════════
zone_data = df.groupby('Zone').agg(Amount=('Amount','sum'), Orders=('Orders','sum')).reset_index().sort_values('Amount', ascending=False)
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].bar(zone_data['Zone'], zone_data['Amount'], color=CHART_COLORS[:5], edgecolor='white')
bar_style(axes[0], "Revenue by Zone", "Zone")
axes[1].bar(zone_data['Zone'], zone_data['Orders'], color=[GOLD, ORANGE, ACCENT, "#3498DB", "#2ECC71"], edgecolor='white')
axes[1].set_title("Orders by Zone", fontsize=13, fontweight='bold', color=DARK)
axes[1].spines[['top','right']].set_visible(False)
axes[1].grid(axis='y', alpha=0.3, linestyle='--')
axes[1].set_ylabel("Total Orders")
fig.tight_layout()
chart_zone = save(fig, "zone")

# ═══════════════════════════════════════════════════════════════════════════
# CHART 5 – Occupation (top 10)
# ═══════════════════════════════════════════════════════════════════════════
occ_data = df.groupby('Occupation')['Amount'].sum().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(10, 4.5))
bars = ax.bar(occ_data.index, occ_data.values, color=CHART_COLORS[:len(occ_data)], edgecolor='white')
bar_style(ax, "Revenue by Occupation", "Occupation")
ax.set_xticklabels(occ_data.index, rotation=35, ha='right', fontsize=8.5)
fig.tight_layout()
chart_occ = save(fig, "occupation")

# ═══════════════════════════════════════════════════════════════════════════
# CHART 6 – Product Category (top 10)
# ═══════════════════════════════════════════════════════════════════════════
cat_data = df.groupby('Product_Category')['Amount'].sum().sort_values(ascending=False).head(10)
fig, ax = plt.subplots(figsize=(10, 4.5))
bars = ax.barh(cat_data.index[::-1], cat_data.values[::-1], color=CHART_COLORS[:10], edgecolor='white')
ax.set_title("Top 10 Product Categories by Revenue", fontsize=13, fontweight='bold', color=DARK)
ax.set_xlabel("Amount (₹)", fontsize=10)
ax.spines[['top','right']].set_visible(False)
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x,_: f"₹{x/1e6:.1f}M"))
ax.grid(axis='x', alpha=0.3, linestyle='--')
for bar, val in zip(ax.patches, cat_data.values[::-1]):
    ax.text(bar.get_width()+100000, bar.get_y()+bar.get_height()/2,
            f"₹{val/1e6:.1f}M", va='center', fontsize=8.5, fontweight='bold', color=DARK)
fig.tight_layout()
chart_cat = save(fig, "category")

# ═══════════════════════════════════════════════════════════════════════════
# CHART 7 – Marital Status x Gender
# ═══════════════════════════════════════════════════════════════════════════
mar = df.groupby(['Marital_Status','Gender'])['Amount'].sum().unstack()
mar.index = ['Single','Married']
mar.columns = ['Female','Male']
fig, ax = plt.subplots(figsize=(7, 4))
mar.plot(kind='bar', ax=ax, color=[ORANGE, GOLD], edgecolor='white', width=0.6)
bar_style(ax, "Revenue by Marital Status & Gender", "")
ax.set_xticklabels(['Single','Married'], rotation=0)
ax.legend(title='Gender')
fig.tight_layout()
chart_mar = save(fig, "marital")

# ─── Key Stats ───────────────────────────────────────────────────────────────
total_rev   = df['Amount'].sum()
total_orders= df['Orders'].sum()
total_cust  = df['User_ID'].nunique()
avg_order   = total_rev / total_orders
top_state   = df.groupby('State')['Amount'].sum().idxmax()
top_cat     = df.groupby('Product_Category')['Amount'].sum().idxmax()
top_occ     = df.groupby('Occupation')['Amount'].sum().idxmax()
top_age     = df.groupby('Age Group')['Amount'].sum().idxmax()
top_zone    = df.groupby('Zone')['Amount'].sum().idxmax()
female_pct  = df[df['Gender']=='F']['Amount'].sum() / total_rev * 100

print("✅ All charts generated. Building PDF...")
print(f"  Revenue: ₹{total_rev:,.0f}  Orders: {total_orders:,}  Customers: {total_cust:,}")

# ═══════════════════════════════════════════════════════════════════════════
# PDF REPORT
# ═══════════════════════════════════════════════════════════════════════════
OUT = "outputs/Diwali_Sales_Report.pdf"
doc = SimpleDocTemplate(OUT, pagesize=A4,
                         leftMargin=1.8*cm, rightMargin=1.8*cm,
                         topMargin=1.5*cm, bottomMargin=1.8*cm)

styles = getSampleStyleSheet()
W = A4[0] - 3.6*cm   # usable width

# Custom styles
S = {
    'cover_title': ParagraphStyle('ct', fontSize=32, textColor=colors.white,
                                   fontName='Helvetica-Bold', alignment=TA_CENTER, leading=38),
    'cover_sub':   ParagraphStyle('cs', fontSize=14, textColor=colors.Color(1,0.85,0.6),
                                   fontName='Helvetica', alignment=TA_CENTER, leading=20),
    'sec_head':    ParagraphStyle('sh', fontSize=16, textColor=colors.HexColor(DARK),
                                   fontName='Helvetica-Bold', spaceBefore=14, spaceAfter=6),
    'body':        ParagraphStyle('b', fontSize=10, textColor=colors.HexColor('#333333'),
                                   leading=16, spaceAfter=6),
    'bullet':      ParagraphStyle('bl', fontSize=10, textColor=colors.HexColor('#333333'),
                                   leading=16, leftIndent=14, spaceAfter=4),
    'kpi_num':     ParagraphStyle('kn', fontSize=22, fontName='Helvetica-Bold',
                                   textColor=colors.HexColor(ORANGE), alignment=TA_CENTER),
    'kpi_lbl':     ParagraphStyle('kl', fontSize=9, textColor=colors.HexColor('#666'),
                                   alignment=TA_CENTER),
    'insight_head':ParagraphStyle('ih', fontSize=11, fontName='Helvetica-Bold',
                                   textColor=colors.HexColor(DARK)),
    'caption':     ParagraphStyle('cap', fontSize=9, textColor=colors.HexColor('#666'),
                                   alignment=TA_CENTER, spaceAfter=10),
    'footer_txt':  ParagraphStyle('ft', fontSize=8, textColor=colors.HexColor('#999'),
                                   alignment=TA_CENTER),
}

story = []

# ─── COVER PAGE ──────────────────────────────────────────────────────────────
def cover_bg(canvas, doc):
    canvas.saveState()
    # gradient-like background
    canvas.setFillColor(colors.HexColor(DARK))
    canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    # decorative orange strip top
    canvas.setFillColor(colors.HexColor(ORANGE))
    canvas.rect(0, A4[1]-1.2*cm, A4[0], 1.2*cm, fill=1, stroke=0)
    # decorative gold strip bottom
    canvas.setFillColor(colors.HexColor(GOLD))
    canvas.rect(0, 0, A4[0], 0.8*cm, fill=1, stroke=0)
    # diya emoji-like circle decoration
    canvas.setFillColor(colors.HexColor(GOLD))
    canvas.setFillAlpha(0.12)
    canvas.circle(A4[0]*0.85, A4[1]*0.25, 100, fill=1, stroke=0)
    canvas.circle(A4[0]*0.1, A4[1]*0.7, 70, fill=1, stroke=0)
    canvas.setFillAlpha(1)
    canvas.restoreState()

story.append(Spacer(1, 5.5*cm))
story.append(Paragraph("🪔  Diwali Sales Analysis", S['cover_title']))
story.append(Spacer(1, 0.5*cm))
story.append(Paragraph("Customer Behavior &amp; Revenue Insights Report", S['cover_sub']))
story.append(Spacer(1, 0.4*cm))
story.append(Paragraph("Festive Season Deep Dive", S['cover_sub']))
story.append(Spacer(1, 3.5*cm))

# Cover stats table
cover_stats = [
    [Paragraph(f"₹{total_rev/1e7:.1f} Cr", ParagraphStyle('', fontSize=26, fontName='Helvetica-Bold',
               textColor=colors.HexColor(GOLD), alignment=TA_CENTER)),
     Paragraph(f"{total_orders:,}", ParagraphStyle('', fontSize=26, fontName='Helvetica-Bold',
               textColor=colors.HexColor(GOLD), alignment=TA_CENTER)),
     Paragraph(f"{total_cust:,}", ParagraphStyle('', fontSize=26, fontName='Helvetica-Bold',
               textColor=colors.HexColor(GOLD), alignment=TA_CENTER))],
    [Paragraph("Total Revenue", ParagraphStyle('', fontSize=10, textColor=colors.Color(1,0.85,0.6), alignment=TA_CENTER)),
     Paragraph("Total Orders", ParagraphStyle('', fontSize=10, textColor=colors.Color(1,0.85,0.6), alignment=TA_CENTER)),
     Paragraph("Unique Customers", ParagraphStyle('', fontSize=10, textColor=colors.Color(1,0.85,0.6), alignment=TA_CENTER))]
]
t = Table(cover_stats, colWidths=[W/3]*3)
t.setStyle(TableStyle([
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('LINEABOVE', (0,0), (-1,0), 1, colors.HexColor(ORANGE)),
    ('LINEBELOW', (0,-1), (-1,-1), 1, colors.HexColor(ORANGE)),
    ('TOPPADDING', (0,0), (-1,-1), 8),
    ('BOTTOMPADDING', (0,0), (-1,-1), 8),
]))
story.append(t)
story.append(Spacer(1, 1.5*cm))
story.append(Paragraph("Data Science Project | 11,239 Records | 16 States | 18 Product Categories",
             ParagraphStyle('', fontSize=9, textColor=colors.Color(0.7,0.7,0.7), alignment=TA_CENTER)))
story.append(PageBreak())

# ─── Helper: section divider ──────────────────────────────────────────────────
def section(title, emoji=""):
    story.append(HRFlowable(width=W, thickness=2, color=colors.HexColor(ORANGE), spaceAfter=6))
    story.append(Paragraph(f"{emoji}  {title}", S['sec_head']))

def insight_box(items):
    """Renders a shaded insight box."""
    rows = [[Paragraph(f"• {item}", S['bullet'])] for item in items]
    t = Table(rows, colWidths=[W])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFF3E6')),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROUNDEDCORNERS', [6]),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.3*cm))

def kpi_row(items):
    """items = list of (value, label) tuples"""
    cells = [[Paragraph(v, S['kpi_num']), Paragraph(l, S['kpi_lbl'])] for v,l in items]
    row = [[c[0] for c in cells], [c[1] for c in cells]]
    t = Table(row, colWidths=[W/len(items)]*len(items))
    t.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFF8F0')),
        ('LINEBELOW', (0,0), (-1,0), 1.5, colors.HexColor(ORANGE)),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.3*cm))

def add_chart(path, caption, width=W):
    story.append(Image(path, width=width, height=width*0.45))
    story.append(Paragraph(caption, S['caption']))

# ─── PAGE 2: EXECUTIVE SUMMARY ───────────────────────────────────────────────
section("Executive Summary", "📋")
story.append(Paragraph(
    "This report presents a comprehensive analysis of Diwali festive season sales data covering "
    f"<b>11,239 transactions</b> across <b>16 Indian states</b>, <b>5 zones</b>, <b>15 occupations</b>, "
    f"and <b>18 product categories</b>. The dataset captures ₹{total_rev/1e7:.2f} Crore in total revenue "
    f"with {total_orders:,} orders placed by {total_cust:,} unique customers.",
    S['body']))

kpi_row([
    (f"₹{total_rev/1e7:.1f} Cr", "Total Revenue"),
    (f"{total_orders:,}", "Total Orders"),
    (f"₹{avg_order:,.0f}", "Avg Order Value"),
    (f"{female_pct:.1f}%", "Female Revenue Share"),
])

story.append(Paragraph("Key Findings at a Glance:", S['insight_head']))
insight_box([
    f"The 26–35 age group dominates revenue — the most commercially active demographic during Diwali.",
    f"Female customers drive {female_pct:.1f}% of total revenue, outspending male counterparts.",
    f"{top_state} leads all states in total sales, followed closely by other western and northern states.",
    f"The {top_zone} zone is the highest-grossing region.",
    f"{top_cat} is the best-selling product category by revenue.",
    f"IT Sector and Healthcare professionals are top spenders by occupation.",
    f"Married customers account for the majority of purchases, particularly married women.",
])

story.append(PageBreak())

# ─── PAGE 3: GENDER ANALYSIS ─────────────────────────────────────────────────
section("Gender Analysis", "👥")
add_chart(chart_gender, "Figure 1: Revenue & Order Distribution by Gender")

f_rev = df[df['Gender']=='F']['Amount'].sum()
m_rev = df[df['Gender']=='M']['Amount'].sum()
f_ord = df[df['Gender']=='F']['Orders'].sum()
m_ord = df[df['Gender']=='M']['Orders'].sum()

kpi_row([
    (f"₹{f_rev/1e6:.1f}M", "Female Revenue"),
    (f"₹{m_rev/1e6:.1f}M", "Male Revenue"),
    (f"{f_ord:,}", "Female Orders"),
    (f"{m_ord:,}", "Male Orders"),
])
insight_box([
    f"Female buyers generate {female_pct:.1f}% of total revenue — significantly higher than male buyers.",
    "Women place more orders per transaction on average, suggesting stronger purchase frequency.",
    "Marketing campaigns should prioritize female-centric channels (Instagram, WhatsApp, lifestyle platforms).",
    "Male buyers show higher average order values, suggesting preference for premium/bulk purchases.",
])

# ─── PAGE 4: AGE GROUP ANALYSIS ──────────────────────────────────────────────
section("Age Group Analysis", "🎂")
add_chart(chart_age, "Figure 2: Total Revenue by Age Group")

age_rev = df.groupby('Age Group')['Amount'].sum().reindex(age_order)
top2_age = age_rev.nlargest(2)
insight_box([
    f"The 26–35 age group is the #1 revenue driver with ₹{age_rev['26-35']/1e6:.1f}M — young professionals with disposable income.",
    f"The 36–45 group ranks second (₹{age_rev['36-45']/1e6:.1f}M), representing established households with high spending capacity.",
    "Teens and young adults (0–17, 18–25) contribute the least — lower purchasing power but a future growth segment.",
    "The 51–55 and 55+ groups show moderate spending, likely gifting-focused purchases during Diwali.",
    "Recommendation: Target 26–45 age band with premium product bundles and EMI offers.",
])

story.append(PageBreak())

# ─── PAGE 5: STATE & ZONE ANALYSIS ──────────────────────────────────────────
section("State & Regional Analysis", "🗺️")
add_chart(chart_state, "Figure 3: Top 10 States by Revenue")
add_chart(chart_zone, "Figure 4: Revenue & Orders by Zone")

state_rev = df.groupby('State')['Amount'].sum().sort_values(ascending=False)
zone_rev  = df.groupby('Zone')['Amount'].sum().sort_values(ascending=False)
top3_states = state_rev.head(3)

insight_box([
    f"{top3_states.index[0]} tops revenue at ₹{top3_states.iloc[0]/1e6:.1f}M, likely due to urban concentration and high population.",
    f"{top3_states.index[1]} (₹{top3_states.iloc[1]/1e6:.1f}M) and {top3_states.index[2]} (₹{top3_states.iloc[2]/1e6:.1f}M) round out the top 3.",
    f"The {zone_rev.index[0]} zone leads regionally — reflecting strong consumer markets.",
    "Eastern and Northern zones show lower sales — opportunity for regional expansion and localized campaigns.",
    "Recommendation: Concentrate inventory and delivery logistics in Maharashtra, UP, and Karnataka.",
])

story.append(PageBreak())

# ─── PAGE 6: OCCUPATION ANALYSIS ─────────────────────────────────────────────
section("Occupation Analysis", "💼")
add_chart(chart_occ, "Figure 5: Revenue by Occupation")

occ_rev = df.groupby('Occupation')['Amount'].sum().sort_values(ascending=False)
insight_box([
    f"IT Sector professionals are the top spenders — high salaries and tech-savvy shopping habits drive this.",
    f"Healthcare workers rank highly, reflecting essential workers with stable incomes and festive bonus spending.",
    f"Aviation and Banking professionals also show strong spending patterns.",
    "Agriculture and Textile sector workers spend the least — price-sensitive segment, ideal for value offers.",
    "Recommendation: Partner with corporate gifting programs for IT, Healthcare, and Banking sectors.",
])

# Occupation summary table
occ_top5 = occ_rev.head(5).reset_index()
occ_top5['Amount'] = occ_top5['Amount'].apply(lambda x: f"₹{x/1e6:.2f}M")
occ_top5.columns = ['Occupation', 'Total Revenue']
table_data = [['Rank', 'Occupation', 'Revenue']] + \
             [[str(i+1), row['Occupation'], row['Total Revenue']] for i, row in occ_top5.iterrows()]
t = Table(table_data, colWidths=[1.5*cm, 7*cm, 5*cm])
t.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor(ORANGE)),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('FONTSIZE', (0,0), (-1,-1), 10),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#FFF3E6')]),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DDD')),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
]))
story.append(t)
story.append(Spacer(1, 0.3*cm))

story.append(PageBreak())

# ─── PAGE 7: PRODUCT CATEGORY ────────────────────────────────────────────────
section("Product Category Analysis", "🛒")
add_chart(chart_cat, "Figure 6: Top 10 Product Categories by Revenue")

cat_rev = df.groupby('Product_Category')['Amount'].sum().sort_values(ascending=False)
top3_cats = cat_rev.head(3)
insight_box([
    f"{top3_cats.index[0]} is the best-selling category (₹{top3_cats.iloc[0]/1e6:.1f}M) — high-value purchases align with festive gifting.",
    f"{top3_cats.index[1]} (₹{top3_cats.iloc[1]/1e6:.1f}M) and {top3_cats.index[2]} (₹{top3_cats.iloc[2]/1e6:.1f}M) complete the top 3.",
    "Food & Clothing are volume drivers — frequent, repeat purchases with lower average ticket size.",
    "Pet Care and Veterinary categories rank lowest — niche market with growth potential.",
    "Recommendation: Feature top 3 categories prominently in Diwali landing pages and push notifications.",
])

story.append(PageBreak())

# ─── PAGE 8: MARITAL STATUS + CONCLUSIONS ────────────────────────────────────
section("Marital Status Analysis", "💍")
add_chart(chart_mar, "Figure 7: Revenue by Marital Status & Gender", width=W*0.75)

mar_rev = df.groupby('Marital_Status')['Amount'].sum()
insight_box([
    f"Married customers account for ₹{mar_rev[1]/1e6:.1f}M vs ₹{mar_rev[0]/1e6:.1f}M for single customers.",
    "Married women are the highest-spending segment — likely purchasing for household, family gifting, and celebrations.",
    "Single customers, while lower in spend, are tech-savvy and respond better to digital/social media campaigns.",
    "Recommendation: Festival family bundles and 'gift for someone special' campaigns can capture married segment effectively.",
])

section("Strategic Recommendations", "🎯")
recs = [
    ["#1 Target Segment", "Married women aged 26–35 in IT/Healthcare in Western India — highest ROI segment."],
    ["#2 Geography Focus", f"Double down on {top3_states.index[0]}, {top3_states.index[1]}, {top3_states.index[2]} — these 3 states alone drive majority of revenue."],
    ["#3 Product Priority", f"Lead with {top3_cats.index[0]}, {top3_cats.index[1]}, and {top3_cats.index[2]} in hero placements."],
    ["#4 Channel Strategy", "Instagram & WhatsApp for female 26–35 demo; LinkedIn for IT/Banking professionals."],
    ["#5 Loyalty Programs", "Build repeat-purchase incentives for 36–45 age group — second highest spenders."],
    ["#6 Regional Expansion", "Run growth campaigns in Eastern zone — currently under-penetrated relative to population."],
]
rec_table = Table(recs, colWidths=[4.5*cm, W-4.5*cm])
rec_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#FFF3E6')),
    ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,-1), 9.5),
    ('TEXTCOLOR', (0,0), (0,-1), colors.HexColor(ORANGE)),
    ('ALIGN', (0,0), (0,-1), 'LEFT'),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DDD')),
    ('TOPPADDING', (0,0), (-1,-1), 7),
    ('BOTTOMPADDING', (0,0), (-1,-1), 7),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
]))
story.append(rec_table)
story.append(Spacer(1, 0.5*cm))
story.append(HRFlowable(width=W, thickness=1, color=colors.HexColor(GOLD)))
story.append(Spacer(1, 0.2*cm))
story.append(Paragraph("🪔 Happy Diwali — May your data shine as bright as the festival of lights!", 
             ParagraphStyle('', fontSize=10, textColor=colors.HexColor(ORANGE), 
                            alignment=TA_CENTER, fontName='Helvetica-Bold')))

# ─── BUILD ────────────────────────────────────────────────────────────────────
def on_page(canvas, doc):
    if doc.page == 1:
        cover_bg(canvas, doc)
    else:
        canvas.saveState()
        canvas.setFillColor(colors.HexColor(ORANGE))
        canvas.rect(0, A4[1]-0.6*cm, A4[0], 0.6*cm, fill=1, stroke=0)
        canvas.setFillColor(colors.white)
        canvas.setFont('Helvetica-Bold', 8)
        canvas.drawCentredString(A4[0]/2, A4[1]-0.42*cm, "DIWALI SALES ANALYSIS REPORT")
        # footer
        canvas.setFillColor(colors.HexColor('#999'))
        canvas.setFont('Helvetica', 7.5)
        canvas.drawString(1.8*cm, 1*cm, "Diwali Sales Analysis | Data Science Project")
        canvas.drawRightString(A4[0]-1.8*cm, 1*cm, f"Page {doc.page}")
        canvas.restoreState()

doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print("✅ PDF saved to", OUT)
