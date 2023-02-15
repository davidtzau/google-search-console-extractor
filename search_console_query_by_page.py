###########################################################################################################################
#Learn more about the Google Search Cosnole API: https://developers.google.com/webmaster-tools
#Author: David Tzau
###########################################################################################################################
import sys
import time
import httplib2
from google.oauth2 import service_account
from apiclient.discovery import build

#set authorization scope to read only
OAUTH_SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']

#load your Service Account credeitnails
credentials = service_account.Credentials.from_service_account_file("YOUR_SERVICE_ACCOUNT_CREDENTIALS_FILE.json", scopes=OAUTH_SCOPES)

#create search console service instance
search_console_service = build('webmasters', 'v3', credentials=credentials)

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
        'startDate': '2023-01-01',
        'endDate': '2023-01-31',
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




