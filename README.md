chain-dl
============

A chained viedeos downloader based on the amazing `youtube-dl`.

This script fetches URL for videos embeded on a "streaming" website and downloads them (via `youtube-dl`).

**Note**: all supported video formats are intrinsically the ones supported by `youtube-dl`.


A/ Installation
------------

This git repository contains a `setup.py` file. To install `chain-dl` you just have to run it :

    git clone https://github.com/ascam42/chain-dl.git
    cd chain-dl
    python3 setup.py install


B/ Utilisation
-----------

In this section, you will see an example of `chain-dl` configuration. The final (and documented) configuration file is avaliable [here](https://github.com/ascam42/chain-dl/blob/master/chain_dl/dl_config.ini).

Let's imagine that I want to chain-download the *Hunter x Hunter* series. It happens that I have found some website that references all episodes. [Check it out](http://www.fairy-streaming.fr/p/episodes-vostfr.html).

### 1. Setup

Once you have installed `chain-dl`, create a 'dowonlads' directory :

    midkr "Hunter x Hunter"
    cd "Hunter x Hunter"

This is the directory where all the magic will happen.



