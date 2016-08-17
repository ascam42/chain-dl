chain-dl
============

A chained viedeos downloader based on the amazing `youtube-dl`.

This script fetches URL for videos embeded on a "streaming" website and downloads them (via `youtube-dl`).

**Note**: all supported video formats are intrinsically the ones supported by `youtube-dl`.





A/ Installation
------------

This git repository contains a `setup.py` file. To install `chain-dl` you just have to run it :

    pip install -U setuptools
    git clone https://github.com/ascam42/chain-dl.git
    cd chain-dl
    python3 setup.py install
    
**Note**: you'll need to have `git`, `python3` and `pip` installed on your computer.

**Note**: in case of `[Errno 13]` during installation, don't panic and `sudo`.





B/ Utilisation
-----------

In this section, you will see an example of `chain-dl` configuration. The final (and documented) configuration file is avaliable [here](https://github.com/ascam42/chain-dl/blob/master/chain_dl/dl_config.ini).

Let's imagine that I want to chain-download the *Hunter x Hunter* series. It happens that I have found some website that references all episodes. [Check it out](http://www.fairy-streaming.fr/p/episodes-vostfr.html).


### 1. Place !

Once you have installed `chain-dl`, create a directory to store your downloads :

    midkr "Hunter x Hunter"
    cd "Hunter x Hunter"

This is where all the magic will happen.


### 2. Config

`chain-dl` needs one configuration file to be present in the downloads directory: `dl_config.ini`.

    touch dl_config.ini


As you can guess, it is an `ini` file in which we will write *what* to download and *where* to find it.

The `dl_config.ini` file accepts two *scopes*: `[download]` and `[show]`. Let's start with `[download]`. The first thing we need to write is the `url` field:

    dl_config.ini
    --------------------------------
    
    [download]
    url=http://www.fairy-streaming.fr/p/episodes-vostfr.html

The `url` field is the url for the page where all the episodes are listed.

### 3. Investigation

Now comes the 'tricky' part. Visit your `url` page, right-click somewhere on the **episodes list** and `inspect element`.

![inspect element](https://github.com/ascam42/chain-dl/blob/master/misc/inspect_element.png)

In your inspector, search for the *lowest* html tag that contains **all** episodes. Then browse the html up to a tag **with precise class and/or id attributes**. As an example: `class="separator"` or `class="text"` are not precise. `class="post-body"` instead is what we're looking for.

![choose div](https://github.com/ascam42/chain-dl/blob/master/misc/choose_div.png)

If your element has only a `class` attribute, add the `list_container_class` field in `dl_config.ini`. But if your element (also) has an `id` attribute, prefer using the `list_container_id` one:

    dl_config.ini
    --------------------------------
    ...
    
    ## HTML class for the 'list-container'
    list_container_class=post-body entry-content
    
    ## HTML id (Note: if the id is specified, the class will be ignored)
    list_container_id=post-body-1906427377956718347

Congratulations ! You've done the hardest part !


### 4. Investgation, again...

Now, visit the link of an entry (i.e. click on the 'Episode 01' item).

On this page, repeat your investigation (right-click and `inspect element`) to find the **precise** element that contains all the video `iframes`:

![choose div](https://github.com/ascam42/chain-dl/blob/master/misc/choose_div_2.png)

**Note**: even if you have an `id` attribute, you shall only use it if it's the same for **every** *episode* page (i.e. if the container `id` in 'Episode 01' is different than in 'Episode 02', use the `class`). Indeed, if you add an invalid `id` in the config, the downloader won't find the iframes.

    dl_config.ini
    --------------------------------
    ...
    
    content_container_class=post-body entry-content

**Note**: in our example, it happens that both `content_container_class` and `list_container_class` are identical. It won't be the case on every streaming site...


### 5. Take a break

No more HTML, I promise !


### 6. Timeout

You can specify the HTTP requests timeout in seconds

    dl_config.ini
    --------------------------------
    ...
    
    timeout_sec=30


### 7. Hosts

In your config, you can specify some `ignore_hosts` and one `preferred_host`.

`ignore_hosts` are *video* hosts from which you don't want to download *any* video. Their `iframes` will be skipped.

The `preferred_host` in the other hand is a *video* host that has a top-priority. If one or more videos
 from this host are found in an episode page, they will be tried first.
 
    dl_config.ini
    --------------------------------
    ...
    
    ignore_hosts=toto.xyz tata.xyz
    preferred_host=videomega.tv
    
    
### 8. Episodes

Then comes the `start_episode` and `ignore_episodes` fields.

    dl_config.ini
    --------------------------------
    ...
    
    ## skip episodes 0-19
    start_episode=20
    ## skip episodes n.4,21,42
    ignore_episodes=4 21 42
    
    
### 9. It's show-time !

If you remember well, I told you earlier that there was another `ini` scope: `show`. For now, it accepts only one field:

    dl_config.ini
    --------------------------------
    ...
    
    [show]
    title=Hunter x Hunter
    
The title of the show you're downloading (for the video filenames).


### 10. Download, at last

Now that your [configuration file](https://github.com/ascam42/chain-dl/blob/master/chain_dl/dl_config.ini) is complete, you can save it and `chain-dl` !

    -> pwd
    /home/yourself/.../Hunter\ x\ Hunter/
    -> ls
    dl_config.ini
    -> chain-dl
    ...
    
**Note**: `chain-dl` is equivalent to `chain-dl -c ./dl_config.ini`



Enjoy
---------

If your configuration has some problem, `chain-dl` will tell you so. Elsewhere, it will start to download **one video** per episode of your show: either from the `preferred_host`, either from the first host found.

If the video downloads succeeds, `chain-dl` will notify you and jump to the next episode. In the other case, it will try the following video for the current episode.

**Note**: once an episode has been downloaded... It won't be downloaded again, unless the *very* video you've downloaded has been replaced on the streaming site. If you want to force the re-download, just `rm episode-to-re-dl.video`.

**Note**: you **can** SIGINT `chain-dl`. It handles it. When you'll restart it, the downloader will resume where he left off.

**Note**: HTTPErrors stops `chain-dl`. As an example, a `404 Error` will cancel the current download session. If it happens that one episode page is causing this, you can simply ignore it (i.e. `ignore_episodes` it).
    
    



