import configparser
import os
import platform
import PySimpleGUI as sg

def gui():
    layout = [
        [ # ---- Titolo
            sg.Push(),sg.Text('Modifica il percorso del backup'),sg.Push()
        ],[ # ---- LineaVuota
            sg.Text('')
        ], [ # ---- New row
            sg.Text('File sorgente', size=(20, 1)), 
            sg.InputText(key="src"), 
            sg.FileBrowse(target="src", button_text = "Scegli") 
        ], [ # ---- New row
            sg.Text('1°dest(Ogni 20 minuti)', size=(20, 1)), 
            sg.InputText(key="dst1"), 
            sg.FolderBrowse(target="dst1",button_text = "Scegli") 
        ], [ # ---- New row
            sg.Text('2°dest(Ogni 40 minuti)', size=(20, 1)), 
            sg.InputText(key="dst2"), 
            sg.FolderBrowse(target="dst2", button_text = "Scegli") 
        ], [ # ---- New row
            sg.Text('3°dest(Ogni 60 minuti)', size=(20, 1)), 
            sg.InputText(key="dst3"), 
            sg.FolderBrowse(target="dst3", button_text = "Scegli") 
        ], [ # ---- New row
            sg.Text('Salvataggio Giornaliero', size=(20, 1)), 
            sg.InputText(key="daily"), 
            sg.FolderBrowse(target="daily", button_text = "Scegli") 
        ],  [ # ----  Submit/Cancel
            sg.Submit(button_color= "green",size=(10, 1), button_text = "Ok"),
            sg.Cancel(button_color= "red", button_text = "Annulla")
        ]
    ]
    window = sg.Window('Windows Backup Manager').Layout(layout)
    while True:
        event, values = window.Read() # Run the window until an "event" is triggered
        if event == "Ok":
            return values
        elif event is None or event == "Annulla":
            return None

def set_ini(result):
    src = result['src'] #src
    dst1 = result['dst1'] #dst1
    dst2 =result['dst2']  #dst2
    dst3 =result['dst3']  #dst3
    daily =result['daily']  #daily

    if platform.system() == 'Windows': 
        config_path=os.path.join(os.path.expanduser('~\Documents'),'WinTaskBackManager\config.ini')
    else:
        config_path = 'config.ini' #test su linux
    
    config = configparser.ConfigParser() 
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
    result = gui()
    set_ini(result)