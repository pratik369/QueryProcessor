__author__ = 'Vivek & Pratik'

import GetBM25
import heapq
import time
from nltk.corpus import stopwords
from struct import unpack



class QueryProcessor:
    lex_file_pt = ''
    url_file_pt = ''
    lex_data = ''
    url_data = ''
    totaldocssize = 0
    urldata = {}
    lexdicondictionary = {}
    cachedictionary = {}
    decodedictionary = {}
    avgd = 0.0

    def __init__(self):
        self.lex_file_pt = open("/Users/vivek/PycharmProjects/query_processor/lexicon.txt", "rb")
        self.url_file_pt = open("/Users/vivek/PycharmProjects/query_processor/Url_Table.txt", "rb")

        self.lex_data = self.lex_file_pt.read().split('\n')
        self.url_data = self.url_file_pt.read().split('\n')

        # Load the lexicon file into Main memory
        for line in self.lex_data:

                lextext = line.split(' ')
                lexlst = []
                lexlst.append(int(lextext[1]))
                lexlst.append(int(lextext[2]))
                self.lexdicondictionary[lextext[0]] = lexlst
        print "\nLexicon file loaded in main memory..."

        # Load the URL Table into Main memory
        for line in self.url_data:
            text = line.split(' ')
            lsurl = []
            lsurl.append(text[1])
            lsurl.append(text[2])
            self.urldata[int(text[0])] = lsurl
            self.totaldocssize += int(text[2])
        print "URL table loaded in main memory...\n"

        # Calculate total number of URL
        self.N = len(self.url_data)

        # Calculate average length of the pages
        self.avgd = float(self.totaldocssize) / float(self.N)


    # Function to decode the data which were encoded using variable byte
    def vb_decode(self, bytestream):
        n = 0
        numbers = []
        bytestream = unpack('%dB' % len(bytestream), bytestream)
        for byte in bytestream:
            if byte < 128:
                n = 128 * n + byte
            else:
                n = 128 * n + (byte - 128)
                numbers.append(n)
                n = 0
        return numbers


    # Function which perform all the major operations
    def read_files(self, keywords, querystring):

        # If the search string is empty or only contains stop words
        if len(keywords) == 0:
            print "No matched page found."
            endtime = time.time()
            return endtime

        keylist = []
        doctemplist = []
        commondoclist = []
        doclength = {}
        urldictionary = {}
        docfreqdictionary = {}
        Result = []

        for k in range(len(keywords)):

            query = keywords[k]

            cacheflag = 0

            # If the word is present into Cache dictionary
            if query in self.cachedictionary:
                cacheflag = 1
                dtemp = self.cachedictionary[query][0]
                temp = self.cachedictionary[query][1]
                self.cachedictionary[query][2] += 1

            # If word is not present in Cache than check the work into lexicon dictionary
            elif (cacheflag == 0) and (query in self.lexdicondictionary):
                index = self.lexdicondictionary[query][0]
                index_file = self.lexdicondictionary[query][1]

            else:
                print "No such Word Found."
                endtime = time.time()
                return endtime

            try:

                if cacheflag == 0:

                    # Open respected index file to get docid and frequency of the word
                    fp = open("/Users/vivek/PycharmProjects/query_processor/index-"+str(index_file), "rb")

                    # Iterate to respected line number in index file
                    for i, line in enumerate(fp):

                        # Reached to respected file number
                        if i == index - 1:

                            # Get encoded docid and frequency from the index file
                            contents = line.split('x4z')
                            word1 = contents[0]
                            doc1 = contents[1]
                            freq1 = contents[2]

                            dtemp = doc1.split('z4x')
                            temp = freq1.split('z4x')

                            # Check if the size of cache dictionary reached to 10
                            if len(self.cachedictionary) == 10:
                                # Get the least frequent word used from Cache
                                lfu = self.leastFrequentUsed()
                                # Remove least frequent used word
                                del self.cachedictionary[lfu]

                            # Insert current word into Cache dictionary
                            cachelist = []
                            cachelist.append(dtemp)
                            cachelist.append(temp)
                            cachelist.append(1)
                            self.cachedictionary[query] = cachelist

                            break

                    fp.close()

                doc = []
                freq = []


                # Decode each and every docid and frequency
                for v in range(len(dtemp)):
                    if dtemp[v] in self.decodedictionary:
                        val1 = self.decodedictionary[dtemp[v]]
                    else:
                        val1 = self.vb_decode(dtemp[v])
                        if len(val1) == 1:
                            self.decodedictionary[dtemp[v]] = val1

                    if temp[v] in self.decodedictionary:
                        val2 = self.decodedictionary[temp[v]]
                    else:
                        val2 = self.vb_decode(temp[v])
                        if len(val2) == 1:
                            self.decodedictionary[temp[v]] = val2

                    if len(val1) == 1 and len(val2) == 1:
                        doc.append(int(val1[0]))
                        freq.append(int(val2[0]))

                dictionary = {}

                # Create dictionary for docid and frequency.
                for j in range(len(doc)):
                    dictionary[doc[j]] = freq[j]

                # Sort the document id
                doc.sort()

                doctemplist.append(doc)

                keylist.append(dictionary)

            except Exception as e:

                print e



        # Find common DocID:
        if len(keywords) > 1:

            # Find the largest docid
            maxel = 0
            for i in range(len(keywords)):
                if maxel < doctemplist[i][len(doctemplist[i])-1]:
                    maxel = doctemplist[i][len(doctemplist[i])-1]

            did = 0
            flag = 0

            # Create the list of common document id
            while did <= maxel:

                # nextGEQ will return document id from the list greater than or equal to did
                did = self.nextGEQ(doctemplist[0], did)

                i = 1

                while i < len(keywords):
                    d = self.nextGEQ(doctemplist[i], did)
                    if d:
                        if d == did:
                            i += 1
                        else:
                            break
                    else:
                        flag = 1
                        break

                if flag == 1:
                    break

                if did:
                    if d > did:
                        did = d
                    else:
                        commondoclist.append(did)
                        templist = []
                        freqsum = 0

                        # Get the frequency of the common doc id
                        for j in range(len(keywords)):
                            tempfreq = keylist[j]
                            freqsum += tempfreq[did]
                            templist.append(tempfreq[did])

                        docfreqdictionary[did] = freqsum

                        # Get the length and URL of the page according to its docid
                        doclength[did] = int(self.urldata[did][1])
                        urldictionary[did] = self.urldata[did][0]

                        did += 1
                else:
                    break
        else:
            templist = []
            dict = keylist[0]
            for did in dict:
                commondoclist.append(did)
                freqsum = dict[did]
                docfreqdictionary[did] = freqsum
                templist.append(dict[did])

                doclength[did] = int(self.urldata[did][1])
                urldictionary[did] = self.urldata[did][0]



        # Calculate BM25 score for common docid
        ft = len(commondoclist)

        if ft == 0:
            print "No matched page found."
            return

        # Insert the common docid into heap according to its BM25 score
        for doc in commondoclist:
            heapq.heappush(Result, (-1 * (GetBM25.getBM25(self.N, ft, docfreqdictionary[doc], doclength[doc], self.avgd)), urldictionary[doc]))

        # Stop the timer
        endtime = time.time()


        if len(commondoclist) >= 20:
            print "\nTop 20 Results for '"+querystring+"' out of "+ str(len(commondoclist)) +" pages:\n"
        else:
            print "\nTop "+ str(len(commondoclist)) +" Results for '"+querystring+"' out of "+ str(len(commondoclist)) +" pages:\n"

        # Get the top 20 results from the heap
        for i in range(len(Result)):
            if i == 20:
                break
            display = heapq.heappop(Result)
            print "URL          :"+str(display[1])
            print "BM25 Score   :"+str(-1 * display[0])
            print

        return endtime

    def nextGEQ(self, lp, k):

        while len(lp) > 0:
            if lp[0] >= k:
                return int(lp[0])
            else:
                lp.pop(0)

        return None

    def leastFrequentUsed(self):
        for word in self.cachedictionary:
            minimum = self.cachedictionary[word][2]
            break
        for word in self.cachedictionary:
            if self.cachedictionary[word][2] <= minimum:
                minimum = self.cachedictionary[word][2]
                w = word
        return w


def main():
    q = QueryProcessor()
    stop = stopwords.words('english')

    while True:

        query = raw_input("Enter your Query: ")

        # Start the timer
        stime = time.time()

        keywords = []

        # Remove stop words from the search query
        for str1 in query.split():                                       # Split the search query into array
            if str1 not in stop:
                keywords.append(str1.lower())

        etime = q.read_files(keywords, query)

        print "\nTime taken: "+str(etime - stime)+" Seconds\n"

        print


if __name__ == '__main__':
    main()
