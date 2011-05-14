import datetime
from flask import Flask, render_template


from auth import email, password
from datasources import login, fetch_feature_data, fetch_wip_data


app = Flask('medleydash')
app.config.from_envvar('MEDLEYDASH_SETTINGS')

def get_the_cache():
    if app.config.get('CACHE_SERVER', None):
        from werkzeug.contrib.cache import MemcachedCache
        cache = MemcachedCache(app.config['CACHE_SERVER'])
    else:
        from werkzeug.contrib.cache import NullCache
        cache = SimpleCache()
    return cache

@app.route('/')
def dashboard():
    cache = get_the_cache()
    feature_data = cache.get('medleydash-features')
    updated_at = cache.get('medleydash-updated')
    if not feature_data:
        connection = login(email, password)
        feature_data = fetch_feature_data(connection)
        cache.set('medleydash-features', feature_data, timeout=5 * 60)
        updated_at = datetime.datetime.now()
        cache.set('medleydash-updated', updated_at,
                   timeout=5 * 60)

    context = {
        'metrics': feature_data,
        'updated_at': updated_at,
        'title': "Medley Development Dashboard"

    }
    return render_template('dashboard.html', **context)

@app.route('/wip/')
def wip():
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

    context = {
        'title': "Medley Work In Progress: %s" % (len(wip_data), ),
        'wip_data': wip_data,
        'headers': wip_data[0]._fields,
        'updated_at': updated_at,
    }
    return render_template('wip.html', **context)

if __name__ == "__main__":
    app.run(debug=True)
