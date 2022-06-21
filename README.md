# A COVID-19 and Monkeypox cases tracker bot for Discord

A Covid-19 and monkeypox cases tracker bot made for the popular social media app Discord. The bot tracks:

- new cases, hospitalizations, ICU cases for COVID-19 in Ontario, Canada
- Covid N1 and N2 gene concentrations in Ontario's wastewater, and
- Monkeypox cases worldwide

If you want to add this bot to your server, use [this invite link](https://discord.com/api/oauth2/authorize?client_id=875446981219217469&permissions=277025475584&scope=bot%20applications.commands)!

## Contributing:

If you'd like to contribute with areas such as code improvement, or data visualization, etc., feel free to open a PR and I will take a look.

## How it works:

For COVID-19 data:

- The bot pulls all its data from [here for the case numbers](https://data.ontario.ca/dataset?q=covid) and [here for the wastewater data](https://covid19-sciencetable.ca/ontario-dashboard/)

- The bot parses and extracts the data, plots the case numbers and embed the plots in a discord `Embed` object

For Monkeypox data:

- The bot pulls all its data from [here](https://raw.githubusercontent.com/globaldothealth/monkeypox/main/latest.csv)

- The bot then extracts the numbers for the top 5 countries with the highest number of cases, and embeds it in an `Embed` object


## TODO

Add visualizations for Monkeypox case numbers, aka a way to visualize how cases have been changing over time. Figre out a better way to present COVID-19 case plots.
