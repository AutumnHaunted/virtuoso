#!/usr/bin/python

from gimpfu import *

#from pathlib import Path
import os
import sys
import json

#sys.path.append(".")

#import pyexcel_ods

# our variables
bg_ass = {
    "ENT": "/assets/entity_bg.bmp",
    "OBJ": "/assets/object_bg.bmp",
    "MAP": "/assets/map_bg.bmp",
    "EVN": "/assets/event_bg.bmp"
}
bg_ass_border = {
    "ENT": "/assets/entity_bg_border_10px.bmp",
    "OBJ": "/assets/object_bg_border_10px.bmp",
    "MAP": "/assets/map_bg_border_10px.bmp",
    "EVN": "/assets/event_bg_border_10px.bmp"
}
sym_ass = {
    "FIG": "/assets/sym_fig.bmp",
    "MOB": "/assets/sym_mob.bmp",
    "LEG": "/assets/sym_leg.bmp",
    "CON": "/assets/sym_con.bmp",
    "AST": "/assets/sym_ast.bmp",
    "HAU": "/assets/sym_hau.bmp",
    "STL": "/assets/sym_stl.bmp",
    "WLD": "/assets/sym_wld.bmp",
    "LAI": "/assets/sym_lai.bmp",
    "IND": "/assets/sym_ind.bmp",
    "MAG": "/assets/sym_mag.bmp",
    "BTF": "/assets/sym_btf.bmp",
    "NML": "/assets/sym_nml.bmp",
    "RSP": "/assets/sym_rsp.bmp",
    "CTN": "/assets/sym_ctn.bmp"
}
font_sizes = [
    (29, 10),
    (28, 10),
    (26, 11),
    (24, 12),
    (23, 12),
    (21, 14),
    (19, 15)
]

def virtuoso_generate_card(cardName, cardType, subtypeA, subtypeB, level, hp, attack, defence, cardDesc, cardID, imgPath, dirPath, advantage, disadvantage, border = None, descTextSize = 16):
    
    cardImage = pdb.gimp_image_new(1, 1, 0)
    
    cardBGPath = dirPath + "/assets/event_bg.bmp"
    
    artOffset = 44
    subtypeCount = 2
    
    # determine card type
    if (bg_ass.get(cardType)):
        cardBGPath = dirPath + bg_ass.get(cardType)
    if (cardType == "ENT"):
        artOffset = 8
    
    # determine subtypes
    subtypePathA = None
    subtypePathB = None
    if (sym_ass.get(subtypeA)):
        subtypePathA = dirPath + sym_ass.get(subtypeA)
    if (sym_ass.get(subtypeB)):
        subtypePathB = dirPath + sym_ass.get(subtypeB)
    if (subtypePathA == None):
        subtypePathA = dirPath + "/assets/sym_null.bmp"
        subtypeCount -= 1
    if (subtypePathB == None):
        subtypePathB = subtypePathA
        subtypePathA = dirPath + "/assets/sym_null.bmp"
        subtypeCount -= 1
    
    # load background
    
    cardBGImage = pdb.gimp_file_load_layer(cardImage, cardBGPath)
    pdb.gimp_image_resize(cardImage, pdb.gimp_drawable_width(cardBGImage), pdb.gimp_drawable_height(cardBGImage), 0, 0)
    pdb.gimp_image_add_layer(cardImage, cardBGImage, 0)
    
    # load subtype icons
    subtypeImageA = None
    subtypeImageB = None
    if (subtypePathA != None):
        subtypeImageA = pdb.gimp_file_load_layer(cardImage, subtypePathA)
        pdb.gimp_image_add_layer(cardImage, subtypeImageA, 0)
        pdb.gimp_layer_set_offsets(subtypeImageA, 396,12)
    if (subtypePathB != None):
        subtypeImageB = pdb.gimp_file_load_layer(cardImage, subtypePathB)
        pdb.gimp_image_add_layer(cardImage, subtypeImageB, 0)
        pdb.gimp_layer_set_offsets(subtypeImageB, 436,12)
    
    # load advantage/disadvantage icons
    if (cardType == "ENT"):
        advantagePath = dirPath + "/assets/sym_null.bmp"
        disadvantagePath = dirPath + "/assets/sym_null.bmp"
        if (len(advantage) > 0 and sym_ass.get(advantage[0])):
            advantagePath = dirPath + sym_ass.get(advantage[0])
        if (len(disadvantage) > 0 and sym_ass.get(disadvantage[0])):
            disadvantagePath = dirPath + sym_ass.get(disadvantage[0])
        
        #pdb.gimp_message(advantage[0])
        #pdb.gimp_message(disadvantage[0])
        
        advantageImage = pdb.gimp_file_load_layer(cardImage, advantagePath)
        pdb.gimp_image_add_layer(cardImage, advantageImage, 0)
        pdb.gimp_layer_set_offsets(advantageImage, 424,334)
        disadvantageImage = pdb.gimp_file_load_layer(cardImage, disadvantagePath)
        pdb.gimp_image_add_layer(cardImage, disadvantageImage, 0)
        pdb.gimp_layer_set_offsets(disadvantageImage, 424,396)
    
    # draw card art
    if ((imgPath != None) and (imgPath != "")):
        cardArt = pdb.gimp_file_load_layer(cardImage, imgPath)
        pdb.gimp_image_add_layer(cardImage, cardArt, 0)
        pdb.gimp_layer_set_offsets(cardArt, artOffset, 56)
    
    # --- draw texts ---
    
    # draw name text
    nameText = pdb.gimp_text_layer_new(cardImage, cardName, "Unispace", 1, 0.01)
    pdb.gimp_image_add_layer(cardImage, nameText, 0)
    # get header size
    headerSize = 464 - (40 * subtypeCount)# - 8
    if (cardType == "ENT" and headerSize > 392):
        headerSize = 392
    if (headerSize == 464 or headerSize == 392):
        headerSize -= 4
    headerSize -= 4
    # find good size for text
    for font_size, text_pos in font_sizes:
        pdb.gimp_text_layer_set_font_size(nameText, font_size, 0.01)
        if (pdb.gimp_drawable_width(nameText) > headerSize):
            continue
        else:
            break
    pdb.gimp_text_layer_set_justification(nameText, 2)
    pdb.gimp_text_layer_set_color(nameText, (255,255,255))
    # squish text if it still doesn't fit
    if (pdb.gimp_drawable_width(nameText) > headerSize):
        pdb.gimp_layer_scale(nameText, headerSize, pdb.gimp_drawable_height(nameText), 0)
    else:
        if (pdb.gimp_drawable_width(nameText) <= 392 and artOffset + 196 + (pdb.gimp_drawable_width(nameText) / 2) <= headerSize):
            if (cardType == "ENT"):
                pdb.gimp_text_layer_resize(nameText, 384, 40)
            else:
                pdb.gimp_text_layer_resize(nameText, 456, 40)
        else:
            pdb.gimp_text_layer_resize(nameText, headerSize, 40)
    pdb.gimp_layer_set_offsets(nameText, 12, text_pos)
    
    # ~ draw stats text ~
    if (cardType == "ENT"):
        # draw level text
        levelText = pdb.gimp_text_layer_new(cardImage, level, "Press Start 2P", 24, 0.01)
        pdb.gimp_image_add_layer(cardImage, levelText, 0)
        pdb.gimp_text_layer_set_justification(levelText, 2)
        pdb.gimp_text_layer_resize(levelText, 60, 21)
        pdb.gimp_layer_set_offsets(levelText, 412, 83)
        pdb.gimp_text_layer_set_color(levelText, (255, 255, 255))
        # draw hp text
        hpText = pdb.gimp_text_layer_new(cardImage, hp, "Press Start 2P", 24, 0.01)
        pdb.gimp_image_add_layer(cardImage, hpText, 0)
        pdb.gimp_text_layer_set_justification(hpText, 2)
        pdb.gimp_text_layer_resize(hpText, 60, 21)
        pdb.gimp_layer_set_offsets(hpText, 412, 144)
        pdb.gimp_text_layer_set_color(hpText, (255, 255, 255))
        # draw attack text
        attackText = pdb.gimp_text_layer_new(cardImage, attack, "Press Start 2P", 24, 0.01)
        pdb.gimp_image_add_layer(cardImage, attackText, 0)
        pdb.gimp_text_layer_set_justification(attackText, 2)
        pdb.gimp_text_layer_resize(attackText, 60, 21)
        pdb.gimp_layer_set_offsets(attackText, 412, 207)
        pdb.gimp_text_layer_set_color(attackText, (255, 255, 255))
        # draw defence text
        defenceText = pdb.gimp_text_layer_new(cardImage, defence, "Press Start 2P", 24, 0.01)
        pdb.gimp_image_add_layer(cardImage, defenceText, 0)
        pdb.gimp_text_layer_set_justification(defenceText, 2)
        pdb.gimp_text_layer_resize(defenceText, 60, 21)
        pdb.gimp_layer_set_offsets(defenceText, 412, 269)
        pdb.gimp_text_layer_set_color(defenceText, (255, 255, 255))
    
    # do border calculation
    
    descText_posX = 10
    descText_posY = 455
    descText_sizeX = 460
    descText_sizeY = 209
    idText_posX = 470
    idText_posY = 651
    
    if (border):
        layer_count, layer_ids = pdb.gimp_image_get_layers(cardImage)
        while layer_count > 2:
            layer = pdb.gimp_image_merge_down(cardImage, gimp._id2drawable(layer_ids[0]), 0)
            layer_count, layer_ids = pdb.gimp_image_get_layers(cardImage)
        pdb.gimp_image_remove_layer(cardImage, gimp._id2drawable(layer_ids[1]))
        
        cardBGPath = "/assets/event_bg_border_10px.bmp"
        if (bg_ass_border.get(cardType)):
            cardBGPath = dirPath + bg_ass_border.get(cardType)
            
        cardBGImage = pdb.gimp_file_load_layer(cardImage, cardBGPath)
        pdb.gimp_image_resize(cardImage, pdb.gimp_drawable_width(cardBGImage), pdb.gimp_drawable_height(cardBGImage), 10, 10)
        pdb.gimp_image_add_layer(cardImage, cardBGImage, 1)
        
        descText_posX = 20
        descText_posY = 465
        #descText_sizeX = 462
        descText_sizeY = 217
        idText_posX = 480
        idText_posY = 669
    
    # draw description text
    descText = pdb.gimp_text_layer_new(cardImage, cardDesc, "Gadugi", descTextSize, 0.01)
    pdb.gimp_image_add_layer(cardImage, descText, 0)
    pdb.gimp_text_layer_set_line_spacing(descText, -4.0)
    pdb.gimp_text_layer_resize(descText, descText_sizeX, descText_sizeY)
    pdb.gimp_layer_set_offsets(descText, descText_posX, descText_posY)
    pdb.gimp_text_layer_set_color(descText, (255,255,255))
    # draw card ID text
    idText = pdb.gimp_text_layer_new(cardImage, "V:/" + cardID, "Microsoft New Tai Lue", 11, 0.01)
    pdb.gimp_image_add_layer(cardImage, idText, 0)
    pdb.gimp_layer_set_offsets(idText, idText_posX - pdb.gimp_drawable_width(idText), idText_posY)
    pdb.gimp_text_layer_set_color(idText, (255, 255, 255))
    pdb.gimp_text_layer_set_antialias(idText, 0)
    
    # display output
    #pdb.gimp_display_new(cardImage)
    
    # output to file
    outLayer = pdb.gimp_image_merge_visible_layers(cardImage, 0)
    
    return (cardImage, outLayer)
    
    #pdb.file_png_save(cardImage, outLayer, outPath, outPath, 0, 0, 0, 0, 0, 0, 0)
    
    #pdb.gimp_image_delete(cardImage)

def generate_all_cards(directory, outDir, border):#, asAtlas):
    
    data = load_json(directory)
    
    #if (asAtlas == 1 or asAtlas == True):
    #    generate_card_atlas(directory, data, outDir)
    #else:
    #    generate_card_list(directory, data, outDir, border)
    
    generate_card_list(directory, data, outDir, border)
    
    #virtuoso_generate_card(string, string, string, string, string, string, string, string, string, string, string)
    #pass

def generate_select_cards(directory, startInd, endInd, outDir, border):
    
    if (endInd < startInd):
        raise(Exception("The end index must be larger than the starting index."))
    
    if (startInd == 0 or endInd == 0):
        startInd += 1
        endInd += 1
    
    data = load_json(directory)
    
    card_range = data[startInd-1:endInd]
    generate_card_list(directory, card_range, outDir, border)

def generate_card_set(directory, setID, outDir, border):#, asAtlas):
    data = load_json(directory)
    
    setID = setID.upper()
    
    select_cards = []
    for card in data:
        if (len(card) >= 8 and card[0] == setID):
            select_cards.append(card)
    
    #if (asAtlas == 1 or asAtlas == True):
    #    generate_card_atlas(directory, select_cards, outDir)
   # else:
    #    generate_card_list(directory, select_cards, outDir, border)
    
    generate_card_list(directory, select_cards, outDir, border)

def generate_single_card(directory, cardID, outPath, outFile, border):
    
    data = load_json(directory)
    
    cardID = cardID.upper()
    
    cardIdArr = str.split(cardID, "-")
    
    card = None
    for x in data:
        if (len(x) >= 2):
            if (x[0] == cardIdArr[0] and int(x[1]) == int(cardIdArr[1])):
                card = x
                break
    
    if (card is None):
        raise(Exception("Could not find that card."))
    
    img, layer = generate_card(directory, card, outPath, border)
    save_image_and_delete(img, layer, outPath + "/" + outFile)

def generate_card(directory, card, outDir, border = None):
    
    subtypes = str.split(str(card[4]), "/")
    while (len(subtypes) < 2):
        subtypes.append("")
    
    stats = str.split(str(card[5]), "/")
    while (len(stats) < 4):
        stats.append(0)
    
    cardDesc = card[7]# + "\n\n" + card[8]
    if (len(card) > 8):
        cardDesc = cardDesc + "\n\n" + card[8]
    
    cardID = get_card_id(card)
    
    imgPath = directory + "/assets/art/" + card[0] + "/" + cardID + ".png"
    if (not os.path.exists(imgPath)):
        imgPath = ""
    
    advs = str.split(str(card[6]).replace(",", " "), " ")
    advantage = []
    disadvantage = []
    for adv in advs:
        #pdb.gimp_message(adv)
        if (adv.startswith('+')):
            advantage.append(adv[1:])
        if (adv.startswith('-')):
            disadvantage.append(adv[1:])
    
    descTextSize = 16
    if (len(card) >= 12):
        descTextSize = int(str(card[11]))
    if (descTextSize == None or descTextSize <= 0):
        descTextSize = 16
    
    return virtuoso_generate_card(card[2], card[3], subtypes[0], subtypes[1], stats[0], stats[1], stats[2], stats[3], cardDesc, cardID, imgPath, directory, advantage, disadvantage, border, descTextSize)

def generate_card_list(directory, card_list, outDir, border = None):
    for card in card_list:
        if (len(card) >= 8):
            img, layer = generate_card(directory, card, outDir, border)
            card_id = get_card_id(card)
            save_image_and_delete(img, layer, outDir + "/" + card_id + ".png")

def generate_card_atlas(directory, card_list, outDir):
    card_list = filter(lambda card: len(card) > 8, card_list)
    
    

def get_card_id(card):
    if (len(card) >= 2):
        card_id = str(card[1])
        while (len(card_id) < 3):
            card_id = "0" + card_id
        return card[0] + "-" + card_id

def save_image_and_delete(img, layer, path):
    if (path[-4:].upper() != ".PNG"):
        path = path + ".png"
    pdb.file_png_save(img, layer, path, path, 0, 0, 0, 0, 0, 0, 0)
    pdb.gimp_image_delete(img)

def load_json(directory):
    
    json_data = None
    with open(directory + "/cards.json", "r") as j:
        json_data = json.load(j)
    
    data = list(json_data.values())[0]
    
    return data

register(
        "python_fu_virtuoso_A",
        "Generate all Virtuoso cards.",
        "Generate all Virtuoso cards.",
        "playinful",
        "Virtuoso is a creation of AutumnHaunted",
        "February 2022",
        "<Toolbox>/File/Virtuoso/Generate all cards...",
        "",
        [
            (PF_DIRNAME,    'directory',    '"Virtuoso" project directory',   '.'),
            (PF_DIRNAME,    'outDir',       'Directory for output images',   '.'),
            (PF_TOGGLE,     'border',       'Add card border',        0)#,
            #(PF_TOGGLE,     'asAtlas',      'Export as texture atlas',        0)
        ],
        [],
        generate_all_cards)
register(
        "python_fu_virtuoso_B",
        "Generate a full set of Virtuoso cards.",
        "Generate a full set of Virtuoso cards.",
        "playinful",
        "Virtuoso is a creation of AutumnHaunted",
        "February 2022",
        "<Toolbox>/File/Virtuoso/Generate a set...",
        "",
        [
            (PF_DIRNAME,    'directory',    '"Virtuoso" project directory',   '.'),
            (PF_STRING,    'setID',        'Set ID',                         'XXXX'),
            (PF_DIRNAME,    'outDir',       'Directory for output images',   '.'),
            (PF_TOGGLE,     'border',       'Add card border',        0)#,
            #(PF_TOGGLE,     'asAtlas',      'Export as texture atlas',        0)
        ],
        [],
        generate_card_set)
register(
        "python_fu_virtuoso_C",
        "Generate a select list of Virtuoso cards.",
        "Generate a select list of Virtuoso cards.",
        "playinful",
        "Virtuoso is a creation of AutumnHaunted",
        "February 2022",
        "<Toolbox>/File/Virtuoso/Generate cards...",
        "",
        [
            (PF_DIRNAME,    'directory',    '"Virtuoso" project directory',   '.'),
            (PF_INT32,    'startInd',       'Starting index',   1),
            (PF_INT32,    'endInd',         'End index',   1),
            (PF_DIRNAME,    'outDir',       'Directory for output images',   '.'),
            (PF_TOGGLE,     'border',       'Add card border',        0)#,
        ],
        [],
        generate_select_cards)
register(
        "python_fu_virtuoso_D",
        "Generate a Virtuoso card.",
        "Generate a Virtuoso card.",
        "playinful",
        "Virtuoso is a creation of AutumnHaunted",
        "February 2022",
        "<Toolbox>/File/Virtuoso/Generate card...",
        "",
        [
            (PF_DIRNAME,    'directory',    '"Virtuoso" project directory',   '.'),
            (PF_STRING,    'cardID',       'The card ID',   'XXXX-000'),
            (PF_DIRNAME,    'outDir',       'Directory for output image',   '.'),
            (PF_STRING,    'outFile',       'Filename of output image',   'output.png'),
            (PF_TOGGLE,     'border',       'Add card border',        0)#,
        ],
        [],
        generate_single_card)

main()