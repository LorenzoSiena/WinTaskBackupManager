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
        os.makedirs(dst1)
    if not os.path.exists(dst2):
        os.makedirs(dst2)
    if not os.path.exists(dst3):
        os.makedirs(dst3)
    if not os.path.exists(daily):
        os.makedirs(daily)


def main():
    # ADD PANIC BUTTON FOR TODAY??
    if not os.path.exists(src):  # MANCA IL FILE!
        sys.exit(42)  # POSSO RACCOGLIERLO E LANCIARE UN AVVERTIMENTO?

    # Uso configparser
    config = configparser.ConfigParser()
    # se non esiste config.ini crealo predefinito
    if not os.path.exists('config.ini'):  # config.ini->path/to/config.ini
        config['STATE'] = {'state': 'a'}
        config['PATH'] = {
            'dst1': '/path/to/dest1/',  # changethis
            'dst2': '/path/to/dest2/',  # changethis
            'dst3': '/path/to/dest3/',  # changethis
            'daily': '/path/to/daily/',  # changethis
            'src': '/path/to/backup'}  # changethis
        with open('config.ini', 'w') as configfile:  # config.ini->path/to/config.ini
            config.write(configfile)
    # recupero dal file ini
    dst1 = config['PATH']['dst1']
    dst2 = config['PATH']['dst2']
    dst3 = config['PATH']['dst3']
    daily = config['PATH']['daily']
    src = config['PATH']['src']

    init(dst1, dst2, dst3, daily)

    # BackupGiornaliero
    # SE la data di salvataggio di daily/backup è != oggi
    data_mod = os.path.getmtime(daily)
    last_mod = datetime.fromtimestamp(data_mod).strftime("%Y%m%d")
    now = datetime.now()
    today = now.strftime("%Y%m%d")
    if today != last_mod:
        shutil.copy2(src, daily)

    # raccoglie lo stato
    state = config['STATE']['st']

    if state == 'a':
        shutil.copy2(src, dst1)
        config['STATE']['st'] = 'b'  # stato-> stato_successivo
        config.write(configfile)  # IL FILE E' CHIUSO?????
        # ? f.close()
    elif state == 'b':
        shutil.copy2(src, dst2)
        config['STATE']['st'] = 'c'  # stato-> stato_successivo
        config.write(configfile)  # IL FILE E' CHIUSO?????
        # ? f.close()
    else:
        shutil.copy2(src, dst3)
        config['STATE']['st'] = 'a'  # stato-> stato_successivo
        config.write(configfile)  # IL FILE E' CHIUSO?????
        # ? f.close()


if __name__ == "__main__":
    main()


# TO-DO
    # IMPLEMENTARE TRY-CATCH
    # ERRORE: la periferica non è montata/ il percorso non esiste
    # IL FILE NON E' chiuso??
    # Atomizzare le funzioni del main->più funzioni
    # UNIT TEST!!!
    # shutil.copy2(src, dst1) salva le ultime modifiche? ---> MAC times
