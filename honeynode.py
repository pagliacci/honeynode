import pyinotify
import json
import geoip2
import geoip2.database
import requests
from time import gmtime, strftime

class MyEventHandler(pyinotify.ProcessEvent):

    def process_IN_MODIFY(self, event):
        print "MODIFY event:", event.pathname
	send_request()

def main():
    # watch manager
    wm = pyinotify.WatchManager()
    wm.add_watch('passwords.json', pyinotify.ALL_EVENTS, rec=True)

    # event handler
    eh = MyEventHandler()

    # notifier
    notifier = pyinotify.Notifier(wm, eh)
    notifier.loop()

def send_request():
    with open('passwords.json') as myfile:
        json_string = json.loads(list(myfile)[-1])
        time = strftime("%Y-%m-%d %H:%M:%S")
        attack_type = "ssh_bruteforce"
        src_ip = json_string['src_ip']
        dst_ip = "ENTER IP ADDRESS HERE"
        login = json_string['username']
        password = json_string['password']
        src_country, src_city, src_latitude, src_longitude = geoposition(src_ip)
        dst_country, dst_city, dst_latitude, dst_longitude = geoposition(dst_ip)
        r = requests.post('http://91.142.94.74:8080', json = {'time':time, 'attack_type':attack_type, 'src_ip':src_ip, \
        'dst_ip':dst_ip, 'login':login, 'password':password, 'src_country':src_country, 'src_city':src_city, \
        'src_latitude':src_latitude, 'src_longitude':src_longitude, 'dst_country':dst_country, 'dst_city':dst_city, \
        'dst_latitude':dst_latitude, 'dst_longitude':dst_longitude})
        print src_country
        print src_city

def geoposition(ip):
    #match = geolite2.lookup(ip)
    #return str(match.location) + str(match.country)
    reader = geoip2.database.Reader('GeoLite2-City.mmdb')
    response = reader.city(ip)
    src_country = response.country.name
    src_city = response.city.name
    src_latitude = response.location.latitude
    src_longitude = response.location.longitude
    return src_country, src_city, src_latitude, src_longitude
if __name__ == '__main__':
    main()
