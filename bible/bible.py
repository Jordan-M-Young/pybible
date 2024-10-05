import requests
import bible.helpers as h
import os
import time
import regex as reg
from bs4 import BeautifulSoup

class BibleAPI():
    def __init__(self, api_key: str, base_url: str):

        self.api_key = api_key
        self.base_url = base_url
        self.headers = {"api-key":self.api_key,"accept":"application/json"}
        if not os.path.isdir("./data"):
            os.mkdir("./data")
            os.mkdir('./data/builds')
            os.mkdir("./data/builds/bibles")
            os.mkdir("./data/builds/books")
            os.mkdir("./data/builds/chapters")


    def get_bibles(self, to_file: bool =False) -> requests.Response:
        url = f"{self.base_url}bibles"
        response = requests.get(url=url,headers=self.headers)

        if to_file:
            h.dict2json(response.json(),"./data/bibles.json")
        return response

    def get_bible(self, bible_id: str, to_file: bool =False) -> requests.Response:
        url = f"{self.base_url}bibles/{bible_id}"
        response = requests.get(url=url, headers=self.headers)

        if to_file:
            h.dict2json(response.json(),f"./data/bible_{bible_id}.json")
        return response
    def get_books(self, bible_id: str, to_file: bool = False) -> requests.Response:
        url = f"{self.base_url}bibles/{bible_id}/books"
        response = requests.get(url=url, headers=self.headers)

        if to_file:
            h.dict2json(response.json(),f"./data/bible_{bible_id}_books.json")
        return response
    def get_book(self, bible_id: str, book_id: str, to_file: bool = False) -> requests.Response:
        url = f"{self.base_url}bibles/{bible_id}/books/{book_id}"
        response = requests.get(url=url, headers=self.headers)

        if to_file:
            h.dict2json(response.json(),f"./data/bible_{bible_id}_book_{book_id}.json")

        return response
    def get_chapters(self, bible_id: str, book_id: str, to_file: bool = False) -> requests.Response:
        url = f"{self.base_url}bibles/{bible_id}/books/{book_id}/chapters"
        response = requests.get(url=url, headers=self.headers)

        if to_file:
            h.dict2json(response.json(),f"./data/bible_{bible_id}_book_{book_id}_chapters.json")
        return response
    def get_chapter(self, bible_id: str, chapter_id: str, to_file: bool = False) -> requests.Response:
        url = f"{self.base_url}bibles/{bible_id}/chapters/{chapter_id}"

        response = requests.get(url=url, headers=self.headers)

        if to_file:
            h.dict2json(response.json(),f"./data/bible_{bible_id}_chapter_{chapter_id}.json")
        return response
    def get_verses(self, bible_id: str, chapter_id: str, to_file: bool = False) -> requests.Response:
        url = f"{self.base_url}bibles/{bible_id}/chapters/{chapter_id}/verses"

        response = requests.get(url=url, headers=self.headers)

        if to_file:
            h.dict2json(response.json(),f"./data/bible_{bible_id}_chapter_{chapter_id}_verses.json")
        return response
    def get_verse(self, bible_id: str, verse_id: str, to_file: bool = False) -> requests.Response:
        url = f"{self.base_url}bibles/{bible_id}/verses/{verse_id}"

        response = requests.get(url=url, headers=self.headers)

        if to_file:
            h.dict2json(response.json(),f"./data/bible_{bible_id}_verse_{verse_id}.json")

        return response
    
    def build_chapter(self, bible_id: str, chapter_id: str, to_file: bool = True, caching: bool = True, wait: float = 0.0) -> dict:
        built_chapter = {"chapter":chapter_id, "verses":{}}
        
        filepath = f"./data/bible_{bible_id}_chapter_{chapter_id}.json"
        if os.path.isfile(filepath):
            print(f"File: {filepath} | Found")
            chapter_metadata = h.json2dict(filepath)
        else:
            print(f"File: {filepath} | Not Found... Fetching Chapter: {chapter_id}")
            time.sleep(wait)
            chapter_metadata = self.get_chapter(bible_id=bible_id,chapter_id=chapter_id, to_file=caching).json()


        soup = BeautifulSoup(chapter_metadata['data']['content'],"html.parser")
        chapter_text = soup.text


        verse_numbers = reg.findall("([0-9][0-9]{0,3}[a-zA-z])+",chapter_text)

        for number in reversed(verse_numbers):
            chapter_text = chapter_text.replace(str(number[0]), f"\n{list(number[0])[-1]}")


        texts = chapter_text.split('\n')
        for idx, text in list(enumerate(texts))[1:]:
            built_chapter['verses'][f"{chapter_id}.{idx}"] = text
        
        if to_file:
            h.dict2json(built_chapter,f"./data/{bible_id}_{chapter_id}_build.json")


        return built_chapter


    def _build_chapter_inefficient(self, bible_id: str, chapter_id: str, to_file:bool = False, caching: bool =True, wait: float = 0.0) -> dict:
        filepath = f"./data/bible_{bible_id}_chapter_{chapter_id}.json"
        if os.path.isfile(filepath):
            print(f"File: {filepath} | Found")
            chapter_metadata = h.json2dict(filepath)
        else:
            print(f"File: {filepath} | Not Found... Fetching Chapter: {chapter_id}")

            chapter_metadata = self.get_chapter(bible_id=bible_id,chapter_id=chapter_id, to_file=caching).json()
        
        
        verses = {}
        verse_count = chapter_metadata['data']['verseCount']
        for count in range(1,verse_count+1):
            time.sleep(wait)
            verse_id = f"{chapter_id}.{count}"
            verse_file = f"./data/bible_{bible_id}_verse_{verse_id}.json"
            if os.path.isfile(verse_file):
                print(f"File: {verse_file} | Found")
                verse_metadata = h.json2dict(verse_file)
            else:
                print(f"File: {verse_file} | Not Found... Fetching Verse: {verse_id}")

                verse_metadata = self.get_verse(bible_id=bible_id,verse_id=verse_id,to_file=caching).json()
            
            verse_text = get_verse_text(verse_metadata)
            verse_text = verse_text.replace(str(count),"",1)
            verses[verse_id] = verse_text

        built_chapter = {"chapter":chapter_id, "verses":verses}

        if to_file:
            h.dict2json(built_chapter,f"./data/{bible_id}_{chapter_id}_build.json")


        return built_chapter
        
    def build_book(self, bible_id: str, book_id: str, to_file: bool = False, caching: bool = True, wait: float = 0.0) -> dict:
        filepath = f"./data/bible_{bible_id}_book_{book_id}_chapters.json"
        if os.path.isfile(filepath):
            print(f"File: {filepath} | Found")
            book_chapters_metadata = h.json2dict(filepath)
        else:
            print(f"File: {filepath} | Not Found... Fetching Book: {book_id}")
            book_chapters_metadata = self.get_chapters(bible_id=bible_id,book_id=book_id,to_file=True).json()


        chapters = book_chapters_metadata['data']
        built_book = {"chapter":"","books":{}}
        for chapter in chapters:
            chapter_id = chapter['id']
            book_id = chapter['bookId']
            chapter_verses = self.build_chapter(bible_id=bible_id,chapter_id=chapter_id,to_file=True,caching=True,wait=wait)
            built_book['books'][chapter_id] = chapter_verses

        built_book['chapter'] = book_id


        if to_file:
            h.dict2json(built_book,f"./data/{bible_id}_{book_id}_build.json")

        return built_book
    
    def build_bible(self, bible_id: str, to_file: bool = True, caching= True, wait: float = 0.0) -> dict:
        filepath =f"./data/bible_{bible_id}_books.json"
        if os.path.isfile(filepath):
            print(f"File: {filepath} | Found")
            bible_books_metadata = h.json2dict(filepath)
        else:
            print(f"File: {filepath} | Not Found... Fetching Bible: {bible_id}")
            bible_books_metadata = self.get_books(bible_id=bible_id,to_file=caching).json()
        
        built_bible = {"bible":bible_id,"books":{}}

        bible_books = bible_books_metadata['data']
        for book in bible_books:
            book_id = book['id']
            built_book = self.build_book(bible_id=bible_id,book_id=book_id,to_file=caching, caching=caching, wait=wait)
            built_bible['books'][book_id] = built_book

        
        if to_file:
            h.dict2json(built_bible,f"./data/builds/bibles/{bible_id}_build.json")



        return built_bible

def get_verse_text(verse: dict) -> str:
    try:
        soup = BeautifulSoup(verse['data']['content'],"html.parser")
        return soup.text
    except Exception as e:
        return str(e)