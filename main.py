"""
=== GŁÓWNY PROGRAM ROZPOZNAWANIA EMOCJI ===

Ten skrypt stanowi serce całego systemu. Jego zadaniem jest:
1. Pobranie obrazu z kamery lub pliku
2. Wykrycie twarzy na obrazie  
3. Obliczenie proporcji charakterystycznych dla każdej twarzy
4. Przewidzenie emocji przy użyciu wytrenowanego modelu
5. Wizualizacja wyników na ekranie

UWAGA DLA STUDENTA:
Jeśli to Twój pierwszy kontakt z projektem, przeczytaj najpierw plik README.md
aby zrozumieć ogólną architekturę systemu.
"""

# Importowanie modułów - każdy odpowiada za inną funkcjonalność
from modules.mediapipe.mediapipe_FaceLandmarks import FaceDetector  # Wykrywanie twarzy
from modules.mediapipe.ratio_calc import RatioCalculator  # Obliczanie proporcji
from modules.svm import SVM  # Model uczenia maszynowego
from modules.fps import FPS  # Pomiar wydajności
import cv2  # OpenCV - biblioteka do przetwarzania obrazu

# Lista wszystkich emocji rozpoznawanych przez system
# Kolejność jest ważna - odpowiada numerom 0-6 używanym wewnętrznie
labels = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']

# TRYB PRACY: False = kamera na żywo, True = pojedyncze zdjęcie
# Zmień na True jeśli chcesz przetestować system na statycznym obrazie
image_mode = False

if image_mode:
    # Tryb obrazka: wczytaj konkretny plik ze ścieżki
    # ZADANIE: Zmień ścieżkę na swoją, wskazującą na zdjęcie twarzy
    img = cv2.imread('C:/Users/HT0710/Pictures/3-views-female-face.jpg')

else:
    # Tryb kamery: uruchom domyślną kamerę (0 = pierwsza kamera w systemie)
    # Jeśli masz kilka kamer, możesz spróbować 1, 2, itd.
    cap = cv2.VideoCapture(0)

# Inicjalizacja obiektu mierzącego FPS (klatki na sekundę)
# FPS pokazuje jak szybko działa nasz program
fps = FPS()

# KROK 1: Przygotowanie modelu wykrywania twarzy
# Parametry: static=True (lepsze dla zdjęć), max_face=10 (maks. liczba twarzy do wykrycia)
face_model = FaceDetector(True, 10)

# KROK 2: Przygotowanie modelu rozpoznawania emocji
# Wczytujemy dane treningowe z pliku CSV
emotion_model = SVM('dataset/mediapipe_train_emotions.csv', labels)

# KROK 3: Trenowanie modelu SVM
# Parametry do eksperymentowania:
# - scale: czy normalizować dane (False = nie)
# - samples_limit: ile próbek na emocję (3000 = równowaga między klasami)
# - kernel: typ kernela SVM ('rbf' = Radial Basis Function, najczęściej używany)
emotion_model.train('emotions', scale=False, samples_limit=3000, kernel='rbf')

# GŁÓWNA PĘTLA PROGRAMU - wykonuje się ciągle, klatka po klatce
while True:
    # Pobierz aktualną klatkę obrazu
    if image_mode:
        frame = img  # Dla trybu zdjęcia - zawsze ten sam obraz
    else:
        _, frame = cap.read()  # Dla kamery - nowa klatka z każdym odczytem

    # Opcjonalne skalowanie obrazu (fx, fy = współczynniki skalowania)
    # fx=1, fy=1 oznacza brak skalowania (oryginalny rozmiar)
    # EKSPERYMENT: Spróbuj fx=0.5, fy=0.5 aby przyspieszyć działanie
    frame = cv2.resize(frame, (0, 0), fx=1, fy=1)
    
    # Pobierz wymiary klatki - potrzebne do rysowania punktów na twarzy
    h, w, _ = frame.shape  # h=wysokość, w=szerokość, _=kanały koloru

    # Zmierz i wyświetl FPS (klatki na sekundę)
    # Wysokie FPS (>20) = płynne działanie, niskie FPS (<10) = opóźnienia
    FPS = fps.start()
    cv2.putText(frame, f'FPS:{int(FPS)}', (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # WYKRYWANIE TWARZY - znajduje wszystkie twarze w aktualnej klatce
    # Zwraca listę wykrytych twarzy (każda twarz = lista 468 punktów dla MediaPipe)
    faces = face_model.detect(frame)

    # Listy do przechowywania wyników dla wszystkich wykrytych twarzy
    result_pred = []  # Wartości numeryczne przewidywań (0-6)
    emotion_pred = []  # Nazwy emocji ("happy", "sad", etc.)
    
    # Przetwarzaj każdą wykrytą twarz osobno
    for i, face in enumerate(faces):
        # KROK A: Oblicz proporcje twarzy (8 wartości liczbowych)
        # To są cechy które model wykorzystuje do rozpoznania emocji
        ratio = RatioCalculator(face)
        
        # KROK B: Przewiduj emocję na podstawie proporcji
        # Model SVM zwraca liczbę zmiennoprzecinkową (np. 3.2 oznacza emocję między 3 a 4)
        result = emotion_model.predict(ratio.result())

        # Konwersja wyniku do odpowiedniego formatu
        result = result.tolist()[0]
        
        # Zabezpieczenie: ogranicz wynik do zakresu 0-6 (mamy 7 emocji)
        result = 6 if result >= 6 else result

        # Zapisz wyniki dla tej twarzy
        result_pred.append(round(result, 5))
        emotion_pred.append(labels[round(result)])  # Zamień numer na nazwę emocji

        # WIZUALIZACJA: Rysuj wszystkie 468 punktów charakterystycznych twarzy
        # To pomaga zobaczyć co system "widzi" na twarzy
        # UWAGA: Rysowanie 468 punktów może spowolnić program
        for j in range(0, 468):
            # Konwertuj znormalizowane współrzędne (0-1) na piksele
            x = int(face[j].x * w)
            y = int(face[j].y * h)
            # Narysuj małą niebieską kropkę dla każdego punktu
            cv2.circle(frame, (x, y), 2, (255, 0, 0), -1)

        # Oznacz numer twarzy na obrazie (przydatne gdy jest wiele osób)
        cv2.putText(frame, str(i), (int(face[10].x * w), int(face[10].y * h)), 0, 1, (0, 0, 255), 2)

    # Wyświetl wyniki w konsoli/terminalu
    # Format: [wartości numeryczne] - [nazwy emocji]
    # Przykład: [3.14159] - ['happy']
    print(f'{result_pred} - {emotion_pred}')

    # Sprawdź czy użytkownik nacisnął klawisz 'q' (quit = wyjście)
    # waitKey(1) czeka 1 milisekundę na naciśnięcie klawisza
    if cv2.waitKey(1) & 0xFF == ord("q"):
        print("\n=== Program zakończony przez użytkownika ===")
        break

    # Wyświetl okno z przetworzoną klatką
    # "main" to nazwa okna - możesz ją zmienić na co chcesz
    cv2.imshow("main", frame)

    # Dla trybu zdjęcia: zapisz wynik i zakończ
    if image_mode:
        cv2.imwrite("main.png", frame)  # Zapisz obraz z adnotacjami
        print("\n=== Wynik zapisany do main.png ===")
        break
