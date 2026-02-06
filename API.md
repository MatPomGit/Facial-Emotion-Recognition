# Dokumentacja API / API Documentation

## 🇵🇱 Polski

### Klasy i Moduły

#### 1. FaceDetector (wykrywanie twarzy)

**Lokalizacja:**
- MediaPipe: `modules/mediapipe/mediapipe_FaceLandmarks.py`
- Dlib: `modules/dlib/dlib_FaceLandmarks.py`

**Konstruktor:**
```python
FaceDetector(static_image_mode: bool = True, max_num_faces: int = 10)
```

**Parametry:**
- `static_image_mode` (bool): True dla zdjęć, False dla wideo
- `max_num_faces` (int): Maksymalna liczba wykrywanych twarzy

**Metody:**

##### detect(image)
Wykrywa twarze na obrazie i zwraca listę punktów charakterystycznych.

**Parametry:**
- `image` (numpy.ndarray): Obraz w formacie BGR (OpenCV)

**Zwraca:**
- `list`: Lista twarzy, każda twarz to lista punktów (468 dla MediaPipe, 68 dla Dlib)

**Przykład:**
```python
from modules.mediapipe.mediapipe_FaceLandmarks import FaceDetector
import cv2

detector = FaceDetector(static_image_mode=True, max_num_faces=5)
image = cv2.imread('photo.jpg')
faces = detector.detect(image)

for face in faces:
    print(f"Wykryto twarz z {len(face)} punktami")
```

---

#### 2. RatioCalculator (obliczanie proporcji)

**Lokalizacja:**
- MediaPipe: `modules/mediapipe/ratio_calc.py`
- Dlib: `modules/dlib/ratio_calc.py`

**Konstruktor:**
```python
RatioCalculator(face_landmarks: list)
```

**Parametry:**
- `face_landmarks` (list): Lista punktów charakterystycznych twarzy

**Metody:**

##### result()
Zwraca 8 obliczonych proporcji twarzy.

**Zwraca:**
- `list[float]`: Lista 8 wartości zmiennoprzecinkowych [a1, a2, a3, a4, a5, a6, a7, a8]

**Proporcje:**
- a1: Szerokość ust / Szerokość twarzy
- a2: Wysokość ust / Wysokość twarzy
- a3: Otwarcie lewego oka / Szerokość twarzy
- a4: Otwarcie prawego oka / Szerokość twarzy
- a5: Wysokość lewej brwi / Wysokość twarzy
- a6: Wysokość prawej brwi / Wysokość twarzy
- a7: Kąt ust (lewy)
- a8: Kąt ust (prawy)

**Przykład:**
```python
from modules.mediapipe.ratio_calc import RatioCalculator

# Zakładając, że mamy wykrytą twarz
ratio_calc = RatioCalculator(face)
ratios = ratio_calc.result()
print(f"Proporcje twarzy: {ratios}")
```

---

#### 3. SVM (klasyfikator emocji)

**Lokalizacja:** `modules/svm.py`

**Konstruktor:**
```python
SVM(dataset: str, labels: list)
```

**Parametry:**
- `dataset` (str): Ścieżka do pliku CSV z danymi treningowymi
- `labels` (list): Lista etykiet emocji w kolejności [0-6]

**Metody:**

##### train(label: str, scale: bool = False, samples_limit: int = None, kernel: str = 'rbf')
Trenuje model SVM na podstawie danych z CSV.

**Parametry:**
- `label` (str): Nazwa kolumny z etykietami w CSV (zwykle "emotions")
- `scale` (bool): Czy normalizować dane przed trenowaniem
- `samples_limit` (int): Maksymalna liczba próbek na klasę (None = wszystkie)
- `kernel` (str): Typ kernela SVM ('rbf', 'poly', 'linear', 'sigmoid')

**Przykład:**
```python
from modules.svm import SVM

labels = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
model = SVM('dataset/mediapipe_train_emotions.csv', labels)
model.train('emotions', scale=False, samples_limit=3000, kernel='rbf')
```

##### predict(data: list)
Przewiduje emocję na podstawie proporcji twarzy.

**Parametry:**
- `data` (list): Lista 8 wartości proporcji twarzy

**Zwraca:**
- `numpy.ndarray`: Wartość zmiennoprzecinkowa 0-6 reprezentująca emocję

**Przykład:**
```python
# Zakładając wytrenowany model i obliczone proporcje
emotion_value = model.predict(ratios)
emotion_index = round(emotion_value.tolist()[0])
emotion_name = labels[emotion_index]
print(f"Przewidziana emocja: {emotion_name}")
```

---

#### 4. FPS (pomiar wydajności)

**Lokalizacja:** `modules/fps.py`

**Konstruktor:**
```python
FPS()
```

**Metody:**

##### start()
Oblicza i zwraca aktualny FPS.

**Zwraca:**
- `float`: Liczba klatek na sekundę

**Przykład:**
```python
from modules.fps import FPS

fps_counter = FPS()

while True:
    # Twoja logika przetwarzania
    current_fps = fps_counter.start()
    print(f"FPS: {current_fps:.2f}")
```

---

### Kompletny Przykład Użycia

```python
from modules.mediapipe.mediapipe_FaceLandmarks import FaceDetector
from modules.mediapipe.ratio_calc import RatioCalculator
from modules.svm import SVM
from modules.fps import FPS
import cv2

# Inicjalizacja
labels = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
face_detector = FaceDetector(static_image_mode=False, max_num_faces=5)
emotion_model = SVM('dataset/mediapipe_train_emotions.csv', labels)
emotion_model.train('emotions', scale=False, samples_limit=3000, kernel='rbf')
fps = FPS()

# Otwórz kamerę
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Pomiar FPS
    current_fps = fps.start()
    
    # Wykryj twarze
    faces = face_detector.detect(frame)
    
    # Przetwórz każdą twarz
    for face in faces:
        # Oblicz proporcje
        ratio_calc = RatioCalculator(face)
        ratios = ratio_calc.result()
        
        # Przewiduj emocję
        emotion_value = emotion_model.predict(ratios)
        emotion_index = round(emotion_value.tolist()[0])
        emotion_name = labels[min(emotion_index, 6)]
        
        print(f"Emocja: {emotion_name}, FPS: {current_fps:.1f}")
    
    # Wyświetl
    cv2.imshow('Facial Emotion Recognition', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

---

## 🇬🇧 English

### Classes and Modules

[The English version follows the same structure as Polish, with identical code examples]

#### 1. FaceDetector (face detection)

**Location:**
- MediaPipe: `modules/mediapipe/mediapipe_FaceLandmarks.py`
- Dlib: `modules/dlib/dlib_FaceLandmarks.py`

**Constructor:**
```python
FaceDetector(static_image_mode: bool = True, max_num_faces: int = 10)
```

**Parameters:**
- `static_image_mode` (bool): True for images, False for video
- `max_num_faces` (int): Maximum number of faces to detect

**Methods:**

##### detect(image)
Detects faces in image and returns list of landmarks.

**Parameters:**
- `image` (numpy.ndarray): Image in BGR format (OpenCV)

**Returns:**
- `list`: List of faces, each face is a list of points (468 for MediaPipe, 68 for Dlib)

---

#### 2. RatioCalculator (ratio calculation)

**Location:**
- MediaPipe: `modules/mediapipe/ratio_calc.py`
- Dlib: `modules/dlib/ratio_calc.py`

**Constructor:**
```python
RatioCalculator(face_landmarks: list)
```

**Methods:**

##### result()
Returns 8 calculated facial ratios.

**Returns:**
- `list[float]`: List of 8 floating-point values [a1, a2, a3, a4, a5, a6, a7, a8]

---

#### 3. SVM (emotion classifier)

**Location:** `modules/svm.py`

**Constructor:**
```python
SVM(dataset: str, labels: list)
```

**Methods:**

##### train(label: str, scale: bool = False, samples_limit: int = None, kernel: str = 'rbf')
Trains the SVM model using data from CSV.

##### predict(data: list)
Predicts emotion based on facial ratios.

---

#### 4. FPS (performance measurement)

**Location:** `modules/fps.py`

**Methods:**

##### start()
Calculates and returns current FPS.

**Returns:**
- `float`: Frames per second

---

### Complete Usage Example

[Same code example as in Polish section]

---

## 📝 Notatki / Notes

### Formaty Danych / Data Formats

**CSV Format (training data):**
```
a1,a2,a3,a4,a5,a6,a7,a8,emotions
0.123,0.456,0.789,0.234,0.567,0.890,45.2,44.8,happy
0.234,0.345,0.456,0.567,0.678,0.789,50.1,49.9,sad
...
```

**Landmark Format:**
- MediaPipe: 468 points, each with `x`, `y`, `z` attributes (normalized 0-1)
- Dlib: 68 points, each as tuple `(x, y)` (pixel coordinates)

### Obsługiwane Kernele SVM / Supported SVM Kernels

- `'rbf'` - Radial Basis Function (domyślny/default, najlepszy dla większości przypadków)
- `'poly'` - Polynomial
- `'linear'` - Linear
- `'sigmoid'` - Sigmoid

### Zakres Wartości / Value Ranges

- **Emotion prediction:** 0.0 - 6.0 (continuous)
- **Ratios (a1-a8):** 0.0 - 1.0 (normalized, except angles which can be 0-90 degrees)
- **FPS:** Typically 5-60 depending on hardware
