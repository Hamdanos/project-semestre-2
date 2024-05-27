import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import spacy
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
text = pytesseract.image_to_string(img, lang='fra')  

# Afficher le texte extrait
print("Texte extrait :\n", text)

# Charger le modèle français de SpaCy
nlp = spacy.load('fr_core_news_sm')

# Traiter le texte avec SpaCy
doc = nlp(text)

# Extraire les entités nommées
entities = {ent.label_: ent.text for ent in doc.ents}

# Afficher les entités extraites
print("Entités extraites :\n", entities)

# Organiser les informations extraites
def extract_information(entities, text):
    info = {}
    info['Nom'] = entities.get('PER', 'N/A')  
    info['Prénom'] = entities.get('PER', 'N/A')
    info['Sexe'] = entities.get('MISC', 'N/A')  
    info['Date de Naissance'] = entities.get('DATE', 'N/A')
    info['Lieu de Naissance'] = entities.get('LOC', 'N/A')  
    info['Numéro de Carte'] = re.search(r'\b\d{9}\b', text).group(0) if re.search(r'\b\d{9}\b', text) else 'N/A'
    info['Date d\'Expiration'] = entities.get('DATE', 'N/A')
    return info

infos = extract_information(entities, text)

# Afficher les informations organisées
print("Informations organisées :\n", infos)
