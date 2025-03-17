import requests
import re
import json
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
        "Název", "Dispozice", "Lokalita", "Cena", "Plocha",
        "GPS_lat", "GPS_lon", "Vlastnosti_budovy", "Občanská_vybavenost",
        "Novostavba", "Hlavní_obrázek", "Odkaz_na_detail"
    ]

    # Zápis dat do CSV souboru
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for estate in estates_data:
            writer.writerow(estate)

    print(f"Data byla úspěšně uložena do souboru: {filename}")
    return filename


def format_price(price):
    """Formátuje cenu do čitelného formátu"""
    if isinstance(price, int):
        return f"{price:,}".replace(",", " ")
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

    for i in range(1, 150):
        current_url = base_url + str(i)
        print(f"Fetching: {current_url}")

        response = requests.get(current_url)

        if response.status_code == 200:
            data = response.json()

            for estate in data["_embedded"]["estates"]:
                # Základní informace
                name = estate.get('name', 'Neuvedeno')
                locality = estate.get('locality', 'Neuvedeno')
                price = estate.get('price', 'Neuvedeno')
                hash_id = estate.get('hash_id', '')

                # Vytvoření přímého odkazu na stránku nemovitosti
                property_url = f"https://www.sreality.cz/detail/prodej/byt//{estate.get('seo', {}).get('locality', '')}/{hash_id}"

                # Extrakce dispozice a plochy z názvu
                layout = "Neuvedeno"
                layout_match = re.search(r'Prodej bytu (\d\+\w+)', name)
                if layout_match:
                    layout = layout_match.group(1)

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
                labels_str = ", ".join(labels) if labels else "Neuvedeno"

                # Kontrola, zda jde o novostavbu
                is_new_building = "Ano" if "Novostavba" in labels else "Ne"

                # Extrakce občanské vybavenosti z labelsAll
                civic_amenities = []
                if 'labelsAll' in estate and len(estate['labelsAll']) > 1:
                    # Druhý seznam v labelsAll obvykle obsahuje občanskou vybavenost
                    for amenity in estate['labelsAll'][1]:
                        # Mapování hodnot API na čitelnější české názvy
                        amenity_mapping = {
                            'theater': 'Divadlo',
                            'vet': 'Veterinář',
                            'small_shop': 'Obchůdek',
                            'movies': 'Kino',
                            'candy_shop': 'Cukrárna',
                            'tavern': 'Hospoda',
                            'playground': 'Dětské hřiště',
                            'sightseeing': 'Památky',
                            'natural_attraction': 'Příroda',
                            'school': 'Škola',
                            'restaurant': 'Restaurace',
                            'tram': 'Tramvaj',
                            'medic': 'Lékař',
                            'metro': 'Metro',
                            'bus_public_transport': 'Autobus',
                            'kindergarten': 'Školka',
                            'sports': 'Sport',
                            'shop': 'Obchod',
                            'post_office': 'Pošta',
                            'train': 'Vlak',
                            'atm': 'Bankomat',
                            'drugstore': 'Lékárna'
                        }
                        readable_name = amenity_mapping.get(amenity, amenity)
                        civic_amenities.append(readable_name)

                civic_amenities_str = ", ".join(civic_amenities) if civic_amenities else "Neuvedeno"

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

                # Získání URL hlavního obrázku, pokud je k dispozici
                main_image = "Neuvedeno"
                if '_links' in estate and 'images' in estate['_links'] and estate['_links']['images']:
                    main_image = estate['_links']['images'][0].get('href', 'Neuvedeno')

                # Vytvoření slovníku s informacemi o nemovitosti
                estate_data = {
                    "Název": name,
                    "Dispozice": layout,
                    "Lokalita": locality,
                    "Cena": format_price(price),
                    "Plocha": area,
                    "GPS_lat": lat,
                    "GPS_lon": lon,
                    "Vlastnosti_budovy": building_features_str,
                    "Občanská_vybavenost": civic_amenities_str,
                    "Novostavba": is_new_building,
                    "Hlavní_obrázek": main_image,
                    "Odkaz_na_detail": property_url
                }

                # Přidání dat o nemovitosti do seznamu
                all_estates.append(estate_data)

                # Výpis informací do konzole
                print(f"Název: {name}")
                print(f"Dispozice: {layout}")
                print(f"Lokalita: {locality}")
                print(f"Cena: {format_price(price)} Kč")
                print(f"Plocha: {area}")
                print(f"GPS: {lat}, {lon}")
                print(f"Vlastnosti budovy: {building_features_str}")
                print(f"Občanská vybavenost: {civic_amenities_str}")
                print(f"Novostavba: {is_new_building}")
                print(f"Hlavní obrázek: {main_image}")
                print(f"Odkaz na detail: {property_url}")
                print("-" * 60)  # Oddělovač mezi nemovitostmi

            print("=" * 80)  # Oddělovač mezi stránkami
        else:
            print(f"Chyba při získávání dat. Status code: {response.status_code}")

    return all_estates


if __name__ == "__main__":
    # Počet stránek, které chceme stáhnout
    num_pages = 4

    # Získání dat
    estates_data = fetch_sreality_data(num_pages)

    # Uložení dat do CSV
    save_to_csv(estates_data, "Kabrt")