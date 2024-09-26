from suapsAPI import SuapsAPI

api = SuapsAPI()

sport = "Tennis"

#api.getCreneaux(activitiy,api.periodId)

print(api.reserverCreneau("Mercredi",sport))