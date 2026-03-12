# 🖼️ Panoramic Image Stitcher

> Assemblage automatique d'images en panorama avec Python et OpenCV — détection de points clés SIFT, homographie et recadrage intelligent.

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-5C3EE8?style=flat&logo=opencv&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-1.x-013243?style=flat&logo=numpy&logoColor=white)

---

## 📌 Description

Ce projet implémente un pipeline complet d'assemblage d'images panoramiques à partir de plusieurs photos prises avec un décalage horizontal. Il repose sur les algorithmes classiques de vision par ordinateur : détection de points d'intérêt **SIFT**, mise en correspondance par **BFMatcher**, estimation de l'**homographie** via RANSAC, et fusion progressive des images.

---

## 📁 Fichiers du projet

| Fichier | Description |
|---|---|
| `sitch.py` | Assemblage de deux images (version de base) |
| `sitichou.py` | Assemblage progressif de N images (version améliorée) |
| `homography.py` | Projection interactive d'une image source sur 4 points choisis par l'utilisateur |

---

## ⚙️ Comment ça marche

1. **Détection de points clés** — SIFT détecte les points d'intérêt dans chaque image
2. **Mise en correspondance** — BFMatcher + ratio test de Lowe pour filtrer les bons matches
3. **Homographie** — `cv2.findHomography` avec RANSAC estime la transformation entre les deux images
4. **Warping** — `cv2.warpPerspective` projette l'image dans le référentiel de l'autre
5. **Fusion & recadrage** — Les images sont fusionnées et les bords noirs sont automatiquement supprimés

---

## 🚀 Installation

```bash
# Cloner le repo
git clone https://github.com/tarekflb/Panoramique-image-assembleur.git
cd Panoramique-image-assembleur

# Installer les dépendances
pip install opencv-contrib-python numpy
```

> ⚠️ Utiliser `opencv-contrib-python` (et non `opencv-python`) pour accéder à SIFT.

---

## ▶️ Utilisation

### Assemblage de 2 images
```bash
python sitch.py
# Modifier les chemins image4.jpg / image5.jpg dans le script
```

### Assemblage progressif de N images
```bash
python sitichou.py
# Modifier les chemins image0.jpg, image1.jpg, image2.jpg dans le script
```

### Projection homographique interactive
```bash
python homography.py image_source.jpg image_destination.jpg
# Cliquer sur 4 points dans l'image destination pour définir la zone de projection
```

---

## 📸 Exemple de résultat

```
image0.jpg + image1.jpg + image2.jpg  ──►  panorama.jpg
```

Le résultat final est sauvegardé automatiquement sous `panorama.jpg`.

---

## 📚 Références

- [PyLessons — OpenCV Image Stitching](https://pylessons.com/OpenCV-image-stiching-continue)
- [OpenCV Documentation — Feature Detection](https://docs.opencv.org/4.x/db/d27/tutorial_py_table_of_contents_feature2d.html)
- [NumPy Array Slicing — W3Schools](https://www.w3schools.com/python/numpy/numpy_array_slicing.asp)
