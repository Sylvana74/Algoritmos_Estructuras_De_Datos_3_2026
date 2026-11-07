from flask import render_template
import config
from models import Customer

app = config.connex_app
app.add_api("swagger.yml")


@app.route("/")
def home():
    customers = Customer.query.all()
    return render_template("home.html", customers=customers)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)