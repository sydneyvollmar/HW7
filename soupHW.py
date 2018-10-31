# To run this, you need to install BeautifulSoup if you aren't using anaconda
# https://pypi.python.org/pypi/beautifulsoup4

from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import unittest
import re

def getSumSpans(url):
    """ return a sum of all of the text values in the span tags at the passed url

        url -- a uniform resource locator - address for a web page

    """
    html = urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")

    spans = soup.find_all('span')

    total = 0
    for span in spans:
        nums = re.findall('([0-9]+)', span.text)
        for num in nums:
            total += int(num)

    return total


def followLinks(url, numAnchor, numTimes):
    """ Repeat for numTimes. Find the url at numAnchor position (the first link is at position 1) at
        the current url and use that as the new url
        return the text in the a tag from the last url that you process

        url -- a uniform resource locator - address for a web page
        numAnchor -- the position of the anchor (a tag) you are looking at on the page - the first link is position 1
        numTimes -- the number of times to repeat the process of finding the new url
    """

    while numTimes > 0:
        html = urlopen(url).read()
        soup = BeautifulSoup(html, "html.parser")
        linkList = soup.find_all('a')

        anchor = linkList[numAnchor - 1]
        url = anchor.get('href', None)
        numTimes -= 1

    return anchor.text

def getGradeHistogram(url):
    """ return a sorted tuple with the grade range (such as 90, 80, etc) and the number of grades in that range
        url -- a uniform resource locator - address for a web page
    """

    html = urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")

    dictGrades = {90: 0, 80: 0, 70: 0, 60: 0, 50: 0, 40: 0, 30: 0, 20: 0, 10: 0, 0: 0}
    spans = soup.find_all('span')

    for span in spans:
        nums = re.findall('([0-9]+)', span.text)
        for num in nums:
            grade = int(num)
            if grade >= 90 and grade < 100:
                dictGrades[90] += 1
            elif grade >= 80:
                dictGrades[80] += 1
            elif grade >= 70:
                dictGrades[70] += 1
            elif grade >= 60:
                dictGrades[60] += 1
            elif grade >= 50:
                dictGrades[50] += 1
            elif grade >= 40:
                dictGrades[40] += 1
            elif grade >= 30:
                dictGrades[30] += 1
            elif grade >= 20:
                dictGrades[20] += 1
            elif grade >= 10:
                dictGrades[10] += 1
            elif grade >= 0:
                dictGrades[0] += 1

    lstGrades = []
    for elem in dictGrades:
        lstGrades.append((elem, dictGrades[elem]))

    return lstGrades


class TestHW7(unittest.TestCase):

    def test_sumSpan1(self):
        self.assertEqual(getSumSpans("http://py4e-data.dr-chuck.net/comments_42.html"), 2553)

    def test_sumSpan2(self):
        self.assertEqual(getSumSpans("http://py4e-data.dr-chuck.net/comments_132199.html"), 2714)

    def test_followLinks1(self):
        self.assertEqual(followLinks("http://py4e-data.dr-chuck.net/known_by_Fikret.html",3,4), "Anayah")

    def test_followLinks2(self):
        self.assertEqual(followLinks("http://py4e-data.dr-chuck.net/known_by_Charlie.html",18,7), "Shannah")

    def test_getGradeHistogram(self):
        self.assertEqual(getGradeHistogram("http://py4e-data.dr-chuck.net/comments_42.html"), [(90, 4), (80, 4), (70, 7), (60, 7), (50, 6), (40, 3), (30, 5), (20, 4), (10, 6), (0, 4)])


unittest.main(verbosity=2)
