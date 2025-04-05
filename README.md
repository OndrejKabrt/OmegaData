# OmegaData
# Webová Aplikace na Odhadování Ceny Bytů

Tato webová aplikace slouží k odhadování ceny bytů na základě zadaných parametrů. Je postavena na HTML s javascriptem na front-endu a Python API na back-endu. Aplikace využívá model strojového učení k predikci ceny nemovitosti.

## Architektura projektu

### Frontend
- Čisté HTML s minimálním CSS (využití frameworku Bootstrap)
- JavaScript pro sběr dat z formuláře a interakci s mapou
- Formulář obsahuje následující vstupy:
  - Počet pokojů
  - Plocha bytu
  - Přítomnost kuchyně (Ano/Ne)
  - Lokace bytu (vybírá se na mapě, získává se zeměpisná šířka a délka)

### Backend
- Python API, které přijímá data z formuláře
- Zpracovává data do formátu požadovaného modelem
- Využívá model k predikci ceny bytu
- Vrací odhadovanou cenu v korunách českých zpět na frontend

### Model
- Random Forest Regression model
- Trénován na přibližně 3200 záznamech z webu Sreality (https://www.sreality.cz/)
- Vybrán na základě nejnižší chybovosti v porovnání s jinými modely

## Instalace a spuštění

Pro spuštění aplikace postupujte následovně:

1. Stáhněte si tento repozitář z Githubu
2. Otevřete příkazový řádek ve složce projektu a proveďte následující příkazy:
   ```bash
   python -m venv venv
   .\venv\Scripts\pip.exe install -r .\requirements.txt
   ```
3. Spusťte soubor `api.py`:
   ```bash
   python api.py
   ```

Po provedení těchto kroků by měl být backend připraven přijímat data z hlavní HTML stránky.

## Trénování modelu

Pro predikci cen bytů byl zvolen model Random Forest Regressor. Tento model byl vybrán na základě porovnání s několika dalšími modely:

- Random Forest Regressor
- AdaBoost Regressor
- Lineární regrese
- Gradient Boosting Regressor
- Neuronová síť

Random Forest Regressor dosáhl nejmenší chybovosti ze všech testovaných modelů. Neuronová síť naopak dosahovala nejhorších výsledků.

Detailní informace o procesu trénování a testování modelů jsou k dispozici v Google Colab sešitu, který je přiložen v repozitáři ve složce `Model`.

## Struktura projektu

- **Root**
  - `index.html` - hlavní stránka aplikace
  - `api.py` - backend API
  - `requirements.txt` - seznam potřebných Python balíčků
  - `script.js` - soubor obsahující javascript potřebný pro funkčnost
  - `costPredict.py` - kod, ve kterém se data vkládají do modelu, který pak vrací odhadovanou cenu
  - **/Data** - složka obsahující trénovací data a skripty pro sběr dat
  - **/Model** - složka obsahující Google Colab sešit s procesem trénování modelu a samotným modelem
  - **/venv** - virtuální prostředí Pythonu (vytvoří se při instalaci)

## Zdroje a konzultace

Projekt byl vytvořen s pomocí konzultací se spolužáky:
- Adam Hlaváčik
- Martin Hornych
- Tomáš Križko

### Externí zdroje:
- https://chatgpt.com/share/67f18bc9-9bac-8004-b204-6144dde9be32
- https://youtu.be/DqyJFV7QJqc?si=yLD0Kn5MuFlzPXpl