import sqlite3

class DbOperation:

    def connection_to_db(self):
        conn = db = sqlite3.connect('password_records.db')
        return conn
    
    def create_table(self, table_name = "password_info"):
        conn = self.connection_to_db()
        query = f'''
        CREATE TABLE IF NOT EXISTS {table_name}(
            ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            WEBSITE TEXT NOT NULL,
            USERNAME VARCHAR(100),
            PASSWORD VARCHAR(50)
        );'''

        with conn as conn:
            cursor = conn.cursor()
            cursor.execute(query)

    def create_record(self, data, table_name = "password_info"):
        
        website = data['website']
        username = data['username']
        password = data['password']
        conn = self.connection_to_db()
        query = f'''
        INSERT INTO {table_name}('WEBSITE', 'USERNAME', 'PASSWORD') VALUES (?, ?, ?);
        '''
        with conn as conn:
            cursor = conn.cursor()
            cursor.execute(query, (website, username, password))



    def show_records(self, table_name = "password_info"):
        conn = self.connection_to_db()
        query = f'''
        SELECT * FROM {table_name};
        '''
        with conn as conn:
            cursor = conn.cursor()
            list_of_records = cursor.execute(query)
            return list_of_records
        
    def update_record(self, data, table_name = "password_info"):

        id = data['ID']
        website = data['website']
        username = data['username']
        password = data['password']

        conn = self.connection_to_db()
        query = f'''
        UPDATE {table_name} SET WEBSITE = ?, USERNAME = ?, PASSWORD = ?
        WHERE ID = ?;
        '''
        with conn as conn:
            cursor = conn.cursor()
            cursor.execute(query, (website, username, password, id))

    def delete_record(self, data, table_name="password_info"):
        id = data

        conn = self.connection_to_db()
        query_delete = f'''
        DELETE FROM {table_name} WHERE ID = ?;
        '''
        query_update = f'''
        UPDATE {table_name} SET ID = ID - 1 WHERE ID > ?;
        '''

        with conn as conn:
            cursor = conn.cursor()
            # Delete the record with the specified ID
            cursor.execute(query_delete, (id,))
            # Update IDs of remaining records
            cursor.execute(query_update, (id,))

    def search(self, Website, table_name = "password_info"):
        conn = self.connection_to_db()
        query = f'''
        SELECT * FROM {table_name} WHERE WEBSITE = ?;
        '''
        with conn as conn:
            cursor = conn.cursor()
            list_of_records = cursor.execute(query, (Website,))
            return list_of_records
