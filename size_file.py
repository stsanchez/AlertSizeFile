import cx_Oracle
import os
import win32api
import win32net
import time
import datetime
import functions

#A LIST IS INITIALIZED WITH THE INFORMATION THAT THE MAIL WILL CONTAIN
mail_information = []

try:
    #I MAKE THE CONNECTION TO THE BASE TO GET ALL THE SERVERS TO WHICH I AM GOING TO CONNECT
    conn = cx_Oracle.connect('USERNAME', 'PASSWORD', 'SCHEMA')
    c = conn.cursor()
    f = conn.cursor()
    c.execute('''SELECT dl.SERVER_IP, dl.id_loc, dl.user_path, rd.ruta_recurso
                 FROM USERNAME.DB_LOC dl
                 join USERNAME.RECURSO_DBLOC rd on (dl.ID_LOC = rd.ID_LOC)
                 WHERE dl.SERVER_IP is not null and actualizar = 'T' and server_ip not like '%10.100.118%' ''')

    data = c.fetchall()

    #I GET THE CURRENT DATE FROM THE DATABASE
    f.execute('''select to_char (sysdate,'DD/MM/YYYY HH24:MI:ss') from dual''')
    date = f.fetchone()
    conn.close()		

except Exception as err:
    print(str(err))
    conn.close()

conn2 = cx_Oracle.connect('USERNAME_2', 'PASSWORD_2', 'SCHEMA_2')
  
second_connection = conn2.cursor()	
print (date[0])

#I ITER ALL THE SERVERS I GET WITH THE QUERY
for ip in data:
    try:
        #CONNECT TO THE REMOTE SERVER 
        username = 'username'
        password = 'password'
        use_dict={}
        use_dict['remote']=(f'\\\\{ip[0]}\\d$')
        use_dict['password']=(password)
        use_dict['username']=(username)
        win32net.NetUseAdd(None, 2, use_dict)

        #I GET THE SIZE OF THE FILE (DATABASE)
        sizefile =round (int (os.path.getsize('\\\\{ip[0]}\\{ip[2][0]}$\\basedatos\\sicam.gdb'/1024.0)),3)
        
        #I GET THE EXE CREATION DATE
        fecha =  (time.ctime(os.path.getmtime('\\\\{ip[0]}\\recursos\\cliente\\sicam.exe')))

        #I TRANSFORM THE STRING WITH THE DATE TO DATE FORMAT
        fecha = datetime.datetime.strptime(fecha, "%a %b %d %H:%M:%S %Y")
        
        try:
            #I RUN THE PROCEDURE INSERTING THE PARAMETERS (IDLOC, SIZE OF DATABASE, FECHA, DATE OF THE FILE (.EXE) IN DD/MM/YYY)
            second_connection.callproc('USERNAME_2.PR_INSERT_SICAM_TAM_BASES', (ip[1] , sizefile , date[0], fecha.strftime('%d/%m/%Y')))
            second_connection.execute('COMMIT')
            print('Se inserto correctamente ', ip[1] )
        except:
            print('No se pudo insertar ', ip[1])
        
        #CHECK DATABASE FILE SIZE
        if sizefile > 1:
            mail_information.append(ip[1])
       
    except:
        print('error de conexion', ip[1])
        #INSERT THE DATA WITHOUT INFO
        second_connection.callproc('MONITOREO.PR_INSERT_SICAM_TAM_BASES', (ip[1] , 0 , date[0], ''))
        second_connection.execute('COMMIT')

#CLOSE THE CONNECTION
conn2.close()

#EXECUTE THE FUNCTION TO SEND THE EMAIL
functions.mail(mail_information)
