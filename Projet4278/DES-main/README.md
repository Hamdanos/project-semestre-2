# **MANUEL D’UTILISATION DES**

Un prototype de chiffrement symétrique Data Encryption Standard (DES) en mode ECB permettant de chiffrer et de déchiffrer un fichier texte en hexadécimal. Il compte cinq modules à savoir : main, des, msg, file et binary ainsi que le makefile. À part le module main, chacun a un fichier d’en-tête (.h) et un fichier source (.c).

## **Description des modules**

- `main.c` est le fichier principal ;
- `des.c` contient l’algorithme de DES ;
- `des.h` les prototypes des fonctions de l’algorithme DES ;
- `file.c` utilitaire permettant de gérer les fichiers à manipuler `plaintext.txt` et `key.txt` ;
- `file.h` prototypes des fonctions contenues dans le fichier `file.c` ;
- `msg.c` génération des différents messages de trace d’exécution de DES ;
- `msg.h` prototypes des fonctions contenues dans le fichier `msg.c` ;
- `binaryUtil.c` pour la conversion entre binaire et hexadécimal ;
- `binaryUtil.h` prototypes des fonctions contenues dans le fichier `binaryUtil.c` ;
- `Makefile` contient les commandes de compilation.

## **Configuration Minimale**

- OS : Windows ;
- GCC : version 10 ou supérieure ;
- Utilitaire `mingw32-make` ;
- `text.txt` en hexadécimal contenant le texte à chiffrer ;
- `key.txt` en hexadécimal pour la clé à 16 caractères.

## **Compilation**

- Cloner le projet depuis "https://github.com/MOUCTAR-MOHAMADOU/DES.git" ;
- Dézipper `des.zip` ;
- Accéder au dossier contenant le code source depuis l'invite de commande ;
- Exécuter la commande `mingw32-make` pour compiler ;
- Obtention d’un exécutable `des.exe` après réussite de la compilation.

## **Exécution**

- Créez les fichiers `text.txt` et `key.txt` et insérez-y le texte et la clé respectivement.
  - Exemple de contenu pour `text.txt` : "0123456789ABCDEF"
  - Exemple de contenu pour `key.txt` : "133457799BBCDFF1"

- Ouvrez le dossier `des` depuis l'invite de commande.

- Lancez l’exécutable en utilisant la commande suivante :
  ```shell
  des.exe
  ```
  
- Suivez les instructions affichées dans la console.

- Une fois l'exécution terminée, vous obtiendrez les fichiers suivants dans le dossier :
  - `desc.txt` : un fichier de trace.
  - `text.txt_cypherText.txt` : contenant le texte chiffré, par exemple "85e813540f0ab405".
  - `text.txt_cypherText.txt_plainText.txt` : contenant le déchiffrement de `text.txt_cypherText.txt`, qui devrait donner "0123456789ABCDEF".

Assurez-vous de suivre attentivement les étapes et de respecter les formats attendus pour les fichiers `text.txt` et `key.txt` afin d'obtenir les résultats escomptés.

