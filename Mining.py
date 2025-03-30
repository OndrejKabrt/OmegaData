import requests
import re
import csv
from datetime import datetime


def save_to_csv(estates_data, filename=None):
    """
    Uloží data o nemovitostech do CSV souboru.

    Args:
        estates_data: List slovníků s informacemi o nemovitostech
        filename: Název výstupního souboru (volitelný)

    Returns:
        Název vytvořeného souboru
    """
    if filename is None:
        # Vytvoření názvu souboru s aktuálním datem a časem
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"sreality_export_{current_time}.csv"

    # Definice hlavičky CSV souboru
    fieldnames = [
        "Pocet_pokoju","Kuchyne", "Cena", "Plocha",
        "GPS_lat", "GPS_lon",
        "Novostavba", "Rekonstuovano", "Vytah", "Parkovani", "Sklep", "Balkon"
    ]

    # Zápis dat do CSV souboru
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for estate in estates_data:
            null_in = 0
            null_cost = 0
            for key,val in estate.items():
                if re.match("Neuvedeno", str(val)):
                    null_in += 1
                elif re.match("Cena", str(key)) and int(val) == 0:
                    null_cost += 1
            if (null_in == 0) and (null_cost == 0):
                writer.writerow(estate)

    print(f"Data byla úspěšně uložena do souboru: {filename}")
    return filename

def format_price(price):
    """Formátuje cenu do čitelného formátu"""
    if isinstance(price, int):
        return f"{price:,}".replace(",", "")
    return str(price)


# Hlavní funkce pro získání dat
def fetch_sreality_data(pages=4):
    """
    Získá data o nemovitostech z API sreality.cz

    Args:
        pages: Počet stránek ke stažení

    Returns:
        List slovníků s informacemi o nemovitostech
    """
    base_url = "https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&category_type_cb=1&per_page=20&page="
    all_estates = []

    for i in range(1, 175):
        current_url = base_url + str(i)
        print(f"Fetching: {current_url}")

        response = requests.get(current_url)

        if response.status_code == 200:
            data = response.json()

            for estate in data["_embedded"]["estates"]:
                # Základní informace
                name = estate.get('name', 'Neuvedeno')
                price = estate.get('price', 'Neuvedeno')


                # Extrakce dispozice a plochy z názvu
                layout = "Neuvedeno"
                room_number = "Neuvedeno"
                kitchen = "Neuvedeno"
                layout_match = re.search(r'Prodej bytu (\d\+\w+)', name)
                if layout_match:
                    layout = layout_match.group(1)
                    if re.match("^\d+\+kk$", layout):
                        s = layout.split("+")
                        room_number = s[0]
                        kitchen = "1"
                    elif re.match("^\d+\+\d+$", layout):
                        s = layout.split("+")
                        room_number = int(s[0]) + int(s[1])
                        kitchen = "0"
                    else:
                        room_number = layout
                        kitchen = "0"

                area = "Neuvedeno"
                area_match = re.search(r'(\d+)\s*m²', name)
                if area_match:
                    area = area_match.group(1) # + " m²"

                # GPS souřadnice
                gps = estate.get('gps', {})
                lat = gps.get('lat', 'Neuvedeno')
                lon = gps.get('lon', 'Neuvedeno')


                # Vlastnosti nemovitosti
                labels = estate.get('labels', [])


                
                # Typ budovy a další vlastnosti z labelsAll
                building_features = []
                if 'labelsAll' in estate and len(estate['labelsAll']) > 0:
                    feature_mapping = {
                        'personal': 'Osobní vlastnictví',
                        'brick': 'Cihlová stavba',
                        'cellar': 'Sklep',
                        'elevator': 'Výtah',
                        'terrace': 'Terasa',
                        'new_building': 'Novostavba'
                    }

                    for feature in estate['labelsAll'][0]:
                        readable_name = feature_mapping.get(feature, feature)
                        building_features.append(readable_name)

                building_features_str = ", ".join(building_features) if building_features else "Neuvedeno"

                # Kontrola, zda jde o novostavbu
                is_new_building = "1" if "Novostavba" in labels else "0"
                is_reconstructed = "1" if "Po rekonstrukci" in labels else "0"
                have_lift = "1" if "Výtah" in building_features_str else "0"
                have_parking = "1" if "parking_lots" in building_features_str else "0"
                have_basement = "1" if "Sklep" in building_features_str else "0"
                have_balcony = "1" if "balcony" in building_features_str else "0"

                # Vytvoření slovníku s informacemi o nemovitosti
                estate_data = {
                    "Pocet_pokoju": room_number,
                    "Kuchyne": kitchen,
                    "Cena": format_price(price),
                    "Plocha": area,
                    "GPS_lat": lat,
                    "GPS_lon": lon,
                    "Novostavba": is_new_building,
                    "Rekonstuovano" : is_reconstructed, 
                    "Vytah": have_lift, 
                    "Parkovani": have_parking, 
                    "Sklep": have_basement,
                    "Balkon": have_balcony
                }

                all_estates.append(estate_data)

            

    return all_estates


if __name__ == "__main__":
    num_pages = 50

    estates_data = fetch_sreality_data(num_pages)

    save_to_csv(estates_data, "Kabrt")