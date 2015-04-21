import FileName
import os
import gzip
import tokenize
from struct import pack, unpack


# Function which will perform variable byte encoding
def vb_encode(number):
    bytes = []
    while True:
        bytes.insert(0, number % 128)
        if number < 128:
            break
        number /= 128
    bytes[-1] += 128
    return pack('%dB' % len(bytes), *bytes)



def read_files():

    # Get the path of initial input files
    path = "/Users/vivek/PycharmProjects/inverted_index/nz2_merged"
    index_list, data_list = FileName.getFiles(path)

    j = 0
    link = []
    urlsize = []
    test1 = ""
    fileindex = 0
    counter = 1

    # Create temp file
    filept = open('temp', 'wb')

    for i in range(len(index_list)):
        try:
            fname = path+"/"+index_list[i]
            dname = path+"/"+data_list[i]
            print "Index: "+str(fname)
            print "Data: "+str(dname)

            # Unzip input data file and index file
            with gzip.open(fname, "rb") as f:
                with gzip.open(dname, "rb") as datapt:
                    for line in f:
                        test1 = line
                        temp = []
                        temp = line.split()

                        # Read the input data file
                        data = datapt.read(int(temp[3]))

                        # Check if the page is valid or not
                        flag = tokenize.test(data)

                        dictionary = {}

                        # If the page is valid
                        if flag:

                            # Create the dictionary of words of each and every page
                            dictionary = tokenize.parse(data)
                            if len(dictionary) != 0:
                                # Store the URL and size of the page
                                link.append(temp[0])
                                urlsize.append(temp[3])

                                for word in dictionary:

                                    data = dictionary[word]

                                    # Limit the intermediate file upto 250000 number of lines
                                    if counter == 250000:
                                        filept.close()
                                        # Sort the intermediate file using Unix sort
                                        os.system("sort -b --output=index"+str(fileindex)+" temp")
                                        # Remove temp file
                                        os.remove('temp')
                                        fileindex += 1
                                        filept = open('temp', 'wb')
                                        counter = 0

                                    counter += 1

                                    # Write word, encoded docid and encoded frequency into intermediate file
                                    filept.write(word+" ")
                                    filept.write(vb_encode(j))
                                    filept.write(" ")
                                    filept.write(vb_encode(data))
                                    filept.write("\n")

                                j += 1

        except Exception as e:
            print "Error..."
            print "Index: "+str(fname)
            print "Link: "+str(test1)
            print e
            pass

    if counter > 0 and counter < 250000:
        filept.close()
        os.system("sort -b --output=index"+str(fileindex)+" temp")
        os.remove('temp')

    final = open("Url_Table.txt", 'w')

    print "Length: "+str(len(link))

    # Write into URL table
    for j in range(len(link)):
        final.write(str(j) + " " + link[j] + " " + urlsize[j] + "\r")

    final.close

    return

