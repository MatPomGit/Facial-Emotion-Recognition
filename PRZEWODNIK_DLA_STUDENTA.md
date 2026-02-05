# Przewodnik dla Studenta - Rozpoznawanie Emocji na Twarzy

## 🎓 Witaj w projekcie!

Ten dokument został stworzony specjalnie dla osób, które po raz pierwszy mają kontakt z systemami rozpoznawania emocji. Przeprowadzimy Cię krok po kroku przez cały proces.

---

## 📚 Spis Treści

1. [Czym jest ten projekt?](#czym-jest-ten-projekt)
2. [Wymagania wstępne](#wymagania-wstępne)
3. [Instalacja krok po kroku](#instalacja-krok-po-kroku)
4. [Jak działa system?](#jak-działa-system)
5. [Pierwsze uruchomienie](#pierwsze-uruchomienie)
6. [Rozumienie wyników](#rozumienie-wyników)
7. [Eksperymenty do przeprowadzenia](#eksperymenty-do-przeprowadzenia)
8. [Rozwiązywanie problemów](#rozwiązywanie-problemów)
9. [Dalsza nauka](#dalsza-nauka)

---

## 🎯 Czym jest ten projekt?

To praktyczny system, który:
- **Wykrywa twarze** na obrazie z kamery lub zdjęcia
- **Analizuje charakterystyczne punkty** twarzy (np. kąciki ust, oczy, brwi)
- **Rozpoznaje emocję** używając algorytmu uczenia maszynowego
- **Pokazuje wyniki** w czasie rzeczywistym

### Jakie emocje rozpoznaje?

System rozpoznaje 7 podstawowych emocji:
1. **angry** (złość) - ściągnięte brwi, zaciśnięte usta
2. **disgust** (obrzydzenie) - pomarszczony nos, uniesiona górna warga
3. **fear** (strach) - szeroko otwarte oczy, napięta twarz
4. **happy** (radość) - szeroki uśmiech, przymrużone oczy
5. **neutral** (neutralność) - spokojna, niewyraźna ekspresja
6. **sad** (smutek) - opuszczone kąciki ust, smutne oczy
7. **surprise** (zaskoczenie) - szeroko otwarte oczy i usta

---

## 💻 Wymagania wstępne

### Co musisz wiedzieć przed rozpoczęciem:

**Poziom podstawowy:**
- Podstawy programowania w Pythonie (zmienne, pętle, funkcje)
- Umiejętność korzystania z terminala/wiersza poleceń
- Podstawowe pojęcia o tym czym jest uczenie maszynowe (opcjonalne, wyjaśnimy po drodze)

**Co musisz mieć na komputerze:**
- Python 3.7 lub nowszy
- Pip (menedżer pakietów Python)
- Kamera internetowa (jeśli chcesz testować na żywo)
- Około 2GB wolnego miejsca na dysku

---

## 🛠️ Instalacja krok po kroku

### Krok 1: Sklonuj repozytorium

Otwórz terminal i wykonaj:

```bash
git clone https://github.com/MatPomGit/Facial-Emotion-Recognition.git
cd Facial-Emotion-Recognition
```

**Co się stało?** Pobrałeś wszystkie pliki projektu na swój komputer.

### Krok 2: Zainstaluj wymagane biblioteki

```bash
pip install opencv-python mediapipe scikit-learn pandas numpy
```

**Co instalujemy?**
- `opencv-python` - przetwarzanie obrazu i wideo
- `mediapipe` - wykrywanie punktów charakterystycznych twarzy (od Google)
- `scikit-learn` - algorytmy uczenia maszynowego (SVM)
- `pandas` - operacje na danych (wczytywanie CSV)
- `numpy` - operacje matematyczne na tablicach

**Jak długo to trwa?** 2-5 minut, w zależności od prędkości internetu.

### Krok 3: Pobierz zbiór danych

Potrzebujesz zbioru zdjęć twarzy z emocjami do wytrenowania modelu.

**Zalecany zbiór danych:** FER-2013 lub podobny

Zorganizuj pliki w następującej strukturze:
```
dataset/
  train/
    angry/
      image1.jpg
      image2.jpg
      ...
    happy/
      image1.jpg
      image2.jpg
      ...
    (pozostałe emocje...)
```

**Wskazówka:** Możesz zacząć od małego zbioru (50 zdjęć na emocję) do testów!

---

## 🧠 Jak działa system?

System działa w 3 głównych etapach:

### Etap 1: Przygotowanie danych treningowych

**Plik:** `modules/mediapipe/dataset_prepare.py`

**Co się dzieje:**
```
Zdjęcia twarzy → Wykrycie twarzy → Zmierzenie punktów → Obliczenie proporcji → CSV
```

**Szczegóły:**
1. Program czyta zdjęcia z folderów `dataset/train/`
2. Dla każdego zdjęcia wykrywa twarz używając MediaPipe
3. Znajduje 468 punktów charakterystycznych
4. Oblicza 8 kluczowych proporcji (np. szerokość uśmiechu / szerokość twarzy)
5. Zapisuje wyniki do pliku CSV wraz z etykietą emocji

**Proporcje zamiast surowych punktów - dlaczego?**
- 468 punktów × 3 współrzędne = 1404 wartości!
- 8 proporcji jest łatwiejsze do analizy
- Proporcje są niezależne od wielkości twarzy i odległości od kamery

### Etap 2: Trenowanie modelu

**Plik:** `modules/svm.py`

**Co się dzieje:**
```
Dane CSV → Przygotowanie → Algorytm SVM → Wytrenowany model
```

**Szczegóły:**
1. Wczytanie danych z CSV (8 proporcji + etykieta emocji)
2. Podział na cechy (X) i etykiety (y)
3. Opcjonalna normalizacja danych
4. Balansowanie zbioru (równa liczba przykładów dla każdej emocji)
5. Trenowanie modelu SVM
6. Model gotowy do przewidywania!

**Co to jest SVM?**
Support Vector Machine to algorytm, który uczy się rozpoznawać wzorce:
- Dostaje przykłady: "te proporcje = radość", "tamte proporcje = smutek"
- Znajduje "granice" między różnymi emocjami w przestrzeni cech
- Nowe przykłady klasyfikuje na podstawie znalezionych granic

### Etap 3: Rozpoznawanie w czasie rzeczywistym

**Plik:** `main.py`

**Co się dzieje:**
```
Kamera → Klatka → Wykryj twarz → Oblicz proporcje → Model przewiduje → Wyświetl
```

**Pętla główna powtarza się ciągle:**
1. Pobierz klatkę z kamery
2. Wykryj wszystkie twarze (MediaPipe)
3. Dla każdej twarzy oblicz 8 proporcji
4. Zapytaj model SVM o emocję
5. Wyświetl wynik na ekranie i w terminalu
6. Wróć do kroku 1

---

## 🚀 Pierwsze uruchomienie

### Opcja A: Przygotuj własne dane treningowe (polecane dla nauki)

```bash
# Przejdź do folderu mediapipe
cd modules/mediapipe

# Uruchom skrypt przygotowania danych
python dataset_prepare.py
```

**Czego oczekiwać:**
- Pasek postępu pokazujący przetwarzanie zdjęć
- Komunikaty o wykrytych twarzach
- Plik CSV z wynikami w `dataset/mediapipe_train_emotions.csv`

### Opcja B: Użyj gotowego pliku CSV (jeśli już masz)

Upewnij się, że plik `dataset/mediapipe_train_emotions.csv` istnieje i jest poprawnie sformatowany.

### Uruchom program główny

```bash
# Wróć do katalogu głównego
cd ../..

# Uruchom program
python main.py
```

**Co zobaczysz:**
1. Komunikaty o inicjalizacji modelu
2. Informacje o trenowaniu (może potrwać 10-60 sekund)
3. Okno z podglądem kamery
4. Niebieskie kropki na wykrytych twarzach
5. FPS w lewym górnym rogu
6. W terminalu: przewidywane emocje

**Aby zakończyć:** Naciśnij klawisz `q` (quit)

---

## 📊 Rozumienie wyników

### Okno podglądu

**Niebieskie kropki:** Wszystkie 468 punktów wykrytych przez MediaPipe
**Czerwona cyfra:** Numer twarzy (gdy wykryto wiele osób)
**Zielony tekst (FPS):** Liczba klatek na sekundę

### Terminal/konsola

Przykładowy wynik:
```
[3.14159] - ['happy']
```

**Interpretacja:**
- `3.14159` - surowa wartość przewidywana przez SVM (0-6)
- `happy` - emocja odpowiadająca wartości 3 (po zaokrągleniu)

**Mapowanie liczb na emocje:**
```
0 → angry
1 → disgust
2 → fear
3 → happy
4 → neutral
5 → sad
6 → surprise
```

**Wartości pośrednie:**
- `3.2` = przeważnie happy, odrobinę neutral
- `2.8` = między fear a happy
- `5.9` = prawie surprise

---

## 🔬 Eksperymenty do przeprowadzenia

Nauka wymaga eksperymentowania! Oto zadania do samodzielnego wykonania:

### Eksperyment 1: Testuj różne emocje

**Zadanie:** Postaw przed kamerą i spróbuj wyrazić każdą z 7 emocji.

**Pytania do przemyślenia:**
- Które emocje są najłatwiej rozpoznawane?
- Które są mylone ze sobą?
- Czy model radzi sobie z subtelnym wyrazami twarzy?

### Eksperyment 2: Zmiana parametrów SVM

**Plik:** `main.py`, linia z `emotion_model.train()`

**Zadania:**
1. Zmień `kernel='rbf'` na `kernel='poly'` - jak zmienia się dokładność?
2. Zmień `samples_limit=3000` na `samples_limit=1000` - czy model działa lepiej czy gorzej?
3. Zmień `scale=False` na `scale=True` - jaki to ma wpływ?

### Eksperyment 3: Optymalizacja wydajności

**Zadanie:** Sprawdź FPS przed i po zmianach.

**Zmiany do przetestowania w `main.py`:**
1. Zmień `fx=1, fy=1` na `fx=0.5, fy=0.5` (mniejsza rozdzielczość)
2. Zmień `max_face=10` na `max_face=1` (jedna twarz zamiast dziesięciu)
3. Zakomentuj pętlę rysującą 468 punktów (linie 49-52)

**Pytania:**
- Jak każda zmiana wpływa na FPS?
- Czy dokładność rozpoznawania się zmienia?

### Eksperyment 4: Porównaj MediaPipe z Dlib

**Zadanie:** Uruchom system z modułem dlib zamiast mediapipe.

**Kroki:**
1. Zmień importy w `main.py`:
   ```python
   # Zamiast mediapipe:
   from modules.dlib.dlib_FaceLandmarks import FaceDetector
   from modules.dlib.ratio_calc import RatioCalculator
   ```
2. Użyj odpowiedniego pliku CSV (dlib_train_emotions.csv)

**Porównaj:**
- Szybkość (FPS)
- Dokładność rozpoznawania
- Stabilność wykrywania

---

## 🐛 Rozwiązywanie problemów

### Problem: "Cannot find file path" przy uruchamianiu

**Rozwiązanie:**
- Sprawdź czy plik CSV istnieje: `dataset/mediapipe_train_emotions.csv`
- Upewnij się że uruchamiasz program z głównego katalogu projektu

### Problem: Bardzo niskie FPS (< 5)

**Przyczyny i rozwiązania:**
1. **Za dużo punktów do rysowania** → Zakomentuj pętlę rysującą
2. **Za wysoka rozdzielczość** → Zmniejsz fx, fy do 0.5
3. **Za dużo wykrywanych twarzy** → Ogranicz max_face do 1
4. **Słaby komputer** → Rozważ użycie dlib zamiast mediapipe

### Problem: Model nie rozpoznaje emocji poprawnie

**Możliwe przyczyny:**
1. **Za mało danych treningowych** → Potrzebujesz minimum 100 zdjęć na emocję
2. **Niezbalansowany zbiór** → Ustaw samples_limit w train()
3. **Zły kernel SVM** → Spróbuj różnych kerneli (rbf, poly, linear)
4. **Potrzeba normalizacji** → Ustaw scale=True

### Problem: Kamera się nie uruchamia

**Rozwiązanie:**
1. Sprawdź czy kamera działa w innych aplikacjach
2. Zmień `cv2.VideoCapture(0)` na `cv2.VideoCapture(1)` (inna kamera)
3. Ustaw `image_mode = True` i testuj na zdjęciach

---

## 📖 Dalsza nauka

### Polecane tematy do zgłębienia:

**Podstawy:**
1. Jak działają sieci neuronowe?
2. Co to jest uczenie nadzorowane vs nienadzorowane?
3. Jak działa walidacja krzyżowa?

**Średniozaawansowane:**
1. Inne algorytmy klasyfikacji (Random Forest, Neural Networks)
2. Augmentacja danych treningowych
3. Metryki oceny modelu (accuracy, precision, recall, F1-score)

**Zaawansowane:**
1. Transfer learning z gotowych modeli (VGG, ResNet)
2. Real-time video stream optimization
3. Deployment na urządzenia mobilne

### Polecane zasoby:

**Polskie:**
- Kursy machine learning na platformach edukacyjnych
- Grupy na Facebooku o AI/ML w Polsce
- Polskie blogi o data science

**Angielskie:**
- Dokumentacja scikit-learn: https://scikit-learn.org/
- MediaPipe dokumentacja: https://google.github.io/mediapipe/
- Kaggle tutorials: https://www.kaggle.com/learn

---

## 🎯 Podsumowanie

Gratulacje! Teraz rozumiesz:
- ✅ Jak działa system rozpoznawania emocji end-to-end
- ✅ Rolę każdego modułu w projekcie
- ✅ Jak trenować i testować model SVM
- ✅ Jak eksperymentować z różnymi parametrami
- ✅ Jak rozwiązywać typowe problemy

**Następne kroki:**
1. Przeprowadź wszystkie eksperymenty z sekcji 🔬
2. Spróbuj poprawić dokładność modelu
3. Dodaj nowe funkcje (np. zapisywanie statystyk)
4. Podziel się wynikami z innymi!

**Pamiętaj:** Nauka przez praktykę jest najważniejsza. Nie bój się eksperymentować i popełniać błędów!

---

## 📝 Notatki i pytania

Użyj tej sekcji do zapisywania własnych obserwacji i pytań podczas pracy z projektem:

```
Moje obserwacje:
-
-
-

Pytania do zbadania:
-
-
-

Pomysły na ulepszenia:
-
-
-
```

Powodzenia w nauce! 🚀
