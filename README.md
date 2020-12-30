# TwitterAPIAutomation
## RUN
Install the dependencies via
pip install -r requirements.txt

Use the below command to run all the scripts
python -m pytest tests/

All the configurations are centralized in config.properties file. Kindly update the keys(client_id, client_secret,resource_owner_key,resource_owner_secret) before running the test scripts


## Project structure
      All the code is organized into folder 'tests' including the utils, model and results.
      The utilities has common functions like read/write file, OAuth1 & 2 authentication, GET/POST request handler and app properties
      Test results shall be found in test_results.png
      
      
## API Test 1
            Test case 1,4 are accessed through OAuth2 and 2&3 are accessed through OAuth1 authentication. The access token of OAuth1 is reused using pytest global config
      1. Get the twitter content of the tweet https://twitter.com/Google/status/1257326183101980673 and store it in a flat-file.
            Retrieved the the tweet text using https://api.twitter.com/2/tweets?ids=1257326183101980673 and saved the text in falt file 'tweet.txt'
      2. Download the video file from the tweet https://twitter.com/Google/status/1257326183101980673 and store it in a folder
            Retrieved the tweet details using https://api.twitter.com/1.1/statuses/show.json?id=1257326183101980673 and accessed the "extended_entities"
            Twitter API does not return extended entities in response for non Twitter native videos(like in the tweet 1257326183101980673)
            as explained here https://twittercommunity.com/t/twitter-video-support-in-rest-and-streaming-api/31258/40. So unable to download it.
            Added the a test case to depict the download of Twitter native videos  'test_should_download_native_video_in_tweet' for tweet id 1343927024214290438
       3. Get the number of retweets for the tweet https://twitter.com/Google/status/1257326183101980673 and store it in the same file
            Retrieved the retweet using https://api.twitter.com/1.1/statuses/retweets/1257326183101980673.json and accessed the retweet_count property from the response.
            The same is saved in the existing flat file 'tweet.txt'
       4. Get the retweeters ID for the tweet https://twitter.com/Google/status/1257326183101980673 and store it in the same file.
            NOTE:: This API returns only the active users, so it will not always match with the retweets count as specified in
            https://developer.twitter.com/en/docs/twitter-api/v1/tweets/post-and-engage/api-reference/get-statuses-retweeters-ids
            The retweeter's id is saved in the existing flat file 'tweet.txt'
        5. Final test case is added to verify the file contents against these test cases
        
 ## API TEST 2
            All the below endpoints are accessed via OAuth1 authentication. The new tweet id is saved in global data of pytest and accessed in remaining test cases
         1. Make a new tweet with the text "We welcome you to MSD family :) 
              Posted tweet using the API 'https://api.twitter.com/1.1/statuses/update.json' through OAuth1 authentication and the tweet id is saved in global data of pytest
         2. Now retweet the same tweet
              Retweeted using 'https://api.twitter.com/1.1/statuses/retweet/{id}.json'
         3. Now get the retweet count & retweeters ID and validate the correctness of the data.
              Access the API 'https://api.twitter.com/1.1/statuses/retweets/{id}.json' and retrieve retweet_count & retweeters id
              The retweet count and retweeters id list lenght is checked if they match
         4. Now revert the previous retweet (un retweet the above tweet) and get the retweet count & retweeters ID and validate the correctness of the data
             Untweeted using the API 'https://api.twitter.com/1.1/statuses/unretweet/{id}.json' and executed the above test cases to see if untweet worked
         5. Now finally delete the tweet
              Deleted the tweet using 'https://api.twitter.com/1.1/statuses/destroy/{id}.json'
         
            
      
      
 
     
