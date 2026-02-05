"""
=== MODUŁ SVM (SUPPORT VECTOR MACHINES) ===

WPROWADZENIE DLA STUDENTA:
Ten moduł implementuje algorytm SVM - jedną z najpopularniejszych metod uczenia maszynowego.
Jeśli uczysz się tego po raz pierwszy, oto kluczowe koncepcje:

CO TO JEST SVM?
Support Vector Machines to algorytm, który "uczy się" na przykładach. Wyobraź sobie, że:
- Masz zdjęcia twarzy z różnymi emocjami (to są Twoje "przykłady")
- Dla każdej twarzy mierzysz pewne cechy (np. szerokość uśmiechu, otwarcie oczu)
- SVM znajduje "granicę decyzyjną" która najlepiej rozdziela różne emocje

ANALOGIA:
Wyobraź sobie, że klasyfikujesz owoce na podstawie rozmiaru i koloru:
- Jabłka: średnie, czerwone
- Pomarańcze: średnie, pomarańczowe  
- Arbuzy: duże, zielone
SVM uczy się gdzie narysować linie rozdzielające te grupy w przestrzeni cech.

W NASZYM PRZYPADKU:
- Zamiast owoców mamy emocje (radość, smutek, złość...)
- Zamiast rozmiaru i koloru mamy proporcje twarzy (8 różnych pomiarów)
- SVM uczy się rozdzielać emocje w 8-wymiarowej przestrzeni cech

DLACZEGO SVR A NIE SVC?
Używamy SVR (Support Vector Regression) zamiast SVC (Classification), ponieważ:
- Emocje nie są całkowicie rozdzielne - istnieją stany pośrednie
- Twarz może wyrażać częściowo radość i częściowo zaskoczenie
- SVR zwraca wartość ciągłą (np. 3.4), którą zaokrąglamy do najbliższej emocji
"""

from sklearn.preprocessing import StandardScaler
from collections import Counter
from sklearn.svm import SVR
import pandas as pd
import numpy as np


class SVM:
    def __init__(self, dataset: str, labels: list) -> None:
        """
        Konstruktor klasy SVM - inicjalizuje model
        
        PARAMETRY:
        dataset: str - ścieżka do pliku CSV z danymi treningowymi
                      Format: kolumny z cechami (a1-a8) + kolumna 'emotions' z etykietami
        labels: list - lista możliwych emocji w kolejności [0, 1, 2, 3, 4, 5, 6]
                      np. ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
        
        CO SIĘ DZIEJE TUTAJ:
        1. Wczytujemy dane z pliku CSV do pamięci
        2. Zapisujemy listę etykiet (będzie nam potrzebna później)
        3. Model (self.__model) jest na razie None - zostanie stworzony podczas trenowania
        """
        try:
            self.__dataset = pd.read_csv(dataset)
        except:
            raise print('Błąd: Odczyt zbioru danych - Nieprawidłowy plik lub nie można znaleźć ścieżki')
        self.__labels = labels
        self.__model = None

    @staticmethod
    def __features_scaling(data):
        """
        Skalowanie cech - normalizacja danych
        
        DLACZEGO TO ROBIMY?
        Różne cechy mogą mieć różne zakresy wartości:
        - Cecha A: wartości od 0.5 do 2.0
        - Cecha B: wartości od 10 do 100
        
        Bez normalizacji, algorytm "myśli" że cecha B jest ważniejsza (ma większe liczby).
        Po normalizacji wszystkie cechy są w podobnym zakresie (średnia=0, odchylenie=1).
        
        PRZYKŁAD:
        Przed: [1.5, 50, 0.8, 75]
        Po:    [-0.5, 0.2, -1.2, 0.8]
        
        KIEDY UŻYWAĆ?
        - Dla SVM z kernelem 'rbf': skalowanie często POPRAWIA wyniki
        - Dla niektórych zbiorów danych: może NIE być potrzebne
        - W naszym projekcie: testujemy z scale=False (bez skalowania)
        
        ZWRACA:
        Dane po normalizacji (te same wymiary, inne wartości)
        """
        sc = StandardScaler()
        return sc.fit_transform(data)

    def __labels_transforming(self, data, labels, limit):
        """
        Transformacja etykiet i balansowanie zbioru danych
        
        PROBLEM DO ROZWIĄZANIA:
        Zbiory danych często są niezbalansowane:
        - 5000 zdjęć z radością ("happy")
        - 500 zdjęć ze strachem ("fear")
        
        To sprawia, że model "preferuje" częstsze emocje - zawsze zgaduje "happy".
        
        ROZWIĄZANIE:
        Ograniczamy liczbę próbek dla każdej emocji do wartości 'limit'.
        Jeśli mamy 5000 próbek "happy" ale limit=3000, używamy tylko 3000.
        Dzięki temu wszystkie emocje mają podobną reprezentację.
        
        TRANSFORMACJA ETYKIET:
        Zamiast tekstów ("happy", "sad") używamy liczb (0, 1, 2, 3, 4, 5, 6).
        Dlaczego? Algorytmy ML operują na liczbach, nie na tekstach.
        
        Mapowanie:
        "angry" -> 0
        "disgust" -> 1
        "fear" -> 2
        "happy" -> 3
        "neutral" -> 4
        "sad" -> 5
        "surprise" -> 6
        
        PARAMETRY:
        data: macierz cech (każdy wiersz = jedna twarz, każda kolumna = jedna cecha)
        labels: lista etykiet tekstowych dla każdej próbki
        limit: maksymalna liczba próbek na emocję (0 = bez limitu)
        
        ZWRACA:
        X: przefiltrowane dane (usunięte nadmiarowe próbki)
        y: przetransformowane etykiety (liczby zamiast tekstów)
        """
        drop = []  # Indeksy próbek do usunięcia
        count = [0 for i in labels]  # Licznik dla każdej emocji

        # Jeśli limit=0, ustaw na nieskończoność (brak limitu)
        limit = float('inf') if limit == 0 else limit
        
        # Przejdź przez wszystkie etykiety
        for i, emotion in enumerate(labels):
            for j, label in enumerate(self.__labels):
                if emotion == label:
                    # Jeśli przekroczono limit dla tej emocji, zaznacz do usunięcia
                    if count[j] >= limit:
                        drop.append(i)
                    else:
                        # W przeciwnym razie, zamień tekst na numer
                        labels[i] = j
                        count[j] += 1

        # Usuń nadmiarowe próbki
        X = np.delete(data, drop, 0)
        y = np.delete(labels, drop, 0)
        return X, y

    def train(self, predict_label: str, scale: bool = False, samples_limit: int = 0, kernel: str = 'rbf') -> None:
        """
        Trenowanie modelu SVM - tutaj dzieje się "magia" uczenia maszynowego
        
        PARAMETRY DO EKSPERYMENTOWANIA:
        
        predict_label: str
            Nazwa kolumny do przewidywania (u nas zawsze 'emotions')
            
        scale: bool (domyślnie False)
            Czy normalizować dane przed treningiem?
            - True: zastosuj StandardScaler (zalecane dla danych o różnych skalach)
            - False: użyj surowych danych (działa gdy cechy są już znormalizowane)
            EKSPERYMENT: Porównaj wyniki z scale=True i scale=False!
            
        samples_limit: int (domyślnie 0)
            Maksymalna liczba próbek na emocję
            - 0: użyj wszystkich dostępnych danych
            - 3000: użyj maksymalnie 3000 próbek dla każdej emocji
            ZASTOSOWANIE: Balansowanie niezrównoważonych zbiorów danych
            EKSPERYMENT: Zobacz jak zmienia się dokładność przy różnych limitach!
            
        kernel: str (domyślnie 'rbf')
            Typ funkcji kernela - to określa JAK SVM oddziela klasy
            
            Dostępne opcje:
            - 'rbf' (Radial Basis Function): Najczęściej używany, działa w większości przypadków
              Tworzy "bąbelki" wokół skupisk punktów tej samej klasy
              ZALETY: Uniwersalny, radzi sobie z nieliniowymi granicami
              WADY: Wymaga dobrania parametrów (gamma, C)
              
            - 'poly' (Polynomial): Używa wielomianów do rozdzielania klas
              ZALETY: Dobry dla danych z wielomianowymi zależnościami
              WADY: Może być wolniejszy, łatwo przeuczenie
              
            - 'linear': Prosta linia/płaszczyzna rozdzielająca
              ZALETY: Szybki, prosty, dobrze interpretowalny
              WADY: Nie radzi sobie z nieliniowymi granicami
              
            EKSPERYMENT: Przetestuj wszystkie kernele i porównaj wyniki!

        PROCES TRENOWANIA KROK PO KROKU:
        1. Wczytanie danych z CSV
        2. Podział na cechy (X) i etykiety (y)
        3. Opcjonalne skalowanie cech
        4. Balansowanie zbioru (ograniczenie próbek)
        5. Utworzenie modelu SVR z wybranym kernelem
        6. Dopasowanie modelu do danych (tutaj następuje uczenie!)
        7. Model gotowy do przewidywania

        ZWRACA:
        None (model jest zapisywany wewnętrznie w self.__model)
        """

        print(f"\n=== KONFIGURACJA TRENINGU ===")
        print(f"Skalowanie: {scale}")
        print(f"Limit próbek: {samples_limit if samples_limit > 0 else 'Bez limitu'}")
        print(f"Kernel: {kernel}")
        print("="*40)

        dataset = self.__dataset

        # Separacja cech (X) od etykiet (y)
        # X = wszystkie kolumny OPRÓCZ kolumny z emocjami (to są nasze cechy wejściowe)
        # y = tylko kolumna z emocjami (to jest to, co chcemy przewidywać)
        X = dataset.loc[:, dataset.columns != predict_label].values
        y = dataset.loc[:, predict_label].values

        # Opcjonalna normalizacja danych
        X = self.__features_scaling(X) if scale else X
        
        # Transformacja etykiet i balansowanie
        X, y = self.__labels_transforming(X, y, samples_limit)
        
        # Możesz odkomentować poniższą linię aby zobaczyć rozkład klas:
        # print(f"Rozkład klas po balansowaniu: {Counter(y)}")

        print("\nTrenowanie modelu... (to może potrwać kilka sekund)")
        
        # TUTAJ DZIEJE SIĘ UCZENIE!
        # Tworzymy model SVR i uczymy go na naszych danych
        self.__model = SVR(kernel=kernel)
        self.__model.fit(X, y)  # fit() = "naucz się na tych danych"
        
        print("✓ Trenowanie zakończone pomyślnie!")
        print("Model gotowy do przewidywania emocji.\n")

    def predict(self, data: list) -> float:
        """
        Przewidywanie emocji dla nowych danych
        
        PARAMETRY:
        data: list - lista 8 wartości reprezentujących proporcje twarzy
                     Kolejność MUSI być taka sama jak podczas trenowania!
                     Format: [a1, a2, a3, a4, a5, a6, a7, a8]
        
        ZWRACA:
        float - przewidywaną wartość emocji jako liczbę zmiennoprzecinkową
                np. 3.14 oznacza "prawie emocja nr 3" (happy)
                     5.89 oznacza "prawie emocja nr 6" (surprise)
        
        JAK TO DZIAŁA?
        1. Model bierze 8 cech wejściowych
        2. Umieszcza je w 8-wymiarowej przestrzeni
        3. Sprawdza "gdzie" ten punkt znajduje się względem wytrenowanych granic
        4. Zwraca najbliższą wartość emocji
        
        UWAGA:
        Wartość może być spoza zakresu 0-6! W main.py ograniczamy ją przed użyciem.
        """
        return self.__model.predict([data])
