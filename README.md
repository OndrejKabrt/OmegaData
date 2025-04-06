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
- Za ceny predikované tímto modelem nijak neručím, protože tento model není 100% přesný a nebere v potaz všechny aspekty potřebné pro určení přesné ceny.

## Instalace a spuštění

Pro spuštění aplikace postupujte následovně:

1. Stáhněte si tento repozitář z Githubu
2. Otevřete příkazový řádek ve složce projektu a proveďte následující příkazy:
   ```bash
   python -m venv venv
   .\venv\Scripts\pip.exe install -r .\requirements.txt
   ```
3. Spusťte soubor `.\venv\Scripts\python.exe .\api.py`:
   ```bash
   .\venv\Scripts\python.exe .\api.py
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
- https://claude.ai/share/a5f4c6ab-6a29-41b3-b2c7-558a506a081e

==============================================================================================================

# Web Application for Apartment Price Estimation

This web application is used to estimate apartment prices based on input parameters. It is built on HTML with JavaScript on the front-end and a Python API on the back-end. The application uses a machine learning model to predict property prices.

## Project Architecture

### Frontend
- Clean HTML with minimal CSS (using Bootstrap framework)
- JavaScript for collecting form data and map interaction
- The form includes the following inputs:
  - Number of rooms
  - Apartment area
  - Presence of a kitchen (Yes/No)
  - Apartment location (selected on a map, providing latitude and longitude)

### Backend
- Python API that receives data from the form
- Processes data into the format required by the model
- Uses the model to predict apartment prices
- Returns the estimated price in Czech crowns back to the frontend

### Model
- Random Forest Regression model
- Trained on approximately 3200 records from the Sreality website (https://www.sreality.cz/)
- Selected based on the lowest error rate compared to other models
- I do not guarantee the prices predicted by this model, as this model is not 100% accurate and does not take into account all aspects necessary to determine an accurate price.

## Installation and Launch

To run the application, follow these steps:

1. Download this repository from Github
2. Open the command line in the project folder and run the following commands:
   ```bash
   python -m venv venv
   .\venv\Scripts\pip.exe install -r .\requirements.txt
   ```
3. Run the `.\venv\Scripts\python.exe .\api.py` file:
   ```bash
   .\venv\Scripts\python.exe .\api.py
   ```

After completing these steps, the backend should be ready to receive data from the main HTML page.

## Model Training

A Random Forest Regressor was chosen for predicting apartment prices. This model was selected after comparison with several other models:

- Random Forest Regressor
- AdaBoost Regressor
- Linear Regression
- Gradient Boosting Regressor
- Neural Network

The Random Forest Regressor achieved the lowest error rate of all tested models. The Neural Network, conversely, produced the worst results.

Detailed information about the training and testing process of the models is available in the Google Colab notebook included in the repository in the `Model` folder.

## Project Structure

- **Root**
  - `index.html` - main application page
  - `api.py` - backend API
  - `requirements.txt` - list of required Python packages
  - `script.js` - file containing JavaScript needed for functionality
  - `costPredict.py` - code that inputs data into the model, which then returns the estimated price
  - **/Data** - folder containing training data and data collection scripts
  - **/Model** - folder containing the Google Colab notebook with the model training process and the model itself
  - **/venv** - Python virtual environment (created during installation)

## Resources and Consultations

The project was created with consultation assistance from classmates:
- Adam Hlaváčik
- Martin Hornych
- Tomáš Križko

### External Sources:
- https://chatgpt.com/share/67f18bc9-9bac-8004-b204-6144dde9be32
- https://youtu.be/DqyJFV7QJqc?si=yLD0Kn5MuFlzPXpl
- https://claude.ai/share/a5f4c6ab-6a29-41b3-b2c7-558a506a081e