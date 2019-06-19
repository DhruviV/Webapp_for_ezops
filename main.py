import os
import pandas as pd
from flask import Flask,render_template,request
import requests
import csv
import json
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')
@app.route('/copy',methods=['GET','POST'])
def copy():
    with open("static/titanic_data.csv") as f:
        with open("copy.txt", "w") as f1:
            for line in f:
                f1.write(line)
    return render_template("output.html")
@app.route('/reverse',methods=['GET','POST'])
def reverse():
    df = pd.read_csv('static/titanic_data.csv')
    columns = df.columns.tolist()
    columns = columns[::-1]
    df = df[columns]
    df.to_csv("new_output.csv", index=False, encoding='utf8')

    with open("new_output.csv") as f:
        with open("reverse.txt", "w")as f1:
            for line in f:
                f1.write(line)
    return render_template('Reverse.html')

@app.route('/Yahoo',methods=['GET','POST'])
def yahoo():
    class Solution:
        print("hi")

        version = '0.3'

        def __init__(self, url, headers):

            self.url = url
            self.headers = {}
            self.headers["X-RapidAPI-Host"] = headers["X-RapidAPI-Host"]
            self.headers["X-RapidAPI-Key"] = headers["X-RapidAPI-Key"]
            self.response = None
            # print(self.headers)
            # print(self.url)

        def get_yahoo_mover(self):
            self.response = requests.get(self.url, headers=self.headers)
            response = requests.get(
                "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/get-movers?region=US&lang=en",
                headers={"X-RapidAPI-Host": "apidojo-yahoo-finance-v1.p.rapidapi.com",
                         "X-RapidAPI-Key": "6318b59f73mshb5cfc92e481ad2ep1bb42ajsnef89d77165e3"})
            print(self.response.status_code)
            print(self.response.headers['content-type'])
            if self.response is not None:
                return True
            return False

        def write_csv(self, file_name):

            count = 0
            assert self.response.status_code == 200
            fin_data = open(file_name, 'w')
            csvwriter = csv.writer(fin_data)
            for fin in self.response.json()[u'result']:
                if count == 0:
                    header = fin.keys()
                    csvwriter.writerow(header)
                    count += 1
                csvwriter.writerow(fin.values())

        def save_json(self, json_file_name):

            assert self.response.status_code == 200
            with open(json_file_name, 'w') as json_file:
                json.dump(self.response.json(), json_file)

    def main():
        query_status = None
        url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/get-movers?region=US&lang=en"
        headers = {}
        headers["X-RapidAPI-Host"] = "apidojo-yahoo-finance-v1.p.rapidapi.com"
        headers["X-RapidAPI-Key"] = ""  # Please put the key here

        solution = Solution(url, headers)
        query_status = solution.get_yahoo_mover()

        assert query_status is True
        solution.save_json(json_file_name='yahoo.json')
        solution.write_csv(file_name='dhruvi_test.csv')
        main()
    return render_template('yahoo.html')


port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))
