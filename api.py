from flask import Flask, request, make_response
from flask_cors import CORS
from costPredict import predict
import logging

app = Flask(__name__)
CORS(app)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="application.log",
    filemode="a",
    encoding="utf-8"
)

@app.route('/api/predict', methods=['POST'])
def predict_cost():
    estate = request.get_json()
    #print(estate)
    logging.info(f"Api recieved {estate}")
    try:
        cost = predict(estate)
    except Exception as e:
        logging.error(f"Error: {e}")
    else:
        logging.info(f"Model predicted {cost}")
        return make_response(cost, 200)
    
if __name__ == "__main__":
    ip = "127.0.0.1"
    port = 65523
    debug = True
    if(not None in [ip,port,debug]):
        app.run(ip,port,debug)
    else:
        print("Selhalo nastartování api")









