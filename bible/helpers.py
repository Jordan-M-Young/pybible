import json

def dict2json(dictionary: dict, filename: str) -> None:
    """"
    take a a dictionary and writes it into a json file.

    args: 

    dictionary: the dictionary we want to write

    filename: the path of the file we're writing out
    
    """


    with open(filename,"w", encoding="utf-8") as jfile:
        jfile.write(json.dumps(dictionary))

def json2dict(filename: str) -> dict:
    """"
    takes a json file and loads it into a dictionary

    args: 
    
    filename: the path of the file were reading in
    
    """
    with open(filename, "r", encoding="utf-8") as jfile:
        return json.loads(jfile.read())

    
