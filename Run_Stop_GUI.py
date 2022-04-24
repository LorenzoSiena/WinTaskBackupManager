#GUI= Avvia e Ferma il Servizio
#Quando viene fermato crea una copia dei backup sul desktop

from pathlib import Path
import PySimpleGUI as sg
import configparser
from datetime import datetime
import os
import platform
import shutil
import sys
from time import strftime


def gui(config, config_path, down):
    flag = True # First iteration EASY STUPID FIX IDK DON'T TOUCH
    if down:
        layout = [[sg.Text('Il servizio è già attivo :)',key='_x_')],
              [sg.Button('Stop Backup', size=(15, 2), button_color=('white', 'red'), key='_B_')]]
    else:
        layout = [[sg.Text('Il servizio è disattivato :(',key='_x_')],
              [sg.Button('Start Backup', size=(15, 2), button_color=('white', 'green'), key='_B_')]]
    
    window = sg.Window('Window Title', layout)
    while True:             # Event Loop
        event, values = window.Read()
        if event in (None, 'Exit'):
            break
        if event == '_B_':
            if flag == True:
                flag= False
            else:
                down = not down
        
        if down:
            print("y")
            stop(config, config_path)
        else:
            print("X")
            run(config, config_path)
        window.Element('_x_').Update(('Il servizio è già attivo :)', 'Il servizio è disattivato :(')[down])
        window.Element('_B_').Update(('Stop Backup', 'Start Backup')[down],button_color=('white', ('red', 'green')[down]))
    window.Close()

def run(config, config_path):
    # CHANGE FLAG RUN (true)
    config['STATE']['flag_run'] = 'run'  # è messo in run
    with open(config_path, 'w') as configfile:
        config.write(configfile)  # Salvo le modifiche
    # TOAST NOTIFY(IL BACKUP E' RIPARTITO)
    print("Backup Attivato!")

                      #SRC= BLABLAB/backup.est #path_desktop=desktop/cartella_backup
def time_stamp_folder(src, path_desktop, bool):
    

   # data modifica in perch->
    data_mod = os.path.getmtime(src)  
    #->CREA Cartella destinazione orario/oggi
    if bool:
        # #daily
        name_dir = datetime.fromtimestamp(data_mod).strftime("Primo_di_Oggi(%d%m)")
    else: #ORARIO_dst1,ORARIO_dst2,ORARIO_dst3
        name_dir = datetime.fromtimestamp(data_mod).strftime("Orario(%H%M%S)Data(%m-%d)")

    # desktop+nomecartella_data
    dest_path = os.path.join(path_desktop, name_dir)
    # crea la cartella
    os.makedirs(dest_path, exist_ok=True)
    # copia il file sul path desktop
    shutil.copy2(src, dest_path)
    print(dest_path)
    print("File copiato correttamente")
    

def save(config, config_path):
    print("salvo")
    # leggo i path da config
    config.read(config_path)
    dst1 = config['PATH']['dst1']
    dst2 = config['PATH']['dst2']
    dst3 = config['PATH']['dst3']
    daily = config['PATH']['daily']
    src = config['PATH']['src']
    src=Path(src).name #ESTRAE IL NOME backup.estensione

    full_dst1 = os.path.join(dst1, src)
    full_dst2 = os.path.join(dst2, src)
    full_dst3 = os.path.join(dst3, src)
    full_daily = os.path.join(daily, src)

    # creo una cartella dove il nome è la data dell'ultima modifica dei file
    # COPY FILE ON DESKTOP WITH TIMESTAMP

    if platform.system() == 'Linux':
        path_desktop = os.path.join(os.path.join(
            os.path.expanduser('~')), 'Scrivania','Backup_di_oggi')
    else:
        path_desktop = os.path.join(os.path.join(
            os.environ['USERPROFILE']), 'Desktop','Backup_di_oggi')

    if os.path.isfile(full_dst1):
        time_stamp_folder(full_dst1, path_desktop, False)
    
    if os.path.isfile(full_dst2):
        time_stamp_folder(full_dst2, path_desktop, False)
    
    
    if os.path.isfile(full_dst3):
        time_stamp_folder(full_dst3, path_desktop, False)
    
    # daily-> Nome deve essere->Giornaliero  :/
    if os.path.isfile(full_daily):
        time_stamp_folder(full_daily, path_desktop, True)
    
    os.startfile(path_desktop)
    # DESKTOP->TIMESTAMP (TODAY)
    print("salvo")


def stop(config, config_path):
    # CHANGE FLAG RUN (false)
    config['STATE']['flag_run'] = 'stop'  # è messo in run
    with open(config_path, 'w') as configfile:
        config.write(configfile)  # Salvo le modifiche
    save(config, config_path)
    print("Backup Disattivato")
    # TOAST NOTIFY(FILE CREATI E BACKUP FERMO)


def main():
    config = configparser.ConfigParser()
    if platform.system() == 'Windows':##--------------------------- BUG sdsd
        config_path = os.path.join(os.path.expanduser(
            '~\Documents'), 'WinTaskBackManager','config.ini')
    else:
        config_path = 'config.ini'

    if not os.path.isfile(config_path):
        print("Prima avvia Settings")
        sg.popup_auto_close("ERRORE! Devi impostare il backup con Settings!",button_color="red",auto_close_duration=10)
        sys.exit(69)

    config.read(config_path)
    st = config['STATE']['flag_run']
    if st == 'run':
        st = True
    else:
        st = False
    gui(config, config_path, st)  # 'run'/'stop' -> True/False


if __name__ == "__main__":
    main()