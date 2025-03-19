import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


livres = pd.read_csv("livres2.csv")


# Distribution des notes
plt.figure(figsize=(8, 5))
sns.countplot(x="note", data=livres, palette="viridis")
plt.title("Distribution des Notes des Livres")
plt.xlabel("Note")
plt.ylabel("Nombre de Livres")
plt.show()

# Corrélation entre le prix et la note
plt.figure(figsize=(10, 6))
sns.scatterplot(x="prix", y="note", data=livres, hue="categorie", palette="Set2")
plt.title("Corrélation entre le Prix et la Note")
plt.xlabel("Prix (£)")
plt.ylabel("Note")
plt.legend(title="Catégorie")
plt.show()

# Répartition des catégories
#plt.figure(figsize=(10, 6))
#sns.countplot(y="categorie", data=livres, palette="Set3", order=livres["categorie"].value_counts().index)
#plt.title("Répartition des Catégories de Livres")
#plt.xlabel("Nombre de Livres")
#plt.ylabel("Catégorie")
#plt.show()
