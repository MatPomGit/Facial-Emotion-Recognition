# Instrukcja Instalacji / Installation Guide

## 🇵🇱 Polski

### Wymagania systemowe

- Python 3.7 lub nowszy
- pip (menedżer pakietów Python)
- Git
- Kamera internetowa (opcjonalnie, dla trybu live)
- ~500MB wolnego miejsca na dysku

### Krok 1: Sklonuj repozytorium

```bash
git clone https://github.com/MatPomGit/Facial-Emotion-Recognition.git
cd Facial-Emotion-Recognition
```

### Krok 2: Utwórz środowisko wirtualne (zalecane)

#### Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux/Mac:
```bash
python3 -m venv venv
source venv/bin/activate
```

### Krok 3: Zainstaluj zależności

```bash
pip install -r requirements.txt
```

### Krok 4: Przygotuj zbiór danych

1. Pobierz zbiór danych z emocjami (np. FER-2013)
2. Zorganizuj pliki w strukturze:
```
dataset/
  train/
    angry/
      image1.jpg
      image2.jpg
    happy/
      image1.jpg
      image2.jpg
    ... (pozostałe emocje)
```

### Krok 5: Przygotuj dane treningowe

```bash
cd modules/mediapipe
python dataset_prepare.py
cd ../..
```

### Krok 6: Uruchom aplikację

```bash
python main.py
```

Naciśnij `q` aby zakończyć program.

### Rozwiązywanie problemów instalacji

#### Problem: "ModuleNotFoundError: No module named 'cv2'"
**Rozwiązanie:**
```bash
pip install opencv-python
```

#### Problem: "ModuleNotFoundError: No module named 'mediapipe'"
**Rozwiązanie:**
```bash
pip install mediapipe
```

#### Problem: Błąd z kamerą
**Rozwiązanie:**
1. Sprawdź czy kamera jest podłączona
2. W pliku `main.py` zmień `cv2.VideoCapture(0)` na `cv2.VideoCapture(1)` (inna kamera)
3. Lub ustaw `image_mode = True` i przetestuj na zdjęciach

---

## 🇬🇧 English

### System Requirements

- Python 3.7 or newer
- pip (Python package manager)
- Git
- Webcam (optional, for live mode)
- ~500MB free disk space

### Step 1: Clone the repository

```bash
git clone https://github.com/MatPomGit/Facial-Emotion-Recognition.git
cd Facial-Emotion-Recognition
```

### Step 2: Create a virtual environment (recommended)

#### Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux/Mac:
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Prepare dataset

1. Download an emotion dataset (e.g., FER-2013)
2. Organize files in this structure:
```
dataset/
  train/
    angry/
      image1.jpg
      image2.jpg
    happy/
      image1.jpg
      image2.jpg
    ... (other emotions)
```

### Step 5: Prepare training data

```bash
cd modules/mediapipe
python dataset_prepare.py
cd ../..
```

### Step 6: Run the application

```bash
python main.py
```

Press `q` to quit the program.

### Troubleshooting Installation

#### Issue: "ModuleNotFoundError: No module named 'cv2'"
**Solution:**
```bash
pip install opencv-python
```

#### Issue: "ModuleNotFoundError: No module named 'mediapipe'"
**Solution:**
```bash
pip install mediapipe
```

#### Issue: Camera error
**Solution:**
1. Check if camera is connected
2. In `main.py` change `cv2.VideoCapture(0)` to `cv2.VideoCapture(1)` (different camera)
3. Or set `image_mode = True` and test with images
