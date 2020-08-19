# Jie Heng
# Original code

import googlemaps
gmaps = googlemaps.Client(key='AIzaSyB9-6pEKUY9XS7ZJlquKGTdE8G6x9kMhaI')
geocode_result = gmaps.geocode('AIzaSyB9-6pEKUY9XS7ZJlquKGTdE8G6x9kMhaI')

left, right = -87.615546, -87.575706
top, down = 41.809241, 41.78013
gmaps = googlemaps.Client(key='AIzaSyB9-6pEKUY9XS7ZJlquKGTdE8G6x9kMhaI')
zip_ = ['60637', '60615', '60649']

def check(input):
    if input == '':
        return None,None
    else:
        latlng =  gmaps.geocode(input)
        if latlng != []:
            if latlng[0]['address_components'][-1]['short_name'] not in zip_:
                input += "hyde park"
                latlng =  gmaps.geocode(input)
                if latlng:
                    lat,lgt = latlng[0]['geometry']['location']['lat'],latlng[0]['geometry']['location']['lng']
                    if down<lat<top and left<lgt<right:
                        return latlng[0]['formatted_address'],[lat,lgt]
                    else:
                        return None,None
            else:
                 return latlng[0]['formatted_address'],[latlng[0]['geometry']['location']['lat'],
                                                        latlng[0]['geometry']['location']['lng']]

        else:
            return None,None