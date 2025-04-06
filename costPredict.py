import pandas as pd
import pickle
import json
import sklearn

def predict(json_data):
    final_cost = 0
    try:
        input_features = ['Pocet_pokoju', 'Kuchyne', 'Plocha', 'GPS_lat', 'GPS_lon']

        print("Vstup pro predikci:", json_data)

        if isinstance(json_data, dict):
            json_data = [json_data]

        data = []
        for estate in json_data:
            ordered_estate = {}
            for key in input_features:
                value = estate.get(key)
                ordered_estate[key] = float(value)
            data.append(ordered_estate)

        df = pd.DataFrame(data)

        load_model = pickle.load(open('./Model/LinearniStrom5Featur.pkl', 'rb'))

        y_pred = load_model.predict(df)
        #print("Predikce:", y_pred)
        final_cost = y_pred[0] * 1000
        return str(int(final_cost))

    except Exception as e:
        print("Chyba při predikci:", e)
        return "Chyba: " + str(e)
    

#output = predict("./data.json")
#print(output)

#data = {'Pocet_pokoju': '5', 'Kuchyne': '1', 'Plocha': '56', 'GPS_lat': '50.0471543', 'GPS_lon': '14.0013247', 'rekonstuovano': '0', 'parkovani': '0', 'sklep': '0'}
#print(predict(data))
