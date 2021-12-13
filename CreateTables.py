import psycopg2
from configuration.config import DBPARAMS

def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = [
        """
        DROP VIEW v_listings;
        """,
        """
        DROP TABLE IF EXISTS listings;
        """,
        """
        CREATE TABLE listings (
            listing_id INTEGER,
            place_id INTEGER NOT NULL,
            price INTEGER,
            area SMALLINT,
            room_count SMALLINT,
            register_date DATE NOT NULL
        );
        """,
        """
        CREATE OR REPLACE VIEW v_listings AS   (
                SELECT
                place_id,
                listing_id,
                min(register_date) AS first_seen,
                max(register_date) AS last_seen,
                array_agg(price ORDER BY register_date) AS prices
                FROM listings
                GROUP BY
                place_id,
                listing_id
        );
        """
    ]

    conn = None
    try:
        # read the connection parameters
        params = DBPARAMS
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    create_tables()

