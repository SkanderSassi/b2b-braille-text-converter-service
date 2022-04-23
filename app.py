from dotenv import load_dotenv
from translateapp import create_app
from config import config

load_dotenv()



app = create_app()


if __name__ == '__main__':

    # import flaskapp.routes
    app.run(host=config.HOST_IP,
            port=config.PORT,
            debug=config.DEBUG)