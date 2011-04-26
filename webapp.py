from flask import Flask, render_template

from auth import email, password
from datasources import login, fetch_feature_data


app = Flask('medleydash')

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
    connection = login(email, password)
    feature_data = fetch_feature_data(connection)
    metrics = []
    for key, verbose_name in METRIC_NAME_MAPPING:
        metrics.append({verbose_name: feature_data[key]})

    context = {
        'metrics': metrics,
    }
    return render_template('dashboard.html', **context)

if __name__ == "__main__":
    app.run(debug=True)
