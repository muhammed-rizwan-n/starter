from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.exception import AppwriteException
from appwrite.query import Query
import os

def main(context):
    # Initialize the Appwrite client
    client = (
        Client()
        .set_endpoint(os.environ["APPWRITE_FUNCTION_API_ENDPOINT"])
        .set_project(os.environ["APPWRITE_FUNCTION_PROJECT_ID"])
        .set_key(context.req.headers["x-appwrite-key"])
    )

    # Initialize the Appwrite Databases service
    databases = Databases(client)

    # Define database and collection IDs
    database_id = os.environ["DATABASE_ID"]
    collection_id = os.environ["COLLECTION_ID"]

    # Extract 'name' parameter from the query if present
    name = context.req.query.get("name")
    if not name:
        return context.res.json({"error": "Missing 'name' parameter"}, status=400)

    # Query the database
    try:
        response = databases.list_documents(
            database_id=database_id,
            collection_id=collection_id,
            queries=[Query.equal("name", "De)]
        )

        # Check if any documents were found
        if response['total'] > 0:
            # Return the first matched document
            return context.res.json(response['documents'][0])
        else:
            return context.res.json({"message": "User not found"}, status=404)

    except AppwriteException as e:
        context.error("Database query failed: " + str(e))
        return context.res.json({"error": "Database query failed"}, status=500)
