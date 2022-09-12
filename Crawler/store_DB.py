from pymongo import MongoClient



def insert_DB(pageUrl,page_text):
    # establing connection
    try:
        connect = MongoClient()
        
    except:
        print("Could not connect to MongoDB")
    db = connect.darkweb
    collection = db.DW_data_onion_only
    page_text = page_text.replace('\n', ' ')
    page_name = { 
        "Name":pageUrl,
        "Page Text":page_text }
    collection.insert_one(page_name)
    print("Data stored in Database")


