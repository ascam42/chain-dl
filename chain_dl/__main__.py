#!/usr/bin/env python3

"""
    A simple chained videos downloader.
    Using the awesome youtube-dl !
"""


import                  log
import                  config
from globals    import  *
import                  argparse
import                  configparser
import                  urllib.request
from bs4        import  BeautifulSoup
from subprocess import  call





def __config_parser():
    """
        Configuring command-line arguments parser
    """
    ret = argparse.ArgumentParser(description="A simple chained videos"
                                  + " downloader")

    ret.add_argument('-c', '--config-file',
                     help='the configuration file to be used for download')
    return (ret)


def __episode_not_skipped(idx, video_desc, config_specs):
    ret = True

    if (START_EPISODE in config_specs) and \
       (idx < config_specs[START_EPISODE]):
        ret = False
        log.warn("Skipping:", video_desc);
    return (ret)


def __episode_not_ignored(idx, video_desc, config_specs):
    ret = True

    if (IGNORE_EPISODES in config_specs) and \
       (idx in config_specs[IGNORE_EPISODES]):
        ret = False
        log.warn("Ignoring:", video_desc)
    return (ret)


def __get_embed_links(episode_page, config_specs):
    """
        Using BeautifulSoup to list all URLS
        of possible embed videos in the page
    """
    video_links = []

    if CONTENT_CONTAINER_ID in config_specs:
        links_container_id = config_specs[CONTENT_CONTAINER_ID]
        container = episode_page.find(id=links_container_id)
        video_links = container.find_all('iframe', src=True)
    else:
        links_container_class = config_specs[CONTENT_CONTAINER_CLASS]
        for container in episode_page.find_all(
                True, {"class": links_container_class.split(' ')}):
            video_links += container.find_all('iframe', src=True)
    return (video_links)


def __get_list_links(list_page, config_specs):
    """
        Using BeautifulSoup to list all URLS
        of listed episodes, based on user's config
    """
    sub_links = []

    if LIST_CONTAINER_ID in config_specs:
        links_container_id = config_specs[LIST_CONTAINER_ID]
        sub_links = list_page.find(
            id=links_container_id).find_all('a', href=True)
    else:
        links_container_class = config_specs[LIST_CONTAINER_CLASS]
        for container in list_page.find_all(
                True, {"class": links_container_class.split(' ')}):
            sub_links += container.find_all('a', href=True)
    return (sub_links)


def __find_best_hrefs(episode_page_url,
                      config_specs):
    """
        Finding urls of embed videos and selecting the
        first corresponding to user's preferred host
    """
    episode_page_html = urllib.request.urlopen(
        episode_page_url, timeout=config_specs[TIMEOUT]).read()
    episode_page = BeautifulSoup(episode_page_html, "lxml")
    video_links = __get_embed_links(episode_page, config_specs)
    ret = []

    log.ok("Opened episode URL: " + episode_page_url)
    if video_links is not None and len(video_links) > 0:
        for link in reversed(video_links):
            if config_specs[PREFERRED_HOST] is not None and \
               link['src'].startswith(config_specs[PREFERRED_HOST]):
                ret.insert(0, link['src'])
            else:
                ret.append(link['src'])
    return (ret)


def __download_video(video_urls, video_desc, config_specs):
    i = 0
    filename = ""
    download_status = 1

    if config_specs[TITLE] is not None:
        filename = config_specs[TITLE] + " - "
    filename += video_desc + "= %(title)s.flv"
    while i < len(video_urls) and download_status != 0:
        log.shiny("Downloading:", video_desc, "from:",
                  log.BOLD + video_urls[i])
        download_args = [YOUTUBE_DL_COMMAND,
                         "-o",
                         filename,
                         video_urls[i]]
        download_status = call(download_args)
        i += 1
    if download_status == 0:
        log.ok_shiny("Download complete:", video_desc)
    else:
        log.ko_shiny("Download failure:", video_desc,
                     "No suitable video found... :(")


def show_download(dl_config):
    """
        Do the download thing you know
    """
    i = 0
    config_specs = config.get_specs(dl_config)

    url = dl_config[DOWNLOAD]['url']
    main_html = urllib.request.urlopen(
        url, timeout=int(
            dl_config[DOWNLOAD][TIMEOUT])).read()
    main_page = BeautifulSoup(main_html, "lxml")
    sub_links = __get_list_links(main_page, config_specs)

    log.ok("Opened list URL: " + url)
    for link in sub_links:
        if __episode_not_skipped(i, link.contents[0], config_specs) and \
           __episode_not_ignored(i, link.contents[0], config_specs):
            video_hrefs = __find_best_hrefs(link['href'], config_specs)
            if len(video_hrefs) > 0:
                __download_video(video_hrefs, link.contents[0],
                        config_specs)
            else:
                log.warn("No downloadable link found at URL: " + link['href'])
        i += 1


if __name__ == '__main__':
    parser = __config_parser()
    prog_args = parser.parse_args()
    config_file = DEFAULT_CONFIG_FILE
    config_contents = configparser.ConfigParser()

    if prog_args.config_file is not None:
        config_file = prog_args.config_file
    config_contents.read(config_file)
    try:
        show_download(config_contents)
    except KeyboardInterrupt:
        log.ko("Keyboard interruption")
        exit(1)
    except urllib.error.HTTPError as err:
        log.ko("HTTPError:", err)
        exit(2)

