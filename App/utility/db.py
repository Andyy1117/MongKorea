import mysql.connector

def connect_db(config):
    conn = mysql.connector.connect(
        host=config["DBHOST"],
        user=config["DBUSERNAME"],
        password=config["DBPASSWORD"],
        database=config["DATABASE"]
    )
    return conn

def init_db(config):
    conn = mysql.connector.connect(
        host=config["DBHOST"],
        user=config["DBUSERNAME"],
        password=config["DBPASSWORD"]
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"DROP DATABASE IF EXISTS {config['DATABASE']};")
    cursor.execute(f"CREATE DATABASE {config['DATABASE']};")
    cursor.execute(f"use {config['DATABASE']};")
    cursor.execute(
        f""" 
        CREATE TABLE Users
        (
            id INT(11) NOT NULL AUTO_INCREMENT
            username VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            PRIMARY KEY (id)
        );
        """
    )
    cursor.execute(
        f"""
        CREATE TABLE Portfolio 
        (
            id INT(11) NOT NULL AUTO_INCREMENT,
            user_id INT(11) NOT NULL,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            PRIMARY KEY (id),
            FOREIGN KEY (user_id) REFERENCES Users(id)
        );
        """
    
    )

    cursor.execute(
        f"""
        CREATE TABLE Portfolio_items
        (
            id INT(11) NOT NULL AUTO_INCREMENT,
            portfolio_id INT(11) NOT NULL,
            title VARCHAR(255) NOT NULL,
            decription TEXT,
            type VARCHAR(50) NOT NULL,
            PRIMARY KEY (id)
            FOREIGN KEY (portfolio_id) REFERENCES Portfolios(id)
        )
        """
    )
    cursor.close()
    conn.close()
