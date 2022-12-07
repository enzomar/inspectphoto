import extcolors
import pandas as pd
from colormap import rgb2hex

from PIL import Image

def _resize(img, output_width=900):
    wpercent = (output_width/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    rimg = img.resize((output_width,hsize), Image.ANTIALIAS)
    return rimg


def extract(img: Image):
    img = _resize(img)
    colors_x = extcolors.extract_from_image(img, tolerance = 12, limit = 12)
    color, frequency = _get_color_frequency(colors_x)
    return color, frequency


def _get_color_frequency(input):
    colors_pre_list = str(input).replace('([(','').split(', (')[0:-1]
    df_rgb = [i.split('), ')[0] + ')' for i in colors_pre_list]
    df_percent = [i.split('), ')[1].replace(')','') for i in colors_pre_list]
    
    #convert RGB to HEX code
    df_color_up = [rgb2hex(int(i.split(", ")[0].replace("(","")),
                          int(i.split(", ")[1]),
                          int(i.split(", ")[2].replace(")",""))) for i in df_rgb]
    
    df = pd.DataFrame(zip(df_color_up, df_percent), columns = ['c_code','occurence'])
    list_color = list(df['c_code'])
    list_precent = [int(i) for i in list(df['occurence'])]
    return list_color, list_precent