from bible import BibleAPI

API_KEY = ""
BASE_URL = "https://api.scripture.api.bible/v1/"
BIBLE_ID = ""


bible_api = BibleAPI(api_key=API_KEY,base_url=BASE_URL)

#builds a json object containing all bible verses nested like so:
# bible -> book -> chapter -> verse

built_bible = bible_api.build_bible(bible_id=BIBLE_ID,to_file=True,caching=True,wait=0.1)