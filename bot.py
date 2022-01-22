import discord
from discord_slash import SlashCommand
import pandas as pd
#from datetime import datetime
import matplotlib.pyplot as plt
import requests

token = 'token'

client = discord.Client()
slash = SlashCommand(client, sync_commands=True)

def main():

    print("covidtesting")
    response = requests.get('https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/resource/ed270bb8-340b-41f9-a7c6-e8ef587e6d11/download/covidtesting.csv')
    # Open file and write the content
    with open('covidtesting.csv', 'wb') as file:
        # A chunk of 128 bytes
        for chunk in response:
            file.write(chunk)
    print("daily cases")
    response = requests.get('https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/resource/8a88fe6d-d8fb-41a3-9d04-f0550a44999f/download/daily_change_in_cases_by_phu.csv')
    # Open file and write the content
    with open('daily_change_in_cases_by_phu.csv', 'wb') as file:
        # A chunk of 128 bytes
        for chunk in response:
            file.write(chunk)
    print("hospitals")
    response = requests.get('https://data.ontario.ca/dataset/8f3a449b-bde5-4631-ada6-8bd94dbc7d15/resource/e760480e-1f95-4634-a923-98161cfb02fa/download/region_hospital_icu_covid_data.csv')
    # Open file and write the content
    with open('region_hospital_icu_covid_data.csv', 'wb') as file:
        # A chunk of 128 bytes
        for chunk in response:
            file.write(chunk)
    print("active cases")
    response = requests.get('https://data.ontario.ca/dataset/1115d5fe-dd84-4c69-b5ed-05bf0c0a0ff9/resource/d1bfe1ad-6575-4352-8302-09ca81f7ddfc/download/cases_by_status_and_phu.csv')
    # Open file and write the content
    with open('cases_by_status_and_phu.csv', 'wb') as file:
        # A chunk of 128 bytes
        for chunk in response:
            file.write(chunk)
    client.run(token)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('/help'))
    print('Bot Ready')

@slash.slash(name="new",description="new COVID data")
async def new(ctx):
    embed=discord.Embed(title="New cases", color=discord.Colour.green())
    daily_cases = pd.read_csv('daily_change_in_cases_by_phu.csv')
    daily_cases = daily_cases.T
    daily_cases.head()
    y = []
    x = []
    for n in range(14,0,-1):
        y.append(daily_cases[len(daily_cases.T)-n][35])
        x.append(daily_cases[len(daily_cases.T)-n][0])
    y=y[-1]
    deaths = pd.read_csv('covidtesting.csv')
    deaths2 = str(int(deaths.newly_reported_deaths[len(deaths)-1]))
    embed.add_field(name="New cases", value=y, inline=True)
    embed.add_field(name="New deaths", value=deaths2, inline=True)
    embed.set_footer(text="Updated on: "+str(deaths['Reported Date'][len(deaths)-1]))
    embed.add_field(name="\u200b", value='\u200b', inline=True)
    embed.add_field(name='\u200b', value='[Source for new cases data](https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/resource/8a88fe6d-d8fb-41a3-9d04-f0550a44999f/download/daily_change_in_cases_by_phu.csv)', inline=True)
    embed.add_field(name='\u200b', value='[Source for new deaths data](https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/resource/ed270bb8-340b-41f9-a7c6-e8ef587e6d11/download/covidtesting.csv)', inline=True)
    embed.add_field(name="\u200b", value='\u200b', inline=True)
    await ctx.send(embed=embed)

@slash.slash(name="graphsummary",description="Graph of past two weeks of new cases, optional argument: days")
async def graphsummary(ctx,*, days = 14):
    if int(days)<1:
        await ctx.send("Error: Days must be >1!")

    await ctx.defer()
    days = int(days)
    print("graph summary")
    y = []
    x = []
    daily_cases = pd.read_csv('daily_change_in_cases_by_phu.csv')
    daily_cases.head()
    daily_cases = daily_cases.T
    daily_cases = daily_cases
    y = []
    x = []
    if days<=150:
        for n in range(days,0,-1):
            y.append(daily_cases[len(daily_cases.T)-n][35])
            x.append(daily_cases[len(daily_cases.T)-n][0])
        for i in range(len(x)):
            x[i] = datetime.strptime(x[i], '%Y-%m-%d').date()
        fig,ax = plt.subplots(figsize=(10,5))
        ax = plt.plot(x,y,label='New cases')
        print(x)
        print(y)
        hospitalisations = pd.read_csv('region_hospital_icu_covid_data.csv')
        hosp = []
        icu = []
        print(type(hospitalisations))
        for n in range(days,0,-1):
            hosp.append(hospitalisations[hospitalisations['oh_region']=='CENTRAL'].hospitalizations.values[n-(days+1)] + hospitalisations[hospitalisations['oh_region']=='EAST'].hospitalizations.values[n-(days+1)] + hospitalisations[hospitalisations['oh_region']=='NORTH'].hospitalizations.values[n-(days+1)] + hospitalisations[hospitalisations['oh_region']=='TORONTO'].hospitalizations.values[n-(days+1)] + hospitalisations[hospitalisations['oh_region']=='WEST'].hospitalizations.values[n-(days+1)])
            icu.append(hospitalisations[hospitalisations['oh_region']=='CENTRAL'].icu_current_covid.values[n-(days+1)] + hospitalisations[hospitalisations['oh_region']=='EAST'].icu_current_covid.values[n-(days+1)] + hospitalisations[hospitalisations['oh_region']=='NORTH'].icu_current_covid.values[n-(days+1)] + hospitalisations[hospitalisations['oh_region']=='TORONTO'].icu_current_covid.values[n-(days+1)] + hospitalisations[hospitalisations['oh_region']=='WEST'].icu_current_covid.values[n-(days+1)])
    else:
        for n in range(days,0,-5):
            y.append(daily_cases[len(daily_cases.T)-n][35])
            x.append(daily_cases[len(daily_cases.T)-n][0])
        for i in range(len(x)):
            x[i] = datetime.strptime(x[i], '%Y-%m-%d').date()
        fig,ax = plt.subplots(figsize=(10,5))
        ax = plt.plot(x,y,label='New cases')
        print(x)
        print(y)
        hospitalisations = pd.read_csv('region_hospital_icu_covid_data.csv')
        hosp = []
        icu = []
        print(type(hospitalisations))
        for n in range(days,0,-5):
            hosp.append(hospitalisations[hospitalisations['oh_region']=='CENTRAL'].hospitalizations.values[n-(days+1)] + hospitalisations[hospitalisations['oh_region']=='EAST'].hospitalizations.values[n-(days+1)] + hospitalisations[hospitalisations['oh_region']=='NORTH'].hospitalizations.values[n-(days+1)] + hospitalisations[hospitalisations['oh_region']=='TORONTO'].hospitalizations.values[n-(days+1)] + hospitalisations[hospitalisations['oh_region']=='WEST'].hospitalizations.values[n-(days+1)])
            icu.append(hospitalisations[hospitalisations['oh_region']=='CENTRAL'].icu_current_covid.values[n-(days+1)] + hospitalisations[hospitalisations['oh_region']=='EAST'].icu_current_covid.values[n-(days+1)] + hospitalisations[hospitalisations['oh_region']=='NORTH'].icu_current_covid.values[n-(days+1)] + hospitalisations[hospitalisations['oh_region']=='TORONTO'].icu_current_covid.values[n-(days+1)] + hospitalisations[hospitalisations['oh_region']=='WEST'].icu_current_covid.values[n-(days+1)])
    hosp.reverse()
    icu.reverse()
    print(hosp)
    print(icu)
    ax = plt.plot(x,hosp, label='Hospitalisations')
    ax = plt.plot(x,icu,label = 'ICUs')
    plt.fill_between(x,y)
    plt.fill_between(x,hosp)
    plt.fill_between(x,icu)
    plt.xlim([min(x),max(x)])
    plt.ylim([0,max(y)])
    plt.legend()
    fig.savefig('new_cases.png',bbox_inches='tight')
    embed= discord.Embed(color=discord.Colour.green())
    embed.add_field(name='Summary over past ' + str(days) + ' days:',value = 'Cases, hospitalizations, ICUs')
    file = discord.File("new_cases.png")
    embed.set_image(url="attachment://new_cases.png")
    embed.add_field(name='\u200b', value='[Source for daily cases data](https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/resource/8a88fe6d-d8fb-41a3-9d04-f0550a44999f/download/daily_change_in_cases_by_phu.csv)', inline=True)
    embed.add_field(name='\u200b', value='[Source for hospitalizations data](https://data.ontario.ca/dataset/8f3a449b-bde5-4631-ada6-8bd94dbc7d15/resource/e760480e-1f95-4634-a923-98161cfb02fa/download/region_hospital_icu_covid_data.csv)', inline=True)
    await ctx.send(embed=embed,file=file)

@slash.slash(name="hospitalizations",description="Graph of past two weeks of hospitalizations and ICUs, optional argument: days")
async def hospitalisations(ctx,*,days=14):
    if int(days)<1:
        await ctx.send("Error: Days must be >1!")

    await ctx.defer()
    days = int(days)
    print("hospitalizations")
    y = []
    x = []
    daily_cases = pd.read_csv('daily_change_in_cases_by_phu.csv')
    daily_cases.head()
    daily_cases = daily_cases.T
    daily_cases = daily_cases
    y = []
    x = []
    if days<150:
        for n in range(days,0,-1):
            y.append(daily_cases[len(daily_cases.T)-n][35])
            x.append(daily_cases[len(daily_cases.T)-n][0])
        for i in range(len(x)):
            x[i] = datetime.strptime(x[i], '%Y-%m-%d').date()
    else:
        for n in range(days,0,-5):
            y.append(daily_cases[len(daily_cases.T)-n][35])
            x.append(daily_cases[len(daily_cases.T)-n][0])
        for i in range(len(x)):
            x[i] = datetime.strptime(x[i], '%Y-%m-%d').date()
    fig,ax = plt.subplots(figsize=(10,5))
    hospitalisations = pd.read_csv('region_hospital_icu_covid_data.csv')
    date  = hospitalisations
    date = date.T
    hosp = []
    icu = []
    print(type(hospitalisations))
    if days<150:
        for n in range(days,0,-1):
            hosp.append(hospitalisations[hospitalisations['oh_region']=='CENTRAL'].hospitalizations.values[n-(days+1)] + hospitalisations[hospitalisations['oh_region']=='EAST'].hospitalizations.values[n-(days+1)] + hospitalisations[hospitalisations['oh_region']=='NORTH'].hospitalizations.values[n-(days+1)] + hospitalisations[hospitalisations['oh_region']=='TORONTO'].hospitalizations.values[n-(days+1)] + hospitalisations[hospitalisations['oh_region']=='WEST'].hospitalizations.values[n-(days+1)])
            icu.append(hospitalisations[hospitalisations['oh_region']=='CENTRAL'].icu_current_covid.values[n-(days+1)] + hospitalisations[hospitalisations['oh_region']=='EAST'].icu_current_covid.values[n-(days+1)] + hospitalisations[hospitalisations['oh_region']=='NORTH'].icu_current_covid.values[n-(days+1)] + hospitalisations[hospitalisations['oh_region']=='TORONTO'].icu_current_covid.values[n-(days+1)] + hospitalisations[hospitalisations['oh_region']=='WEST'].icu_current_covid.values[n-(days+1)])
        print(x)
        print(hosp)
        print(icu)
    else:
        for n in range(days,0,-5):
            hosp.append(hospitalisations[hospitalisations['oh_region']=='CENTRAL'].hospitalizations.values[n-(days+1)] + hospitalisations[hospitalisations['oh_region']=='EAST'].hospitalizations.values[n-(days+1)] + hospitalisations[hospitalisations['oh_region']=='NORTH'].hospitalizations.values[n-(days+1)] + hospitalisations[hospitalisations['oh_region']=='TORONTO'].hospitalizations.values[n-(days+1)] + hospitalisations[hospitalisations['oh_region']=='WEST'].hospitalizations.values[n-(days+1)])
            icu.append(hospitalisations[hospitalisations['oh_region']=='CENTRAL'].icu_current_covid.values[n-(days+1)] + hospitalisations[hospitalisations['oh_region']=='EAST'].icu_current_covid.values[n-(days+1)] + hospitalisations[hospitalisations['oh_region']=='NORTH'].icu_current_covid.values[n-(days+1)] + hospitalisations[hospitalisations['oh_region']=='TORONTO'].icu_current_covid.values[n-(days+1)] + hospitalisations[hospitalisations['oh_region']=='WEST'].icu_current_covid.values[n-(days+1)])
        print(x)
        print(hosp)
        print(icu)
    x.reverse()
    ax = plt.plot(x,hosp, label='Hospitalisations')
    ax = plt.plot(x,icu,label = 'ICUs')
    plt.fill_between(x,hosp)
    plt.fill_between(x,icu)
    x.reverse()
    plt.xlim([min(x),max(x)])
    plt.ylim([0,max(hosp)])
    plt.legend()
    fig.savefig('hospitalisations.png',bbox_inches='tight')
    embed= discord.Embed(color=discord.Colour.green())
    embed.add_field(name='Summary over past ' + str(days) + ' days:',value = 'Hospitalizations, ICUs')
    file = discord.File("hospitalisations.png")
    embed.set_image(url="attachment://hospitalisations.png")
    embed.add_field(name='\u200b', value='[Source](https://data.ontario.ca/dataset/8f3a449b-bde5-4631-ada6-8bd94dbc7d15/resource/e760480e-1f95-4634-a923-98161cfb02fa/download/region_hospital_icu_covid_data.csv)', inline=True)
    await ctx.send(embed=embed,file=file)


@slash.slash(name="positivity",description="Graph of past two weeks of positivity rate (%), optional argument: days")
async def positivity(ctx,*,days=14):
    if int(days)<1:
        await ctx.send("Error: Days must be >1!")

    await ctx.defer()
    days = int(days)
    print("positivity")
    x = []
    daily_cases = pd.read_csv('covidtesting.csv')
    daily_cases.head()
    daily_cases = daily_cases.T
    x = []
    if days<150:
        for n in range(days,0,-1):
            x.append(daily_cases[len(daily_cases.T)-n][0])
        for i in range(len(x)):
            x[i] = datetime.strptime(x[i], '%Y-%m-%d').date()
        posit = []
        for n in range(days,0,-1):
            posit.append(daily_cases[len(daily_cases.T)-n][10])
    else:
        for n in range(days,0,-5):
            x.append(daily_cases[len(daily_cases.T)-n][0])
        for i in range(len(x)):
            x[i] = datetime.strptime(x[i], '%Y-%m-%d').date()
        posit = []
        for n in range(days,0,-5):
            posit.append(daily_cases[len(daily_cases.T)-n][10])
    print(x)
    print(posit)
    fig,ax = plt.subplots(figsize=(10,5))
    ax = plt.plot(x,posit)
    plt.fill_between(x,posit)
    plt.xlim([min(x),max(x)])
    plt.ylim([0,max(posit)])
    #plt.ylabel("%", fontsize=)
    plt.legend()
    fig.savefig('posit.png',bbox_inches='tight')
    embed= discord.Embed(color=discord.Colour.green())
    embed.add_field(name='Summary over past ' + str(days) + ' days:',value = 'Positivity rate (%)')
    file = discord.File("posit.png")
    embed.set_image(url="attachment://posit.png")
    embed.add_field(name='\u200b', value='[Source](https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/resource/ed270bb8-340b-41f9-a7c6-e8ef587e6d11/download/covidtesting.csv)', inline=True)
    await ctx.send(embed=embed,file=file)

@slash.slash(name="total",description="total COVID data")
async def total(ctx):
    print("Total data")
    await ctx.defer()
    deaths = pd.read_csv('covidtesting.csv')
    total_active = pd.read_csv('cases_by_status_and_phu.csv')
    active = total_active.loc[total_active['FILE_DATE']==str(total_active['FILE_DATE'][len(total_active)-1]),'ACTIVE_CASES'].sum()
    print(active)
    total_cases = str(int(deaths['Total Cases'][len(deaths)-1]))
    deaths2 = str(int(deaths.Deaths[len(deaths)-1]))
    embed = discord.Embed(title = 'Cumulative numbers',color=discord.Colour.green())
    embed.add_field(name='Total deaths', value=deaths2, inline=True)
    embed.add_field(name='Total active cases',value=active, inline=True)
    embed.add_field(name='Total cases (cumulative)', value=total_cases, inline=True)
    embed.set_footer(text="Updated on: "+str(deaths['Reported Date'][len(deaths)-1]))
    embed.add_field(name='\u200b', value='[Source for deaths data](https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/resource/ed270bb8-340b-41f9-a7c6-e8ef587e6d11/download/covidtesting.csv)', inline=True)
    embed.add_field(name='\u200b', value='[Source for active cases data](https://data.ontario.ca/dataset/1115d5fe-dd84-4c69-b5ed-05bf0c0a0ff9/resource/d1bfe1ad-6575-4352-8302-09ca81f7ddfc/download/cases_by_status_and_phu.csv)', inline=True)
    embed.add_field(name='\u200b', value='[Source for cumulative cases data](https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/resource/ed270bb8-340b-41f9-a7c6-e8ef587e6d11/download/covidtesting.csv)', inline=True)
    await ctx.send(embed=embed)

@slash.slash(name="vaccine",description="vaccine data")
async def vaccine(ctx):
    print('Vaccine data')
    await ctx.defer()
    embed = discord.Embed(title='Vaccine data', color=discord.Colour.green())
    embed.add_field(name='Doses yesterday', value=Vaccine(0), inline=True)
    embed.add_field(name='Total Doses', value=Vaccine(1), inline=True)
    embed.add_field(name= 'Fully Imunized', value=Vaccine(2), inline=True)
    embed.add_field(name='Partially immunized', value=Vaccine(3), inline=True)
    embed.add_field(name='Boosted', value=Vaccine(5), inline=True)
    embed.add_field(name='\u200b', value='\u200b', inline =True)
    embed.add_field(name='\u200b', value='[Source 1 for vaccine data](https://data.ontario.ca/dataset/752ce2b7-c15a-4965-a3dc-397bf405e7cc/resource/775ca815-5028-4e9b-9dd4-6975ff1be021/download/vaccines_by_age.csv)', inline=True)
    embed.add_field(name='\u200b', value='[Source 2 for vaccine data](https://data.ontario.ca/dataset/752ce2b7-c15a-4965-a3dc-397bf405e7cc/resource/8a89caa9-511c-4568-af89-7f2174b4378c/download/vaccine_doses.csv)')
    date = Vaccine(4)
    embed.set_footer(text="Updated on: "+str(date))
    await ctx.send(embed=embed)

@slash.slash(name="help",description="List of commands and descriptions")
async def help(ctx):
    embed = discord.Embed(title='Help', description='Commands:', color=discord.Colour.green())
    embed.add_field(name='```new```', value='Returns new cases and deaths in Ontario')
    embed.add_field(name='```total```', value='Returns total cases and deaths in Ontario')
    embed.add_field(name='```vaccine```', value='Returns vaccine stats for Ontario')
    embed.add_field(name='```graphsummary```', value='Returns a graph of cases, hospitalizations and ICUs over the last two weeks')
    embed.add_field(name='```hospitalizations```', value='Returns a graph of hospitalizations and ICUs over the last two weeks')
    embed.add_field(name='```positivity```', value='Returns a graph of positivity rate (%) over the last two weeks')
    await ctx.send(embed=embed)

def Vaccine(value):
    try:
        vaccine_data = pd.read_csv('https://data.ontario.ca/dataset/752ce2b7-c15a-4965-a3dc-397bf405e7cc/resource/775ca815-5028-4e9b-9dd4-6975ff1be021/download/vaccines_by_age.csv')
        cond = (vaccine_data['Agegroup']=='Ontario_5plus')
        partpercent = vaccine_data[cond].Percent_at_least_one_dose[-1:]*100
        partpercent = str(list(partpercent)[0])
        fullypercent = vaccine_data[cond].Percent_fully_vaccinated[-1:]*100
        fullypercent = str(list(fullypercent)[0])
        part_vaxxed = vaccine_data[cond]['At least one dose_cumulative'][-1:]
        part_vaxxed = format(int(list(part_vaxxed)[0]),',d')
        fully_vaxxed = vaccine_data[cond].fully_vaccinated_cumulative[-1:]
        fully_vaxxed = format(int(list(fully_vaxxed)[0]),',d')
        boosted = vaccine_data[cond].third_dose_cumulative[-1:]
        boosted = format(int(list(boosted)[0]),',d')
        boostedpercent = vaccine_data[cond].Percent_3doses[-1:]*100
        boostedpercent = str(list(partpercent)[0])
        total_data = pd.read_csv('https://data.ontario.ca/dataset/752ce2b7-c15a-4965-a3dc-397bf405e7cc/resource/8a89caa9-511c-4568-af89-7f2174b4378c/download/vaccine_doses.csv')
        if value == 0:
            daily_doses = total_data.previous_day_total_doses_administered[-1:]
            daily_doses = format(int(list(daily_doses)[0]),',d')
            return(str(daily_doses))
        elif value == 1:
            total_doses = total_data.total_doses_administered[-1:]
            total_doses = format(int(list(total_doses)[0]),',d')
            return(str(total_doses))
        elif value == 2:
            return(fully_vaxxed + ' (' + fullypercent + '%)')
        elif value == 3:
             return(part_vaxxed + ' (' + partpercent + '%)')
        elif value ==4:
            return(vaccine_data.Date[len(vaccine_data)-1])
        elif value == 5:
             return(boosted + ' (' + boostedpercent + '%)')

    except Exception as e:
        print(e)
        return 'Error retrieving data'

if __name__ == '__main__':
    main()
