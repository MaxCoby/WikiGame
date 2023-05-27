from bs4 import BeautifulSoup
import re
import requests
import time


""" Project Primus!
    Implement a bot that will intelligently find a Wikipedia link ladder
    between two given pages. You will be graded on both finding the shortest
    path (or one of them, if there are several of equal length), and how fast
    your code runs.
"""
__author__ = "Max Chou"


def getChildren(wikiPage):
    """ This function returns the Wikipedia links (as a /wiki/)
        that can accessed from the given wikipedia page.
        Uses requests
    """

    links = []
    wikiURL = "https://en.wikipedia.org" + wikiPage
    html = requests.get(wikiURL).text
    bsObj = BeautifulSoup(html, "html.parser")
    linkList = bsObj.find("div", {"id": "bodyContent"}).findAll("a", {"href": re.compile("^\/wiki\/[^:]*$")})
    for link in linkList:
        links.append(link.get("href"))

    return links


def BFS(start, end):
    """ This function implements a breadth first search to return
        a list of the Wikipedia links (as page titles) that
        one could follow to get from the startPage to the endPage.
        This function also tests for invalid starting or ending
        Wikipedia pages and returns which of them is invalid.
        The returned list includes both the start and end pages.
        Uses requests
    """
    pagesFound = set()
    startLink = "/wiki/" + start
    endLink = "/wiki/" + end

    # checking for invalid links using requests
    startLinkValid = requests.get("https://en.wikipedia.org" + startLink).status_code
    endLinkValid = requests.get("https://en.wikipedia.org" + endLink).status_code

    if startLinkValid == 404 and endLinkValid == 404:
        return "Starting and Ending Pages Invalid"
    elif startLinkValid == 404:
        return "Starting Page Invalid"
    elif endLinkValid == 404:
        return "Ending Page Invalid"

    # quick test if the starting page is the same as the ending page
    if start == end:
        return [start]

    queue = [(startLink, [startLink])]
    while queue.__len__() > 0:
        (parent, path) = queue.pop(0)
        pages = getChildren(parent)

        for page in pages:
            # making sure not to visit repeat pages using a set
            if not page in pagesFound:
                pagesFound.add(page)
                # using .lower() to bypass case sensitivity issues
                if page.lower() != endLink.lower():
                    queue.append((page, path + [page]))
                else:
                    listOfLinks = path + [endLink]
                    return [link.replace("/wiki/", "") for link in listOfLinks]


def wikiladder(startPage, endPage):
    """ This function returns a list of the Wikipedia links (as page titles)
        that one could follow to get from the startPage to the endPage.
        The returned list includes both the start and end pages.
    """

    # using try and except to either print error message or fastest path message
    path = BFS(startPage, endPage)
    try:
        # will be a string if error
        print("Error: " + path)
    except:
        # will be a list if path is found
        print("The fastest path from " + startPage + " to " + endPage + " is: " + str(path))


if __name__ == '__main__':
# put your test code here
    start_time = time.time()
    wikiladder("Michael Jordan", "Nintendo")
    print ("My program took", time.time() - start_time, "seconds to run")