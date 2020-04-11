import urllib3
import json
from datetime import datetime

def lambda_handler(event, context):
    # Create pool manager
    http = urllib3.PoolManager()

    # Get the Minecraft version data
    r = http.request('GET', 'https://launchermeta.mojang.com/mc/game/version_manifest.json')
    data = json.loads(r.data.decode('utf-8'))
    
    # Determine the latest release version
    latestVersion = data["latest"]["release"]

    # Initialize variables in case of error
    url = "NOT FOUND"
    releaseTime = "NOT FOUND"
    
    # Find the date on the latest release version
    for items in data["versions"]:
        if items["id"] == latestVersion and items["type"] == "release":
            url = items["url"]
            releaseTime = datetime.strptime(items["releaseTime"][:19],"%Y-%m-%dT%H:%M:%S")
            break

    # In case of missing version info, do not proceed to find URL
    if url != "NOT FOUND" and releaseTime != "NOT FOUND":
        # Get the download URL
        r = http.request('GET', url)
        data = json.loads(r.data.decode('utf-8'))
        url = data["downloads"]["server"]["url"]

    outdata = {
        "version": latestVersion,
        "releaseTime": releaseTime.strftime("%Y-%m-%dT%H:%M:%S"),
        "downloadURL": url
    }

    return {
        'statusCode': 200,
        'body': json.dumps(outdata)
    }
