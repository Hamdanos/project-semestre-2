import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import re

# Chemin vers l'image de la carte d'identité
image_path = "E:/Projet4288/image/cni.jpg"

# Charger l'image
img = Image.open(image_path)

# Prétraitement de l'image
img = img.convert('L')  
img = img.filter(ImageFilter.MedianFilter())  
enhancer = ImageEnhance.Contrast(img)
img = enhancer.enhance(2)  
img = img.point(lambda p: p > 128 and 255)  

# Chemin vers l'exécutable tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Appliquer l'OCR
text = pytesseract.image_to_string(img, lang='eng')

# Afficher le texte extrait
print("Texte extrait :\n", text)

# Analyser et organiser les informations extraites
def extract_information(text):
    info = {}
    match_nom = re.search(r'Nom:(.*)', text)
    if match_nom:
        info['Nom'] = match_nom.group(1).strip()
    else:
        info['Nom'] = "N/A"
    
    match_prenom = re.search(r'Prénom:(.*)', text)
    if match_prenom:
        info['Prénom'] = match_prenom.group(1).strip()
    else:
        info['Prénom'] = "N/A"
    
    match_sexe = re.search(r'Sexe:(.*)', text)
    if match_sexe:
        info['Sexe'] = match_sexe.group(1).strip()
    else:
        info['Sexe'] = "N/A"
    
    match_date_naissance = re.search(r'Date de Naissance:(.*)', text)
    if match_date_naissance:
        info['Date de Naissance'] = match_date_naissance.group(1).strip()
    else:
        info['Date de Naissance'] = "N/A"
    
    match_lieu_naissance = re.search(r'Lieu de Naissance:(.*)', text)
    if match_lieu_naissance:
        info['Lieu de Naissance'] = match_lieu_naissance.group(1).strip()
    else:
        info['Lieu de Naissance'] = "N/A"
    
    match_numero_carte = re.search(r'Numéro de Carte:(.*)', text)
    if match_numero_carte:
        info['Numéro de Carte'] = match_numero_carte.group(1).strip()
    else:
        info['Numéro de Carte'] = "N/A"
    
    match_date_expiration = re.search(r'Date d\'Expiration:(.*)', text)
    if match_date_expiration:
        info['Date d\'Expiration'] = match_date_expiration.group(1).strip()
    else:
        info['Date d\'Expiration'] = "N/A"
    
    return info

infos = extract_information(text)

# Afficher les informations organisées
print("Informations organisées :\n", infos)