import click
import time

from pyowm.weatherapi25 import observation, weather
from Services import weather_svc
from CLI.cli_utils import cli_utils as f
from Services.config.config import WX_LOCATION, WX_UNITS_TEMP


class Context:
    def __init__(self, location):
        self.location = location
        self.weather = weather_svc.Weather()


@click.group()
@click.option("-l", "--location", type=str, help="Location other then default", default = WX_LOCATION, show_default=True)
@click.pass_context
def cli(ctx, location):
    """How's the weather"""
    ctx.obj = Context(location)


@cli.command()
@click.option("-tu", "--temperature-units", type=click.Choice(['c', 'celsius', 'f', 'fahrenheit'], case_sensitive=False), help="Chose temperature units to display", default = WX_UNITS_TEMP, show_default=True)
@click.pass_context
def current(ctx, temperature_units):
    """Current weather at a location"""
    r = ctx.obj.weather.current(location=ctx.obj.location)
    click.echo(
        f' {r["location"]} - {r["status"].upper()} '.center(45, "="))
    if(temperature_units == "c" or temperature_units == "celsius"):
        click.echo(
            f'\U0001F525 Temp:     {round(r["temp"])} - {round(r["min"])}/{round(r["max"])} (min/max)')
    elif(temperature_units == "f" or temperature_units == "fahrenheit"):
        click.echo( f'\U0001F525 Temp:     {round(f.to_fahrenheit(r["temp"]))} - {round(f.to_fahrenheit(r["min"]))}/{round(f.to_fahrenheit(r["max"]))} (min/max)')
    else:
        click.echo(
            f'\U0001F525 Temp:     {round(r["temp"])} - {round(r["min"])}/{round(r["max"])} (min/max)')
    click.echo(f'\U0001F32C  Wind:     {round(r["wind"], 1)}')
    click.echo(
        f'\U0001F4A7 Rain:     {r["rain"] if r["rain"] else "No"}')
    click.echo(f'\U0001F535 Pressure: {r["pressure"]}')
    click.echo(f'\U0001F4A6 Humidity: {r["humidity"]} %')
    click.echo(
        f'\U0001F315 Sunrise: {time.strftime("%H:%m", time.localtime(r["sun_rise"]))} - '
        f'Sunset: {time.strftime("%H:%m", time.localtime(r["sun_set"]))} \U0001F311'
    )

@cli.command()
@click.option("-tu", "--temperature-units", type=click.Choice(['c', 'celsius', 'f', 'fahrenheit'], case_sensitive=False), help="Chose temperature units to display", default = WX_UNITS_TEMP, show_default=True)
@click.pass_context
def forecast(ctx, temperature_units):
    """Forecast for a location"""
    to_display = [wx for wx in ctx.obj.weather.forecast(
        location=ctx.obj.location) if f.is_around_midday(wx["time"])]

    def formatter(data):
        if isinstance(data, float):
            data = round(data, 2) 
        return str(data).center(14)

    click.echo(f' {to_display[0]["location"]} '.center(int(14 * 5.5), "="))
    click.echo(
        "\U0001F4C5 Date:" +
        "".join([formatter(f.convert_epoch_to(wx["time"], "%a %d %b"))
                for wx in to_display])
    )
    if(temperature_units == "c" or temperature_units == "celsius"):
        click.echo("\U0001F525 Temp:" +
               "".join([formatter(wx["temp"]) for wx in to_display]))
    elif(temperature_units == "f" or temperature_units == "fahrenheit"):
        click.echo("\U0001F525 Temp:" +
               "".join([formatter((f.to_fahrenheit(wx["temp"]))) for wx in to_display]))
    click.echo("\U0001F32C  Wind:" +
               "".join([formatter(wx["wind"]) for wx in to_display]))
    click.echo("\U0001F4A7 Rain:" +
               "".join([formatter(wx["rain"] if wx["rain"] else "No") for wx in to_display]))
    click.echo("\U0001F535 Pres:" +
               "".join([formatter(wx["pressure"]) for wx in to_display]))
    click.echo("\U0001F4A6 Humy:" +
               "".join([formatter(wx["humidity"]) for wx in to_display]))