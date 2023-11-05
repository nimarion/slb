import json
import re
from bs4 import BeautifulSoup
import traceback
import csv

class PerformanceEntry:
    def __init__(self):
        self.agegroup = ""
        self.birthyear = 0
        self.club = ""
        self.date = ""
        self.discipline = ""
        self.location = ""
        self.firstname = ""
        self.lastname = ""
        self.athleteId = 0
        self.place = 0
        self.result = ""
        self.isTeam = False

class LadvBestenliste:
    def __init__(self):
        self.performanceEntries = []
        self.teamResultNamePattern = re.compile(r'.*?([a-zA-Z].*)')
        self.analyse("raw/2023//M.html", "M")
        self.analyse("raw/2023//W.html", "F")
        self.analyse("raw/2023//M12.html", "M12")
        self.analyse("raw/2023//W12.html", "W12")
        self.analyse("raw/2023//M13.html", "M13")
        self.analyse("raw/2023//W13.html", "W13")
        self.analyse("raw/2023//M14.html", "M14")
        self.analyse("raw/2023//W14.html", "W14")
        self.analyse("raw/2023//M15.html", "M15")
        self.analyse("raw/2023//W15.html", "W15")
        self.analyse("raw/2023//MJU18.html", "MU18")
        self.analyse("raw/2023//WJU18.html", "WU18")
        self.analyse("raw/2023//MJU20.html", "MU20")
        self.analyse("raw/2023//WJU20.html", "WU20")
        self.analyse("raw/2023//MJU16.html", "M15")
        self.analyse("raw/2023//WJU16.html", "W15")
        self.analyse("raw/2023//MJU14.html", "M13")
        self.analyse("raw/2023//WJU14.html", "W13")
        self.updateTeamPerformances()
        print("Found " + str(len(self.performanceEntries)) + " entries")
       # Create a function to generate a unique key for an entry based on specific attributes
        def generate_entry_key(entry):
            key = f"{entry.agegroup}{entry.discipline}{entry.firstname}{entry.lastname}{entry.birthyear}{entry.club}{entry.result}"
            return key

        print("Found " + str(len(self.performanceEntries)) + " entries")

        # Use a dictionary to filter duplicates based on the generated key
        unique_entries_dict = {generate_entry_key(entry): entry for entry in self.performanceEntries}

        # Convert the dictionary back to a list to get the unique entries
        self.performanceEntries = list(unique_entries_dict.values())

        print("Found " + str(len(self.performanceEntries)) + " entries after filtering duplicates")

        self.write_to_csv("data/2023.csv")

    def analyse(self, filename, agegroup):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
            soup = BeautifulSoup(content, 'html.parser')
            elements = soup.select('html body main div div div:nth-of-type(1) div:nth-of-type(4) > *')
            currentDiscipline = ""
            for element in elements:
                if element.name == 'h4':
                    currentDiscipline = element.get_text()
                    continue
                results = element.find_all(recursive=False)
                for resultElement in results:
                    if(len(resultElement.select('.col-1')) == 0):
                        continue
                    place = int(resultElement.select('.col-1')[0].get_text())
                    result = resultElement.select('.col-2 .col-12.text-right')[0].get_text().replace('\t', '').replace('\n', '').replace('\r', '').strip()
                    name = resultElement.select('.col-5 .col-12')[0].get_text().replace('\t', '').replace('\n', '').replace('\r', '').strip()
                    club = resultElement.select('.col-5 .col-12')[1].get_text().replace('\t', '').replace('\n', '').replace('\r', '').strip()
                    location = resultElement.select('.col-4 .col-12')[0].get_text().replace('\t', '').replace('\n', '').replace('\r', '').strip()
                    date = resultElement.select('.col-4 .col-12')[1].get_text().replace('\t', '').replace('\n', '').replace('\r', '').strip()
                    singleResult = bool(re.search(r'\(\d{4}\)', name))
                    yob = 0
                    athleteIds = []
                    firstnames = []
                    lastnames = []
                    birthyears = []
                    if singleResult:
                        yob = int(re.search(r'\((\d{4})\)', name).group(1))
                        name = name.rsplit(' (', 1)[0]
                        athleteId = resultElement.select('.col-5 .col-12 a')[0]['href'].split('#')[1]
                        athleteIds.append(int(athleteId))
                    else:
                        athleteLinks = resultElement.select('.col-5 .col-12 a')
                        for athleteLink in athleteLinks:
                            athleteId = athleteLink['href'].split('#')[1]
                            athleteIds.append(int(athleteId))

                        #print(resultElement)
                        teamMembers = resultElement.select('.col-5 .col-12.text-wrap')[0].get_text().split(',')
                        if len(athleteIds) != len(teamMembers):
                            print("AthleteIds: " + str(len(athleteIds)))
                            print("TeamMembers: " + str(len(teamMembers)))
                            print("TeamMembers: " + str(teamMembers))
                            exit(-1)
                        for teamMember in teamMembers:
                            match = re.search(r'[a-zA-Z].*', teamMember)
                            if match:
                                teamMember = match.group(0)
                                firstname, rest = teamMember.split('.')
                                lastname = rest[:-4]
                                firstnames.append(firstname.strip() + ".")
                                lastnames.append(lastname.strip())
                                birthyears.append(int(rest[-4:]))
                            else:
                                print("^no match: " + teamMember)
                                exit(-1)
                        club = name
                        name = None

                    for i in range(len(athleteIds)):
                        id = athleteIds[i]
                        performanceEntry = PerformanceEntry()
                        performanceEntry.agegroup = agegroup
                        performanceEntry.birthyear = yob
                        performanceEntry.club = club
                        # check if date is in format dd.mm.yyyy
                        if re.match(r'\d{2}\.\d{2}\.\d{4}', date):
                            performanceEntry.date = date
                        # check if date is in format 01.07./02.07.2023
                        elif re.match(r'\d{2}\.\d{2}\./\d{2}\.\d{2}\.\d{4}', date):
                            # take the first date + year
                            performanceEntry.date = date[:5] + date[-5:]
                            print("Date: " + date + " -> " + performanceEntry.date)
                        
                        if performanceEntry.date == "":
                            print("Wrong Date: " + date + " -> " + performanceEntry.date)
                            exit(-1)

                        performanceEntry.discipline = currentDiscipline
                        performanceEntry.location = location
                        if name is not None:
                            firstname = name.split(" ")[0]
                            performanceEntry.firstname = firstname
                            performanceEntry.lastname = name[len(firstname) + 1:]
                        else:
                            performanceEntry.firstname = firstnames[i]
                            performanceEntry.lastname = lastnames[i]
                            performanceEntry.birthyear = birthyears[i]
                        performanceEntry.lastname = performanceEntry.lastname.strip()
                        performanceEntry.firstname = performanceEntry.firstname.strip()
                        performanceEntry.athleteId = id
                        performanceEntry.place = place
                        performanceEntry.result = result
                        performanceEntry.isTeam = False
                        if len(athleteIds) > 1:
                            performanceEntry.isTeam = True
                       # print(performanceEntry.__dict__)
                        self.performanceEntries.append(performanceEntry)
        except Exception as e:
            print(traceback.format_exc())

    def updateTeamPerformances(self):
        for teamEntry in filter(lambda entry: entry.isTeam, self.performanceEntries):
            singleEntry = self.getSingleEntryById(teamEntry.athleteId)
            if singleEntry:
                teamEntry.birthyear = singleEntry.birthyear
                teamEntry.firstname = singleEntry.firstname
                teamEntry.lastname = singleEntry.lastname

    def getSingleEntryById(self, id):
        return next((entry for entry in self.performanceEntries if entry.athleteId == id and not entry.isTeam), None)

    def write_to_json(self, filename):
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump([entry.__dict__ for entry in self.performanceEntries], file, ensure_ascii=False, indent=4)
    
    def write_to_csv(self, filename):
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write the header row
            writer.writerow([
                "club",
                "discipline",
                "firstname",
                "lastname",
                "birthyear",
                "result",
                "ageGroup",
                "date",
                "location",
                "place",
                "teamResult",
                "athleteId"
            ])
            
            # Write the data rows
            for entry in self.performanceEntries:
                writer.writerow([
                    entry.club,
                    entry.discipline,
                    entry.firstname,
                    entry.lastname,
                    entry.birthyear,
                    entry.result,
                    entry.agegroup,
                    entry.date,
                    entry.location,
                    entry.place,
                    entry.isTeam,
                    entry.athleteId
                ])

if __name__ == "__main__":
    LadvBestenliste()
