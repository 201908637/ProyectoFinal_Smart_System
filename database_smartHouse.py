from database_base import *


class CDatabaseSmartHouse(CDatabase):

    def insertar_clientes(
        self,
        clientValues: list,   
    ):
        try:
            ok = True
            response : []
            
            for iban, cif in clientValues:
                os = "INSERT INTO CLIENTE (iban, cif) VALUES (%s, %s)"
                param = [iban, cif]
                
                ok_partial, response = self._insert_query(os, param)
                ok = ok_partial and ok
            return ok, response
        except Exception as e:
            self._logger.error(e)
            return False, e
        
    def insertar_zona(
        self,
        id_zona: int,
    ):
        try:
            ok = True
            response : []
            
            for id_zona_param in id_zona:
                os = "INSERT INTO ZONA_METEOROLOGICA (id_zona) VALUES (%s)"
                param = [id_zona_param]
                
                ok_partial, response = self._insert_query(os, param)
                ok = ok_partial and ok
            return ok, response
        except Exception as e:
            self._logger.error(e)
            return False, e
    
    def insertar_casa(
        self,
        casaValues: list,
    ):
        try:
            ok = True
            response : []
            
            for id_casa, adress, id_zona in casaValues:
                os = "INSERT INTO CASA (id_casa, adress, id_zona) VALUES (%s, %s, %s)"
                param = [id_casa, adress, id_zona]
                
                ok_partial, response = self._insert_query(os, param)
                ok = ok_partial and ok
            return ok, response
        except Exception as e:
            self._logger.error(e)
            return False, e


    def insertar_habitacion(
        self,
        habitacionValues: list,
    ):
        try:
            ok = True
            response : []
            
            for id_habitacion, id_casa in habitacionValues:
                os = "INSERT INTO HABITACION (id_habitacion, id_casa) VALUES (%s, %s)"
                param = [id_habitacion, id_casa]
                
                ok_partial, response = self._insert_query(os, param)
                ok = ok_partial and ok
            return ok, response
        except Exception as e:
            self._logger.error(e)
            return False, e
        
    def insertar_clientecasa(
        self,
        clientecasaValues: list,
    ):
        try:
            ok = True
            response : []
            
            for iban, id_casa in clientecasaValues:
                os = "INSERT INTO CLIENTE_CASA (iban, id_casa) VALUES (%s, %s)"
                param = [iban, id_casa]
                
                ok_partial, response = self._insert_query(os, param)
                ok = ok_partial and ok
            return ok, response
        except Exception as e:
            self._logger.error(e)
            return False, e 
         
    def insertar_tiposensor(
        self,
        tiposensorValues: list,
    ):
        try:
            ok = True
            response : []
            
            for id_tipo_sensor, description, unidad in tiposensorValues:
                os = "INSERT INTO TIPO_SENSOR (id_tipo_sensor, description, unidad) VALUES (%s, %s, %s)"
                param = [id_tipo_sensor, description, unidad]
                
                ok_partial, response = self._insert_query(os, param)
                ok = ok_partial and ok
            return ok, response
        except Exception as e:
            self._logger.error(e)
            return False, e     
        
    def insertar_sensor(
        self,
        sensorValues: list,
    ):
        try:
            ok = True
            response : []
            
            for n_serie_sensor, id_habitacion, id_tipo_sensor, id_casa in sensorValues:
                os = "INSERT INTO SENSOR (n_serie_sensor, id_habitacion, id_tipo_sensor, id_casa) VALUES (%s, %s, %s, %s)"
                param = [n_serie_sensor, id_habitacion, id_tipo_sensor, id_casa]
                
                ok_partial, response = self._insert_query(os, param)
                ok = ok_partial and ok
            return ok, response
        except Exception as e:
            self._logger.error(e)
            return False, e 
        
    def insertar_tipoactuador(
        self,
        tipoactuadorValues: list,
    ):
        try:
            ok = True
            response : []
            
            for id_tipo_actuador, desc_actuador, unidad in tipoactuadorValues:
                os = "INSERT INTO TIPO_ACTUADOR (id_tipo_actuador, desc_actuador, unidad) VALUES (%s, %s, %s)"
                param = [id_tipo_actuador, desc_actuador, unidad]
                
                ok_partial, response = self._insert_query(os, param)
                ok = ok_partial and ok
            return ok, response
        except Exception as e:
            self._logger.error(e)
            return False, e   
        
