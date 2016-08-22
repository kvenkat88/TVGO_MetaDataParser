import csv
import os.path
from Library import Helper as hl

def csv_info_writer(url):
    status,channellist,error = hl.stream_info_parser(url,method = "GET")
    stream_type_identify = hl.stream_type_identifier(url)
    try:
        current_time = hl.currentTime()
        filename = "%s_stream_info_collector"%(stream_type_identify) + "_"+current_time
        file_writer = csv.writer(open("%s.csv"%(filename), "w"),lineterminator='\n')
        file_writer.writerow(["_type","Stream Name","ProviderCodes","Ratings","NtworkId","Stream_Id",'udbServiceId',"CC Status","SAP Status","Live_Stream_URL","Playback_URL"])
        for channel in channellist:
            file_writer.writerow([channel['_type'],channel['title'],channel['providerCodes'][0],channel['rating'],channel['networkId'],
                                  channel['id'],channel['udbServiceId'],channel['closeCaption'],channel['secondaryAudioProgram'],channel['_links']['website']['href'],channel['_links']['playback']['href']])
        print "Metadata File for requested - %s stream URLs are created" %(stream_type_identify)
    except Exception as e:
        print "Exception Occured :::::" ,e

get_url = hl.get_input_from_user()
csv_info_writer(get_url)

