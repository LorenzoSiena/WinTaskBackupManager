# WinTaskBackupManager

## Test
Il file source viene copiato ogni volta che lo script viene avviato in uno dei 3 path sequenziali preimpostati da config.ini.
(Legge uno stato [a,b,c] preso da config.ini a cui corrisponde un path [dst1, dst2, dst3])

Ogni giorno viene creato un backup giornaliero

Se manca il file il programma esce e non fa niente

### $ Run_Stop.py run imposta un flag per abilitare l'applicazione
### $ Run_Stop.py stop imposta un flag per disabilitare l'applicazione
