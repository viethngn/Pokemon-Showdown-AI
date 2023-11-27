import re

from src.db.mysql_connector import MySQLConnector


def fix_response_text(text):
    removed_irrelevant_text = re.sub('exports.Battle.*?= ', '',
                                     text.replace("'", '').replace('â\x80\x99d', '')
                                     .replace(';', '')
                                     .replace('Ì\x81beÌ\x81', 'be')
                                     .replace('Type: Null', 'Type Null'))
    json_string = re.sub(',desc:.*?"}', '}', removed_irrelevant_text)
    return re.sub("(\w+):", r'"\1":', json_string)

def open_mysql_connection(configs):
    print(f"Opening MySQL Connection {configs['mysql_user']}@{configs['mysql_host']}:{configs['mysql_port']}")

    return MySQLConnector(host=configs['mysql_host'],
                          user=configs['mysql_user'],
                          password=configs['mysql_password'],
                          database=configs['mysql_db'],
                          port=configs['mysql_port'])