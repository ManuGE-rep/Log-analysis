#!/usr/bin/env python3

import psycopg2

# Main and only class for the project


class DB_connection:
    def __init__(self):
        # Connect to the database
        try:
            self.connection = psycopg2.connect("dbname=news")
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    # Function to find Top 3 articles
    def Top_articles(self):
        query = ("""
        SELECT title, count(*) as article_view
        FROM articles
        JOIN log
        ON articles.slug = substring(log.path, 10)
        GROUP BY title
        ORDER BY article_view
        DESC LIMIT 3;""")
        self.cursor.execute(query)
        return self.cursor.fetchall()

    # Function to find Top authors
    def Top_authors(self):
        query = ("""
        SELECT authors.name, count(*) as authors_view
        FROM articles
        JOIN authors
        ON articles.author = authors.id
        JOIN log
        ON articles.slug = substring(log.path, 10)
        WHERE log.status LIKE '200 OK'
        GROUP BY authors.name
        ORDER BY authors_view
        DESC;""")
        self.cursor.execute(query)
        return self.cursor.fetchall()

    # Function to print result of above queries
    def PrintResult(self, request):
        top = request
        for i in range(len(top)):
            title = top[i][0]
            res = top[i][1]
            print(f"{title} - {res} views")
        print("\n")

    # Function to create total view
    def Create_view_total(self):
        query = ("""
        CREATE OR REPLACE VIEW total AS
        SELECT time::date, status
        FROM log;
        ;""")
        self.cursor.execute(query)

    # Function to create failed view
    def Create_view_failed(self):
        query = ("""
        CREATE OR REPLACE VIEW failed AS
        SELECT time, count(*) AS sum
        FROM total
        WHERE status LIKE '%404%'
        GROUP BY time;
        """)

    # Function to create stall view
    def Create_view_stall(self):
        query = ("""
        CREATE OR REPLACE VIEW stall AS
        SELECT time, count(*) AS sum
        FROM total
        GROUP BY time;
        """)

    # Function to create calcul view
    def Create_view_calcul(self):
        query = ("""
        CREATE OR REPLACE VIEW calcul AS
        SELECT stall.time, stall.sum AS nball,
        failed.sum AS nbfailed,
        ROUND((failed.sum::decimal/stall.sum::decimal * 100), 1) AS pctfailed
        FROM stall, failed
        WHERE statall.time = fai.time;
        """)

    # Function to query above views and return result
    def Error_log(self):
        query = ("""
        SELECT time, pctfailed
        FROM calcul
        WHERE round(pctfailed, 1) > 1;
        """)
        self.cursor.execute(query)
        return self.cursor.fetchall()

    # Function to print result of above query
    def Print_Error_log(self):
        for i in self.Error_log():
            print(f"{i[0]:%B %d, %Y}"
                  f" -- , {i[1]} % errors\n\n")


if __name__ == '__main__':
    # Connect to database and define variables for futur args
    db = DB_connection()
    articles = eval("db.Top_articles()")
    authors = eval("db.Top_authors()")
    log = eval("db.Error_log()")

    # Apply to object create views functions
    db.Create_view_total()
    db.Create_view_failed()
    db.Create_view_stall()
    db.Create_view_calcul()

    # Print output result
    print("\nThe most popular three articles of all time are : \n")
    db.PrintResult(articles)
    print("\nThe most popular article authors of all time are : \n")
    db.PrintResult(authors)
    print("\nDays with more than 1% of requests leading to errors? : \n")
    db.Print_Error_log()

    # Close connection
    db.connection.close()

    # Check to be sure that connection is closed
    # if db.connection.closed:
    #     print("\nThe connection is closed.")
    # else:
    #     print("The connectin is still opened.")
