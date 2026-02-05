"""
=== MODUŁ WYKRYWANIA TWARZY - MEDIAPIPE ===

HISTORIA I KONTEKST:
MediaPipe to framework opracowany przez zespół badaczy z Google. Powstał z potrzeby
stworzenia szybkich, dokładnych algorytmów działających nawet na urządzeniach mobilnych.
Jeśli kiedykolwiek używałeś filtrów na Snapchacie czy Instagramie, prawdopodobnie
korzystałeś z podobnej technologii!

ARCHITEKTURA SYSTEMU:
Ten moduł stanowi "oczy" naszego systemu. Jego zadanie:
Obraz wejściowy → Lokalizacja twarzy → 468 punktów orientacyjnych → Dane wyjściowe

DLACZEGO 468 PUNKTÓW?
MediaPipe używa bardzo szczegółowej siatki punktów:
- Kontur twarzy: ~70 punktów
- Oczy (każde): ~71 punktów  
- Brwi (każda): ~10 punktów
- Nos: ~38 punktów
- Usta: ~40 punktów
- Pozostałe obszary twarzy: ~168 punktów

Dla porównania: Starsze systemy jak dlib używają tylko 68 punktów.
Więcej punktów = większa dokładność, ale też więcej obliczeń.

TRYBY DZIAŁANIA:
1. Static Mode (static_image_mode=True):
   - Dla pojedynczych zdjęć
   - Każde zdjęcie analizowane od nowa
   - Wolniejsze, ale bardziej dokładne
   
2. Video Mode (static_image_mode=False):
   - Dla strumienia wideo
   - Śledzi twarz między klatkami
   - Szybsze, wykorzystuje ciągłość ruchu
"""

import cv2
import mediapipe as mp


class FaceDetector:
    def __init__(self, static=False, max_face=1):
        """
        Konstruktor detektora twarzy
        
        PARAMETRY KONFIGURACYJNE:
        
        static: bool (domyślnie False)
            Określa tryb pracy modelu:
            - True: Tryb statyczny - każda klatka analizowana niezależnie
                    UŻYJ gdy: przetwarzasz pojedyncze zdjęcia lub jakość > szybkość
            - False: Tryb wideo - śledzi twarze między klatkami  
                     UŻYJ gdy: przetwarzasz wideo i potrzebujesz płynności
        
        max_face: int (domyślnie 1)
            Maksymalna liczba twarzy do wykrycia na jednym obrazie
            PRZYKŁADY ZASTOSOWAŃ:
            - max_face=1: Aplikacja z jednym użytkownikiem (portret, selfie)
            - max_face=5: Zdjęcie grupowe, mała grupa
            - max_face=10: Duże zdjęcie grupowe, tłum
            
            UWAGA: Więcej twarzy = więcej obliczeń = niższe FPS!
            Dla max_face=10 program może działać 10x wolniej niż dla max_face=1
        
        INICJALIZACJA WEWNĘTRZNA:
        - Ładujemy moduł face_mesh z MediaPipe
        - Konfigurujemy go z zadanymi parametrami
        - Przygotowujemy pustą listę na wykryte punkty
        """
        self.__mpFaceMesh = mp.solutions.face_mesh
        self.__faceMesh = self.__mpFaceMesh.FaceMesh(static_image_mode=static, max_num_faces=max_face)
        self.__faceLandmarks = None

    def landmarks(self) -> (list or None):
        """
        Zwraca ostatnio wykryte punkty orientacyjne
        
        STRUKTURA DANYCH:
        Lista list - każda zewnętrzna lista to jedna twarz:
        [
            [punkt_0, punkt_1, ..., punkt_467],  # Twarz nr 0
            [punkt_0, punkt_1, ..., punkt_467],  # Twarz nr 1
            ...
        ]
        
        Każdy punkt to obiekt z atrybutami:
        - x: współrzędna pozioma (0.0 do 1.0, znormalizowana)
        - y: współrzędna pionowa (0.0 do 1.0, znormalizowana)
        - z: głębokość (przybliżona, mniej dokładna niż x, y)
        
        ZWRACA:
        list lub None - lista wykrytych twarzy lub None jeśli nic nie wykryto
        """
        return self.__faceLandmarks

    def detect(self, image) -> (list or None):
        """
        Główna metoda wykrywania - analizuje obraz i znajduje twarze
        
        PROCES KROK PO KROKU:
        
        1. PRZYGOTOWANIE
           - Resetujemy listę wykrytych punktów (zaczynamy od czystej kartki)
           - Konwertujemy obraz z BGR na RGB (MediaPipe wymaga RGB)
        
        2. DETEKCJA
           - Przekazujemy obraz do sieci neuronowej MediaPipe
           - Sieć analizuje obraz i zwraca lokalizacje twarzy
        
        3. EKSTRAKCJA PUNKTÓW
           - Dla każdej wykrytej twarzy wydobywamy wszystkie 468 punktów
           - Punkty są zapisywane w znormalizowanym formacie (0.0-1.0)
        
        4. ZWROT WYNIKU
           - Jeśli nic nie wykryto: None
           - Jeśli wykryto twarze: lista ze wszystkimi punktami
        
        PARAMETRY:
        image: numpy.ndarray
            Obraz wejściowy w formacie BGR (standardowy format OpenCV)
            Może być dowolnej rozdzielczości, ale większe = wolniejsze
        
        ZWRACA:
        list lub None
            Lista wykrytych twarzy lub None gdy nie wykryto żadnej
        
        TYPOWE PROBLEMY I ROZWIĄZANIA:
        
        Problem: Nic nie wykrywa mimo widocznej twarzy
        Rozwiązanie: Sprawdź oświetlenie, upewnij się że twarz nie jest zasłonięta
        
        Problem: Wykrywa twarze tam gdzie ich nie ma (false positive)
        Rozwiązanie: Zwiększ confidence threshold (wymaga modyfikacji kodu MediaPipe)
        
        Problem: Punkty "skaczą" między klatkami w wideo
        Rozwiązanie: Ustaw static=False dla trybu wideo (lepsze śledzenie)
        
        Problem: Bardzo wolne działanie
        Rozwiązanie: Zmniejsz rozdzielczość obrazu, ogranicz max_face
        """
        # Krok 1: Reset i przygotowanie
        self.__faceLandmarks = []

        # Krok 2: Konwersja kolorów (BGR → RGB)
        # OpenCV używa BGR, ale MediaPipe wymaga RGB
        imgRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Krok 3: Wykrywanie twarzy przez model MediaPipe
        # To jest moment gdy działa sieć neuronowa!
        facial = self.__faceMesh.process(imgRGB)
        landmarks = facial.multi_face_landmarks

        # Krok 4: Sprawdzenie czy cokolwiek wykryto
        if landmarks is None:
            return self.landmarks()  # Zwróć None jeśli brak twarzy

        # Krok 5: Ekstrakcja punktów dla każdej wykrytej twarzy
        for i, facial_landmarks in enumerate(landmarks):
            # Utworz pustą listę dla tej konkretnej twarzy
            self.__faceLandmarks.append([])
            
            # Dodaj wszystkie 468 punktów
            for j in range(0, 468):
                self.__faceLandmarks[i].append(facial_landmarks.landmark[j])

        return self.landmarks()
