# Web Application Firewall


## Installazione
Dopo aver clonato la repository, basterà andare nella cartella `waf` e avviare il WAF

    docker compose up -d

Si consiglia di interrompere i container prima di un nuovo riavvio

    docker compose down

## Funzionamento
Quello che avviene è che il WAF si mette in ascolto del traffico su localhost alla porta 8000 e una volta verificati i controlli reindirizza il traffico sulla porta 5000.

Quindi teoricamente un amministratore dovrà configurare il proxy sostituendo a http://localhost:8000 l'url della propria web app da proteggere.

L'indirizzo http://localhost:5000 dove gira la web app è raggiungibile solo dal firewall.

Nota: nella repository sono state incluse le cartelle dei singoli servizi in modo da facilitare l'accessibilità per revisionare il codice. Tuttavia non sono necessari in quanto `docker-compose.yml` attinge direttamente da Docker Hub dove sono stati pushati i container.

## Amministrazione

Si può accedere al pannello dell'amministratore connnettendosi a http://localhost:3000 e da qui sarà possibile visualizzare le regole attive, modificarle, aggiungerele, visualizzare i log e monitorare in tempo reale il traffico.

Le credenziali per l'admin sono:

    Username: admin
    Password: admin123

## Sito d'esempio
In questa repository è stato aggiunto anche un semplicissimo sito d'esempio (nella cartella `website`) il cui unico scopo è quello di girare sulla porta 5000 e testare il funzionamento del firewall.
