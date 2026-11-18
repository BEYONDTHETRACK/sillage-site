#!/usr/bin/env python3
"""Fabrique en/index.html (version anglaise de l'accueil) à partir de index.html.

Usage : python3 tools/build_en.py
Les textes sont remplacés à l'identique : un texte français absent du
dictionnaire reste en français (la liste est affichée à la fin).
"""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / 'index.html'
DST = ROOT / 'en' / 'index.html'

# Textes visibles et attributs (texte exact, espaces ramenés à un seul)
TXT = {
"Carte": "Map",
"Carte · les points utiles des cyclistes": "Map · the places cyclists need",
"De l'eau, un ravito, un abri. Là où tu roules.": "Water, food, shelter. Wherever you ride.",
"Fontaines, boulangeries, épiceries, bivouacs, abris, cafés, ateliers vélo, prises pour recharger : plus d'un million de points en France, et l'Europe en route. Les cyclistes en ajoutent, les vérifient et laissent leurs avis. Même sans réseau, ils restent sur ton téléphone.":
  "Water fountains, bakeries, grocery shops, bivouac spots, shelters, cafés, bike repair shops, charging points: over a million points in France, with the rest of Europe on its way. Cyclists add them, check them and leave reviews. Even with no signal, they stay on your phone.",
"Carte autour du lac d'Annecy avec les points utiles : fontaines, boulangeries, épiceries, bivouacs, abris, cafés, atelier vélo et recharge ; une fontaine à Bluffy est sélectionnée, vérifiée par les cyclistes":
  "Map around Lake Annecy with useful places: water fountains, bakeries, grocery shops, bivouac spots, shelters, cafés, a bike repair shop and a charging point; a fountain in Bluffy is selected, verified by cyclists",
"Eau": "Water", "Pain": "Bakery", "Épicerie": "Shop", "Bivouac": "Camp", "Abri": "Shelter", "Café": "Café", "Atelier": "Repair", "Recharge": "Charge",
"+ Ajouter": "+ Add",
"© contributeurs OpenStreetMap · CyclOSM": "© OpenStreetMap contributors · CyclOSM",
"Fontaine du village": "Village fountain",
"Eau potable · Bluffy · à 40 m de ta trace": "Drinking water · Bluffy · 40 m from your route",
"Vérifié par les cyclistes": "Verified by cyclists",
"Toujours là ?": "Still there?",
"Oui, ça coule": "Yes, it flows",
"Non, à sec": "No, dry",
"5 étoiles sur 5": "5 stars out of 5",
"4 étoiles sur 5": "4 stars out of 5",
"Eau fraîche et bon débit, parfait avant la montée vers Thônes.": "Cool water and a good flow, perfect before the climb to Thônes.",
"Un·e cycliste · il y a 3 jours": "A cyclist · 3 days ago",
"Coupée l’hiver : elle coule d’avril à octobre.": "Turned off in winter: it flows from April to October.",
"Un·e cycliste · il y a 2 semaines": "A cyclist · 2 weeks ago",
"Y aller": "Go there",
"Laisser un avis": "Leave a review",
"Illustration · en pointillés : points OpenStreetMap · en plein : ajoutés par les cyclistes · cerclé d’or : nouveau, en cours de validation":
  "Illustration · dotted: OpenStreetMap points · solid: added by cyclists · gold ring: new, awaiting review",
"Ajoute tes bons coins": "Add your favourite spots",
"Une fontaine qui coule, un abri pour la nuit : pose le point, une photo, un avis. Il est visible tout de suite.": "A fountain that flows, a shelter for the night: drop the point, a photo, a review. It shows up straight away.",
"« Toujours là ? » : chacun confirme en un geste. Un point qui a disparu ne t'envoie plus au mauvais endroit.": "“Still there?”: anyone can confirm with one tap. A place that's gone no longer sends you the wrong way.",
"Même sans réseau": "Even with no signal",
"Télécharge les points d'un pays avant de partir. Ton ultra traverse la frontière ? Sillage te prévient.": "Download a country's points before you leave. Your ultra crosses a border? Sillage lets you know.",
"Un appui, et Plans, Google Maps ou Waze te guide jusqu'au point. Ta position et la boussole sont sur la carte.": "With one tap, Apple Maps, Google Maps or Waze will guide you there. Your position and the compass are on the map.",
"Sillage — la météo sur ta trace": "Sillage — the weather along your route",
"Sillage, l'app vélo qui te donne la météo sur ta trace GPX : vent, pluie, température, et la meilleure heure pour partir.":
  "Sillage, the cycling app that gives you the weather along your GPX route: wind, rain, temperature, and the best time to set off.",
"Navigation principale": "Main navigation",
"L'app": "The app",
"Sortie": "Ride",
"Modèles météo": "Weather models",
"Me prévenir": "Notify me",
"App vélo · iPhone et Android": "Cycling app · iOS and Android",
"La météo sur ta trace.": "The weather along your route.",
"Importe ton GPX. Sillage te dit quel temps tu auras, kilomètre par kilomètre, et à quelle heure partir pour garder le vent dans le dos.":
  "Import your GPX. Sillage tells you what weather you'll encounter, kilometre by kilometre, and when to set off to make the most of a tailwind.",
"Télécharger sur": "Download on the",
"l'App Store": "App Store",
"Disponible sur": "Get it on",
"Bientôt disponible": "Coming soon",
"Bientôt dispo": "Coming soon",
"Vue satellite de la boucle Annecy, rive est du lac, Thônes, col du Marais, Faverges et rive ouest : la météo défile heure par heure, de 6 h à 17 h":
  "Satellite view of the Annecy loop: east shore of the lake, Thônes, Col du Marais, Faverges and the west shore. The weather plays out hour by hour, from 6 am to 5 pm",
"Lac d'Annecy": "Lake Annecy",
"Orthophoto © IGN · Licence ouverte": "Orthophoto © IGN · Open Licence",
"Sillage · la veille, 20:00": "Sillage · the evening before, 20:00",
"Demain 09:00 · Col du Marais": "Tomorrow 09:00 · Col du Marais",
"Beau au départ, mais orage au col vers 11 h. Pars à 15 h : soleil et vent dans le dos.":
  "Clear skies at the start, but storms expected on the pass around 11 am. Leave at 3 pm: sunshine and a tailwind.",
"Départ": "Start",
"· Col du Marais · 64,7 km": "· Col du Marais · 64.7 km",
"Source :": "Source:",
", le plus précis ici": ", the most accurate here",
"Heure de départ": "Start time",
"Dans l'app": "In the app",
"Ta trace, ta météo. Voilà ce que tu vois.": "Your route, your weather. Here's what you see.",
"Col du Marais · 64,7 km": "Col du Marais · 64.7 km",
"Dim. 13:00": "Sun 13:00",
"Vent dans le dos le long du lac": "Tailwind along the lake",
"13:00 → 15:48 · 2 h 48 de selle": "13:00 → 15:48 · 2 h 48 in the saddle",
"↑ Rafales 32 km/h": "↑ Gusts 32 km/h",
"à la montée du col": "on the climb to the pass",
"11 → 15 °C · manchettes pour la descente": "11 → 15 °C · arm warmers for the descent",
"Vue satellite de la boucle Annecy, col du Marais avec flèches de vent": "Satellite view of the Annecy loop and Col du Marais, with wind arrows",
"Pluie": "Rain",
"Vent": "Wind",
"Ressenti": "Feels like",
"KM 64,7": "KM 64.7",
"Partir à 13:00": "Leave at 13:00",
"Sortie · le verdict en une ligne": "Ride · the verdict in one line",
"ULTRA · 5 JOURS": "ULTRA · 5 DAYS",
"Trace de Chasing The Sun, de Strasbourg à la Méditerranée, découpée en quatre jours": "Chasing The Sun route, from Strasbourg to the Mediterranean, split into days",
"J1": "D1", "J2": "D2", "J3": "D3", "J4": "D4", "J5": "D5",
"soleil": "sunny", "nuageux": "cloudy", "pluie": "rain", "éclaircies": "sunny spells",
"Ultra · la trace en journées": "Ultra · the route split into days",
"CHASING THE SUN · PLANNING": "CHASING THE SUN · PLAN",
"5 jours de 226 km": "Five days of 226 km each",
"Arrivée": "Finish",
"MER": "SEA",
"Boulangerie · km 142": "Bakery · km 142",
"↓ ouverte à ton passage (11:20)": "↓ open when you ride by (11:20)",
"Rien à manger": "Nothing to eat",
"du km 498 au km 541 · fais le plein avant": "from km 498 to km 541 · stock up before",
"Nuit J2": "Night D2",
"· coucher 18:12 · lune 64 % · 4 °C au plus froid": "· sunset 18:12 · moon 64% · 4 °C at the coldest",
"Ultra · étapes et ravitos": "Ultra · stages and food stops",
"MES SORTIES · SAMEDI 09:00": "MY RIDES · SATURDAY 09:00",
"Où rouler ce week-end ?": "Where to ride this weekend?",
"Tour du lac Annecy avec Col du Marais": "Lake Annecy loop with Col du Marais",
"64,7 km": "64.7 km",
"· ↓ au sec, vent faible": "· ↓ dry, light wind",
"246,9 km": "246.9 km",
"· ↓ vent de dos au retour": "· ↓ tailwind on the way back",
"Ventoux - face Sud": "Ventoux - south side",
"95,4 km": "95.4 km",
"· → vent de travers ·": "· → crosswind ·",
"Mieux à 14:00": "Better at 14:00",
"Sortie récup'": "Recovery ride",
"115,6 km": "115.6 km",
"↑ rafales 48 km/h": "↑ gusts 48 km/h",
"ULTRA · À PART": "ULTRA · SEPARATE LEADERBOARD",
"Mes sorties · le classement du week-end": "My rides · the weekend ranking",
"Mode Sortie · ta boucle du jour": "Ride mode · today's loop",
"Ta sortie, au bon moment.": "Ride at the right time.",
"La météo de ton parcours, pas celle de ta ville. Tu choisis le jour et l'heure : Sillage simule ta sortie kilomètre par kilomètre, à ta vitesse et avec ton dénivelé, puis compare tous les départs de la journée.":
  "The weather along your route, not in your town. Pick the day and time: Sillage simulates your ride kilometre by kilometre, at your pace and taking elevation gain into account, then compares every start time of the day.",
"Meilleure heure de départ": "Best start time",
"64,7 km · 514 m D+ · 25 km/h sur le plat": "64.7 km · 514 m climbing · 25 km/h on the flat",
"Ton départ · 09:00 → 11:55": "Your start · 09:00 → 11:55",
"Beau au départ, mais l'orage te rattrape au col vers 11 h · 8 mm": "Fine at the start, but the storm catches you on the pass around 11 am · 8 mm",
"Le meilleur · 15:00 → 18:05": "Best time to ride · 15:00 → 18:05",
"Au sec et ensoleillé, vent dans le dos le long du lac": "Dry and sunny, tailwind along the lake",
"au sec": "dry",
"au sec &nbsp;": "dry &nbsp;",
"routes mouillées ou arrivée de nuit": "wet roads or finishing after dark",
"routes mouillées ou arrivée de nuit &nbsp;": "wet roads or finishing after dark &nbsp;",
"orage": "storm",
"Départ 15:00 · toute la sortie sur un profil": "Start 15:00 · the whole ride on one profile",
"Profil du Tour du lac d'Annecy avec le col du Marais, départ 15 h : soleil toute la sortie, col à 832 m au km 29, vent dans le dos sauf une heure de léger vent de face dans la montée":
  "Profile of the Lake Annecy loop with Col du Marais, 3 pm start: sunshine the whole way, pass at 832 m at km 29, tailwind except for one hour of light headwind on the climb",
"face": "head", "dos": "tail",
"64,7": "64.7",
"Relief, ciel heure par heure et vent ressenti :": "Elevation, hourly sky and the wind you feel:",
"de dos": "tailwind",
"vers le bas,": "pointing down,",
"de face": "headwind",
"vers le haut.": "pointing up.",
"Carte météo du parcours": "Route weather map",
"Flèches de vent": "Wind arrows",
"Ciel": "Sky",
"Vent animé": "Animated wind",
"Vent ressenti": "Wind you feel",
"Température": "Temperature",
"Soleil": "Sun",
"Carte du Tour du lac d'Annecy avec le col du Marais, départ 15 h : trace en vert là où le vent pousse dans le dos, en rouille dans la montée vers le col, flèches et pastilles de température et de vent tous les 8 km":
  "Map of the Lake Annecy loop with Col du Marais, 3 pm start: route in green where the wind pushes you, in rust on the climb to the pass, with wind arrows and temperature badges every 8 km",
"© contributeurs OpenStreetMap · CyclOSM": "© OpenStreetMap contributors · CyclOSM",
"Vent à": "Wind at",
"· tu es au km": "· you're at km",
"Mon départ 15:00": "My start 15:00",
"Vent de face": "Headwind",
"Travers ou faible": "Cross or light",
"Vent de dos": "Tailwind",
"Force (km/h)": "Strength (km/h)",
"Export image": "Image export",
"Envoie-la aux ami·es avec qui tu vas rouler.": "Send it to the friends you're riding with.",
"Un bouton, et ta sortie devient une image : la carte, le verdict, les horaires et la météo. Tu la postes dans le groupe, et tout le monde sait à quoi s'attendre.":
  "One tap and your ride becomes an image: the map, the verdict, the times and the weather. Post it in the group chat and everyone knows what to expect.",
"Story 9:16": "Story 9:16",
"Écran 16:9": "Screen 16:9",
"Image complète": "Full image",
"Exemple d'image exportée en story : Tour du lac Annecy avec Col du Marais, belles conditions, au sec, vent dans le dos le long du lac":
  "Example of an image exported as a story: Lake Annecy loop with Col du Marais, great conditions, dry, tailwind along the lake",
"DIM. 15:00": "SUN 15:00",
"64,7 km · 514 m D+ · 15:00 → 18:05": "64.7 km · 514 m climbing · 15:00 → 18:05",
"● Belles conditions": "● Great conditions",
"Au sec, vent dans le dos le long du lac": "Dry, tailwind along the lake",
"dos 64 %": "tail 64%",
"92 %": "92%",
"la météo sur ta trace": "the weather along your route",
"Le vent, tronçon par tronçon": "The wind, section by section",
"Des flèches tout au long de la trace :": "Arrows all along the route:",
"↓ de dos": "↓ tailwind",
"→ de travers": "→ crosswind",
"↑ de face": "↑ headwind",
", avec les rafales en km/h.": ", with gusts in km/h.",
"La bonne tenue": "The right kit",
"Températures et ressenti du départ à l'arrivée, avec un conseil : manchettes, coupe-vent ou gants longs.":
  "Temperature and feels-like from start to finish, with a tip: arm warmers, windproof or long gloves.",
"Des tours de boucle": "Laps of a loop",
"Un circuit de 10 km à enchaîner ? Dis combien de tours et ta pause : Sillage te donne la météo tour par tour.":
  "A 10 km circuit to ride again and again? Say how many laps and how long you stop: Sillage gives you the weather lap by lap.",
"Mes sorties": "My rides",
"Tous tes parcours classés selon la météo du jour : celui qui reste au sec arrive en tête.":
  "All your routes ranked by the day's weather: the one that stays dry comes out on top.",
"L'alerte de la veille": "The night-before alert",
"À 20 h, une notification : le verdict de demain et l'heure à viser.": "At 8 pm, a notification: tomorrow's verdict and the time to aim for.",
"Vent, pluie, soleil, ressenti": "Wind, rain, sun, feels-like",
"Colore la trace selon ce qui compte pour toi aujourd'hui : le vent ressenti, la température, la pluie ou le soleil.":
  "Colour the route by what matters to you today: the wind you feel, the temperature, the rain or the sun.",
"Mode Ultra · bikepacking et longue distance": "Ultra mode · bikepacking and long distance",
"Ton ultra, préparé jour par jour.": "Your ultra, planned one day at a time.",
"Exemple :": "Example:",
", 1 128 km et 10 454 m de dénivelé, de Strasbourg à la Méditerranée par les Vosges, le Jura, l'Ardèche et la Camargue. Tu dis à Sillage combien de jours tu veux rouler : il découpe, prévoit la météo de chaque journée et te dit où manger à l'heure où tu passes. Ici, cinq jours de 226 km, du dimanche 27 septembre au jeudi 1er octobre.":
  ", 1,128 km and 10,454 m of climbing, from Strasbourg to the Mediterranean through the Vosges, the Jura, the Ardèche and the Camargue. Tell Sillage how many days you want to ride: it splits the route, forecasts each day's weather and tells you where to eat at the time you ride by. Here, five days of 226 km, from Sunday 27 September to Thursday 1 October.",
"1 128 km · 10 454 m D+": "1,128 km · 10,454 m climbing",
"1 163 km · 12 971 m D+": "1,163 km · 12,971 m climbing",
"soleil, 6 → 28 °C": "sunny, 6 → 28 °C",
"nuageux, 9 °C au plus frais": "cloudy, 9 °C at the coolest",
"nuageux, 12 → 24 °C": "cloudy, 12 → 24 °C",
"pluie toute la journée, jusqu'à 38 mm/h": "rain all day, up to 38 mm/h",
"averse le matin, puis 26 °C": "morning shower, then 26 °C",
"Plan de Chasing The Sun : le soleil suit la trace de Strasbourg à Argelès-sur-Mer, par le Jura, Genève, la vallée du Rhône et Montpellier":
  "Map of Chasing The Sun: the sun follows the route from Strasbourg to Argelès-sur-Mer, through the Jura, Geneva, the Rhône valley and Montpellier",
"Le planning jour par jour, dans l'app": "Your day-by-day plan, in the app",
"Chasing The Sun · 5 jours · départ dim. 27 sept.": "Chasing The Sun · 5 days · start Sun 27 Sept",
"Choisir la journée": "Choose the day",
"Total : arrivée jeudi 1er octobre à 16 h 01, 1 128 km, 10 454 m de dénivelé, 50 h 09 de pédalage, 6 h 16 de pauses":
  "Total: finish Thursday 1 October at 16:01, 1,128 km, 10,454 m of climbing, 50 h 09 riding, 6 h 16 of stops",
"Une ligne par jour": "One line per day",
": départ, arrivée, km, dénivelé, temps de selle et de pause.": ": start, finish, km, climbing, time in the saddle and stopped.",
"Heure par heure": "Hour by hour",
": le ciel, la flèche du vent et la température sur le relief.": ": the sky, the wind arrow and the temperature over the elevation.",
"La pluie": "The rain",
"en mm par heure : ici, le jour 4 sous l'orage, jusqu'à 38 mm.": "in mm per hour: here, day 4 in the storm, up to 38 mm.",
"La nuit": "The night",
": lever du soleil et éclairement de la lune pour les départs à la frontale.": ": sunrise and moonlight for head-torch starts.",
"Les villes traversées": "The towns you ride through",
", au kilomètre près, pour caler tes ravitos.": ", to the kilometre, to plan your food stops.",
"Des étapes réalistes": "Realistic stages",
"Même distance chaque jour, ou adaptée au terrain pour garder le même temps de selle.": "The same distance each day, or adjusted to the terrain to keep the same time in the saddle.",
"Ton allure, pas une moyenne": "Your pace, not an average",
"Vitesse sur le plat, VAM, arrêts et vent : chaque heure d'arrivée colle à ta façon de rouler.": "Speed on the flat, VAM, stops and wind: every arrival time matches the way you ride.",
"Les ravitos ouverts": "Food stops that are open",
"Boulangeries, épiceries et points d'eau comparés à ton heure de passage.": "Bakeries, grocery shops and water points checked against the time you ride by.",
"La nuit anticipée": "The night, planned ahead",
"Coucher du soleil, lune, température au plus froid : tu sais quoi emporter.": "Sunset, moon, coldest temperature: you know what to pack.",
"Mode Commute · domicile – travail": "Commute mode · home – work",
"Le trajet du travail, sans arriver trempé·e.": "Your ride to work, without arriving soaked.",
"Enregistre ton trajet une fois. Sillage te montre l'aller et le retour de chaque jour, sur deux semaines, et te dit quand décaler ton départ.":
  "Save your commute once. Sillage shows you the ride in and the ride home for every day over two weeks, and tells you when to shift your start time.",
"Ce que l'app te montre": "What the app shows you",
"21,6 km près de Brest · aller 7 h 30 · retour 17 h": "21.6 km near Brest · in at 7:30 · home at 17:00",
"Mode Commute dans Sillage, trajet « Maison ↔ Travail », lundi 26 octobre : aller 7 h 30 → 8 h 25, au sec, beau trajet, ressenti 12 à 14 °C, vent de dos ; retour 17 h → 17 h 59, rafales à 60 km/h. Deux cartes avec la température le long du trajet, puis deux semaines de trajets, une pastille verte, dorée ou rouge pour l'aller et le retour de chaque jour.":
  "Commute mode in Sillage, “Home ↔ Work” route, Monday 26 October: in 7:30 → 8:25, dry, a good ride, feels like 12 to 14 °C, tailwind; home 17:00 → 17:59, gusts of 60 km/h. Two maps with the temperature along the route, then two weeks of commutes, with a green, gold or red dot for each day's ride in and ride home.",
"Export image de l'app, tel quel · météo Météo-France (AROME, ARPEGE) via Open-Meteo · © OpenStreetMap":
  "Image exported from the app, as is (in French) · weather Météo-France (AROME, ARPEGE) via Open-Meteo · © OpenStreetMap",
"Tes horaires, jour par jour": "Your times, day by day",
"Une heure de départ, ou l'heure où tu veux arriver. Le mercredi est différent ? Règle-le.": "A start time, or the time you want to arrive. Wednesdays are different? Set it.",
"Esquiver l'averse": "Dodge the shower",
"Si partir 30 minutes plus tôt te garde au sec, Sillage te le propose.": "If leaving 30 minutes earlier keeps you dry, Sillage suggests it.",
"Ressenti, vent, rafales : gants ou simple maillot, sans ouvrir trois applis.": "Feels-like, wind, gusts: gloves or just a jersey, without opening three apps.",
"L'alerte de 7 h": "The 7 am alert",
"L'aller et le retour résumés avant le petit-déjeuner.": "Your ride in and ride home, summed up before breakfast.",
"Une vingtaine de modèles météo": "About twenty weather models",
"Le bon modèle, là où tu roules.": "The right model, where you ride.",
"Chaque pays a son service météo, avec un modèle taillé pour son territoire. Sillage en réunit une vingtaine et prend tout seul le plus précis là où passe ta trace. Partout ailleurs, et pour les sorties à plus de quelques jours, le centre européen ECMWF prend le relais. Tu préfères choisir ? Tous sont dans le menu, y compris des modèles d'intelligence artificielle.":
  "Every country has its weather service, with a model built for its own territory. Sillage brings together about twenty of them and automatically picks the most accurate one wherever your route goes. Everywhere else, and for rides more than a few days away, the European centre ECMWF takes over. Prefer to choose? They're all in the menu, including AI models.",
"Carte de l'Amérique du Nord à l'Europe : modèles nationaux aux États-Unis, au Canada, en Islande et dans toute l'Europe, ECMWF ailleurs":
  "Map from North America to Europe: national models in the United States, Canada, Iceland and across Europe, ECMWF elsewhere",
"Chaque couleur, c'est un modèle national plus précis que le modèle mondial. Le reste du monde est couvert aussi, par ECMWF et, au Japon, par le modèle de la JMA.":
  "Each colour is a national model, more accurate than the global one. The rest of the world is covered too, by ECMWF and, in Japan, by the JMA model.",
"Zoom sur l'Europe : AROME en France, ICON-CH en Suisse, ICON-2I en Italie, Met Office au Royaume-Uni, KNMI au Benelux, GeoSphere en Autriche, CHMI en Tchéquie, MET Norway en Scandinavie, ICON ailleurs en Europe":
  "Close-up on Europe: AROME in France, ICON-CH in Switzerland, ICON-2I in Italy, Met Office in the UK, KNMI in the Benelux, GeoSphere in Austria, CHMI in Czechia, MET Norway in Scandinavia, ICON elsewhere in Europe",
"Zoom sur l'Europe": "Close-up on Europe",
"Qui prévoit ta météo": "Who forecasts your weather",
"France, Corse": "France, Corsica",
"· DWD, Allemagne": "· DWD, Germany",
"Suisse, Jura, Savoie du Nord": "Switzerland, Jura, northern Savoie",
"Italie, Slovénie": "Italy, Slovenia",
"Autriche, Alpes de l'Est": "Austria, Eastern Alps",
"Tchéquie": "Czechia",
"Royaume-Uni, Irlande": "United Kingdom, Ireland",
"Pays-Bas, Belgique": "Netherlands, Belgium",
"Islande": "Iceland",
"Scandinavie, pays baltes": "Scandinavia, Baltic states",
"États-Unis": "United States",
"· Environnement Canada": "· Environment Canada",
"Japon": "Japan",
"· centre européen": "· European centre",
"partout ailleurs": "everywhere else",
"Lac du Bourget": "Lake Bourget",
"Bientôt sur iPhone et Android": "Coming soon to iOS and Android",
"Ta prochaine sortie mérite le bon départ.": "Your next ride deserves the right start.",
"Laisse ton e-mail : tu seras prévenu·e avant tout le monde de la sortie de Sillage, et tu pourras le tester en avant-première.":
  "Leave your email: you'll hear about Sillage's launch before anyone else, and you'll get to try it early.",
"Boucle col de l'Épine – col du Chat · 58 km · 1 210 m D+": "Col de l'Épine – Col du Chat loop · 58 km · 1,210 m climbing",
"Tu es…": "You are…",
"Je roule": "I ride",
"J'organise des événements": "I organise events",
"Sorties, ultras, commute : on te prévient le jour de la sortie, avec un accès anticipé pour tester l'app.":
  "Rides, ultras, commuting: we'll let you know on launch day, with early access to try the app.",
"Course, brevet, ultra ou sortie de club : Sillage peut donner la météo de ton parcours à tes participant·es. On revient vers toi pour en parler.":
  "Race, brevet, ultra or club ride: Sillage can give your participants the weather on your route. We'll get back to you to talk about it.",
"Prénom": "First name",
"(facultatif)": "(optional)",
"E-mail": "Email",
"toi@exemple.fr": "you@example.com",
"Ton événement ou ton club": "Your event or club",
"Type d'événement": "Type of event",
"Choisis…": "Choose…",
"Brevet / randonnée": "Brevet / audax",
"Cyclosportive / course": "Sportive / race",
"Sorties de club": "Club rides",
"Autre": "Other",
"J'accepte de recevoir les e-mails de Sillage. Désinscription en un clic, à tout moment.": "I agree to receive emails from Sillage. Unsubscribe in one click, at any time.",
"Confidentialité": "Privacy",
"Pas de spam : un e-mail à la sortie, et quelques nouvelles d'ici là.": "No spam: one email at launch, and a little news until then.",
"C'est noté !": "You're on the list!",
"On te prévient avant tout le monde.": "We'll let you know before anyone else.",
"© 2026 Sillage · La météo sur ta trace.": "© 2026 Sillage · The weather along your route.",
"Mentions légales": "Legal notice",
"Gérer mes cookies": "Manage cookies",
}

# Chaînes du script (remplacement littéral)
JS = [
("'Beau au départ, mais l’orage te rattrape au col'", "'Fine at the start, but the storm catches you on the pass'"),
("'Orage vers 11 h'", "'Storm around 11 am'"),
("'Pars à 15 h : soleil et vent dans le dos.'", "'Leave at 3 pm: sunshine and a tailwind.'"),
("'Orage au col du Marais vers 11 h'", "'Storm on Col du Marais around 11 am'"),
("'Reporte : mieux à 15 h.'", "'Wait: better at 3 pm.'"),
("'Orage dès le col de Bluffy'", "'Storm from Col de Bluffy on'"),
("'Ne pars pas : mieux à 15 h.'", "'Don’t go: better at 3 pm.'"),
("'Orage, grêle possible au col'", "'Storm, hail possible on the pass'"),
("'Reste au chaud : mieux à 15 h.'", "'Stay warm indoors: better at 3 pm.'"),
("'L’orage s’éloigne vers 14 h'", "'The storm moves away around 2 pm'"),
("'Les routes resteront mouillées.'", "'The roads will stay wet.'"),
("'Gris, routes mouillées'", "'Grey, wet roads'"),
("'Le soleil revient à 15 h.'", "'The sun is back at 3 pm.'"),
("'Soleil et vent dans le dos le long du lac'", "'Sunshine and a tailwind along the lake'"),
("'Le meilleur créneau de l’après-midi.'", "'The best slot of the afternoon.'"),
("'Soleil, vent dans le dos'", "'Sunshine, tailwind'"),
("'Bon créneau, pense à l’éclairage pour la fin.'", "'Good slot, bring lights for the end.'"),
("'Soleil et vent dans le dos jusqu’au bout'", "'Sunshine and a tailwind all the way'"),
("'Prends l’éclairage pour le retour.'", "'Bring lights for the way back.'"),
("'↑ Rafales ", "'↑ Gusts "),
("'Pluie 0,3 mm'", "'Rain 0.3 mm'"),
("'Pluie ", "'Rain "),
("'↓ Vent NO ", "'↓ Wind NW "), ("'↑ Vent SO ", "'↑ Wind SW "), ("'→ Vent O ", "'→ Wind W "), ("'↓ Vent N ", "'↓ Wind N "),
("{ sun: 'Soleil', part: 'Éclaircies', cloud: 'Gris', rain: 'Pluie', storm: 'Orage' }",
 "{ sun: 'Sunny', part: 'Sunny spells', cloud: 'Grey', rain: 'Rain', storm: 'Storm' }"),
("aria: 'Départ ' + hh.label + ', ' + SKY[hh.sky] + ', ' + hh.t + ' degrés'", "aria: 'Start ' + hh.label + ', ' + SKY[hh.sky] + ', ' + hh.t + ' degrees'"),
("label: 'Jour ' + (i + 1)", "label: 'Day ' + (i + 1)"),
("date: 'dim. 27 sept.', sky: 'soleil'", "date: 'Sun 27 Sept', sky: 'sunny'"),
("date: 'lun. 28 sept.', sky: 'nuageux'", "date: 'Mon 28 Sept', sky: 'cloudy'"),
("date: 'mar. 29 sept.', sky: 'nuageux'", "date: 'Tue 29 Sept', sky: 'cloudy'"),
("date: 'mer. 30 sept.', sky: 'pluie'", "date: 'Wed 30 Sept', sky: 'rain'"),
("date: 'jeu. 1 oct.', sky: 'éclaircies'", "date: 'Thu 1 Oct', sky: 'sunny spells'"),
("'Jour 1, dimanche 27 septembre : départ 6 h, arrivée 17 h 21, km 0 à 226, 2 081 m de dénivelé. Soleil, de 6 à 28 °C, par Gérardmer et Lure.'",
 "'Day 1, Sunday 27 September: start 6:00, finish 17:21, km 0 to 226, 2,081 m of climbing. Sunny, from 6 to 28 °C, via Gérardmer and Lure.'"),
("'Jour 2, lundi 28 septembre : départ 6 h, arrivée 17 h 33, km 226 à 451, 2 346 m de dénivelé. Nuageux, 9 °C au plus frais, par Pontarlier et Valserhône.'",
 "'Day 2, Monday 28 September: start 6:00, finish 17:33, km 226 to 451, 2,346 m of climbing. Cloudy, 9 °C at the coolest, via Pontarlier and Valserhône.'"),
("'Jour 3, mardi 29 septembre : départ 6 h, arrivée 19 h 07, km 451 à 677, 3 032 m de dénivelé. Nuageux, de 12 à 24 °C, par Tournon-sur-Rhône et Le Cheylard.'",
 "'Day 3, Tuesday 29 September: start 6:00, finish 19:07, km 451 to 677, 3,032 m of climbing. Cloudy, from 12 to 24 °C, via Tournon-sur-Rhône and Le Cheylard.'"),
("'Jour 4, mercredi 30 septembre : départ 6 h, arrivée 16 h 20, km 677 à 903, 1 538 m de dénivelé. Pluie toute la journée, jusqu’à 38 mm par heure, par Vallon-Pont-d’Arc et Aigues-Mortes.'",
 "'Day 4, Wednesday 30 September: start 6:00, finish 16:20, km 677 to 903, 1,538 m of climbing. Rain all day, up to 38 mm per hour, via Vallon-Pont-d’Arc and Aigues-Mortes.'"),
("'Jour 5, jeudi 1er octobre : départ 6 h, arrivée 16 h 01, km 903 à 1 128, 1 457 m de dénivelé. Averse le matin puis éclaircies, jusqu’à 26 °C, par Narbonne jusqu’à Canet-en-Roussillon.'",
 "'Day 5, Thursday 1 October: start 6:00, finish 16:01, km 903 to 1,128, 1,457 m of climbing. Morning shower then sunny spells, up to 26 °C, via Narbonne to Canet-en-Roussillon.'"),
("'Indique une adresse e-mail valide.'", "'Please enter a valid email address.'"),
("'Coche la case pour accepter de recevoir nos e-mails.'", "'Tick the box to agree to receive our emails.'"),
("'Envoi…'", "'Sending…'"),
("'On te prévient avant tout le monde, et on revient vers toi pour parler de ton événement.'", "'We’ll let you know before anyone else, and get back to you about your event.'"),
("'On te prévient avant tout le monde, avec un accès pour tester l\\u2019app en avant-première.'", "'We’ll let you know before anyone else, with early access to try the app.'"),
("'L\\u2019inscription n\\u2019est pas passée. Réessaie dans un instant, ou écris-nous à hello@sillage-ride.eu.'",
 "'Your sign-up didn’t go through. Try again in a moment, or email us at hello@sillage-ride.eu.'"),
("btn.textContent = 'Me prévenir'", "btn.textContent = 'Notify me'"),
("consent: true, site: form.site.value", "consent: true, lang: 'en', site: form.site.value"),
]

# Liens et chemins (la page anglaise est dans /en/)
PATHS = [
('href="img/', 'href="/img/'), ('src="img/', 'src="/img/'), ("img: 'img/", "img: '/img/"),
('href="/mentions-legales/"', 'href="/en/legal-notice/"'),
('href="/confidentialite/"', 'href="/en/privacy/"'),
('<html lang="fr">', '<html lang="en">'),
('<option value="fr" selected>FR</option><option value="en">EN</option><option value="de">DE</option><option value="es">ES</option>', '<option value="fr">FR</option><option value="en" selected>EN</option><option value="de">DE</option><option value="es">ES</option>'),
('<a class="sl-lang" href="/en/" hreflang="en" lang="en" aria-label="English version" onclick="try{localStorage.setItem(\'sillage-lang\',\'en\')}catch(e){}">EN</a>',
 '<a class="sl-lang" href="/" hreflang="fr" lang="fr" aria-label="Version française" onclick="try{localStorage.setItem(\'sillage-lang\',\'fr\')}catch(e){}">FR</a>'),

]

ATTRS = ('aria-label', 'alt', 'title', 'placeholder', 'content')


def norm(s):
    return ' '.join(s.split())


def build(TXT=TXT, JS=JS, PATHS=PATHS, DST=DST, FEELS=r"'feels like \1 °C'"):
    h = SRC.read_text()
    missing = set()
    # sépare script/style du reste
    parts = re.split(r'(<script\b[\s\S]*?</script>|<style\b[\s\S]*?</style>)', h)
    out = []
    for p in parts:
        if p.startswith('<script'):
            p = re.sub(r"'(\d+) °C ressenti'", FEELS, p)
            for a, b in JS:
                if a not in p and 'consent.js' not in p and len(p) > 2000:
                    missing.add('JS: ' + a[:60])
                p = p.replace(a, b)
            out.append(p)
            continue
        if p.startswith('<style'):
            out.append(p)
            continue
        def txt(m):
            s = m.group(1)
            k = norm(s)
            if not k:
                return m.group(0)
            if k in TXT:
                lead = s[:len(s) - len(s.lstrip())]
                trail = s[len(s.rstrip()):]
                return '>' + lead + TXT[k] + trail + '<'
            if re.search(r'[a-zà-ÿ]{3}', k) and re.search(r'[éèàùçêâîôû]|\b(le|la|les|de|du|des|et|ton|ta|tes)\b', k):
                missing.add(k)
            return m.group(0)
        p = re.sub(r'>([^<>]+)<', txt, p)
        def att(m):
            k = norm(m.group(2))
            if k in TXT:
                return m.group(1) + '="' + TXT[k] + '"'
            return m.group(0)
        p = re.sub(r'\b(' + '|'.join(ATTRS) + r')="([^"]*)"', att, p)
        out.append(p)
    h = ''.join(out)
    for a, b in PATHS:
        h = h.replace(a, b)
    h = re.sub(r'<script>\n/\* Langue :[\s\S]*?</script>\n', '', h)
    DST.parent.mkdir(exist_ok=True)
    DST.write_text(h)
    for m in sorted(missing):
        print('PAS TRADUIT :', m)
    print('écrit', DST)


if __name__ == '__main__':
    build()
