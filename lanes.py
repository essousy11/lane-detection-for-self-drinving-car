# Importer les bibliothèques nécessaires
import cv2
import numpy as np  # Charge de faire les calculs matriciels
import matplotlib.pyplot as plt  # Traitement graphique
def make_coordinates(image, line_parameters):
    try:
        slope, intercept = line_parameters
        y1 = image.shape[0]
        y2 = int(y1 * (3/5))
        x1 = int((y1 - intercept) / slope)
        x2 = int((y2 - intercept) / slope)
        return np.array([x1, y1, x2, y2])
    except TypeError:
        # Gérer le cas où le déballage échoue
        return np.array([0, 0, 0, 0])
'''Make_coordinates description
Entrées:
    - Image
    - Paramètres de ligne (pente, ordonnée à l'origine)

Sortie:
    - Coordonnées de la ligne [x1, y1, x2, y2]

Étapes:
1. Déballage des paramètres de ligne (pente, ordonnée à l'origine).
2. Obtention de la hauteur de l'image (y1 = image.shape[0]).
3. Calcul de y2 comme étant 3/5 de la hauteur de l'image (y2 = int(y1 * (3/5))).
4. Calcul de x1 en utilisant l'équation de la ligne (x1 = int((y1 - intercept) / slope)).
5. Calcul de x2 en utilisant l'équation de la ligne (x2 = int((y2 - intercept) / slope)).
6. Retour des coordonnées de la ligne [x1, y1, x2, y2].
7. Gestion d'une éventuelle exception de type (TypeError) lors du déballage.
   - Retour des coordonnées [0, 0, 0, 0] en cas d'erreur.

'''

def average_slope_intercept(image, lines):
    left_fit = []
    right_fit = []
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        #Cette ligne extrait les coordonnées des points (x1, y1) et (x2, y2) de chaque ligne.
        #La fonction reshape(4) est utilisée pour s'assurer que la ligne a bien quatre coordonnées.
        try:
            parameters = np.polyfit((x1, x2), (y1, y2), 1)#définir la pente et y-intercept [(p1,yi1),(p2,yi2)....]
            slope = parameters[0]
            intercept = parameters[1]
            if slope < 0:
                left_fit.append((slope, intercept))
            else:
                right_fit.append((slope, intercept))
        except TypeError:
            # Gérer le cas où np.polyfit échoue
            pass

    left_fit_average = np.average(left_fit, axis=0)
    right_fit_average = np.average(right_fit, axis=0)
    left_line = make_coordinates(image, left_fit_average)
    right_line = make_coordinates(image, right_fit_average)
    return np.array([left_line, right_line])
'''Average_slope_intercept
Entrées:
    - Image
    - Lignes détectées

Sortie:
    - Coordonnées moyennes des lignes gauche et droite [left_line, right_line]

Étapes:
1. Initialisation des listes `left_fit` et `right_fit` pour stocker les paramètres des lignes gauche et droite.
2. Pour chaque ligne détectée dans l'ensemble `lines` :
   a. Déballage des coordonnées (x1, y1, x2, y2).
   b. Calcul des paramètres de la ligne (pente et ordonnée à l'origine) en utilisant np.polyfit.
   c. Ajout des paramètres aux listes `left_fit` ou `right_fit` en fonction de la pente.
   d. Gestion d'une éventuelle exception de type (TypeError) lors du déballage.

3. Calcul de la moyenne des paramètres pour les lignes gauche et droite.
   - `left_fit_average` est la moyenne des paramètres des lignes gauches.
   - `right_fit_average` est la moyenne des paramètres des lignes droites.

4. Création des coordonnées des lignes gauche et droite moyennes en utilisant la fonction `make_coordinates`.
   - `left_line` est le résultat de `make_coordinates` avec les paramètres moyens pour les lignes gauches.
   - `right_line` est le résultat de `make_coordinates` avec les paramètres moyens pour les lignes droites.

5. Retour des coordonnées moyennes des lignes gauche et droite sous la forme d'un tableau numpy.


'''
# Charger l'image
image = cv2.imread('test_image.jpg')

# Fonction pour détecter les contours de l'image
def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convertir l'image en niveaux de gris
    blur = cv2.GaussianBlur(gray, (5, 5), 0)  # Appliquer un flou gaussien pour réduire le bruit
    canny = cv2.Canny(blur, 50, 150)  # Appliquer l'algorithme Canny pour détecter les contours
    return canny
    # Fonction pour afficher les lignes détectées sur une image
def display_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for x1, y1, x2, y2 in lines :
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)  # Dessiner une ligne sur l'image
    return line_image
    '''Display_lines_description
    Entrées:
    - Image d'origine
    - Coordonnées des lignes à afficher

Sortie:
    - Image contenant les lignes dessinées (line_image)

Étapes:
1. Initialisation d'une image noire (`line_image`) avec la même forme que l'image d'origine.

2. Si des lignes sont fournies (non nulles) :
   a. Pour chaque ensemble de coordonnées de ligne (x1, y1, x2, y2) dans l'ensemble `lines` :
      i. Dessiner une ligne sur l'image `line_image` entre les points (x1, y1) et (x2, y2).
      ii. La couleur de la ligne est définie comme (255, 0, 0) (bleu) avec une épaisseur de 10 pixels.

3. Retourner l'image résultante `line_image` contenant les lignes dessinées.


    '''

# Fonction pour définir une région d'intérêt dans l'image
def region_of_interest(image):
    height = image.shape[0]
    polygons = np.array([[(200, height), (1100, height), (550, 250)]])  # Coordonnées des points définissant la région
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygons, 255)  # Remplir la région avec du blanc (255)
    masked_image = cv2.bitwise_and(image, mask)  # Appliquer le masque à l'image
    return masked_image
'''
Entrée:
    - Image d'origine

Sortie:
    - Image avec une région d'intérêt extraite (masked_image)

Étapes :
1. Obtention de la hauteur de l'image (`height`).
2. Définition des coordonnées des points définissant un polygone représentant la région d'intérêt (`polygons`).
   - Les points sont (200, height), (1100, height), et (550, 250).

3. Initialisation d'une image noire (`mask`) avec la même forme que l'image d'origine.

4. Remplissage de la région définie par le polygone avec du blanc (255) sur l'image `mask` en utilisant la fonction `cv2.fillPoly`.

5. Application du masque `mask` à l'image d'origine en utilisant un "ET logique" (`cv2.bitwise_and`).
   - Cela conserve uniquement les pixels de l'image d'origine là où le masque est blanc.

6. Retour de l'image résultante (`masked_image`) avec la région d'intérêt extraite.


'''
# Copier l'image pour éviter de modifier l'original
lane_image = np.copy(image)
#

#Main 
cap = cv2.VideoCapture("test2.mp4")
while (cap.isOpened()):
    _, frame = cap.read()
    # Appliquer la détection de bord (Canny)
    canny_image = canny(frame)
    # Appliquer la région d'intérêt
    cropped_image = region_of_interest(canny_image)
    # Appliquer la transformation de Hough pour détecter les lignes
    lines = cv2.HoughLinesP(cropped_image, 2, np.pi / 180, 100, np.array([]), minLineLength=40, maxLineGap=5)
    averaged_lines = average_slope_intercept(frame , lines)
    # Afficher les lignes détectées sur l'image d'origine
    line_image = display_lines(frame, averaged_lines)
    #
    combo_image= cv2.addWeighted( frame, 0.8 , line_image , 1 , 1 )
    #

     # Afficher l'image résultante
    cv2.imshow("result",combo_image )
    # Attendre un événement clé et fermer la fenêtre
    if cv2.waitKey(1) & 0xFF == ord ('q'):
        break
cap.release()
cv2.destroyAllWindows()
'''
+---------------------------+
|  Ouvrir la vidéo          |
|  ("test2.mp4")            |
+-------------+-------------+
              |
              v
+---------------------------+
| Boucle principale          |
| de traitement des frames  |
+-------------+-------------+
              |
              v
+---------------------------+
| Lecture de la frame       |
+-------------+-------------+
              |
              v
+---------------------------+
| Détection de bord (Canny) |
+-------------+-------------+
              |
              v
+---------------------------+
| Application de la région  |
| d'intérêt                  |
+-------------+-------------+
              |
              v
+---------------------------+
| Transformation de Hough   |
| pour détecter les lignes  |
+-------------+-------------+
              |
              v
+---------------------------+
| Calcul des lignes moyennes|
+-------------+-------------+
              |
              v
+---------------------------+
| Affichage des lignes sur  |
| l'image d'origine         |
+-------------+-------------+
              |
              v
+---------------------------+
| Combinaison des images     |
| d'origine et avec les     |
| lignes détectées           |
+-------------+-------------+
              |
              v
+---------------------------+
| Affichage de l'image       |
| résultante                |
+-------------+-------------+
              |
              v
+---------------------------+
| Attente d'un événement    |
| clé et fermeture de la     |
| fenêtre si 'q' est pressé  |
+-------------+-------------+
              |
              v
+---------------------------+
| Libération de la capture  |
| vidéo et fermeture des     |
| fenêtres                  |
+---------------------------+

'''
