from application import settings
from sqlalchemy import create_engine

user = settings.DATABASES['default']['USER']
password = settings.DATABASES['default']['PASSWORD']
host = settings.DATABASES['default']['HOST']
port = settings.DATABASES['default']['PORT']
database_name = settings.DATABASES['default']['NAME']

def get_engine():
    database_url = 'mysql+pymysql://{user}:{password}@{host}:{port}/{database_name}?charset=utf8'.format(
        user=user,
        password=password,
        host=host,
        port=port,
        database_name=database_name,
    )
    return create_engine(database_url, echo=False)