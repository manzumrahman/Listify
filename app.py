from website import create_app
from dotenv import dotenv_values

database_uri = dotenv_values(".env")["DATABASE_URI"]
app = create_app(database_uri=database_uri)

if __name__ == '__main__':
    app.run(debug=True)
