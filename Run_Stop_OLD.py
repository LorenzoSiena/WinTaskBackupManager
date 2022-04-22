#TODO-> # controllare e testare time_stamp_folder_     
        # CREARE 2 FILE START e STOP con pyinstaller su WINDOWS

import configparser
from datetime import datetime
import os
import platform
import shutil
import sys
from time import strftime

#Se riceve 1 Start backup
    #flag -> run
#Se riceve 0 Stop Backup
    #flag -> stop
    #copy file sul desktop

def run(config,config_path):
    #CHANGE FLAG RUN (true)
    config['STATE']['flag_run'] = 'run'  # è messo in run
    with open(config_path, 'w') as configfile:
        config.write(configfile)  # Salvo le modifiche
    #TOAST NOTIFY(IL BACKUP E' RIPARTITO)
    print("Backup Attivato!")

def time_stamp_folder(src,path_desktop,bool):
    #se il file di backup esiste
    if os.path.exists(src) :

            #data modifica in perch
            data_mod = os.path.getmtime(src) 
            
            if bool:
                #nome_cartella da salvare sul desktop
                name_dir = datetime.fromtimestamp(data_mod).strftime("Oggi[Giorno:%d,Mese:%m]") #fix
            else:
                 name_dir = datetime.fromtimestamp(data_mod).strftime("[Ore%H:%M,giorno%m_%d]") #
            
            #desktop+nomecartella_data
            full_path=os.path.join(path_desktop,name_dir)
            #crea la cartella
            os.makedirs(full_path, exist_ok=True)
            #copia il file sul path desktop
            shutil.copy2(src, full_path)
            print(full_path)
            print("File copiato correttamente")
    else:   #exception
        print(src," non è stato trovato")

def save(config,config_path):
    print("salvo")
    #leggo i path da config
    config.read(config_path)
    dst1 = config['PATH']['dst1']
    dst2 = config['PATH']['dst2']
    dst3 = config['PATH']['dst3']
    daily = config['PATH']['daily']
    src = config['PATH']['src']
    
    full_dst1 = os.path.join(dst1,src)
    full_dst2 = os.path.join(dst2,src)
    full_dst3 = os.path.join(dst3,src)
    full_daily = os.path.join(daily,src)

    # creo una cartella dove il nome è la data dell'ultima modifica dei file 
    # COPY FILE ON DESKTOP WITH TIMESTAMP

    if platform.system() == 'Linux': 
        path_desktop= os.path.join(os.path.join(os.path.expanduser('~')),'Scrivania\Backup_oggi')
    else:
        path_desktop= os.path.join(os.path.join(os.environ['USERPROFILE']),'Desktop')

    #DESKTOP->TIMESTAMP (60)
    time_stamp_folder(full_dst1,path_desktop,False)
    #DESKTOP->TIMESTAMP (40)
    time_stamp_folder(full_dst2,path_desktop,False)
    #DESKTOP->TIMESTAMP (20)
    time_stamp_folder(full_dst3,path_desktop,False)
    #daily-> Nome deve essere->Giornaliero  :/
    time_stamp_folder(full_daily,path_desktop,True)
    
    #DESKTOP->TIMESTAMP (TODAY)
    print("salvo")

def stop(config,config_path):
    #CHANGE FLAG RUN (false)
    config['STATE']['flag_run'] = 'stop'  # è messo in run
    with open(config_path, 'w') as configfile:
        config.write(configfile)  # Salvo le modifiche
    save(config,config_path)
    print("Backup Disattivato")
    #TOAST NOTIFY(FILE CREATI E BACKUP FERMO)

def main():

    #PERCORSO DEL FILE INI DA CERCARE
    config = configparser.ConfigParser()
    if platform.system() == 'Windows': 
        config_path= os.path.join(os.path.expanduser('~\Documents'),'WinTaskBackManager\config.ini')
    else:
        config_path = 'config.ini' #test su linux
    config.read(config_path)
    
    
    #FUNZIONE STOP+SALVA SU SCRIVANIA
    stop(config,config_path)
    
    run(config,config_path)
    
if __name__ == "__main__":
    main()