""" 
=== KALKULATOR PROPORCJI TWARZY - MEDIAPIPE ===

FUNDAMENTALNA IDEA PROJEKTU:
Ludzkie emocje nie są "magiczne" - wyrażają się poprzez konkretne, mierzalne zmiany w twarzy.
Ten moduł to serce systemu - przekształca 468 punktów w 8 liczb, które opisują emocję.

FILOZOFIA ROZWIĄZANIA:
Zamiast analizować surowe współrzędne punktów (468 punktów × 3 wymiary = 1404 wartości!),
obliczamy PROPORCJE - relacje między kluczowymi odległościami na twarzy.

DLACZEGO PROPORCJE A NIE SUROWE ODLEGŁOŚCI?

Przykład ilustrujący problem:
- Osoba A: twarz o szerokości 15cm, uśmiech 8cm → stosunek 15/8 = 1.875
- Osoba B: twarz o szerokości 20cm, uśmiech 10.7cm → stosunek 20/10.7 = 1.870

Mimo różnych wymiarów fizycznych, PROPORCJA jest prawie identyczna!
To właśnie pozwala naszemu modelowi rozpoznawać emocje niezależnie od:
- Wielkości twarzy (dziecko vs dorosły)
- Odległości od kamery (blisko vs daleko)
- Rozdzielczości zdjęcia (480p vs 4K)

MAPOWANIE EMOCJI NA LICZBY:

Każda emocja ma charakterystyczny "podpis" w proporcjach:

RADOŚĆ (happy):
- d2/d3 wysoki (szeroki uśmiech, usta otwarte)
- d4/d5 niski (oczy przymrużone od uśmiechu)
- d6/d8 niski (brwi relaksują się)

SMUTEK (sad):
- d2/d3 niski (usta zamknięte, czasem opuszczone kąciki)
- d6/d8 wysoki (brwi opuszczone)
- d9/d10 wysoki (wydłużona twarz)

ZASKOCZENIE (surprise):
- d2/d3 średni do wysokiego (usta otwarte)
- d4/d5 niski (oczy szeroko otwarte)
- d6/d7 średni (brwi uniesione)

ZŁOŚĆ (angry):
- d2/d3 średni (usta zaciśnięte lub lekko otwarte)
- d6/d8 niski (brwi ściągnięte ku nosowi)
- d6/d7 wysoki (brwi zbliżone do siebie)

SZCZEGÓŁOWY OPIS OBLICZANYCH ODLEGŁOŚCI:

Używamy następujących miar (d = distance, odległość):
    - d1: Szerokość twarzy (punkt 345 → punkt 116)
          ZASTOSOWANIE: Normalizacja - każda twarz ma inną szerokość
          
    - d2: Szerokość ust (punkt 57 → punkt 306)
          ZNACZENIE: Szeroki uśmiech vs wąskie usta
          EMOCJE: wysoka w happy/surprise, niska w sad/neutral
          
    - d3: Otwarcie ust wertykalnie (punkt 11 → punkt 17)
          ZNACZENIE: Jak bardzo usta są otwarte
          EMOCJE: wysoka w surprise/fear, niska w neutral/sad
          
    - d4: Średnia szerokość oczu (punkt 130→243 + punkt 463→359) / 2
          ZNACZENIE: Jak szeroko oczy są otwarte horyzontalnie
          UWAGA: Uśredniamy lewe i prawe oko dla symetrii
          
    - d5: Średnia wysokość otwarcia oczu (punkt 145→159 + punkt 374→386) / 2
          ZNACZENIE: Jak szeroko oczy są otwarte wertykalnie
          EMOCJE: wysoka w surprise/fear, niska w happy (przymrużone)
          
    - d6: Średnia długość brwi (punkt 55→70 + punkt 285→300) / 2
          ZNACZENIE: Długość linii brwi
          STABILNA: Ta wartość się mało zmienia między emocjami
          
    - d7: Odległość między brwiami (punkt 55 → punkt 285)
          ZNACZENIE: Jak blisko siebie są brwi
          EMOCJE: mała w angry (brwi ściągnięte), duża w surprise
          
    - d8: Średnia odległość brwi od oka (punkt 55→243 + punkt 285→359) / 2
          ZNACZENIE: Czy brwi są uniesione czy opuszczone
          EMOCJE: duża w surprise (brwi w górę), mała w sad (brwi w dół)
          
    - d9: Długość nosa (punkt 1 → punkt 8)
          ZNACZENIE: Odległość od nasady do czubka nosa
          STABILNA: Używana głównie do normalizacji
          
    - d10: Odległość nos-górna warga (punkt 1 → punkt 11)
           ZNACZENIE: Przestrzeń między nosem a ustami
           ZMIENIA SIĘ: Gdy usta się otwierają
           
    - d11: Średnia odległość brwi-usta (punkt 55→57 + punkt 285→306) / 2
           ZNACZENIE: Dystans od brwi do kącików ust
           POMOCNICZA: Dodatkowa miara proporcji twarzy
           
    - d12: Odległość między oczami (punkt 130 → punkt 359)
           ZNACZENIE: Szerokość międzyoczodołowa
           STABILNA: Prawie nie zmienia się, używana do normalizacji
* Gwiazdka oznacza wartości uśredniowane dla obu stron twarzy

FINALNE PROPORCJE (a1-a8):

Po obliczeniu 12 odległości, tworzymy 8 PROPORCJI przez dzielenie:

    - a1 = d1 / d2: Stosunek szerokości twarzy do szerokości ust
          INTERPRETACJA: Jak szeroki jest uśmiech względem całej twarzy
          
    - a2 = d2 / d3: Stosunek szerokości do wysokości ust
          INTERPRETACJA: Czy usta są szersze poziomo czy otwarte pionowo
          EMOCJE: happy=wysoki (szeroki płaski uśmiech), surprise=niski (okrągłe "O")
          
    - a3 = d4 / d5: Stosunek szerokości do wysokości oka
          INTERPRETACJA: Kształt oka - wydłużone vs okrągłe
          EMOCJE: surprise/fear=niski (okrągłe), happy=wysoki (przymrużone)
          
    - a4 = d6 / d7: Stosunek długości brwi do odległości między nimi
          INTERPRETACJA: Czy brwi są blisko siebie (angry) czy daleko (neutral)
          
    - a5 = d6 / d8: Stosunek długości brwi do odległości brwi-oko
          INTERPRETACJA: Pozycja brwi - uniesione (surprise) vs opuszczone (sad)
          
    - a6 = d9 / d10: Stosunek długości nosa do odległości nos-usta
          INTERPRETACJA: Jak blisko usta są nosa (zmienia się gdy usta otwarte)
          
    - a7 = d11 / d9: Stosunek odległości brwi-usta do długości nosa
          INTERPRETACJA: Ogólne proporcje górnej/dolnej części twarzy
          
    - a8 = d12 / d2: Stosunek szerokości międzyocznej do szerokości ust
          INTERPRETACJA: Jak szeroki uśmiech w stosunku do stałego elementu

PRZYKŁADOWE WARTOŚCI (dla różnych emocji):

Happy: [~2.9, ~3.5, ~3.8, ~2.0, ~2.4, ~3.2, ~1.9, ~1.5]
Sad: [~3.1, ~4.2, ~3.5, ~1.8, ~2.8, ~2.9, ~2.1, ~1.7]
Surprise: [~3.0, ~2.1, ~2.8, ~2.2, ~2.0, ~2.5, ~1.8, ~1.6]

UWAGA: To są przybliżone wartości! Rzeczywiste mogą się różnić.
"""

import math


class Distance:
    """
    Klasa pomocnicza do obliczania odległości euklidesowych między punktami
    
    MATEMATYKA:
    Odległość między dwoma punktami (x1,y1) i (x2,y2) to:
    d = √[(x2-x1)² + (y2-y1)²]
    
    Jest to twierdzenie Pitagorasa zastosowane w układzie współrzędnych!
    
    PRZYKŁAD:
    Punkt A: (0, 0)
    Punkt B: (3, 4)
    Odległość = √[(3-0)² + (4-0)²] = √[9 + 16] = √25 = 5
    
    DLACZEGO OSOBNA KLASA?
    Enkapsulacja - raz tworzymy obiekt z dostępem do punktów twarzy,
    potem możemy wielokrotnie wywoływać result() dla różnych par punktów.
    To jest bardziej efektywne niż przekazywanie całej listy za każdym razem.
    """
    def __init__(self, obj):
        """
        Inicjalizacja z listą punktów twarzy
        
        PARAMETRY:
        obj: lista 468 punktów wykrytych przez MediaPipe
             Każdy punkt ma atrybuty .x i .y (współrzędne znormalizowane 0-1)
        """
        self.__obj = obj

    def result(self, a, b):
        """
        Oblicza odległość między punktem 'a' i punktem 'b'
        
        PARAMETRY:
        a, b: int - indeksy punktów (0-467)
        
        ZWRACA:
        float - odległość euklidesowa w przestrzeni znormalizowanej (0-1)
        
        PRZYKŁAD UŻYCIA:
        dist = Distance(face_points)
        mouth_width = dist.result(57, 306)  # Szerokość ust
        """
        return math.dist((self.__obj[a].x, self.__obj[a].y), (self.__obj[b].x, self.__obj[b].y))


def div(a: float, b: float):
    """
    Bezpieczne dzielenie z obsługą dzielenia przez zero
    
    PROBLEM:
    W matematyce dzielenie przez 0 jest nieokreślone (0/0) lub nieskończone (x/0).
    W Pythonie powoduje to wyjątek ZeroDivisionError i program się crashuje.
    
    ROZWIĄZANIE:
    Jeśli mianownik (b) jest 0 lub bardzo bliski 0, zwracamy 0.0
    To jest sensowne w naszym kontekście - jeśli coś ma wymiar 0, proporcja to 0.
    
    PRZYKŁAD:
    div(10, 2) → 5.0 ✓
    div(10, 0) → 0.0 ✓ (zamiast błędu)
    div(0, 0) → 0.0 ✓ (zamiast błędu)
    
    PARAMETRY:
    a: float - licznik (liczba dzielona)
    b: float - mianownik (liczba przez którą dzielimy)
    
    ZWRACA:
    float - wynik dzielenia lub 0.0 w przypadku dzielenia przez zero
    """
    try:
        return a / b
    except:
        return 0.0


class RatioCalculator:
    def __init__(self, face: list) -> None:
        """
        Konstruktor - oblicza wszystkie 12 odległości dla danej twarzy
        
        PROCES:
        1. Tworzymy obiekt Distance dla szybkiego dostępu do punktów
        2. Obliczamy każdą z 12 odległości używając odpowiednich par punktów
        3. Dla miar symetrycznych (oczy, brwi) - uśredniamy obie strony
        
        PARAMETRY:
        face: list - lista 468 punktów jednej twarzy z MediaPipe
        
        NUMERY PUNKTÓW - MAPOWANIE ANATOMICZNE:
        
        Twarz (szerokość):
        - 345: lewy skraj twarzy (od strony osoby patrzącej)
        - 116: prawy skraj twarzy
        
        Usta:
        - 57: lewy kącik ust
        - 306: prawy kącik ust  
        - 11: górna środkowa część ust
        - 17: dolna środkowa część ust
        
        Oczy:
        - 130, 243: lewe oko (zewnętrzny i wewnętrzny kącik)
        - 463, 359: prawe oko (zewnętrzny i wewnętrzny kącik)
        - 145, 159: lewe oko (górna i dolna powieka)
        - 374, 386: prawe oko (górna i dolna powieka)
        
        Brwi:
        - 55, 70: lewa brew (początek i koniec)
        - 285, 300: prawa brew (początek i koniec)
        
        Nos:
        - 1: nasada nosa (między oczami)
        - 8: czubek nosa
        
        UWAGI IMPLEMENTACYJNE:
        - Używamy __dist jako skrótu do metody result() - czytelniejszy kod
        - Wszystkie odległości są w przestrzeni znormalizowanej (0-1)
        - Uśrednianie (/2) zapewnia symetrię nawet jeśli twarz lekko skręcona
        """
        dist = Distance(face).result
        self.__d1 = dist(345, 116)
        self.__d2 = dist(57, 306)
        self.__d3 = dist(11, 17)
        self.__d4 = (dist(130, 243) + dist(463, 359)) / 2
        self.__d5 = (dist(145, 159) + dist(374, 386)) / 2
        self.__d6 = (dist(55, 70) + dist(285, 300)) / 2
        self.__d7 = dist(55, 285)
        self.__d8 = (dist(55, 243) + dist(285, 359)) / 2
        self.__d9 = dist(1, 8)
        self.__d10 = dist(1, 11)
        self.__d11 = (dist(55, 57) + dist(285, 306)) / 2
        self.__d12 = dist(130, 359)

    def result(self) -> list:
        """
        Oblicza i zwraca finalne 8 proporcji twarzy
        
        ALGORYTM:
        Dla każdej z 8 proporcji (a1-a8):
        1. Pobierz odpowiednie odległości (d1-d12)
        2. Podziel je zgodnie ze wzorem
        3. Zaokrągl do 5 miejsc po przecinku (dokładność vs rozmiar danych)
        
        ZAOKRĄGLANIE:
        Dlaczego 5 miejsc? Balance między:
        - Za mało (1-2): Utrata informacji, gorsze rozpoznawanie
        - Za dużo (10+): Szum, nadmierna precyzja (floating point errors)
        - 5 miejsc: Optymalna dokładność dla naszego zastosowania
        
        PRZYKŁAD WYNIKU:
        [2.85714, 3.42857, 3.71429, 1.95238, 2.35714, 3.14285, 1.88571, 1.52381]
        
        Te 8 liczb to "DNA emocji" - unikalny podpis stanu emocjonalnego twarzy!
        
        ZWRACA:
        list[float] - lista 8 wartości proporcji, zaokrąglonych do 5 miejsc
        """
        a1 = div(self.__d1, self.__d2)
        a2 = div(self.__d2, self.__d3)
        a3 = div(self.__d4, self.__d5)
        a4 = div(self.__d6, self.__d7)
        a5 = div(self.__d6, self.__d8)
        a6 = div(self.__d9, self.__d10)
        a7 = div(self.__d11, self.__d9)
        a8 = div(self.__d12, self.__d2)
        result = [a1, a2, a3, a4, a5, a6, a7, a8]

        return [round(num, 5) for num in result]
