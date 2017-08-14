# Inventrom_DetailFromFedEx_Deblina
To scrape the FEDEX website to obtain the tracking details
of the given shipment tracking details. The output is in JSON format.

On taking the tracking number as input from the user, it for possible errors such as :
 1. If the number is not an integer
 2. If the number is an integer but it's value is less than 0
 3. If the number is an integer but it's length is not 12(which is the valid length of the tracking number)

If such an error is found, necessary error messages are displayed on the console

If no such error is encountered, the required details are extracted using the tracking number from the FEDEX website.
