import pandas as pd
from tqdm import tqdm

dat = open("1_AirportsData.sql", 'w')

data = pd.read_csv('1_Airports.csv')

huh = list(data.itertuples(index=False, name=None))

for index in tqdm(range(len(huh))):
    dat.write('INSERT INTO Airports VALUES ' + str(huh[index]) + ';\n')
dat.write('\n')

dat.close()

dat = open("2_AirlinesData.sql", 'w')

data = pd.read_csv('2_Airlines.csv')

huh = list(data.itertuples(index=False, name=None))

for index in tqdm(range(len(huh))):
    dat.write('INSERT INTO Airlines VALUES ' + str(huh[index]) + ';\n')
dat.write('\n')

dat.close()

dat = open("3_PlanesData.sql", 'w')

data = pd.read_csv('3_Planes.csv')

huh = list(data.itertuples(index=False, name=None))

for index in tqdm(range(len(huh))):
    dat.write('INSERT INTO Planes VALUES ' + str(huh[index]) + ';\n')
dat.write('\n')

dat.close()

dat = open("4_PassengersData.sql", 'w')

data = pd.read_csv('4_Passengers.csv')

huh = list(data.itertuples(index=False, name=None))

for index in tqdm(range(len(huh))):
    dat.write('INSERT INTO Passengers VALUES ' + str(huh[index]) + ';\n')
dat.write('\n')

dat.close()

dat = open("5_FlightsData.sql", 'w')

data = pd.read_csv('5_Flights.csv')

huh = list(data.itertuples(index=False, name=None))

for index in tqdm(range(len(huh))):
    dat.write('INSERT INTO Flights VALUES ' + str(huh[index]) + ';\n')
dat.write('\n')

dat.close()

dat = open("6_TicketsData.sql", "w")

data = pd.read_csv('6_Tickets.csv')

huh = list(data.itertuples(index=False, name=None))

for index in tqdm(range(len(huh))):
    dat.write('INSERT INTO Tickets VALUES ' + str(huh[index]) + ';\n')
dat.write('\n')

dat.close()
