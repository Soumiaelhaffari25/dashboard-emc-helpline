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
import streamlit as st

# ==============================================================================
# 1. CONFIGURATION GÉNÉRALE
# ==============================================================================

st.set_page_config(
    page_title="EMC Helpline — Tableau de bord CMRPI",
    page_icon="assets/cmrpi.png" if os.path.exists("assets/cmrpi.png") else "📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Palette EMC Helpline
COULEUR_PRINCIPALE = "#3E6668"
COULEUR_SECONDAIRE = "#97B6D2"
TEXTE = "#1A1A1A"        # noir pour tout le texte

FIG_DIR = "output/figures"

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

        /* Sidebar blanche */
        [data-testid="stSidebar"] {{
            background-color: #FFFFFF;
        }}
        /* Sur DESKTOP uniquement : sidebar toujours visible et large.
           Sur mobile, on laisse Streamlit gérer le repli normal. */
        @media (min-width: 769px) {{
            [data-testid="stSidebar"] {{
                display: flex !important;
                visibility: visible !important;
                transform: none !important;
                min-width: 300px !important;
                width: 300px !important;
            }}
        }}
        /* Bouton d'ouverture/fermeture de la sidebar : bien visible (vert CMRPI) */
        [data-testid="stSidebarCollapsedControl"] {{
            display: block !important;
            visibility: visible !important;
        }}
        [data-testid="stSidebarCollapsedControl"] svg,
        [data-testid="collapsedControl"] svg,
        [data-testid="stSidebarCollapseButton"] svg {{
            color: {COULEUR_PRINCIPALE} !important;
            fill: {COULEUR_PRINCIPALE} !important;
            width: 26px; height: 26px;
        }}

        /* ---- DROPDOWNS (selectbox) : FOND BLANC FORCÉ (bat le thème sombre) ---- */
        [data-testid="stSidebar"] [data-baseweb="select"],
        [data-testid="stSidebar"] [data-baseweb="select"] div,
        [data-testid="stSidebar"] [data-baseweb="select"] [role="button"],
        [data-testid="stSidebar"] [data-baseweb="base-input"],
        [data-testid="stSidebar"] [data-baseweb="input"],
        [data-testid="stSidebar"] [data-baseweb="input"] input {{
            background-color: #FFFFFF !important;
            background: #FFFFFF !important;
            color: {TEXTE} !important;
        }}
        [data-testid="stSidebar"] [data-baseweb="select"] > div:first-child {{
            border: 1px solid #CBD5DC !important;
            border-radius: 8px !important;
        }}
        [data-testid="stSidebar"] [data-baseweb="select"] svg {{
            fill: {TEXTE} !important; color: {TEXTE} !important;
        }}
        /* Liste d'options ouverte */
        div[data-baseweb="popover"],
        div[data-baseweb="popover"] div,
        ul[role="listbox"],
        ul[role="listbox"] li {{
            background-color: #FFFFFF !important;
            background: #FFFFFF !important;
            color: {TEXTE} !important;
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
            /* Réduire les marges latérales pour gagner de la place */
            .block-container {{ padding-left: 0.8rem !important; padding-right: 0.8rem !important; }}
        }}

        /* Rendre le bandeau d'en-tête Streamlit transparent (retire le fond noir)
           tout en gardant les boutons de contrôle de la sidebar accessibles */
        header[data-testid="stHeader"] {{
            background: transparent !important;
            box-shadow: none !important;
            height: 0 !important;
        }}
        [data-testid="stToolbar"] {{ display: none !important; }}
        [data-testid="stDecoration"] {{ display: none !important; }}
        /* Récupérer l'espace laissé par le header supprimé */
        .block-container {{ padding-top: 1.5rem !important; }}
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

with onglet1:
    st.markdown("<p class='section-title'>Évolution mensuelle</p>", unsafe_allow_html=True)
    img("kpi1_volume_mensuel.png")

    g1, g2 = st.columns(2)
    with g1:
        st.markdown("<p class='section-title'>Type de cyberviolence</p>", unsafe_allow_html=True)
        img("kpi2_type_cyberviolence.png")
    with g2:
        st.markdown("<p class='section-title'>Plateformes</p>", unsafe_allow_html=True)
        img("kpi3_plateforme.png")

with onglet2:
    g1, g2 = st.columns(2)
    with g1:
        st.markdown("<p class='section-title'>Genre</p>", unsafe_allow_html=True)
        img("kpi4_genre.png")
    with g2:
        st.markdown("<p class='section-title'>Tranche d'âge</p>", unsafe_allow_html=True)
        img("kpi4_age.png")

    st.markdown("<p class='section-title'>Anonymat et accompagnement</p>", unsafe_allow_html=True)
    img("kpi5_anonymat_accompagnement.png")

with onglet3:
    g1, g2 = st.columns(2)
    with g1:
        st.markdown("<p class='section-title'>Âge × Genre</p>", unsafe_allow_html=True)
        img("kpi6a_age_genre.png")
    with g2:
        st.markdown("<p class='section-title'>Cyberviolence × Genre</p>", unsafe_allow_html=True)
        img("kpi6b_cyberviolence_genre.png")

    g3, g4 = st.columns(2)
    with g3:
        st.markdown("<p class='section-title'>Cyberviolence × Plateforme</p>", unsafe_allow_html=True)
        img("kpi6c_cyberviolence_plateforme.png")
    with g4:
        st.markdown("<p class='section-title'>Plateforme × Genre</p>", unsafe_allow_html=True)
        img("kpi6d_plateforme_genre.png")

    g5, g6 = st.columns(2)
    with g5:
        st.markdown("<p class='section-title'>Anonymat × Genre</p>", unsafe_allow_html=True)
        img("kpi6e_anonymat_genre.png")
    with g6:
        st.markdown("<p class='section-title'>Accompagnement × Cyberviolence</p>", unsafe_allow_html=True)
        img("kpi6f_accompagnement_cyberviolence.png")

# ==============================================================================
# 8. PIED DE PAGE
# ==============================================================================

st.markdown(
    "<div class='footer'>© 2025 CMRPI — EMC Helpline · "
    "Tableau de bord décisionnel et analytique des signalements</div>",
    unsafe_allow_html=True,
)