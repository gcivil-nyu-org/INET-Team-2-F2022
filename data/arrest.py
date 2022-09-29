import pandas as pd
import geopy 


df = pd.read_csv('NYPD_Arrest.csv', header=None, nrows=10)
df = df[1:]

geo_locator = geopy.Nominatim(user_agent='1234')


def coord_to_zipcode(point): # (lati, longti)
    r = geo_locator.reverse(point)
    return r.raw['address']['postcode']

result = df.apply(lambda row: coord_to_zipcode((row[16],row[17])), axis=1)
print(result)
