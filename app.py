from pathlib import PurePath
from http import HTTPStatus as statuses
from dotenv import load_dotenv
from common.helpers import check_filetype_allowed, get_request_data
from converterapp import create_app
from config import config
from flask import (
    after_this_request,
    jsonify,
    make_response,
    request,
    Response,
    send_file,
    send_from_directory,
)
from utils.document import PEFDocument, BRFDocument
from common.exceptions import *
import os

load_dotenv()


app = create_app()

# Document extension + translation table + data
@app.route("/translate", methods=["POST"])
def translate():

    data = request.json
    extension, filename, content, translation_table = get_request_data(data)
    file_basename = PurePath(filename).stem
    saved_file_name = f"{file_basename}.{extension}"
    file_path = PurePath(config.SAVE_DIR, saved_file_name)

    @after_this_request
    def remove_file(response):
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"Error happened while trying to remove file {e}")

        return response

    try:
        check_filetype_allowed(extension, config.ALLOWED_CONVERSIONS)
        if extension == "pef":
            document = PEFDocument(content, filename)
        elif extension == "brf":
            document = BRFDocument(content)

        generated_data = document.generate_document(translation_table)
        with open(file_path, "w") as f:
            f.write(generated_data)
        return send_file(
            file_path,
            as_attachment=True,
            download_name=saved_file_name,
            mimetype=document.file_format,
        )

        # save_path = Path.joinpath(config.SAVE_DIR, saved_file_name)
    except FileTypeNotAllowed as e:
        response = make_response(
            jsonify({"message": f"Cannot convert to file type {extension}"}),
            statuses.BAD_REQUEST,
        )
        return response
    except TranslationTableNotFound as e:
        response = make_response(
            jsonify({"message": f"Cannot translate to {translation_table}"}),
            statuses.BAD_REQUEST,
        )
    except FileNotFoundError as e:
        make_response(
            jsonify({"message": "File is not found in server"}), statuses.NOT_FOUND
        )
    except Exception as e:
        print(e)
        make_response(
            jsonify({"message": "Something bad happened"}),
            statuses.INTERNAL_SERVER_ERROR,
        )


if __name__ == "__main__":

    # import flaskapp.routes
    app.run(host=config.HOST_IP, port=config.PORT, debug=config.DEBUG)
