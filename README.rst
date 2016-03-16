Synopsis
========
LeoMeijuDownloader project is a tool to download the Meiju video for collection.

Table of Contents
-----------------
  * [Requirements](#requirements)
  * [Installation](#installation)
  * [Usage](#usage)
  * [Motivation](#motivation)
  * [Contributors](#contributors)
  * [License](#license)
  * [Thanks](#thanks)

Requirements
------------
LeoMeijuDownloader requires following to run:

- Python Version 2.7

Installation
------------
LeoMuFundPicker can be installed by unzipping the source code in one directory and using this command. ::

    python setup.py install

Usage
-----
Run the tool without any sub-command, or use --help option to show the help manual ::

    $> LeoMeijuDownloader
    Usage: __main__.py [OPTIONS] COMMAND [ARGS]...
    Options:
        --help  Show this message and exit.
    Commands:
        download
        search
        show

Use search sub-command to get all Meiju which contains the keywwords that you have input. Here is the example ::

    $> LeoMeijuDownloader search
    Please input the keywords of the Meiju you want to search: big
    Total 2 Meiju is found. Following are the lists:
    One Big Happy
    The Big Bang Theory

Use show sub-command to get the detailed information of the Meiju. Here is the example ::

    $> LeoMeijuDownloader show
    Please input the name of Meiju which you want to see the details: The Big Bang Theory
    Season 1 [Ep1, Ep2, Ep3, Ep4, Ep5, Ep6, Ep7, Ep8, Ep9, Ep10, Ep11, Ep12, Ep13, Ep14, Ep15, Ep16, Ep17, ]
    Season 2 [Ep1, Ep2, Ep3, Ep4, Ep5, Ep6, Ep7, Ep8, Ep9, Ep10, Ep11, Ep12, Ep13, Ep14, Ep15, Ep16, Ep17, Ep18, Ep19, Ep20, Ep21, Ep22, Ep23, ]
    Season 3 [Ep1, Ep2, Ep3, Ep4, Ep5, Ep6, Ep7, Ep8, Ep9, Ep10, Ep11, Ep12, Ep13, Ep14, Ep15, Ep16, Ep17, Ep18, Ep19, Ep20, Ep21, Ep22, Ep23, ]
    Season 4 [Ep1, Ep2, Ep3, Ep4, Ep5, Ep6, Ep7, Ep8, Ep9, Ep10, Ep11, Ep12, Ep13, Ep14, Ep15, Ep16, Ep17, Ep18, Ep19, Ep20, Ep21, Ep22, Ep23, Ep24, ]
    Season 5 [Ep1, Ep2, Ep3, Ep4, Ep5, Ep6, Ep7, Ep8, Ep9, Ep10, Ep11, Ep12, Ep13, Ep14, Ep15, Ep16, Ep17, Ep18, Ep19, Ep20, Ep21, Ep22, Ep23, Ep24, ]
    Season 6 [Ep1, Ep2, Ep3, Ep4, Ep5, Ep6, Ep7, Ep8, Ep9, Ep10, Ep11, Ep12, Ep13, Ep14, Ep15, Ep16, Ep17, Ep18, Ep19, Ep20, Ep21, Ep22, Ep23, Ep24, ]
    Season 7 [Ep1, Ep2, Ep3, Ep4, Ep5, Ep6, Ep7, Ep8, Ep9, Ep10, Ep11, Ep12, Ep13, Ep14, Ep15, Ep16, Ep17, Ep18, Ep19, Ep20, Ep21, Ep22, Ep23, Ep24, ]
    Season 8 [Ep1, Ep2, Ep3, Ep4, Ep5, Ep6, Ep7, Ep8, Ep9, Ep10, Ep11, Ep12, Ep13, Ep14, Ep15, Ep16, Ep17, Ep18, Ep19, Ep20, Ep21, Ep22, Ep23, Ep24, ]
    Season 9 [Ep1, Ep2, Ep3, Ep4, Ep5, Ep6, Ep7, Ep8, Ep9, Ep10, Ep11, Ep12, Ep13, Ep14, Ep15, Ep16, Ep17, ]

Use download sub-command to download the all season of Meiju / one season / one episode of one season ::

    $> LeoMeijuDownloader download
    Please input the name of Meiju: The Big Bang Theory
    Please input the Season number that you want to download (0 means download all season): 4
    Please input the Episode number that you want to download (0 means download all episode): 0
    Please input the destination directory path: c:\Personal

Motivation
----------
- I am so lazy that everything can be automated by machine, i don't want to do it myself.
- I am a big fan of Python. Life is short, use Python.
- I am a big fan of Meiju. They are my memories.

Contributors
------------
Leo Deng

License
-------
MIT

Thanks
------
Special thanks to project youtube-dl. They have done an awesome job.
