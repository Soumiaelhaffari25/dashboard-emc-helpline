"""
================================================================================
 TABLEAU DE BORD DÉCISIONNEL ET ANALYTIQUE — EMC HELPLINE
 CMRPI — Centre Marocain de Recherche Polytechnique et d'Innovation
 Jalon 3 — Dashboard Streamlit
================================================================================

Lancement :
    streamlit run app.py

Ce dashboard AFFICHE les figures produites par src/kpi.py (dossier
output/figures/). Exécutez donc d'abord :
    python src/cleaning.py
    python src/kpi.py

Arborescence attendue :
    ├── app.py
    ├── assets/cmrpi.png
    ├── data/processed/signalements_clean.csv
    └── output/figures/kpi*.png
"""

import base64
import os

import pandas as pd
import plotly.express as px
import streamlit as st

# ==============================================================================
# 1. CONFIGURATION GÉNÉRALE
# ==============================================================================

st.set_page_config(
    page_title="EMC Helpline — Tableau de bord CMRPI",
    page_icon="assets/cmrpi.png" if os.path.exists("assets/cmrpi.png") else "📊",
    layout="wide",
    initial_sidebar_state="auto",
)

# Palette EMC Helpline (reprise de src/kpi.py)
COULEUR_PRINCIPALE = "#3E6668"
COULEUR_SECONDAIRE = "#97B6D2"
TEXTE = "#1A1A1A"        # noir pour tout le texte

PALETTE_SEQ = ["#3E6668", "#97B6D2", "#8F7C9A", "#BDA5AE",
               "#F8CEC1", "#8AB097", "#FFE5A5", "#D9D9D9"]
COULEURS_GENRE = {"Féminin": "#C96583", "Masculin": "#5C6594"}
COULEURS_ACC = {"Oui": "#4B994B", "Non": "#CE6262"}
ORDRE_AGE = ["Âges de 13 à 17 ans", "Âges de 18 à 25 ans", "Plus de 26 ans"]

FIG_DIR = "output/figures"


def styliser(fig, hauteur=380):
    """Mise en forme commune des graphiques Plotly."""
    fig.update_layout(
        template="plotly_white", height=hauteur,
        margin=dict(l=10, r=10, t=50, b=10),
        title_font=dict(size=15, color=COULEUR_PRINCIPALE),
        font=dict(size=12, color="#1A1A1A"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig

# ==============================================================================
# 2. STYLE (CSS) — TOUT LE TEXTE EN NOIR, FILTRES SANS ROUGE
# ==============================================================================

st.markdown(
    f"""
    <style>
        /* Forcer les variables de thème Streamlit en CLAIR (pilote le fond des widgets) */
        :root, .stApp {{
            --background-color: #F4F6F8;
            --secondary-background-color: #FFFFFF;
            --text-color: #1A1A1A;
            --primary-color: #3E6668;
            color-scheme: light !important;
        }}

        /* Fond clair + police noire partout */
        .stApp {{ background-color: #F4F6F8; color: {TEXTE}; }}

        /* Forcer le NOIR sur tous les textes (corrige l'illisibilité) */
        .stApp, .stApp p, .stApp span, .stApp label, .stApp div,
        .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp li,
        [data-testid="stSidebar"] * ,
        [data-testid="stMarkdownContainer"] * {{
            color: {TEXTE} !important;
        }}

        /* Sidebar blanche (Streamlit gère l'affichage/repli, y compris sur mobile) */
        [data-testid="stSidebar"] {{
            background-color: #FFFFFF;
        }}

        /* ---- DROPDOWNS (selectbox) : FOND BLANC FORCÉ (bat le thème sombre) ---- */
        /* Approche universelle : tous les conteneurs de widgets dans la sidebar en blanc */
        [data-testid="stSidebar"] [data-baseweb="select"] *,
        [data-testid="stSidebar"] [data-baseweb="select"],
        [data-testid="stSidebar"] [data-baseweb="popover"] *,
        [data-testid="stSidebar"] [data-baseweb="base-input"],
        [data-testid="stSidebar"] [data-baseweb="input"] *,
        [data-testid="stSidebar"] [class*="st-"] [data-baseweb="select"] > div {{
            background-color: #FFFFFF !important;
            background: #FFFFFF !important;
            color: #1A1A1A !important;
        }}
        /* Le conteneur cliquable du selectbox (celui qui est noir) */
        [data-testid="stSidebar"] div[data-baseweb="select"] > div,
        [data-testid="stSidebar"] div[data-baseweb="select"] > div > div {{
            background-color: #FFFFFF !important;
            background: #FFFFFF !important;
            border: 1px solid #CBD5DC !important;
            border-radius: 8px !important;
            color: #1A1A1A !important;
        }}
        [data-testid="stSidebar"] [data-baseweb="select"] svg,
        [data-testid="stSidebar"] [data-baseweb="select"] path {{
            fill: #1A1A1A !important; color: #1A1A1A !important;
        }}
        /* Liste d'options ouverte (popover global, hors sidebar dans le DOM) */
        div[data-baseweb="popover"],
        div[data-baseweb="popover"] *,
        ul[role="listbox"],
        ul[role="listbox"] li {{
            background-color: #FFFFFF !important;
            background: #FFFFFF !important;
            color: #1A1A1A !important;
        }}
        ul[role="listbox"] li:hover {{ background-color: #EAF0F1 !important; }}

        /* ---- FILTRES DRILL-DOWN : neutraliser le rouge des tags multiselect ---- */
        /* Streamlit colore les tags avec sa couleur primaire (rouge). On force le vert CMRPI. */
        span[data-baseweb="tag"],
        [data-testid="stSidebar"] span[data-baseweb="tag"],
        div[data-baseweb="select"] span[data-baseweb="tag"] {{
            background-color: {COULEUR_PRINCIPALE} !important;
            border-color: {COULEUR_PRINCIPALE} !important;
        }}
        span[data-baseweb="tag"] *,
        span[data-baseweb="tag"] span,
        span[data-baseweb="tag"] svg {{
            color: #FFFFFF !important;
            fill: #FFFFFF !important;
        }}
        /* Expander (drill-down) : en-tête lisible */
        [data-testid="stSidebar"] [data-testid="stExpander"] summary {{
            font-weight: 600;
            color: {TEXTE} !important;
        }}

        /* Bandeau d'en-tête : fond BLANC, texte foncé, filet vert CMRPI */
        .header-band {{
            background: #FFFFFF;
            padding: 22px 32px; border-radius: 14px; margin-bottom: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.06);
            border-left: 6px solid {COULEUR_PRINCIPALE};
        }}
        .header-title {{ font-size: 30px; font-weight: 800; margin: 0; line-height: 1.15;
                         color: {COULEUR_PRINCIPALE} !important; }}
        .header-sub {{ font-size: 15px; margin-top: 4px; color: #444 !important; }}

        /* Cartes KPI */
        .kpi-card {{
            background: #FFFFFF; border-radius: 14px; padding: 16px 16px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.06);
            border-left: 6px solid {COULEUR_PRINCIPALE}; height: 100%;
        }}
        .kpi-value {{ font-size: 30px; font-weight: 800; color: {COULEUR_PRINCIPALE} !important; margin: 0; }}
        .kpi-label {{ font-size: 11px; color: #333 !important; margin: 4px 0 0 0;
                      text-transform: uppercase; letter-spacing: 0.3px;
                      line-height: 1.3; word-break: normal; overflow-wrap: normal;
                      hyphens: none; white-space: normal; }}

        .section-title {{
            color: {COULEUR_PRINCIPALE} !important; font-size: 20px; font-weight: 700;
            border-bottom: 3px solid {COULEUR_SECONDAIRE}; padding-bottom: 6px;
            margin: 12px 0 8px 0;
        }}
        .footer {{ text-align: center; color: #555 !important; font-size: 12.5px; padding: 18px 0 4px 0; }}
        #MainMenu, footer {{ visibility: hidden; }}

        /* ============ RESPONSIVE MOBILE (écrans étroits) ============ */
        @media (max-width: 768px) {{
            .header-band {{ padding: 14px 16px !important; }}
            .header-title {{ font-size: 20px !important; line-height: 1.2 !important; }}
            .header-sub {{ font-size: 12px !important; }}
            .kpi-value {{ font-size: 26px !important; }}
            .kpi-label {{ font-size: 11px !important; }}
            .section-title {{ font-size: 17px !important; }}
            /* Les colonnes Streamlit s'empilent verticalement sur mobile */
            [data-testid="stHorizontalBlock"] {{ flex-direction: column !important; }}
            [data-testid="column"] {{ width: 100% !important; flex: 1 1 100% !important; }}
            .block-container {{ padding-left: 0.8rem !important; padding-right: 0.8rem !important; }}
        }}

        /* Masquer seulement la barre d'outils "Deploy" et le liseré coloré.
           On NE touche PAS au header ni au bouton d'ouverture de la sidebar,
           pour que les filtres restent accessibles sur mobile. */
        [data-testid="stToolbar"] {{ display: none !important; }}
        [data-testid="stDecoration"] {{ display: none !important; }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ==============================================================================
# 3. DONNÉES (pour les cartes KPI uniquement — les graphiques sont des PNG)
# ==============================================================================


@st.cache_data(show_spinner=False)
def charger_donnees():
    for p in ("data/processed/signalements_clean.csv",):
        if os.path.exists(p):
            df = pd.read_csv(p)
            df["date"] = pd.to_datetime(df["date"], errors="coerce")
            return df
    return None


@st.cache_data(show_spinner=False)
def logo_base64():
    for p in ("assets/cmrpi.png", "cmrpi.png"):
        if os.path.exists(p):
            with open(p, "rb") as f:
                return base64.b64encode(f.read()).decode()
    return None


def img(nom):
    """Affiche une figure PNG produite par kpi.py, si présente."""
    chemin = os.path.join(FIG_DIR, nom)
    if os.path.exists(chemin):
        st.image(chemin, use_container_width=True)
    else:
        st.warning(f"Figure manquante : {chemin} — exécutez `python src/kpi.py`.")


df = charger_donnees()
logo = logo_base64()

# ==============================================================================
# 4. BARRE LATÉRALE — LOGO + FILTRES EN DRILL-DOWN
# ==============================================================================

with st.sidebar:
    if logo:
        st.markdown(
            f"<div style='text-align:center;padding:6px 0 14px 0;'>"
            f"<img src='data:image/png;base64,{logo}' width='190'></div>",
            unsafe_allow_html=True,
        )
    st.markdown("### Filtres")

    sel_langue, sel_plateforme, sel_genre = "Toutes", "Toutes", "Tous"
    if df is not None:
        langues = ["Toutes"] + sorted(df["langue"].dropna().unique().tolist())
        plateformes = ["Toutes"] + sorted(df["plateforme"].dropna().unique().tolist())
        genres = ["Tous"] + sorted(df["genre"].dropna().unique().tolist())

        sel_langue = st.selectbox("Langue", langues, index=0)
        sel_plateforme = st.selectbox("Plateforme", plateformes, index=0)
        sel_genre = st.selectbox("Genre", genres, index=0)

    st.markdown("---")
    st.caption("**CMRPI — EMC Helpline** · 2025")

# Application des filtres (pour les cartes KPI)
if df is not None:
    dff = df.copy()
    if sel_langue != "Toutes":
        dff = dff[dff["langue"] == sel_langue]
    if sel_plateforme != "Toutes":
        dff = dff[dff["plateforme"] == sel_plateforme]
    if sel_genre != "Tous":
        dff = dff[dff["genre"] == sel_genre]
else:
    dff = None

# ==============================================================================
# 5. EN-TÊTE
# ==============================================================================

col_logo, col_titre = st.columns([1, 6])
with col_logo:
    if logo:
        st.markdown(
            f"<img src='data:image/png;base64,{logo}' width='150' style='margin-top:10px;'>",
            unsafe_allow_html=True,
        )
with col_titre:
    st.markdown(
        """
        <div class="header-band">
            <p class="header-title">Tableau de bord des signalements — EMC Helpline</p>
            <p class="header-sub">Analyse décisionnelle de la cyberviolence · Année 2025 · CMRPI</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ==============================================================================
# 6. CARTES D'INDICATEURS CLÉS
# ==============================================================================


def carte(col, valeur, label):
    col.markdown(
        f"<div class='kpi-card'><p class='kpi-value'>{valeur}</p>"
        f"<p class='kpi-label'>{label}</p></div>",
        unsafe_allow_html=True,
    )


if dff is not None:
    total = len(dff)

    # Un seul indicateur, centré
    _g, c1, _d = st.columns([2, 2, 2])
    c1.markdown(
        f"<div class='kpi-card' style='text-align:center;border-left:none;"
        f"border-top:6px solid #3E6668;'>"
        f"<p class='kpi-value'>{total}</p>"
        f"<p class='kpi-label'>Signalements</p></div>",
        unsafe_allow_html=True,
    )
else:
    st.info(
        "CSV nettoyé introuvable — l'indicateur est masqué. "
        "Exécutez `python src/cleaning.py`. Les graphiques restent affichés."
    )

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# 7. ONGLETS — GRAPHIQUES = FIGURES PNG DE kpi.py
# ==============================================================================

onglet1, onglet2, onglet3 = st.tabs(
    ["Vue d'ensemble", "Profil des victimes", "Analyses croisées"]
)

# Les figures reproduisent celles de src/kpi.py (mêmes couleurs, titres, formats)
# mais sont calculées sur d = données FILTRÉES → elles changent avec les filtres.
d = dff if dff is not None else pd.DataFrame()

C_GENRE = {"Féminin": "#C96583", "Masculin": "#5C6594"}
C_ACC = {"Non": "#CE6262", "Oui": "#4B994B"}
SEQ8 = ["#3E6668", "#97B6D2", "#8F7C9A", "#BDA5AE", "#F8CEC1", "#8AB097", "#FFE5A5", "#D9D9D9"]
ORDRE_AGE = ["Âges de 13 à 17 ans", "Âges de 18 à 25 ans", "Plus de 26 ans"]


def montrer(fig):
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font=dict(color="#1A1A1A"), title_font=dict(color=COULEUR_PRINCIPALE),
                      margin=dict(l=10, r=10, t=50, b=10))
    st.plotly_chart(fig, use_container_width=True)


with onglet1:
    st.markdown("<p class='section-title'>Évolution mensuelle</p>", unsafe_allow_html=True)
    if not d.empty and d["date"].notna().any():
        dm = d.dropna(subset=["date"]).copy()
        dm["mois"] = dm["date"].dt.to_period("M")
        mois_complets = pd.period_range("2025-01", "2025-12", freq="M")
        kpi1 = dm.groupby("mois").size().reindex(mois_complets, fill_value=0).reset_index()
        kpi1.columns = ["mois", "nombre_signalements"]
        kpi1["mois"] = kpi1["mois"].astype(str)
        fig1 = px.bar(kpi1, x="mois", y="nombre_signalements",
                      title="Volume mensuel des signalements EMC Helpline — 2025",
                      labels={"mois": "Mois", "nombre_signalements": "Nombre de signalements"},
                      text="nombre_signalements", color_discrete_sequence=[COULEUR_PRINCIPALE])
        fig1.update_traces(textposition="outside")
        fig1.update_layout(xaxis_tickangle=-45)
        montrer(fig1)
    else:
        st.info("Aucune donnée pour ce filtre.")

    g1, g2 = st.columns(2)
    with g1:
        st.markdown("<p class='section-title'>Type de cyberviolence</p>", unsafe_allow_html=True)
        if not d.empty:
            kpi2 = d["cyberharcelementType"].value_counts().reset_index()
            kpi2.columns = ["type_cyberviolence", "nombre_signalements"]
            kpi2["pourcentage"] = kpi2["nombre_signalements"] / kpi2["nombre_signalements"].sum() * 100
            fig2 = px.bar(kpi2, x="type_cyberviolence", y="pourcentage",
                          title="Répartition par type de cyberviolence — 2025",
                          labels={"type_cyberviolence": "Type de cyberviolence",
                                  "pourcentage": "Part des signalements (%)"},
                          text="pourcentage", color_discrete_sequence=SEQ8)
            fig2.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
            fig2.update_layout(xaxis_tickangle=-45)
            montrer(fig2)
    with g2:
        st.markdown("<p class='section-title'>Plateformes</p>", unsafe_allow_html=True)
        if not d.empty:
            kpi3 = d["plateforme"].value_counts().reset_index()
            kpi3.columns = ["plateforme", "nombre_signalements"]
            kpi3["pourcentage"] = kpi3["nombre_signalements"] / kpi3["nombre_signalements"].sum() * 100
            fig3 = px.bar(kpi3, x="plateforme", y="pourcentage",
                          title="Répartition par plateforme — 2025",
                          labels={"plateforme": "Plateforme",
                                  "pourcentage": "Part des signalements (%)"},
                          text="pourcentage",
                          color_discrete_sequence=["#3E6668", "#97B6D2", "#8F7C9A", "#BDA5AE"])
            fig3.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
            montrer(fig3)

with onglet2:
    g1, g2 = st.columns(2)
    with g1:
        st.markdown("<p class='section-title'>Genre</p>", unsafe_allow_html=True)
        if not d.empty and d["genre"].notna().any():
            k = d["genre"].dropna().value_counts().reset_index()
            k.columns = ["genre", "nombre_signalements"]
            k["pourcentage"] = k["nombre_signalements"] / k["nombre_signalements"].sum() * 100
            fig = px.bar(k, x="genre", y="pourcentage",
                         title="Répartition par genre — 2025",
                         labels={"genre": "Genre", "pourcentage": "Part des signalements (%)"},
                         text="pourcentage", color="genre", color_discrete_map=C_GENRE)
            fig.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
            montrer(fig)
    with g2:
        st.markdown("<p class='section-title'>Tranche d'âge</p>", unsafe_allow_html=True)
        if not d.empty and d["age"].notna().any():
            k = d["age"].dropna().value_counts().reset_index()
            k.columns = ["tranche_age", "nombre_signalements"]
            k["pourcentage"] = k["nombre_signalements"] / k["nombre_signalements"].sum() * 100
            fig = px.bar(k, x="tranche_age", y="pourcentage",
                         title="Répartition par tranche d'âge — 2025",
                         labels={"tranche_age": "Tranche d'âge",
                                 "pourcentage": "Part des signalements (%)"},
                         text="pourcentage", color="tranche_age",
                         color_discrete_sequence=["#558F91", "#9A70B1", "#CA85A0"])
            fig.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
            fig.update_layout(xaxis_tickangle=-25)
            montrer(fig)

    st.markdown("<p class='section-title'>Anonymat et accompagnement</p>", unsafe_allow_html=True)
    if not d.empty:
        total_s = len(d)
        taux_anonymat = d["anonymat"].eq("Oui").sum() / total_s * 100 if total_s else 0
        taux_accompagnement = d["accompagnement"].eq("Oui").sum() / total_s * 100 if total_s else 0
        kpi5 = pd.DataFrame({"indicateur": ["Signalements anonymes", "Demandes d'accompagnement"],
                             "pourcentage": [taux_anonymat, taux_accompagnement]})
        fig5 = px.bar(kpi5, x="indicateur", y="pourcentage",
                      title="Taux d'anonymat et de demande d'accompagnement — 2025",
                      labels={"indicateur": "Indicateur", "pourcentage": "Taux (%)"},
                      text="pourcentage", color="indicateur",
                      color_discrete_sequence=["#558F91", "#9A70B1"])
        fig5.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
        fig5.update_layout(yaxis_range=[0, 100])
        montrer(fig5)

with onglet3:
    def croise(data, lig, col, titre, cmap, ordre_lig=None, angle=0, yr=None):
        dd = data.dropna(subset=[lig, col])
        if dd.empty:
            st.info("Aucune donnée pour ce filtre.")
            return
        t = pd.crosstab(dd[lig], dd[col])
        tp = t.div(t.sum(axis=1), axis=0) * 100
        gr = tp.reset_index().melt(id_vars=lig, var_name=col, value_name="pourcentage")
        if ordre_lig:
            gr[lig] = pd.Categorical(gr[lig], categories=ordre_lig, ordered=True)
            gr = gr.sort_values(lig)
        fig = px.bar(gr, x=lig, y="pourcentage", color=col, barmode="group",
                     title=titre, text="pourcentage",
                     labels={lig: lig, "pourcentage": "Pourcentage (%)", col: col},
                     color_discrete_map=cmap)
        fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        if angle:
            fig.update_layout(xaxis_tickangle=angle)
        if yr:
            fig.update_layout(yaxis_range=yr)
        montrer(fig)

    g1, g2 = st.columns(2)
    with g1:
        st.markdown("<p class='section-title'>Âge × Genre</p>", unsafe_allow_html=True)
        if not d.empty:
            croise(d, "age", "genre", "Répartition du genre selon la tranche d'âge — 2025",
                   C_GENRE, ordre_lig=ORDRE_AGE, yr=[0, 110])
    with g2:
        st.markdown("<p class='section-title'>Cyberviolence × Genre</p>", unsafe_allow_html=True)
        if not d.empty:
            croise(d, "cyberharcelementType", "genre",
                   "Répartition du genre selon le type de cyberviolence", C_GENRE, angle=-45)

    g3, g4 = st.columns(2)
    with g3:
        st.markdown("<p class='section-title'>Plateforme × Genre</p>", unsafe_allow_html=True)
        if not d.empty:
            croise(d, "plateforme", "genre",
                   "Répartition du genre selon la plateforme", C_GENRE)
    with g4:
        st.markdown("<p class='section-title'>Anonymat × Genre</p>", unsafe_allow_html=True)
        if not d.empty:
            croise(d, "anonymat", "genre",
                   "Répartition du genre selon l'anonymat", C_GENRE)

    g5, g6 = st.columns(2)
    with g5:
        st.markdown("<p class='section-title'>Accompagnement × Cyberviolence</p>", unsafe_allow_html=True)
        if not d.empty:
            croise(d, "cyberharcelementType", "accompagnement",
                   "Demande d'accompagnement selon le type de cyberviolence",
                   C_ACC, angle=-45)

# ==============================================================================
# 8. PIED DE PAGE
# ==============================================================================

st.markdown(
    "<div class='footer'>© 2025 CMRPI — EMC Helpline · "
    "Tableau de bord décisionnel et analytique des signalements </div>",
    unsafe_allow_html=True,
)