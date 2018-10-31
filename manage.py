import psycopg2

import os

from instance.config import app_config

from app import create_app

env = os.environ['ENV']

def connection(config):
    app = create_app(config)
    dbname = app.config['DATABASE_NAME']
    user = app.config['USER']
    host = app.config['HOST']
    password = app.config ['PASSWORD']
    con = psycopg2.connect(database=dbname, user=user, host=host, password=password)
    return con


def create_database(self):
    """Create tables in the PostgreSQL database"""
    con = self.connection()
    curr = self.cursor()
    queries = self.tables()
    try:
        for query in queries:
            curr = con.cursor
            curr.execute(query)
            con.commit()
            print('Admin account created')
    except psycopg2.Error as e:
        print(e.pgerror)


def create_default_administrator(self):
    """Create a default administrator account"""
    con = self.connection()
    curr = self.cursor()
    query = "SELECT * FROM users WHERE email_address=%s" 
    curr.execute(query,('store.admin@storemanager.com',))
    admin = curr.fetchone()
    if not admin:
        query = "INSERT INTO users(first_name, last_name, email_address, password, role)\
         VALUES(%s, %s, %s, %s, %s)"
        curr.execute(query, ('Store', 'Owner', 'store.admin@storemanager.com', 'admin254', 'admin'))
        con.commit()


def commit(self):
    """A method that commits all changes to the database"""
    con = self.connection
    con.commit()


def db_tables(self):
    user_accounts = """CREATE TABLES IF NOT EXISTS users(
        user_id SERIAL PRIMARY KEY NOT NULL,
        first_name varchar(30) NOT NULL,
        last_name varchar(30) NOT NULL,
        email_address varchar(100) NOT NULL,
        password varchar(100) NOT NULL,
        role varchar(30) NOT NULL,
        member_since TIMESTAMP with timezone default(now::text)::date NOT NULL)"""


    product_tables = """CREATE TABLE IF NOT EXIST products(
        productId integer PRIMARY KEY NOT NULL,
        product_name varchar(100) NOT NULL,
        product_category varchar(100) NOT NULL,
        selling_price integer NOT NULL
        quantity integer NOT NULL,
        moq integer NOT NULL
        description varchar(150),
        date_added TIMESTAMP with timezone default(now::text)::date NOT NULL)"""


    sales_tables = """CREATE TABLE IF NOT EXIST sales(
        sale_id serial PRIMARY KEY NOT NULL,
        price integer NOT NULL,
        quantity integer NOT NULL,
        productId integer NOT NULL,
        sold by varchar(100) NOT NULL,
        date_of_sale TIMESTAMP with timezone default(now::text)::date NOT NULL)"""


    queries = [user_accounts, product_tables, sales_tables]
    return queries


