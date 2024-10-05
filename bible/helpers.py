import json

def dict2json(dictionary: dict, filename: str) -> None:
    with open(filename,"w", encoding="utf-8") as jfile:
        jfile.write(json.dumps(dictionary))

def json2dict(filename: str) -> dict:
    with open(filename, "r", encoding="utf-8") as jfile:
        return json.loads(jfile.read())

    
