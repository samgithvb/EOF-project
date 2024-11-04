from operator import itemgetter
from flask import Flask, render_template, request, redirect, url_for, flash 
import sqlite3

app = Flask(__name__)


# Set a secret key for flash messages (used to show alerts to the user )
app.secret_key = "supersecretkey"

# Function to connect to the SQLite database
def get_db_connection():
    # Connectt to 'games.db' database - or whatever you have called it
    conn = sqlite3.connect('item.db')
    # This makes it easier to access rows as dictionaries and the 
    # data by the field heading rather than numbers
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')





@app.route('/games')
def view_age():
    # Connect to the database.
    conn = get_db_connection()
        # Rn an SQL query to get all the games from the 'games' table.
    item = conn.execute( 'SELECT * FROM item').fetchall()
    conn.close() # Close the database connection after getting the data
        # render the 'view_games.html' template and pass the games data to it
    conn.commit
    conn.close
    render_template('view_item.html', item = item )

@app.route('/edit/<int:id>', methods = ('GET', 'POST'))
def edit_item(id): 
    # Connect the database and get the game with the given id
    conn = get_db_connection()
    game = conn.execute('SELECT * FROM items WHERE id = ?', (id,)).fetchone()

    # If the form was submitted (POST request)
    if request.method == 'POST':
        # Get the updated data from the form
        name = request.form['name']
        description = request.form['description']
        origin = request.form['origin']
        age = request.form['age']
        provenance = request.form['provenance']
        # If any field is missing, show an error message
        if not name or not description or not origin or not age or not provenance:
            flash('All fields are required!')
        else:
            # Update the game in the databse with the new data
            conn.execute('UPDATE games SET title =  ?, platform = ?, genre = ?, year = ?, sales = ?, WHERE id = ?  ',
                    (name, description, origin, age, provenance))
            # Save the changes to the database
            conn.commit()
            # Close the connection
            conn.close()
            # Redirect to the 'view_games' page
            return redirect(url_for('view_item'))
# If its a GET request, show the form with the existing
    # game data so the user can edit it
    return render_template('edit_item.html', item = itemgetter)

def view_games(): 
    return render_template('view_item.html')
# Route to add a new game to the databse ('/add') - handles both GET (show the form) and POST (submit the form)

@app.route('/add', methods = ('GET', 'POST'))
def add_game():
    # If the form was submitted (POST request)
    if request.method == 'POST':
        # Get form data: title, platform, genre, year, sales
        name = request.form['name']
        description = request.form['description']
        origin = request.form['origin']
        age = request.form['age']
        provenance = request.form['provenance']

        # If any field is missing, shwow an error message
        if not name or not description or not origin or not age or not provenance:
            flash('All fields are required ')
        else:
            # If everything is filled im, insert the new game into the database
            conn = get_db_connection()
            conn.execute('INSERT INTO games (name, description, origin, age, provenance) VALUES (?, ?, ?, ?, ?, ?)')
            # Save the changes to the database
            conn.commit()
            # Close the connection
            conn.close()
            # Redirect to the 'view_games' page
            return redirect(url_for('view_item'))
# If its a GET request ( the user is just visiting the page),
# show the form to add a new game
if __name__ == '__main__':
    app.run(debug = True)