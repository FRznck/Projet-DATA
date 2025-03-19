import mysql.connector
import pandas as pd

# Connexion à MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Monserveur123",
    database="books_db"
)
cursor = conn.cursor()

try:
    # Création de la table avec la colonne 'note' en INT
    cursor.execute("""  
    CREATE TABLE IF NOT EXISTS books (
        id INT AUTO_INCREMENT PRIMARY KEY,        
        titre VARCHAR(255) NOT NULL,              
        prix DECIMAL(10,2) NOT NULL,            
        categorie VARCHAR(100) NOT NULL,         
        disponibilite VARCHAR(50) NOT NULL,  
        note INT NOT NULL,                        
        lien TEXT NOT NULL,                      
        description TEXT,
        moyenne_avis DECIMAL(10,2)  # Nouvelle colonne pour la moyenne des avis
    )
    """)
    conn.commit()
    print("Table créée avec succès.")

    # Importer les données du fichier CSV
    livres = pd.read_csv("livres2.csv", encoding="utf-8")

    # Vérifier les colonnes manquantes
    required_columns = {"titre", "prix", "categorie", "disponibilite", "note", "lien", "description"}
    if not required_columns.issubset(livres.columns):
        print(f"Erreur : Colonnes manquantes dans le fichier CSV : {required_columns - set(livres.columns)}")
        exit(1)

    # Nettoyer la colonne 'prix'
    livres["prix"] = livres["prix"].str.replace("\u00a3", "", regex=False)  # Supprimer le symbole £
    livres["prix"] = livres["prix"].str.replace(",", ".", regex=False)  # Remplacer les virgules par des points
    livres["prix"] = pd.to_numeric(livres["prix"], errors="coerce")  # Convertir en nombre décimal

    # Vérifier les valeurs manquantes après conversion
    if livres["prix"].isnull().any():
        print("Erreur : La colonne 'prix' contient des valeurs non numériques ou invalides.")
        exit(1)

    # Remplacer les valeurs NaN par des valeurs par défaut
    livres = livres.fillna({
        "description": ""    
    })

    # Dictionnaire de conversion des notes
    mapping_notes = {
        "un": 1, "deux": 2, "trois": 3, "quatre": 4, "cinq": 5,
        "one": 1, "two": 2, "three": 3, "four": 4, "five": 5 
    }

    # Convertir les notes en minuscules puis en nombres
    livres["note"] = livres["note"].str.lower().map(mapping_notes)

    # Vérifier si des notes n'ont pas été converties
    if livres["note"].isnull().any():
        print("Erreur : Certaines notes contiennent des valeurs inconnues :", livres["note"].unique())
        exit(1)

    # Normaliser les catégories
    livres["categorie"] = livres["categorie"].str.strip().str.capitalize()

    # Calculer la moyenne des avis
    moyenne_avis = livres["note"].mean()
    livres["moyenne_avis"] = moyenne_avis

    # Fonction pour vérifier les contraintes
    def verifier_donnees(row):
        if not row["titre"] or not row["categorie"] or not row["disponibilite"] or row["note"] is None or not row["lien"]:
            print(f"Erreur : Une ligne contient des valeurs vides. {row.to_dict()}")
            return False
        if row["prix"] <= 0:
            print(f"Erreur : Prix invalide pour {row['titre']} ({row['prix']})")
            return False
        return True

    # Appliquer la vérification
    livres = livres[livres.apply(verifier_donnees, axis=1)]

    # Préparation des données pour l'insertion
    data_to_insert = [
        (row["titre"], row["prix"], row["categorie"], row["disponibilite"], row["note"], row["lien"], row["description"], row["moyenne_avis"])
        for index, row in livres.iterrows()
    ]

    # Insertion des données
    cursor.executemany(
        "INSERT INTO books (titre, prix, categorie, disponibilite, note, lien, description, moyenne_avis) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        data_to_insert
    )
    conn.commit()
    print("Données CSV insérées avec succès !")

except Exception as e:
    print(f"Une erreur s'est produite : {e}")
    conn.rollback()  # Annuler les changements en cas d'erreur

finally:
    
    cursor.close()
    conn.close()