# Facial-Emotion-Recognition

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![OpenCV](https://img.shields.io/badge/OpenCV-4.5%2B-red)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.8%2B-orange)
![scikit--learn](https://img.shields.io/badge/scikit--learn-1.0%2B-yellow)

System rozpoznawania emocji na twarzy (FER - Facial Expression Recognition)

> **English**: Real-time facial emotion recognition system using MediaPipe for face detection and SVM for emotion classification. Detects 7 basic emotions: angry, disgust, fear, happy, neutral, sad, surprise.
>
> **Polski**: System rozpoznawania emocji na twarzy w czasie rzeczywistym wykorzystujący MediaPipe do wykrywania twarzy i SVM do klasyfikacji emocji. Wykrywa 7 podstawowych emocji: złość, obrzydzenie, strach, radość, neutralność, smutek, zaskoczenie.

## Wprowadzenie dla studentów
Ten projekt to praktyczna implementacja systemu do rozpoznawania emocji na ludzkich twarzach. Jeśli dopiero zaczynasz przygodę z machine learning i computer vision, ten projekt pomoże Ci zrozumieć podstawowe koncepcje:
- Wykrywanie twarzy na obrazie
- Ekstrakcja cech charakterystycznych z twarzy
- Trenowanie modelu uczenia maszynowego
- Predykcja emocji w czasie rzeczywistym

## Modele wykorzystywane w projekcie
(#) oznacza aktualnie używany model

### A. Wykrywanie twarzy na obrazie
Pierwszym krokiem jest zlokalizowanie twarzy na obrazie. Wykorzystujemy do tego następujące metody:

#### Dlib HoG Face Detection
**Co to jest?** Dlib to biblioteka zawierająca algorytm wykrywania twarzy oparty na metodzie HoG (Histogram of Oriented Gradients).

**Zalety:** Model jest stosunkowo szybki i dobrze sprawdza się w podstawowych zastosowaniach.

**Wady:** Jest to starsza technologia. Dokładność nie jest tak dobra jak w nowszych modelach opartych na sieciach neuronowych. Model ma również problemy z wykrywaniem twarzy pod kątem lub w trudnych warunkach oświetleniowych.

#### Mediapipe Deep Learning-based Face Detection (#)
**Co to jest?** Mediapipe to biblioteka od Google wykorzystująca głębokie sieci neuronowe do wykrywania twarzy.

**Zalety:** Bardzo wysoka dokładność, szybkie działanie, świetnie radzi sobie z różnymi kątami i pozycjami twarzy.

**Wady:** Czasami wykrywa bardzo szczegółowe punkty charakterystyczne, co może spowolnić działanie systemu lub być zbędne dla prostszych zastosowań.

**Dlaczego to wybraliśmy?** Ten model jest obecnie używany w projekcie ze względu na lepszą dokładność i nowoczesne podejście.

### B. Rozpoznawanie emocji
Po wykryciu twarzy, system musi określić emocję. Używamy do tego:

#### Support Vector Machines (SVM) (#)
**Co to jest?** SVM to algorytm uczenia maszynowego, który uczy się rozpoznawać wzorce na podstawie przykładowych danych.

**Jak to działa?** System analizuje proporcje twarzy (np. szerokość uśmiechu, otwarcie oczu, pozycję brwi) i na tej podstawie klasyfikuje emocję.

**Rozpoznawane emocje:** angry (złość), disgust (obrzydzenie), fear (strach), happy (radość), neutral (neutralność), sad (smutek), surprise (zaskoczenie)

**Ograniczenia:** Model dobrze radzi sobie z większością emocji, ale ma trudności z rozróżnieniem emocji o podobnych proporcjach twarzy (np. strach i zaskoczenie mogą być czasem mylone).

## Instrukcja krok po kroku

### Krok 1: Przygotowanie zbioru danych z emocjami
**Cel:** Stworzyć plik CSV zawierający proporcje twarzy dla różnych emocji, który posłuży do trenowania modelu.

**Co musisz wiedzieć:**
- Projekt wymaga zbioru danych ze zdjęciami twarzy wyrażających różne emocje
- Zdjęcia powinny być pogrupowane w foldery według emocji (np. `dataset/train/happy/`, `dataset/train/sad/`)
- System automatycznie przetworzy te zdjęcia i wyekstrahuje z nich cechy charakterystyczne

**Dostępne moduły:**
1. **Moduł dlib:** `modules/dlib/`
   - Starszy, ale nadal funkcjonalny system wykrywania punktów charakterystycznych twarzy
   - Używa 68 punktów orientacyjnych na twarzy

2. **Moduł mediapipe:** `modules/mediapipe/` (ZALECANY)
   - Nowszy, bardziej dokładny system
   - Używa 468 punktów orientacyjnych na twarzy

**Pliki w każdym module:**
- `dataset_prepare.py` - Główny skrypt do przetwarzania zdjęć i tworzenia zbioru danych
  * Wczytuje zdjęcia z folderów
  * Wykrywa twarze na każdym zdjęciu
  * Oblicza proporcje charakterystyczne
  * Zapisuje wyniki do pliku CSV

- `mediapipe_FaceLandmarks.py` lub `dlib_FaceLandmarks.py` - Kod odpowiedzialny za wykrywanie twarzy i punktów charakterystycznych

- `ratio_calc.py` - Oblicza proporcje twarzy (np. stosunek szerokości ust do szerokości twarzy)
  * Szczegółowy opis obliczanych proporcji znajduje się w komentarzach w pliku
  * System oblicza 8 różnych proporcji (a1-a8) na podstawie odległości między punktami twarzy

**Wynik:** Plik CSV w folderze `dataset/` (np. `mediapipe_train_emotions.csv`) zawierający:
- Kolumny z wartościami proporcji (8 wartości liczbowych)
- Kolumna z etykietą emocji (angry, happy, sad, itd.)

### Krok 2: Trenowanie modelu rozpoznawania emocji
**Cel:** Nauczyć model SVM rozpoznawać emocje na podstawie proporcji twarzy.

**Główny plik:** `main.py`
- Uruchamia kamerę lub wczytuje zdjęcie
- Ładuje wytrenowany model SVM
- Wykrywa twarze w czasie rzeczywistym
- Przewiduje emocje
- Wyświetla wyniki

**Pomocnicze moduły:**
- `modules/svm.py` - Implementacja algorytmu SVM
  * Wczytuje dane z pliku CSV
  * Trenuje model na podstawie przykładów
  * Dokonuje predykcji emocji dla nowych danych
  
- `modules/fps.py` - Oblicza i wyświetla liczbę klatek na sekundę (FPS)
  * Pomaga monitorować wydajność systemu
  * Im wyższe FPS, tym płynniejsze działanie

**Jak to działa:**
1. Program uruchamia kamerę i pobiera obraz
2. System wykrywa wszystkie twarze na obrazie
3. Dla każdej twarzy oblicza proporcje
4. Model SVM analizuje proporcje i przewiduje emocję
5. Wynik jest wyświetlany na ekranie i w terminalu
6. Proces powtarza się dla każdej klatki wideo

**Wynik:** Okno z podglądem kamery, gdzie widoczne są:
- Wykryte punkty charakterystyczne twarzy (niebieskie kropki)
- Numer rozpoznanej twarzy
- FPS w lewym górnym rogu
- W terminalu: przewidywane wartości liczbowe i nazwy emocji

## 🚀 Szybki start / Quick Start

### Instalacja / Installation

```bash
# Sklonuj repozytorium / Clone the repository
git clone https://github.com/MatPomGit/Facial-Emotion-Recognition.git
cd Facial-Emotion-Recognition

# Zainstaluj zależności / Install dependencies
pip install -r requirements.txt

# Lub zainstaluj jako pakiet / Or install as package
pip install -e .
```

### Pierwsze uruchomienie / First Run

```bash
# Uruchom program z domyślną kamerą / Run with default camera
python main.py
```

Naciśnij `q` aby zakończyć / Press `q` to quit

## 📋 Wymagania techniczne / Requirements

- Python 3.7+
- Biblioteki / Libraries:
  - OpenCV (opencv-python) >= 4.5.0
  - MediaPipe >= 0.8.10
  - scikit-learn >= 1.0.0
  - pandas >= 1.3.0
  - numpy >= 1.21.0
- Kamera internetowa (opcjonalnie) / Webcam (optional)
- Zbiór danych z emocjami / Emotion dataset

Pełna lista zależności w `requirements.txt` / Full dependency list in `requirements.txt`

## Wskazówki dla początkujących
1. **Zacznij od małego zbioru danych** - Nie potrzebujesz tysięcy zdjęć na początku. Zacznij od kilkudziesięciu zdjęć na każdą emocję, żeby zrozumieć jak działa system.

2. **Eksperymentuj z parametrami** - W pliku `main.py` możesz zmieniać parametry jak `samples_limit` czy `kernel`, żeby zobaczyć jak wpływają na wyniki.

3. **Obserwuj FPS** - Jeśli program działa wolno, zmniejsz liczbę wykrywanych punktów lub użyj prostszego modelu.

4. **Testuj różne emocje** - Spróbuj różnych wyrazów twarzy przed kamerą i zobacz jak model reaguje.

5. **Czytaj komentarze w kodzie** - Każdy plik zawiera szczegółowe komentarze wyjaśniające co robi poszczególny fragment kodu.

## 📚 Dokumentacja / Documentation

- **[PRZEWODNIK_DLA_STUDENTA.md](PRZEWODNIK_DLA_STUDENTA.md)** - Kompleksowy przewodnik dla studentów i początkujących / Comprehensive student guide
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Jak pomóc w rozwoju projektu / How to contribute
- **[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)** - Kodeks postępowania / Code of conduct
- **[CHANGELOG.md](CHANGELOG.md)** - Historia zmian / Change history

## 🤝 Jak pomóc? / How to Contribute?

Zapraszamy do współpracy! Zobacz [CONTRIBUTING.md](CONTRIBUTING.md) po więcej informacji.

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for more information.

## 📜 Licencja / License

Ten projekt jest dostępny na licencji MIT. Zobacz plik [LICENSE](LICENSE) po szczegóły.

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 📞 Kontakt / Contact

- GitHub Issues: [Report a bug or request a feature](https://github.com/MatPomGit/Facial-Emotion-Recognition/issues)
- Pull Requests: [Contribute to the project](https://github.com/MatPomGit/Facial-Emotion-Recognition/pulls)

## 🙏 Podziękowania / Acknowledgments

- Google MediaPipe team - za doskonałą bibliotekę do wykrywania twarzy
- Twórcy scikit-learn - za implementację algorytmu SVM
- Społeczność OpenCV - za wszechstronne narzędzia do przetwarzania obrazu

---

**Stworzone z ❤️ dla edukacji i nauki / Made with ❤️ for education and learning**