import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import re
import spacy
import sqlite3
import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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

# Fonction pour structurer les données extraites
def clean_and_structure_data(text):
    nlp = spacy.load('fr_core_news_sm')
    doc = nlp(text)
    entities = {ent.label_: ent.text for ent in doc.ents}
    
    data = {}
    data['Nom'] = entities.get('PER', 'N/A')
    data['Prénoms'] = entities.get('PER', 'N/A')
    data['Date de naissance'] = entities.get('DATE', 'N/A')
    data['Lieu de naissance'] = entities.get('LOC', 'N/A')
    data['Sexe'] = 'N/A'  
    data['Taille'] = 'N/A'  
    data['Profession'] = 'N/A'  

    return data

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

    return valid, invalid_fields

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

# Fonction pour afficher toutes les données dans un tableau
def display_all_data():
    conn = sqlite3.connect('cni.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM cni''')
    all_data = cursor.fetchall()
    conn.close()

    data_window = tk.Toplevel(root)
    data_window.title("Données enregistrées")

    for idx, row in enumerate(all_data):
        for j, value in enumerate(row):
            tk.Label(data_window, text=value).grid(row=idx, column=j)

# Fonction pour afficher la répartition des sexes
def display_gender_distribution():
    conn = sqlite3.connect('cni.db')
    cursor = conn.cursor()
    cursor.execute('SELECT sexe, COUNT(*) FROM cni GROUP BY sexe')
    data = cursor.fetchall()
    conn.close()

    labels = [row[0] for row in data]
    sizes = [row[1] for row in data]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%')
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    chart_window = tk.Toplevel(root)
    chart_window.title("Répartition des sexes")

    canvas = FigureCanvasTkAgg(fig, master=chart_window)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Fonction pour gérer le téléchargement d'images et l'extraction de texte
def upload_image():
    image_path = filedialog.askopenfilename()
    if image_path:
        text = extract_text(image_path)
        data = clean_and_structure_data(text)
        valid, invalid_fields = validate_data(data)
        if not valid:
            messagebox.showerror("Données invalides", f"Les champs suivants sont invalides : {', '.join(invalid_fields)}")
        else:
            store_data(data)
            messagebox.showinfo("Succès", "Les données ont été enregistrées avec succès")
            display_all_data()

# Configuration de l'interface Tkinter
root = tk.Tk()
root.title("Extraction de CNI")

upload_button = tk.Button(root, text="Télécharger une image", command=upload_image)
upload_button.pack(pady=20)

display_button = tk.Button(root, text="Afficher toutes les données", command=display_all_data)
display_button.pack(pady=20)

gender_distribution_button = tk.Button(root, text="Afficher la répartition des sexes", command=display_gender_distribution)
gender_distribution_button.pack(pady=20)

root.mainloop()
