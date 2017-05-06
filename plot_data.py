

import numpy as np
import matplotlib.pyplot as plt
import datetime

depart_airport_string = 'BWI'
arrive_airport_string = 'BUF'
depart_date_string = '6-30'

data_name = '{}_to_{}_{}.csv'.format(depart_airport_string,
                                     arrive_airport_string,
                                     depart_date_string)
flight_numbers = []
date_checkeds = []
fare_types = []
prices = []
with open(data_name,'rt') as f:
    for line in f:
        #print(line)
        data = line.split(',')
        # captial b for full month, small be for abbreviated month
        date_checked = datetime.datetime.strptime(data[0], '%a %b %d %H:%M:%S %Y')
        flight_number = data[1]
        fare_type = data[2]
        price = data[3]

        flight_numbers.append(flight_number)
        date_checkeds.append(date_checked)
        fare_types.append(fare_type)
        prices.append(price)
        
unique_flight_numbers = set( flight_numbers )
unique_fare_types = set( fare_types )
legend = []
for n in unique_flight_numbers:
    for t in unique_fare_types:
        toplot = [ [a,float(d[1:])] for a,b,c,d, in zip(date_checkeds,flight_numbers,fare_types,prices) if b == n and c == t and d != 'Sold Out']
        if toplot:
            toplota = np.array(toplot)
            print(toplota)
            plt.plot_date(toplota[:,0],toplota[:,1]+np.random.rand()*10,linestyle='solid')
            legend.append('{} {}'.format(n,t))
plt.legend(legend)            
plt.show()
