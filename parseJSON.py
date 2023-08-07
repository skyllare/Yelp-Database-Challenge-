import json


def cleanStr4SQL(s):
    return s.replace("'","''").replace("\n"," ")

def getAttributes(attributes):
    L = []
    for (attribute, value) in list(attributes.items()):
        if isinstance(value, dict):
            L += getAttributes(value)
        else:
            L.append((attribute,value))
    return L

def parseBusinessData():
    print("Parsing businesses...")
    #read the JSON file
    with open(r'C:\Users\Skyllar\OneDrive\Documents\Summer 2023\CptS 451\Project Code\Yelp-CptS451\yelp_business.JSON','r') as f:
        outfile =  open('.//yelp_business.txt', 'w')
        line = f.readline()
        count_line = 0
        #read each JSON abject and extract data
        while line:
            data = json.loads(line)
            business = data['business_id'] #business id
            business_insert_str = "INSERT INTO Business (business_id, name,address,city,state,postal_code,latitude,longitude,stars,review_count,is_open)"
            business_str = "'" + business + "'," + \
                            "'" + cleanStr4SQL(data['name']) + "'," + \
                            "'" + cleanStr4SQL(data['address']) + "'," + \
                            "'" + cleanStr4SQL(data['city']) + "'," +  \
                            "'" + data['state'] + "'," + \
                            "'" + data['postal_code'] + "'," +  \
                            str(data['latitude']) + "," +  \
                            str(data['longitude']) + "," + \
                            str(data['stars']) + "," + \
                            str(data['review_count']) + "," + \
                            str(data['is_open'])
            outfile.write(business_insert_str + '\n' + "VALUES" + "(" + business_str + ")" + ";" + '\n')

            if data['categories']:
                category_ins_str = "INSERT INTO Category (business_id, type)"
                outfile.write(category_ins_str + '\n' + "VALUES")
                num_categories = len(data['categories'])
                for i, category in enumerate(data['categories']):
                    category = category.replace("'", "''")  # Replace ' with ''
                    category_str = "('" + business + "','" + category + "')"
                    if i < num_categories - 1:
                        category_str += ","
                    else:
                        category_str += ";"
                    outfile.write(category_str + '\n')

            if data['hours']:
                hours_ins_str = "INSERT INTO Hours (business_id, day, open, close)"
                outfile.write(hours_ins_str + '\n' + "VALUES")
                for day, hours in data['hours'].items():
                    hours_str = "('" + business + "','" + str(day) + "','" + str(hours.split('-')[0]) + "','" + str(
                        hours.split('-')[1]) + "')"
                    if day != list(data['hours'].keys())[-1]:
                        hours_str += ","
                    else:
                        hours_str += ";"
                    outfile.write(hours_str + '\n')

            if data['attributes']:
                attributes_ins_str = "INSERT INTO Attributes (business_id, attribute, value)"
                outfile.write(attributes_ins_str + '\n' + "VALUES")
                attribute_list = list(getAttributes(data['attributes']))
                num_attributes = len(attribute_list)
                for i, (attr, value) in enumerate(attribute_list):
                    attr_str = "('" + business + "','" + str(attr) + "','" + str(value) + "')"
                    outfile.write(attr_str)
                    if i < num_attributes - 1:
                        outfile.write(",\n")
                    else:
                        outfile.write(";\n")

            ##

            line = f.readline()
            count_line +=1
    print(count_line)
    outfile.close()
    f.close()


def parseReviewData():
    print("Parsing reviews...")
    #reading the JSON file
    with open('Yelp-CptS451\yelp_review.JSON','r') as f:
        outfile =  open('.//yelp_review.txt', 'w')
        line = f.readline()
        count_line = 0
        failed_inserts = 0
        while line:
            user_insert_str = "INSERT INTO Review (review_id, user_id, business_id, stars, date, text, useful, funny, cool) VALUES"
            data = json.loads(line)
            review_str = "('" + data['review_id'] + "'," +  \
                         "'" + data['user_id'] + "'," + \
                         "'" + data['business_id'] + "'," + \
                         str(data['stars']) + "," + \
                         "'" + data['date'] + "'," + \
                         "'" + cleanStr4SQL(data['text']) + "'," +  \
                         str(data['useful']) + "," +  \
                         str(data['funny']) + "," + \
                         str(data['cool']) + ");"
            outfile.write(user_insert_str + '\n' + review_str + '\n')
            line = f.readline()
            count_line +=1

    print(count_line)
    outfile.close()
    f.close()

def parseUserData():
    print("Parsing users...")
    #reading the JSON file
    with open('Yelp-CptS451\yelp_user.JSON','r') as f:
        outfile =  open('.//yelp_user.txt', 'w')
        line = f.readline()
        count_line = 0
        while line:
            user_insert_str = "INSERT INTO Users (user_id,name,yelping_since,review_count,fans,average_stars,funny,useful,cool)"
            data = json.loads(line)
            user_id = data['user_id']
            user_str = \
                      "'" + user_id + "'," + \
                      "'" + cleanStr4SQL(data["name"]) + "'," + \
                      "'" + cleanStr4SQL(data["yelping_since"]) + "'," + \
                      str(data["review_count"]) + "," + \
                      str(data["fans"]) + "," + \
                      str(data["average_stars"]) + "," + \
                      str(data["funny"]) + "," + \
                      str(data["useful"]) + "," + \
                      str(data["cool"])
            outfile.write(user_insert_str + '\n' + "VALUES" + "(" + user_str + ")" + ";" + '\n')

            if data['friends']:
                friend_ins_str = "INSERT INTO Friends (user_id, friend)"
                outfile.write(friend_ins_str + '\n' + "VALUES")
                for i, friend in enumerate(data['friends']):
                    friend_str = "('" + user_id + "'" + "," + "'" + friend + "')"
                    if i < len(data['friends']) - 1:
                        friend_str += ","
                    else:
                        friend_str += ";"
                    friend_str += "\n"
                    outfile.write(friend_str)

            line = f.readline()
            count_line +=1

    print(count_line)
    outfile.close()
    f.close()

#checkin_insert_str = "INSERT INTO Checkin (business_id, day, hour, num_checkin)"
def parseCheckinData():
    print("Parsing checkins...")
    #reading the JSON file
    len_checkin = 0
    with open('Yelp-CptS451\yelp_checkin.JSON','r') as f:  # Assumes that the data files are available in the current directory. If not, you should set the path for the yelp data files.
        outfile = open('yelp_checkin.txt', 'w')
        line = f.readline()
        count_line = 0
        #read each JSON abject and extract data
        checkin_insert_str = "INSERT INTO Checkin (business_id, day, hour, num_checkin)"
        while line:
            data = json.loads(line)
            business_id = data['business_id']
            for (dayofweek,time) in data['time'].items():
                for (hour,count) in time.items():
                    outfile.write(checkin_insert_str + "VALUES" + '\n')
                    checkin_str = "('" + business_id + "',"  \
                                  "'" + dayofweek + "'," + \
                                  "'" + hour + "'," + \
                                  str(count) + ');'
                    outfile.write(checkin_str + "\n")
            line = f.readline()
            count_line += 1
        print(count_line)
    outfile.close()
    f.close()


#parseBusinessData()
#parseUserData()
#parseCheckinData()
parseReviewData()

