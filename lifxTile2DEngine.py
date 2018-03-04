# Author: Devon Beckett
# email: devonabeckett@gmail.com

import time
from copy   import deepcopy
from colour import Color
from socket import *
from struct import *

#//////////////////////////////////////////////////////////////////////////////////////////////////////////
# GLOBAL DEFINES
#//////////////////////////////////////////////////////////////////////////////////////////////////////////
LOOP_INTERVAL          = .075      # how often we want to check the time (in seconds)
TILE_NAME              = "Tile" # Set this to what you named your Tile
CLIENT_ID              = 0      # Make Something up
BROADCAST_ADDR         = '255.255.255.255' 
LIFX_PORT              = 56700
LIFX_PROTOCOL          = 1024
LIFX_PROTOCOL_TAGGED   = 0b00110100
LIFX_PROTOCOL_UNTAGGED = 0b00010100

WIDTH  = 48
HEIGHT =  8


class DeviceMessage:
        GetService = 2
        StateService = 3
        GetHostInfo = 12
        StateHostInfo = 13
        GetHostFirmware = 14
        StateHostFirmware = 15
        GetWifiInfo = 16
        StateWifiInfo = 17
        GetWifiFirmwareLevel = 18
        StateWifiFirmwareLevel = 19
        GetPower = 20
        SetPower = 21
        StatePower = 22
        GetLabel = 23
        SetLabel = 24
        StateLabel = 25
        GetVersion = 32
        StateVersion = 33
        GetInfo = 34
        StateInfo = 35
        Acknowledgement = 45
        GetLocation = 48
        SetLocation = 49
        StateLocation = 50
        GetGroup = 51
        SetGroup = 52
        StateGroup = 53
        EchoRequest = 58
        EchoResponse = 59
# class DeviceMessage

class LightMessage:
        Get = 101
        SetColor = 102
        SetWaveform = 103
        SetWaveFormOptional = 119
        State = 107
        GetPower = 116
        SetPower = 117
        StatePower = 118
        GetInfrared = 120
        StateInfrared = 121
        SetInfrared = 122
# class LightMessage
        
class MultiZoneMessage:
        NO_APPLY = 0
        APPLY = 1
        APPLY_ONLY = 2
        
        SetColorZones = 502
        StateZone = 503
        StateMultiZone = 506
# class MultiBoneMessage

class TileMessages:
        GetDeviceChain = 701
        StateDeviceChain = 702
        SetUserPosition = 703
        GetTileState64 = 707
        StateTileState64 = 711
        SetTileState64 = 715
#class TileMessages

##################################################
#         Image Supporting Globals               #
##################################################

def hsbk (hue, sat, lum, kel):
        return pack("HHHH",hue,sat,lum,kel)

def RGBtoHSBK (red, green, blue, brightness=1):
        c = Color(rgb=(red, green, blue))
        hue = int(c.hue * 65535)
        sat = int(c.saturation * 65535)
        brt = int(c.luminance * 65535 * brightness)
        return hsbk(hue,sat,brt,0)

lum = .3

cyan   = RGBtoHSBK(.25, .5, .7,lum)
yellow = RGBtoHSBK(.75,.75, 0 ,lum)
white  = RGBtoHSBK( 1 , 1 , 1 ,lum)
pink   = RGBtoHSBK( .5, .3,.35,lum)
orange = RGBtoHSBK( .5, .2, 0 ,lum)
red    = RGBtoHSBK( 1 , 0 , 0 ,lum)
green  = RGBtoHSBK( 0 , 1 , 0 ,lum)
blue   = RGBtoHSBK( 0 , 0 , 1 ,lum)
black  = RGBtoHSBK( 0 , 0 , 0 , 1 )
transparent  = RGBtoHSBK( 0 , 0 , 0 , 0 )

blankscene = [
[hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0)],
[hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0)],
[hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0)],
[hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0)],
[hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0)],
[hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0)],
[black,hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0)],
[black,hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0)]]

blanktile = [
[hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0)],
[hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0)],
[hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0)],
[hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0)],
[hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0)],
[hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0)],
[hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0)],
[hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0),hsbk(0,0,0,0)]]



def GetView8x8(scene, x, y):
        pos_x = x
        pos_y = y
        t_x = 0
        t_y = 0
        tile = blanktile
        while t_y < 8:
            while t_x < 8:
                if pos_x < WIDTH and pos_y < HEIGHT:
                    tile[t_y][t_x] = scene[pos_y][pos_x]
                else:
                    tile[t_y][t_x] = hsbk(0,0,0,0)
                t_x += 1
                pos_x += 1
            pos_x = x
            t_x = 0
            pos_y += 1
            t_y += 1
        return tile

def BuildSetTileState64(tile, data):
    pixels = ""
    x = 0
    y = 0
    while y < 8:
        while x < 8:
            pixels += data[y][x]
            x += 1
        x = 0
        y += 1
    return pack("<BBxBBBL512s", tile, 1, 0, 0, 8, 0, pixels)
    
def DrawSprite(x, y, sprite, scene):
    pos_x = x
    pos_y = y
    sz_y = len(sprite)
    if sz_y > 0:
        sz_x = len(sprite[0])
    s_x = 0
    s_y = 0
    while s_y < sz_y:
        while s_x < sz_x:
            if pos_x < WIDTH and pos_x >= 0 and pos_y < HEIGHT and pos_y >= 0:
                if sprite[s_y][s_x] is not transparent:
                    scene[pos_y][pos_x] = sprite[s_y][s_x]
            s_x += 1
            pos_x += 1
        pos_x = x
        s_x = 0
        pos_y += 1
        s_y += 1

def DrawRectangle(x, y, size_x, size_y, hsbk, scene):
    pos_x = x
    pos_y = y
    s_x = 0
    s_y = 0
    while s_y < size_y:
        while s_x < size_x:
            if pos_x < WIDTH and pos_x >= 0 and pos_y < HEIGHT and pos_y >= 0:
                scene[pos_y][pos_x] = hsbk
            s_x += 1
            pos_x += 1
        pos_x = x
        s_x = 0
        pos_y += 1
        s_y += 1

def DrawPoint(x, y, hsbk, scene):
    if x < WIDTH and x >= 0 and y < HEIGHT and y >= 0:
        scene[y][x] = hsbk


##################################################
#                     Sprites                    #
##################################################

# All the sprites are just 2D arrays of HSBK color values which represent the pixels of the sprite
# I have an 'image' for each digit plus one that is all background color. I may add some
# extra characters here like the colon that typically goes between the hours and minutes.

pacman = [ # right to left, mouth open
          [transparent,transparent,yellow,yellow,yellow,yellow,transparent,transparent],
          [transparent,yellow,yellow,yellow,yellow,yellow,yellow,transparent],
          [transparent,transparent,yellow,yellow,yellow,yellow,yellow,yellow],
          [transparent,transparent,transparent,yellow,yellow,yellow,yellow,yellow],
          [transparent,transparent,transparent,transparent,yellow,yellow,yellow,yellow],
          [transparent,transparent,yellow,yellow,yellow,yellow,yellow,yellow],
          [transparent,yellow,yellow,yellow,yellow,yellow,yellow,transparent],
          [transparent,transparent,yellow,yellow,yellow,yellow,transparent,transparent]
         ]
pacman2 = [ # mouth closed
          [transparent,transparent,yellow,yellow,yellow,yellow,transparent,transparent],
          [transparent,yellow,yellow,yellow,yellow,yellow,yellow,transparent],
          [yellow,yellow,yellow,yellow,yellow,yellow,yellow,yellow],
          [yellow,yellow,yellow,yellow,yellow,yellow,yellow,yellow],
          [yellow,yellow,yellow,yellow,yellow,yellow,yellow,yellow],
          [yellow,yellow,yellow,yellow,yellow,yellow,yellow,yellow],
          [transparent,yellow,yellow,yellow,yellow,yellow,yellow,transparent],
          [transparent,transparent,yellow,yellow,yellow,yellow,transparent,transparent]
         ]
pacman3 = [ # left to right mouth open
          [transparent,transparent,yellow,yellow,yellow,yellow,transparent,transparent],
          [transparent,yellow,yellow,yellow,yellow,yellow,yellow,transparent],
          [yellow,yellow,yellow,yellow,yellow,yellow,transparent,transparent],
          [yellow,yellow,yellow,yellow,yellow,transparent,transparent,transparent],
          [yellow,yellow,yellow,yellow,transparent,transparent,transparent,transparent],
          [yellow,yellow,yellow,yellow,yellow,yellow,transparent,transparent],
          [transparent,yellow,yellow,yellow,yellow,yellow,yellow,transparent],
          [transparent,transparent,yellow,yellow,yellow,yellow,transparent,transparent]
         ]
blinky = [
          [transparent,transparent,red,red,red,red,transparent,transparent],
          [transparent,red,red,red,red,red,red,transparent],
          [transparent,white,white,red,white,white,red,transparent],
          [red,blue,white,red,blue,white,red,red],
          [red,red,red,red,red,red,red,red],
          [red,red,red,red,red,red,red,red],
          [red,red,red,red,red,red,red,red],
          [transparent,red,transparent,red,red,transparent,red,transparent]
         ]
pinky = [
          [transparent,transparent,pink,pink,pink,pink,transparent,transparent],
          [transparent,pink,pink,pink,pink,pink,pink,transparent],
          [transparent,white,white,pink,white,white,pink,transparent],
          [pink,blue,white,pink,blue,white,pink,pink],
          [pink,pink,pink,pink,pink,pink,pink,pink],
          [pink,pink,pink,pink,pink,pink,pink,pink],
          [pink,pink,pink,pink,pink,pink,pink,pink],
          [transparent,pink,transparent,pink,pink,transparent,pink,transparent]
         ]
inky = [
          [transparent,transparent,cyan,cyan,cyan,cyan,transparent,transparent],
          [transparent,cyan,cyan,cyan,cyan,cyan,cyan,transparent],
          [transparent,white,white,cyan,white,white,cyan,transparent],
          [cyan,blue,white,cyan,blue,white,cyan,cyan],
          [cyan,cyan,cyan,cyan,cyan,cyan,cyan,cyan],
          [cyan,cyan,cyan,cyan,cyan,cyan,cyan,cyan],
          [cyan,cyan,cyan,cyan,cyan,cyan,cyan,cyan],
          [transparent,cyan,transparent,cyan,cyan,transparent,cyan,transparent]
         ]
clyde = [
          [transparent,transparent,orange,orange,orange,orange,transparent,transparent],
          [transparent,orange,orange,orange,orange,orange,orange,transparent],
          [transparent,white,white,orange,white,white,orange,transparent],
          [orange,blue,white,orange,blue,white,orange,orange],
          [orange,orange,orange,orange,orange,orange,orange,orange],
          [orange,orange,orange,orange,orange,orange,orange,orange],
          [orange,orange,orange,orange,orange,orange,orange,orange],
          [transparent,orange,transparent,orange,orange,transparent,orange,transparent]
         ]
ghost = [ # When pacman has the power-pill
          [transparent,transparent,blue,blue,blue,blue,transparent,transparent],
          [transparent,blue,blue,blue,blue,blue,blue,transparent],
          [transparent,blue,blue,white,blue,white,blue,transparent],
          [blue,blue,blue,white,blue,white,blue,blue],
          [blue,blue,blue,blue,blue,blue,blue,blue],
          [blue,white,blue,white,blue,white,blue,blue],
          [blue,blue,white,blue,white,blue,white,blue],
          [transparent,blue,transparent,blue,blue,transparent,blue,transparent]
         ]

#//////////////////////////////////////////////////////////////////////////////////////////////////////////

##################################################
#      Packet Parser                             #
##################################################
class LifxPacket:
        def __init__(self, msg):
                self.Message = unpack("<HHLQ6xBB8xHxx", msg[0][0:36])
                self.Address = msg[1]
                # Frame    2+2+4+8+6+2+8+2+3 = 16+16+5 = 36
                self.Size = self.Message[0]
                self.Origin = self.Message[1] #need to modify
                self.Tagged = self.Message[1] #need to modify
                self.Addressable = self.Message[1] #need to modify
                self.Protocol = self.Message[1] #need to modify
                self.Source = self.Message[2]
                # Frame Address
                self.Target = self.Message[3]
                self.ACK_Req = self.Message[4]
                self.RES_Req = self.Message[4]
                self.Sequence = self.Message[5]
                # Protocol Header
                self.Type = self.Message[6]
                self.Data = msg[0][36:]
                # No checking done here - should work on that.

        def ProcessPacket(self):
                global LifxBulbs
                bulb = LifxBulb()
                if self.Type == DeviceMessage.StateLabel:
                        for b in LifxBulbs:
                                if b == self.Source:
                                        bulb = b
                        bulb.Name = self.Data.strip()
                        bulb.Address = self.Address
                        print bulb.Name + ": " + bulb.Address[0]
                        if bulb == 0:
                                LifxBulbs.append(bulb)
                                return bulb
                # Do more here eventually I guess        
                                        


##################################################
#               Bulb Class                       #
##################################################
class LifxBulb:
        Name = ""
        Location = ""
        Group = ""
        Address = ""
        Socket = socket(AF_INET, SOCK_DGRAM)
        Id = 0
        Hue = 0
        Saturation = 0
        Bright = 0
        Kelvin = 0
        Power = 0
        Seq = 0

        def __repr__(self):
                return self.Name
        
        def __str__(self):
                return self.Name

        def __eq__(self, identifier):
                return self.Id == identifier

        def Send(self, msg):
                self.Socket.sendto(msg, self.Address)
        
                        
##############################   Lifx Tile Finder   #####################################
                        
m = []
LifxBulbs = []

getServiceMsg = pack("<HBBLQ6xBB8xH3x",
                    # Frame
                    37, # (H) Total message Size
                    0, # (B) Lower byte of the protocol field
                    LIFX_PROTOCOL_TAGGED, # (B) Flags and upper bits of the protocol field
                    CLIENT_ID, # (L) Source 
                    # Frame Address
                    0, # (Q) Target: zero = all
                    # (xxxxxx) Reserved
                    1, # (B) Reserved + Response required flag
                    0, # (B) Sequence number
                    # Protocol Header
                    # (xxxxxxxx) Reserved
                    DeviceMessage.GetLabel) # (H) Type
                    # (xx) Reserved
                    # (x) Empty buffer
cs = socket(AF_INET, SOCK_DGRAM)
cs.bind(('',LIFX_PORT))
cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
cs.sendto(getServiceMsg, (BROADCAST_ADDR, LIFX_PORT))
cs.settimeout(1);

print "Looking for " + TILE_NAME
Tile = 0 #default value to detect bulb data later on
while True:
        m = cs.recvfrom(1048)
        packet = LifxPacket(m)
        bulb = packet.ProcessPacket()
        for bulb in LifxBulbs:
                if bulb.Name.find(TILE_NAME) >= 0:
                        print "Found " + TILE_NAME
                        Tile = bulb
                        break
        if Tile != 0:
                break

# Get the tile information: TODO! Not doing anything with this at the moment
msg = pack("<HBBLQ6xBB8xH2x6s",
           # Frame
           8 + 16 + 12 + 6, # Size(Frame + Frame Address + Protocol Header + payload
           0,
           0b00110100,
           CLIENT_ID,
           # Frame Address
           0,
           0,
           Tile.Seq,
           # Protocol Header
           TileMessages.GetTileState64,
           pack("BBxBBB", 0, 1, 0, 0, 8) )

Tile.Send(msg)
Tile.Seq += 1
if Tile.Seq >= 256:
        Tile.Seq = 0

# Pacman variables
pill = False
pacman_pos = WIDTH
blinky_pos = pacman_pos + 10
pinky_pos = pacman_pos + 20
inky_pos = pacman_pos + 30
clyde_pos = pacman_pos + 40
scene = []


def Pacman( adv ):
    global pacman_pos, blinky_pos, pinky_pos, inky_pos, clyde_pos, scene, pill
    if pacman_pos < -48:
        pill = True
    elif pacman_pos > 48:
        pill = False

    blinky_pos = pacman_pos + 10
    pinky_pos = pacman_pos + 20
    inky_pos = pacman_pos + 30
    clyde_pos = pacman_pos + 40

    if pacman_pos % 4 < 2:
        if pill:
            DrawSprite(pacman_pos, 0, pacman3, scene)
        else:
            DrawSprite(pacman_pos, 0, pacman, scene)
    else:
        DrawSprite(pacman_pos, 0, pacman2, scene)
    if pill:
        DrawSprite(blinky_pos, 0, ghost, scene)
        DrawSprite(pinky_pos, 0, ghost, scene)
        DrawSprite(inky_pos, 0, ghost, scene)
        DrawSprite(clyde_pos, 0, ghost, scene)
        pacman_pos += adv
    else:
        DrawSprite(blinky_pos, 0, blinky, scene)
        DrawSprite(pinky_pos, 0, pinky, scene)
        DrawSprite(inky_pos, 0, inky, scene)
        DrawSprite(clyde_pos, 0, clyde, scene)
        pacman_pos -= adv
    
    
while Tile != 0:
        # Clear the sceen
        scene = deepcopy(blankscene)

        # Build the scene
        Pacman(1)

        # Update tiles
        view = GetView8x8(scene, 0, 0)
        TileState64 = BuildSetTileState64(0, view)
        TileState64size = len(TileState64)
        msg = pack("<HBBLQ6xBB8xH2x522s",
                   # Frame
                   8 + 16 + 12 + TileState64size, # Size(Frame + Frame Address + Protocol Header + payload
                   0,
                   0b00110100,
                   CLIENT_ID,
                   # Frame Address
                   0,
                   0,
                   Tile.Seq,
                   # Protocol Header
                   TileMessages.SetTileState64,
                   TileState64)

        Tile.Send(msg)
        Tile.Seq += 1
        if Tile.Seq >= 256:
                Tile.Seq = 0

        view = GetView8x8(scene, 10, 0)
        TileState64 = BuildSetTileState64(1, view)
        TileState64size = len(TileState64)
        msg = pack("<HBBLQ6xBB8xH2x522s",
                   # Frame
                   8 + 16 + 12 + TileState64size, # Size(Frame + Frame Address + Protocol Header + payload
                   0,
                   0b00110100,
                   CLIENT_ID,
                   # Frame Address
                   0,
                   0,
                   Tile.Seq,
                   # Protocol Header
                   TileMessages.SetTileState64,
                   TileState64)

        Tile.Send(msg)
        Tile.Seq += 1
        if Tile.Seq >= 256:
                Tile.Seq = 0
                
        view = GetView8x8(scene, 20, 0)
        TileState64 = BuildSetTileState64(2, view)
        TileState64size = len(TileState64)
        msg = pack("<HBBLQ6xBB8xH2x522s",
                   # Frame
                   8 + 16 + 12 + TileState64size, # Size(Frame + Frame Address + Protocol Header + payload
                   0,
                   0b00110100,
                   CLIENT_ID,
                   # Frame Address
                   0,
                   0,
                   Tile.Seq,
                   # Protocol Header
                   TileMessages.SetTileState64,
                   TileState64)

        Tile.Send(msg)
        Tile.Seq += 1
        if Tile.Seq >= 256:
                Tile.Seq = 0
                
        view = GetView8x8(scene, 30, 0)
        TileState64 = BuildSetTileState64(3, view)
        TileState64size = len(TileState64)
        msg = pack("<HBBLQ6xBB8xH2x522s",
                   # Frame
                   8 + 16 + 12 + TileState64size, # Size(Frame + Frame Address + Protocol Header + payload
                   0,
                   0b00110100,
                   CLIENT_ID,
                   # Frame Address
                   0,
                   0,
                   Tile.Seq,
                   # Protocol Header
                   TileMessages.SetTileState64,
                   TileState64)

        Tile.Send(msg)
        Tile.Seq += 1
        if Tile.Seq >= 256:
                Tile.Seq = 0
                
        view = GetView8x8(scene, 40, 0)
        TileState64 = BuildSetTileState64(4, view)
        TileState64size = len(TileState64)
        msg = pack("<HBBLQ6xBB8xH2x522s",
                   # Frame
                   8 + 16 + 12 + TileState64size, # Size(Frame + Frame Address + Protocol Header + payload
                   0,
                   0b00110100,
                   CLIENT_ID,
                   # Frame Address
                   0,
                   0,
                   Tile.Seq,
                   # Protocol Header
                   TileMessages.SetTileState64,
                   TileState64)

        Tile.Send(msg)
        Tile.Seq += 1
        if Tile.Seq >= 256:
                Tile.Seq = 0

        #wake up ever so often and perform this ...                
        time.sleep(LOOP_INTERVAL)