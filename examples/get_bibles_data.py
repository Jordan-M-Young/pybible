from bible import BibleAPI

API_KEY = ""
BASE_URL = "https://api.scripture.api.bible/v1/"

bible_api = BibleAPI(api_key=API_KEY,base_url=BASE_URL)

#gets a json object containing all available bibles and metadata
bibles = bible_api.get_bibles(to_file=True).json()