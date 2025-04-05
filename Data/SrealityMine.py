import requests
import re
import json

base_url = "https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&category_type_cb=1&per_page=20&page="

for i in range(1, 5):
    current_url = base_url + str(i)
    response = requests.get(current_url)
    print(f"Fetching: {current_url}")

    if response.status_code == 200:
        data = response.json()
        # Print each estate on a separate line with more details
        for estate in data["_embedded"]["estates"]:
            # Basic information
            name = estate.get('name', 'Neuvedeno')
            locality = estate.get('locality', 'Neuvedeno')
            price = estate.get('price', 'Neuvedeno')
            hash_id = estate.get('hash_id', '')

            # Create direct link to property page
            property_url = f"https://www.sreality.cz/detail/prodej/byt//{estate.get('seo', {}).get('locality', '')}/{hash_id}"

            # Extract layout and area from the name
            layout = "Neuvedeno"
            layout_match = re.search(r'Prodej bytu (\d\+\w+)', name)
            if layout_match:
                layout = layout_match.group(1)

            area = "Neuvedeno"
            area_match = re.search(r'(\d+)\s*m²', name)
            if area_match:
                area = area_match.group(1) + " m²"

            # GPS coordinates
            gps = estate.get('gps', {})
            lat = gps.get('lat', 'Neuvedeno')
            lon = gps.get('lon', 'Neuvedeno')

            # Property features/labels
            labels = estate.get('labels', [])
            labels_str = ", ".join(labels) if labels else "Neuvedeno"

            # Check if it's a new building
            is_new_building = "Ano" if "Novostavba" in labels else "Ne"

            # Extract civic amenities from labelsAll if available
            civic_amenities = []
            if 'labelsAll' in estate and len(estate['labelsAll']) > 1:
                # The second list in labelsAll usually contains civic amenities
                for amenity in estate['labelsAll'][1]:
                    # Map API values to more readable Czech names
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

            # Building type and other features from labelsAll
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

            # Print formatted output
            print(f"Název: {name}")
            print(f"Dispozice: {layout}")
            print(f"Lokalita: {locality}")
            print(f"Cena: {price:,} Kč".replace(",", " "))
            print(f"Plocha: {area}")
            print(f"GPS: {lat}, {lon}")
            print(f"Vlastnosti budovy: {building_features_str}")
            print(f"Občanská vybavenost: {civic_amenities_str}")
            print(f"Novostavba: {is_new_building}")

            # Get main image URL if available
            if '_links' in estate and 'images' in estate['_links'] and estate['_links']['images']:
                main_image = estate['_links']['images'][0].get('href', 'Neuvedeno')
                print(f"Hlavní obrázek: {main_image}")

            # Add link to property page
            print(f"Odkaz na detail: {property_url}")

            print("-" * 60)  # Separator between estates

        print("=" * 80)  # Separator between pages
    else:
        print(f"Chyba při získávání dat. Status code: {response.status_code}")