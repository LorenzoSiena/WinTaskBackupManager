# DEMONE= Va avviato ogni 20 minuti

from pathlib import Path
import shutil
import os
import platform
import subprocess
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
            print("Directory " + dst1 + " created successfully")
        except OSError as error:
            print("Directory " + dst1 + " can not be created")
            print(error)

    if not os.path.exists(dst2):
        try:
            os.makedirs(dst2, exist_ok=True)
            print("Directory " + dst2 + " created successfully")
        except OSError as error:
            print("Directory " + dst2 + " can not be created")
            print(error)

    if not os.path.exists(dst3):
        try:
            os.makedirs(dst3, exist_ok=True)
            print("Directory " + dst3 + " created successfully")
        except OSError as error:
            print("Directory " + dst3 + " can not be created")
            print(error)

    if not os.path.exists(daily):
        try:
            os.makedirs(daily, exist_ok=True)
            print("Directory " + daily + " created successfully")
        except OSError as error:
            print("Directory " + daily + " can not be created")
            print(error)


def errorh(flag, msg):
    err = 'New-BurntToastNotification -Text '
    command = err+msg
    if flag:
        subprocess.Popen(command, shell=True)  # TEST1
        print(msg)


def main():
    # PERCORSO DEL FILE INI DA CREARE
    if platform.system() == 'Windows':
        # 'C:\\Users\\Luca_\\Documents\\WinTaskBackManager'
        config_path = os.path.join(os.path.expanduser(
            '~\Documents'), 'WinTaskBackManager')
        # 'C:\\Users\\Luca_\\Documents\\WinTaskBackManager\\config.ini'
        config_file = os.path.join(config_path, "config.ini")
        os.environ["COMSPEC"] = 'powershell'
        flag_win = True
    else:
        config_file = 'config.ini'  # test su linux
        flag_win = False

    # Uso configparser
    config = configparser.ConfigParser()
    try:
        # se non esiste config.ini crealo predefinito
        # <- SE NON ESISTE UN FILE CHIAMATO #'C:\\Users\\Luca_\\Documents\\WinTaskBackManager\\config.ini'
        if not os.path.isfile(config_file):
            # CREA IL path di config.ini
            os.makedirs(config_path, exist_ok=True)
            config['STATE'] = {'st': 'a', 'flag_run': 'run'}
            config['PATH'] = {
                'dst1': '',  # TEST changethis  ->> Z:\Backup\20minfa
                'dst2': '',  # TEST changethis  ->> Z:\Backup\40minfa
                'dst3': '',  # TEST changethis  ->> Z:\Backup\60minfa
                'daily': '',  # TEST changethis ->> Z:\Backup\Oggi
                'src': ''  # TEST changethis->> Nome.ESTENSIONE
            }
            with open(config_file, 'w') as configfile:  # SHOULD WORK!
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
        msg = "Errore_config_ini"
        errorh(flag_win, msg)
        sys.exit(12)

    try:
        init(dst1, dst2, dst3, daily)
    except:
        msg = "Errore_funzione_init"
        errorh(flag_win, msg)
        sys.exit(22)

    if config['STATE']['flag_run'] == 'stop':
        msg = "Il_servizio_è_stoppato"
        errorh(flag_win, msg)
        sys.exit(0)

    if not os.path.exists(src):  # MANCA IL FILE!
        msg = "File_del_database_non_trovato"
        errorh(flag_win, msg)
        sys.exit(99)

    try:

        # BackupGiornaliero
        # SE la data di salvataggio di daily/backup è != oggi
        # daily = path nel config.ini
        src_name = Path(src).name  # ESTRAE IL NOME backup.estensione
        # dest è il path #C:/daily/backup.est
        dest = os.path.join(daily, src_name)

        if os.path.isfile(dest):  # se il file esiste
            data_mod = os.path.getmtime(dest)  # estrai data ultima modifica
            # estrai data ultima modifica file_mod=(YYYY/MM/DD)
            last_mod = datetime.fromtimestamp(data_mod).strftime("%Y%m%d")
            now = datetime.now()  # estrai data oggi
            today = now.strftime("%Y%m%d")  # oggi(YYYY/MM/DD)
            if today != last_mod:  # oggi=(YYYY/MM/DD) != file_mod?
                shutil.copy2(src, daily)  # copia in daily
        else:
            shutil.copy2(src, daily)  # NON ESISTE? il file? -> copia!!!
    except:
        msg = "Errore_Creazione_backup_Giornaliero"
        errorh(flag_win, msg)
        sys.exit(32)

    try:
        # raccoglie lo stato
        state = config['STATE']['st']

        if state == 'a':
            shutil.copy2(src, dst1)
            config['STATE']['st'] = 'b'  # stato-> stato_successivo
            with open(config_file, 'w') as configfile:
                config.write(configfile)
        elif state == 'b':
            shutil.copy2(src, dst2)
            config['STATE']['st'] = 'c'  # stato-> stato_successivo
            with open(config_file, 'w') as configfile:
                config.write(configfile)
        else:
            shutil.copy2(src, dst3)
            config['STATE']['st'] = 'a'  # stato-> stato_successivo
            with open(config_file, 'w') as configfile:
                config.write(configfile)
    except FileNotFoundError as f:
        print(f)
        err = str(f).replace(" ", "_")
        errorh(flag_win, "Destinazione_non_trovata"+err)
        sys.exit(72)
    except Exception as e:
        print(e)
        msg = "Errore_passaggio_di_stato"
        errorh(flag_win, msg)
        sys.exit(52)


if __name__ == "__main__":
    main()
