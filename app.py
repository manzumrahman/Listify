from website import create_app
import os

database_uri = os.environ.get('DATABASE_URL')
print(database_uri)
app = create_app(database_uri=database_uri)

if __name__ == '__main__':
    app.run(debug=True)
