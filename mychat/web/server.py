
from flask import Flask, render_template, request

import requests
import json
REQUEST_URL = "http://localhost:5005/webhooks/rest/webhook"
HEADER = {'Content-Type':'application/json; charset=utf-8'}


app = Flask(__name__, static_url_path='')


def Botresponse(sender, meg):
    requestDict = {"sender": sender, "message": meg}
    rsp = requests.post(REQUEST_URL, data=json.dumps(requestDict), headers=HEADER)
    if rsp.status_code == 200:
        rspJson = json.loads(rsp.text.encode())
        return rspJson[0]["text"]
    else:
        return ""


########################################


@app.route('/', methods=['GET', 'POST'])
def view():
    return render_template('index.html')


@app.route('/chat', methods=['GET'])
def response():
    data = request.args.to_dict()
    message = data['message']
    if message != '':
        answer = Botresponse("user1", message)
        return answer


@app.route('/forget', methods=['GET'])
def forget():
    return 'success'


if __name__ == '__main__':
    print("web init success!")
    app.run('0.0.0.0','5150', debug=True)
