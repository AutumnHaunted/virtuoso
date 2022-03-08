import random
from pyexcel_ods import get_data

CARD_RARITIES = [
    (0.5 , "CM"),
    (0.75, "AR"),
    (0.90, "BR"),
    (0.98, "GR"),
    (1   , "XR")
]
CARDS_BY_RARITY = {
    "CM": [],
    "AR": [],
    "BR": [],
    "GR": [],
    "XR": [],
}

# loading card data
def load_card_data(path):
    print("Loading data...")
    return list(get_data(path).values())[0]
def list_rarities(data):
    print("Processing...")
    for card in data:
        if (len(card) >= 10):
            rarities = str.split(str.replace(card[9], ",", " "), " ")
            for rarity in rarities:
                if (rarity in CARDS_BY_RARITY.keys()):
                    CARDS_BY_RARITY.get(rarity).append(card[2])
CARD_DATA = load_card_data('./gimp/cards.ods')
list_rarities(CARD_DATA)

def draw_card():
    random_float = random.random()
    rarity = CARD_RARITIES[0][1]
    for r, a in CARD_RARITIES:
        if (random_float <= r):
            rarity = a
            break
    card = "NO CARD"
    card_map = CARDS_BY_RARITY.get(rarity)
    if (len(card_map) > 0):
        card = random.choice(card_map)
    return card, rarity

def interface_main():
    while (True):
        draw_num = input("Type the number of cards you would like to draw: ")
        g = 1
        try:
            g = int(draw_num)
        except:
            print("Please specify a number.")
            continue
        if (g > 0):
            while (g > 0):
                card, rarity = draw_card()
                print('You draw "' + card + '" (' + rarity + ').')
                g = g - 1
        else:
            print("Please specify a number greater than zero.")
interface_main()