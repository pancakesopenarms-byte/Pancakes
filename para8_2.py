import logging

logging.basicConfig(level=logging.DEBUG,
                    filename="logs_p82.log",
                    filemode="w",
                    format="We have logging message: %(asctime)s:%(levelname)s - %(message)s")



try:
    print(10/0)
except Exception:
    logging.exception("Exceptions")