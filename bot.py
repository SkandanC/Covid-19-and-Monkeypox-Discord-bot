import discord
from discord_slash import SlashCommand
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import requests


# discord bot token
token = 'token'


# initialize slahs commands and client instance
client = discord.Client()
slash = SlashCommand(client, sync_commands=True)


def main():

    client.run(token) # run the bot


# Set status
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('/help'))
    print('Bot Ready')


def compute_data_graphsum(days: int):
    x = []
    y = []
    hosp = []
    icu = []

    # read daily cases data    
    daily_cases = pd.read_csv('https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/resource/8a88fe6d-d8fb-41a3-9d04-f0550a44999f/download/daily_change_in_cases_by_phu.csv').T

    # extract x and y data
    step = -1 if days<=150 else -5
    for n in range(days,0,step):
        y.append(daily_cases[len(daily_cases.T)-n][35])
        x_ = daily_cases[len(daily_cases.T)-n][0]
        x.append(datetime.strptime(x_, '%Y-%m-%d').date()) 

    # read hospitalizations data
    hospitalisations = pd.read_csv('https://data.ontario.ca/dataset/8f3a449b-bde5-4631-ada6-8bd94dbc7d15/resource/e760480e-1f95-4634-a923-98161cfb02fa/download/region_hospital_icu_covid_data.csv')

    # extract hospitalizations and ICU data
    for n in range(days,0,step):
        hosp.append(hospitalisations[hospitalisations['oh_region']=='CENTRAL'].hospitalizations.values[n-(days+1)] + hospitalisations[hospitalisations['oh_region']=='EAST'].hospitalizations.values[n-(days+1)] + hospitalisations[hospitalisations['oh_region']=='NORTH'].hospitalizations.values[n-(days+1)] + hospitalisations[hospitalisations['oh_region']=='TORONTO'].hospitalizations.values[n-(days+1)] + hospitalisations[hospitalisations['oh_region']=='WEST'].hospitalizations.values[n-(days+1)])
        icu.append(hospitalisations[hospitalisations['oh_region']=='CENTRAL'].icu_current_covid.values[n-(days+1)] + hospitalisations[hospitalisations['oh_region']=='EAST'].icu_current_covid.values[n-(days+1)] + hospitalisations[hospitalisations['oh_region']=='NORTH'].icu_current_covid.values[n-(days+1)] + hospitalisations[hospitalisations['oh_region']=='TORONTO'].icu_current_covid.values[n-(days+1)] + hospitalisations[hospitalisations['oh_region']=='WEST'].icu_current_covid.values[n-(days+1)])

    return (x, y, hosp, icu)


# send a graph of covid-19 cases, hospitalizations and ICU cases in an embed
@slash.slash(name="Covid-19",description="Graph of past two weeks of new cases, optional argument: days")
async def graphsummary(ctx,*, days = 14):
    if int(days)<2:
        await ctx.send("Error: Days must be >2!")

    await ctx.defer()

    days = int(days)

    x, y, hosp, icu = compute_data_graphsum(days)
    hosp.reverse()
    icu.reverse()

    fig, _= plt.subplots(figsize=(10,5))
    _ = plt.plot(x,y,label='New cases')

    # plot the data
    _ = plt.plot(x,hosp, label='Hospitalisations')
    _ = plt.plot(x,icu,label = 'ICUs')
    plt.fill_between(x,y)
    plt.fill_between(x,hosp)
    plt.fill_between(x,icu)
    plt.xlim([min(x),max(x)])
    plt.ylim([0,max(y)])
    plt.legend()

    # save the plot as an image to be later sent in an embed
    fig.savefig('new_cases.png',bbox_inches='tight')

    # initialize and edit embed object
    embed= discord.Embed(color=discord.Colour.green())
    embed.add_field(name=f'Summary over past {days} days:',value = 'Cases, hospitalizations, ICUs')
    file = discord.File("new_cases.png")
    embed.set_image(url="attachment://new_cases.png")
    embed.add_field(name='\u200b', value='[Source for daily cases data](https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/resource/8a88fe6d-d8fb-41a3-9d04-f0550a44999f/download/daily_change_in_cases_by_phu.csv)', inline=True)
    embed.add_field(name='\u200b', value='[Source for hospitalizations data](https://data.ontario.ca/dataset/8f3a449b-bde5-4631-ada6-8bd94dbc7d15/resource/e760480e-1f95-4634-a923-98161cfb02fa/download/region_hospital_icu_covid_data.csv)', inline=True)

    # send message
    await ctx.send(embed=embed,file=file)


# send a graph of covid-19 wastewater data in an embed
@slash.slash(name="Wastewater",description="Graph of covid gene traces in Ontario's wastewater")
async def Wastewater(ctx):
   
    await ctx.defer()
    print("Re\n")

    # get wastewater graph    
    url = 'https://covid19-sciencetable.ca/wp-content/uploads/' + (datetime.now()-timedelta(1)).strftime("%Y/%m") + '/' + (datetime.now()-timedelta(1)).strftime("%Y-%m-%d") + '-Province-Wide-COVID-19-Wastewater-Signal-in-Ontario.png'
    img_data = requests.get(url).content
    with open('wastewater.jpg', 'wb') as handler:
        handler.write(img_data)

    # initialize and edit embed
    embed= discord.Embed(color=discord.Colour.green())
    embed.add_field(name="Covid-19 N1 and N2 gene standardized concentrations in Ontario's wastewater", value='\u200b')
    file = discord.File("wastewater.jpg")
    embed.set_image(url="attachment://wastewater.jpg")
    embed.add_field(name='\u200b', value=f'[Source]({url})', inline=True)

    await ctx.send(embed=embed,file=file)


# send data of number of monkeypox cases worldwide in an embed
@slash.slash(name="monkeypox",description="global monkeypox data summarized")
async def monkeypox(ctx):
    await ctx.defer()

    # get cases data
    df = pd.read_csv("https://raw.githubusercontent.com/globaldothealth/monkeypox/main/latest.csv")

    # extract confirmed cases and neglect suspected and discarded cases
    confirmed = df.loc[df['Status'] == 'confirmed']

    # sort by country and extract top 5 countries with highest monkeypox cases
    countries = {country: confirmed[confirmed.Country == country].shape[0] for country in confirmed.Country.unique()}
    top_5 = sorted(countries, key=countries.get, reverse=True)[:5]

    # initializze and edit embed
    embed = discord.Embed(title="Global top 5 monkeypox cases (and in Canada)", color=discord.Colour.green())
    for country in top_5:
        embed.add_field(name=country, value=countries[country], inline=True)
    if 'Canada' not in top_5:
        embed.add_field(name='Canada', value=countries['Canada'], inline=True)
    embed.add_field(name='\u200b', value='[Source for data](https://raw.githubusercontent.com/globaldothealth/monkeypox/main/latest.csv)', inline=True)

    await ctx.send(embed=embed)


# help command
@slash.slash(name="help",description="List of commands and descriptions")
async def help(ctx):
    embed = discord.Embed(title='Help', description='Commands:', color=discord.Colour.green())
    embed.add_field(name='```graphsummary```', value='Returns a graph of cases, hospitalizations and ICUs over the last two weeks')
    embed.add_field(name='```wastewater```', value="Returns a graph of Covid N1 and N2 gene in Ontario's wastewater")
    embed.add_field(name='```monkeypox```', value="Returns data on monkeypox cases globally")
    await ctx.send(embed=embed)


if __name__ == '__main__':
    main()
