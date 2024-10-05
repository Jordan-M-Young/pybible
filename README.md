# pybible
Library for collecting bible data

# Installation

```bash
pip install pybible-api
```


# Quick Start

```python

from bible.bible import BibleAPI

# api key, create one in your https://scripture.api.bible/ account dashboard
API_KEY = "<MY_API_KEY>"
BASE_URL = "https://api.scripture.api.bible/v1/"

# bible api handler object
bible_api = BibleAPI(api_key=API_KEY,base_url=BASE_URL)
```
