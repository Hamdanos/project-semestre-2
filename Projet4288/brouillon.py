import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import re
import tkinter as tk
from tkinter import filedialog, messagebox
import sqlite3



# Fonction pour valider les données
def validate_data(data):
    valid = True
    invalid_fields = []

    # Vérification du nom
    if not data['Nom'].isalpha():
        invalid_fields.append('Nom')
        valid = False

    # Vérification des prénoms
    if not data['Prénoms'].replace(' ', '').isalpha():
        invalid_fields.append('Prénoms')
        valid = False

    # Vérification de la date de naissance (format jj/mm/aaaa)
    date_pattern = re.compile(r'\d{2}/\d{2}/\d{4}')
    if not date_pattern.match(data['Date de naissance']):
        invalid_fields.append('Date de naissance')
        valid = False

    # Vérification du lieu de naissance
    if not data['Lieu de naissance'].replace(' ', '').isalpha():
        invalid_fields.append('Lieu de naissance')
        valid = False

    # Vérification du sexe
    if data['Sexe'] not in ['Homme', 'Femme']:
        invalid_fields.append('Sexe')
        valid = False

    # Vérification de la taille (format xx.yy)
    if not re.match(r'\d{1,2}\.\d{1,2}', data['Taille']):
        invalid_fields.append('Taille')
        valid = False

    # Vérification de la profession
    if not data['Profession'].replace(' ', '').isalpha():
        invalid_fields.append('Profession')
        valid = False

    # Si des champs sont invalides, demandez à l'utilisateur de les corriger manuellement
    if not valid:
        messagebox.showerror("Données invalides", f"Les champs suivants sont invalides : {', '.join(invalid_fields)}")
        
        # Ajouter le code pour permettre à l'utilisateur de saisir manuellement les données invalides
        for field in invalid_fields:
            user_input = tk.simpledialog.askstring("Saisie manuelle", f"Saisissez le champ {field} manuellement:")
            data[field] = user_input
        
        # Réexécuter la validation après la saisie manuelle
        return validate_data(data)

    return valid


# Fonction pour stocker les données dans la base de données SQLite
def store_data(data):
    # Connexion à la base de données
    conn = sqlite3.connect('cni.db')
    cursor = conn.cursor()
    
    # Insertion des données dans la table
    cursor.execute('''INSERT INTO cni (nom, prenom, date_naissance, lieu_naissance, sexe, taille, profession)
                      VALUES (?, ?, ?, ?, ?, ?, ?)''', (data['Nom'], data['Prénoms'], data['Date de naissance'],
                                                        data['Lieu de naissance'], data['Sexe'], data['Taille'],
                                                        data['Profession']))
    
    # Commit et fermeture de la connexion
    conn.commit()
    conn.close()

# Définition de la fonction pour créer la table dans la base de données
def creer_table():
    # Connexion à la base de données
    conn = sqlite3.connect('cni.db')
    cursor = conn.cursor()
    
    # Création de la table si elle n'existe pas
    # Création de la table si elle n'existe pas
    cursor.execute('''CREATE TABLE IF NOT EXISTS cni (
                    id INTEGER PRIMARY KEY,
                    nom TEXT, 
                    prenom TEXT, 
                    date_naissance TEXT, 
                    lieu_naissance TEXT, 
                    sexe TEXT, 
                    taille TEXT, 
                    profession TEXT)''')

    
    # Commit et fermeture de la connexion
    conn.commit()
    conn.close()

# Appel à la fonction de création de la table (à appeler une seule fois)
creer_table()

# Fonction pour extraire le texte de l'image
def extract_text(image_path):
    img = Image.open(image_path)
    img = img.convert('L')
    img = img.filter(ImageFilter.MedianFilter())
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2)
    img = img.point(lambda p: p > 128 and 255)
    text = pytesseract.image_to_string(img, lang='fra')
    return text

# Fonction pour structurer les données
def clean_and_structure_data(text):
    data = {}
    match = re.search(r'NOM/SURNOM:\s*(.*)', text)
    data['Nom'] = match.group(1).strip() if match else 'N/A'
    
    match = re.search(r'PRÉNOMS/GIVEN NAMES:\s*(.*)', text)
    data['Prénoms'] = match.group(1).strip() if match else 'N/A'
    
    match = re.search(r'DATE DE NAISSANCE/DATE OF BIRTH:\s*(.*)', text)
    data['Date de naissance'] = match.group(1).strip() if match else 'N/A'
    
    match = re.search(r'LIEU DE NAISSANCE/PLACE OF BIRTH:\s*(.*)', text)
    data['Lieu de naissance'] = match.group(1).strip() if match else 'N/A'
    
    match = re.search(r'SEXE/SEX:\s*(.*)', text)
    data['Sexe'] = match.group(1).strip() if match else 'N/A'
    
    match = re.search(r'TAILLE/HEIGHT:\s*(.*)', text)
    data['Taille'] = match.group(1).strip() if match else 'N/A'
    
    match = re.search(r'PROFESSION/OCCUPATION:\s*(.*)', text)
    data['Profession'] = match.group(1).strip() if match else 'N/A'
    
    return data

# Fonction pour gérer le téléchargement d'images et l'extraction de texte
def upload_image():
    image_path = filedialog.askopenfilename()
    if image_path:
        text = extract_text(image_path)
        data = clean_and_structure_data(text)
        result = '\n'.join([f'{k}: {v}' for k, v in data.items()])
        messagebox.showinfo("Données extraites", result)
# Fonction pour mettre à jour les données existantes dans la base de données SQLite
def update_data(data, id):
    conn = sqlite3.connect('cni.db')
    cursor = conn.cursor()
    cursor.execute('''UPDATE cni SET nom=?, prenom=?, date_naissance=?, lieu_naissance=?, sexe=?, taille=?, profession=? WHERE id=?''',
                   (data['Nom'], data['Prénoms'], data['Date de naissance'], data['Lieu de naissance'], data['Sexe'], data['Taille'], data['Profession'], id))
    conn.commit()
    conn.close()

# Fonction pour ajouter de nouvelles données dans la base de données SQLite
def add_data(data):
    conn = sqlite3.connect('cni.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO cni (nom, prenom, date_naissance, lieu_naissance, sexe, taille, profession) VALUES (?, ?, ?, ?, ?, ?, ?)''',
                   (data['Nom'], data['Prénoms'], data['Date de naissance'], data['Lieu de naissance'], data['Sexe'], data['Taille'], data['Profession']))
    conn.commit()
    conn.close()

# Fonction pour afficher toutes les données dans la base de données SQLite
def display_all_data():
    conn = sqlite3.connect('cni.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM cni''')
    all_data = cursor.fetchall()
    conn.close()
    for row in all_data:
        print(row)  # Vous pouvez remplacer cette ligne par l'affichage dans l'interface utilisateur

# Exemple d'utilisation de la fonction d'ajout de données
new_data = {
    'Nom': 'Doe',
    'Prénoms': 'John',
    'Date de naissance': '01/01/1990',
    'Lieu de naissance': 'Paris',
    'Sexe': 'Homme',
    'Taille': '180.5',
    'Profession': 'Ingénieur'
}
add_data(new_data)

# Exemple d'utilisation de la fonction de mise à jour de données
# Fonction pour mettre à jour les données existantes dans la base de données SQLite
def update_data(data):
    conn = sqlite3.connect('cni.db')
    cursor = conn.cursor()
    cursor.execute('''UPDATE cni SET nom=?, prenom=?, date_naissance=?, lieu_naissance=?, sexe=?, taille=?, profession=?''',
                   (data['Nom'], data['Prénoms'], data['Date de naissance'], data['Lieu de naissance'], data['Sexe'], data['Taille'], data['Profession']))
    conn.commit()
    conn.close()

# Exemple d'utilisation de la fonction pour afficher toutes les données
display_all_data()

# Configuration de l'interface Tkinter
root = tk.Tk()
root.title("Extraction de CNI")

upload_button = tk.Button(root, text="Télécharger une image", command=upload_image)
upload_button.pack(pady=20)

root.mainloop()



#Réaliser par HAMDANE ALLAMINE MOUSSA