import datetime

from flask import Flask, render_template
from werkzeug.contrib.cache import SimpleCache

from auth import email, password
from datasources import login, fetch_feature_data


app = Flask('medleydash')
cache = SimpleCache()

@app.route('/')
def dashboard():
    feature_data = cache.get('medleydash-features')
    updated_at = cache.get('medleydash-updated')
    if not feature_data:
        connection = login(email, password)
        feature_data = fetch_feature_data(connection)
        cache.set('medleydash-features', feature_data, timeout=5 * 60)
        cache.set('medleydash-updated', datetime.datetime.now(),
                   timeout=5 * 60)
        updated_at = cache.get('medleydash-updated')

    context = {
        'metrics': feature_data,
        'updated_at': updated_at,

    }
    return render_template('dashboard.html', **context)

if __name__ == "__main__":
    app.run(debug=True)
