# lucerne_scraping
Scraping the [lucerne summer festival webpage](https://www.lucernefestival.ch/en/program/summer-festival-22) and storing the data in postgres database system.

To run the code, do:

`docker-compose up -d db`

`docker-compose up --build pythonapp`

The resulting database when viewed using dbeaver looks like this:
First half of the database is (since the full database was not fitting on the screen of the laptop): 
