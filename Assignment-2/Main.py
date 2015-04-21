__author__ = 'Pratik Patel and Vivek Desai'

import ParseFiles
import merge


def main():

    ParseFiles.read_files()     # Create intermediate index files
    merge.mergeFiles()          # Merge all the intermediate files


if __name__=='__main__':
    main()
