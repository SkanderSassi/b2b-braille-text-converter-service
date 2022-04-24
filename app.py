from dotenv import load_dotenv
from converterapp import create_app
from config import config
from flask import jsonify, request
import json
import pprint
load_dotenv()



app = create_app()


@app.route('/convert', methods=['POST'])
def convert():
    data = request.json
    pprint.pprint(data)
    pass

    

if __name__ == '__main__':

    # import flaskapp.routes
    app.run(host=config.HOST_IP,
            port=config.PORT,
            debug=config.DEBUG)