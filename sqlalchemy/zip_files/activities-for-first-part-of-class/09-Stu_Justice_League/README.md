# Justice League API

* In this activity, you will write a route that returns the json for a Python Dictionary containing the superhero name and real name for each member of the DC Comics Justice League.

## Instructions

* Create a file called `app.py` for your Flask app.

* Define a Python dictionary containing the superhero name and real name for each member of the DC Comics Justice Leage (Superman, Batman, Wonder Woman,  Green Lantern, Flash, Aquaman, and Cyborg).

  * You can gather that information here: [Justice League](https://en.wikipedia.org/wiki/Justice_League)

  * Only gather the information for the 7 characters listed above.

* Create a **GET** route called `/api/v1.0/heroes`.

  * Inside of your GET route, create a function called `justice_league` that will use `jsonify` to convert the dictionary of Justice League members to a json object and return that data as a request.

* Define a root route `/` that will return the usage statement for your API.

BONUS:

* Define a route that will take in a character's name (ex: Superman) and return their row in the list 

{
real_name: "Clark Kent/Kal-El",
superhero: "Superman"
}

- - -

### Copyright

Trilogy Education Services © 2017. All Rights Reserved.
