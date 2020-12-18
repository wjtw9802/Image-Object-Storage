from __future__ import print_function
from datetime import datetime
import mysql.connector

def sqlConnect():
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

    cnxcursor = cnx.cursor(buffered=True)

    while True:
        decision = input('choose what you would like to do (url, download, remove): ')
        print('choose a metadata to search')
        cnxcursor.execute("SELECT * FROM image")
        params = cnxcursor.column_names
        print(params)
        parameter = input()

        if parameter == 'altitude':
            minAltitude = input('specify minimum altitude: ')
            maxAltitude = input('specify maximum altitude: ')
            if decision == 'remove':
                sql = "SELECT * FROM image WHERE altitude >= '%s' and altitude <= '%s'" % (minAltitude, maxAltitude)
                cnxcursor.execute(sql)
                results = cnxcursor.fetchall()
                print("Here are are the results where: '%s' <= altitude <= '%s'" % (minAltitude, maxAltitude))
                printResults(results)
                if len(results) > 0:
                    ask = input("Delete anyway? (y/n)")
                    if ask == 'y':
                        sql = "DELETE FROM image WHERE altitude >= '%s' and altitude <= '%s'" % (minAltitude, maxAltitude)
                        cnxcursor.execute(sql)
                        results = cnxcursor.fetchall()
                        cnx.commit()
            else:
                sql = "SELECT * FROM image WHERE altitude >= '%s' and altitude <= '%s'" % (minAltitude, maxAltitude)
                cnxcursor.execute(sql)
                results = cnxcursor.fetchall()
                print("Here are are the results where: '%s' <= altitude <= '%s'" % (minAltitude, maxAltitude))
                printResults(results)
            return results, decision

        elif parameter == 'date':
            startDate = input('specify start date (mm/dd/yyyy): ')
            endDate = input('specify  end  date (mm/dd/yyyy): ')
            startDate_obj = datetime.strptime(startDate, '%m/%d/%Y')
            endDate_obj = datetime.strptime(endDate, '%m/%d/%Y')
            startDate_form = datetime.strftime(startDate_obj, "%Y-%m-%d")
            endDate_form = datetime.strftime(endDate_obj, "%Y-%m-%d")
            
            if decision == 'remove':
                sql = "SELECT * FROM image WHERE date >= '%s' and date <= '%s'" % (startDate_form, endDate_form)
                cnxcursor.execute(sql)
                results = cnxcursor.fetchall()
                print("Here are are the results where '%s' <= date <= '%s'" % (startDate_form, endDate_form))
                printResults(results)
                if len(results) > 0:
                    ask = input("Delete anyway? (y/n)")
                    if ask == 'y':
                        sql = "DELETE FROM image WHERE date >= '%s' and date <= '%s'" % (startDate_form, endDate_form)
                        cnxcursor.execute(sql)
                        results = cnxcursor.fetchall()
                        cnx.commit()
            else:
                sql = "SELECT * FROM image WHERE date >= '%s' and date <= '%s'" % (startDate_form, endDate_form)
                cnxcursor.execute(sql)
                results = cnxcursor.fetchall()
                print("Here are are the results where '%s' <= date <= '%s'" % (startDate_form, endDate_form))
                printResults(results)
            return results, decision

        elif any(x == parameter for x in params):
            cnxcursor.execute("SELECT DISTINCT "+parameter+" FROM image")
            results = cnxcursor.fetchall()
            resultlist = [row[0] for row in results]
            print('choose a(n) ', parameter, ' from the following options: ', resultlist)
            selection = input()
            if decision == 'remove':
                sql = """SELECT * FROM image WHERE """ + parameter + ' = %s'
                cnxcursor.execute(sql, (selection,))
                results = cnxcursor.fetchall()
                print('Here are are the results where ', parameter, ' = ', selection)
                printResults(results)
                if len(results) > 0:
                    ask = input("Delete anyway? (y/n)")
                    if ask == 'y':
                        sql = """DELETE FROM image WHERE """ + parameter + ' = %s'
                        cnxcursor.execute(sql, (selection,))
                        cnx.commit()
            else:
                sql = """SELECT * FROM image WHERE """ + parameter + ' = %s'
                cnxcursor.execute(sql, (selection,))
                results = cnxcursor.fetchall()
                print('Here are are the results where ', parameter, ' = ', selection)
                printResults(results)
            return results, decision  

        else:
            print('invalid parameter')
        
    cnxcursor.close()
    cnx.close()

def printResults(results):
    for row in results:
        print("name = ", row[0])
        print("camera = ", row[1])
        print("altitude = ", row[2])
        print("object = ", row[3])
        print("date = ", row[4])
        print("bucket = ", row[5])
        print("size = ", row[6], "\n")

    print(len(results), ' results found\n')

def remove(cnxcursor, decision):
    #sql_delete = """DELETE FROM table where id
    print("removing ")

