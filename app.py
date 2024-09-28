from flask import Flask, render_template, request, jsonify
import requests
import urllib.parse

app = Flask(__name__)


WOLFRAM_ALPHA_APPID = '5Y2AYK-7YX89VEL8K'


@app.route('/', methods=['GET', 'POST'])
def index():
    print(request)
    if request.method == 'POST':
        print(request.headers)
        query = request.form['query']
        encoded_query = urllib.parse.quote_plus(query)
        url = f"https://api.wolframalpha.com/v2/query?appid={WOLFRAM_ALPHA_APPID}&input={encoded_query}&format=plaintext&output=json"
        print(url)
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            print(data)
            result = data['queryresult']['pods'][1]['subpods'][0]['plaintext']
            return render_template('index.html', result=result)
        else:
            return render_template('index.html', error=f"Ошибка: {response.status_code}")
    else:
        return render_template('index.html')


@app.route('/api', methods=['GET', 'POST'])
def api():
    if request.method == 'POST':
        encoded_query = request.args.get("query")
        print(encoded_query)
        url = f"https://api.wolframalpha.com/v2/query?appid={WOLFRAM_ALPHA_APPID}&input={encoded_query}&format=plaintext&output=json"
        print(url)
        response = requests.get(url)
        data = {}
        if response.status_code == 200:
            data = response.json()
            result = data['queryresult']['pods'][1]['subpods'][0]['plaintext']
            return jsonify({
                "Method": "POST",
                "status": 200,
                "success": True,
                "data": result
            })
        else:
            return jsonify({
                "Method": "POST",
                "status": 400,
                "success": True,
                "data": None
            })
    else:
        return jsonify({
                "Method": "GET",
                "status": 400,
                "success": True,
                "data": None
        })


if __name__ == '__main__':
    app.run(debug=True)


