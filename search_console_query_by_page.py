###########################################################################################################################
#Learn more about the Google Search Cosnole API: https://developers.google.com/webmaster-tools/search-console-api-original/
#Author: David Tzau
###########################################################################################################################
import sys
import time
from oauth2client.service_account import ServiceAccountCredentials
from apiclient.discovery import build
import httplib2

#set authorization scope to read only
OAUTH_SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']

#load your Service Account credeitnails
credentials = ServiceAccountCredentials.from_json_keyfile_name('YOUR_SERVICE_ACCOUNT_CREDENTIALS_FILE.json', OAUTH_SCOPES)

#create Http object and authorize it to access with our credentials to access Search Console data
http = httplib2.Http()
authorized_http = credentials.authorize(http)

#create search console service instance
search_console_service = build('webmasters', 'v3', http=authorized_http)

#open output file to write infromation returned from Google Search Console API.
with open('output.csv', 'w') as outputfile:

  #write header information
  outputfile.write('URL,Keyword,Impressions,Clicks,CTR,Position\n')

  #read the input file of target URLs
  input_file = open('input_target_urls.csv', 'r')
  
  #for index, row in dataframe.iterrows():
  for target_url in input_file:

    #remove carraige return from end fo target_url
    target_url_stripped = target_url.strip()
    
    #Build api request. Get top 10 queries for the date range, sorted by click count descending with page filter applied
    request = {
        'startDate': '2017-03-01',
        'endDate': '2017-03-20',
        'dimensions': ['query'],
        'dimensionFilterGroups': [{
          'filters': [{
            'dimension': 'page',
            'operator': 'equals',
            'expression': target_url_stripped
            }]
          }],
        'rowLimit': 10
      }

    print 'obtaining keyword data for page: ' + target_url_stripped
    
    #call the search console service
    response = search_console_service.searchanalytics().query(siteUrl='https://www.yourwebsite.com/', body=request).execute()

    #determine if there is any data returend from Google Search Console for this specific URL
    if 'rows' in response.keys():

      #iterate through top 10 keyword level data results and write to output file
      for keyword_result in response['rows']:
        outputfile.write(target_url_stripped + ',' +
                     keyword_result['keys'][0] + ',' +
                     repr(keyword_result['impressions']) + ',' +
                     repr(keyword_result['clicks']) + ',' +
                     repr(keyword_result['ctr']) + ',' +
                     repr(keyword_result['position']) + '\n')                     
      
    else:
      #Google does not have data for this target URL
      outputfile.write(target_url_stripped + ',No Data for this target URL\n')

  #close input file
  input_file.close()

#close output file
outputfile.close()

print 'done'




