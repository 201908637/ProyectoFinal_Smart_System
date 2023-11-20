from database_base import *


class CDatabaseExample(CDatabase):
    def getSensorLastValue(
        self,
        sensorID: int,
    ):
        try:
            os = (
                "select origin.ID_SENSOR, origin.INFO_DATE, origin.VALUE from sensor_values origin, "
                "(select ID_SENSOR, MAX(INFO_DATE) as info_Date from sensor_values where ID_SENSOR = %s group by ID_SENSOR) latest "
                "where origin.ID_SENSOR = latest.ID_SENSOR and origin.INFO_DATE = latest.INFO_DATE;"
            )

            param = [sensorID]

            ok, response = self._select_query(os, param)

            return ok, response

        except Exception as e:
            self._logger.error(e)
            return False, e

    def insertCustomer(
        self,
        name: str,
    ):
        try:
            ## Get last id
            os_getID = ""
            os_getID = "SELECT MAX(ID_CUSTOMER) as ID FROM CUSTOMER;"
            ok, response = self._select_query(os_getID)
            if ok:
                lastID = response[1][0]
                customerID = lastID + 1
                ## Insert new customer
                os_insert = "INSERT INTO CUSTOMER (ID_CUSTOMER, NAME) VALUES (%s, %s);"
                param = [customerID, name]
                ok, response_insert = self._insert_query(os_insert, param)
            return ok, customerID
        except Exception as e:
            self._logger.error(e)
            return False, e

    def insertSensorValues(
        self,
        sensor_id: int,
        sensorValues: list,
    ):
        ok = True
        try:
            for timestamp, value in sensorValues:
                os = "INSERT INTO SENSOR_VALUES (id_sensor, info_date, value) VALUES (%s,FROM_UNIXTIME(%s),%s);"
                param = [sensor_id, timestamp, value]
                ok_partial, response = self._insert_query(os, param)
                ok = ok_partial and ok
            return ok, response
        except Exception as e:
            self._logger.error(e)
            return False, e
