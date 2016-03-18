#!/usr/bin/python

import click
from downloader import Downloader
from collector import Collector
from searcher import Searcher

@click.group()
def cli():
    click.echo("")

@cli.command()
@click.option("--name", prompt='Please input the name of Meiju you want to update info("all" means update all Meiju info)')
def update(name):
    if name == "all":
        collector = Collector()
        collector.save_all_meiju_update_info()
        collector.write_all_meiju_info_to_file()
    else:
        collector = Collector()
        if collector.is_meiju_info_file_exist():
            collector.read_all_meiju_info_from_file()
            if name in collector.meiju_ename_inst_dict:
                collector.save_all_meiju_update_info()
                collector.write_all_meiju_info_to_file()
            else:
                click.echo("Failed to lookup Meiju named %s" % name)
        else:
            collector.save_all_meiju_info()
            collector.write_all_meiju_info_to_file()

@cli.command()
@click.option("--keywords", prompt='Please input the keywords of the Meiju you want to search')
def search(keywords):

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
    return

@cli.command()
@click.option("--name", prompt='Please input the name of Meiju which you want to see the details')
def show(name):

    collector = Collector()
    if collector.is_meiju_info_file_exist():
        collector.read_all_meiju_info_from_file()
    else:
        collector.save_all_meiju_info()
        collector.write_all_meiju_info_to_file()
    if name in collector.meiju_ename_inst_dict:
        meiju_inst = collector.meiju_ename_inst_dict[name]
        click.echo("Detailed information for Meiju - %s" % name)
        for (season_id, season_inst) in meiju_inst.season_id_inst_dict.items():
            output = "Season %d [" % season_id
            for (episode_id, episode_inst) in season_inst.episode_id_inst_dict.items():
                output += "Ep%d, " % episode_id
            output += "]"
            click.echo(output)
    else:
        click.echo("Failed to find any Meiju named %s" % name)
    return

@cli.command()
@click.option("--name", prompt='Please input the name of Meiju')
@click.option("--season", prompt='Please input the Season number that you want to download (0 means download all season)')
@click.option("--episode", prompt='Please input the Episode number that you want to download (0 means download all episode)')
@click.option("--path", prompt='Please input the destination directory path')
def download(name, season, episode, path):

    collector = Collector()
    if collector.is_meiju_info_file_exist():
        collector.read_all_meiju_info_from_file()
    else:
        collector.save_all_meiju_info()
        collector.write_all_meiju_info_to_file()
    if name in collector.meiju_ename_inst_dict:
        if int(season) == 0 and int(episode) == 0:
            downloader = Downloader()
            downloader.download_meiju(collector, name, path)
        elif int(season) != 0 and int(episode) == 0:
            downloader = Downloader()
            downloader.download_meiju_season(collector, name, int(season), path)
        elif int(season) != 0 and int(episode) != 0:
            downloader = Downloader()
            downloader.download_meiju_episode(collector, name, int(season), int(episode), path)
    else:
        click.echo("Failed to find Meiju named is %s" % name)
    return

if __name__ == "__main__":
    cli()
