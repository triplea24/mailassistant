from requests import get

def get_mails(sender):
    url = '/api/mails' 
    params = {'sender': sender}
    r = get(url, params=params)
    mails = r.json()