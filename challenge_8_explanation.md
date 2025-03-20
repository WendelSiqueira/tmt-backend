### Intructions to create a new Inventory Item: ###

1 - Check if the endpoint you need already exists and only needs adaptations

2 - If the endpoint does not exist, look at the documentation or the code for similar examples to help you understand how we are organizing these things in the project

3 - If it does not exist, create the endpoint and logic in the correct place (in this case, the app where the inventory model is or following some other standard determined in the project)

4 - Remember that the endpoint you need to create will receive the information, so it needs to be a POST method

5 - prepare a payload for testing with the data you need to receive, here is an example:

```json
{
    "year": 2000, 
    "actors": ["Vin Diesel"], 
    "imdb_rating": 10, 
    "rotten_tomatoes_rating": 10, 
    "film_locations": "Brazil"
}

```

6 - use a tool to send this data to your new endpoint (curl, postman, python-requests, etc)

7 - validate if the data you are receiving is correct, and being saved correctly

8 - send a similar payload with incorrect data to validate if everything is working as expected

9 - Remember to write the tests for this new endpoint

Any problem, don't hesitate to ask for help, good luck
