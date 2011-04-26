from flask import Flask
app = Flask('medleydash')

from auth import email, password
from datasources import login, fetch_feature_data

@app.route('/')
def dashboard():
    connection = login(email, password)
    feature_data = fetch_feature_data(connection)
    return str(feature_data)

if __name__ == "__main__":
    app.run()
