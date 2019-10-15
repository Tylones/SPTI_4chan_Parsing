import requests
import json
import datetime
import time

def main():
    print("Hello World!")
    timestamp=datetime.datetime.now()

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

if __name__ == "__main__":
    main()