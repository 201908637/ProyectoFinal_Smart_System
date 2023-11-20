import datetime as dt
import logging
import dotenv
import os
import sys

from database_example import *
import database_smartHouse as db_sh
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

    while 1:
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
            _database: db_sh.CDatabaseSmartHouse = db_sh.CDatabaseSmartHouse(
                schema=db_schema,
                host=db_host,
                port=db_port,
                user=db_user,
                password=db_password,
                logger=logger,
            )
            if _database.connect():
                #### Extract data
                ok, results = _database.getSensorLastValue(
                    sensorID=1,
                )
                if ok:
                    for row in results:
                        for column_name, column_value in row.items():
                            print(f"{column_name}: {column_value}")

                #### Make decisions

                #### Export output
                ## Always start a new transaction when inserting data
                # _database.start_transaction()
                sensor_id = 1
                ok, insertedDataCount = _database.insertSensorValues(
                    sensor_id=sensor_id,
                    sensorValues=[
                        (int(dt.datetime.now().timestamp()), 23.1),
                        (int(dt.datetime.now().timestamp() + 1), 24.1),
                    ],
                )

                ## Decide if commit or rollback
                if ok:
                    logger.info(
                        f"{insertedDataCount} values inserted to sensor with ID-{sensor_id}"
                    )
                    _database.commit_transaction()
                else:
                    logger.info(f"Something went wrong inserting the new sensor values")
                    _database.rollback_transaction()

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
    a = 300
    b = 305

    print(f'{a}')
    a = b
    print(f'{a}')
    a = a + 1
    print(f'{b}')
    b = b + 4
    print(f'{b}')
    print(f'{a}')
    main()
