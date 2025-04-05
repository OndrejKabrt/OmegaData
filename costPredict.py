import pandas as pd
import pickle
import json
import sklearn

def predict(json_path):
    input_features = ['Pocet_pokoju', 'Kuchyne', 'Plocha', 'GPS_lat', 'GPS_lon']

    with open(json_path, 'r', encoding='utf-8') as file:
        estate_data = json.load(file)

    data = []

    for estate in estate_data:
        ordered_estate = {}
        for i in range(len(input_features)):
            key = input_features[i]
            value = estate.get(key)
            ordered_estate[key] = value
        data.append(ordered_estate)

    df = pd.DataFrame(data)

    load_model = pickle.load(open('./Model/LinearniStrom5Featur.pkl', 'rb'))

    y_pred = load_model.predict(df)
    final_cost = y_pred * 1000
    return f"{final_cost} Kč."

#output = predict("./data.json")
#print(output)