import os
import json
from pyexcel_ods import get_data

card_type = 0
file_maps = {
    "http://cloud-3.steamusercontent.com/ugc/772865031540542706/585DBDDB6650A0462A6506B74B8B87A585FDFCD9/" : ("https://raw.githubusercontent.com/AutumnHaunted/virtuoso/main/images/back.png", None, None, None),
    "http://cloud-3.steamusercontent.com/ugc/772865031540540794C98E93BB4F42DBEE03DC3198BA79FF79D57FFF92/"  : ("https://raw.githubusercontent.com/AutumnHaunted/virtuoso/main/images/atlas/no-border/SBLE_001-050.png", "SBLE",   1, 50),
    "http://cloud-3.steamusercontent.com/ugc/772865031540547686F63C9013BC63CF97C7E37F5F30071B0757196A5C/"  : ("https://raw.githubusercontent.com/AutumnHaunted/virtuoso/main/images/atlas/no-border/SBLE_101-150.png", "SBLE", 101, 50),
    "http://cloud-3.steamusercontent.com/ugc/1040841723868399691/3DA8B8223A717C8CC304783E667F47910566838E/": ("https://raw.githubusercontent.com/AutumnHaunted/virtuoso/main/images/atlas/no-border/SBLE_001-050.png", "SBLE",   1, 50),
    "http://cloud-3.steamusercontent.com/ugc/1040841723868463096/DA4B589E5914F7E216778FE083B6A0089BE0E811/": ("https://raw.githubusercontent.com/AutumnHaunted/virtuoso/main/images/atlas/no-border/SBLE_051-100.png", "SBLE",  51, 50),
    "http://cloud-3.steamusercontent.com/ugc/1040841723868471605/D0D25E461EC433E32B92C3FAE923AC6FBE009430/": ("https://raw.githubusercontent.com/AutumnHaunted/virtuoso/main/images/atlas/no-border/SBLE_101-150.png", "SBLE", 101, 50),
    "http://cloud-3.steamusercontent.com/ugc/1040841723868477880/6E29E839C223CC3B7C87FAE4910A640570517171/": ("https://raw.githubusercontent.com/AutumnHaunted/virtuoso/main/images/atlas/no-border/SBLE_101-150.png", "LUNM",   1, 50),
    "http://cloud-3.steamusercontent.com/ugc/1040841723868482039/6D328F694BA1BEBC28D8B7F6B0F68EE7E98246AC/": ("https://raw.githubusercontent.com/AutumnHaunted/virtuoso/main/images/atlas/no-border/LUNM_051-100.png", "LUNM",  51, 50)
}
file_maps_border = {
    "http://cloud-3.steamusercontent.com/ugc/772865031540542706/585DBDDB6650A0462A6506B74B8B87A585FDFCD9/" : ("https://raw.githubusercontent.com/AutumnHaunted/virtuoso/main/images/back.png", None, None, None),
    "http://cloud-3.steamusercontent.com/ugc/772865031540540794C98E93BB4F42DBEE03DC3198BA79FF79D57FFF92/"  : ("https://raw.githubusercontent.com/AutumnHaunted/virtuoso/main/images/atlas/border/SBLE_001-050.png", "SBLE",   1, 50),
    "http://cloud-3.steamusercontent.com/ugc/772865031540547686F63C9013BC63CF97C7E37F5F30071B0757196A5C/"  : ("https://raw.githubusercontent.com/AutumnHaunted/virtuoso/main/images/atlas/border/SBLE_101-150.png", "SBLE", 101, 50),
    "http://cloud-3.steamusercontent.com/ugc/1040841723868399691/3DA8B8223A717C8CC304783E667F47910566838E/": ("https://raw.githubusercontent.com/AutumnHaunted/virtuoso/main/images/atlas/border/SBLE_001-050.png", "SBLE",   1, 50),
    "http://cloud-3.steamusercontent.com/ugc/1040841723868463096/DA4B589E5914F7E216778FE083B6A0089BE0E811/": ("https://raw.githubusercontent.com/AutumnHaunted/virtuoso/main/images/atlas/border/SBLE_051-100.png", "SBLE",  51, 50),
    "http://cloud-3.steamusercontent.com/ugc/1040841723868471605/D0D25E461EC433E32B92C3FAE923AC6FBE009430/": ("https://raw.githubusercontent.com/AutumnHaunted/virtuoso/main/images/atlas/border/SBLE_101-150.png", "SBLE", 101, 50),
    "http://cloud-3.steamusercontent.com/ugc/1040841723868477880/6E29E839C223CC3B7C87FAE4910A640570517171/": ("https://raw.githubusercontent.com/AutumnHaunted/virtuoso/main/images/atlas/border/LUNM_001-050.png", "LUNM",   1, 50),
    "http://cloud-3.steamusercontent.com/ugc/1040841723868482039/6D328F694BA1BEBC28D8B7F6B0F68EE7E98246AC/": ("https://raw.githubusercontent.com/AutumnHaunted/virtuoso/main/images/atlas/border/LUNM_051-100.png", "LUNM",  51, 50)
}

card_types = {
    "OBJ": "Object",
    "MAP": "Map",
    "EVN": "Event"
}

print("Loading...")

ods_data = list(get_data("cards.ods").values())[0]
card_data = {}
for card in ods_data:
    if (card != None and len(card) >= 6):
        card_id = str(card[1])
        while (len(card_id) < 3):
            card_id = "0" + card_id
        card_id = card[0] + "-" + card_id
        
        if (len(card) >= 11 and card[10] != None and card[10] != ""):
            card_data[card_id] = (card[2], card[10])
            continue
        
        if (card[3] == "ENT"):
            stats = str.split(card[5], "/")
            card_data[card_id] = (card[2], "LV " + stats[0] + " HP " + stats[1] + "/" + stats[1] + " ATK " + stats[2] + " DEF " + stats[3])
        else:
            card_data[card_id] = (card[2], card[4] + " " + card_types.get(card[3]))
#print(card_data)

def convert_file(filepath, border = 0):
    
    cur_file_map = file_maps
    if (border == 1):
        cur_file_map = file_maps_border
        card_type = 0
    else:
        card_type = 1
    
    try:
        json_file = None
        with open(filepath, "r") as j:
            json_file = json.load(j)
    except:
        print( 'Could not open file "' + '".')
    
    os.rename(filepath, filepath + '.bak')
    
    deck_map = {}
    
    try:
        for key, custom_deck in list(json_file.get("ObjectStates")[0].get("CustomDeck").items()):
            deck_map[custom_deck.get("FaceURL")] = key
            custom_deck["BackURL"] = cur_file_map.get("http://cloud-3.steamusercontent.com/ugc/772865031540542706/585DBDDB6650A0462A6506B74B8B87A585FDFCD9/")[0]
            if (cur_file_map.get(custom_deck.get("FaceURL"))):
                custom_deck["FaceURL"] = cur_file_map.get(custom_deck.get("FaceURL"))[0]
            custom_deck["Type"] = card_type
        
        #print(deck_map)
        
        for card in json_file.get("ObjectStates")[0].get("ContainedObjects"):
            deck_url = None
            for value in list(card.get("CustomDeck").values()):
                deck_url = value.get("FaceURL")
                value["BackURL"] = cur_file_map.get("http://cloud-3.steamusercontent.com/ugc/772865031540542706/585DBDDB6650A0462A6506B74B8B87A585FDFCD9/")[0]
                if (cur_file_map.get(value.get("FaceURL"))):
                    value["FaceURL"] = cur_file_map.get(value.get("FaceURL"))[0]
                value["Type"] = card_type
            
            if (deck_map.get(deck_url)):
                card_ind = int(str(card.get("CardID"))[-2:])
                path, set, set_start, set_end = cur_file_map.get(deck_url)
                
                card_id = str(card_ind + set_start)
                while (len(card_id) < 3):
                    card_id = "0" + card_id
                card_id = set + "-" + card_id
                
                title, subtitle = card_data.get(card_id)
                card["Nickname"] = title
                card["Description"] = subtitle
                
                #print(card_id + ": " + title + " | " + subtitle)
        
        with open(filepath, "w") as x:
            json.dump(json_file, x)
        
        print( 'Successfully converted "' + filepath + '".')
    except Exception as err:
        #raise(err)
        print( 'Failed to parse "' + filepath + '".')
        os.rename(filepath + '.bak', filepath)

def choiceYN(message):
    confirm = 0
    while (True):
        confirm = input(message)
        if (len(confirm) > 0 and confirm.upper()[0] == "Y"):
            return 1
        elif (len(confirm) > 0 and confirm.upper()[0] == "N"):
            return 0

while (True):
    path = input("Type the path to the file or directory you want to convert: ")
    
    if (not os.path.exists(path)):
        print('The file or directory "' + path + '" does not exist. Please try again.')
        continue
    
    if (os.path.isfile(path)):
        if (path.upper().endswith('.JSON')):
            confirm = choiceYN("Convert this file? (Y/N): ")
            if (confirm == 1):
                border = choiceYN("Use card borders? (Y/N): ")
                convert_file(path, border)
            else:
                continue
        else:
            print("This is not a JSON file.")
            continue
    elif (os.path.isdir(path)):
        confirm = choiceYN('Convert all JSON files in directory "' + path + '"? (Y/N): ')
        if (confirm == 1):
            border = choiceYN("Use card borders? (Y/N): ")
            for file in os.scandir(path):
                if (file.name.upper().endswith(".JSON")):
                    convert_file(file.path, border)
        else:
            continue
    else:
        print('An unknown error occured while trying to access "' + path + '". Please try again.')
        continue