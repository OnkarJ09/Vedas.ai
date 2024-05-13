import pymongo


def query_finder(audio):
    """
    This function finds the query in the database and returns the function name.
    """

    # Establish a connection to MongoDB
    client = pymongo.MongoClient("localhost", 27017)
    db = client["Vedas"]
    collection = db["Queries"]

    # For searching the Query keywords with " "(space) in the Database {strings}
    if " " in audio:
        # Search documents where multi_key is True and match individual query words
        temp = audio.split()
        for document in collection.find({"multi_key": True}):
            q = all(word in document["query"] for word in temp)
            if q:
                return document["function_name"]

    # For searching the Query keywords without " "(space) in the Database {keywords}
    for document in collection.find():
        q = audio in document["query"]
        if q:
            return document["function_name"]

    # Close the connection to MongoDB
    client.close()

