import datetime
from flask import (Flask, render_template, redirect, url_for, 
                  render_template_string, make_response)


from auth import email, password
from datasources import login, fetch_feature_data, fetch_wip_data, fetch_done_data

from medleydash import __version__

app = Flask('medleydash')
app.config.from_envvar('MEDLEYDASH_SETTINGS')

def get_the_cache():
    if app.config.get('CACHE_SERVER', None):
        from werkzeug.contrib.cache import MemcachedCache
        cache = MemcachedCache(app.config['CACHE_SERVER'])
    else:
        from werkzeug.contrib.cache import SimpleCache
        cache = SimpleCache()
    return cache

def get_metrics_data():
    cache = get_the_cache()
    feature_data = cache.get('medleydash-features')
    updated_at = cache.get('medleydash-features-updated')
    if not feature_data:
        connection = login(email, password)
        feature_data = fetch_feature_data(connection)
        cache.set('medleydash-features', feature_data, timeout=5 * 60)
        updated_at = datetime.datetime.now()
        cache.set('medleydash-features-updated', updated_at,
                   timeout=5 * 60)
    return feature_data, updated_at

def get_wip_data():
    cache = get_the_cache()
    wip_data = cache.get('medleydash-wip')
    updated_at = cache.get('medleydash-wip-updated')
    if not wip_data:
        connection = login(email, password)
        wip_data = fetch_wip_data(connection)
        cache.set('medleydash-wip', wip_data, timeout=5 * 60)
        updated_at = datetime.datetime.now()
        cache.set('medleydash-wip-updated', updated_at,
                   timeout=5 * 60)
    return wip_data, updated_at

def get_done_data():
    cache = get_the_cache()
    done_data = cache.get('medleydash-done')
    updated_at = cache.get('medleydash-done-updated')
    if not done_data:
        connection = login(email, password)
        done_data = fetch_done_data(connection)
        cache.set('medleydash-done', done_data, timeout=5 * 60)
        updated_at = datetime.datetime.now()
        cache.set('medleydash-done-updated', updated_at,
                   timeout=5 * 60)
    return done_data, updated_at

#Courtesy http://flask.pocoo.org/snippets/33/
@app.template_filter()
def timesince(dt, default="just now"):
    """
    Returns string representing "time since" e.g.
    3 days ago, 5 hours ago etc.
    """

    now = datetime.datetime.now()
    diff = now - dt
    
    periods = (
        (diff.days / 365, "year", "years"),
        (diff.days / 30, "month", "months"),
        (diff.days / 7, "week", "weeks"),
        (diff.days, "day", "days"),
        (diff.seconds / 3600, "hour", "hours"),
        (diff.seconds / 60, "minute", "minutes"),
        (diff.seconds, "second", "seconds"),
    )

    for period, singular, plural in periods:
        
        if period:
            return "%d %s ago" % (period, singular if period == 1 else plural)

    return default

@app.route('/')
def combined():
    wip_data, wip_updated_at = get_wip_data()
    metrics_data, metrics_updated_at = get_metrics_data()

    print "%s -- %s" % (wip_updated_at, metrics_updated_at)

    if metrics_updated_at < wip_updated_at:
        updated_at = metrics_updated_at
    else:
        updated_at = wip_updated_at

    context = {
        'title': 'Medley Development Dashboard',
        'wip_data': wip_data,
        'headers': wip_data[0]._fields,
        'metrics': metrics_data,
        'updated_at': updated_at,
        'version': __version__,
    }
    return render_template('combined.html', **context)

@app.route('/done')
def done():
    done_data, updated_at = get_done_data()

    context = {
        'title': 'Medley Development Dashboard: %s Done' % (len(done_data), ),
        'done_data': done_data,
        'headers': done_data[0]._fields,
        'updated_at': updated_at,
        'version': __version__,
    }
    return render_template('done.html', **context)

@app.route('/flush')
def flush():
    """Blanks out all the cache keys, so you can force a re-fetch from Google."""
    cache = get_the_cache()

    key_bases = ['features', 'wip', 'done']
    for key_base in key_bases:
        cache.delete('medleydash-%s' % key_base)
        cache.delete('medleydash-%s-updated' % key_base)
    return redirect(url_for('combined'))

@app.route('/done/report/<int:year_number>/<int:month_number>')
def done_report(year_number, month_number):
    """Returns a text version of the completed cards for the month."""
    done_data, updated_at = get_done_data()

    done_data = [ record for record in done_data if record.doneon.year == year_number
                 and record.doneon.month == month_number ]

    context = {
        'title': 'Medley Development Report %s/%s: %s Done' % (month_number, year_number, 
                  len(done_data), ),
        'done_data': done_data,
        'headers': done_data[0]._fields,
        'updated_at': updated_at,
        'version': __version__,
    }
    response = make_response(render_template('done-report.txt', **context))
    response.headers['Content-Type'] = "text/plain"
    return response


if __name__ == "__main__":
    app.run(debug=True)
