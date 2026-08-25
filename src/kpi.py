import pandas as pd
import plotly.express as px
from scipy.stats import chi2_contingency, fisher_exact
import numpy as np
import os

os.makedirs("output/figures", exist_ok=True)


# PALETTE DE COULEURS — EMC HELPLINE

COULEUR_PRINCIPALE = "#3E6668"
COULEUR_SECONDAIRE = "#97B6D2"
COULEUR_ACCENT = "#8F7C9A"
COULEUR_ROSE = "#BDA5AE"
COULEUR_PEACH = "#F8CEC1"
COULEUR_VERT = "#8AB097"
COULEUR_JAUNE = "#FFE5A5"
COULEUR_GRIS = "#D9D9D9"

COULEURS_GENRE = {
    "Féminin": COULEUR_ACCENT,
    "Masculin": COULEUR_PRINCIPALE
}

COULEURS_OUI_NON = {
    "Oui": COULEUR_PRINCIPALE,
    "Non": COULEUR_GRIS
}


# CHARGEMENT DES DONNÉES NETTOYÉES


df = pd.read_csv(
    "data/processed/signalements_clean.csv"
)

# Reconvertir la colonne date
df["date"] = pd.to_datetime(df["date"])


# KPI 1 — VOLUME MENSUEL DES SIGNALEMENTS

# Extraire le mois
df["mois"] = df["date"].dt.to_period("M")

# Créer les 12 mois de l'année 2025
mois_complets = pd.period_range(
    start="2025-01",
    end="2025-12",
    freq="M"
)

# Compter les signalements par mois
kpi1 = (
    df.groupby("mois")
      .size()
      .reindex(mois_complets, fill_value=0)
      .reset_index()
)

kpi1.columns = [
    "mois",
    "nombre_signalements"
]

# Affichage du résultat
print("\n===== KPI 1 — VOLUME MENSUEL =====")
print(kpi1)

print(
    "\nTotal :",
    kpi1["nombre_signalements"].sum()
)


# GRAPHIQUE KPI 1 — VOLUME MENSUEL

# Conversion en texte pour Plotly
kpi1["mois"] = kpi1["mois"].astype(str)

fig1 = px.bar(
    kpi1,
    x="mois",
    y="nombre_signalements",
    title="Volume mensuel des signalements EMC Helpline — 2025",
    labels={
        "mois": "Mois",
        "nombre_signalements": "Nombre de signalements"
    },
    text="nombre_signalements",
    color_discrete_sequence=[COULEUR_PRINCIPALE]
)

fig1.update_traces(
    textposition="outside"
)

fig1.update_layout(
    xaxis_tickangle=-45
)

fig1.show()
fig1.write_image("output/figures/kpi1_volume_mensuel.png")


# KPI 2 — RÉPARTITION PAR TYPE DE CYBERVIOLENCE

# Compter les signalements par type
kpi2 = (
    df["cyberharcelementType"]
    .value_counts()
    .reset_index()
)

# Renommer les colonnes
kpi2.columns = [
    "type_cyberviolence",
    "nombre_signalements"
]

# Calculer le pourcentage
kpi2["pourcentage"] = (
    kpi2["nombre_signalements"]
    / kpi2["nombre_signalements"].sum()
    * 100
)


# Affichage du résultat
print("\n===== KPI 2 — TYPE DE CYBERVIOLENCE =====")
print(kpi2)

print(
    "\nTotal des signalements :",
    kpi2["nombre_signalements"].sum()
)

print(
    "Total des pourcentages :",
    kpi2["pourcentage"].sum()
)


# GRAPHIQUE KPI 2 — TYPE DE CYBERVIOLENCE

fig2 = px.bar(
    kpi2,
    x="type_cyberviolence",
    y="pourcentage",
    title="Répartition des signalements par type de cyberviolence — 2025",
    labels={
        "type_cyberviolence": "Type de cyberviolence",
        "pourcentage": "Part des signalements (%)"
    },
    text="pourcentage",
    color_discrete_sequence=[
        COULEUR_PRINCIPALE,
        COULEUR_SECONDAIRE,
        COULEUR_ACCENT,
        COULEUR_ROSE,
        COULEUR_PEACH,
        COULEUR_VERT,
        COULEUR_JAUNE,
        COULEUR_GRIS
    ]
)

fig2.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig2.update_layout(
    xaxis_tickangle=-45
)

fig2.show()
fig2.write_image("output/figures/kpi2_type_cyberviolence.png")


# KPI 3 — RÉPARTITION PAR PLATEFORME

kpi3 = (
    df["plateforme"]
    .value_counts()
    .reset_index()
)

kpi3.columns = [
    "plateforme",
    "nombre_signalements"
]

# Calcul du pourcentage
kpi3["pourcentage"] = (
    kpi3["nombre_signalements"]
    / kpi3["nombre_signalements"].sum()
    * 100
)

print("\n===== KPI 3 — PLATEFORME =====")
print(kpi3)

print(
    "\nTotal des signalements :",
    kpi3["nombre_signalements"].sum()
)

print(
    "Total des pourcentages :",
    kpi3["pourcentage"].sum()
)


# GRAPHIQUE KPI 3 — PLATEFORME

fig3 = px.bar(
    kpi3,
    x="plateforme",
    y="pourcentage",
    title="Répartition des signalements par plateforme — 2025",
    labels={
        "plateforme": "Plateforme",
        "pourcentage": "Part des signalements (%)"
    },
    text="pourcentage",
    color_discrete_sequence=[
        COULEUR_PRINCIPALE,
        COULEUR_SECONDAIRE,
        COULEUR_ACCENT,
        COULEUR_ROSE
    ]
)

fig3.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig3.show()
fig3.write_image("output/figures/kpi3_plateforme.png")
# KPI 4 — RÉPARTITION PAR GENRE

kpi4_genre = (
    df["genre"]
    .dropna()
    .value_counts()
    .reset_index()
)

kpi4_genre.columns = [
    "genre",
    "nombre_signalements"
]

# Calcul du pourcentage sur les valeurs renseignées
kpi4_genre["pourcentage"] = (
    kpi4_genre["nombre_signalements"]
    / kpi4_genre["nombre_signalements"].sum()
    * 100
)

print("\n===== KPI 4 — GENRE =====")
print(kpi4_genre)

print(
    "\nTotal des genres renseignés :",
    kpi4_genre["nombre_signalements"].sum()
)

print(
    "Total des pourcentages :",
    kpi4_genre["pourcentage"].sum()
)


# KPI 4 — RÉPARTITION PAR TRANCHE D'ÂGE
kpi4_age = (
    df["age"]
    .dropna()
    .value_counts()
    .reset_index()
)

kpi4_age.columns = [
    "tranche_age",
    "nombre_signalements"
]

# Calcul du pourcentage sur les âges renseignés
kpi4_age["pourcentage"] = (
    kpi4_age["nombre_signalements"]
    / kpi4_age["nombre_signalements"].sum()
    * 100
)

print("\n===== KPI 4 — ÂGE =====")
print(kpi4_age)

print(
    "\nTotal des âges renseignés :",
    kpi4_age["nombre_signalements"].sum()
)

print(
    "Total des pourcentages :",
    kpi4_age["pourcentage"].sum()
)


# GRAPHIQUE KPI 4 — GENRE

fig4_genre = px.bar(
    kpi4_genre,
    x="genre",
    y="pourcentage",
    title="Répartition des signalements par genre — 2025",
    labels={
        "genre": "Genre",
        "pourcentage": "Part des signalements (%)"
    },
    text="pourcentage",
    color="genre",
    color_discrete_map={
        "Féminin": "#C96583",
        "Masculin": "#5C6594"
    }
)

fig4_genre.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig4_genre.show()
fig4_genre.write_image("output/figures/kpi4_genre.png")

# GRAPHIQUE KPI 4 — TRANCHE D'ÂGE

fig4_age = px.bar(
    kpi4_age,
    x="tranche_age",
    y="pourcentage",
    title="Répartition des signalements par tranche d'âge — 2025",
    labels={
        "tranche_age": "Tranche d'âge",
        "pourcentage": "Part des signalements (%)"
    },
    text="pourcentage",
    color="tranche_age",
    color_discrete_sequence=[
        "#558F91",  
        "#9A70B1",  
        "#CA85A0" 
    ]
)

fig4_age.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig4_age.update_layout(
    xaxis_tickangle=-25
)

fig4_age.show()
fig4_age.write_image("output/figures/kpi4_age.png")

# KPI 5 — TAUX D'ANONYMAT ET D'ACCOMPAGNEMENT

# Taux d'anonymat

nombre_anonymes = (
    df["anonymat"]
    .eq("Oui")
    .sum()
)

total_signalements = len(df)

taux_anonymat = (
    nombre_anonymes
    / total_signalements
    * 100
)


# Taux de demande d'accompagnement

nombre_accompagnement = (
    df["accompagnement"]
    .eq("Oui")
    .sum()
)

taux_accompagnement = (
    nombre_accompagnement
    / total_signalements
    * 100
)


# Affichage

print("\n===== KPI 5 — ANONYMAT / ACCOMPAGNEMENT =====")

print(
    "Signalements anonymes :",
    nombre_anonymes
)

print(
    "Taux d'anonymat :",
    round(taux_anonymat, 2),
    "%"
)

print(
    "Demandes d'accompagnement :",
    nombre_accompagnement
)

print(
    "Taux de demande d'accompagnement :",
    round(taux_accompagnement, 2),
    "%"
)

print(
    "Total des signalements :",
    total_signalements
)


# GRAPHIQUE KPI 5 — ANONYMAT / ACCOMPAGNEMENT

kpi5 = pd.DataFrame({
    "indicateur": [
        "Signalements anonymes",
        "Demandes d'accompagnement"
    ],
    "pourcentage": [
        taux_anonymat,
        taux_accompagnement
    ]
})

fig5 = px.bar(
    kpi5,
    x="indicateur",
    y="pourcentage",
    title="Taux d'anonymat et de demande d'accompagnement — 2025",
    labels={
        "indicateur": "Indicateur",
        "pourcentage": "Taux (%)"
    },
    text="pourcentage",
    color="indicateur",
    color_discrete_sequence=[
        "#558F91",  
        "#9A70B1"   
    ]
)

fig5.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig5.update_layout(
    yaxis_range=[0, 100]
)

fig5.show()
fig5.write_image("output/figures/kpi5_anonymat_accompagnement.png")
# KPI 6a — ÂGE × GENRE

# Garder uniquement les lignes où âge ET genre sont renseignés
df_6a = df.dropna(
    subset=["age", "genre"]
).copy()


# Tableau de contingence — effectifs

table_6a = pd.crosstab(
    df_6a["age"],
    df_6a["genre"]
)

print("\n===== KPI 6a — ÂGE × GENRE =====")

print("\nTableau de contingence — Effectifs :")
print(table_6a)

print(
    "\nTotal des observations utilisées :",
    table_6a.values.sum()
)


# Pourcentages en ligne

table_6a_pct = (
    table_6a
    .div(table_6a.sum(axis=1), axis=0)
    * 100
)

print("\nPourcentages en ligne :")
print(
    table_6a_pct.round(2)
)


# Vérification

print("\nTotaux des lignes :")
print(
    table_6a.sum(axis=1)
)

print("\nTotaux des pourcentages par ligne :")
print(
    table_6a_pct.sum(axis=1).round(2)
)

# KPI 6a — VÉRIFICATION DES CONDITIONS DU CHI-DEUX

# Calcul du test du chi-deux
chi2, p_value, ddl, expected = chi2_contingency(
    table_6a
)

# Transformer les effectifs théoriques en DataFrame
table_6a_expected = pd.DataFrame(
    expected,
    index=table_6a.index,
    columns=table_6a.columns
)

print("\n===== EFFECTIFS THÉORIQUES =====")
print(
    table_6a_expected.round(2)
)

# Vérification de la condition
nombre_cases = expected.size

nombre_cases_ge_5 = (
    expected >= 5
).sum()

pourcentage_cases_ge_5 = (
    nombre_cases_ge_5
    / nombre_cases
    * 100
)

print("\n===== CONDITION DU CHI-DEUX =====")

print(
    "Nombre total de cases :",
    nombre_cases
)

print(
    "Cases avec effectif théorique >= 5 :",
    nombre_cases_ge_5
)

print(
    "Pourcentage de cases >= 5 :",
    round(pourcentage_cases_ge_5, 2),
    "%"
)

# RÉSULTAT DU CHI-DEUX — À INTERPRÉTER AVEC PRUDENCE

print("\n===== TEST DU CHI-DEUX — 6a =====")

print(
    "Statistique χ² :",
    round(chi2, 4)
)

print(
    "Degrés de liberté :",
    ddl
)

print(
    "p-value :",
    round(p_value, 4)
)

if pourcentage_cases_ge_5 >= 80:

    if p_value < 0.05:
        print(
            "Conclusion : association statistiquement significative."
        )
    else:
        print(
            "Conclusion : aucune association statistiquement "
            "significative détectée."
        )

else:

    print(
        "⚠ Le χ² n'est pas retenu pour une interprétation "
        "statistique fiable."
    )

    print(
        "Motif : moins de 80 % des cases ont un effectif "
        "théorique >= 5."
    )

    print(
        "→ Interprétation descriptive uniquement."
    )
    

# GRAPHIQUE KPI 6a — ÂGE × GENRE

# Ordre logique des tranches d'âge
ordre_age = [
    "Âges de 13 à 17 ans",
    "Âges de 18 à 25 ans",
    "Plus de 26 ans"
]

graph_6a = (
    table_6a_pct
    .reset_index()
    .melt(
        id_vars="age",
        var_name="genre",
        value_name="pourcentage"
    )
)

# Imposer l'ordre des tranches d'âge
graph_6a["age"] = pd.Categorical(
    graph_6a["age"],
    categories=ordre_age,
    ordered=True
)

graph_6a = graph_6a.sort_values("age")

print("\n===== DONNÉES DU GRAPHIQUE 6a =====")
print(graph_6a.round(2))


fig6a = px.bar(
    graph_6a,
    x="age",
    y="pourcentage",
    color="genre",
    barmode="group",
    title="Répartition du genre selon la tranche d'âge — 2025",
    labels={
        "age": "Tranche d'âge",
        "pourcentage": "Pourcentage (%)",
        "genre": "Genre"
    },
    text="pourcentage",
    color_discrete_map={
        "Féminin": "#C96583",
        "Masculin": "#5C6594"
    }
)

fig6a.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig6a.update_layout(
    yaxis_title="Pourcentage (%)",
    xaxis_title="Tranche d'âge",
    yaxis_range=[0, 110]
)

fig6a.show()
fig6a.write_image("output/figures/kpi6a_age_genre.png")
# KPI 6b — TYPE DE CYBERVIOLENCE × GENRE

# Garder uniquement les lignes où le type de cyberviolence
# et le genre sont renseignés
df_6b = df.dropna(
    subset=["cyberharcelementType", "genre"]
).copy()


# Tableau de contingence — effectifs

table_6b = pd.crosstab(
    df_6b["cyberharcelementType"],
    df_6b["genre"]
)

print("\n===== KPI 6b — TYPE DE CYBERVIOLENCE × GENRE =====")

print("\nTableau de contingence — Effectifs :")
print(table_6b)

print(
    "\nTotal des observations utilisées :",
    table_6b.values.sum()
)


# Pourcentages en ligne

table_6b_pct = (
    table_6b
    .div(table_6b.sum(axis=1), axis=0)
    * 100
)

print("\nPourcentages en ligne :")
print(
    table_6b_pct.round(2)
)

# Vérification des totaux

print("\nTotaux des lignes :")
print(
    table_6b.sum(axis=1)
)

print("\nTotaux des pourcentages par ligne :")
print(
    table_6b_pct.sum(axis=1).round(2)
)

# KPI 6b — VÉRIFICATION DES CONDITIONS DU CHI-DEUX

# Calcul des effectifs théoriques
chi2_6b, p_value_6b, ddl_6b, expected_6b = chi2_contingency(
    table_6b
)

# Transformer les effectifs théoriques en DataFrame
table_6b_expected = pd.DataFrame(
    expected_6b,
    index=table_6b.index,
    columns=table_6b.columns
)

print("\n===== EFFECTIFS THÉORIQUES — 6b =====")

print(
    table_6b_expected.round(2)
)


# Vérification de la condition du χ²

nombre_cases_6b = expected_6b.size

nombre_cases_ge_5_6b = (
    expected_6b >= 5
).sum()

pourcentage_cases_ge_5_6b = (
    nombre_cases_ge_5_6b
    / nombre_cases_6b
    * 100
)

print("\n===== CONDITION DU CHI-DEUX — 6b =====")

print(
    "Nombre total de cases :",
    nombre_cases_6b
)

print(
    "Cases avec effectif théorique >= 5 :",
    nombre_cases_ge_5_6b
)

print(
    "Pourcentage de cases >= 5 :",
    round(pourcentage_cases_ge_5_6b, 2),
    "%"
)

# KPI 6b — REGROUPEMENT DES CATÉGORIES RARES
# TYPE DE CYBERVIOLENCE × GENRE

print("\n===== KPI 6b — REGROUPEMENT DES CATÉGORIES RARES =====")

# Copie des données utilisées pour le croisement
df_6b = df[['cyberharcelementType', 'genre']].dropna().copy()

# Regroupement des catégories très rares
categories_rares = [
    "Escroquerie",
    "Usurpation d’identité",
    "Propos raciste ou discriminatoire"
]

df_6b["type_cyberviolence_regroupe"] = df_6b[
    "cyberharcelementType"
].replace(
    categories_rares,
    "Autres"
)

# Tableau de contingence après regroupement
table_6b_regroupe = pd.crosstab(
    df_6b["type_cyberviolence_regroupe"],
    df_6b["genre"]
)

print("\nTableau de contingence après regroupement :")
print(table_6b_regroupe)

# EFFECTIFS THÉORIQUES

chi2_6b, p_value_6b, ddl_6b, effectifs_theoriques_6b = chi2_contingency(
    table_6b_regroupe
)

effectifs_theoriques_df_6b = pd.DataFrame(
    effectifs_theoriques_6b,
    index=table_6b_regroupe.index,
    columns=table_6b_regroupe.columns
)

print("\n===== EFFECTIFS THÉORIQUES — 6b APRÈS REGROUPEMENT =====")
print(effectifs_theoriques_df_6b.round(2))

# VÉRIFICATION DE LA CONDITION DU CHI-DEUX

total_cases_6b = effectifs_theoriques_df_6b.size

cases_ge_5_6b = (
    effectifs_theoriques_df_6b >= 5
).sum().sum()

pourcentage_cases_6b = (
    cases_ge_5_6b / total_cases_6b
) * 100

print("\n===== CONDITION DU CHI-DEUX — 6b APRÈS REGROUPEMENT =====")
print(f"Nombre total de cases : {total_cases_6b}")
print(f"Cases avec effectif théorique >= 5 : {cases_ge_5_6b}")
print(f"Pourcentage de cases >= 5 : {pourcentage_cases_6b:.2f} %")

# TEST DU CHI-DEUX SI LA CONDITION EST RESPECTÉE

if pourcentage_cases_6b >= 80:

    print("\n===== TEST DU CHI-DEUX — 6b APRÈS REGROUPEMENT =====")

    print(f"Statistique χ² : {chi2_6b:.4f}")
    print(f"Degrés de liberté : {ddl_6b}")
    print(f"p-value : {p_value_6b:.4f}")

    if p_value_6b < 0.05:
        print("✓ Association statistiquement significative entre")
        print("  le type de cyberviolence et le genre.")
    else:
        print("✓ Aucune association statistiquement significative")
        print("  entre le type de cyberviolence et le genre.")

    # V DE CRAMÉR

    n_6b = table_6b_regroupe.to_numpy().sum()

    nombre_lignes = table_6b_regroupe.shape[0]
    nombre_colonnes = table_6b_regroupe.shape[1]

    min_dimension = min(
        nombre_lignes - 1,
        nombre_colonnes - 1
    )

    v_cramer_6b = np.sqrt(
        chi2_6b / (n_6b * min_dimension)
    )

    print(f"V de Cramér : {v_cramer_6b:.4f}")

else:

    print("\n⚠ Le χ² n'est toujours pas retenu.")
    print("Motif : moins de 80 % des cases ont un effectif théorique >= 5.")
    print("→ Interprétation descriptive uniquement.")
    

# GRAPHIQUE KPI 6b — TYPE DE CYBERVIOLENCE × GENRE

# Calcul des pourcentages en ligne après regroupement

table_6b_regroupe_pct = (
    table_6b_regroupe
    .div(table_6b_regroupe.sum(axis=1), axis=0)
    * 100
)

print("\n===== POURCENTAGES — 6b APRÈS REGROUPEMENT =====")
print(
    table_6b_regroupe_pct.round(2)
)


# Transformation pour Plotly

graph_6b = (
    table_6b_regroupe_pct
    .reset_index()
    .melt(
        id_vars="type_cyberviolence_regroupe",
        var_name="genre",
        value_name="pourcentage"
    )
)


fig6b = px.bar(
    graph_6b,
    x="type_cyberviolence_regroupe",
    y="pourcentage",
    color="genre",
    barmode="group",
    title="Répartition du genre selon le type de cyberviolence — 2025",
    labels={
        "type_cyberviolence_regroupe": "Type de cyberviolence",
        "pourcentage": "Pourcentage (%)",
        "genre": "Genre"
    },
    text="pourcentage",
    color_discrete_map={
        "Féminin": "#C96583",
        "Masculin": "#5C6594"
    }
)

fig6b.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig6b.update_layout(
    yaxis_title="Pourcentage (%)",
    xaxis_title="Type de cyberviolence",
    yaxis_range=[0, 110],
    xaxis_tickangle=-25
)

fig6b.show()
fig6b.write_image("output/figures/kpi6b_cyberviolence_genre.png")
# KPI 6c — TYPE DE CYBERVIOLENCE × PLATEFORME

print("\n===== KPI 6c — TYPE DE CYBERVIOLENCE × PLATEFORME =====")

# Garder uniquement les lignes où les deux variables sont renseignées
df_6c = df.dropna(
    subset=["cyberharcelementType", "plateforme"]
).copy()

# Tableau de contingence — effectifs
table_6c = pd.crosstab(
    df_6c["cyberharcelementType"],
    df_6c["plateforme"]
)

print("\nTableau de contingence — Effectifs :")
print(table_6c)

print(
    f"\nTotal des observations utilisées : {table_6c.values.sum()}"
)

# POURCENTAGES EN LIGNE

pourcentages_6c = (
    table_6c
    .div(table_6c.sum(axis=1), axis=0)
    * 100
)

print("\nPourcentages en ligne :")
print(pourcentages_6c.round(2))

print("\nTotaux des lignes :")
print(table_6c.sum(axis=1))

print("\nTotaux des pourcentages par ligne :")
print(pourcentages_6c.sum(axis=1).round(2))

# EFFECTIFS THÉORIQUES

chi2_6c_initial, p_6c_initial, ddl_6c_initial, expected_6c_initial = (
    chi2_contingency(table_6c)
)

expected_6c_initial_df = pd.DataFrame(
    expected_6c_initial,
    index=table_6c.index,
    columns=table_6c.columns
)

print("\n===== EFFECTIFS THÉORIQUES — 6c =====")
print(expected_6c_initial_df.round(2))

# CONDITION DU CHI-DEUX
# Au moins 80 % des cases doivent avoir un effectif >= 5

nombre_cases_6c = expected_6c_initial.size
nombre_cases_5_6c = (expected_6c_initial >= 5).sum()

pourcentage_cases_5_6c = (
    nombre_cases_5_6c / nombre_cases_6c * 100
)

print("\n===== CONDITION DU CHI-DEUX — 6c =====")
print(f"Nombre total de cases : {nombre_cases_6c}")
print(
    f"Cases avec effectif théorique >= 5 : "
    f"{nombre_cases_5_6c}"
)
print(
    f"Pourcentage de cases >= 5 : "
    f"{pourcentage_cases_5_6c:.2f} %"
)

if pourcentage_cases_5_6c >= 80:
    print(
        "✓ Condition du χ² respectée "
        "(au moins 80 % des cases ont un effectif théorique >= 5)."
    )
else:
    print(
        "⚠ Condition du χ² non respectée."
    )
    print(
        "→ Un regroupement des catégories rares sera envisagé."
    )
    
# KPI 6c — REGROUPEMENT DES CATÉGORIES RARES

print("\n===== KPI 6c — REGROUPEMENT DES CATÉGORIES RARES =====")

# Catégories conservées séparément
categories_principales_6c = [
    "Autres",
    "Propos de haine",
    "Publication de photos intimes ou personnelles"
]

# Regroupement des catégories rares
df_6c["type_cyberviolence_regroupe"] = df_6c[
    "cyberharcelementType"
].apply(
    lambda x: x if x in categories_principales_6c else "Autres"
)

# Tableau de contingence après regroupement
table_6c_regroupe = pd.crosstab(
    df_6c["type_cyberviolence_regroupe"],
    df_6c["plateforme"]
)

print("\nTableau de contingence après regroupement :")
print(table_6c_regroupe)

# POURCENTAGES EN LIGNE

pourcentages_6c_regroupe = (
    table_6c_regroupe
    .div(table_6c_regroupe.sum(axis=1), axis=0)
    * 100
)

print("\nPourcentages en ligne après regroupement :")
print(pourcentages_6c_regroupe.round(2))

# EFFECTIFS THÉORIQUES

chi2_6c_regroupe, p_6c_regroupe, ddl_6c_regroupe, expected_6c_regroupe = (
    chi2_contingency(table_6c_regroupe)
)

expected_6c_regroupe_df = pd.DataFrame(
    expected_6c_regroupe,
    index=table_6c_regroupe.index,
    columns=table_6c_regroupe.columns
)

print("\n===== EFFECTIFS THÉORIQUES — 6c APRÈS REGROUPEMENT =====")
print(expected_6c_regroupe_df.round(2))

# CONDITION DU CHI-DEUX

nombre_cases_6c_regroupe = expected_6c_regroupe.size

nombre_cases_5_6c_regroupe = (
    expected_6c_regroupe >= 5
).sum()

pourcentage_cases_5_6c_regroupe = (
    nombre_cases_5_6c_regroupe
    / nombre_cases_6c_regroupe
    * 100
)

print("\n===== CONDITION DU CHI-DEUX — 6c APRÈS REGROUPEMENT =====")
print(
    f"Nombre total de cases : "
    f"{nombre_cases_6c_regroupe}"
)

print(
    f"Cases avec effectif théorique >= 5 : "
    f"{nombre_cases_5_6c_regroupe}"
)

print(
    f"Pourcentage de cases >= 5 : "
    f"{pourcentage_cases_5_6c_regroupe:.2f} %"
)

if pourcentage_cases_5_6c_regroupe >= 80:
    print(
        "✓ Condition du χ² respectée."
    )
else:
    print(
        "⚠ Condition du χ² toujours non respectée."
    )
    
# TEST DU CHI-DEUX — KPI 6c APRÈS REGROUPEMENT

print("\n===== TEST DU CHI-DEUX — 6c APRÈS REGROUPEMENT =====")

chi2_6c_final, p_6c_final, ddl_6c_final, expected_6c_final = (
    chi2_contingency(table_6c_regroupe)
)

print(f"Statistique χ² : {chi2_6c_final:.4f}")
print(f"Degrés de liberté : {ddl_6c_final}")
print(f"p-value : {p_6c_final:.4f}")

# Interprétation
alpha = 0.05

if p_6c_final < alpha:
    print(
        "✓ Association statistiquement significative"
    )
    print(
        "  entre le type de cyberviolence et la plateforme."
    )
else:
    print(
        "✓ Aucune association statistiquement significative"
    )
    print(
        "  entre le type de cyberviolence et la plateforme."
    )

# V DE CRAMÉR

n_6c = table_6c_regroupe.values.sum()

r_6c, k_6c = table_6c_regroupe.shape

v_cramer_6c = np.sqrt(
    chi2_6c_final /
    (n_6c * min(r_6c - 1, k_6c - 1))
)

print(f"V de Cramér : {v_cramer_6c:.4f}")

# Interprétation descriptive du V de Cramér
if v_cramer_6c < 0.10:
    interpretation_v_6c = "association très faible"
elif v_cramer_6c < 0.30:
    interpretation_v_6c = "association faible"
elif v_cramer_6c < 0.50:
    interpretation_v_6c = "association modérée"
else:
    interpretation_v_6c = "association forte"

print(
    f"Interprétation du V de Cramér : "
    f"{interpretation_v_6c}."
)

# DONNÉES POUR LE GRAPHIQUE 6c

graphique_6c = (
    pourcentages_6c_regroupe
    .reset_index()
    .melt(
        id_vars="type_cyberviolence_regroupe",
        var_name="plateforme",
        value_name="pourcentage"
    )
)

print("\n===== DONNÉES DU GRAPHIQUE 6c =====")
print(graphique_6c.round(2))

fig6c = px.bar(
    graphique_6c,
    x="type_cyberviolence_regroupe",
    y="pourcentage",
    color="plateforme",
    barmode="group",
    title="Répartition des plateformes selon le type de cyberviolence — 2025",
    labels={
        "type_cyberviolence_regroupe": "Type de cyberviolence",
        "pourcentage": "Pourcentage (%)",
        "plateforme": "Plateforme"
    },
    text="pourcentage",
    color_discrete_map={
        "Facebook": "#3268A1",
        "Instagram": "#E73DD9",
        "Tiktok": "#AE5C28",
        "WhatsApp": "#2AAE58"
    }
)

fig6c.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside"
)

fig6c.update_layout(
    yaxis_title="Pourcentage (%)",
    xaxis_title="Type de cyberviolence",
    yaxis_range=[0, 110],
    xaxis_tickangle=-25
)

fig6c.show()
fig6c.write_image("output/figures/kpi6c_cyberviolence_plateforme.png")
# KPI 6d — PLATEFORME × GENRE

print("\n===== KPI 6d — PLATEFORME × GENRE =====")

# 1. Préparation des données

df_6d = df[
    ["plateforme", "genre"]
].dropna()

# 2. Tableau de contingence — Effectifs

table_6d = pd.crosstab(
    df_6d["plateforme"],
    df_6d["genre"]
)

print("\nTableau de contingence — Effectifs :")
print(table_6d)

print(
    "\nTotal des observations utilisées :",
    table_6d.to_numpy().sum()
)

# 3. Pourcentages par ligne

pourcentages_6d = (
    table_6d
    .div(table_6d.sum(axis=1), axis=0)
    .multiply(100)
    .round(2)
)

print("\nPourcentages en ligne :")
print(pourcentages_6d)

print("\nTotaux des lignes :")
print(table_6d.sum(axis=1))

print("\nTotaux des pourcentages par ligne :")
print(pourcentages_6d.sum(axis=1))

# 4. Effectifs théoriques

chi2_6d, p_value_6d, ddl_6d, effectifs_theoriques_6d = chi2_contingency(
    table_6d
)

effectifs_theoriques_6d = pd.DataFrame(
    effectifs_theoriques_6d,
    index=table_6d.index,
    columns=table_6d.columns
)

print("\n===== EFFECTIFS THÉORIQUES — 6d =====")
print(effectifs_theoriques_6d.round(2))

# 5. Vérification de la condition du χ²

nombre_cases_6d = effectifs_theoriques_6d.size

nombre_cases_sup_5_6d = (
    effectifs_theoriques_6d >= 5
).sum().sum()

pourcentage_cases_sup_5_6d = (
    nombre_cases_sup_5_6d / nombre_cases_6d
) * 100

print("\n===== CONDITION DU CHI-DEUX — 6d =====")
print("Nombre total de cases :", nombre_cases_6d)
print(
    "Cases avec effectif théorique >= 5 :",
    nombre_cases_sup_5_6d
)
print(
    "Pourcentage de cases >= 5 :",
    round(pourcentage_cases_sup_5_6d, 2),
    "%"
)

# 6. Test du χ²

if pourcentage_cases_sup_5_6d >= 80:

    print("✓ Condition du χ² respectée.")

    print("\n===== TEST DU CHI-DEUX — 6d =====")

    print(
        "Statistique χ² :",
        round(chi2_6d, 4)
    )

    print(
        "Degrés de liberté :",
        ddl_6d
    )

    print(
        "p-value :",
        round(p_value_6d, 4)
    )

    alpha = 0.05

    if p_value_6d < alpha:
        print(
            "✓ Association statistiquement significative"
            " entre la plateforme et le genre."
        )
    else:
        print(
            "✓ Aucune association statistiquement significative"
            " entre la plateforme et le genre."
        )

    # 7. V de Cramér

    n_6d = table_6d.to_numpy().sum()

    min_dimension_6d = min(
        table_6d.shape[0] - 1,
        table_6d.shape[1] - 1
    )

    v_cramer_6d = np.sqrt(
        chi2_6d /
        (n_6d * min_dimension_6d)
    )

    print(
        "V de Cramér :",
        round(v_cramer_6d, 4)
    )

    # Interprétation descriptive de l'intensité
    if v_cramer_6d < 0.10:
        interpretation_v_6d = "association très faible"
    elif v_cramer_6d < 0.30:
        interpretation_v_6d = "association faible"
    elif v_cramer_6d < 0.50:
        interpretation_v_6d = "association modérée"
    else:
        interpretation_v_6d = "association forte"

    print(
        "Interprétation du V de Cramér :",
        interpretation_v_6d + "."
    )

else:

    print(
        "⚠ Condition du χ² non respectée."
    )

    print(
        "→ Interprétation descriptive uniquement."
    )

# 8. Données pour le graphique 6d

graphique_6d = (
    pourcentages_6d
    .reset_index()
    .melt(
        id_vars="plateforme",
        var_name="genre",
        value_name="pourcentage"
    )
)

print("\n===== DONNÉES DU GRAPHIQUE 6d =====")
print(graphique_6d)

# ===== GRAPHIQUE KPI 6d =====

fig6d = px.bar(
    graphique_6d,
    x="plateforme",
    y="pourcentage",
    color="genre",
    barmode="group",
    text="pourcentage",
    title="Répartition du genre selon la plateforme",
    labels={
        "plateforme": "Plateforme",
        "pourcentage": "Pourcentage (%)",
        "genre": "Genre"
    },
    color_discrete_map={
        "Féminin": "#C96583",
        "Masculin": "#5C6594"
    }
)

fig6d.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside"
)

fig6d.update_layout(
    yaxis_title="Pourcentage (%)",
    xaxis_title="Plateforme"
)

fig6d.show()
fig6d.write_image("output/figures/kpi6d_plateforme_genre.png")
# KPI 6e — ANONYMAT × GENRE

print("\n===== KPI 6e — ANONYMAT × GENRE =====")

# Garder uniquement les observations ayant anonymat ET genre renseignés
df_6e = df[
    df["anonymat"].notna() &
    df["genre"].notna()
].copy()

# Tableau de contingence
table_6e = pd.crosstab(
    df_6e["anonymat"],
    df_6e["genre"]
)

print("\nTableau de contingence — Effectifs :")
print(table_6e)

print(
    "\nTotal des observations utilisées :",
    table_6e.values.sum()
)

# Pourcentages en ligne

pourcentages_6e = (
    table_6e
    .div(table_6e.sum(axis=1), axis=0)
    * 100
)

print("\nPourcentages en ligne :")
print(pourcentages_6e.round(2))

print("\nTotaux des lignes :")
print(table_6e.sum(axis=1))

print("\nTotaux des pourcentages par ligne :")
print(pourcentages_6e.sum(axis=1).round(2))


# TEST EXACT DE FISHER

print("\n===== TEST EXACT DE FISHER — 6e =====")

# Vérifier qu'on possède bien un tableau 2 × 2
if table_6e.shape == (2, 2):

    odds_ratio, p_value_fisher = fisher_exact(table_6e)

    print("Odds ratio :", round(odds_ratio, 4))
    print("p-value de Fisher :", round(p_value_fisher, 4))

    if p_value_fisher < 0.05:
        print(
            "✓ Association statistiquement significative "
            "entre l'anonymat et le genre."
        )
    else:
        print(
            "✓ Aucune association statistiquement significative "
            "entre l'anonymat et le genre."
        )

else:
    print(
        "⚠ Le tableau n'est pas 2×2. "
        "Le test exact de Fisher ne peut pas être appliqué directement."
    )

# DONNÉES DU GRAPHIQUE 6e

graphique_6e = (
    pourcentages_6e
    .reset_index()
    .melt(
        id_vars="anonymat",
        var_name="genre",
        value_name="pourcentage"
    )
)

print("\n===== DONNÉES DU GRAPHIQUE 6e =====")
print(graphique_6e)

# GRAPHIQUE KPI 6e

fig6e = px.bar(
    graphique_6e,
    x="anonymat",
    y="pourcentage",
    color="genre",
    barmode="group",
    text="pourcentage",
    title="Répartition du genre selon l'anonymat",
    labels={
        "anonymat": "Anonymat",
        "pourcentage": "Pourcentage (%)",
        "genre": "Genre"
    },
    color_discrete_map={
        "Féminin": "#C96583",
        "Masculin": "#5C6594"
    }
)

fig6e.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside"
)

fig6e.update_layout(
    yaxis_title="Pourcentage (%)",
    xaxis_title="Anonymat"
)

fig6e.show()
fig6e.write_image("output/figures/kpi6e_anonymat_genre.png")
# KPI 6f — ACCOMPAGNEMENT × TYPE DE CYBERVIOLENCE

print("\n===== KPI 6f — ACCOMPAGNEMENT × TYPE DE CYBERVIOLENCE =====")

# Garder uniquement les observations renseignées
df_6f = df[
    df["accompagnement"].notna()
    & df["cyberharcelementType"].notna()
].copy()

# Tableau de contingence — effectifs
table_6f = pd.crosstab(
    df_6f["cyberharcelementType"],
    df_6f["accompagnement"]
)

print("\nTableau de contingence — Effectifs :")
print(table_6f)

print(
    "\nTotal des observations utilisées :",
    table_6f.values.sum()
)

# Pourcentages en ligne
pourcentages_6f = (
    table_6f
    .div(table_6f.sum(axis=1), axis=0)
    * 100
)

print("\nPourcentages en ligne :")
print(pourcentages_6f.round(2))

print("\nTotaux des lignes :")
print(table_6f.sum(axis=1))

print("\nTotaux des pourcentages par ligne :")
print(pourcentages_6f.sum(axis=1).round(2))

# VERIFICATION DE LA CONDITION DU CHI-DEUX

chi2_6f, p_6f, ddl_6f, expected_6f = chi2_contingency(
    table_6f
)

expected_6f_df = pd.DataFrame(
    expected_6f,
    index=table_6f.index,
    columns=table_6f.columns
)

print("\n===== EFFECTIFS THÉORIQUES — 6f =====")
print(expected_6f_df.round(2))


# Vérification de la condition du χ²
nb_cases_6f = expected_6f.size

nb_cases_valides_6f = (
    expected_6f >= 5
).sum()

pourcentage_valides_6f = (
    nb_cases_valides_6f
    / nb_cases_6f
    * 100
)

print("\n===== CONDITION DU CHI-DEUX — 6f =====")

print(
    "Nombre total de cases :",
    nb_cases_6f
)

print(
    "Cases avec effectif théorique >= 5 :",
    nb_cases_valides_6f
)

print(
    "Pourcentage de cases >= 5 :",
    round(pourcentage_valides_6f, 2),
    "%"
)


# CHOIX DU TEST STATISTIQUE

if pourcentage_valides_6f >= 80:
    # CONDITION DU CHI-DEUX RESPECTEE

    print(
        "\n✓ Condition du χ² respectée."
    )

    print(
        "\n===== TEST DU CHI-DEUX — 6f ====="
    )

    print(
        "Statistique χ² :",
        round(chi2_6f, 4)
    )

    print(
        "Degrés de liberté :",
        ddl_6f
    )

    print(
        "p-value :",
        round(p_6f, 4)
    )

    if p_6f < 0.05:

        print(
            "✓ Association statistiquement significative "
            "entre l'accompagnement et le type de cyberviolence."
        )

    else:

        print(
            "✓ Aucune association statistiquement significative "
            "entre l'accompagnement et le type de cyberviolence."
        )


else:
    # CONDITION DU CHI-DEUX NON RESPECTEE

    print(
        "\n⚠ Condition du χ² non respectée."
    )

    print(
        "→ Utilisation du test exact de Fisher."
    )

    print(
        "\n===== TEST EXACT DE FISHER — 6f ====="
    )

    try:

        odds_ratio_6f, p_fisher_6f = fisher_exact(
            table_6f.values
        )

        print(
            "p-value de Fisher :",
            round(p_fisher_6f, 4)
        )

        if p_fisher_6f < 0.05:

            print(
                "✓ Association statistiquement significative "
                "entre l'accompagnement et le type de cyberviolence."
            )

        else:

            print(
                "✓ Aucune association statistiquement significative "
                "entre l'accompagnement et le type de cyberviolence."
            )

    except ValueError:

        print(
            "⚠ Le test exact de Fisher n'est pas disponible "
            "pour ce tableau avec cette version de SciPy."
        )

        print(
            "→ Interprétation descriptive uniquement."
        )

# POURCENTAGES POUR LE GRAPHIQUE

pourcentages_final_6f = (
    table_6f
    .div(table_6f.sum(axis=1), axis=0)
    * 100
)

print(
    "\n===== POURCENTAGES — 6f ====="
)

print(
    pourcentages_final_6f.round(2)
)

# GRAPHIQUE KPI 6f

graphique_6f = (
    pourcentages_final_6f
    .reset_index()
    .melt(
        id_vars=pourcentages_final_6f.index.name,
        var_name="accompagnement",
        value_name="pourcentage"
    )
)

graphique_6f.columns = [
    "type_cyberviolence",
    "accompagnement",
    "pourcentage"
]

print(
    "\n===== DONNÉES DU GRAPHIQUE 6f ====="
)

print(
    graphique_6f
)


fig6f = px.bar(
    graphique_6f,
    x="type_cyberviolence",
    y="pourcentage",
    color="accompagnement",
    barmode="group",
    title=(
        "Demande d'accompagnement "
        "selon le type de cyberviolence"
    ),
    labels={
        "type_cyberviolence":
            "Type de cyberviolence",
        "pourcentage":
            "Pourcentage (%)",
        "accompagnement":
            "Demande d'accompagnement"
    },
    text="pourcentage",
    color_discrete_map={
        "Non": "#CE6262",
        "Oui": "#4B994B"
    }
)

fig6f.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside"
)

fig6f.update_layout(
    xaxis_tickangle=-45
)

fig6f.show()
fig6f.write_image("output/figures/kpi6f_accompagnement_cyberviolence.png")