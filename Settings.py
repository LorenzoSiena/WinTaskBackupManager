# GUI= Imposta i path di lavoro

from ast import If
from asyncore import read
import configparser
import os
import platform
from tkinter.filedialog import Open
import PySimpleGUI as sg


def gui(s,d1,d2,d3,day):
    layout = [
        [  # ---- Titolo
            sg.Push(), sg.Text('Modifica il percorso del backup'), sg.Push()
        ], [  # ---- LineaVuota
            sg.Text('')
        ], [  # ---- New row
            sg.Text('File sorgente', size=(20, 1)),
            sg.InputText(default_text=s,key="src"),
            sg.FileBrowse(target="src", button_text="Scegli")
        ], [  # ---- New row
            sg.Text('1°dest(Ogni 20 minuti)', size=(20, 1)),
            sg.InputText(default_text=d1,key="dst1"),
            sg.FolderBrowse(target="dst1", button_text="Scegli")
        ], [  # ---- New row
            sg.Text('2°dest(Ogni 40 minuti)', size=(20, 1)),
            sg.InputText(default_text=d2,key="dst2"),
            sg.FolderBrowse(target="dst2", button_text="Scegli")
        ], [  # ---- New row
            sg.Text('3°dest(Ogni 60 minuti)', size=(20, 1)),
            sg.InputText(default_text=d3,key="dst3"),
            sg.FolderBrowse(target="dst3", button_text="Scegli")
        ], [  # ---- New row
            sg.Text('Salvataggio Giornaliero', size=(20, 1)),
            sg.InputText(default_text=day,key="daily"),
            sg.FolderBrowse(target="daily", button_text="Scegli")
        ], [  # ----  Submit/Cancel
            sg.Submit(button_color="green", size=(10, 1), button_text="Ok"),
            sg.Cancel(button_color="red", button_text="Annulla")
        ]
    ]
    window = sg.Window('Windows Backup Manager').Layout(layout)
    while True:
        event, values = window.Read()  # Run the window until an "event" is triggered
        if event == "Ok":
            return values
        elif event is None or event == "Annulla":
            return None


def test_ini():
    if platform.system() == 'Windows':
        config_path_file = os.path.join(os.path.expanduser('~\Documents'), 'WinTaskBackManager','config.ini')
        config_path = os.path.join(os.path.expanduser('~\Documents'), 'WinTaskBackManager')
    else:
        config_path = 'config.ini'  # test su linux
    if not os.path.isfile(config_path_file):
        os.makedirs(config_path, exist_ok=True)# CREA IL path di config.ini 
        result = {
            "src": "",
            "dst1": "",
            "dst2": "",
            "dst3": "",
            "daily": ""
        }
        set_ini(result)


def set_ini(result):
    src = result['src']  # src
    dst1 = result['dst1']  # dst1
    dst2 = result['dst2']  # dst2
    dst3 = result['dst3']  # dst3
    daily = result['daily']  # daily

    if platform.system() == 'Windows':
        config_path = os.path.join(os.path.expanduser('~\Documents'), 'WinTaskBackManager\config.ini')
    else:
        config_path = 'config.ini'  # test su linux

    config = configparser.ConfigParser()
    try:
        state = config['STATE']['st']
        flg = config['STATE']['flag_run']
    except KeyError:
        state = 'a'
        flg = 'run'

    config['STATE'] = {
        'st': state,
        'flag_run': flg
    }
    config['PATH'] = {
        'dst1': dst1,
        'dst2': dst2,
        'dst3': dst3,
        'daily': daily,
        'src': src
    }
    with open(config_path, 'w') as configfile:
            config.write(configfile)
    
if __name__ == "__main__":
    test_ini()

    
    #QUA DOVREI SAPERE LE SCELTE GIA FATTE :/    
    if platform.system() == 'Windows':
        config_path = os.path.join(os.path.expanduser('~\Documents'), 'WinTaskBackManager','config.ini')
    else:
        config_path = 'config.ini'  # test su linux
    if os.path.isfile(config_path):
        config = configparser.ConfigParser()
        config.read(config_path)
    
        src = config['PATH']['src']  # src
        dst1 = config['PATH']['dst1']  # dst1
        dst2 = config['PATH']['dst2']  # dst2
        dst3 = config['PATH']['dst3']  # dst3
        daily = config['PATH']['daily']  # daily
        print(src,dst1,dst2,dst3,daily)
    else:
        print("Il file non esiste -> valori nulli")
        src = ""
        dst1 = ""
        dst2 = ""
        dst3 = ""
        daily = ""
        
    result = gui(src,dst1,dst2,dst3,daily)
    if result != None:
        set_ini(result)
