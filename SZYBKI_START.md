# Szybki Start / Quick Start

## 🇵🇱 5 minut do pierwszego uruchomienia

### 1. Pobierz projekt (30 sekund)

```bash
git clone https://github.com/MatPomGit/Facial-Emotion-Recognition.git
cd Facial-Emotion-Recognition
```

### 2. Zainstaluj biblioteki (2-3 minuty)

```bash
pip install -r requirements.txt
```

Czekaj aż wszystkie pakiety się zainstalują...

### 3. Uruchom program (natychmiast)

```bash
python main.py
```

**Gotowe!** 🎉

- Zobaczysz okno z podglądem kamery
- Niebieskie kropki oznaczają wykrytą twarz
- W terminalu zobaczysz przewidywane emocje
- Naciśnij `q` aby zakończyć

---

## ⚠️ Problemy?

### "ModuleNotFoundError: No module named 'cv2'"

```bash
pip install opencv-python
```

### "No module named 'mediapipe'"

```bash
pip install mediapipe
```

### Kamera się nie uruchamia

W pliku `main.py` zmień linię 39:
```python
cap = cv2.VideoCapture(0)  # Zmień 0 na 1 lub 2
```

### Chcę przetestować na zdjęciu zamiast kamery

W pliku `main.py` zmień linię 28:
```python
image_mode = True  # Było False
```

I w linii 34 podaj ścieżkę do swojego zdjęcia:
```python
img = cv2.imread('sciezka/do/twojego/zdjecia.jpg')
```

---

## 🎯 Co dalej?

### Krok 1: Przeczytaj dokumentację
- [PRZEWODNIK_DLA_STUDENTA.md](PRZEWODNIK_DLA_STUDENTA.md) - Jeśli uczysz się ML

### Krok 2: Eksperymentuj
Spróbuj zmienić w `main.py`:
- `kernel='rbf'` na `kernel='poly'` (linia 58)
- `samples_limit=3000` na inną wartość (linia 58)
- `fx=1, fy=1` na `fx=0.5, fy=0.5` (linia 71) - szybsze działanie

### Krok 3: Dodaj własne dane
1. Utwórz folder `dataset/train/nazwa_emocji/`
2. Dodaj tam zdjęcia
3. Uruchom:
   ```bash
   cd modules/mediapipe
   python dataset_prepare.py
   ```

---

## 🇬🇧 English - 5 minutes to first run

### 1. Download project (30 seconds)

```bash
git clone https://github.com/MatPomGit/Facial-Emotion-Recognition.git
cd Facial-Emotion-Recognition
```

### 2. Install libraries (2-3 minutes)

```bash
pip install -r requirements.txt
```

Wait for all packages to install...

### 3. Run the program (immediately)

```bash
python main.py
```

**Done!** 🎉

- You'll see a camera preview window
- Blue dots indicate detected face
- Terminal shows predicted emotions
- Press `q` to quit

---

## 📊 Oczekiwane wyniki / Expected Results

**FPS (klatki na sekundę):**
- Szybki komputer: 25-30 FPS
- Średni komputer: 15-20 FPS
- Wolny komputer: 8-15 FPS

**Dokładność:**
- Happy (radość): ~80%
- Surprise (zaskoczenie): ~70%
- Sad (smutek): ~65%
- Neutral (neutralność): ~60%
- Angry (złość): ~60%
- Fear (strach): ~55%
- Disgust (obrzydzenie): ~50%

**Uwaga:** Dokładność zależy od jakości danych treningowych!

---

## 🔍 Podstawowe komendy

### Sprawdź wersję Pythona
```bash
python --version
```
Potrzebujesz: Python 3.7+

### Sprawdź zainstalowane pakiety
```bash
pip list
```

### Zaktualizuj pip
```bash
pip install --upgrade pip
```

### Utwórz środowisko wirtualne (zalecane)
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# lub
venv\Scripts\activate  # Windows
```

---

## 💡 Wskazówki

1. **Oświetlenie ma znaczenie** - Upewnij się, że twarz jest dobrze oświetlona
2. **Patrz prosto w kamerę** - Lepsze wykrywanie przy twarzy en face
3. **Stabilna pozycja** - Nie ruszaj się zbyt szybko
4. **Wyraźne emocje** - Subtelne ekspresje mogą być trudniejsze do wykrycia

---

**Potrzebujesz więcej pomocy?**
- Zobacz [INSTALACJA.md](INSTALACJA.md) - szczegółowa instrukcja
- Zobacz [PRZEWODNIK_DLA_STUDENTA.md](PRZEWODNIK_DLA_STUDENTA.md) - dla początkujących
- Utwórz [Issue](https://github.com/MatPomGit/Facial-Emotion-Recognition/issues) - zadaj pytanie
