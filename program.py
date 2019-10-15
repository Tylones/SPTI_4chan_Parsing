import requests
import json
import datetime
import time
import sys
import getopt

board = '/b/'  # default board is /b/
outputfile = 'output.json' # default output file is output.json

def main(argv):

    try:
        opts, args = getopt.getopt(argv,"hb:o:",["board=","ofile="])
    except getopt.GetoptError:
        print("test.py -i <inputfile> -o <outputfile>")
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print("test.py -b <board> -o <outputfile>")
            sys.exit()
        elif opt in ("-b", "--board"):
            board = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    
    print(board + " " + outputfile)
    timestamp=datetime.datetime.now()
    start = timestamp
    # Retrieving the list of every existing thread in the desired board (here /po/)
    responseThreads = requests.get('https://a.4cdn.org/po/threads.json', 
    headers={'If-Modified-Since': str(timestamp)},)
    for page in json.loads(responseThreads.content):

        # For each thread 
        for thread in page["threads"]:
            timestamp=datetime.datetime.now()

            # Retrieve the list of every existing replies for the thread
            responseThreadContent = requests.get('https://a.4cdn.org/po/thread/' + str(thread["no"]) + '.json', 
    headers={'If-Modified-Since': str(timestamp)},)
            content = json.loads(responseThreadContent.content)
            
            # For each replie, check if it contains a specific word (here "I")
            for replie in content["posts"]:
                if("com" in replie and "I" in replie["com"]):
                    print(replie["com"])
                else:
                    print("no")
            time.sleep(1);

    print(str(datetime.datetime.now()- start))

if __name__ == "__main__":
    main(sys.argv[1:])