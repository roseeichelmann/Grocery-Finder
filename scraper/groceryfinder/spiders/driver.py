import scrapy
from geopy.geocoders import Nominatim

class GroceryFinder(scrapy.Spider):
    name = "driver"

    def start_requests(self):
        self.coordinates = []
        self.geolocator = Nominatim(user_agent="UT Austin geographic info science")
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
        base_url = 'https://www.grocery-stores.org/grocery-stores-in-'
        urls = []
        for zip_code in zipcodes:
            url = base_url + str(zip_code) + '/'
            urls.append(url)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.grocery_parse)

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

    def Log(self, msg):
        self.log("\n\n-----------------------")
        self.log(msg)
        self.log("--------------------------\n")