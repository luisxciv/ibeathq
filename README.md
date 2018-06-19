
ibeathq is a python script that will help you win that juicey HQ Trivia prize. It uses Google's Cloud Vision, Cloud Language and Custom Search API's to find the answer choice with the most number of iterations. 
## Example 
```bash
./bot.py -i n64.png
```
<p align="center">
  <img src="https://i.gyazo.com/543ee0c2c94fd2ae09cf76efb1799365.png?raw=true" alt="N64"/>
</p>

## Dependencies
The following modules are required

    google-cloud-vision
    google-cloud-language
    google-api-python-client
    
## How to Install 
1. Install the required packages with pip, execute the following on the commandine

```bash
path/to/python.exe pip install -r requirements.txt
```
2. Enable API's in Google Cloud Console, You'll need to set-up a billing account but won't be charged anything. [Google Cloud](https://console.cloud.google.com/home/dashboard).
    Enable [Google Cloud Natural Language API](https://console.cloud.google.com/apis/library/language.googleapis.com), [Google Cloud Custom Search API](https://console.cloud.google.com/apis/api/customsearch.googleapis.com) and [Google Cloud Vision API](https://console.cloud.google.com/apis/library/vision.googleapis.com).
    
 3.  Go to [Google Cloud Credentials Page](https://cloud.google.com/storage/docs/authentication#service_accounts) generate a new key and download the JSON. 
 
 4.  Set `GOOGLE_APPLICATION_CREDENTIALS` in the config file [botcfg] to the path of where you saved the JSON file.
 
 5.  Create a new Custom Search Engine @ [https://cse.google.com/cse/all]. Enter `www.google.com` in the sites to search input. Click `Create`. Then click `Modify your search engine`, then go down to `Sites to search` and under advanced change from `Search only included sites` to `Search the entire web but emphasize included sites`.
 
 6.  Set `customsearch_id` in the config file to your search engine ID found under the details section of CSE.
 
 7.  Set `developerKey` in the config file to your Developer API Key found in the [Credentials Page](https://console.developers.google.com/apis/credentials)
 
 8. Test it : 
```bash
./bot.py -i n64.png
```
 