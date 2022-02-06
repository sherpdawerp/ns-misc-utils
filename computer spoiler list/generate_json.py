import json
import requests
import re
import time

BASE_REPO_URL = "https://raw.githubusercontent.com/sherpdawerp/NationStates-Issue-Megathread/master/002%20-%20Issue%20Megalist%20(MAIN)/"
EFFECTS_URL = "http://www.mwq.dds.nl/ns/results/issues.html"

with open("./repo_files.txt", "r") as f:
	filenames = f.read().split("\n")

parsed = {
	"issues": { }
}

for filename in filenames:
	text = requests.get(BASE_REPO_URL+filename).text
	text = re.sub(r"\r\n", "\n", text)
	
	issues = re.split(r"\n[\-]+\n", text)
	
	for issue in issues:
		authors, editors, num, title, desc, backstory = ("", "", "", "", "", "")
		options = {}
		
		s = re.search(r"\[([^\\\[\]]+?)[\;\,\:\.\s]\s{0,1}ed[\;\,\:\.\s]\s{0,2}([^\\\[\]]+?)[\]\[\:]", issue) # search for [author; ed: editor]
		if s is None:
			editors = "Maxtopia"
			
			s = re.search(r"\[([^\\\[\]]*?)\]\[\/b\]", issue) # search for [author][/b] -> (edited by Max)
			if s is None:
				authors = "Maxtopia"
			else:
				authors = s.group(1)
		else:
			authors = s.group(1)
			editors = s.group(2)
		
		issue = re.sub(r"\[(\d+)\]", r"\g<1>", issue) # replace [#] options with just the number
		issue = re.sub(r"\*+(\d+)", r"\g<1>", issue) # replace *# options with just the number
		issue = re.sub(r"\[\[.+?\]\]", "", issue) # remove [[color]validites[/color]]
		issue = re.sub(r"[\[\}].*?[\]\}]", "", issue) # remove [bbcode] and {notes}
		
		s = re.search(r"#(\d+)[\:\;\,][ ](.+?)[\s+]\n", issue); # search for #num: title
		if s is None:
		
			# TODO: fix the regex so this isn't necessary
			if issue.startswith("#1353"):
				continue
			elif issue.startswith("#1502"):
				break
			elif issue.startswith("#1350"):
				continue
			
			print(issue)
			raise RuntimeError()
		else:
			num = s.group(1)
			title = s.group(2)

		s = re.search(r"The [iI]ssue[:]{0,1}[ ]{0,1}\n{1,2}(.+?)[\n]", issue) # search for description
		if s is None:
			print(issue)
			raise RuntimeError()
		else:
			desc = s.group(1)
		
		s = re.search(r"The Story So Far[:]{0,1}[ ]{0,1}\n(.+?)\n", issue) # search for chain backstory
		if s is None:
			backstory = ""
		else:
			backstory = s.group(1)
	
		s = re.finditer(r"\n([0-9]+)\.\s{0,1}(.+)\n", issue) # search for options
		if s is None:
			if re.search(r"The Debate[:]{0,1}[ ]{0,1}\n", issue) is not None: # handle no options
				print(issue)
				raise RuntimeError()
			else:
				options = {}
		else:
			while True:
				try:
					option = next(s)
					
					options[option.group(1)] = {
						"text": option.group(2),
						"effect": ""
					}
				except (StopIteration):
					break
		
		# write to output
		parsed["issues"][num] = {
			"title": title,
			"writers": {
				"authors": authors,
				"editors": editors
			},
			"chain_background": backstory,
			"description": desc,
			"options": options
		}

# effect lines
effects = requests.get(EFFECTS_URL).text
print(effects)

with open("./issues_list.json", "w") as f:
	f.write(str(json.dumps(parsed, indent=4, sort_keys=False)))
