# Przewodnik dla kontrybutorów / Contributing Guide

## 🇵🇱 Wersja polska

### Jak pomóc w rozwoju projektu?

Dziękujemy za zainteresowanie rozwojem projektu Facial-Emotion-Recognition! Twoja pomoc jest mile widziana.

#### Zgłaszanie błędów (Issues)

Jeśli znalazłeś błąd:
1. Sprawdź czy problem nie został już zgłoszony
2. Utwórz nowy issue z dokładnym opisem:
   - Kroki do odtworzenia problemu
   - Oczekiwane zachowanie
   - Aktualne zachowanie
   - Zrzuty ekranu (jeśli dotyczy)
   - Wersja Pythona i systemu operacyjnego

#### Proponowanie nowych funkcji

Masz pomysł na ulepszenie?
1. Utwórz issue z tagiem "enhancement"
2. Opisz dokładnie proponowaną funkcjonalność
3. Wyjaśnij dlaczego byłaby przydatna
4. Zaproponuj sposób implementacji (opcjonalnie)

#### Proces tworzenia Pull Request

1. **Fork repozytorium** i utwórz swoją gałąź (branch):
   ```bash
   git checkout -b feature/nazwa-funkcji
   ```

2. **Dokonaj zmian** przestrzegając stylu kodu:
   - Używaj opisowych nazw zmiennych (po angielsku)
   - Dodawaj komentarze w języku polskim dla kluczowych fragmentów
   - Przestrzegaj PEP 8 (styl kodowania Python)

3. **Przetestuj zmiany**:
   - Upewnij się, że kod działa poprawnie
   - Sprawdź czy nie powoduje regresji

4. **Commit z opisową wiadomością**:
   ```bash
   git commit -m "Dodaj funkcję rozpoznawania mikroekspresji"
   ```

5. **Push do swojego forka**:
   ```bash
   git push origin feature/nazwa-funkcji
   ```

6. **Utwórz Pull Request**:
   - Opisz wprowadzone zmiany
   - Odnieś się do powiązanego issue (jeśli istnieje)
   - Dodaj screenshoty dla zmian UI

#### Standardy kodowania

- **Język kodu**: Nazwy zmiennych, funkcji i klas po angielsku
- **Język komentarzy**: Polski (dla ułatwienia nauki studentom)
- **Dokumentacja**: Dwujęzyczna (polski + angielski w docstringach)
- **Formatowanie**: Zgodnie z PEP 8
- **Importy**: Grupowane (standardowa biblioteka, zewnętrzne, lokalne)

#### Obszary do pomocy

Szukamy pomocy w następujących obszarach:
- 📊 Zwiększanie dokładności modelu
- ⚡ Optymalizacja wydajności
- 📝 Tłumaczenie dokumentacji na angielski
- 🧪 Dodawanie testów jednostkowych
- 🎨 Poprawa interfejsu użytkownika
- 📱 Wsparcie dla urządzeń mobilnych

---

## 🇬🇧 English Version

### How to Contribute?

Thank you for your interest in the Facial-Emotion-Recognition project! Your contributions are welcome.

#### Reporting Bugs

If you found a bug:
1. Check if the issue hasn't been reported already
2. Create a new issue with detailed description:
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Screenshots (if applicable)
   - Python version and operating system

#### Suggesting Features

Have an improvement idea?
1. Create an issue with "enhancement" tag
2. Describe the proposed functionality in detail
3. Explain why it would be useful
4. Suggest implementation approach (optional)

#### Pull Request Process

1. **Fork the repository** and create your branch:
   ```bash
   git checkout -b feature/feature-name
   ```

2. **Make changes** following code style:
   - Use descriptive variable names (in English)
   - Add comments in Polish for key sections
   - Follow PEP 8 (Python coding style)

3. **Test your changes**:
   - Ensure code works correctly
   - Check for no regressions

4. **Commit with descriptive message**:
   ```bash
   git commit -m "Add micro-expression recognition feature"
   ```

5. **Push to your fork**:
   ```bash
   git push origin feature/feature-name
   ```

6. **Create Pull Request**:
   - Describe changes made
   - Reference related issue (if exists)
   - Add screenshots for UI changes

#### Coding Standards

- **Code language**: Variable, function, and class names in English
- **Comments language**: Polish (to help students learn)
- **Documentation**: Bilingual (Polish + English in docstrings)
- **Formatting**: According to PEP 8
- **Imports**: Grouped (standard library, external, local)

#### Areas Needing Help

We're looking for help in the following areas:
- 📊 Improving model accuracy
- ⚡ Performance optimization
- 📝 Documentation translation to English
- 🧪 Adding unit tests
- 🎨 UI improvements
- 📱 Mobile device support

---

## Kodeks postępowania / Code of Conduct

- Bądź uprzejmy i szanuj innych / Be kind and respectful
- Przyjmuj konstruktywną krytykę / Accept constructive criticism
- Skup się na tym, co najlepsze dla projektu / Focus on what's best for the project
- Pomóż innym się uczyć / Help others learn

## Licencja / License

Kontrybuując do tego projektu, zgadzasz się na udostępnienie swojego wkładu na licencji MIT.

By contributing to this project, you agree to license your contribution under the MIT License.
