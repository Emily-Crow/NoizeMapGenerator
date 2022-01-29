import math
import numpy as np
from PIL import Image, ImageDraw
from perlin_noise import PerlinNoise
import json

##Приблежение шума, 1 - ближе, 16 - дальше
noise_zoom = 16

##Размер одного сектора (одна единица координат в квадрате) в пикселях
##Размер конечной картинке равен..
##..(sector_size*sectors_view) X (равен sector_size*sectors_view) пикселей
sector_size = 16

##Количество секторов (квадрат со стороной равный указаной)
##Рекомендуется от 1 до 64
sectors_view = 64

octaves = 2
seed = 1
pos_x = 0
pos_y = 0

##if pos_x < 640:
##  with open('data.json', 'w') as f:
##      json.dump((pos_x + (sectors_view), pos_y), f)

def perlin_map(vp_size, vp_x, vp_y, vp_zoom, vp_octaves, vp_seed):  
  ret_noise_ground = np.eye(sectors_view)
  ret_noise_water = np.eye(sectors_view)  
  p_noise = PerlinNoise(vp_octaves, vp_seed)  
  for x_sector in range(sectors_view):
    for y_sector in range(sectors_view):
      ret_noise_ground[x_sector][y_sector] = p_noise([(vp_x+x_sector)/(noise_zoom), (vp_y+y_sector)/(noise_zoom)])##/vp_size
      ret_noise_water[x_sector][y_sector] = p_noise([(vp_y+y_sector)/(noise_zoom * 3), (vp_x+x_sector)/(noise_zoom * 3)])  
  ret_noise_ground = clamp_func(ret_noise_ground)
  ret_noise_water = clamp_func(ret_noise_water)
  return (ret_noise_ground, ret_noise_water)

def clamp_func(vp_noise):
  for x in range(len(vp_noise)):
    for y in range(len(vp_noise)):
      vp_noise[x, y] = abs(vp_noise[x, y]) * 2.5
  return vp_noise

def draw_map(vp_perlin_map, vp_chunk_size):
  noise_ground, noise_water = vp_perlin_map
  size = sector_size*sectors_view
  img_size = size
##  img_size = round(math.sqrt(len(vp_perlin_map))*vp_chunk_size)
  image = Image.new(mode="RGB", size=[img_size, img_size])
  draw = ImageDraw.Draw(image)	
  ##print(noise)
  for x in range(sectors_view):
    for y in range(sectors_view):
      if noise_ground[x,y] <= 0.3:
        r = round(230 * round(noise_ground[x,y] + 0.7))
        g = round(180 * round(noise_ground[x,y] + 0.7))
        b = round(150 * round(noise_ground[x,y] + 0.7))
      elif noise_ground[x,y] <= 0.8:
        r = round(150 * round(noise_ground[x,y] + 0.2))
        g = round(240 * round(noise_ground[x,y] + 0.2))
        b = round(50 * round(noise_ground[x,y] + 0.2))
      else:
        r = round(255*noise_ground[x,y])
        g = round(255*noise_ground[x,y])
        b = round(255*noise_ground[x,y])        
      draw.rectangle((x * sector_size, y * sector_size, x * sector_size + sector_size, y * sector_size + sector_size), (r, g, b))          
  image.show()
  

print("start")
print("start_perlin_map on x,y", pos_x, pos_y)
pm = perlin_map(sector_size, pos_x, pos_y, sectors_view, octaves, seed)
print("end_perlin_map")
print("start_draw_map")
draw_map(pm, noise_zoom)
print("end_draw_map")
