#library imports
import psycopg2
from psycopg2.extras import RealDictCursor
import os
import datetime

#local imports
from instance.config import app_config, db_url

env = os.environ['ENV']

class DbSetup:
    #this class initializes database connections
    def __init__(self, config_name):
        self.db_url = db_url
        self.db_connection = psycopg2.connect(self.db_url)


    def create_tables(self):
        db_connection = self.db_connection
        cursor = self.db_connection.cursor()
        queries = self.db_tables()
        for query in queries:
            cursor.execute(query)
        db_connection.commit()


    def drop_tables(self):
        table1 = """DROP TABLE IF EXISTS test_users CASCADE"""
        table2 = """DROP TABLE IF EXISTS test_products CASCADE"""
        table3 = """DROP TABLE IF EXISTS test_sales CASCADE"""

        db_connection=self.db_connection
        cursor = self.db_connection.cursor()
        queries = [table1, table2, table3]
        for query in queries:
            cursor.execute(query)
        db_connection.commit()




    def create_default_administrator(self):
        """Create a default administrator account"""
        db_connection = self.db_connection
        cursor = self.db_connection.cursor
        query = "SELECT * FROM users WHERE role=%s" 
        cursor.execute(query,('Admin',))
        Admin = cursor.fetchone()
        if not Admin:
            query = "INSERT INTO users(first_name, last_name, email_address, password, role)\
            VALUES(%s, %s, %s, %s, %s)"
            cursor.execute(query, ('Store', 'Owner', 'store.admin@storemanager.com', 'admin254', 'Admin'))
            db_connection.commit()


    def cursor(self):
        #this method holds data temporarily while it's being from or to the database
        cursor = self.db_connection.cursor(cursor_factory=RealDictCursor)
        return cursor


    def commit(self):
        #this method commits all changes to the database
        db_connection = self.db_connection()
        db_connection.commit()


    def db_tables(self):
        user_accounts = """CREATE TABLE IF NOT EXISTS users(
            user_id SERIAL PRIMARY KEY NOT NULL,
            first_name varchar(30) NOT NULL,
            last_name varchar(30) NOT NULL,
            email_address varchar(100) NOT NULL,
            password varchar(100) NOT NULL,
            role varchar(30) NOT NULL,
            member_since timestamp with time zone DEFAULT('now'::text)::date NOT NULL)"""


        product_tables = """CREATE TABLE IF NOT EXISTS products(
            productId integer PRIMARY KEY NOT NULL,
            product_name varchar(100) NOT NULL,
            product_category varchar(100) NOT NULL,
            selling_price integer NOT NULL,
            quantity integer NOT NULL,
            moq integer NOT NULL,
            description varchar(150),
            created_on timestamp with time zone DEFAULT('now'::text)::date NOT NULL)"""


        sales_tables = """CREATE TABLE IF NOT EXISTS sales(
            sale_id serial PRIMARY KEY NOT NULL,
            price integer NOT NULL,
            quantity integer NOT NULL,
            productId integer NOT NULL,
            sold_by varchar(100) NOT NULL,
            date_of_sale timestamp with time zone DEFAULT('now'::text)::date NOT NULL)"""


        queries = [user_accounts, product_tables, sales_tables]
        return queries