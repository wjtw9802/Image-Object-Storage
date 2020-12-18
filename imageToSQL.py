from __future__ import print_function
from datetime import datetime
import mysql.connector

def sqlConnect(name, bucket, size):
    try:
        cnx = mysql.connector.connect(
            user = "newuser",
            password = "newpassword",
            host = "localhost",
            database = "images",
        )
        if (cnx.is_connected()):
            print('--Connected to mysql--')
    except:
        print('Unable to connect to mysql')

    cnxcursor = cnx.cursor()

    formedDate = acquireDate()
    camera = acquireCamera()
    altitude = acquireAltitude()
    obj = acquireObject()
    rows = formRows(name, bucket, size, camera, formedDate, altitude, obj)
    addRows(cnx, cnxcursor, rows)
    #printRows(cnx, cnxcursor)
    cnxcursor.close()
    cnx.close()


def acquireDate():
    dateDecision = input("specify date? (Y/N): ")
    if dateDecision == "Y":
        when = input("enter date (mm/dd/YYYY): ")
        chosenDate = datetime.strptime(when, '%m/%d/%Y')
    else:
        chosenDate = datetime.now()
    formedDate = datetime.strftime(chosenDate, "%Y-%m-%d")
    return formedDate

def acquireAltitude():
    altitude = input("specify altitude (meters): ")
    return altitude
    
def acquireObject():
    obj = input("specify object: ")
    return obj

def acquireCamera():
    camera = input("specify camera: ")
    return camera

def formRows(name, bucket, size, camera, date, altitude, obj):
    n = len(name)
    return list(zip(name, [camera]*n, [altitude]*n, [obj]*n, [date]*n, bucket, size))

def addRows(cnx, cnxcursor, rows):
    sql = 'INSERT INTO image(name, camera, altitude, object, date, bucket, size) VALUES(%s, %s, %s, %s, %s, %s, %s)'
    try:
        cnxcursor.executemany(sql, rows)
        cnx.commit()
        print( len(rows), 'rows added to mysql' )
    except:
        cnx.rollback()
        print('Unable to insert data')

def printRows(cnx, cnxcursor):
    cnxcursor.execute('SELECT * FROM image')
    results = cnxcursor.fetchall()
    for row in results:
        print(row)