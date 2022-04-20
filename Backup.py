from re import I
import shutil
import os,platform,subprocess
import sys
import configparser
import datetime
from datetime import datetime
from setuptools import Command

# Il file source viene copiato ogni volta che lo script viene avviato in uno dei 3 path sequenziali preimpostati da config.ini
# (Legge uno stato [a,b,c] preso da config.ini a cui corrisponde un path [dst1, dst2, dst3])
# Ogni giorno viene creato un backup giornaliero
# Se manca il file il programma esce e non fa niente


# Check che i path in cui salvare esistano
def init(dst1, dst2, dst3, daily):

    if not os.path.exists(dst1):
        try:
            os.makedirs(dst1, exist_ok=True)
            print("Directory "+ dst1 +" created successfully")
        except OSError as error:
            print("Directory "+ dst1 +" can not be created")
            print(error)

    if not os.path.exists(dst2):
        print("XXXX")
        try:
            os.makedirs(dst2, exist_ok=True)
            print("Directory "+ dst2 +" created successfully")
        except OSError as error:
            print("Directory "+ dst2 +" can not be created")
            print(error)

    if not os.path.exists(dst3):
        try:
            print("XXXX")
            os.makedirs(dst3, exist_ok=True)
            print("Directory "+ dst3 +" created successfully")
        except OSError as error:
            print("Directory "+ dst3 +" can not be created")
            print(error)

    if not os.path.exists(daily):
        try:
            print("XXXX")
            os.makedirs(daily, exist_ok=True)
            print("Directory "+ daily +" created successfully")
        except OSError as error:
            print("Directory "+ daily +" can not be created")
            print(error)

def errorh(flag,msg):

    err= 'New-BurntToastNotification -Text '
    command= err+msg
    if flag:
        print("test1:")
        subprocess.Popen(command, shell=True) #TEST1
        print("test2:")
        subprocess.Popen("New-BurntToastNotification -Text '%s' " % msg, shell=True) #TEST2
    print(msg)


def main():
    config_path = 'config.ini'  #PATH DEL FILE CONFIG.INI
    #Sono su windows?
    if platform.system() == 'Windows': 
        os.environ["COMSPEC"] = 'powershell'
        flag_win = True
    # Uso configparser
    config = configparser.ConfigParser()
     
    try:
        # se non esiste config.ini crealo predefinito
        if not os.path.exists(config_path): 
            config['STATE'] = {'st': 'a', 'flag_run': 'run'} 
            config['PATH'] = {
                'dst1': 'path/to/dest1/',  # changethis
                'dst2': 'path/to/dest2/',  # changethis
                'dst3': 'path/to/dest3/',  # changethis
                'daily': 'path/to/daily/',  # changethis
                'src': 'backup'   # changethis
                
            }
            with open(config_path, 'w') as configfile: 
                config.write(configfile)
        config.read(config_path) 
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
        msg="Errore config.ini"
        errorh(flag_win,msg)
        sys.exit(12)

    try:
        init(dst1, dst2, dst3, daily)
    except:
        msg="Errore funzione init()"
        errorh(flag_win,msg)
        sys.exit(22)

    if config['STATE']['flag_run'] == 'stop':
        msg="Il servizio è stoppato"
        errorh(flag_win,msg)
        sys.exit(0)

    if not os.path.exists(src):  # MANCA IL FILE!
        # TOAST NOTIFY -> IL FILE NON ESISTE
        msg="Il file del database non è stato trovato"
        errorh(flag_win,msg)
        sys.exit(99)

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
        msg="Errore Creazione backup Giornaliero"
        errorh(flag_win,msg)
        sys.exit(32)

    try:
        # raccoglie lo stato
        state = config['STATE']['st']

        if state == 'a':
            shutil.copy2(src, dst1)
            config['STATE']['st'] = 'b'  # stato-> stato_successivo
            with open(config_path, 'w') as configfile:
                config.write(configfile)  # IL FILE E' CHIUSO?????
            # ? f.close()
        elif state == 'b':
            shutil.copy2(src, dst2)
            config['STATE']['st'] = 'c'  # stato-> stato_successivo
            with open(config_path, 'w') as configfile:
                config.write(configfile)  # IL FILE E' CHIUSO?????
            # ? f.close()
        else:
            shutil.copy2(src, dst3)
            config['STATE']['st'] = 'a'  # stato-> stato_successivo
            with open(config_path, 'w') as configfile:
                config.write(configfile)  # IL FILE E' CHIUSO?????
            # ? f.close()
    except :
        msg="Errore passaggio di stato"
        errorh(flag_win,msg)
        sys.exit(52)
        
        


if __name__ == "__main__":
    main()


# TO-DO
    # IMPLEMENTARE TRY-EXEPT
    # ERRORE: la periferica non è montata/ il percorso non esiste
    # IL FILE NON E' chiuso??
    # Atomizzare le funzioni del main->più funzioni
    # UNIT TEST!!!
    # shutil.copy2(src, dst1) salva le ultime modifiche? ---> MAC times

#TRY
#Using the subprocess library it's possible to run CMD commands within Python. In order to run powershell commands, all you'd need to do is execute C:\Windows\System32\powershell.exe and pass through the arguments.
#import subprocess
#subprocess.call('C:\Windows\System32\powershell.exe Get-Process', shell=True)
#You can replace "Get-Process" with the PowerShell command you need


#####FUNZIONA#########
#IF WINDOWS FLAG =true 
# LANCIA QUESTO MESSAGGIO nelle eccezioni
#import os, subprocess    
#os.environ["COMSPEC"] = 'powershell'
#subprocess.Popen('New-BurntToastNotification -Text "MESSAGGIO_DA_INVIARE" ', shell=True)


############################