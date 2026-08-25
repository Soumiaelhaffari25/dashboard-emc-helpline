import pandas as pd

df = pd.read_excel("data/raw/signalements.xlsx")

print("===== PREMIÈRES LIGNES =====")
print(df.head())

print("\n===== DIMENSIONS =====")
print(df.shape)

print("\n===== INFORMATIONS =====")
df.info()

print("\n===== VALEURS DES VARIABLES CATEGORIELLES =====")
colonnes_categorielles = [
    "cyberharcelementType",
    "plateforme",
    "genre",
    "age",
    "anonymat",
    "accompagnement",
    "typeAccompagnement",
    "langue"
]

for col in colonnes_categorielles:
    print(f"\n--- {col} ---")
    print(df[col].value_counts(dropna=False))