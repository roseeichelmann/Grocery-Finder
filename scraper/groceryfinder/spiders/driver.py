import scrapy
from geopy.geocoders import Nominatim

class GroceryFinder(scrapy.Spider):
    name = "driver"

    def start_requests(self):
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
         paragraphs = response.xpath('//p').getall()
         for paragraph in paragraphs:
             if "condensed-listing" in paragraph:
                paragraph_as_list = paragraph.split('\n')
                title = paragraph_as_list[2]
                address = paragraph.split('address">\n')[1].split('<')[0].strip()
                # now need to parse title
                title = title.split('title="')[1].split('(')[0].strip()
                # now rose has to figure out the corordinates
                self.Log(address)
                self.Log(title)
                location = self.geolocator.geocode(address)
                self.Log(location)

                latitude = str(location.latitude)
                longitude = str(location.longitude)
                with open(self.file_location, "a") as f:
                    f.write(str(title + ',' + address + ',' + latitude + ',' + longitude + '\n'))

    def Log(self, msg):
        self.log("\n\n-----------------------")
        self.log(msg)
        self.log("\n--------------------------\n\n")