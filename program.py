import requests
import json
import datetime
import time
import sys
import getopt
import os



def main(argv):
    board = 'b'  # default board is /b/
    outputfile = 'output.json' # default output file is output.json

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


    if(not os.path.exists(outputfile) or os.stat(outputfile).st_size == 0):
        data = {}
        data["threads"] = []
        jsonFile = open(outputfile, "w+")
        jsonFile.write(json.dumps(data))
        jsonFile.close()

    jsonFile = open(outputfile, "r") # Open the JSON file for reading
    outputData = json.load(jsonFile) # Read the JSON into the buffer
    jsonFile.close()
    timestamp=datetime.datetime.now()
    start = timestamp
    # Retrieving the list of every existing thread in the desired board (here /po/)
    responseThreads = requests.get('https://a.4cdn.org/'+board+'/threads.json', 
    headers={'If-Modified-Since': str(timestamp)},)
    for page in json.loads(responseThreads.content):

        # For each thread 
        for thread in page["threads"]:
            timestamp=datetime.datetime.now()

            # Retrieve the list of every existing replies for the thread
            responseThreadContent = requests.get('https://a.4cdn.org/'+board+'/thread/' + str(thread["no"]) + '.json', 
    headers={'If-Modified-Since': str(timestamp)},)
            content = json.loads(responseThreadContent.content)
            
            # For each replie, check if it contains a specific word (here "I")
            for replie in content["posts"]:
                if("com" in replie and "I" in replie["com"]):
                    outputData["threads"].append(content["posts"])
                    print(replie["com"])
                    jsonFile = open(outputfile, "w+")
                    jsonFile.write(json.dumps(outputData))
                    jsonFile.close()
                    sys.exit();
                else:
                    print("no")
            time.sleep(1);

    print(str(datetime.datetime.now()- start))

if __name__ == "__main__":
    main(sys.argv[1:])