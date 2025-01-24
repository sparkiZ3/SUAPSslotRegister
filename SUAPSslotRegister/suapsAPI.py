from config import data
import requests
import json
from datetime import datetime, timezone
import logging
from logging.handlers import RotatingFileHandler


class SuapsAPI:
    def __init__(self):
        self.ACCESS_TOKEN = data["API-KEY"]
        self.periodId = self.getCatalogue()[0]["id"]
        handler = RotatingFileHandler('app.log', backupCount=5)
        logging.basicConfig(
            handlers=[handler],
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            level=logging.INFO
        )
    
    #permet de recuperer des informations sur l'utilisateur en fonction de son accessToken
    def getUserData(self, value=None):
        url = "https://u-sport.univ-nantes.fr/api/individus/me"

        headers = {
            "Cookie": "accessToken="+self.ACCESS_TOKEN,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0",
        }
        response = requests.get(url, headers=headers)
        if value is not None:
            try:
                return response.json()[value]
            except:
                return "Error : aucune valeur ne correspond a la valeur renseignée pour getUserData"
        else:
            return response.json()

    #Pas tellement compris l'utilité mais renvoie l'Id de la periode pour l'annnée en cours
    def getCatalogue(self):
        url = "https://u-sport.univ-nantes.fr/api/extended/periodes/catalogue?idCatalogue="

        headers = {
            "Cookie": "accessToken="+self.ACCESS_TOKEN,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0",
        }
        response = requests.get(url, headers=headers)
        return response.json()


    #permet de recuperer les activités lié a votre compte en fonction de l'ID de la période
    #A moitié fonctionnel car je n'ai qu'un seul sport et je ne sais pas ce que renvoie la requete si on a plusieurs sports
    def getActivities(self):
        url = "https://u-sport.univ-nantes.fr/api/extended/activites/individu/paiement?idIndividu=E232643Y&typeIndividu=ETUDIANT_INTERNE&idPeriode="+self.periodId

        headers = {
            "Cookie": "accessToken="+self.ACCESS_TOKEN,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0",
        }

        response = requests.get(url, headers=headers)

        return response.json()
    
    def getActivitiesName(self):
        activities = self.getActivities()
        returnActivities = []
        for activity in activities["activites"]:
            returnActivities.append(activity["nom"])
            print(activity["nom"])
        return returnActivities
        
    
    def getActivitieId(self,sport):
        activities = self.getActivities()
        for activity in activities["activites"]:
            if activity["nom"] == sport:
                return activity["id"]
        return None

    #permet de recuperer les créneaux disponibles en fonction de l'ID de l'activité et de la période
    def getCreneaux(self,activityId,periodeId):
        url = "https://u-sport.univ-nantes.fr/api/extended/creneau-recurrents/semaine?idActivite="+activityId+"&idPeriode="+periodeId+"&idIndividu=E232643Y"

        headers = {
            "Cookie": "accessToken="+self.ACCESS_TOKEN,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0",
        }


        response = requests.get(url, headers=headers)

        response_dict= json.loads(response.text)
        
        #print("il y a "+ str(len(response_dict)) + " créneaux disponibles pour cette activité")
        return response.json()


    #comme la fonction getCreneaux mais prend en consideration le jour en parametre
    def getCreneau(self,activityId,periodeId ,jour):
        jour=jour.upper()
        print(jour)
        creneaux = self.getCreneaux(activityId,periodeId)
        
        
        for creneau in creneaux:
            if creneau["jour"] == jour:
                return creneau["id"],creneau["quota"],creneau["nbInscrits"]
   
   
    def getCreneauJSON(self,activityId,periodeId ,jour):
        jour=jour.upper()
        creneaux = self.getCreneaux(activityId,periodeId)
        
        #print(creneaux)
        
        for creneau in creneaux:
            if creneau["jour"] == jour:
                return creneau
        print("Aucun creneau trouvé pour le jour : "+jour)
        return None
        
    #sert a formater les données pour la requete de reservation
    def createJson(self,activityId,jour):
        userData = self.getUserData()
        iso_format_time = datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace("+00:00", "Z")
        creneauData = self.getCreneauJSON(activityId,self.periodId,jour)

        if creneauData is None:
            return None

        jsonData ={
            "utilisateur": {
                "login": userData["code"],
                "typeUtilisateur": "ETUDIANT_INTERNE"
            },
            "dateReservation": iso_format_time,
            "actif": False,
            "forcage": False,
            "creneau": creneauData,
            "individuDTO": userData
        }
        
        jsonData["creneau"]["actif"] = True

        jsonData = json.dumps(jsonData, indent=4) #convertir le dictionnaire en json
        #print(jsonData)
        return jsonData

    def reserverCreneau(self,jour,sport):
        url = "https://u-sport.univ-nantes.fr/api/extended/reservation-creneaux?idPeriode="+self.periodId
        
        activityId = self.getActivitieId(sport)

        jsonData = self.createJson(activityId,jour)
        #print(jsonData)

        if jsonData is None:
            return {"error":"Aucun creneau trouvé pour le jour : "+jour}

        headers = {
            "Cookie": "accessToken="+self.ACCESS_TOKEN,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0",
        }

        response = requests.post(url, headers=headers, json=json.loads(jsonData))
        
        if response.status_code == 200:
            logging.info("Créneau réservé avec succès")
            return {"success":"Créneau réservé avec succès"}
        else:
            logging.error("Erreur lors de la réservation du créneau" + response.text)
            return {"error":"Erreur lors de la réservation du créneau"}
        
        
        return response.json()