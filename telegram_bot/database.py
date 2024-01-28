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
        user_id INTEGER NOT NULL,
        phone_number VARCHAR(255) DEFAULT NULL
    )"""
)

cur.execute(
    """CREATE TABLE IF NOT EXISTS request_from_user (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        description VARCHAR(255) NOT NULL,
        file_url VARCHAR(255) NOT NULL,
        location VARCHAR(255) DEFAULT NULL,
        verified BOOLEAN DEFAULT FALSE
    )"""
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
    
def add_user(user_id):
    cur.execute(
        """INSERT INTO users (user_id)
        VALUES (%s)""",
        (user_id,)
    )

def add_phone_number(user_id, phone_number):
    cur.execute(
        """UPDATE users
        SET phone_number = %s
        WHERE user_id = %s""",
        (phone_number, user_id)
    )
    
def get_phone_number(user_id):
    cur.execute(
        """SELECT phone_number FROM users
        WHERE user_id = %s""",
        (user_id,)
    )
    data = cur.fetchone()
    return data[0]

def get_users():
    cur.execute(
        """SELECT * FROM users"""
    )
    data = cur.fetchall()
    return [
        {
            "id": row[0],
            "user_id": row[1],
            "phone_number": row[2]
        }
        for row in data
    ]

def get_user(user_id): 
    cur.execute(
        """SELECT * FROM users
        WHERE user_id = %s""",
        (user_id,)
    )
    data = cur.fetchone()
    return {
        "id": data[0],
        "user_id": data[1],
        "phone_number": data[2]
    }
    
def all_phone_numbers():
    cur.execute(
        """SELECT phone_number FROM users"""
    )
    data = cur.fetchall()
    return [
        row[0]
        for row in data
    ]