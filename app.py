from website import create_app
from dotenv import dotenv_values
import os

try:
    DATABASE_URI = dotenv_values(".env")["DATABASE_URL"]

except:
    DATABASE_URI = "postgresql://"+os.environ.get('DATABASE_URL')[11:]


app = create_app(database_uri=DATABASE_URI)

if __name__ == '__main__':
    app.run(debug=True)
