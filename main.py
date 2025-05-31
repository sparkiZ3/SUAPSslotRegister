import time
import locale
from suapsAPI import SuapsAPI


#define the API
api = SuapsAPI()

#recuperation du jour de la semaine actuel
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
jour_actuel = time.strftime("%A", time.localtime())

#définition du sport souhaité
sport = "Tennis"

print(api.reserverCreneau(jour_actuel,sport))

print(api.getActivitiesName())