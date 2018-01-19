import cx_Freeze

executables = [cx_Freeze.Executable("Side Scroller game.py")]

cx_Freeze.setup(
    name="Jiggle Jump",
    options={"build_exe": {"packages" : ["pygame"],
                           "include_files": ["cloud1.png", "cloud2.png", "cloud3.png",
                                              "Soft Marshmallow.otf", "spritesheet_jumper.xml",
                                              "Explosion4.wav", "Jump10.wav", "Pickup_Coin4.wav",
                                              "wind.ogg"]}},
    executables=executables

    )