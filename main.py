import datetime as dt
import logging
import dotenv
import os
import sys

import database_smarthouse as sh
from logging.handlers import RotatingFileHandler


def main():
    dotenv.load_dotenv("./config/env_vars.env")

    log_filename = os.environ.get("LOG_FILENAME")
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_level = logging.INFO
    logger = logging.getLogger("Main")
    setUpLogger(
        logger=logger, filename=log_filename, format=log_format, level=log_level
    )
    check_env_vars(logger=logger)

    last_exe = 0

    # while 1:
    current_time = int(dt.datetime.now().timestamp())

    ## Execute every 15 min
    if (current_time - last_exe) > 900:
        start_time = int(dt.datetime.now().timestamp())
        logger.info("Starting main loop execution")

        db_schema = os.environ.get("DB_SCHEMA")
        db_host = os.environ.get("DB_HOSTNAME")
        db_port = os.environ.get("DB_PORT")
        db_user = os.environ.get("DB_USERNAME")
        db_password = os.environ.get("DB_PASSWORD")

        #### Connect to DDBB
        _database: sh.CDatabaseExample = sh.CDatabaseExample(
            schema=db_schema,
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            logger=logger,
        )
        if _database.connect():

            clientValues = [("12345678", "123"), 
                            ("23456789", "123")]
            ok, response_insert_cliente = _database.insertar_clientes(clientValues)

            id_zona = [("1"),
                       ("2"),]
            ok, response_insert_zona = _database.insertar_zona(id_zona)
            
            casaValues = [("1", "Calle A", "1"), 
                          ("2", "Calle B", "1"),
                          ("3", "Calle C", "2")]
            ok, response_insert_casa = _database.insertar_casa(casaValues)



            habitacionValues = [("1", "1"), 
                                ("2", "1"),
                                ("3", "1"),
                                ("4", "1"),
                                ("5", "1"),
                                ("1", "2"),
                                ("2", "2"),
                                ("3", "2")]
            ok, response_insert_habitacion = _database.insertar_habitacion(habitacionValues)

            clientecasaValues = [("12345678", "1"),
                                ("23456789", "2")]
            ok, response_insert_clientecasa = _database.insertar_clientecasa(clientecasaValues)

            tiposensorValues = [("1", "Mide temperatura", "Grados Celsius"),
                                ("2", "Mide potencia", "kW"),
                                ("3", "Mide humedad", "%")]
            ok, response_insert_tiposensor = _database.insertar_tiposensor(tiposensorValues)

            sensorValues = [("123", "1", "1", "1"),
                            ("456", "2", "1", "1"),
                            ("789", "3", "2", "2")]
            ok, response_insert_sensor = _database.insertar_sensor(sensorValues)

            tipoactuadorValues = [("1", "Mide temperatura", "Grados Celsius"),
                                  ("2", "Mide potencia", "kW"),
                                  ("3", "Mide humedad", "%")]

            _database.commit_transaction()
            
            ## Close connection to DB
            _database.disconnect()

            end_time = int(dt.datetime.now().timestamp())
            logger.info(f"Execution time (s): {end_time - start_time}")

            last_exe = current_time


def check_env_vars(
    logger: logging.Logger,
) -> bool:
    env_vars_list = [
        "DB_HOSTNAME",
        "DB_PORT",
        "DB_USERNAME",
        "DB_PASSWORD",
        "DB_SCHEMA",
        "LOG_FILENAME",
    ]

    for env_var in env_vars_list:
        if env_var not in os.environ:
            logger.error(f"Missing config env var: {env_var}")
            return False

    return True


def setUpLogger(logger, filename: str, format: str, level: int):
    # Add handler to show logging on console
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    formatter = logging.Formatter(format)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Check if log exists and should therefore be rolled
    needRoll = os.path.isfile(filename)

    # Add handler to manage rotation of logs
    log_rotationHandler = RotatingFileHandler(filename, backupCount=10)
    log_rotationHandler.setLevel(level)
    logger.addHandler(log_rotationHandler)

    # Create new log file every execution
    # if needRoll:
    #    logger.handlers[1].doRollover()

    logging.basicConfig(
        filename=filename,
        level=level,
        format=format,
    )


if __name__ == "__main__":
    main()
