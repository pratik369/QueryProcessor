import heapq
from os import listdir
import re


sortList = []


def mergeFiles():
    try:
        path = "/Users/vivek/PycharmProjects/inverted_index"
        index_file = []
        # Get the filenames of all the intermediate files
        for f in listdir(path):
            if re.search('index', f):
                index_file.append(f)

        print index_file

        filept = []
        for i in range(len(index_file)):
            filept.append(i)

        # Create file pointers for all the intermediate files
        index = 0
        for file in index_file:
            filept[index] = open(file, 'rb')
            index += 1

        index = 0

        # Create file pointer for output file
        f3 = open("index-"+ str(index) +".txt", 'wb')
        lexfile = open("lexicon.txt", 'wb')

        print "Start...!!!"

        document_list = []
        frequency_list = []

        # Insert first word from all the intermediate files into heap
        for i in range(len(filept)):
            heapq.heappush(sortList, (filept[i].readline(), i))

        word_extra = heapq.heappop(sortList)
        first = word_extra[0].split(' ')
        previous = first[0]
        heapq.heappush(sortList, (word_extra[0], word_extra[1]))

        line = 0
        templine = 0
        startline = 1

        while len(sortList) > 0:

            # Get the first word from the heap
            word = heapq.heappop(sortList)
            temp = word[0].split(' ')

            # If the length of current word is more than 25 then remove that word
            if len(temp[0]) > 25:
                continue

            if len(temp) >= 3:

                if previous == temp[0]:
                    document_list.append(temp[1].rstrip('\n'))
                    frequency_list.append(temp[2].rstrip('\n'))

                else:
                    if len(document_list) == 0:
                        document_list.append(temp[1].rstrip('\n'))
                        frequency_list.append(temp[2].rstrip('\n'))

                    # If the lines of index file reaches upto 150000 then create another index file
                    if line == 150000:
                        index += 1
                        f3.close()
                        f3 = open("index-"+ str(index) +".txt", 'wb')
                        startline = 1
                        line = 0

                    # Write word into index file
                    f3.write(previous+"x4z")

                    # Write encoded docid into index file
                    for i in range(len(document_list)):
                        if i == len(document_list) - 1:
                            f3.write(str(document_list[i]))
                        else:
                            f3.write(str(document_list[i]))
                            f3.write("z4x")

                    f3.write('x4z')

                    # Write encoded frequency into index file
                    for i in range(len(frequency_list)):
                        if i == len(frequency_list) - 1:
                            f3.write(str(frequency_list[i]))
                        else:
                            f3.write(str(frequency_list[i]))
                            f3.write("z4x")

                    f3.write("\n")

                    # Write into lexicon file
                    lexfile.write(previous+" "+str(startline)+" "+str(index)+"\n")

                    # Increase line number
                    line += 1
                    startline += 1

                    document_list = []
                    frequency_list = []

                # Read the next word from respected intermediate file
                text1 = (filept[word[1]].readline()).split('\n')[0]
                if text1:
                    heapq.heappush(sortList, (text1, word[1]))

        if previous == temp[0]:
            document_list.append(temp[1].rstrip('\n'))
            frequency_list.append(temp[2].rstrip('\n'))

            if line == 150000:
                index += 1
                f3.close()
                f3 = open("index-"+ str(index) +".txt", 'wb')
                startline = 1
                line = 0

            f3.write(previous+"x4z")

            for i in range(len(document_list)):
                if i == len(document_list) - 1:
                    f3.write(str(document_list[i]))
                else:
                    f3.write(str(document_list[i]))
                    f3.write("z4x")

            f3.write('x4z')

            for i in range(len(frequency_list)):
                if i == len(frequency_list) - 1:
                    f3.write(str(frequency_list[i]))
                else:
                    f3.write(str(frequency_list[i]))
                    f3.write("z4x")

            f3.write("\n")

            lexfile.write(previous+" "+str(startline)+" "+str(index)+"\n")

        print "End...!!!"

        # Close all the file pointers
        for file in filept:
            file.close()

        lexfile.close()
        f3.close()

    except Exception as e:
        print e