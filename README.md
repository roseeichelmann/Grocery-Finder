Grocery Finder 
================


### The Problem 
This project aims to address the problem that is present when trying to find:
1. name
2. address
3. coordinates 
of grocery stores within a zip code 

### Approach 
1. Get familiar with the Scrapy Python Module and setup project using https://docs.scrapy.org/en/latest/intro/tutorial.html
2. Inspect Element and figure out what part of https://www.zip-codes.com/city/tx-austin.asp stores the zip codes in austin and how we can get our bot to recognize 
3. Use Scrapy to scrape all the zipcodes in austin 
4. Inspect Yelp URL to figure out how to forge URLs that give us a search for 'grocery store' in each zip code
5. Go through each zip code and visit url for a grocery store search in that area.
6. Inspect Yelp results page to figure out which part of page contains address that we would like to scrape
7. Use Scrapy to scrape all the addresses and names of the results
8. Dont forget to take into consideration pages, if there are multiple pages we need to flip through them until we are at last one. 
9. We also dont want duplicates in the collection so lets store our results in a Set or implement a way to check for duplicates
10. Learn about geopy, heres a demo that will be useful, as the next thing we need to do is get coordinates given address and zip code 
    
    >>> from geopy.geocoders import Nominatim
    >>> geolocator = Nominatim()
    >>> location = geolocator.geocode("175 5th Avenue NYC")
    >>> print(location.address)
    Flatiron Building, 175, 5th Avenue, Flatiron, New York, NYC, New York, ...
    >>> print((location.latitude, location.longitude))
    (40.7410861, -73.9896297241625)
    
11. Finally, write the name, address, and coordinates for each grocery store out to a file so we can use another time


### Bonus points! 
- Allow the Grocery-finder to be scalable. This would mean we would use the `input() `function to take user input and ask for a city, and given that city we can find all the grocery stores by just finding a zipcode page for it and continuing with the rest of the steps.
    
