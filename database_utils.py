import mysql.connector


# Table Schema 
# CREATE TABLE IF NOT EXISTS chattab (modalid INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255),
# contentType VARCHAR(50), samplefile VARCHAR(255), guidelines VARCHAR(255), responeSize VARCHAR(50), paid BOOLEAN);

def connect_db():
    db_config = { "host":"localhost",
    "user":"kzangoh",
    "database":"demozang",
    "password":"Super1432#*",
    "port" : "3306"}

    connection = mysql.connector.connect(**db_config)
    return connection 
  

def createUser(modalId, title, contentType, s3Path, guidelines, responseSize, description,openkey,paid=False):
    """
    Creates enteries in the Database 

    Parameter
    - modalId (string)
    - title (string)
    - contentType (string)
    - s3Path (string)
    - guidelines (string)
    - description (string)
    - paid (bool)

    Returns
    - string
    """


    try:
        connection = connect_db()
        cursor = connection.cursor()

        query = "DELETE FROM chattab WHERE modalid = %s"
        cursor.execute(query,(modalId,))
        connection.commit()

        query = """INSERT INTO chattab (modalid, title, contentType, samplefile, guidelines, responSeSize, description,paid,openkey) 
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

        cursor.execute(query,(modalId, title, contentType, s3Path, guidelines, responseSize, description, paid,openkey))
        connection.commit()

        if connection:
            connection.close()

        if cursor:
            cursor.close()
    
    except Exception as e:
        return str(e)

    return "success"


def getData(modalId):
    """
    Queries database to get a particular instance according to ModalId

    Parameters
    - modalId (string)

    Returns
    - String
    """

    try:
        connection = connect_db()
        cursor = connection.cursor()
        select_query = "SELECT * FROM chattab WHERE modalId = %s"
        cursor.execute(select_query, (modalId,))
        result = cursor.fetchone()
        if result:
            return result
        else:
            return None, None
    except Exception as e:
        return None, None
    finally:
        cursor.close()
        connection.close()


def getContentType(modal_id):
    """
    Queries database to get contentType and paid status for particular ModalId

    Parameters
    - modalId (string)

    Returns
    - string
    """

    try:
        connection = connect_db()
        cursor = connection.cursor()

        query = """SELECT paid, contentType FROM chattab WHERE modalId = %s"""
        cursor.execute(query,(modal_id,))
        res = cursor.fetchone()
        return res
    
    except Exception as e:
        print(f"error fetching data from database: {str(e)}")
        return None
    
    finally:
        cursor.close()
        connection.close()



def getOpenAI(modalId):
    connection = connect_db()
    cursor = connection.cursor()

    query = "SELECT openkey FROM chattab WHERE modalId=%s"

    cursor.execute(query,(modalId,))
    result = cursor.fetchone()[0]

    if connection:
        connection.close()

    if cursor:
        cursor.close()

    return result

