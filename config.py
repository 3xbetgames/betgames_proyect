class Config:
    SECRET_KEY = 'betgames3x'


class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = 'autorack.proxy.rlwy.net'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'aUJCbMrDpEfkcWjaOXuWmcyvpkwZLBbx'
    MYSQL_DB = 'railway'
    MYSQL_PORT = 16342  # Puerto de la instancia

# Configuración del entorno
config = {
    'development': DevelopmentConfig
}

