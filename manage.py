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


def create_default_administrator(self):
    """Create a default administrator account"""
    con = self.connection()
    curr = self.cursor()
    query = "SELECT * FROM users WHERE role=%s" 
    curr.execute(query,('Admin',))
    Admin = curr.fetchone()
    if not Admin:
        query = "INSERT INTO users(first_name, last_name, email_address, password, role)\
         VALUES(%s, %s, %s, %s, %s)"
        curr.execute(query, ('Store', 'Owner', 'store.admin@storemanager.com', 'admin254', 'Admin'))
        con.commit()


def db_init(self):
    """A method that initializes the database connection"""
    con = self.connection
    con.commit()
    return con


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


