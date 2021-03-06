from flask import Flask, render_template, flash, request
import requests
from os import environ

app = Flask(__name__)


def tfserving_request(req_input, model_name):
    # Use this if using Docker compose
    # url = f"http://server:8501/v1/models/{model_name}:predict"
    # This is configured to match the kubernetes service: tf-cluster-ip-service
    url = f"http://tf-cluster-ip-service:8501/v1/models/{model_name}:predict"

    input_request = {"instances": [req_input]}
    response = requests.post(url=url, json=input_request)
    return response


@app.route("/home", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        inp1 = int(request.form["inp1"])
        inp2 = int(request.form["inp2"])

        response = tfserving_request([inp1, inp2], "1628956907")

        resp = response.json()
        print(resp)
        flash(f"obtained {inp1} and {inp2} have a prediction of {resp['predictions']}", 'success')

    return render_template("index.html")


app.secret_key = "nlhkjtgjhfhvhjfyfgcjgdtdgcngcghdt"
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(environ.get('PORT', 8080)))
