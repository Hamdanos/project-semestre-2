import os
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import re

# Définir la variable d'environnement TESSDATA_PREFIX
os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR'

# Chemin vers l'image du relevé de notes
image_path = 'E:/Projet4288/image/relevé.jpg'

# Charger l'image
img = Image.open(image_path)

# Prétraitement de l'image
img = img.convert('L')  # Convertir en niveaux de gris
img = img.filter(ImageFilter.MedianFilter())  # Appliquer un filtre médian pour réduire le bruit
enhancer = ImageEnhance.Contrast(img)
img = enhancer.enhance(2)  # Augmenter le contraste
img = img.point(lambda p: p > 128 and 255)  # Binarisation

# Chemin vers l'exécutable tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Appliquer l'OCR
text = pytesseract.image_to_string(img, lang='FRA')

# Afficher le texte extrait
print("Texte extrait :\n", text)

# Analyser et organiser les informations extraites
def extract_information(text):
    info = {}

    nom_match = re.search(r'Nom et Prénoms:\s*(.*)', text)
    date_naissance_match = re.search(r'Né\(e\) le:\s*(\d{2}/\d{2}/\d{4})', text)
    lieu_naissance_match = re.search(r'Né\(e\) le:\s*\d{2}/\d{2}/\d{4}\s*NDJAMENA', text)
    genre_match = re.search(r'Genre:\s*(.*)', text)
    nationalite_match = re.search(r'Nationalité:\s*(.*)', text)
    centre_examen_match = re.search(r'Centre d\'examen:\s*(.*)', text)
    serie_match = re.search(r'Série:\s*(.*)', text)
    num_matricule_match = re.search(r'N° Matricule:\s*(.*)', text)
    
    if nom_match:
        info['Nom et Prénoms'] = nom_match.group(1).strip()
    else:
        info['Nom et Prénoms'] = None

    if date_naissance_match:
        info['Date de Naissance'] = date_naissance_match.group(1).strip()
    else:
        info['Date de Naissance'] = None

    if lieu_naissance_match:
        info['Lieu de Naissance'] = "NDJAMENA"  # Puisque l'information est statique dans ce cas
    else:
        info['Lieu de Naissance'] = None

    if genre_match:
        info['Genre'] = genre_match.group(1).strip()
    else:
        info['Genre'] = None

    if nationalite_match:
        info['Nationalité'] = nationalite_match.group(1).strip()
    else:
        info['Nationalité'] = None

    if centre_examen_match:
        info['Centre d\'examen'] = centre_examen_match.group(1).strip()
    else:
        info['Centre d\'examen'] = None

    if serie_match:
        info['Série'] = serie_match.group(1).strip()
    else:
        info['Série'] = None

    if num_matricule_match:
        info['N° Matricule'] = num_matricule_match.group(1).strip()
    else:
        info['N° Matricule'] = None
        
    return info

infos = extract_information(text)

# Afficher les informations organisées
print("Informations organisées :\n", infos)





import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import re
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
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
            user_input = simpledialog.askstring("Saisie manuelle", f"Saisissez le champ {field} manuellement:")
            data[field] = user_input
        
        # Réexécuter la validation après la saisie manuelle
        return validate_data(data)

    return valid

# Fonction pour stocker les données dans la base de données SQLite
def store_data(data):
    conn = sqlite3.connect('cni.db')
    cursor = conn.cursor()
    
    cursor.execute('''INSERT INTO cni (nom, prenom, date_naissance, lieu_naissance, sexe, taille, profession)
                      VALUES (?, ?, ?, ?, ?, ?, ?)''', (data['Nom'], data['Prénoms'], data['Date de naissance'],
                                                        data['Lieu de naissance'], data['Sexe'], data['Taille'],
                                                        data['Profession']))
    
    conn.commit()
    conn.close()

# Définition de la fonction pour créer la table dans la base de données
def creer_table():
    conn = sqlite3.connect('cni.db')
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS cni (
                    id INTEGER PRIMARY KEY,
                    nom TEXT, 
                    prenom TEXT, 
                    date_naissance TEXT, 
                    lieu_naissance TEXT, 
                    sexe TEXT, 
                    taille TEXT, 
                    profession TEXT)''')

    conn.commit()
    conn.close()

# Appel à la fonction de création de la table
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
    match = re.search(r'Nom:\s*(.*)', text)
    data['Nom'] = match.group(1).strip() if match else 'N/A'
    
    match = re.search(r'Prénoms:\s*(.*)', text)
    data['Prénoms'] = match.group(1).strip() if match else 'N/A'
    
    match = re.search(r'Date de naissance:\s*(.*)', text)
    data['Date de naissance'] = match.group(1).strip() if match else 'N/A'
    
    match = re.search(r'Lieu de naissance:\s*(.*)', text)
    data['Lieu de naissance'] = match.group(1).strip() if match else 'N/A'
    
    match = re.search(r'Sexe:\s*(.*)', text)
    data['Sexe'] = match.group(1).strip() if match else 'N/A'
    
    match = re.search(r'Taille:\s*(.*)', text)
    data['Taille'] = match.group(1).strip() if match else 'N/A'
    
    match = re.search(r'Profession:\s*(.*)', text)
    data['Profession'] = match.group(1).strip() if match else 'N/A'
    
    return data

# Fonction pour gérer le téléchargement d'images et l'extraction de texte
def upload_image():
    image_path = filedialog.askopenfilename()
    if image_path:
        text = extract_text(image_path)
        data = clean_and_structure_data(text)
        if validate_data(data):
            store_data(data)
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

# Fonction pour afficher toutes les données dans la base de données SQLite
def display_all_data():
    conn = sqlite3.connect('cni.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM cni''')
    all_data = cursor.fetchall()
    conn.close()
    for row in all_data:
        print(row)  # Vous pouvez remplacer cette ligne par l'affichage dans l'interface utilisateur

# Configuration de l'interface Tkinter
root = tk.Tk()
root.title("Extraction de CNI")

upload_button = tk.Button(root, text="Télécharger une image", command=upload_image)
upload_button.pack(pady=20)

root.mainloop()

