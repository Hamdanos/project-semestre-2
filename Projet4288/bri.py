import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import re
import tkinter as tk
from tkinter import filedialog, messagebox
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
        valid, invalid_fields = validate_data(data)
        if not valid:
            messagebox.showerror("Données invalides", f"Les champs suivants sont invalides : {', '.join(invalid_fields)}")
        display_data(data)

# Fonction pour afficher les données dans des champs de saisie et permettre la modification
def display_data(data):
    def save_data():
        updated_data = {
            'Nom': entry_nom.get(),
            'Prénoms': entry_prenoms.get(),
            'Date de naissance': entry_date_naissance.get(),
            'Lieu de naissance': entry_lieu_naissance.get(),
            'Sexe': entry_sexe.get(),
            'Taille': entry_taille.get(),
            'Profession': entry_profession.get()
        }
        valid, invalid_fields = validate_data(updated_data)
        if valid:
            store_data(updated_data)
            messagebox.showinfo("Succès", "Les données ont été enregistrées avec succès")
            data_window.destroy()
        else:
            messagebox.showerror("Données invalides", f"Les champs suivants sont invalides : {', '.join(invalid_fields)}")

    data_window = tk.Toplevel(root)
    data_window.title("Données extraites")

    tk.Label(data_window, text="Nom:").grid(row=0, column=0)
    entry_nom = tk.Entry(data_window)
    entry_nom.grid(row=0, column=1)
    entry_nom.insert(0, data['Nom'])

    tk.Label(data_window, text="Prénoms:").grid(row=1, column=0)
    entry_prenoms = tk.Entry(data_window)
    entry_prenoms.grid(row=1, column=1)
    entry_prenoms.insert(0, data['Prénoms'])

    tk.Label(data_window, text="Date de naissance:").grid(row=2, column=0)
    entry_date_naissance = tk.Entry(data_window)
    entry_date_naissance.grid(row=2, column=1)
    entry_date_naissance.insert(0, data['Date de naissance'])

    tk.Label(data_window, text="Lieu de naissance:").grid(row=3, column=0)
    entry_lieu_naissance = tk.Entry(data_window)
    entry_lieu_naissance.grid(row=3, column=1)
    entry_lieu_naissance.insert(0, data['Lieu de naissance'])

    tk.Label(data_window, text="Sexe:").grid(row=4, column=0)
    entry_sexe = tk.Entry(data_window)
    entry_sexe.grid(row=4, column=1)
    entry_sexe.insert(0, data['Sexe'])

    tk.Label(data_window, text="Taille:").grid(row=5, column=0)
    entry_taille = tk.Entry(data_window)
    entry_taille.grid(row=5, column=1)
    entry_taille.insert(0, data['Taille'])

    tk.Label(data_window, text="Profession:").grid(row=6, column=0)
    entry_profession = tk.Entry(data_window)
    entry_profession.grid(row=6, column=1)
    entry_profession.insert(0, data['Profession'])

    tk.Button(data_window, text="Sauvegarder", command=save_data).grid(row=7, column=0, columnspan=2)

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



#Réaliser par HAMDANE ALLAMINE MOUSSA   


#brouillon de système d'analyse de donnée
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
