# Facial-Emotion-Recognition
System rozpoznawania emocji na twarzy (FER - Facial Expression Recognition)

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

## Wymagania techniczne
- Python 3.x
- Biblioteki: OpenCV, MediaPipe (lub Dlib), scikit-learn, pandas, numpy
- Kamera internetowa (do działania w czasie rzeczywistym) lub zdjęcia testowe
- Zbiór danych z emocjami (obrazy pogrupowane według emocji)

## Wskazówki dla początkujących
1. **Zacznij od małego zbioru danych** - Nie potrzebujesz tysięcy zdjęć na początku. Zacznij od kilkudziesięciu zdjęć na każdą emocję, żeby zrozumieć jak działa system.

2. **Eksperymentuj z parametrami** - W pliku `main.py` możesz zmieniać parametry jak `samples_limit` czy `kernel`, żeby zobaczyć jak wpływają na wyniki.

3. **Obserwuj FPS** - Jeśli program działa wolno, zmniejsz liczbę wykrywanych punktów lub użyj prostszego modelu.

4. **Testuj różne emocje** - Spróbuj różnych wyrazów twarzy przed kamerą i zobacz jak model reaguje.

5. **Czytaj komentarze w kodzie** - Każdy plik zawiera szczegółowe komentarze wyjaśniające co robi poszczególny fragment kodu.