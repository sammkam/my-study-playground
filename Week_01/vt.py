import urllib
import urllib2
import json
import sys 

hash_value = sys.argv[1]
vt_url = "https://www.virustotal.com/vtapi/v2/file/report"
api_key = "XXX"
parameters = {'apikey' : api_key, 'resource': hash_value}
encodet_parameters = urllib.urlencode(parameters)
request = urllib2.Request(vt_url, encodet_parameters)
response = urllib2.urlopen(request)
json_response = json.loads(response.read())
if json_response['response_code']:
    detection = json_response['positives']
    total = json_response['total']
    scan_results = json_response['scans']
    printf("Detections: " + detections + "/" + total)
    printf("VirusTotal Results:")
    for av_name, av_data in scan_results.items():
        printf("\t" + av_name + "==>" + av_data['result'])
