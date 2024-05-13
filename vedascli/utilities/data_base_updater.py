from vedascli.data.queries import query
import pymongo


def upload_query():
    """
    This function help's Uploading queries to DataBase or MongoDB
    """

    # Establish connection with MongoDB
    client = pymongo.MongoClient("localhost", 27017)
    db = client["Vedas"]
    collection = db["Queries"]

    # Uploading data into DB
    for queries, func_name in query.items():
        if isinstance(queries, tuple) and len(queries) > 1:
            # Create a document for additional field for keys in multiple elements
            Queries = {
                "query": queries,
                "function_name": func_name,
                "multi_key": True
            }
        else:
            # Create a document for additional field for keys in single element
            Queries = {
                "query": queries,
                "function_name": func_name,
                "multi_key": False
            }
        collection.insert_one(Queries)
    print("Query uploaded successfully")
