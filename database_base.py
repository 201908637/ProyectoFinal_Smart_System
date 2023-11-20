import mysql.connector
import logging
-- jnjkn

class CDatabase:
    def __init__(
        self,
        schema: str,
        host: str,
        port: str,
        user: str,
        password: str,
        logger: logging.Logger = logging.getLogger(__name__),
    ):
        self._logger = logger
        self._db_schema = schema
        self._db_host = host
        self._db_user = user
        self._db_port = port
        self._db_pass = password
        self._db = mysql.connector.CMySQLConnection()

    def connect(self):
        try:
            self._db = mysql.connector.connect(
                host=self._db_host,
                port=self._db_port,
                user=self._db_user,
                passwd=self._db_pass,
                database=self._db_schema,
            )
        except Exception as e:
            self._logger.error(e)
            return False, e

        return True

    def disconnect(self):
        try:
            self._db.close()
        except Exception as e:
            self._logger.error(e)
            return False, e

        return True, None

    def _select_query(self, query: str, parameters: tuple = None) -> tuple[bool, list]:
        if self._db.is_connected() == False:
            self.connect()

        response = []
        try:
            cursor = self._db.cursor(dictionary=True)
            cursor.execute(query, parameters)
            response = cursor.fetchall()
            return True, response

        except Exception as e:
            self._logger.error(e)
            return False, e

    def _insert_query(self, query: str, parameters: tuple = None):
        if self._db.is_connected() == False:
            self.connect()

        try:
            cursor = self._db.cursor()
            cursor.execute(query, parameters)
            cursor.close()
            return True, cursor.rowcount

        except Exception as e:
            self._logger.error(e)
            return False, e

    def start_transaction(self):
        if self._db.is_connected() == False:
            self.connect()

        try:
            self._db.start_transaction()
            return True, None
        except Exception as e:
            self._logger.error(e)
            return False, e

    def commit_transaction(self):
        if self._db.is_connected() == False:
            self.connect()

        try:
            self._db.commit()
            return True, None
        except Exception as e:
            self._logger.error(e)
            return False, e

    def rollback_transaction(self):
        if self._db.is_connected() == False:
            self.connect()
        try:
            self._db.rollback()
            return True, None
        except Exception as e:
            self._logger.error(e)
            return False, e
