import psycopg2


class WalletDB:
    def __init__(self, database_name: str = None, user: str = None, password: str = None,
                 host: str = None, port: int = None):
        self.database_name = database_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port

        self.create_table('wallets')

    def connect(self):
        try:
            conn = psycopg2.connect(
                dbname=self.database_name,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            return conn
        except Exception as e:
            raise e

    def create_table(self, table_name: str):
        try:
            conn = self.connect()
            cur = conn.cursor()
            sql = f'''CREATE TABLE IF NOT EXISTS "{table_name.upper()}" (
                "db_id"                 SERIAL NOT NULL PRIMARY KEY ,
                "db_date"               TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP ,
                "db_label"              TEXT ,
                "db_classic_address"    TEXT ,
                "db_xaddress"           TEXT ,
                "db_private_key"        TEXT ,
                "db_public_key"         TEXT ,
                "db_seed"               TEXT ,
                "db_sequence"           BIGINT 
                );'''
            cur.execute(sql)
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            raise e

    def insert_wallet(self, label: str, classic_address: str, xaddress: str,
                      private_key: str, public_key: str, seed: str, sequence: int):
        try:
            conn = self.connect()
            cur = conn.cursor()
            sql = f'''
            INSERT INTO "WALLETS" 
            ("db_label", "db_classic_address", "db_xaddress", "db_private_key", "db_public_key", "db_seed", "db_sequence") 
            VALUES (%s, %s, %s, %s, %s, %s, %s)'''
            cur.execute(sql, (label, classic_address, xaddress, private_key, public_key, seed, sequence))
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            raise e
