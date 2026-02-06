# Architektura Systemu / System Architecture

## 🇵🇱 Struktura Projektu

```
Facial-Emotion-Recognition/
│
├── main.py                          # Główny punkt wejścia aplikacji
├── requirements.txt                 # Lista zależności
├── setup.py                         # Konfiguracja instalacji pakietu
├── LICENSE                          # Licencja MIT
├── README.md                        # Dokumentacja główna
├── PRZEWODNIK_DLA_STUDENTA.md      # Przewodnik dla studentów
├── CONTRIBUTING.md                  # Przewodnik dla kontrybutorów
├── CODE_OF_CONDUCT.md              # Kodeks postępowania
├── CHANGELOG.md                     # Historia zmian
├── INSTALACJA.md                    # Instrukcja instalacji
├── ARCHITEKTURA.md                  # Ten plik
│
├── .github/                         # Konfiguracja GitHub
│   ├── workflows/                   # GitHub Actions
│   │   └── python-app.yml          # CI/CD pipeline
│   ├── ISSUE_TEMPLATE/             # Szablony issues
│   │   ├── bug_report.md
│   │   ├── feature_request.md
│   │   └── question.md
│   └── PULL_REQUEST_TEMPLATE.md    # Szablon PR
│
├── modules/                         # Moduły systemu
│   ├── __init__.py
│   ├── fps.py                      # Pomiar wydajności (FPS)
│   ├── svm.py                      # Algorytm uczenia maszynowego
│   │
│   ├── mediapipe/                  # Moduł MediaPipe (zalecany)
│   │   ├── __init__.py
│   │   ├── dataset_prepare.py      # Przygotowanie danych
│   │   ├── mediapipe_FaceLandmarks.py  # Wykrywanie twarzy
│   │   └── ratio_calc.py           # Obliczanie proporcji
│   │
│   └── dlib/                       # Moduł Dlib (alternatywny)
│       ├── __init__.py
│       ├── dataset_prepare.py      # Przygotowanie danych
│       ├── dlib_FaceLandmarks.py   # Wykrywanie twarzy
│       └── ratio_calc.py           # Obliczanie proporcji
│
├── dataset/                         # Dane treningowe i testowe
│   ├── train/                      # Zbiór treningowy
│   │   ├── angry/
│   │   ├── disgust/
│   │   ├── fear/
│   │   ├── happy/
│   │   ├── neutral/
│   │   ├── sad/
│   │   └── surprise/
│   └── *.csv                       # Przetworzone dane
│
└── test/                            # Eksperymenty i testy
    ├── README.md
    ├── Face-Detection/
    └── SVM.ipynb
```

## 📊 Przepływ Danych

### 1. Etap Przygotowania (Offline)

```
Zdjęcia → dataset_prepare.py → Wykrywanie twarzy → Ekstrakcja punktów
                                                           ↓
                                                   Obliczanie proporcji
                                                           ↓
                                                       CSV file
```

**Pliki zaangażowane:**
- `modules/mediapipe/dataset_prepare.py`
- `modules/mediapipe/mediapipe_FaceLandmarks.py`
- `modules/mediapipe/ratio_calc.py`

**Wynik:** Plik CSV z 8 proporcjami twarzy + etykieta emocji

### 2. Etap Trenowania (Offline)

```
CSV file → modules/svm.py → Balansowanie danych → Trenowanie SVM → Model
```

**Parametry kluczowe:**
- `kernel`: typ kernela SVM ('rbf', 'poly', 'linear')
- `samples_limit`: maksymalna liczba próbek na klasę
- `scale`: czy normalizować dane

**Wynik:** Wytrenowany model SVM w pamięci

### 3. Etap Rozpoznawania (Real-time)

```
Kamera → Klatka wideo → Wykrycie twarzy → Oblicz proporcje → SVM → Emocja
    ↑                                                               ↓
    └──────────────────────────── Wyświetl wynik ─────────────────┘
```

**Plik:** `main.py`

**Częstotliwość:** 15-30 FPS (w zależności od sprzętu)

## 🧩 Komponenty Systemu

### 1. Face Detection (Wykrywanie Twarzy)

**Odpowiedzialność:** Znajdowanie twarzy na obrazie i ekstrakcja punktów charakterystycznych

**Implementacje:**
- **MediaPipe** (zalecane): 468 punktów, wysoka dokładność
- **Dlib**: 68 punktów, lżejsze obliczeniowo

**Klasa:** `FaceDetector`

**Główne metody:**
- `detect(frame)`: Zwraca listę wykrytych twarzy z punktami

### 2. Ratio Calculator (Kalkulator Proporcji)

**Odpowiedzialność:** Obliczanie 8 kluczowych proporcji twarzy

**Proporcje (a1-a8):**
- a1: Szerokość ust / Szerokość twarzy
- a2: Wysokość ust / Wysokość twarzy
- a3: Otwarcie lewego oka / Szerokość twarzy
- a4: Otwarcie prawego oka / Szerokość twarzy
- a5: Wysokość lewej brwi / Wysokość twarzy
- a6: Wysokość prawej brwi / Wysokość twarzy
- a7: Kąt ust (lewy)
- a8: Kąt ust (prawy)

**Klasa:** `RatioCalculator`

**Główne metody:**
- `result()`: Zwraca listę 8 wartości proporcji

### 3. SVM (Support Vector Machines)

**Odpowiedzialność:** Trenowanie modelu i przewidywanie emocji

**Algorytm:** Support Vector Regression (SVR)

**Klasa:** `SVM`

**Główne metody:**
- `train(label, scale, samples_limit, kernel)`: Trenuje model
- `predict(data)`: Przewiduje emocję dla danych proporcji

### 4. FPS Counter

**Odpowiedzialność:** Pomiar wydajności systemu

**Klasa:** `FPS`

**Główne metody:**
- `start()`: Oblicza i zwraca aktualny FPS

## 🔄 Cykl Życia Aplikacji

1. **Inicjalizacja (start programu)**
   ```python
   face_model = FaceDetector()
   emotion_model = SVM('dataset/mediapipe_train_emotions.csv', labels)
   emotion_model.train('emotions', scale=False, samples_limit=3000, kernel='rbf')
   ```

2. **Główna pętla (co klatkę)**
   ```python
   while True:
       frame = cap.read()              # Pobierz klatkę
       faces = face_model.detect(frame)  # Wykryj twarze
       
       for face in faces:
           ratio = RatioCalculator(face)  # Oblicz proporcje
           emotion = emotion_model.predict(ratio.result())  # Przewiduj emocję
           # Wyświetl wynik
   ```

3. **Zakończenie (klawisz 'q')**
   ```python
   cap.release()
   cv2.destroyAllWindows()
   ```

## 🎯 Decyzje Architektoniczne

### Dlaczego SVR zamiast SVC?

**Wybór:** Support Vector Regression (SVR)

**Powody:**
1. Emocje są ciągłe, nie dyskretne
2. SVR pozwala wykrywać stany pośrednie (np. "między radością a zaskoczeniem")
3. Wartości zmiennoprzecinkowe dają więcej informacji niż etykiety kategoryczne

### Dlaczego 8 proporcji zamiast surowych punktów?

**Wybór:** 8 obliczonych proporcji

**Alternatywa:** 468 punktów × 3 współrzędne = 1404 wartości

**Powody:**
1. **Redukcja wymiarowości:** 1404 → 8 wartości
2. **Niezależność od skali:** Proporcje są niezmienne względem odległości od kamery
3. **Szybsze trenowanie:** Mniej cech = szybszy model
4. **Lepsze uogólnienie:** Mniej ryzyka przeuczenia

### Dlaczego MediaPipe jest domyślnym wyborem?

**Wybór:** MediaPipe jako główna metoda wykrywania

**Powody:**
1. Nowoczesne podejście (deep learning)
2. Wysoka dokładność
3. Dobra wydajność (optymalizowane przez Google)
4. Aktywnie wspierane i rozwijane
5. Działa dobrze w różnych warunkach oświetleniowych

## 🔧 Możliwości Rozszerzenia

### 1. Dodanie nowych emocji

**Gdzie:** `main.py`, linia z `labels`

```python
labels = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise', 'contempt']
```

**Wymagane zmiany:**
- Dodać folder z nowymi danymi w `dataset/train/`
- Przetrainować model

### 2. Zmiana metody wykrywania twarzy

**Gdzie:** `main.py`, linie z importami

```python
# Z MediaPipe na Dlib:
from modules.dlib.dlib_FaceLandmarks import FaceDetector
from modules.dlib.ratio_calc import RatioCalculator
```

### 3. Dodanie zapisu wyników

```python
# Po przewidywaniu:
with open('results.csv', 'a') as f:
    f.write(f'{timestamp},{emotion},{confidence}\n')
```

### 4. Integracja z innymi algorytmami ML

**Możliwości:**
- Random Forest
- Neural Networks (TensorFlow/PyTorch)
- XGBoost

**Gdzie:** Zastąpić `modules/svm.py` nową implementacją

## 📈 Metryki Wydajności

**Typowe wartości:**

- **FPS:** 15-30 (w zależności od sprzętu)
- **Dokładność modelu:** 60-80% (zależy od jakości danych)
- **Czas trenowania:** 10-60 sekund (3000 próbek na emocję)
- **Użycie RAM:** ~500MB podczas działania

## 🔐 Bezpieczeństwo i Prywatność

- **Brak przechowywania:** System nie zapisuje zdjęć z kamery
- **Local-only:** Wszystkie obliczenia lokalne, brak wysyłania danych
- **Open Source:** Kod źródłowy dostępny do audytu

---

## 🇬🇧 English Summary

This document describes the complete architecture of the Facial Emotion Recognition system, including:

- **Project Structure:** File organization and module hierarchy
- **Data Flow:** How data moves through the system from images to predictions
- **Components:** Detailed description of each system component
- **Application Lifecycle:** Initialization, main loop, and shutdown
- **Architectural Decisions:** Why certain technologies and approaches were chosen
- **Extension Points:** How to add new features or modify existing ones
- **Performance Metrics:** Expected system performance

The system follows a modular architecture with clear separation of concerns:
- Face detection (MediaPipe/Dlib)
- Feature extraction (RatioCalculator)
- Classification (SVM)
- Real-time processing (main.py)

All processing is done locally with no data transmission to external servers.
