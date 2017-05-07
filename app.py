from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait # for waiting!
from selenium.webdriver.common.by import By # pick by ID or something
from selenium.webdriver.support import expected_conditions as EC

import time
timestr = time.asctime()

depart_airport_string = 'BWI'
arrive_airport_string = 'BUF'
# format for this? looking at browser it shows newDepartDate=7-1
depart_date_string = '6-30'
passengers_string = '2'

service_args=[]
# this may help with my current_url being  u'about:blank'
#service_args = ['--ignore-ssl-errors=true','--ssl-protocol=tlsv1','--proxy-type=None','--load-images=false']

# a minimal subset that works is the following
browser = webdriver.PhantomJS(service_args = ['--ssl-protocol=any'])
browser.get('https://www.southwest.com/')
#print(browser.current_url)
# okay this works!!!!


with open('tmp.png','wb') as f:
    f.write( browser.get_screenshot_as_png() )
print('screenshot written')

depart_airport = browser.find_element_by_id("air-city-departure")
depart_airport.send_keys(depart_airport_string)

arrive_airport = browser.find_element_by_id("air-city-arrival")
arrive_airport.send_keys(arrive_airport_string)

depart_date = browser.find_element_by_id("air-date-departure")
depart_date.clear()
depart_date.send_keys(depart_date_string)

# passengers, first remove read only
passengers = browser.find_element_by_id("air-pax-count-adults")
browser.execute_script("arguments[0].removeAttribute('readonly', 0);", passengers)
passengers.click()
passengers.clear()
passengers.send_keys(passengers_string)

# daniel adds this
oneway = browser.find_element_by_id('trip-type-one-way')
oneway.click()


# now we search!
search = browser.find_element_by_id("jb-booking-form-submit-button")
search.click()

outbound_array = []

# webdriver might be too fast
#print('about to wait')
wait = WebDriverWait(browser, 120) # 120 is a timeout
wait.until(EC.element_to_be_clickable((By.ID, "faresOutbound")))
#print('waited')

outbound_fares = browser.find_element_by_id("faresOutbound")
outbound_prices = outbound_fares.find_elements_by_class_name("product_price")

for price in outbound_prices:
    realprice = price.text.replace("$","")
    outbound_array.append(int(realprice))

# daniel will add these
time = outbound_fares.find_elements_by_class_name("time")
indicator = outbound_fares.find_elements_by_class_name("indicator")

# well the weird thing is that I'm not getting the same values when I just use a webbrowser
#for data in zip(outbound_prices,time,indicator):
#    print('time {}{}: {}'.format(data[1].text,data[2].text,data[0].text))

#out = browser.find_element_by_id("Out1A")
#print(out.get_attribute('title'))
#print(out.get)

# what about sold out?
price_column = browser.find_elements_by_class_name("price_column")
#print([p.text for p in price_column])

# something a bit more structured
data_name = '{}_to_{}_{}.csv'.format(depart_airport_string,
                                     arrive_airport_string,
                                     depart_date_string)
with open(data_name,'at') as f:
    count = 0
    for i in range(1,10):
        for abc in 'ABC':


            elements = browser.find_elements_by_id('Out{}{}'.format(i,abc))
            # if its empty, the price doesn't exist
            for e in elements:

                print(e.get_attribute('title') + '( fare: {} {})'.format(abc,price_column[count].text))
                #print(e.get_attribute('value')) # more detail in here but not easy to read



                # current time
                f.write(timestr)
                f.write(',')

                # flight number
                parts = e.get_attribute('title').split()
                f.write(parts[2])
                f.write(',')
                
                # fare type
                f.write(abc)
                f.write(',')

                f.write(price_column[count].text)
                f.write(',')

                f.write('\n')

                count += 1


import plot_data
