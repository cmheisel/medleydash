from collections import namedtuple

import gdata.spreadsheet.service
import gdata.service
import gdata.spreadsheet

SPREADSHEET_ID = "tMrsDYOEObCRpe8rkVsuerg"
DASHBOARD_ID = 'odq'
WIP_ID = 'odo'

WIPRecord = namedtuple('WIPRecord', 
                       ['category', 'backlogdate', 'startdate', 
                        'ticket', 'title', 'cycletime'])


def login(email, password):
    gd_client = gdata.spreadsheet.service.SpreadsheetsService()
    gd_client.email = email
    gd_client.password = password
    gd_client.source = 'CMGd-MedleyDashboard-1'
    gd_client.ProgrammaticLogin()
    return gd_client


def dashboard_feed_to_list(feed):
    data = []
    for item in feed.entry:
        value = item.content.text.split(":")[1].split(",")[0].strip()
        data.append({item.title.text: value})
    return data


def fetch_feature_data(connection, spreadsheet_id=SPREADSHEET_ID,
                       dashboard_id=DASHBOARD_ID):
    feed = connection.GetListFeed(spreadsheet_id, dashboard_id)
    dashboard_data = dashboard_feed_to_list(feed)
    return dashboard_data


def fetch_wip_data(connection, spreadsheet_id=SPREADSHEET_ID,
                   dashboard_id=WIP_ID):
    feed = connection.GetListFeed(spreadsheet_id, dashboard_id)
    wip_data = []
    for entry in feed.entry:
        row_kwargs = {}
        # We do this because dict(row.custom.items()) doesn't return the values
        for key in entry.custom:
            row_kwargs[key] = entry.custom[key].text
        row = WIPRecord(**row_kwargs)
        wip_data.append(row)
    wip_data = sorted(wip_data, key=lambda row: row.cycletime)
    wip_data.reverse()
    return wip_data


def list_worksheets(connection, spreadsheet_id=SPREADSHEET_ID):
    feed = connection.GetWorksheetsFeed(spreadsheet_id)
    worksheets = {}
    for i, entry in enumerate(feed.entry):
        worksheet_id = feed.entry[i].id.text.split('/')[-1]
        worksheets[worksheet_id] = feed.entry[i].title.text
    return worksheets

if __name__ == "__main__":
    from auth import email, password
    client = login(email, password)
    import pprint
    pprint.pprint(fetch_wip_data(client))
