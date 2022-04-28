# WinTaskBackupManager
Demone/Servizio in python per Windows e Linux(Beta)
Il programma si comporta come una state machine 

(A->B)
(B->C)
(C->A)

che in ogni stato copia un sorgente in una  dellle tre locazioni diverse

Ogni giorno salva il sorgente la prima volta nella cartella giornaliera

# Utilizzo:
Impostarre un task scheduler
	
	Task Scheduler->WINDOWS
	cron daemon -> LINUX
	
per avviare il Demone/Servizio ad un intervallo scelto.

## Installazione

(Consigliato)
Path_installazione = C:\Program Files (x86)\WinTaskbackManager

Creazione del TASK windows:
	Azione:
		Programma o script ($where.exe pythonw.exe)
		Aggiungi argomenti Backup.pyw
		inizio ->Path dello script == (C:\User.....Programmi(x86))
	
	Attivazione:
	
		[v]All'avvio Ritarda per 15 minuti
		[v]Ripeti l'attività ogni 20 minuti

REQUISITI:
  
  Python
	
  For Windows:  
    From POWERSHELL(ADMIN)
  
		  Set-ExecutionPolicy Unrestricted (ATTENZIONE:Abilita TUTTI gli script)
		  pip install PySimpleGUI 
		  Install-Module -Name BurntToast 
		  Import-Module BurntToast                                                                        

	

## Istruzioni
Dopo aver impostato il task per il file Backup.pyw

Se c'è un ERRORE con i file e vuoi fermare TUTTO e copiare i backup sulla scrivania
	Vai su Run_Stop_GUI.py  e clicca su STOP BACKUP
	Verrà create sul desktop una cartella "Backup_di_Oggi"
	con il backup negli orari degli ultimi 20,40,60 minuti
	e il backup giornaliero
