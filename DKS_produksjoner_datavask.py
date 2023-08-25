# Program som henter ned data om produksjoner fra API'et til Den kulturelle skolesekken (DKS)
# Data hentes fra API i JSON-format. Rådataene "vaskes", konverteres og lagres som en CSV-fil
# CC BY SA - VTFK

# Importerer nødvendige bibliotek
import html2text
import csv
import requests

class Production:
    def __init__(self, id, name, description, agemin, agemax, thumbnail, culturalExpressions, hyperlinks, firstLink):
        self.id = id
        self.name = name
        self.description = description
        self.agemin = agemin
        self.agemax = agemax
        self.thumbnail = thumbnail
        self.culturalExpression = culturalExpressions
        self.hyperlinks = hyperlinks
        self.firstLink = firstLink

######## Repacking #############
def repackName(nameRaw):
    repack = nameRaw.replace('\"', '\'')
    return repack

def repackDescription(descriptionRaw):
    preformat = descriptionRaw.replace('&aring;', '\u00E5').replace('&oslash;', '\u00F8').replace('&aelig;', '\u00E6')
    
    html2text.html2text.escape_all = True
    repack = html2text.html2text(preformat).replace('\n',' ').replace('**', '').replace('&laquo;', '«').replace('&raquo;', '»').replace('&ndash;', '-').replace('&nbsp;', ' ').replace('_', '')
    return repack

def repackthumbnail(thumbnailRaw):
    if str(thumbnailRaw)[:4] == "http":
        return thumbnailRaw
    else:
        return

def repackCulturalExpressions(culturalExpressionsRaw):
    return culturalExpressionsRaw[0]["parentId"]

def repackHyperlinks(hyperlinksRaw):
    repack = ""
    if len(hyperlinksRaw) == 0:
        return "Ingen lenker"
    else:
        for link in hyperlinksRaw:
            repack += link["name"] + " - " + link["description"] + " - " + link["url"] + ", "
        return repack[:-2]
    
def repackFirstLink(hyperlinksRaw):
    if len(hyperlinksRaw) != 0:
        if hyperlinksRaw[0]["url"][:4] != "http":
            hyperlinksRaw[0]["url"] = "http://" + hyperlinksRaw[0]["url"] 
        return hyperlinksRaw[0]["url"]

# Endepunkt til DKS-API'et - Henter alle produksjoner
endepunkt = "https://portal.denkulturelleskolesekken.no/public/productions"

# Parameter som sendes med til API'et
parameter = {
    "page": 1,
    "pageSize": 50
}

# Henting av data fra DKS på Objekt-format
# respons = requests.get(endepunkt, params=parameter).json()
data = [Production("id", "Tittel", "Beskrivelse", "Trinn fra", "Trinn til", "Illustrasjon", "Kulturuttrykk", "Lenkebeskrivelser", "Første lenke")]

temp_store = []

respons = requests.get(endepunkt, params=parameter).json()
while len(respons) > 0:
    for e in respons:
        temp_store.append(e)    
    parameter['page'] += 1
    respons = requests.get(endepunkt, params=parameter).json()
    print("Henter data fra side: ", parameter['page'])

for e in temp_store:
    data.append(
        Production(e["id"],
        repackName(e["name"]),
        repackDescription(e["descriptionShort"]),
        e["yearLevelMinimum"],
        e["yearLevelMaximum"],
        repackthumbnail(e["thumbnail"]),
        repackCulturalExpressions(e["culturalExpressions"]),
        repackHyperlinks(e["links"]),
        repackFirstLink(e["links"])
        )
    )

######### Skriving til CSV-fil ###########
# Konverterer og skriver data til CSV-fil
data_file = open('DKS_datafil_vasket_lang.csv', 'w', encoding="utf-8", newline='')
csv_writer = csv.writer(data_file, delimiter=',')

for linje in data:
    csv_writer.writerow([linje.id, linje.name, linje.description, linje.agemin, linje.agemax, linje.thumbnail, linje.culturalExpression, linje.hyperlinks, linje.firstLink])
data_file.close()   
print("Ferdig!")
