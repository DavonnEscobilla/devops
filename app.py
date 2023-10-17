from flask import Flask, render_template, request
import urllib.parse
import requests

app = Flask(__name__)

main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "TBtlmUT4pNQJghJoxJ1slrqKV8utZ5fo"

class Conversion:
    def __init__(self, x, path, avoid):
        self.x = x
        self.Paths = ["Fastest Path", "Shortest Path", "Walking path"]
        self.Avoids = ["Highways", "Bridge", "Tunnel", "Streets"]
        self.Path = path
        self.Avoid = avoid

    def main(self):
        if self.x == "km" or self.x == "KM" or self.x == "Km" or self.x == "kM":
            y = "km"
        elif self.x == "mi":
            y = "mi"
        # Add other conditions as needed
        self.y = y
        return self.y

    def choices(self):
        print("Choose path do you want to take.\n")
        for i in range(len(self.Paths)):
            print("[" + str(i + 1) + "] {}\n".format(self.Paths[i]))
        self.Path = int(request.form.get('path'))
        print("Choose what you want to avoid\n")
        for i in range(len(self.Avoids)):
            print("[" + str(i + 1) + "] {}\n".format(self.Avoids[i]))
        self.Avoid = int(request.form.get('avoid'))
        return self.Path, self.Avoid

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        orig = request.form.get('orig')
        dest = request.form.get('dest')
        x = request.form.get('x')
        path = request.form.get('path')
        avoid = request.form.get('avoid')

        if orig is None or dest is None or x is None or path is None or avoid is None:
            return render_template('index.html', error="Please fill in all the fields.")

        path = int(path)
        avoid = int(avoid)

        z = Conversion(x, path, avoid)
        z.choices()

        url = main_api + urllib.parse.urlencode({"key": key, "from": orig, "to": dest})
        json_data = requests.get(url).json()
        return render_template('index.html', orig=orig, dest=dest, json_data=json_data, path=path, avoid=avoid)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
