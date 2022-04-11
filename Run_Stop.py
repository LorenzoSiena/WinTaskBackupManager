import configparser
import sys

#Se riceve 1 Start backup
    #flag -> run
#Se riceve 0 Stop Backup
    #flag -> stop
    #copy file sul desktop

def run(config):
    #CHANGE FLAG RUN (true)
    config['STATE']['flag_run'] = 'run'  # è messo in run
    with open('config.ini', 'w') as configfile:
        config.write(configfile)  # Salvo le modifiche
    #TOAST NOTIFY(IL BACKUP E' RIPARTITO)
    print("Backup Attivato!")
       
def save():
    print("salvo")
    print("salvo")
    print("salvo")
    print("salvo")
    print("salvo")
    #COPY FILE ON DESKTOP WITH TIMESTAMP
    #DESKTOP->TIMESTAMP (60)
    #DESKTOP->TIMESTAMP (40)
    #DESKTOP->TIMESTAMP (20)
    #DESKTOP->TIMESTAMP (TODAY)
    print("salvo")

def stop(config):
    #CHANGE FLAG RUN (false)
   
    config['STATE']['flag_run'] = 'stop'  # è messo in run
    with open('config.ini', 'w') as configfile:
        config.write(configfile)  # Salvo le modifiche
    save()
    print("Backup Disattivato")
    #TOAST NOTIFY(FILE CREATI E BACKUP FERMO)

def main():
    if len(sys.argv) < 2:
        sys.exit("ERRORE: Argomenti mancanti")
    config = configparser.ConfigParser()
    config.read('config.ini')
    if sys.argv[1] == "stop":
        stop(config)
    elif sys.argv[1] == "run":
        run(config)
    else :
        sys.exit("ERRORE: Argomenti sbagliati contattare admin")



if __name__ == "__main__":
    main()
