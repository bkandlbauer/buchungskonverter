# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

from firebase_functions import https_fn, options
from firebase_admin import initialize_app
import subprocess
from convert_lotto import xml_to_csv_lotto
from convert_tipp3 import xml_to_csv_tipp3

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/lotto", methods=["POST"])
def handle_post_lotto():

    # Ensure it's XML content
    if request.content_type != "application/xml":
        return jsonify({"error": "Unsupported content type"}), 400
    
    xml_content = request.data.decode("utf-8")  # Read XML content
    print(xml_content)
    response = xml_to_csv_lotto(xml_content)  # Call function with XML content
    
    return response, 200 

@app.route("/tipp3", methods=["POST"])
def handle_post_tipp3():

    # Ensure it's XML content
    if request.content_type != "application/xml":
        return jsonify({"error": "Unsupported content type"}), 400
    
    xml_content = request.data.decode("utf-8")  # Read XML content
    print(xml_content)
    response = xml_to_csv_tipp3(xml_content)  # Call function with XML content
    
    return response, 200 

initialize_app()

@https_fn.on_request(cors=options.CorsOptions(cors_origins="*", cors_methods=["get", "post"]))
def on_request_example(req: https_fn.Request) -> https_fn.Response:
    with app.request_context(req.environ):
        return app.full_dispatch_request()



