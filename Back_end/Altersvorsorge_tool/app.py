from flask import Flask, request, render_template
from Pension_Calculator import calculate_vintage

app = Flask(__name__, 
            template_folder="Front_end", 
            static_folder="Front_end")

@app.route("/data")
def data():
    return render_template("data.html")

@app.route("/calculate", methods=["POST"])
def return_vintage():
    web_vintage = int(request.form["return-vintage"])
    return web_vintage


if __name__ == "__main__":
    app.run(debug=True)
