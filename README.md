**Logs Analysis Project**

This project is part of the Udacity’s Full Stack Web Developer.

**The program**

This program will display the results of three queries :

1.  What are the most popular three articles of all time ?

2.  Who are the most popular article authors of all time ?

3.  On which days did more than 1% of requests lead to errors?

**Project Requirements**

The project should follow good practices like :

-   SQL style

-   Python code quality (PEP8 style guide)

**Setup steps**

**You don’t need to create table views (although mentioned beyond), the program
will do it.**

To run this project you will need the following software installed on your
computer :

-   Virtual Box

-   Vagrant (with a linux-based vm)

-   Python 3.7 or newer

-   PostgreSQL 9.5.x or newer

Clone or download the program and the database:

-   “loganalysis.py” (the program)

-   “newsdata.zip” (the database)

In your linux-based virtual machine on vagrant, populate the database with the
following command:

-   psql -d news -f newsdata.sql

Launch the program with the following command:

-   “python3.7 loganalysis.py”

**Views**

The views used here are only for the query : on wich day did more than 1% of
requests lead to errors ?

**View total :**

CREATE OR REPLACE VIEW total AS

SELECT time::date, status

FROM log;

**View failed:**

CREATE OR REPLACE VIEW failed AS

SELECT time, count(\*) AS sum

FROM total WHERE status like '%404%'

GROUP BY time;

**View stall:**

CREATE OR REPLACE VIEW stall AS

SELECT time, count(\*) AS sum

FROM total GROUP BY time;

**View calcul:**

CREATE OR REPLACE VIEW calcul AS

SELECT stall.time,

stall.sum AS nball,

failed.sum AS nbfailed,

ROUND((failed.sum::decimal/stall.sum::decimal \* 100),3) AS pctfailed

FROM stall, failed

WHERE stall.time = failed.time;
