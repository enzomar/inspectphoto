#!/usr/bin/env python3

import argparse
from PIL import Image
from PIL.Image import Exif
from PIL.ExifTags import TAGS, GPSTAGS
import palette



def _parse_arg():
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input', required=True)
    args = parser.parse_args()

    return args.input


def _load(image_file_path):
    # https://pillow.readthedocs.io/en/stable/reference/Image.html
    image = Image.open(image_file_path)
    return image


def _dms_to_dd(gps_coords, gps_coords_ref):
    d, m, s =  gps_coords
    dd = d + m / 60 + s / 3600
    if gps_coords_ref.upper() in ('S', 'W'):
        return float(-dd)
    elif gps_coords_ref.upper() in ('N', 'E'):
        return float(dd)
    else:
        raise RuntimeError('Incorrect gps_coords_ref {}'.format(gps_coords_ref))


def _get_info(image):

    # info from image

    #"Image Size": image.size, <- it breaks json
    #"Filename": image.filename,


    info_dict = {
        "Height": image.height,
        "Width": image.width,
        "Format": image.format,
        "Mode": image.mode,
        "isAnimated": getattr(image, "is_animated", False),
        "Frames": getattr(image, "n_frames", 1)
    }

    # info from exif
    exif = image.getexif()

    for tag_id in exif:
        # get the tag name, instead of human unreadable tag id
        tag = TAGS.get(tag_id, tag_id)
        data = exif.get(tag_id)
        # decode bytes 
        if isinstance(data, bytes):
            data = data.decode()
        info_dict[str(tag)] = str(data) 


    # info from exif - GPS
    try:
        for key, value in TAGS.items():
            if value == "GPSInfo":
                break
        gps_info = exif.get_ifd(key)
        lat_ref = gps_info[1]
        lat = gps_info[2]
        lon_ref = gps_info[3]
        lon = gps_info[4]
        try:
            del info_dict['GPSInfo']
        except:
            pass 
        info_dict['Lat'] = _dms_to_dd(lat, lat_ref)
        info_dict['Long'] = _dms_to_dd(lon, lon_ref)
    except:
        pass
    
    """
    try:
        hex, freq = palette.extract(image)
        print(hex)
        print(freq)
        info_dict["Color"] = hex
        info_dict["Frequency"] = freq
    except Exception as ex:
        print(str(ex))
    """

 
    return info_dict


def run(image_pointer):
    imagedata = _load(image_pointer)
    info_dict = _get_info(imagedata)
    return info_dict

if __name__ == "__main__":
    image_file_path = _parse_arg()
    with open(image_file_path) as fp:
        imagedata = _load(fp)
        info_dict = run(imagedata)

        for label,value in info_dict.items():
            print(f"{label:25}: {value}")
