# Program som henter ned data fra API'et til Den kulturelle skolesekken (DKS)
# Data hentes fra API i JSON-format og konverteres og lagres som en CSV-fil

# Importerer nødvendige bibliotek

import json
import csv
import requests
import pprint as pp

# Liste med endepunkt som er tilgjengelig i API'et
endepunkt = [
    "https://portal.denkulturelleskolesekken.no/public/events/findByTourId",
    "https://portal.denkulturelleskolesekken.no/public/productions",
    "https://portal.denkulturelleskolesekken.no/public/tours",
    "https://portal.denkulturelleskolesekken.no/public/events/findBySchool",
    "https://portal.denkulturelleskolesekken.no/public/productions/findById"
]

# Standardparameter som sendes med til API'et
parameter = {
    "page": 1,
    "pageSize": 50
}

# Løkke som skriver ut hjelpetekst med informasjon om endepunktenes innhold
i = 0 # Løpenummer til utskrift
for d in endepunkt:
	print(i, " - ", d.split('/')[-1])
	i = i + 1

# Brukerinput
endepunkt_nr = int(input("Hva slags data vil du hente ned? "))

if endepunkt_nr == 0:
	parameter["tourId"] = int(input("Tast inn turneId: "))
elif endepunkt_nr == 3:
	parameter["orgNumber"] = int(input("Tast inn skolens orgnummer: "))
elif endepunkt_nr == 4:
    parameter["productionId"] = int(input("Tast inn produksjonsId: "))	

# Henting av data fra DKS på JSON-format
respons = requests.get(endepunkt[endepunkt_nr], params=parameter).json()
data = []
while len(respons) > 0:
    for e in respons:
        data.append(e)    
    parameter['page'] += 1
    respons = requests.get(endepunkt[endepunkt_nr], params=parameter).json()
    print("Henter data fra side: ", parameter['page'])

# pp.pprint(data) # Skriver ut testdata

# Konverterer og skriver data til CSV-fil
data_file = open('DKS_datafil.csv', 'w', encoding="utf-8", newline='')

csv_writer = csv.writer(data_file)

# Teller for å holde styr på headers i CSV-fila
count = 0

for row in data:
	# Skriver overskriftene
	if count == 0:
		header = row.keys()
		csv_writer.writerow(header)
		count += 1
    # Skriver data linje for linje
	csv_writer.writerow(row.values())
data_file.close()

print("Ferdig!")