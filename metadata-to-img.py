#!/usr/bin/env python3

import piexif
import fractions
import yaml


def to_deg(value, loc):
    if value < 0:
       loc_value = loc[0]
    elif value > 0:
       loc_value = loc[1]
    else:
       loc_value = ""
    abs_value = abs(value)
    deg =  int(abs_value)
    t1 = (abs_value-deg)*60
    minu = int(t1)
    sec = round((t1 - minu)* 60, 5)
    return (deg, minu, sec, loc_value)

def change_to_rational(number):
    f = fractions.Fraction(str(number))
    return (f.numerator, f.denominator)



with open("metadata.yaml", 'r') as stream:
  data= yaml.load(stream, Loader=yaml.FullLoader)
for jpg_filepath in data.keys():
    lat = data[jpg_filepath]['gps']['lat']
    lng = data[jpg_filepath]['gps']['long']
    altitude = data[jpg_filepath]['gps']['alt']

    lat_deg = to_deg(lat, ["S", "N"])
    lng_deg = to_deg(lng, ["W", "E"])
    exif_lat = (change_to_rational(lat_deg[0]), change_to_rational(lat_deg[1]), change_to_rational(lat_deg[2]))
    exif_lng = (change_to_rational(lng_deg[0]), change_to_rational(lng_deg[1]), change_to_rational(lng_deg[2]))


    gps_ifd = {
        piexif.GPSIFD.GPSVersionID: (2, 0, 0, 0),
        piexif.GPSIFD.GPSAltitudeRef: 0,
        piexif.GPSIFD.GPSAltitude: change_to_rational(round(altitude, 3)),
        piexif.GPSIFD.GPSLatitudeRef: lat_deg[3],
        piexif.GPSIFD.GPSLatitude: exif_lat,
        piexif.GPSIFD.GPSLongitudeRef: lng_deg[3],
        piexif.GPSIFD.GPSLongitude: exif_lng,
    }

    gps_exif = {"GPS": gps_ifd}
    exif_data = piexif.load(jpg_filepath)
    exif_data.update(gps_exif)
    exif_bytes = piexif.dump(exif_data)
    piexif.insert(exif_bytes, jpg_filepath)
