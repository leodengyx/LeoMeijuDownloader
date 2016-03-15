#!/usr/bin/python

import click
from downloader import Downloader
from collector import Collector
from searcher import Searcher

@click.group()
def cli():
    click.echo("cli")


#@cli.command()
#@click.argument("keywords", nargs=-1)
def search(keywords):
    click.echo("search_entry. keywords=%s" % keywords)
    keyword_list = keywords.split(" ")
    collector = Collector()
    if collector.is_meiju_info_file_exist():
        collector.read_all_meiju_info_from_file()
    else:
        collector.save_all_meiju_info()
        collector.write_all_meiju_info_to_file()
    searcher = Searcher()
    meiju_ename_list = searcher.search_meiju_list_by_english_name_keyword(collector, keyword_list)
    click.echo("Total %d Meiju is found. Following are the lists:" % len(meiju_ename_list))
    for meiju_ename in meiju_ename_list:
        click.echo("%s" % meiju_ename)
    if len(meiju_ename_list) != 0:
        click.echo("Now you can use command 'LeoMeijuDownloader download' to download.")
    return


#@cli.command()
#@click.option("--name", prompt='Please input the name of Meiju:')
#@click.option("--path", prompt='Please input the destination directory path:')
def download(name, path):
    click.echo("download_entry")
    collector = Collector()
    if collector.is_meiju_info_file_exist():
        collector.read_all_meiju_info_from_file()
    else:
        collector.save_all_meiju_info()
        collector.write_all_meiju_info_to_file()
    if name in collector.meiju_ename_inst_dict:
        downloader = Downloader()
        downloader.download_meiju(collector.meiju_ename_inst_dict[name], path)
    else:
        click.echo("Failed to find Meiju whose name is %s" % name)
    return

if __name__ == "__main__":
    #cli()
    download("The Big Bang Theory", "C:\Personal")
