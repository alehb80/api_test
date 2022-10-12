## Avvertenze

Usare le cartella "backend" come root del componente da sviluppare.

L'applicato Backend dovrà girare sulla porta 8000 su localhost.
Per lanciare lo stack è necessario usare docker-compose.

Per lanciare l'applicativo usare il comando 'bin/start.sh'.
Per fermare lo stack applicativo usare il comando 'bin/stop.sh'.

Nel package config risiedono i file con tutte le configurazioni del sistema.

Nel package odm risiedono i file con le classi d'interfacciamento al db.
È stata utilizzata la classe DocumentOdm come ODM per comunicare con il db e per effettuare le operazioni CRUD nel db.

Nel package services risiedono i file i servizi esposti del sistema.

Nel package test risiedono i file per testare operazioni del sistema.

Nel package utils risiedono i file che offrono operazioni di utility del sistema.
