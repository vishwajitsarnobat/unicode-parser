# postgresql database config

DB_CONFIG = {
    "drivername": "postgresql",
    "username": "vishwajit",
    "password": "vishwajit",
    "host": "localhost",
    "port": "5432",
    "database": "answer-key"
}

# Connection string format: postgresql://user:password@host:port/database
CONNECTION_STRING = f"{DB_CONFIG['drivername']}://{DB_CONFIG['username']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
