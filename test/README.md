# README
Le programme `Test-Communication.py` permet de tester la carte de kill.

## Matériel
* 1x fils USB
* 3x fils Ethernet
* 1x carte interface RS-485
* 1x carte carte RS485 spliter
* 1x carte kill switch

## Installation
L'installation doit être faite une seule fois par dossier.

Dans le dossier /test, créer un environnement virtuel et faite l'installation des modules (entrez les commandes dans le terminal):

"""
python3 -m venv .venv
source .venv\Scripts\activate
python3 -m pip install -r requirements.txt
"""

## Utilisation
### Activation de l'environnement
L'environnement virtuel doit être activé à chaque nouvelle session de terminal.

Vérifier si l'environnement virtuel est activié: dans le terminal, le nom de l'environnement virtuel devrait être écrit avant le nom de session du terminal par ex: `(.venv) sonia-ele@soniaele-ThinkPad-T480s`. Si ce n'est pas le cas, activez l'environnement en entrant dans le terminal la commande suivante depuis le dossier test:

"""
source .venv/bin/activate
"""

### Modification du ficher `Test-Communication.py`
Le fichier Test-Communication.py doit être modifier en fonction du port série qui est utilisé l'interface RS. Connectez l'interface et entrez la commande suivante dans le terminal:
"""
ls /dev/ | grep ttyUSB
"""

Le nom du device associé devrait être afficher (par exemple: `ttyUSB0`). Modifier le fichier `Test-Communication.py`, pour changer le valeur de `PORT_SERIE` pour la valeur du device utiliser (par exemple `PORT_SERIE = '/dev/ttyUSB0'` si vous avez eu `ttyUSB0`)

Vous devez aussi modifier le fichier pour indiquer quel commande tester. Pour ce faire, utilisez `cmd_to_test = CMD_KILL` ou `cmd_to_test = CMD_MISSION` selon la commande que vous voulez tester (la premmière demande la valeur de la kill, la seconde la valeur de la mission)

### Execution du programme de test
Assurez vous d'avoir connecter l'interface RS, le board RS485 spliter et le board de kill (note: le board RS485 splitter est utiliser pour alimenter le board de kill, assurez vous qu'il est connecté à une source 12V avec un barrel jack, que le RS485 du board des IO est connecté dans le port de la KILL et que l'interface RS-485 est connecté à un autre port).

Dans le terminal dans lequel vous avez activer l'environnement virtuel, executez le fichier:
"""
python3 Test-Communication.py
""" 

### Interpretation de la sortie
Le programme commence par envoyer un message:
"""
> Envoi de la trame : ['0x3a', '0x4', '0x1', '0x0', '0x0', '0x4c', '0xd']
"""

Le programme reçoit ensuite une réponse 
"""
<- Réponse reçue : ['0x3a', '0x4', '0x1', '0x1', '0x0', '0x0', '0x4d', '0xd']
"""

La réponse est ensuite analysée:
"""
==================================
    start byte OK
    addr byte OK
    cmd kill OK
    kill state : 0
    size byte OK
    checksum byte OK
    end byte OK
MSG: OK
==================================
"""

### Fermeture du programme
Le programme peut-être arrêté en appyant sur CTRL+c