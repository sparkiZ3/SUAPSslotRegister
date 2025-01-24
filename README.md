# SUAPS slots register

A python program using the SUAPS API to register to a sport slot

# Installation

Use the package manager pip to install all the librairies via the `requirements.txt`.

`pip install -r requirements.txt`

# Usage

## API key 

Set your api key in  `SUAPSslotRegister/config.py` 

```
data={
    "API-KEY":"Your API key here"
}
```

the API key can be find in the cookies of your browser once connected to your account as `accessToken` :
- on firefox : `inspect` > `storage` > `cookies` > `https://u-sport.univ-nantes.fr` > copy `accessToken`

## Register to a slot

To register to a slot, have a look at `SUAPSslotRegister/main.py`

with this code you can register to 'tennis' on the 'Wednesday' of the current week

```py
#define the API
api = SuapsAPI()

#définition du sport souhaité
sport = "Tennis"
jour = "MERCREDI"

api.reserverCreneau(jour,sport)
```

you can retrieve all the activities you are registered for via the function `api.getActivitiesName()`

# Automate registration 
/!\ you must have a computer running at the time of registration

## Linux

To automate the registering in linux, you can use [crontab](https://doc.ubuntu-fr.org/cron) to automaticaly launch the script whenever you want. You can follow the documentation or ask chatgpt for the configuration file.

## Windows

To automate the registering with windows, you can use  [Schtasks](https://learn.microsoft.com/en-us/previous-versions/orphan-topics/ws.10/cc772785(v=ws.10)?redirectedfrom=MSDN) to automaticaly launch the script whenever you want. You can follow the documentation or ask chatgpt for the configuration file

## main API function

### **getUserData()**
with this function you can get some information about your account :

| name | type | exemple |
|--|--|--|
| code | string | 'E2XXXXXX' |
| numero | string | 'E2XXXXXX' |
| type | string | 'ETUDIANT_INTERNE' |
| typeExterne | ? | None |
| civilite | ? | None |
| nom | string | 'DUPONT' |
| prenom | string | 'David' |
| email | string | 'david.dupont@etu.univ-nantes.fr' |
| telephone | ? | None |
| dateNaissance | string | 2025-01-01 |
| estBoursier | boolean | True/False |
| composante | string | 'DEPT. XXXX' |
| departement | string | 'XXXX' |
| estInscrit | boolean | True/False |
| paiementEffectue | boolean | True/False |
| casContact | ? | None |
| reduction | ? | None |
| etablissementOrigine | ? | None |
| tagHexa | ? | None |
| majorite | string | 'Majeur' |

you can get only one element by passing the argument in the function :
for exemple, if you only want to get your name :
`api.getUserData('nom')`

### **getActivitiesName()**

this function returns an array of activities you are registered for

