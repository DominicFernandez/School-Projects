import sys
from cx_Freeze import setup, Executable

base = None

executables = [Executable("RabbitHops.py", base=base)]

if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Rabbit Hops",

    version="1",
    options={"build_exe": {"packages" : ["pygame"],
                           "include_files": ["cloud1.png", "cloud2.png", "cloud3.png",
                                              "Soft Marshmallow.otf", "spritesheet_jumper.xml",
                                              "Explosion4.wav", "Jump10.wav", "Pickup_Coin4.wav",
                                              "wind.ogg"]}},
    executables=executables)