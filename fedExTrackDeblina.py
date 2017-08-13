import requests
import json
import calendar as cal
from datetime import date as dt


# Function to convert a 12 hr format time to 24 hr format time
def convertTimeTo24hr(t):

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


# Function to obtain the name of the day which is represented by the given date
def getDay(date, month, year):
    dd = int(date)
    mm = int(month)
    yy = int(year)
    tempDate = dt(yy, mm, dd)

    # Obtaining the name of the day using the calender package
    name_of_day = cal.day_name[tempDate.weekday()]

    # Returning only the first three characters of the name of the day
    return name_of_day[:3]


#tracking_number = '744668909687'

tracking_number = input("Tracking number:")
try:
    int(tracking_number)
    if int(tracking_number)<0 :
        print("Tracking number cannot be negative.")
    elif len(str(tracking_number)) == 12 :
        #print("it's an integer number")

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
        shipDay = getDay(shipDate[1], shipDate[0], shipDate[2])

        # If the value of date, month or year is less than 10 then it
        # should be of the form 01/02/03/04/... accordingly
        if int(shipDate[0]) < 10:
            shipDate[0] = '0' + shipDate[0]
        if int(shipDate[1]) < 10:
            shipDate[1] = '0' + shipDate[1]
        if int(shipDate[2]) < 10:
            shipDate[2] = '0' + shipDate[2]

        # concatenating day,month,year to get desired shipping date
        desiredShipDate = shipDate[1] + '/' + shipDate[0] + '/' + shipDate[2]

        # fetching the delivery status and date from mainData
        deliveryData = mainData.split(':')
        status = deliveryData[0]
        deliveryDate = deliveryData[1][1:10].split('/')

        # obtaining name of day of delivery from the delivery date
        deliveryDay = getDay(deliveryDate[1], deliveryDate[0], deliveryDate[2])

        # If the value of date, month or year is less than 10 then it
        # should be of the form 01/02/03/04/... accordingly
        if int(deliveryDate[0]) < 10:
            deliveryDate[0] = '0' + deliveryDate[0]
        if int(deliveryDate[1]) < 10:
            deliveryDate[1] = '0' + deliveryDate[1]
        if int(deliveryDate[2]) < 10:
            deliveryDate[2] = '0' + deliveryDate[2]
        deliveryDate = deliveryDate[1] + '/' + deliveryDate[0] + '/' + deliveryDate[2]

        time = deliveryData[1][-1] + ':' + deliveryData[2][0:2]+""+deliveryData[2][3:5]
        #print(mainDataSplit[2][3:5])
        #print(time)

        # converting the 12 hr format time into 24 hr format time
        time = convertTimeTo24hr(time)

        output = "{\nTracking no: " + tracking_number + ",\nShip date: " + shipDay + " " + desiredShipDate + ",\nStatus: " + status + ',\nScheduled Delivery: ' + deliveryDay + " " + deliveryDate + " " + time + "\n}"

        print(output)

    elif len(str(tracking_number)) != 12:
        print("Invalid length of tracking number! Valid tracking number has length=12.")

except ValueError:
    print("Tracking number has to be an integer")
