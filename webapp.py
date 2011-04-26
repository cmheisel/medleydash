import datetime

from flask import Flask, render_template
from werkzeug.contrib.cache import SimpleCache

from auth import email, password
from datasources import login, fetch_feature_data


app = Flask('medleydash')
cache = SimpleCache()


METRIC_NAME_MAPPING = (
    ('done_this_week', "Features this week"),
    ('this_weeks_goal', "This week's goal"),
    ('done_this_month', "Features this month"),
    ('this_months_goal', "This month's goal"),
    ('done_last_week', "Last week"),
    ('done_last_month', "Last month"),
)

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

    metrics = []
    for key, verbose_name in METRIC_NAME_MAPPING:
        metrics.append({verbose_name: feature_data[key]})

    context = {
        'metrics': metrics,
        'updated_at': updated_at,

    }
    return render_template('dashboard.html', **context)

if __name__ == "__main__":
    app.run(debug=True)
