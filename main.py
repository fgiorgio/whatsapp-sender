import os
from dotenv import load_dotenv
import mysql.connector
import pywhatkit

try:
    load_dotenv()

    mydb = mysql.connector.connect(
        host=os.environ.get('DB_HOST'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        database=os.environ.get('DB_NAME')
    )

    with mydb.cursor() as cursor:

        cursor.execute("SELECT telephone, message FROM " + os.environ.get('DB_TABLE'))
        result = cursor.fetchall()

        for row in result:
            telephone = row[0]
            message = row[1]

            try:
                pywhatkit.sendwhatmsg_instantly(
                    telephone,
                    message,
                    int(os.environ.get('WHATSAPP_WAIT_TIME')),
                    True,
                    int(os.environ.get('WHATSAPP_CLOSE_TIME'))
                )
                cursor.execute("DELETE FROM " + os.environ.get('DB_TABLE') + " WHERE telephone='" + telephone + "'")
            except Exception as e:
                print(telephone + ' - ' + str(e))

    mydb.close()

except Exception as e:
    print(e)
