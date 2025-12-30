from dotenv import load_dotenv
import os

load_dotenv()

db = os.getenv('DB')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
server = os.getenv('DB_SERVER')
port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')


__DB_CONFIG=f"{db}://{db_user}:{db_password}@{server}:{port}/{db_name}"
