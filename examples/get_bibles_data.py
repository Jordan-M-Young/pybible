from bible.bible import BibleAPI

# api key, create one in your https://scripture.api.bible/ account dashboard
API_KEY = ""

BASE_URL = "https://api.scripture.api.bible/v1/"

# bible api handler object
bible_api = BibleAPI(api_key=API_KEY,base_url=BASE_URL)

#gets a json object containing all available bibles and metadata
bibles = bible_api.get_bibles(to_file=True).json()