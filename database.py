import psycopg2

# Database connection parameters
db_params = {
    'dbname': 'HarmX',
    'user': 'postgres',
    'password': '02052005',
    'host': 'localhost',  # or your database server address
    'port': 5432          # default port for PostgreSQL
}

# Connect to your postgres DB
conn = psycopg2.connect(**db_params)

# Open a cursor to perform database operations
cur = conn.cursor()

conn.autocommit = True

cur.execute(
    """CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL
    )"""
    )

cur.execute(
    """CREATE TABLE IF NOT EXISTS request_from_user (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        description VARCHAR(255) NOT NULL,
        file_url VARCHAR(255) NOT NULL,
        verified BOOLEAN DEFAULT FALSE
    )"""
)

def add_user(username, password):
    cur.execute(
        """INSERT INTO users (username, password)
        VALUES (%s, %s)""",
        (username, password)
    )
    
def add_request(title, description, file_url):
    cur.execute(
        """INSERT INTO request_from_user (title, description, file_url)
        VALUES (%s, %s, %s)""",
        (title, description, file_url)
    )

def verify_request(id):
    cur.execute(
        """UPDATE request_from_user
        SET verified = TRUE
        WHERE id = %s""",
        (id,)
    )

def get_requests():
    cur.execute(
        """SELECT * FROM request_from_user"""
    )
    data = cur.fetchall()
    return [
        {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "file_url": row[3],
            "verified": row[4]
        }
        for row in data
    ]


def get_verified_requests():
    cur.execute(
        """SELECT * FROM request_from_user
        WHERE verified = TRUE"""
    )
    data = cur.fetchall()
    return [
        {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "file_url": row[3],
            "verified": row[4]
        }
        for row in data
    ]

def get_unverified_requests():
    cur.execute(
        """SELECT * FROM request_from_user
        WHERE verified = FALSE"""
    )
    data = cur.fetchall()
    return [
        {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "file_url": row[3],
            "verified": row[4]
        }
        for row in data
    ]