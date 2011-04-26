import gdata.spreadsheet.service
import gdata.service
import gdata.spreadsheet

def login(email, password):
    gd_client = gdata.spreadsheet.service.SpreadsheetsService()
    gd_client.email = email
    gd_client.password = password
    gd_client.source = 'CMGd-MedleyDashboard-1'
    gd_client.ProgrammaticLogin()
    return gd_client


def dashboard_feed_to_dict(feed):
    data = {}
    for item in feed.entry:
        data[item.title.text] = item.content.text.split(":")[1].strip()
    return data


def fetch_feature_data(connection):
    spreadsheet_id = "tMrsDYOEObCRpe8rkVsuerg"
    dashboard_id = 'odq'
    feed = connection.GetListFeed(spreadsheet_id, dashboard_id)
    dashboard_data = dashboard_feed_to_dict(feed)
    return dashboard_data
