import requests
import config
import json



def get_data(next_page_token, zip_):
    '''
        Makes a search for grocery stores in a given zip code. Limited to only 20 results per
        request so next_page_token is used to bring up the next portion of results for a previous query
        
        params:
            next_page_token(str) : token used for getting next portion of results, or 'first_request' if its the first 
            search for this zipcode
            zip_(str) : zipcode that will be searched in 

        returns:
            [0]: the output to be added, e.g.: HEB, 101 E Dallas, 20.23423,23.234234\n ...
            [1]: next_page_token or None if none exists
    '''

    # result to be returned
    output = ''

    # save api key
    api_key = config.api_key
    type_ = 'supermarket'
    query = 'grocery stores in ' + zip_

    url = "https://maps.googleapis.com/maps/api/place/textsearch/json?key=" + api_key + "&query=" + query   
    response = requests.get(url)

    response_json = response.json()

    for key in response_json:
        if key == 'next_page_token':
            next_page_token = key
        if key == 'results':
            # found results, a list of dictionaries.. lets travers
            results = key
            for place in response_json[results]:
                print(place)
                name = place['name']
                address = place['formatted_address']
                latitude = place['geometry']['location']['lat']
                longitude = place['geometry']['location']['lng']
                output += name + ', ' + address + ', ' + str(latitude) + ', ' + str(longitude) + '\n'
                print(output)
    

    return output, next_page_token


output = "Title, Address, Latitude, Longitude\n"

addition, next_page_token = get_data('first_request', '78701')

'''while next_page_token != None:
    addition, next_page_token = get_data(next_page_token)
    # add to our output string
    output += addition
'''
output += addition

output_file = './output.csv'

with open(output_file, 'a') as f:
    f.write(output)

