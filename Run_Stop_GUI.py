#GUI= Avvia e Ferma il Servizio
#Quando viene fermato crea una copia dei backup sul desktop

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
    #down = True
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
        window.Element('_B_').Update(('Stop Backup', 'Start Backup')[down],##CHE CAZZO FA STO COSO DIO?????
         button_color=(('white', ('red', 'green')[down])))
    window.Close()

def run(config, config_path):
    # CHANGE FLAG RUN (true)
    config['STATE']['flag_run'] = 'run'  # è messo in run
    with open(config_path, 'w') as configfile:
        config.write(configfile)  # Salvo le modifiche
    # TOAST NOTIFY(IL BACKUP E' RIPARTITO)
    print("Backup Attivato!")


def time_stamp_folder(src, path_desktop, bool):
    # se il file di backup esiste
    if os.path.exists(src):

        # data modifica in perch
        data_mod = os.path.getmtime(src)

        if bool:
            # nome_cartella da salvare sul desktop
            name_dir = datetime.fromtimestamp(data_mod).strftime(
                "Oggi[Giorno_%d_Mese_%m]")  # fix
        else:
            name_dir = datetime.fromtimestamp(
                data_mod).strftime("[Ore%H_%M_giorno%m_%d]")

        # desktop+nomecartella_data
        full_path = os.path.join(path_desktop, name_dir)
        # crea la cartella
        os.makedirs(full_path, exist_ok=True)
        # copia il file sul path desktop
        shutil.copy2(src, full_path)
        print(full_path)
        print("File copiato correttamente")
    else:  # exception
        print(src, " non è stato trovato")


def save(config, config_path):
    print("salvo")
    # leggo i path da config
    config.read(config_path)
    dst1 = config['PATH']['dst1']
    dst2 = config['PATH']['dst2']
    dst3 = config['PATH']['dst3']
    daily = config['PATH']['daily']
    src = config['PATH']['src']

    full_dst1 = os.path.join(dst1, src)
    full_dst2 = os.path.join(dst2, src)
    full_dst3 = os.path.join(dst3, src)
    full_daily = os.path.join(daily, src)

    # creo una cartella dove il nome è la data dell'ultima modifica dei file
    # COPY FILE ON DESKTOP WITH TIMESTAMP

    if platform.system() == 'Linux':
        path_desktop = os.path.join(os.path.join(
            os.path.expanduser('~')), 'Scrivania/Backup_oggi')
    else:
        path_desktop = os.path.join(os.path.join(
            os.environ['USERPROFILE']), 'Desktop')

    # DESKTOP->TIMESTAMP (60)
    time_stamp_folder(full_dst1, path_desktop, False)
    # DESKTOP->TIMESTAMP (40)
    time_stamp_folder(full_dst2, path_desktop, False)
    # DESKTOP->TIMESTAMP (20)
    time_stamp_folder(full_dst3, path_desktop, False)
    # daily-> Nome deve essere->Giornaliero  :/
    time_stamp_folder(full_daily, path_desktop, True)

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
            '~\Documents'), 'WinTaskBackManager\config.ini')
    else:
        config_path = 'config.ini'  # funziona su linux ##--------------------------- BUG sdsd

    # FUNZIONE CHE CREA FILE INI  PREDEFINITO SE NON ESISTE
    #OPPURE
    #ERRORE -> IL FILE NON ESISTE
    config.read(config_path)
    st = config['STATE']['flag_run']
    if st == 'run':
        st = True
    else:
        st = False

    gui(config, config_path, st)  # 'run'/'stop' -> True/False


if __name__ == "__main__":

    main()