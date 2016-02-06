Quick start (only windows binaries for now)
-------------------------------------------

1. download package (http://katiska.dy.fi/files/stuff_and_things/python_steering_behaviors/windows_binaries.zip)

2. unzip anywhere

3. run application.exe



Developer install (from git)
----------------------------

Requires pySFML:
http://www.python-sfml.org/download.html

    git clone https://github.com/warbaque/python-steering-behaviors
    cd python-steering-behaviors
    python3 application.py

    # you might need to update imports on newer versions of pysfml
    #    from 'import sfml as sf'
    #    to   'from sfml import sf'
    find ./ -type f -name "*.py" | xargs sed -i 's/import sfml as sf/from sfml import sf/g'



Settings
--------

Change simulation parameters and keybindings from settings.py



Default bindings
----------------

    [Mousebindings]

    [Left Click ]   : Add boid to cursor position


    [Keybindings]

    [ESC]           : Exit application
    [F1]            : Toggle help
    [DEL]           : Delete all boids
    [A]             : Toggle Attractive mouse on/off
    [S]             : Toggle Scary mouse on/off
    [D]             : Scatter boids around map
    [1]             : Decrease Boid Sight Radius
    [Q]             : Increase Boid Sight Radius
    [2]             : Decrease Desired Separation
    [W]             : Increase Desired Separation
    [3]             : Decrease Max Steering Force
    [E]             : Increase Max Steering Force
    [4]             : Decrease Separation Factor
    [R]             : Increase Separation Factor
    [5]             : Decrease Alignment Factor
    [T]             : Increase Alignment Factor
    [6]             : Decrease Cohesion Factor
    [Y]             : Increase Cohesion Factor
