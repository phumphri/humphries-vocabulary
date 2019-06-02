
# Upgrade libraries.
import os
if False:
    os.system("python -m pip install --upgrade pip")
    os.system("python -m pip install --upgrade flask")
    os.system("python -m pip install --upgrade flask_cors")
    os.system("pip install flask")
    os.system("pip install flask_cors")
    os.system("pip install flask_moment")
    os.system("pip install flask_bootstrap")
    os.system("pip install psycopg2")

# Application microservice.
import flask                            
from flask import (
    Response,
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

# Current date and time.
from flask_moment import Moment        
import datetime

 # Will not need since application server does everything.
from flask_cors import CORS            

# Dynamically arrange objects on webpage.
from flask_bootstrap import Bootstrap   

# S3 access.  This is to be replaced with a Postgres API.
# import boto3                            
# import botocore

# HTTP exceptions.
from werkzeug.exceptions import (    
    NotFound, 
    InternalServerError,
    NotImplemented)

# Needed for database connection.
import socket                          

# JSON fuctions.
import json                             
import pprint

# Libraries for accessing Postgres.
import psycopg2

# Assigning the Flask framework.
app = Flask(__name__)

# Rendering the single-page application.
@app.route("/")
def home():
    return render_template("index.html", 
        project_name="Vocabulary", 
        current_time=datetime.datetime.utcnow())

# Error Handler for Page Not Found
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', 
        project_name="Oops!", 
        message_from_the_application = e,
        current_time=datetime.datetime.utcnow()), 404

@app.route("/oops")
def simulate_page_not_found():
    raise NotFound('Just a test.  Everything is okay.')
 
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', 
        project_name="Bummer!", 
        message_from_the_application = e,
        current_time=datetime.datetime.utcnow()), 500

@app.route("/bummer")
def simulate_internal_server_error():
    raise InternalServerError('Relax.  This was only a test.')
    
# Error Handler for Not Implemented Exception
@app.errorhandler(501)
def not_implemented_exception(e):
    return render_template('501.html', 
        message_from_application = e,
        project_name="Not Implemented", 
        current_time=datetime.datetime.utcnow()), 501

@app.route("/not_implemented")
def simulate_not_implemented():
    raise NotImplemented('Relax, this was only a test message.')

# Accessor First Word
@app.route("/first_word", methods=['GET'])
def first_word():

    word = database_get_first_word()

    status_code = word["status_code"]

    # Convert the dictionary into a json string.
    word = json.dumps(word)

    # Return a response.
    response = Response(word, status=status_code, mimetype='application/json')
    return response

# Accessor Last Word
@app.route("/last_word", methods=['GET'])
def last_word():

    word = database_get_last_word()

    status_code = word["status_code"]

    # Convert the dictionary into a json string.
    word = json.dumps(word)

    # Return a response.
    response = Response(word, status=status_code, mimetype='application/json')
    return response

# Accessor Previous Word
@app.route("/previous_word/<word_spelling>", methods=['GET'])
def previous_word(word_spelling):

    word = database_get_previous_word(word_spelling)

    status_code = word["status_code"]

    # Convert the dictionary into a json string.
    word = json.dumps(word)

    # Return a response.
    response = Response(word, status=status_code, mimetype='application/json')
    return response

# Accessor Next Word
@app.route("/next_word/<word_spelling>", methods=['GET'])
def next_word(word_spelling):

    word = database_get_next_word(word_spelling)

    status_code = word["status_code"]

    # Convert the dictionary into a json string.
    word = json.dumps(word)

    # Return a response.
    response = Response(word, status=status_code, mimetype='application/json')
    return response

# Accessor Next Word
@app.route("/random_word", methods=['GET'])
def random_word():

    word = database_get_random_word()

    status_code = word["status_code"]

    # Convert the dictionary into a json string.
    word = json.dumps(word)

    # Return a response.
    response = Response(word, status=status_code, mimetype='application/json')
    return response

# Accessor Get Word
@app.route("/get_word/<word_spelling>", methods=['GET'])
def get_word(word_spelling):

    word = database_get_a_word(word_spelling)

    status_code = word["status_code"]

    # Convert the dictionary into a json string.
    word = json.dumps(word)

    # Return a response.
    response = Response(word, status=status_code, mimetype='application/json')
    return response

# Mutator Add Word
@app.route('/add_word', methods=['POST'])
def add_word():

    try:
        # Convert the transported string into a dictiornary.
        if request.is_json:

            # The transported string is converted into a json object.
            response = request.get_json()
    
            # Database update returns an HTTP status code.
            status_code = database_add_a_word(response)

            # Format a resonse with just the status code.
            response = Response(status=status_code)
            return response
        else:
            raise InternalServerError('Request was not in JSON format.')

    except UnicodeDecodeError as e:
        raise InternalServerError('An UnicodeDecoderError was thrown while parsing request:  ' + str(e))

    except Exception as f:
        raise InternalServerError('An Exception was thrown:  ' + str(f))

# Mutator Update Word
@app.route('/update_word', methods=['POST'])
def update_word():

    try:
        # Check if the request is in json format.
        if request.is_json:

            # Get the json response from the request.
            response = request.get_json()
    
            # Database update returns the status code of the update.
            status_code = database_update_a_word(response)

            # Format a json string and return it in a response.
            response = Response(status=status_code)
            return response
        else:
            raise InternalServerError('Request was not in JSON format.')

    except UnicodeDecodeError as e:
        raise InternalServerError('An UnicodeDecoderError was thrown while parsing request:  ' + str(e))

    except Exception as f:
        raise InternalServerError('An Exception was thrown:  ' + str(f))
    
# Mutator Delete Word
@app.route('/delete_word/<word_spelling>', methods=['GET'])
def deleted_word(word_spelling):

    # Database delete returns the status code of the deletion.
    status_code = database_delete_a_word(word_spelling)

    # Format a json string and return it in a response.
    response = Response(status=status_code)
    return response

# Connect to a Postgres database depending on location.
def connect_to_postgres():
    hostname = socket.gethostname()
    try:
        if (hostname == 'XPS'):
            conn = psycopg2.connect(os.environ['LOCAL_POSTGRES'])
            return conn
        elif (hostname == 'DESKTOP-S08TN4O'):  
            conn = psycopg2.connect(os.environ['LOCAL_POSTGRES'])
            return conn
        else:
            conn = psycopg2.connect(os.environ['AWS_POSTGRES'])
            return conn
    except Exception as e:
        print('Could not make database connedtion:', e)
        raise InternalServerError('Could not make database connection.')

# Database add
def database_add_a_word(response):

    ws = response["wordSpelling"]
    wg = response["wordGrammar"]
    wd = response["wordDefinition"]
    we = response["wordExample"]
    wa = response["wordAttempts"]
    wc = response["wordCorrect"]
    ww = response["wordWrong"]
    wp = response["wordPercentage"]

    print('\n\nws:', ws)
    print('wg:', wg)
    print('wd:', wd)
    print('we:', we)
    print('wa:', wa)
    print('wc:', wc)
    print('ww:', ww)
    print('wp:', wp)

    sql = 'insert into viterbi.vocabulary '
    sql += 'values(%s, %s, %s, %s, %s, %s, %s, %s) '

    conn = None
    try:
        conn = connect_to_postgres()
        cur = conn.cursor()
        cur.execute(sql, (ws, wg, wd, we, wa, wc, ww, wp))
        if cur.rowcount > 0:
            status_code = 200
        else:
            status_code = 404
        conn.commit()
        cur.close()

    except Exception as e:
        print('Exception was thrown:', str(e))
        raise InternalServerError('Exception was thrown:  ' + str(e))

    except psycopg2.DatabaseError as e:
        print('DatabaseError was thrown:', str(e))
        raise InternalServerError('A database error occurred:  ' + str(e))

    finally:
        if conn is not None:
            conn.close()
    return status_code

# Database update
def database_update_a_word(response):

    ws = response["wordSpelling"]
    wg = response["wordGrammar"]
    wd = response["wordDefinition"]
    we = response["wordExample"]
    wa = response["wordAttempts"]
    wc = response["wordCorrect"]
    ww = response["wordWrong"]
    wp = response["wordPercentage"]

    sql = 'update viterbi.vocabulary '
    sql += 'set word_type = %s, '
    sql += '    word_definition = %s, '
    sql += '    word_example = %s, '
    sql += '    word_attempts = %s, '
    sql += '    word_correct = %s, '
    sql += '    word_wrong = %s, '
    sql += '    word_percentage = %s '
    sql += 'where word_spelling = %s '

    conn = None
    try:
        conn = connect_to_postgres()
        cur = conn.cursor()
        cur.execute(sql, (wg, wd, we, wa, wc, ww, wp, ws))
        if cur.rowcount > 0:
            status_code = 200
        else:
            status_code = 404
        conn.commit()
        cur.close()

    except Exception as e:
        print('Exception was thrown:', str(e))
        raise InternalServerError('Exception was thrown:  ' + str(e))

    except psycopg2.DatabaseError as e:
        print('DatabaseError was thrown:', str(e))
        raise InternalServerError('A database error occurred:  ' + str(e))

    finally:
        if conn is not None:
            conn.close()
    return status_code

# Database delete
def database_delete_a_word(word_spelling):

    status_code = 0

    sql = "delete from viterbi.vocabulary "
    sql += "where word_spelling = %s"

    conn = None
    try:
        conn = connect_to_postgres()
        cur = conn.cursor()
        cur.execute(sql, (word_spelling,))
        if cur.rowcount > 0:
            status_code = 200
        else:
            status_code = 404
        conn.commit()
        cur.close()

    except Exception as e:
        print('Exception was thrown:', str(e))
        raise InternalServerError('Exception was thrown:  ' + str(e))

    except psycopg2.DatabaseError as e:
        print('DatabaseError was thrown:', str(e))
        raise InternalServerError('A database error occurred:  ' + str(e))

    finally:
        if conn is not None:
            conn.close()
    
    return status_code

# Connect to the database depending on location.
def connect_to_postgres():
    hostname = socket.gethostname()
    try:
        if (hostname == 'XPS'):
            conn = psycopg2.connect(os.environ['LOCAL_POSTGRES'])
            return conn
        elif (hostname == 'DESKTOP-S08TN4O'):  
            conn = psycopg2.connect(os.environ['LOCAL_POSTGRES'])
            return conn
        else:
            conn = psycopg2.connect(os.environ['AWS_POSTGRES'])
            return conn
    except Exception as e:
        print('Connection failed:', e)

# Database get first word.
def database_get_first_word():

    word = dict()

    sql = "select "
    sql += "word_spelling, "
    sql += "word_type, "
    sql += "word_definition, "
    sql += "word_example, "
    sql += "word_attempts, "
    sql += "word_correct, "
    sql += "word_wrong, "
    sql += "word_percentage "
    sql += "from viterbi.vocabulary "
    sql += "where word_spelling = (select min(word_spelling) from viterbi.vocabulary)"

    conn = None
    try:
        conn = connect_to_postgres()
        cur = conn.cursor()
        cur.execute(sql)
        row = None
        row = cur.fetchone()

        if row == None:
            word["wordSpelling"] = ""
            word["wordGrammar"] = ""
            word["wordDefinition"] = ""
            word["wordExample"] = ""
            word["wordAttempts"] = 0
            word["wordCorrect"] = 0
            word["wordWrong"] = 0
            word["wordPercentage"] = 0.0
            word["status_code"] = 404
        else:
            word["wordSpelling"] = row[0]
            word["wordGrammar"] = row[1]
            word["wordDefinition"] = row[2]
            word["wordExample"] = row[3]
            word["wordAttempts"] = row[4]
            word["wordCorrect"] = row[5]
            word["wordWrong"] = row[6]
            word["wordPercentage"] = row[7]
            word["status_code"] = 200

    except Exception as e:
        print('Exception was thrown:', str(e))
        raise InternalServerError('Exception was thrown:  ' + str(e))

    except psycopg2.DatabaseError as e:
        print('DatabaseError was thrown:', str(e))
        raise InternalServerError('A database error occurred:  ' + str(e))

    finally:
        if conn is not None:
            conn.close()
    
    return word

# Database get previous word.
def database_get_previous_word(word_spelling):

    word = dict()

    sql = "select "
    sql += "word_spelling, "
    sql += "word_type, "
    sql += "word_definition, "
    sql += "word_example, "
    sql += "word_attempts, "
    sql += "word_correct, "
    sql += "word_wrong, "
    sql += "word_percentage "
    sql += "from viterbi.vocabulary "
    sql += "where word_spelling = ("
    sql += "    select previous_word_spelling "
    sql += "    from viterbi.previous_word_spelling "
    sql += "    where word_spelling = %s) "

    conn = None
    try:
        conn = connect_to_postgres()
        cur = conn.cursor()
        cur.execute(sql, (word_spelling,))
        row = None
        row = cur.fetchone()

        if row == None:
            word["wordSpelling"] = ""
            word["wordGrammar"] = ""
            word["wordDefinition"] = ""
            word["wordExample"] = ""
            word["wordAttempts"] = 0
            word["wordCorrect"] = 0
            word["wordWrong"] = 0
            word["wordPercentage"] = 0.0
            word["status_code"] = 404
        else:
            word["wordSpelling"] = row[0]
            word["wordGrammar"] = row[1]
            word["wordDefinition"] = row[2]
            word["wordExample"] = row[3]
            word["wordAttempts"] = row[4]
            word["wordCorrect"] = row[5]
            word["wordWrong"] = row[6]
            word["wordPercentage"] = row[7]
            word["status_code"] = 200

    except Exception as e:
        print('Exception was thrown:', str(e))
        raise InternalServerError('Exception was thrown:  ' + str(e))

    except psycopg2.DatabaseError as e:
        print('DatabaseError was thrown:', str(e))
        raise InternalServerError('A database error occurred:  ' + str(e))

    finally:
        if conn is not None:
            conn.close()
    
    return word

# Database get a word.
def database_get_a_word(word_spelling):

    word = dict()

    sql = "select "
    sql += "word_spelling, "
    sql += "word_type, "
    sql += "word_definition, "
    sql += "word_example, "
    sql += "word_attempts, "
    sql += "word_correct, "
    sql += "word_wrong, "
    sql += "word_percentage "
    sql += "from viterbi.vocabulary "
    sql += "where word_spelling = %s"

    conn = None
    try:
        conn = connect_to_postgres()
        cur = conn.cursor()
        cur.execute(sql, (word_spelling,))

        row = None
        row = cur.fetchone()

        if row == None:
            word["wordSpelling"] = ""
            word["wordGrammar"] = ""
            word["wordDefinition"] = ""
            word["wordExample"] = ""
            word["wordAttempts"] = 0
            word["wordCorrect"] = 0
            word["wordWrong"] = 0
            word["wordPercentage"] = 0.0
            word["status_code"] = 404
        else:
            word["wordSpelling"] = row[0]
            word["wordGrammar"] = row[1]
            word["wordDefinition"] = row[2]
            word["wordExample"] = row[3]
            word["wordAttempts"] = row[4]
            word["wordCorrect"] = row[5]
            word["wordWrong"] = row[6]
            word["wordPercentage"] = row[7]
            word["status_code"] = 200

        cur.close()

    except Exception as e:
        print('Exception was thrown:', str(e))
        raise InternalServerError('Exception was thrown:  ' + str(e))

    except psycopg2.DatabaseError as e:
        print('DatabaseError was thrown:', str(e))
        raise InternalServerError('A database error occurred:  ' + str(e))

    finally:
        if conn is not None:
            conn.close()
    
    return word

# Database get next word.
def database_get_next_word(word_spelling):

    word = dict()

    sql = "select "
    sql += "word_spelling, "
    sql += "word_type, "
    sql += "word_definition, "
    sql += "word_example, "
    sql += "word_attempts, "
    sql += "word_correct, "
    sql += "word_wrong, "
    sql += "word_percentage "
    sql += "from viterbi.vocabulary "
    sql += "where word_spelling = ("
    sql += "    select next_word_spelling "
    sql += "    from viterbi.next_word_spelling "
    sql += "    where word_spelling = %s) "

    conn = None
    try:
        conn = connect_to_postgres()
        cur = conn.cursor()
        cur.execute(sql, (word_spelling,))

        row = None
        row = cur.fetchone()

        if row == None:
            word["wordSpelling"] = ""
            word["wordGrammar"] = ""
            word["wordDefinition"] = ""
            word["wordExample"] = ""
            word["wordAttempts"] = 0
            word["wordCorrect"] = 0
            word["wordWrong"] = 0
            word["wordPercentage"] = 0.0
            word["status_code"] = 404
        else:
            word["wordSpelling"] = row[0]
            word["wordGrammar"] = row[1]
            word["wordDefinition"] = row[2]
            word["wordExample"] = row[3]
            word["wordAttempts"] = row[4]
            word["wordCorrect"] = row[5]
            word["wordWrong"] = row[6]
            word["wordPercentage"] = row[7]
            word["status_code"] = 200

    except Exception as e:
        print('Exception was thrown:', str(e))
        raise InternalServerError('Exception was thrown:  ' + str(e))

    except psycopg2.DatabaseError as e:
        print('DatabaseError was thrown:', str(e))
        raise InternalServerError('A database error occurred:  ' + str(e))

    finally:
        if conn is not None:
            conn.close()
    
    return word

# Database get last word.
def database_get_last_word():

    word = dict()

    sql = "select "
    sql += "word_spelling, "
    sql += "word_type, "
    sql += "word_definition, "
    sql += "word_example, "
    sql += "word_attempts, "
    sql += "word_correct, "
    sql += "word_wrong, "
    sql += "word_percentage "
    sql += "from viterbi.vocabulary "
    sql += "where word_spelling = (select max(word_spelling) from viterbi.vocabulary)"

    conn = None
    try:
        conn = connect_to_postgres()
        cur = conn.cursor()
        cur.execute(sql)

        row = None
        row = cur.fetchone()

        if row == None:
            word["wordSpelling"] = ""
            word["wordGrammar"] = ""
            word["wordDefinition"] = ""
            word["wordExample"] = ""
            word["wordAttempts"] = 0
            word["wordCorrect"] = 0
            word["wordWrong"] = 0
            word["wordPercentage"] = 0.0
            word["status_code"] = 404
        else:
            word["wordSpelling"] = row[0]
            word["wordGrammar"] = row[1]
            word["wordDefinition"] = row[2]
            word["wordExample"] = row[3]
            word["wordAttempts"] = row[4]
            word["wordCorrect"] = row[5]
            word["wordWrong"] = row[6]
            word["wordPercentage"] = row[7]
            word["status_code"] = 200

    except Exception as e:
        print('Exception was thrown:', str(e))
        raise InternalServerError('Exception was thrown:  ' + str(e))

    except psycopg2.DatabaseError as e:
        print('DatabaseError was thrown:', str(e))
        raise InternalServerError('A database error occurred:  ' + str(e))

    finally:
        if conn is not None:
            conn.close()
    
    return word

# Database get RANDOM word.
def database_get_random_word():

    word = dict()

    sql = "select "
    sql += "word_spelling, "
    sql += "word_type, "
    sql += "word_definition, "
    sql += "word_example, "
    sql += "word_attempts, "
    sql += "word_correct, "
    sql += "word_wrong, "
    sql += "word_percentage "
    sql += "from viterbi.vocabulary "
    sql += "where word_percentage = (select min(word_percentage) from viterbi.vocabulary) "
    sql += "ORDER BY RANDOM() LIMIT 1"

    conn = None
    try:
        conn = connect_to_postgres()
        cur = conn.cursor()
        cur.execute(sql)

        row = None
        row = cur.fetchone()

        if row == None:
            word["wordSpelling"] = ""
            word["wordGrammar"] = ""
            word["wordDefinition"] = ""
            word["wordExample"] = ""
            word["wordAttempts"] = 0
            word["wordCorrect"] = 0
            word["wordWrong"] = 0
            word["wordPercentage"] = 0.0
            word["status_code"] = 404
        else:
            word["wordSpelling"] = row[0]
            word["wordGrammar"] = row[1]
            word["wordDefinition"] = row[2]
            word["wordExample"] = row[3]
            word["wordAttempts"] = row[4]
            word["wordCorrect"] = row[5]
            word["wordWrong"] = row[6]
            word["wordPercentage"] = row[7]
            word["status_code"] = 200

    except Exception as e:
        print('Exception was thrown:', str(e))
        raise InternalServerError('Exception was thrown:  ' + str(e))

    except psycopg2.DatabaseError as e:
        print('DatabaseError was thrown:', str(e))
        raise InternalServerError('A database error occurred:  ' + str(e))

    finally:
        if conn is not None:
            conn.close()
    
    return word

# Determine if running on home workstation, laptop, or from a deployment server.
if __name__ == "__main__":
    hostname = socket.gethostname()
    bootstrap = Bootstrap(app)
    moment = Moment(app)
    
    if (hostname == 'XPS'):
        app.run(debug=True)
    elif (hostname == 'DESKTOP-S08TN4O'):  
        app.run(debug=True)
    else:
        from os import environ
        app.run(debug=False, host='0.0.0.0', port=int(environ.get("PORT", 5000)))

