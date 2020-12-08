
coordinates = [] 
with open('./grocery_stores.csv', 'r') as f:
    lines = f.readlines()
    print (lines)
    
    for line in lines:
        lng = line.split(',')[-1].replace('\n', '')
        lat = line.split(',')[-2]
        new_cood = [lng, lat]
        if not new_cood in coordinates:
            coordinates.append([lng, lat])
            with open('./unique_stores.csv', 'a') as s:
                s.write(line)



