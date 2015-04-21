__author__ = 'vivek'


import StringIO
import nltk
import re
from nltk.corpus import stopwords
from collections import Counter


# Check if the page is valid or not
def test(data):

    try:
        buf = StringIO.StringIO(data)

        line = buf.readline()

        if line.__contains__("200 OK"):
            return True
        else:
            return False
    except Exception as e:
        print "Test Function Error...!!!"
        print e
        return False


# Parse the html page
def parse(data):

    # Tranfer all the words to lower case
    data = data.lower()

    # Skip the html page header and go to <html> tag
    if data.__contains__("<html"):

        index = data.index("<html")
        try:
            page = data[index:]

            # Clean the contents of html page using NLTK
            page_clean = (nltk.clean_html(page)).strip()
            page_data = re.sub(r'[^a-z0-9 ]+', ' ', page_clean)

            dictionary = {}

            # Create the dictionary of words for each and every pages
            dictionary = Counter(page_data.split(' '))
            dictionary = dict(dictionary.viewitems())
            if '' in dictionary:
                del dictionary['']

            return dictionary

        except Exception as e:
            print e
            return {}
    else:
        return {}