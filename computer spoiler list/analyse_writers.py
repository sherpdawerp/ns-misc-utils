""" https://www.nationstates.net/page=boneyard/nation=The_Marsupial_Illuminati
https://www.nationstates.net/page=boneyard/nation=Helaw
https://www.nationstates.net/page=boneyard/nation=Kandarin
https://www.nationstates.net/page=boneyard/nation=Golgothastan
https://www.nationstates.net/page=boneyard/nation=Candlewhisper_Archive
https://www.nationstates.net/page=boneyard/nation=Zwangzug
https://www.nationstates.net/page=boneyard/nation=The_Most_Glorious_Hack
https://www.nationstates.net/page=boneyard/nation=The_Grim_Reaper
https://www.nationstates.net/page=boneyard/nation=Maxtopia
https://www.nationstates.net/page=boneyard/nation=Maurepas
https://www.nationstates.net/page=boneyard/nation=Dustistan
https://www.nationstates.net/page=boneyard/nation=Myrth
https://www.nationstates.net/page=boneyard/nation=Ransium
https://www.nationstates.net/page=boneyard/nation=Frieden-und_Freudenland
https://www.nationstates.net/page=boneyard/nation=Wyethalania
https://www.nationstates.net/page=boneyard/nation=Lenyo
https://www.nationstates.net/page=boneyard/nation=Frisbeeteria
https://www.nationstates.net/page=boneyard/nation=Caracasus
https://www.nationstates.net/page=boneyard/nation=Sirocco
https://www.nationstates.net/page=boneyard/nation=Pogaria
https://www.nationstates.net/page=boneyard/nation=Sleep
https://www.nationstates.net/page=boneyard/nation=USS_Monitor
https://www.nationstates.net/page=boneyard/nation=Sedgistan
https://www.nationstates.net/page=boneyard/nation=Responsible
https://www.nationstates.net/page=boneyard/nation=Raurosia
https://www.nationstates.net/page=boneyard/nation=GMC_Military_Arms
https://www.nationstates.net/page=boneyard/nation=The_SLAGLands
https://www.nationstates.net/page=boneyard/nation=SalusaSecondus
https://www.nationstates.net/page=boneyard/nation=Drasnia
https://www.nationstates.net/page=boneyard/nation=Euroslavia
https://www.nationstates.net/page=boneyard/nation=The_Free_Joy_State
https://www.nationstates.net/page=boneyard/nation=Altmer_Dominion
https://www.nationstates.net/page=boneyard/nation=Tactical_Grace
https://www.nationstates.net/page=boneyard/nation=Kryozerkia
https://www.nationstates.net/page=boneyard/nation=Baggieland
https://www.nationstates.net/page=boneyard/nation=Melkor_Unchained
https://www.nationstates.net/page=boneyard/nation=Glen-Rhodes
https://www.nationstates.net/page=boneyard/nation=Luna_Amore
https://www.nationstates.net/page=boneyard/nation=Scolopendra
https://www.nationstates.net/page=boneyard/nation=Enodia
https://www.nationstates.net/page=boneyard/nation=Reploid_Productions
https://www.nationstates.net/page=boneyard/nation=Nation_of_Quebec
https://www.nationstates.net/page=boneyard/nation=Gnejs
https://www.nationstates.net/page=boneyard/nation=Sanctaria
https://www.nationstates.net/page=boneyard/nation=Logophilia_Lyricalia
"""
import json

with open("./issues_list.json", "r") as file:
	big_fat_data_set_of_words = json.load(file)

rankings = {}
SUFFIXES = {1: 'st', 2: 'nd', 3: 'rd'}

known_puppets = {"[i]chan island[/i]": ["chan island", "annihilators of chan island", "[i]chan island[/i]"],
				 "[i]unibot[/i]": ["unibot", "unibot ii", "unibot iii", "[i]unibot[/i]"],
				 "[i]drasnia[/i]": ["drasnia", "dwasnia", "[i]drasnia[/i]"],
				 "[i]sedgistan[/i]": ["sedgistan", "sedgelight sparkle", "[i]sedgistan[/i]"]}


def placing(num):
	if 10 <= num <= 20:
		suffix = 'th'
	else:
		suffix = SUFFIXES.get(num % 10, 'th')
	return str(num) + suffix


for issue_num in big_fat_data_set_of_words["issues"]:
	issue = big_fat_data_set_of_words["issues"][issue_num]

	if __debug__:
		authors = issue["writers"]["authors"]
	else:
		authors = issue["writers"]["editors"]
	
	if "&" in authors:
		authors = authors.replace(" & ", "*")
	if ";" in authors:
		authors = authors.replace("; ", "*")
	if "," in authors:
		authors = authors.replace(", ", "*")
		authors = authors.replace(",", "*")
	if " and " in authors:
		authors = authors.replace(" and ", "*")
	
	authors = [x for x in authors.split("*") if x != ""]

	for author in authors:
		author_fixed = author.lower()

		if __debug__:
			for player in known_puppets:
				if author_fixed in known_puppets[player]:
					author_fixed = player

		if author_fixed in rankings.keys():
			rankings.update({author_fixed: rankings[author_fixed]+1})
		else:
			rankings.update({author_fixed: 1})

sorted_rankings = {k: v for k, v in list(reversed(sorted(rankings.items(), key=lambda item: item[1])))}

place = 0
last_ranking = 0
sum = 0

for element in sorted_rankings:
	current_ranking = sorted_rankings[element]

	if current_ranking != last_ranking:
		place += 1

	if __debug__:
		for player in known_puppets:
			if element in known_puppets[player]:
				output = element + ": " + str(current_ranking) + " (" + placing(place) + ") - " + str(known_puppets[player][:-1])
				break
			else:
				output = element + ": " + str(current_ranking) + " (" + placing(place) + ")"
	else:
		output = element + ": " + str(current_ranking) + " (" + placing(place) + ")"

	sum += current_ranking
	print(output)
	last_ranking = current_ranking
print(sum)
