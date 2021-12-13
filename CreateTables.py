import psycopg2
from configuration.config import DBPARAMS,create_commands

def create_tables():
    """ script that creates the listing table and an associated view"""

    conn = None
    try:
        # read the connection parameters
        params = DBPARAMS
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in create_commands:
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

