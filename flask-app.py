import os
from pathlib import Path
from flask import Flask, request
from logging import basicConfig, FileHandler, WARNING

from src import engine
from src.utilities import tools

SITE = Path(__file__).parent if "__file__" in globals() else Path(os.getcwd())
app  = Flask(__name__)

file_handler = FileHandler(SITE/'data'/'logs'/'errorlog.txt')
file_handler.setLevel(WARNING)


@app.route("/")
def base_route():
    return {"status": "success!", "message":  "version 1.0.3"}


@app.route("/get-user-360", methods=["POST", "GET"])
def get_user_360():
    an_input   = request.json
    
    input_file = SITE/"openapi"/"0-input-360.json"
    
    app.logger.info(f"Logged web app.\nThe input: {str(an_input)}")
    a_validation = tools.validate_input(an_input, input_file)
    if ("error" in a_validation) and a_validation["error"]:
        return a_validation["output"] 

    b_messages   = engine.process_request(an_input)
    return b_messages


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False)