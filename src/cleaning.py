import pandas as pd

# 1. CHARGEMENT DES DONNÉES
df = pd.read_excel("data/raw/signalements.xlsx")
print("Dimensions avant nettoyage :", df.shape)


# 2. NETTOYAGE DES ESPACES
colonnes_textuelles = [
    "cyberharcelementType",
    "plateforme",
    "genre",
    "age",
    "anonymat",
    "accompagnement",
    "typeAccompagnement",
    "langue"
]

for col in colonnes_textuelles:
    df[col] = df[col].apply(
        lambda x: x.strip() if isinstance(x, str) else x
    )


# 3. NORMALISATION DE L'ACCOMPAGNEMENT
df["accompagnement"] = (
    df["accompagnement"]
    .str.lower()
    .map({
        "oui": "Oui",
        "non": "Non"
    })
)


# 4. NORMALISATION DE LA LANGUE
df["langue"] = df["langue"].str.lower()


# 5. CONVERSION DE LA DATE
df["date"] = pd.to_datetime(
    df["date"],
    errors="coerce"
)


# 6. CONTRÔLE APRÈS NETTOYAGE
print("\nDimensions après nettoyage :", df.shape)

print("\nValeurs de cyberharcelementType :")
print(df["cyberharcelementType"].value_counts(dropna=False))

print("\nValeurs de accompagnement :")
print(df["accompagnement"].value_counts(dropna=False))

print("\nValeurs de langue :")
print(df["langue"].value_counts(dropna=False))

print("\nValeurs manquantes :")
print(df.isnull().sum())


# 7. VALIDATION DU NETTOYAGE
assert len(df) == 138, "Le nombre de lignes a changé !"
assert df["cyberharcelementType"].str.contains(
    r"^\s|\s$", regex=True
).sum() == 0, "Des espaces superflus sont encore présents !"

assert set(df["accompagnement"].dropna().unique()) == {"Oui", "Non"}, \
    "Les modalités de accompagnement ne sont pas normalisées !"

assert set(df["langue"].dropna().unique()) == {"fr", "ar"}, \
    "Les modalités de langue ne sont pas normalisées !"

print("\n✓ Validation du nettoyage réussie.")


# 8. SAUVEGARDE DES DONNÉES NETTOYÉES
df.to_csv(
    "data/processed/signalements_clean.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nFichier nettoyé sauvegardé avec succès.")