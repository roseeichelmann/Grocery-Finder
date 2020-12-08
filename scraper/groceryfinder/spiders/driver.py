import scrapy
import config
import requests

class GroceryFinder(scrapy.Spider):
    name = "driver"

    def start_requests(self):
        self.coordinates = []
        self.file_location = '../grocery_stores.csv'
        with open(self.file_location, "w") as f:
            f.write("Title, Address, Latitude, Longitude\n")

        urls = [
            'https://www.zip-codes.com/county/tx-travis.asp',
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        paragraphs = response.xpath('//td').getall()

        # need to find zip codes now!
        zipcodes = []
        for paragraph in paragraphs:
            if "ZIP Code" in paragraph:
                if "label" in paragraph:
                    if "title" in paragraph:
                        if len(paragraph) < 165:
                            zip_code = paragraph[37:42]
                            zipcodes.append(zip_code)
                      
        # NOW WE HAVE ZIPCODES!! HOORAY!!!
        for zip_code in zipcodes:
            # make first request
            addition, next_page_token = self.get_data('first_request', zip_code)
            with open(self.file_location, 'a') as f:
                f.write(addition)

            # keep making requests til we get all in this zip code 
            while next_page_token != None:
                addition, next_page_token = self.get_data(next_page_token, zip_code)
                with open(self.file_location, 'a') as f:
                    f.write(addition)


    '''
    def grocery_parse(self, response):
        zip_ = response.url.split('/')[-2].split('-')[-1]
        paragraphs = response.xpath('//p').getall()
        for paragraph in paragraphs:
            if "condensed-listing" in paragraph:
                paragraph_as_list = paragraph.split('\n')
                title = paragraph_as_list[2]
                address = paragraph.split('address">\n')[1].split('<')[0].strip()
                # now need to parse title
                title = title.split('title="')[1].split('(')[0].strip()
                title = title.replace("&amp;","and")
                title = title.replace("??", "i") ##FIXME: only needed for this specific dataset
                # now rose has to figure out the corordinates
                self.Log(str(title) + ","+ str(address) + " " + str(zip_))
                latitude, longitude = self.get_lat_and_long(address, zip_)
                for element in self.coordinates:
                    if latitude == element[0] and longitude == element[1]:
                        return
                self.coordinates.append((latitude,longitude)) 
                with open(self.file_location, "a") as f:
                    f.write(str(title + ',' + address + ',' + latitude + ',' + longitude + '\n'))
    
    def get_lat_and_long(self, address, zip_):
        # FIXME: this is hardcoded error avoidance, not suitable for general algorithm
        if '5300 S Mopac Expy' in address:
            latitude = '30.234200'
            longitude = "-97.828430"
        elif '2101 W Ben White Blvd' in address:
            latitude = '30.229760'
            longitude = '-97.791090'
        elif '825 E Rundberg' in address:
            latitude = '30.357360'
            longitude = '-97.686780'
        elif '500 W 5th St' in address:
            latitude = '30.268670'
            longitude = '-97.747840'
        elif '11940 Manchaca' in address:
            latitude = '30.1407692'
            longitude = '-97.833055'
        elif '2501 W William Cannon' in address:
            latitude = '30.2015532'
            longitude = '-97.806476'
        # TODO: continue this 
        else:
            location = self.geolocator.geocode(str(address) + ' ' + str(zip_))
            latitude = str(location.latitude)
            longitude = str(location.longitude)
        return latitude, longitude
    '''

    def get_data(self, next_page_token, zip_):
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

        if next_page_token == None or next_page_token == 'first_request': 

            query = 'grocery stores in ' + zip_
            url = "https://maps.googleapis.com/maps/api/place/textsearch/json?key=" + api_key + "&query=" + query   

        else:
            url = "https://maps.googleapis.com/maps/api/place/textsearch/json?key=" + api_key + "&pagetoken=" + next_page_token

        response = requests.get(url)
        response_json = response.json()

        next_page_token = None

        for key in response_json:
            if key == 'next_page_token':
                next_page_token = response_json[key]
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

        return output, next_page_token



    def Log(self, msg):
        self.log("\n\n-----------------------")
        self.log(msg)
        self.log("--------------------------\n")
