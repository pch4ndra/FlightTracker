from xml.dom.minidom import ReadOnlySequentialNamedNodeMap
import numpy as np
import pandas as pd
import names
import random
import datetime
import math
from time import sleep
from tqdm import tqdm

def GeneratePassengers(amount):
    cols = ['Name', 'MainAirline', 'RewardsID', 'Age', 'Gender', 'Race', 'HomeAirport']
    airports = pd.read_csv('1_Airports.csv')['IATACode'].tolist()
    airlines = pd.read_csv('2_Airlines.csv')['IATACode'].tolist()
    races = ['White', 'Black/African American', 'Asian', 'Native American/Alaska Native', 'Native Hawaiian/Pacific Islander', 'Hispanic/Latino']

    totalrewards = []
    for line in airlines:
        for i in range(10000,100000):
            totalrewards.append(line+str(i))

    df = pd.DataFrame(columns=cols)

    for i in tqdm(range(amount)):
        a = random.randint(0,1)

        # NAME
        name = names.get_full_name('male') if a == 0 else names.get_full_name('female')

        # MAINAIRLINE and REWARDSID
        index = random.randint(0,len(totalrewards) - 1)
        rewardsid = totalrewards[index]
        airline = rewardsid[:2]
        totalrewards.remove(rewardsid)

        # AGE
        age = random.randint(22,84)

        # GENDER
        gender = "M" if a == 0 else "F"

        # RACE
        race = races[random.randint(0,len(races)-1)]

        #HOMEAIRPORT
        homeairport = airports[random.randint(0,len(airports) - 1)]

        df.loc[len(df.index)] = [name, airline, rewardsid, age, gender, race, homeairport] 

    df.to_csv('4_Passengers.csv', index=False)

def GenerateFlights(amount):
    cols = ['IATACode', 'FlightNum', 'DepartFrom', 'Destination', 'Manufacturer', 'Model', 'TakeoffDate']
    
    airports = pd.read_csv('1_Airports.csv')['IATACode'].tolist()
    airlines = pd.read_csv('2_Airlines.csv')['IATACode'].tolist()
    planes = np.array([pd.read_csv('3_Planes.csv')['Manufacturer'].tolist(),pd.read_csv('3_Planes.csv')['Model'].tolist()]).T.tolist()
    numplanes = len(planes) - 1
    numairports = len(airports) - 1
    numairlines = len(airlines) - 1
    
    df = pd.DataFrame(columns=cols)

    oldflights = []
    totalflights = {}
    for air in airlines:
        totalflights[air] = [air + str(i) for i in range(1000,10000)]


    for i in tqdm(range(amount)):
        # IATA
        iata = airlines[random.randint(0,numairlines)]
        
        # FLIGHTNUM
        flight_num = totalflights[iata][random.randint(0,len(totalflights[iata])-1)]
        totalflights[iata].remove(flight_num)

        # DepartFrom and Destination
        depfrom = airports[random.randint(0,numairports)]
        dest = airports[random.randint(0,numairports)]
        while (dest == depfrom): dest = airports[random.randint(0,numairports)]

        # 'Manufacturer', 'Model'
        manu, model = planes[random.randint(0,numplanes)]

        # takeoff date
        start_date = datetime.date(2020, 1, 1)
        end_date = datetime.date(2022, 12, 31)

        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        random_date = start_date + datetime.timedelta(days=random_number_of_days)

        takeoffdate = random_date.strftime("%Y-%m-%d")

        df.loc[len(df.index)] = [iata, flight_num, depfrom, dest, manu, model, takeoffdate]

    df.to_csv('5_Flights.csv', index=False)

def GenerateTickets():
    cols = ['TicketID', 'Airline', 'FlightNum', 'RewardsID', 'Price']
    planes = pd.read_csv('3_Planes.csv')
    # ['IATACode', 'FlightNum', 'DepartFrom', 'Destination', 'Manufacturer', 'Model', 'TakeoffDate']
    flights = pd.read_csv('5_Flights.csv')

    df = pd.DataFrame(columns=cols)

    print(">>> populating totalTicketIDs...")
    totaltickid = {}
    for air in ['SW', 'HA', 'DL', 'AS', 'UA', 'AA']:
        totaltickid[air] = [air + str(i) for i in range(1000000,10000000)]
    print(">>> populated totalTicketIDs")

    for index in range(100): #range(flights.shape[0]):
        passengers = pd.read_csv('4_Passengers.csv')['RewardsID'].tolist()
        airline = flights['IATACode'].values[index]
        flightnum = flights['FlightNum'].values[index]

        max_pass = planes.loc[planes['Model'] == flights['Model'].values[index], 'MaxPassengers'].iloc[0]
        passengers_amount = math.ceil((random.randint(80,100) / 100) * max_pass) # need min 80%
        print(index + 1)
        for i in tqdm(range(passengers_amount)):
            # TICKETID
            ticketid = totaltickid[airline][random.randint(0,len(totaltickid[airline])-1)]
            totaltickid[airline].remove(ticketid)

            rewardsid = passengers[random.randint(0,len(passengers)-1)]
            passengers.remove(rewardsid)

            df.loc[len(df.index)] = [ticketid, airline, flightnum, rewardsid, random.uniform(50,250)]


    df.to_csv('6_Tickets.csv', index=False)


# GeneratePassengers(64963)
# GenerateFlights(1327)
GenerateTickets()

print('>>> Done')