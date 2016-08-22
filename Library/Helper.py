__author__ = '269896'

import json, sys,os
import urllib2
import httplib
import datetime
reload(sys)
sys.setdefaultencoding('utf8')

#Class to deal the URL redirects of the request
class RedirectHandler(urllib2.HTTPRedirectHandler):

    def http_error_301(self, req, fp, code, msg, headers):
        return urllib2.HTTPRedirectHandler.http_error_301(self, req, fp, code, msg, headers)

    def http_error_302(self, req, fp, code, msg, headers):
        return urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)

    http_error_303 = http_error_307 = http_error_302

def stream_type_identifier(url):

    url1 = url.split("//")
    url2 = url1[1].split("/")
    return url2[3]

def currentTime():
    timeFormat = "%Y-%m-%dT%H-%M-%S"
    currentTime = datetime.datetime.now()
    return currentTime.strftime(timeFormat)

def json_processor():
    configPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '../Configuration'))
    with open(configPath + '/info.json') as data_file:
        data = json.load(data_file)
    return data

def get_input_from_user():
    json_data = json_processor()
    choice = raw_input("Enter the Endpoints as ios/android/desktop :: ")
    if choice == "ios":
        print ("Metadata File Requested for IOS is executing........")
        return json_data['ios_feed']
    elif choice == "android":
        print ("Metadata File Requested for Android is executing........")
        return json_data['android_feed']
    elif choice == "desktop":
        print ("Metadata File Requested for web is executing........")
        return json_data['desktop_feed']
    else:
        print ("Please provide valid endpoint for fetching the metadata information!!!!!!!!!!")
        sys.exit(1)

def stream_info_parser(url,method=None):
    status_code = 500
    error_msg = None
    channellist = None
    stream_type_identify = stream_type_identifier(url)
    request = urllib2.Request(url)
    if not method == None:
        request.get_method = lambda: method
    opener = urllib2.build_opener(RedirectHandler())
    try:
        print "URL Requested for processing is %s" %(url)
        response = opener.open(request)
    except (urllib2.URLError,urllib2.HTTPError,httplib.HTTPException) as  e:
        print("Exception returned. URL :: " + url)
        if hasattr(e, 'code') and hasattr(e, 'read'):
            status_code = e.code
            error_msg =  e.read()
        elif hasattr(e, 'msg'):
            error_msg = e.msg
        elif hasattr(e, 'reason'):
            error_msg = e.reason
        print("Error code :: " + str(status_code) + " || Error message :: " + str(error_msg))
    except:
        print("UNKNOWN Exception returned. Need to validate further")
    else:
        status_code = response.code
        response_data = response.read()
        response = json.loads(response_data)
        channellist = response['streams']
        totalStreams = len(response['streams'])
        print "Total streams available for %s: %s" %(stream_type_identify,totalStreams)

    return status_code,channellist, error_msg