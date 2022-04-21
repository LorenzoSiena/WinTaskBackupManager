import PySimpleGUI as sg

def gui():
    layout = [
        [ # ---- First row
            sg.Text('Will copy all files and subfolders from the source to the destination') 
        ], [ # ---- New row
            sg.Text('Source foldersFIX', size=(15, 1)), 
            sg.InputText(key="source"), 
            sg.FileBrowse(target="source") 
        ], [ # ---- New row
            sg.Text('DestinationFolder1= Ogni 20 minuti', size=(15, 1)), 
            sg.InputText(key="destination1"), 
            sg.FolderBrowse(target="destination1") 
        ], [ # ---- New row
            sg.Text('DestinationFolder2= Ogni 40 minuti', size=(15, 1)), 
            sg.InputText(key="destination2"), 
            sg.FolderBrowse(target="destination2") 
        ], [ # ---- New row
            sg.Text('DestinationFolder3= Ogni 60 minuti', size=(15, 1)), 
            sg.InputText(key="destination3"), 
            sg.FolderBrowse(target="destination3") 
        ], [ # ---- New row
            sg.Text('DestinationFolderDaily= Ogni giorno', size=(15, 1)), 
            sg.InputText(key="destinationD"), 
            sg.FolderBrowse(target="destinationD") 
        ], [ # ---- New row
            sg.Button('Clicca per fermare il Backup', size=(5,2), button_color=('white', 'green'), key='_B_')
        ], [ # ---- New row
            sg.Submit(), sg.Cancel()
        ]
    ]
    window = sg.Window('Windows Backup Manager').Layout(layout)
    while True:
        event, values = window.Read() # Run the window until an "event" is triggered
        if event == "Submit":
            return values
        elif event is None or event == "Cancel":
            return None

if __name__ == "__main__":
    result = gui()
    result['source'] #src
    result['destination1'] #dst1
    result['destination2']  #dst2
    result['destination3']  #dst3
    result['destinationD']  #daily
    print(result)
