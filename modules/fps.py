"""
=== MODUŁ FPS (FRAMES PER SECOND) ===

WPROWADZENIE DLA STUDENTA:
Ten prosty moduł mierzy wydajność programu poprzez obliczanie FPS - liczby klatek na sekundę.

CO TO JEST FPS?
FPS (Frames Per Second) = ile razy na sekundę program przetwarza nową klatkę obrazu.

DLACZEGO TO WAŻNE?
- FPS > 24: Obraz wygląda płynnie, naturalne doświadczenie
- FPS 15-24: Zauważalne lekkie szarpnięcia, ale użyteczne
- FPS < 15: Wyraźne opóźnienia, frustrujące doświadczenie
- FPS < 5: Program praktycznie nie nadaje się do użytku w czasie rzeczywistym

CO WPŁYWA NA FPS?
1. Złożoność algorytmów (np. wykrywanie 468 punktów vs 68 punktów)
2. Rozdzielczość obrazu (1920x1080 vs 640x480)
3. Moc komputera (procesor, karta graficzna)
4. Liczba wykrywanych twarzy (1 twarz vs 10 twarzy)

OPTYMALIZACJA:
Jeśli Twój program działa wolno:
- Zmniejsz rozdzielczość obrazu (fx=0.5, fy=0.5 w main.py)
- Ogranicz liczbę wykrywanych twarzy (max_face=1)
- Nie rysuj wszystkich punktów (usuń pętlę rysowania w main.py)
- Użyj prostszego modelu (dlib zamiast mediapipe)
"""

import time


class FPS:
    def __init__(self):
        """
        Inicjalizacja licznika FPS
        
        ZMIENNE WEWNĘTRZNE:
        __pTime: poprzedni czas (previous time) - używany do obliczenia różnicy czasu
        
        Inicjalnie ustawiony na 0, co oznacza "jeszcze nie mierzono".
        """
        self.__pTime = 0

    def start(self):
        """
        Oblicza i zwraca aktualny FPS
        
        JAK TO DZIAŁA?
        FPS = 1 / (czas między klatkami)
        
        PRZYKŁAD:
        Jeśli między klatkami upłynęło 0.033 sekundy:
        FPS = 1 / 0.033 = 30 klatek na sekundę
        
        ALGORYTM:
        1. Pobierz aktualny czas (cTime)
        2. Oblicz różnicę z poprzednim czasem (cTime - pTime)
        3. Oblicz FPS jako odwrotność tej różnicy
        4. Zapisz aktualny czas jako "poprzedni" dla następnego wywołania
        5. Zwróć obliczone FPS
        
        OBSŁUGA BŁĘDÓW:
        Przy pierwszym wywołaniu pTime=0, co spowodowałoby dzielenie przez 0.
        Dlatego używamy try-except - przy pierwszym razie zwracamy 0 lub pomijamy błąd.
        
        ZWRACA:
        float - liczba klatek na sekundę (np. 28.5 FPS)
        """
        cTime = time.time()  # Aktualny czas w sekundach (np. 1709849302.3421)
        try:
            # Oblicz FPS jako odwrotność czasu między klatkami
            fps = 1 / (cTime - self.__pTime)
        except:
            # Przy pierwszym wywołaniu lub dzieleniu przez 0, ustaw FPS na 0
            fps = 0
        
        # Zaktualizuj "poprzedni czas" dla następnego pomiaru
        self.__pTime = cTime

        return fps
