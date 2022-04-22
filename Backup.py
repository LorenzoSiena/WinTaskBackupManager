#DEMONE= Va avviato ogni 20 minuti

#TODO-> sistemare e controllare le eccezioni
#controllare e testare su windows
    # ERRORE: la periferica non è montata/ il percorso non esiste
    # IL FILE NON E' chiuso??
    # UNIT TEST!!!

import shutil
import os,platform,subprocess
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
       # print("test2:")
       # subprocess.Popen("New-BurntToastNotification -Text '%s' " % msg, shell=True) #TEST2
    print(msg)

def main():
    n_conf="config.ini"
    #PERCORSO DEL FILE INI DA CREARE
    if platform.system() == 'Windows':
        config_path=os.path.join(os.path.expanduser('~\Documents'),'WinTaskBackManager')
        config_file=os.path.join(config_path,"config.ini")
        os.environ["COMSPEC"] = 'powershell'
        flag_win = True
    else:
        config_file = 'config.ini' #test su linux
        flag_win = False
    
    # Uso configparser
    config = configparser.ConfigParser()

    try:
        # se non esiste config.ini crealo predefinito
        if not os.path.exists(config_file):
            os.makedirs(config_path, exist_ok=True)#PATH DI config.ini
            
            config['STATE'] = {'st': 'a', 'flag_run': 'run'} 
            config['PATH'] = {
                'dst1': 'path/to/dest1/',  #TEST changethis  ->> Z:\Backup\20minfa
                'dst2': 'path/to/dest2/',  #TEST changethis  ->> Z:\Backup\40minfa
                'dst3': 'path/to/dest3/',  #TEST changethis  ->> Z:\Backup\60minfa
                'daily': 'path/to/daily/',  #TEST changethis ->> Z:\Backup\Oggi
                'src': 'backup'   #TEST changethis->> Nome 
            }
            with open(config_file, 'w') as configfile: #SHOULD WORK!
                config.write(configfile)
        config.read(config_file) 
        # recupero dal file ini
        dst1 = config['PATH']['dst1']
        dst2 = config['PATH']['dst2']
        dst3 = config['PATH']['dst3']
        daily = config['PATH']['daily']
        src = config['PATH']['src']

    except Exception as e: 
        print(e)
        msg="Errore_config_ini"
        errorh(flag_win,msg)
        sys.exit(12)

    try:
        init(dst1, dst2, dst3, daily)
    except:
        msg="Errore_funzione_init"
        errorh(flag_win,msg)
        sys.exit(22)

    if config['STATE']['flag_run'] == 'stop':
        msg="Il_servizio_è_stoppato"
        errorh(flag_win,msg)
        sys.exit(0)

    if not os.path.exists(src):  # MANCA IL FILE!
        msg="Il_file_del_database_non_trovato"
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
        msg="Errore_Creazione_backup_Giornaliero"
        errorh(flag_win,msg)
        sys.exit(32)

    try:
        # raccoglie lo stato
        state = config['STATE']['st']

        if state == 'a':
            shutil.copy2(src, dst1)
            config['STATE']['st'] = 'b'  # stato-> stato_successivo
            with open(config_file, 'w') as configfile:
                config.write(configfile)  # IL FILE E' CHIUSO?????
            #tEST ? f.close()
        elif state == 'b':
            shutil.copy2(src, dst2)
            config['STATE']['st'] = 'c'  # stato-> stato_successivo
            with open(config_file, 'w') as configfile:
                config.write(configfile)  # IL FILE E' CHIUSO?????
            #TEST ? f.close()
        else:
            shutil.copy2(src, dst3)
            config['STATE']['st'] = 'a'  # stato-> stato_successivo
            with open(config_file, 'w') as configfile:
                config.write(configfile)  # IL FILE E' CHIUSO?????
            ##TEST ? f.close()
    except :
        msg="Errore_passaggio_di_stato"
        errorh(flag_win,msg)
        sys.exit(52)
        
if __name__ == "__main__":
    main()
