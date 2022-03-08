# ImageMagick
from wand.image   import Image
from wand.drawing import Drawing
from wand.font    import Font
from wand.color   import Color
import numpy
#import cv2

# other modules
import os
import sys
import re
import time
import json
import math
from pyexcel_ods import get_data

# declare path
ASSETS_PATH = "."

# our variables
BG_ASS = {
    "ENT": "/assets/entity_bg.bmp",
    "OBJ": "/assets/object_bg.bmp",
    "MAP": "/assets/map_bg.bmp",
    "EVN": "/assets/event_bg.bmp"
}
BG_ASS_BORDER = {
    "ENT": "/assets/entity_bg_border_10px.bmp",
    "OBJ": "/assets/object_bg_border_10px.bmp",
    "MAP": "/assets/map_bg_border_10px.bmp",
    "EVN": "/assets/event_bg_border_10px.bmp"
}
SYM_ASS = {
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
    "CTN": "/assets/sym_ctn.bmp",
    None:  "/assets/sym_null.bmp"
}
ON_OFF_ASS = {
    True: "ON",
    False: "OFF"
}

# special formatting rules
FORMAT_RULES = [
    {
        "type": "i",
        "regex": r'("[^"]*")'
    },
    {
        "type": "span",
        "regex": r'(\bLV\b\s*\d+|\bLV\b)',
        "bgcolor": "#FFCB21",
        "weight": "bold",
        "color": "black",
        "size": "eval{str(int((desc_font_size * (11/12)) * 1024))}",
        "padding": " "
    },
    {
        "type": "span",
        "regex": r'(\d+\s*\bHP\b|\bHP\b)',
        "bgcolor": "#13B226",
        "weight": "bold",
        "color": "black",
        "size": "eval{str(int((desc_font_size * (11/12)) * 1024))}",
        "padding": " "
    },
    {
        "type": "span",
        "regex": r'(\d+\s*\bATK\b|\bATK\b)',
        "bgcolor": "#FF2626",
        "weight": "bold",
        "color": "black",
        "size": "eval{str(int((desc_font_size * (11/12)) * 1024))}",
        "padding": " "
    },
    {
        "type": "span",
        "regex": r'(\d+\s*\bDEF\b|\bDEF\b)',
        "bgcolor": "#0C31FF",
        "weight": "bold",
        "color": "black",
        "size": "eval{str(int((desc_font_size * (11/12)) * 1024))}",
        "padding": " "
    },
    {
        "type": "span",
        "regex": r'(\b(FIG|STL|NML)\b)',
        "bgcolor": "#FF6D0C",
        "weight": "bold",
        "color": "black",
        "size": "eval{str(int((desc_font_size * (11/12)) * 1024))}",
        "padding": " "
    },
    {
        "type": "span",
        "regex": r'(\b(MOB|WLD|CTN)\b)',
        "bgcolor": "#0DFF39",
        "weight": "bold",
        "color": "black",
        "size": "eval{str(int((desc_font_size * (11/12)) * 1024))}",
        "padding": " "
    },
    {
        "type": "span",
        "regex": r'(\b(CON|IND)\b)',
        "bgcolor": "#FFD60C",
        "weight": "bold",
        "color": "black",
        "size": "eval{str(int((desc_font_size * (11/12)) * 1024))}",
        "padding": " "
    },
    {
        "type": "span",
        "regex": r'(\b(LEG|BTF)\b)',
        "bgcolor": "#FF0C0C",
        "weight": "bold",
        "color": "black",
        "size": "eval{str(int((desc_font_size * (11/12)) * 1024))}",
        "padding": " "
    },
    {
        "type": "span",
        "regex": r'(\b(HAU|LAI|RSP)\b)',
        "bgcolor": "#970AD8",
        "weight": "bold",
        "color": "black",
        "size": "eval{str(int((desc_font_size * (11/12)) * 1024))}",
        "padding": " "
    },
    {
        "type": "span",
        "regex": r'(\b(AST|MAG)\b)',
        "bgcolor": "#0C9AFF",
        "weight": "bold",
        "color": "black",
        "size": "eval{str(int((desc_font_size * (11/12)) * 1024))}",
        "padding": " "
    },
    {
        "type": "span",
        "regex": r'(\[\+\]\s?)',
        "bgcolor": "#0000FFFF",
        "replace": "                  ",
        "size": "9216"
    },
    {
        "type": "span",
        "regex": r'(\[\-\]\s?)',
        "bgcolor": "#FF00FFFF",
        "replace": "                  ",
        "size": "9216"
    }
]
FORMAT_COLORS = [ Color("#FFCB21FF"), Color("#13B226FF"), Color("#FF2626FF"), Color("#0C31FFFF"), Color("#FF6D0CFF"), Color("#0DFF39FF"), Color("#FFD60CFF"), Color("#FF0C0CFF"), Color("#970AD8FF"), Color("#0C9AFFFF"),
    Color("#0000FFFF"), Color("#FF00FFFF") ] # <-- Plus and minus

# our fonts
FONT_NAME    = Font(ASSETS_PATH + "/fonts/unispace rg.ttf"         ,             color=Color("#FFFFFF"))
FONT_STATS   = Font(ASSETS_PATH + "/fonts/PressStart2P-Regular.ttf", size=24   , color=Color("#FFFFFF"))
FONT_DESC    = Font(ASSETS_PATH + "/fonts/gadugi.ttf"              , size=16   , color=Color("#FFFFFF"))
FONT_DESC_SM = Font(ASSETS_PATH + "/fonts/gadugi.ttf"              ,             color=Color("#FFFFFF"))
FONT_ID      = Font(ASSETS_PATH + "/fonts/ntailu.ttf"              , size=11.25, color=Color("#FFFFFF"))
FONT_SIZES_NAME = [
    (29, 10),
    (28, 10),
    (26, 11),
    (24, 12),
    (23, 12),
    (21, 14),
    (19, 15)
]

# loading card data
def load_card_data(path):
    print("Loading data...")
    return list(get_data("cards.ods").values())[0]
CARD_DATA = load_card_data(ASSETS_PATH + '/cards.ods')

# main functions
def virtuoso_generate_card(card_data, assets_path, border = None, VERBOSE_MODE = False):
    
    # abort if card is invalid
    if (card_data != None and len(card_data) < 8):
        return (None, None, None)
    
    try:
        if (VERBOSE_MODE): print("Parsing card data...")
        # set some local variables
        art_offset = 44
        subtype_count = 0
        
        # determine card type and path
        BG_ASS_temp = BG_ASS
        if (border):
            BG_ASS_temp = BG_ASS_BORDER
        
        card_type = card_data[3].upper()
        card_bg_path = assets_path + BG_ASS_temp.get("EVN")
        if (BG_ASS_temp.get(card_type)):
            card_bg_path = assets_path + BG_ASS_temp.get(card_type)
        
        if (card_type == "ENT"):
            art_offset = 8
        
        # determine card subtype(s) and path
        card_subtypes = list(map(lambda x: x.upper(), str.split(card_data[4], "/")))[0:2]
        while (len(card_subtypes) < 2): # extend to 2 values
            card_subtypes.insert(0, None)
        card_subtype_paths = []
        for st in card_subtypes:
            if (SYM_ASS.get(st) and st != None):
                card_subtype_paths.append(assets_path + SYM_ASS.get(st))
                subtype_count += 1
            else:
                card_subtype_paths.append(assets_path + SYM_ASS.get(None))
        
        # determine card advantage(s)/disadvantage(s) and path
        card_advantages = []
        card_disadvantages = []
        for adv in str.split(card_data[6].upper().replace(",", " "), " "):
            if (len(adv) == 4):
                if (adv.startswith("+")):
                    card_advantages.append(adv[1:])
                elif (adv.startswith("-")):
                    card_disadvantages.append(adv[1:])
        card_advantage_paths = []
        card_disadvantage_paths = []
        for src_list, path_list in ((card_advantages, card_advantage_paths), (card_disadvantages, card_disadvantage_paths)):
            for adv in src_list:
                if (SYM_ASS.get(adv)):
                    path_list.append(assets_path + SYM_ASS.get(adv))
                else:
                    path_list.append(assets_path + SYM_ASS.get(None))
        
        # parse card stats
        card_stats = str.split(card_data[5], "/")[0:4]
        while (len(card_stats) < 4):
            card_stats.append("0")
        
        # parse card name
        card_name = card_data[2]
        
        # parse card description
        card_description = card_data[7]
        if (len(card_data) > 8):
            card_description += "\n\n" + card_data[8]
        card_description = re.sub(r'\n(?=\n)', "\n ", card_description) #adding spaces for debug purposes
        # ~~ apply modifiers ~~
        for rule in FORMAT_RULES:
            bgcolor = rule.get("bgcolor")
            
            replacement = "<" + rule.get("type")
            if (bgcolor            != None): replacement = replacement + ' bgcolor="' + bgcolor            + '"'
            if (rule.get("color" ) != None): replacement = replacement + ' color="'   + rule.get("color" ) + '"'
            if (rule.get("size"  ) != None): replacement = replacement + ' size="'    + rule.get("size"  ) + '"'
            if (rule.get("weight") != None): replacement = replacement + ' weight="'  + rule.get("weight") + '"'
            replacement = replacement + ">"
            if (bgcolor == None):
                bgcolor = "#00000000"
            if (rule.get("padding") != None): replacement = replacement + '<span color="' + bgcolor + '">' + rule.get("padding") + '</span>'
            if (rule.get("replace") != None):
                replacement = replacement + rule.get("replace")
            else:
                replacement = replacement + "\g<1>"
            if (rule.get("padding") != None): replacement = replacement + '<span color="' + bgcolor + '">' + rule.get("padding") + '</span>'
            replacement = replacement + "</" + rule.get("type") + ">"
            card_description = re.sub(rule.get("regex"), replacement, card_description)
        
        # parse card ID
        card_set_id = card_data[0]
        card_index = card_data[1]
        card_id = str(card_index)
        while (len(card_id) < 3):
            card_id = "0" + card_id
        card_id = card_set_id + "-" + card_id
        if (VERBOSE_MODE): print('Proccessing card ' + card_id + ' "' + card_name + '"...')
        
        # load card background
        if (VERBOSE_MODE): print("Loading card background...")
        card_bg_image = Image(filename=card_bg_path)
        
        # create new image
        assets_image = Image(width=card_bg_image.width, height=card_bg_image.height)
        
        # load subtype icon(s)
        if (VERBOSE_MODE): print("Loading subtype icon(s)...")
        for ind, st in zip(range(len(card_subtype_paths)), card_subtype_paths):
            assets_image.composite(Image(filename=st), left=396 + (ind * 40), top=12)
        
        # load advantage/disadvantage icon(s)
        if (VERBOSE_MODE): print("Loading advantage/disadvantage icon(s)...")
        if (card_type == "ENT"):
            if (len(card_advantages) > 0):
                assets_image.composite(Image(filename=card_advantage_paths[0]), left=424, top=334)
            if (len(card_disadvantages) > 0):
                assets_image.composite(Image(filename=card_disadvantage_paths[0]), left=424, top=396)
        
        # load card art
        if (VERBOSE_MODE): print("Loading card art...")
        card_art_path = assets_path + "/assets/art/" + card_set_id + "/" + card_id + ".png"
        if (os.path.exists(card_art_path)):
            assets_image.composite(Image(filename=card_art_path), left=art_offset, top=56)
        
        # --- draw texts ---
        
        # ~ draw name text ~ (TODO: test behaviour with centering and many subtype icons?)
        if (VERBOSE_MODE): print("Drawing name text...")
        # get header size
        header_size = 464 - (40 * subtype_count)# - 8
        if (card_type == "ENT" and header_size > 392):
            header_size = 392
        if (header_size == 464 or header_size == 392):
            header_size -= 4
        header_size -= 4
        # generate text
        name_text_image = Image(width=header_size,height=40)
        name_text_drawing = Drawing()
        name_text_drawing.font = FONT_NAME.path
        name_text_drawing.fill_color = Color("white")
        name_text_drawing.gravity = "center"
        # find a good size
        name_text_offset = 0
        for size, offset in FONT_SIZES_NAME:
            name_text_drawing.font_size = size
            name_text_offset = offset
            if (name_text_drawing.get_font_metrics(name_text_image, card_name).text_width > header_size):
                continue
            else:
                break
        name_text_drawing.text(0, 0, card_name)
        if (name_text_drawing.get_font_metrics(name_text_image, card_name).text_width > header_size):
            name_text_image = Image(width=int(name_text_drawing.get_font_metrics(name_text_image, card_name).text_width), height=40)
            name_text_drawing(name_text_image)
            name_text_image.resize(width=header_size, height=40)
        else:
            name_text_drawing(name_text_image)
        assets_image.composite(name_text_image, left=12, top=8)
        
        # draw stats text
        if (VERBOSE_MODE): print("Drawing stats...")
        if (card_type == "ENT"):
            for stat, y in zip(card_stats, [70,132,194,256]):
                assets_image.caption(stat, left=410, top=y, width=60, height=44, font=FONT_STATS, gravity="center")
        
        # draw description text
        if (VERBOSE_MODE): print("Drawing description text...")
        description_image = Image(width=460, height=309)
        if (border):
            description_image = Image(width=460, height=317)
        description_image.options["background"] = "#00000000"
        desc_font_size = 12.0
        font_face = "Lato"
        while (True):
            draw_description = card_description
            
            # parse description for evals
            eval_search = re.search(r'eval{([^}]*)}', draw_description)
            while (eval_search):
                eval_expression = eval_search.group()[5:-1]
                draw_description = draw_description[:eval_search.start()] + eval(eval_expression) + draw_description[eval_search.end():]
                #print(draw_description)
                eval_search = re.search(r'eval{([^}]*)}', draw_description)
            
            description_image.pseudo(description_image.width, description_image.height, 'pango:<span face="' + font_face + '" bgcolor="black" color="white"  size="' + str(int(desc_font_size * 1024)) + '">' + draw_description + '</span>')
            if (description_image[0,description_image.height-100].string != "srgba(0,0,0,0)" and desc_font_size > 0.25): # test if the bottom-leftmost pixel is transparent
                description_image = Image(width=description_image.width, height=description_image.height)
                description_image.options["background"] = "#00000000"
                desc_font_size = desc_font_size - 0.25
                continue
            else:
                break
        description_image.merge_layers("merge")
        # colour formatting
        numpy_image = numpy.array(description_image)
        color_coords = []
        for c in FORMAT_COLORS:
            c_list = [c.red_int8, c.green_int8, c.blue_int8, c.alpha_int8]
            x, y = numpy.where(numpy.all(numpy_image==c_list,axis=2))
            color_coords.extend(zip(x,y))
            # draw description text
        if (VERBOSE_MODE): print("Drawing description text...")
        description_image = Image(width=460, height=309)
        if (border):
            description_image = Image(width=460, height=317)
        description_image.options["background"] = "#00000000"
        desc_font_size = 12.0
        font_face = "Lato"
        while (True):
            draw_description = card_description
            
            # parse description for evals
            eval_search = re.search(r'eval{([^}]*)}', draw_description)
            while (eval_search):
                eval_expression = eval_search.group()[5:-1]
                draw_description = draw_description[:eval_search.start()] + eval(eval_expression) + draw_description[eval_search.end():]
                #print(draw_description)
                eval_search = re.search(r'eval{([^}]*)}', draw_description)
            
            description_image.pseudo(description_image.width, description_image.height, 'pango:<span face="' + font_face + '" bgcolor="black" color="white"  size="' + str(int(desc_font_size * 1024)) + '">' + draw_description + '</span>')
            if (description_image[0,description_image.height-100].string != "srgba(0,0,0,0)" and desc_font_size > 0.25): # test if the bottom-leftmost pixel is transparent
                description_image = Image(width=description_image.width, height=description_image.height)
                description_image.options["background"] = "#00000000"
                desc_font_size = desc_font_size - 0.25
                continue
            else:
                break
        temp_image = Image(width=description_image.width+4,height=description_image.height+1,background=Color("#00000000"))
        description_image.merge_layers("merge")
        temp_image.composite(description_image,top=1,left=2)
        description_image = temp_image # we're putting the description image onto a slightly bigger image because it fucks with the formatting otherwise
        # colour formatting
        if (VERBOSE_MODE): print("Marking up text...")
        numpy_image = numpy.array(description_image)
        color_coords = []
        for c in FORMAT_COLORS:
            c_list = [c.red_int8, c.green_int8, c.blue_int8, c.alpha_int8]
            x, y = numpy.where(numpy.all(numpy_image==c_list,axis=2))
            color_coords = []
            color_coords.extend(zip(x,y))
            #for x, y in color_coords: # corner detection
            color_coords = numpy.array(color_coords)
            color_boxes = []
            while (color_coords.size>0):
                # find all four coordinates
                topmost, leftmost  = color_coords[0]
                condition = color_coords==[topmost,0]
                x1 = numpy.where(condition)[0]
                rightmost = color_coords[numpy_consecutive(x1)[0][-1]][1]
                condition = color_coords==[0,rightmost]
                x2 = numpy.where(condition)[0]
                ys = color_coords[x2].swapaxes(0,1)[0]
                bottommost = numpy_consecutive(ys)[0][-1]
                
                #print(leftmost,end=",")
                #print(topmost,end=",")
                #print(rightmost,end=",")
                #print(bottommost)
                
                # append color box
                color_boxes.append((leftmost,topmost,rightmost,bottommost))
                #print((leftmost,topmost,rightmost,bottommost))
                
                # remove areas in list with coordinates
                colors_y, colors_x = color_coords.swapaxes(0,1)
                color_coords = color_coords[numpy.where(numpy.logical_or(numpy.logical_or(colors_x<leftmost,colors_x>rightmost),numpy.logical_or(colors_y<topmost,colors_y>bottommost)))]
            
            # mark up color boxes
            for left, top, right, bottom in color_boxes:
                if (description_image[left,top] in [ Color("#0000FFFF"), Color("#FF00FFFF") ]):
                    #TODO
                    filler_image = Image(width=right-left+1,height=bottom-top+1,background=Color("#000000"))
                    inline_icon_image = None
                    if (description_image[left,top] == Color("#0000FFFF")):
                        inline_icon_image = Image(filename=ASSETS_PATH+"/assets/advantage.bmp")
                    elif (description_image[left,top] == Color("#FF00FFFF")):
                        inline_icon_image = Image(filename=ASSETS_PATH+"/assets/disadvantage.bmp")
                    midpoint = math.ceil(filler_image.height / 2)
                    filler_image.composite(inline_icon_image,left=1,top=midpoint - int(inline_icon_image.height / 2))
                    description_image.composite(filler_image,left=left,top=top)
                else:
                    if (right-left > 3 and bottom-top > 3):
                        # adjust text slightly
                        text_adjust = Image(description_image)
                        text_adjust.crop(left=left,top=top+1,width=right-left+1,height=bottom-top)
                        description_image.composite(text_adjust,left=left,top=top)
                        # draw box corners
                        box_base = Image(width=right-left+1,height=bottom-top+1,background=Color("#00000000")).convert("PNG")
                        corner_image = Image(filename=ASSETS_PATH+"/assets/corner.png")
                        box_base.composite(corner_image,left=left-left,top=top-top)
                        corner_image.rotate(90)
                        box_base.composite(corner_image,left=right-left-1,top=top-top)
                        corner_image.rotate(90)
                        box_base.composite(corner_image,left=right-left-1,top=bottom-top-1)
                        corner_image.rotate(90)
                        box_base.composite(corner_image,left=left-left,top=bottom-top-1)
                        # composite corners onto desc image
                        description_image.composite(box_base,left=left,top=top)
        ##for x, y in color_coords: # corner detection
        #color_coords = numpy.array(color_coords)
        #color_boxes = []
        #while (color_coords.size>0):
        #    # find all four coordinates
        #    topmost, leftmost  = color_coords[0]
        #    condition = color_coords==[topmost,0]
        #    x1 = numpy.where(condition)[0]
        #    rightmost = color_coords[numpy_consecutive(x1)[0][-1]][1]
        #    condition = color_coords==[0,rightmost]
        #    x2 = numpy.where(condition)[0]
        #    ys = color_coords[x2].swapaxes(0,1)[0]
        #    bottommost = numpy_consecutive(ys)[0][-1]
        #    
        #    #print(leftmost,end=",")
        #    #print(topmost,end=",")
        #    #print(rightmost,end=",")
        #    #print(bottommost)
        #    
        #    # append color box
        #    color_boxes.append((leftmost,topmost,rightmost,bottommost))
        #    print((leftmost,topmost,rightmost,bottommost))
        #    
        #    # remove areas in list with coordinates
        #    colors_y, colors_x = color_coords.swapaxes(0,1)
        #    color_coords = color_coords[numpy.where(numpy.logical_or(numpy.logical_or(colors_x<leftmost,colors_x>rightmost),numpy.logical_or(colors_y<topmost,colors_y>bottommost)))]
        #
        ## mark up color boxes
        #for left, top, right, bottom in color_boxes:
        #    if (description_image[left,top] in [ Color("#0000FFFF"), Color("#FF00FFFF") ]):
        #        #TODO
        #        filler_image = Image(width=right-left+1,height=bottom-top+1,background=Color("#000000"))
        #        inline_icon_image = None
        #        if (description_image[left,top] == Color("#0000FFFF")):
        #            inline_icon_image = Image(filename=ASSETS_PATH+"/assets/advantage.bmp")
        #        elif (description_image[left,top] == Color("#FF00FFFF")):
        #            inline_icon_image = Image(filename=ASSETS_PATH+"/assets/disadvantage.bmp")
        #        midpoint = int(filler_image.height / 2)
        #        filler_image.composite(inline_icon_image,left=0,top=midpoint - int(inline_icon_image.height / 2))
        #        description_image.composite(filler_image,left=left,top=top)
        #    else:
        #        if (right-left > 3 and bottom-top > 3):
        #            # adjust text slightly
        #            text_adjust = Image(description_image)
        #            text_adjust.crop(left=left,top=top+1,width=right-left+1,height=bottom-top)
        #            description_image.composite(text_adjust,left=left,top=top)
        #            # draw box corners
        #            box_base = Image(width=right-left+1,height=bottom-top+1,background=Color("#00000000")).convert("PNG")
        #            corner_image = Image(filename=ASSETS_PATH+"/assets/corner.png")
        #            box_base.composite(corner_image,left=left-left,top=top-top)
        #            corner_image.rotate(90)
        #            box_base.composite(corner_image,left=right-left-1,top=top-top)
        #            corner_image.rotate(90)
        #            box_base.composite(corner_image,left=right-left-1,top=bottom-top-1)
        #            corner_image.rotate(90)
        #            box_base.composite(corner_image,left=left-left,top=bottom-top-1)
        #            # composite corners onto desc image
        #            description_image.composite(box_base,left=left,top=top)
        
        assets_image.composite(description_image, left=8, top=457)
        
        # draw ID text
        if (VERBOSE_MODE): print("Drawing ID text...")
        id_image = Image(height=209, width=464)
        if (border):
            id_image = Image(height=217, width=464)
        id_drawing = Drawing()
        id_drawing.text_antialias = False
        id_drawing.font = FONT_ID.path
        id_drawing.fill_color = FONT_ID.color
        id_drawing.font_size = FONT_ID.size
        id_drawing.gravity = "south_east"
        id_drawing.text(0, 0, "V:/" + card_id)
        id_drawing(id_image)
        assets_image.composite(id_image, left=8, top=456)
        
        card_border_left = 0
        card_border_top = 0
        if (border):
            card_border_left = 10
            card_border_top  = 10
        
        card_bg_image.composite(assets_image, left=card_border_left, top=card_border_top) # layer assets onto image
        return (card_bg_image.convert("png"), card_id, card_name)
    except Exception as err:
        raise(err)
        return (None, None, None)

def generate_all_cards(outDir, border = None, VERBOSE_MODE = False):
    outDir = make_path(outDir)
    generate_card_list(CARD_DATA, outDir, border, VERBOSE_MODE)
def generate_select_cards(startInd, endInd, outDir, border = None, VERBOSE_MODE = False):
    
    outDir = make_path(outDir)
    
    if (endInd < startInd):
        print("The end index must be larger than the starting index.")
        return None
    
    if (startInd == 0 or endInd == 0):
        startInd += 1
        endInd += 1
    
    card_range = CARD_DATA[startInd-1:endInd]
    
    generate_card_list(card_range, outDir, border, VERBOSE_MODE)
def generate_card_set(setID, outDir, border = None, VERBOSE_MODE = False):
    
    outDir = make_path(outDir)
    
    setID = setID.upper()
    select_cards = []
    for card in CARD_DATA:
        if (len(card) >= 8 and card[0] == setID):
            select_cards.append(card)
    
    generate_card_list(select_cards, outDir, border, VERBOSE_MODE)
def generate_single_card(cardID, outPath, border = None, VERBOSE_MODE = False):
    cardID = cardID.upper()
    cardIdArr = str.split(cardID, "-")
    
    if (not outPath.upper().endswith(".PNG")):
        outPath = outPath + ".png"
    
    outPath = make_path_file(outPath)
    
    card = None
    for x in CARD_DATA:
        if (len(x) >= 2):
            if (x[0] == cardIdArr[0] and int(x[1]) == int(cardIdArr[1])):
                card = x
                break
    
    if (card is None):
        print("Could not find that card.")
        return None
    
    start_time = time.time()
    image, card_id, card_name = virtuoso_generate_card(card, ASSETS_PATH, border, VERBOSE_MODE)
    
    if (VERBOSE_MODE): print("Saving image...")
    image.save(filename=outPath)
    
    time_elapsed = time.time() - start_time
    if (not VERBOSE_MODE): time_elapsed = round(time_elapsed, 3)
    print('Saved card ' + card_id + ' "' + card_name + '" as "' + outPath + '". Time elapsed: ' + str(time_elapsed) + ' seconds.')

def generate_card_list(card_list, outDir, border = None, VERBOSE_MODE = False):
    master_start_time = time.time()
    for card in card_list:
        try:
            start_time = time.time()
            image, card_id, card_name = virtuoso_generate_card(card, ASSETS_PATH, border, VERBOSE_MODE)
            
            if (VERBOSE_MODE): print("Saving image...")
            out_path = outDir + "/" + card_id + ".png"
            image.save(filename=out_path)
            
            time_elapsed = time.time() - start_time
            if (not VERBOSE_MODE): time_elapsed = round(time_elapsed, 3)
            print('Saved card ' + card_id + ' "' + card_name + '" as "' + out_path + '". Time elapsed: ' + str(time_elapsed) + ' seconds.')
        except:
            pass
    time_elapsed = time.time() - master_start_time
    if (not VERBOSE_MODE): time_elapsed = round(time_elapsed, 3)
    print("Process completed in " + str(time_elapsed) + " seconds.")

#other functions
def make_path(path):
    path = re.sub(r'[\\/]+', "/", path)
    if (os.path.isdir(path)):
        return path
    else:
        master_path = ""
        for file_dir in str.split(path, "/"):
            master_path = master_path + file_dir + "/"
            if (not os.path.exists(master_path)):
                os.mkdir(master_path)
        print('Created path "' + path +'".')
        return path
def make_path_file(path):
    path = re.sub(r'[\\/]+', "/", path)
    filename = "/".join(str.split(path, "/")[:-1])
    if (len(filename) > 0): make_path(filename)
    return path
def numpy_consecutive(data, stepsize=1):
    return numpy.split(data, numpy.where(numpy.diff(data) != stepsize)[0]+1)

# interface functions
def interface_main():
    VERBOSE_MODE = False
    while (True):
        gen_mode = input("\nWelcome to the Virtuoso Card Generator. What would you like to do?\n(A): Generate a single card.\n(B): Generate a range of cards.\n(C): Generate a set of cards.\n(D): Generate all cards.\n(V): Turn verbose mode " + ON_OFF_ASS.get(not VERBOSE_MODE) + ".\n(X): Exit.\n\nType the letter of your answer: ")
        if (len(gen_mode) > 0):
            gen_mode = gen_mode[0].upper()
        if (gen_mode == "A"):
            card_id = input("Type the ID of the card you wish to generate (XXXX-000): ")
            path = interface_get_path("Type the path to the output file: ")
            border = interface_choiceYN("Use card borders? (Y/N): ")
            generate_single_card(card_id, path, border, VERBOSE_MODE)
        elif (gen_mode == "B"):
            start_ind = interface_int("Type the index of the first card to generate: ")
            end_ind   = interface_int("Type the index of the last card to generate: ")
            path = interface_get_path("Type the path to the output directory: ")
            border = interface_choiceYN("Use card borders? (Y/N): ")
        elif (gen_mode == "C"):
            set_id = input("Type the ID of the set you wish to generate (XXXX): ")
            path = interface_get_path("Type the path to the output directory: ")
            border = interface_choiceYN("Use card borders? (Y/N): ")
            generate_card_set(set_id, path, border, VERBOSE_MODE)
        elif (gen_mode == "D"):
            path = interface_get_path("Type the path to the output directory: ")
            border = interface_choiceYN("Use card borders? (Y/N): ")
            generate_all_cards(path, border, VERBOSE_MODE)
        elif (gen_mode == "X"):
            print("Goodbye.")
            break
        elif (gen_mode == "V"):
            VERBOSE_MODE = not VERBOSE_MODE
            print("Verbose mode " + ON_OFF_ASS.get(VERBOSE_MODE) + ".")

def interface_get_path(message):
    return input(message)
    return None
def interface_choiceYN(message):
    confirm = ""
    while (True):
        confirm = input(message)
        if (len(confirm) > 0 and confirm.upper()[0] == "Y"):
            return True
        elif (len(confirm) > 0 and confirm.upper()[0] == "N"):
            return False
def interface_int(message):
    choice = -1
    while (True):
        choice = input(message)
        try:
            choice = int(choice)
            return choice
        except:
            print("That's not a valid integer.")

interface_main()