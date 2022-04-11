import shutil
import os
import sys
import configparser
import datetime
from datetime import datetime

# Il file source viene copiato ogni volta che lo script viene avviato in uno dei 3 path sequenziali preimpostati da config.ini
# (Legge uno stato [a,b,c] preso da config.ini a cui corrisponde un path [dst1, dst2, dst3])
# Ogni giorno viene creato un backup giornaliero
# Se manca il file il programma esce e non fa niente


# Check che i path in cui salvare esistano
def init(dst1, dst2, dst3, daily):

    if not os.path.exists(dst1):
        try:
            os.makedirs(dst1, exist_ok=True)
            print("Directory '%s' created successfully" % dst1)
        except OSError as error:
            print("Directory '%s' can not be created")
    print("A")

    if not os.path.exists(dst2):
        print("XXXX")
        try:
            os.makedirs(dst2, exist_ok=True)
            print("Directory '%s' created successfully" % dst2)
        except OSError as error:
            print("Directory '%s' can not be created")
    print("B")

    if not os.path.exists(dst3):
        try:
            print("XXXX")
            os.makedirs(dst3, exist_ok=True)
            print("Directory '%s' created successfully" % dst3)
        except OSError as error:
            print("Directory '%s' can not be created")
    print("C")

    if not os.path.exists(daily):
        try:
            print("XXXX")
            os.makedirs(daily, exist_ok=True)
            print("Directory '%s' created successfully" % daily)
        except OSError as error:
            print("Directory '%s' can not be created")
    print("D")


def main():

    # Uso configparser
    config = configparser.ConfigParser()

    try:
        # se non esiste config.ini crealo predefinito
        if not os.path.exists('config.ini'):  # config.ini->path/to/config.ini
            config['STATE'] = {'st': 'a', 'flag_run': '1'}  # FLAG 1-0 RUN-STOP
            config['PATH'] = {
                'dst1': 'path/to/dest1/',  # changethis
                'dst2': 'path/to/dest2/',  # changethis
                'dst3': 'path/to/dest3/',  # changethis
                'daily': 'path/to/daily/',  # changethis
                'src': 'backup'   # changethis
            }
            with open('config.ini', 'w') as configfile:  # config.ini->path/to/config.ini
                config.write(configfile)
        print("BROH!")
        config.read('config.ini') ######???????????
        # recupero dal file ini
        dst1 = config['PATH']['dst1']
        dst2 = config['PATH']['dst2']
        dst3 = config['PATH']['dst3']
        daily = config['PATH']['daily']
        src = config['PATH']['src']
        print(daily)
        print(dst1)
        print(dst2)
        print(dst3)
        print(src)
    except Exception as e: 
        print(e)
        # TOAST NOTIFY
        # exit?

    try:
        init(dst1, dst2, dst3, daily)
    except:
        print('Errore funzione init()')
        # TOAST NOTIFY
        sys.exit(42)

    if config['STATE']['flag_run'] == '0':
        # TOAST NOTIFY -> Disattivo
        print("Il servizio è stoppato")

        sys.exit(42)

    if not os.path.exists(src):  # MANCA IL FILE!
        # TOAST NOTIFY -> IL FILE NON ESISTE
        print("IL file non esiste")
        sys.exit(42)

    try:

        # BackupGiornaliero
        # SE la data di salvataggio di daily/backup è != oggi
        
        dest = os.path.join(daily,src)
        if os.path.exists(dest) :
            data_mod = os.path.getmtime(dest)
            last_mod = datetime.fromtimestamp(data_mod).strftime("%Y%m%d")
            now = datetime.now()
            today = now.strftime("%Y%m%d")
            if today != last_mod:
                shutil.copy2(src, daily)
        else:
            shutil.copy2(src, daily)
    except:
        print('Errore Creazione backup Giornaliero!!')
        # TOAST NOTIFY
        # exit?

    try:
        # raccoglie lo stato
        state = config['STATE']['st']

        if state == 'a':
            shutil.copy2(src, dst1)
            config['STATE']['st'] = 'b'  # stato-> stato_successivo
            with open('config.ini', 'w') as configfile:
                config.write(configfile)  # IL FILE E' CHIUSO?????
            # ? f.close()
        elif state == 'b':
            shutil.copy2(src, dst2)
            config['STATE']['st'] = 'c'  # stato-> stato_successivo
            with open('config.ini', 'w') as configfile:
                config.write(configfile)  # IL FILE E' CHIUSO?????
            # ? f.close()
        else:
            shutil.copy2(src, dst3)
            config['STATE']['st'] = 'a'  # stato-> stato_successivo
            with open('config.ini', 'w') as configfile:
                config.write(configfile)  # IL FILE E' CHIUSO?????
            # ? f.close()
    except:
        print('Errore passaggio di stato!!')
        # TOAST NOTIFY
        # exit?


if __name__ == "__main__":
    main()


# TO-DO
    # IMPLEMENTARE TRY-EXEPT
    # ERRORE: la periferica non è montata/ il percorso non esiste
    # IL FILE NON E' chiuso??
    # Atomizzare le funzioni del main->più funzioni
    # UNIT TEST!!!
    # shutil.copy2(src, dst1) salva le ultime modifiche? ---> MAC times
