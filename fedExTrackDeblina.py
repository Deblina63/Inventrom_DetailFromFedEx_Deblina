import requests
import json
import calendar as cal
from datetime import date as dt


# Function to convert a 12 hr format time to 24 hr format time
def convertTimeTo24hr(t):
    """ Function which takes a 12 hour format time value by the parameter t, converts into a 24 hour format
    time value and finally returns the new updated time value. """

    # Splitting up the time to get the integer values of hour and minute
    # and storing then in the form of a list of strings
    timeSplit = t.split(':')


    # If the time is in PM and hour is less than 12 then we need to
    # increase the value of hour by 12 hours
    if (timeSplit[1][2:] == 'PM' or timeSplit[1][2:] == 'pm') and timeSplit[0] != '12':
        timeSplit[0] = str(12 + int(timeSplit[0]))

    # If the time is in the range of 12:00AM to 12:59AM, we need to make the
    # value of hour as 00
    elif int(timeSplit[0]) == 12 and (timeSplit[1][2:] == 'AM' or timeSplit[1][2:] == 'am'):
        timeSplit[0] = '00'

    timeSplit[1] = timeSplit[1][:2]

    # Joining the values of updated hour and minute to get the updated time
    getTime= ":".join(str(e) for e in timeSplit)
    #print(getTime)

    return getTime


# Function to concatenate day or month value with 0 in the beginning if they are single digit values
def updateDate(d, m, y):
    """ Function to concatenate day or month value with a 0 in the beginning if they are single digit values and
    return the updated date."""

    # checking for the value of day
    if int(d) < 10:
        d = '0' + d

    # checking for the value of month
    if int(m) < 10:
        m = '0' + m

    # returning the updated date
    return d+'/'+m+'/'+y


# Function to obtain the name of the day which is represented by the given date
def getDayName(day, month, year):
    """ Function to take the day, month and year values as parameters, obtain the name of the day represented by that
    date using the calender instance in python and finally retuen the name of the date so obtained."""

    dd = int(day)
    mm = int(month)
    yy = int(year)
    tempDate = dt(yy, mm, dd)

    # Obtaining the name of the day using the calender package
    name_of_day = cal.day_name[tempDate.weekday()]

    # Returning only the first three characters of the name of the day
    return name_of_day[:3]


""""Taking tracking number as input. This tracking number is used to get the details of the package from the FedEx 
website. The details are stored in the form of JSON file, from where the required fields are extracted and displayed"""
tracking_number = input("Tracking number:")
try:
    int(tracking_number)
    # If the tracking number is not an integer, the program control will go on to the exception section
    if int(tracking_number) < 0:
        # If tacking number is a negative value, then the process cannot be continued
        print("Tracking number cannot be negative.")
    elif len(str(tracking_number)) == 12 :
        # If the length of the tracking number is 12 then the details are extracted

        # fetching delivery details and storing it in json format
        data = requests.post('https://www.fedex.com/trackingCal/track', data={
            'data': json.dumps({
                'TrackPackagesRequest': {
                    'appType': 'wtrk',
                    'uniqueKey': '',
                    'processingParameters': {
                        'anonymousTransaction': True,
                        'clientId': 'WTRK',
                        'returnDetailedErrors': True,
                        'returnLocalizedDateTime': False
                    },
                    'trackingInfoList': [{
                        'trackNumberInfo': {
                            'trackingNumber': tracking_number,
                            'trackingQualifier': '',
                            'trackingCarrier': ''
                        }
                    }]
                }
            }),
            'action': 'trackpackages',
            'locale': 'en_US',
            'format': 'json',
            'version': 99
        }).json()

        # Obtaining the details of the package being tracked
        packageDetail = data["TrackPackagesResponse"]["packageList"][0]
        # Storing the status of delivery and scheduled date of delivery from the list of all details
        mainData = packageDetail["statusWithDetails"]
        # Fetching the shipping date of the package being tracked
        shipDate = packageDetail["displayTenderedDt"].split('/')

        # Obtaining the name od day from the fetched ship date
        shipDay = getDayName(shipDate[1], shipDate[0], shipDate[2])

        # If the value of date, month or year is less than 10 then it
        # should be of the form 01/02/03/04/... accordingly and
        # concatenating day,month,year to get desired shipping date
        desiredShipDate = updateDate(shipDate[1], shipDate[0], shipDate[2])

        # fetching the delivery status and date from mainData
        deliveryData = mainData.split(':')
        status = deliveryData[0]
        deliveryDate = deliveryData[1][1:10].split('/')

        # obtaining name of day of delivery from the delivery date
        deliveryDay = getDayName(deliveryDate[1], deliveryDate[0], deliveryDate[2])

        # If the value of date, month or year is less than 10 then it
        # should be of the form 01/02/03/04/... accordingly
        deliveryDate = updateDate(deliveryDate[1], deliveryDate[0], deliveryDate[2])

        time = deliveryData[1][-1] + ':' + deliveryData[2][0:2]+""+deliveryData[2][3:5]
        #print(mainDataSplit[2][3:5])
        #print(time)

        # converting the 12 hr format time into 24 hr format time
        time = convertTimeTo24hr(time)


        # Dictionary for the purpose of storing the desired results
        result_dict={
            "Tracking number": tracking_number,
            "Ship date": shipDay + " " + desiredShipDate,
            "Status": status,
            "Scheduled Delivery": deliveryDay + " " + deliveryDate + " " + time
        }


        # Displaying the details from the dictionary
        print("{")
        for key, value in result_dict.items():
            print(key, " : ", value)
        print("}")

    elif len(str(tracking_number)) != 12:
        # If the length of tracking number is not equal to 12 then the process cannot be continued, hence
        # an error message is displayed on the console
        print("Invalid length of tracking number! Valid tracking number has length=12.")

except ValueError:
    # If the tracking number is not an integer value then an error message is displayed
    print("Tracking number has to be an integer")
