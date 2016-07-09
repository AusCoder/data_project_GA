from bs4 import BeautifulSoup
import requests
import lxml
import random



"""
get mathematicians name
"""
def getName(soup):
    return soup.find("h2").text.strip().replace(',','')

"""
get the advisors of the mathematician
"""
def getAdvisors(soup):
    for x in soup.findAll("p"):
        if "Advisor" in x.text:
            return ';'.join([y.text.replace(',','') for y in x.findAll('a')])


"""
get the thesis thesisTitle
"""
def getThesisTitle(soup):
    return soup.find('span', id='thesisTitle').text.strip().replace(',', '')

"""
get year and university of the dissertation
"""
def getUniversity(soup):
    for x in soup.findAll('span'):
        if 'Ph.D.' in x.text:
            return ' '.join(x.text.split()[1:-1]).replace(',', '')
        elif 'Dr. phil.' in x.text:
            return ' '.join(x.text.split()[2:-1]).replace(',', '')
    return ''

"""
get the dissertation year
"""
def getYear(soup):
    try:
        for x in soup.findAll('span'):
            if 'Ph.D.' in x.text or 'Dr. phil.' in x.text:
                return x.text.split()[-1].replace(',', '')
    except IndexError:
        return ''

"""
get the country where the mathematician did their dissertation
"""
def getCountry(soup):
    try:
        return [x['title'].replace(',', '') for x in soup.findAll('img') if 'img/flags' in x['src']][0]
    except IndexError:
        return ''

"""
get number of students and descendants from the soup
"""
def numStudentsAndDescendants(soup):
    try:
        line = [x.text for x in soup.findAll('p') if 'According to our current on-line database' in x.text][0].strip('.').split()
        students = -1
        descendants = -1
        for i in range(len(line)-1):
            if line[i].isdigit() and 'students' in line[i+1]:
                students = int(line[i])
            if line[i].isdigit() and 'descendants' in line[i+1]:
                descendants = int(line[i])
        return students, descendants

    except IndexError:
        return 0,0

"""
method to check page is a valid mathematican's page
"""
def isValidPage(soup):
    for x in soup.findAll("p"):
        if "You have specified an ID that does not exist in the database" in x.text:
            return False
    return True


"""
main method: gets webpage, calls various scraping functions and writes output to a csv file
"""
def main():
    outlines = []
    base_url = "http://www.genealogy.ams.org/id.php?id="
    outFileName = "test.csv"
    colNames = ['mathId', 'name', 'advisors', 'thesis', 'thesisUniversity', 'thesisCountry', 'thesisYear', 'numStudents', 'numDescendants' ]

    print("starting scraping math genealogy project")
    print("please don't block my IP")

    for i in range(100,120):
        an_id = str(i)
        print("scraping id: ", an_id)

        response = requests.get(base_url + an_id)

        if (response.status_code == 200):
            soup = BeautifulSoup(response.text, 'lxml')
        else:
            print("bad response for id: " + an_id)
            continue
        if not isValidPage(soup):
            print("bad page for id: " + an_id)
            continue

        numStud, numDes = numStudentsAndDescendants(soup)
        comb = an_id+',' + getName(soup) + ','+ getAdvisors(soup) +','+ getThesisTitle(soup) + ',' + getUniversity(soup) +',' + getCountry(soup) + ',' + getYear(soup) + ',' + str(numStud) + ',' + str(numDes)
        outlines.append(comb)

    print("writing to file: " + outFileName)
    with open(outFileName, "w") as outFile:
        outFile.write(','.join(colNames) + '\n')
        outFile.writelines([line+'\n' for line in outlines])


if __name__ == "__main__":
    main()
