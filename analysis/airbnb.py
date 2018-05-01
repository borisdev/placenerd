import pandas as pd
import nltk
store = pd.HDFStore('store.h5')
file_object = open("../data/listings.csv")
#fo = pd.read_csv(f)
VIBE_FIELDS = [
    "name",
    "summary",
    "description",
    "neighborhood_overview",
    "notes",
    "transit",
    "house_rules",
    "host_about",
    "neighbourhood_cleansed",
    "city",
    "state",
    "zipcode",
    "market",
    "smart_location",
    "country_code"
]
COST_FIELDS = [
    "zipcode",
    "city",
    "neighbourhood_cleansed",
    "market",
    "smart_location",
    "room_type",  # =Private room
    "bedrooms",  # =1
    "beds",  # =1
    "price"
]

df = pd.read_csv(file_object, usecols=lambda x: x in VIBE_FIELDS)
sentences = []
for document in df['neighborhood_overview'][1:100]:
    try:
        sentences.extend(nltk.sent_tokenize(document))
    except:
        pass
file = open('sentence2label.csv', "w")
sentence2label = []
for sentence in sentences:
    print sentence
    try:
        labels = raw_input("Enter labels. ex. green,diverse  :")
    except ValueError:
        labels = None
    file.write(sentence + "," + labels + "\n") 
#sentence2label = [(sentence,labels)]
#print sentence2labels
    

#store['airbnb_vibes_raw'] = df
#TODO: Aggregate by zipcodes
