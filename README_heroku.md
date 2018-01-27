## FLASK-HEROKU

> This repository is short guide for deploying a flask-postgres application to Heroku. The files and dependencies are the minimum requirements. Additional dependencies can be added to `requirements.txt`.


## Install Python:
- if not done yet, make sure to have [Python](https://www.python.org/downloads/) installed.
- versions 2.7 and 3.6 are both [supported](https://devcenter.heroku.com/articles/python-runtimes).

## File structure setup:
- `clone` && `cd` into the repo you created from GitHub.
- ***note: replace `username` and `repo-name` below with yours.***
```
$ git clone git@github.com:username/repo-name.git`
$ cd repo-name/
```
- make the following files inside `repo-name`:

| file name        |  description                        |  
|------------------|-------------------------------------|
| app.py           | contains all your Flask source code |
| [Procfile](https://devcenter.heroku.com/articles/procfile) | file required by Heroku to run your [Dyno](https://www.heroku.com/dynos) containers |
| README.md        | describes your application          |
| requirements.txt | list of all dependencies for your app  |
| .gitignore       | has files you do not want to track |

- hosting steps will be covered in a later section called `Deploying your application`.

## Heroku instructions

> Sign up for a [free Heroku account](https://signup.heroku.com/dc). The account is free until you have exceeded the app limit. For more info, refer to the [documentation](https://devcenter.heroku.com/categories/python).

- download the Heroku [`Command Line Interface`](https://devcenter.heroku.com/articles/heroku-cli).
- when done, open a terminal and sign in with credentials:
```
$ heroku login
Enter your Heroku credentials:
Email: my.email@gmail.com
Password: ***********
```
- to see a list of Heroku CLI commands, type in:
```
$ heroku help
Usage: heroku COMMAND

Help topics, type heroku help TOPIC for more details:

 access          manage user access to apps
 addons          tools and services for developing, extending, and operating your app
 apps            manage apps
 auth            heroku authentication
 authorizations  OAuth authorizations
 ...
```
> **A quick note before starting. Any time you see a series of "X"s, it's just a replacement for an encrypted or unique number.**
- create a new heroku app:
```
$ heroku create
Creating app... done, ⬢ unique-name-XXXXX
https://unique-name-XXXXX.herokuapp.com/ | https://git.heroku.com/unique-name-XXXXX.git
```
- Heroku auto-generates a unique name for your application, although it can be renamed with the `rename` command: 
```
$ heroku rename repo-name
Renaming unique-name-XXXXX to repo-name... !
 ▸    Name is already taken
 ```
- the name may be already taken, so rename until unique:
```
$ heroku rename repo-name2
Renaming unique-name-XXXXX to repo-name2... done
https://repo-name2.herokuapp.com/ | https://git.heroku.com/repo-name2.git
Git remote heroku updated
 ▸    Don't forget to update git remotes for all other local checkouts of the app.
 ```
 - verify your new heroku remote repo with the following:
 ```
 $ git remote -v
 heroku  https://git.heroku.com/repo-name2.git (fetch)
heroku  https://git.heroku.com/repo-name2.git (push)
origin  git@github.com:username/repo-name.git (fetch)
origin  git@github.com:username/repo-name.git (push)
```
- the above output demonstrates that you can `push` source code updates to both remote repos.

## Adding Postgres
- add-on a `Postgres` database to Heroku:
```
$ heroku addons:create heroku-postgresql:hobby-dev
Creating heroku-postgresql:hobby-dev on ⬢ repo-name2... free
Database has been created and is available
 ! This database is empty. If upgrading, you can transfer
 ! data from another database with pg:copy
Created postgresql-unique-XXXXX as DATABASE_URL
Use heroku addons:docs heroku-postgresql to view documentation
```
- `hobby-dev` is the free plan for `Postgres` which has storage limits.
- check that pg was added: 
```
$ heroku addons
Add-on                                          Plan       Price  State
──────────────────────────────────────────────  ─────────  ─────  ───────

heroku-postgresql (postgresql-unique-XXXXX)  hobby-dev  free   created
 └─ as DATABASE

The table above shows add-ons and the attachments to the current app (repo-name2) or other apps.
```
- to see the database plan details, enter:
```
$ heroku pg:info
=== DATABASE_URL
Plan:                  Hobby-dev
Status:                Available
Connections:           0/20
PG Version:            9.6.4
Created:               2017-10-20 03:25 UTC
Data Size:             7.1 MB
Tables:                0
Rows:                  0/10000 (In compliance)
Fork/Follow:           Unsupported
Rollback:              Unsupported
Continuous Protection: Off
Add-on:                postgresql-unique-XXXXX
```
- your `Postgres` instance has an environment variable called: `DATABASE_URL`
- to see this URL provision, enter:
```
$ heroku config
=== repo-name2 Config Vars
DATABASE_URL: postgres://...@...amazonaws.com:5432/...
```
- this URL will be used to connect to the remote AWS container.
- in order to add `data` to your `Heroku Postgres`, you must have an existing Postgres database locally. To check, log into the pg interactive client. (note that your psql prompt may look different)
- use the `psql commands`: `\l`, `\c` and `\dt` to `list databases`, `connect to a db` and `list tables` respectively.  
```
$ psql postgres
psql (9.6.3)
Type "help" for help.

[local]:5432 postgres@postgres # \l
                                           List of databases
           Name            |   Owner    | Encoding |   Collate   |    Ctype    |   Access privileges
---------------------------+------------+----------+-------------+-------------+-----------------------
 myDB                      | username   | UTF8     | en_US.UTF-8 | en_US.UTF-8 |
```
- connect to `myDB` and view its tables:
```
[local]:5432 postgres@postgres # \c myDB
You are now connected to database "myDB" as user "postgres".
[local]:5432 postgres@myDB # \dt
                           List of relations
 Schema |       Name       | Type  |  Owner   |    Size    | Description
--------+------------------+-------+----------+------------+-------------
 public | table1           | table | postgres | 48 kB      |
 public | table2           | table | postgres | 88 kB      |
```
- transfer the contents from `myDB` to `Heroku Postgres`. The output will display Heroku adding data via the [pg_dump](https://www.postgresql.org/docs/9.6/static/app-pgdump.html) utility:
```
$ heroku pg:push myDB DATABASE_URL --app repo-name2
heroku-cli: Pushing myDB ---> postgresql-unique-XXXXX
pg_dump: last built-in OID is XXXXX
pg_dump: reading extensions
pg_dump: identifying extension members
pg_dump: reading schemas
pg_dump: reading user-defined tables
pg_dump: reading user-defined functions
...
```
- when complete, confirm `myDB` was added by the `Heroku psql` client: 
```
$ heroku pg:psql
--> Connecting to postgresql-unique-XXXXX
psql (9.6.3, server 9.6.4)
SSL connection (protocol: TLSv1.2, cipher: XXXXX-RSA-XXXXXX-XXX-SHAXXX, bits: 256, compression: off)
Type "help" for help.

XXX-XX-XXX-XXX-XXX.compute-1.amazonaws.com:5432 xxxxxxxxxxxxxx@xxxxxxx > \dt
                List of relations
 Schema |       Name       | Type  |     Owner
--------+------------------+-------+----------------
 public | table1           | table | xxxxxxxxxxxxxx
 public | table2           | table | xxxxxxxxxxxxxx

XXX-XX-XXX-XXX-XXX.compute-1.amazonaws.com:5432 xxxxxxxxxxxxxx@xxxxxxx > select * from table1;
repo-name2::DATABASE-> ;
 user_id  | first_name  |  last_name   |     last_update
----------+-------------+--------------+---------------------
        1 | FIRST1      | LAST1        | 2006-02-15 09:34:33
        2 | FIRST2      | LAST2        | 2006-02-15 09:34:33
```
- if `myDB` was successfully transferred to the `Heroku Postgres DATABASE_URL`, you should be able to query it from the `Heroku psql` client just as above.

## Deploying your application
- add the dependency modules to `requirements.txt`.
- this is needed to instruct Heroku to make pip installations to your `Dyno`.
- use `pip freeze` (or `pip3 freeze`) to see a list of Python libraries globally installed in your local machine.
- if you want to add all your libraries, write to the file with this line:
```
$ pip freeze > requirements.txt
```
- alternatively, you can add the minimum requirement for a Flask app by inserting the following into `requirements.txt` (recommended):
```
Flask==0.12.2
gunicorn==19.7.1
itsdangerous==0.24
Jinja2==2.7.3
MarkupSafe==0.23
Werkzeug==0.10.1
```
- create a `Procfile` to indicate that app.py is a Python application to run.
- two notes to keep in mind:
  1. a `Procfile` ***does not*** have a file type appended (e.g., Procfile.txt, Procfile.py, etc.)
  2. the first letter is always capitalized, and the rest lowercase.
  - for more info, click [here](https://devcenter.heroku.com/articles/procfile).
- add the following line to `Procfile`:
```
web: gunicorn app:app
```
- `gunicorn` is a HTTP Server for Python apps. It is also a dependency for Flask. See [documentation](http://gunicorn.org/).


- finally, deploy your application to Heroku.
- ***note: Heroku defaults code deployment pushed to the master branch***.
```
$ git push heroku master
```
- to deploy your application from a `non-master` branch (i.e. testbranch), enter:
```
$ git push heroku testbranch:master
```
- to view the live app, open in a browser to https://repo-name2.herokuapp.com or 
open via the Heroku CLI: 
```
$ heroku open
```
## Troubleshooting issues

- error: src refspec master does not match any.
  - https://stackoverflow.com/questions/26595874/i-want-make-push-and-get-error-src-refspec-master-does-not-match-any
- Heroku login does not work with cygwin or git bash.
  - https://github.com/heroku/cli/issues/84
  ```
  $ winpty heroku login
  ```
- heroku login authentication failure.
  - https://stackoverflow.com/questions/27810419/git-push-heroku-master-is-still-asking-for-authentication
  - first find the `_netrc` file that is created by heroku. In windows it can be found in:
  ```
  C:\Users\User Name\_netrc
  ```
  - that file contains credentials for git.heroku.com
   ```
  $ machine git.heroku.com
        login abcd123@gmail.com
        password xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
   ```
  - use that login and password when ask for authentication after $ git push heroku master command.

- use command `$ heroku logs` to see the latest 1500 lines from the log file.