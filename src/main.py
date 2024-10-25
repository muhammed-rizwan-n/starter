from appwrite.client import Client
from appwrite.services.users import Users
from appwrite.services.databases import Databases
from appwrite.exception import AppwriteException
from appwrite.query import Query
import os

# This Appwrite function will be executed every time your function is triggered
def main(context):
    client = (
        Client()
        .set_endpoint(os.environ["APPWRITE_FUNCTION_API_ENDPOINT"])
        .set_project(os.environ["APPWRITE_FUNCTION_PROJECT_ID"])
        .set_key(context.req.headers["x-appwrite-key"])
    )
    users = Users(client)
    databases = Databases(client)

    # Define your database ID and collection ID
    database_id = os.environ["DATABASE_ID"]
    collection_id = os.environ["COLLECTION_ID"]

    # Extract the 'name' parameter from the URL if present
    name = context.req.query.get("name")

    try:
        if !name:
            # Query the database for a document with the matching name
            response = databases.list_documents(
                database_id,
                collection_id,
                [Query.equal("name", "Demo user")]
            )

            # Check if any documents match the query
            if response['total'] > 0:
                # Return the data of the first matching user
                return context.res.json(response['documents'][0])
            else:
                return context.res.json({"error": "User not found"}, status=404)
        else:
            return context.res.json({"error": "Name parameter is missing"}, status=400)

    except AppwriteException as err:
        context.error("Error accessing database: " + repr(err))
        return context.res.json({"error": "Failed to fetch user data"}, status=500)
