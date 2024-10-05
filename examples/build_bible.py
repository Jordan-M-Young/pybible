from bible.bible import BibleAPI

# api key, create one in your https://scripture.api.bible/ account dashboard
API_KEY = ""
BASE_URL = "https://api.scripture.api.bible/v1/"

#id of the bible you want to build.
BIBLE_ID = ""

# bible api handler object
bible_api = BibleAPI(api_key=API_KEY,base_url=BASE_URL)

# builds a full bible dictionary
built_bible = bible_api.build_bible(bible_id=BIBLE_ID,to_file=True,caching=True,wait=0.1)