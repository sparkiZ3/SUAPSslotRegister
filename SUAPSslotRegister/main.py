from config import *
import time
import locale
from suapsAPI import SuapsAPI

print(data["API-KEY"])

"""
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
jour_actuel = time.strftime("%A", time.localtime())

print(jour_actuel)


api = SuapsAPI()

sport = "Tennis"

#api.getCreneaux(activitiy,api.periodId)

print(api.reserverCreneau(jour_actuel,sport))"""