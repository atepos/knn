# for region in layout.regions:
#         print(region.polygon)
#         xs, ys = zip(*region.polygon)
#         plt.plot(xs,ys) 
#         print(region.get_region_transcription())
#         plt.text(xs[0], ys[0], region.get_region_transcription())
#     plt.show() 


### USAGE ###
# python3 questionSeparator.py <folder with xmls > <folder with hashed logins (ann/)>


# EXAMPLE:
# python3 questionSeparator.py pero.page_xml.transformer_medium.removed/ ann/

from pero_ocr.document_ocr.layout import PageLayout
import os
import sys
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import regionsA_2022_1 as regions
from shapely.geometry import Polygon
from shapely.affinity import translate
from shapely import Point
import yaml

# Set year, test number and page you want to check. DisplayPage starts at index 1

year = '2022'
group = 'A'
test = '1'
displayPage = 7

#################################################################################

color = ['red', 'green', 'black', 'orange']

currentPageNum = displayPage - 1
currentPerson = 0
saveCurrentPage = False
pagesRegions = {}

transformationMatrix = [0, 0]

# argv1 = folder with xmls
# argv2 = folder with hashed logins
class Person:
    def __init__(self, id, examHashs):
        self.id = id
        self.examHashs = [examHashs]
    def __str__(self):
        return f"<Id:{self.id} Hash:{self.examHashs}>"
    def __repr__(self):
        return f"<Id:{self.id} Hash:{self.examHashs}>"

persons = []

def on_press(event):
    global currentPageNum
    global currentPerson
    global saveCurrentPage
    if event.key == 'n':
        saveCurrentPage = True
        currentPerson += 1
        transformationMatrix[1] = 0
    if event.key == "m":
        currentPerson += 1
        saveCurrentPage = False
    if event.key == '1':
        currentPageNum = 0
    if event.key == '2':
        currentPageNum = 1
    if event.key == '3':
        currentPageNum = 2
    if event.key == '4':
        currentPageNum = 3
    if event.key == '5':
        currentPageNum = 4
    if event.key == '6':
        currentPageNum = 5
    if event.key == '7':
        currentPageNum = 6
    if event.key == "up":
        transformationMatrix[1] = transformationMatrix[1] + 19
    if event.key == "down":
        transformationMatrix[1] = transformationMatrix[1] - 19
    plt.close(event.canvas.figure)

def getPageRegions(layout):
    separatedRegions = [[], [], [], []]
    for region in layout.regions:
        max = 0
        index = 0
        for i in range(0, len(regions.template[currentPageNum])):
            p = Polygon(regions.template[currentPageNum][i])
            p = translate(p, xoff=transformationMatrix[0], yoff=transformationMatrix[1])
            x, y = p.exterior.xy
            plt.plot(x, y, color='grey')
            q = Polygon(region.polygon)
            try:
                area = p.intersection(q).area
            except Exception as e:
                print(e)
                return None
            if area > max:
                max = area
                index = i
        if max > 0:
            separatedRegions[index].append(region.id)
            polygonColor = color[index]
        else: 
            polygonColor = 'yellow'
        xs, ys = zip(*region.polygon)
        plt.plot(xs,ys, color=polygonColor) 
        plt.text(xs[0], ys[0], region.get_region_transcription())
    plt.show() 
    return separatedRegions

def writeRegions(separatedRegions, fileId, personId):
    if fileId not in pagesRegions:
        pagesRegions[fileId] = {
            'year' : year,
            'test' : test,
            'login' : personId,
            'questions': {},
            'answers': {}
        }
    pagesRegions[fileId]['questions'][currentPageNum * 2] = separatedRegions[0]
    pagesRegions[fileId]['questions'][currentPageNum * 2 + 1]= separatedRegions[2]
    pagesRegions[fileId]['answers'][currentPageNum * 2] = separatedRegions[1]
    pagesRegions[fileId]['answers'][currentPageNum * 2 + 1] = separatedRegions[3]
    yaml.dump(pagesRegions, yamlfile, default_flow_style=False)

def personIsFromAnotherGroup(personId, group):
    fileName = "body-{}_{}.txt.uniform.anon".format(year, test)
    filePath = os.path.join(sys.argv[2], fileName)
    with open(filePath) as f:
        for line in f:
            lineSplit = line.split()
            if lineSplit[0] == personId:
                if lineSplit[1][0] != group:
                    # print("Person {} is from another group".format(personId))
                    return True
                else:
                    # print("Person {} is from this group".format(personId))
                    return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 xmlParser.py <file>")
        sys.exit(1)
    print(sys.argv)
    folder = sys.argv[1]
    fileAnnName = "{}_{}.page-login.hashed".format(year, test)
    fileAnn = os.path.join(sys.argv[2], fileAnnName)

    yamlOutputName = year + '_' + test + '_' + str(currentPageNum + 1) + '.yaml'

    #load existing yaml
    try:
        with open(yamlOutputName,'r') as yamlfile:
            pagesRegions = yaml.safe_load(yamlfile)
    except:
        pagesRegions = {}

    with open(fileAnn) as f:
        #find login in file
        for line in f:
            lineSplit = line.split()
            found = False
            if personIsFromAnotherGroup(lineSplit[1], group):
                continue
            for person in persons:
                if person.id == lineSplit[1]:
                    person.examHashs.append(lineSplit[0])
                    found = True
                    break
            if found == False:
                persons.append(Person(lineSplit[1], lineSplit[0]))

    while currentPerson < len(persons):
        findPerson = False
        fileId = ''
        personId = ''
        for file in os.listdir(folder):
            if len(persons[currentPerson].examHashs) < displayPage:
                currentPerson += 1
                continue
            if persons[currentPerson].examHashs[displayPage - 1] in file:
                findPerson = True
                fig, ax = plt.subplots()
                fig.canvas.mpl_connect('key_press_event', on_press)
                layout = PageLayout(file=os.path.join(folder, file))
                separatedRegions = getPageRegions(layout)
                if separatedRegions == None:
                    currentPerson += 1
                    break
                fileId = file
                personId = persons[currentPerson - 1].id 
                print(currentPerson + 1, '/', len(persons))
                break

        if saveCurrentPage:
            with open(yamlOutputName,'w') as yamlfile:
                writeRegions(separatedRegions, fileId, personId)
            saveCurrentPage = False

        if not findPerson:
            currentPerson += 1