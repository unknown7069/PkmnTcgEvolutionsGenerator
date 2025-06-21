import pandas 
import os 
from PIL import Image, ImageDraw, ImageFont
import glob 
import textwrap
import time 
import itertools
from collections import namedtuple
import logging 
# Set up a basic logger, filter out to only this logger and set it to debug 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


this_dir = os.path.dirname(os.path.dirname(__file__))

OUTPUT_DIR = os.path.join(this_dir, 'generated_cards')

OUTPUT_SIZE = (734, 1024)

COLOR_BLACK = (0, 0, 0, 255)
COLOR_BLACK_FLAVOR = (0, 0, 0, 170)
COLOR_WHITE = (255, 255, 255, 255)
COLOR_WHITE_FLAVOR = (255, 255, 255, 170)
COLOR_EMPTY = (0, 0, 0, 0)
COLOR_GREY = (200, 200, 200, 255)

COLOR_RED = (235, 30, 45, 255)
COLOR_BLUE = (11, 97, 174, 255)

TEXTURE = {card_path.split('\\')[-1].split('.')[0]: card_path 
           for card_path in glob.glob(os.path.join(this_dir, 'resource/card_textures/*'))}
assert len(TEXTURE) > 0, TEXTURE
SYMBOLS = {card_path.split('\\')[-1].split('.')[0]: card_path 
           for card_path in glob.glob(os.path.join(this_dir, 'resource/card_symbols/*'))}

SYMBOLS.update({name[0].upper(): path for name, path in SYMBOLS.items()})
SYMBOLS['D'] = SYMBOLS['dark']
SYMBOLS['R'] = SYMBOLS['fighting']
SYMBOLS['Y'] = SYMBOLS['psychic']

SYMBOL_LARGE_SIZE = (55, 55)
SYMBOL_MEDIUM_SIZE = (39, 39)
SYMBOL_SMALL_SIZE = (34, 34)
assert len(SYMBOLS) > 0, SYMBOLS

_FONT_GILL = os.path.join(this_dir, "resource/fonts/gill-sans-2/")
_FONT_FUTURA = os.path.join(this_dir, "resource/fonts/futura/")
_FONT_SIMPLO = os.path.join(this_dir, "resource/fonts/Simplo/")
_FONT_HUMANIST = os.path.join(this_dir, "resource/fonts/humanist521-bt/")
_FONT_FRUTIGER = os.path.join(this_dir, "resource/fonts/frutiger/")
_FONT_FRUTIGER_PRO = os.path.join(this_dir, "resource/fonts/frutiger-lt-pro/")

# Usually gill sans, humanist, futura, frutiger are your go to's


# CARD TOP 

FONT_NAME = ImageFont.truetype(_FONT_GILL + "GillSans Condensed Bold.otf", 55)
FONT_NAME_TIGHT = ImageFont.truetype(_FONT_GILL + "GillSans Condensed Bold.otf", 48)
FONT_NAME_LOCATION = (68, 75)
FONT_NAME_TIGHT_OFFSET = 5
FONT_NAME_STAGE_LOCATION = (193, 75)


FONT_HP = ImageFont.truetype(_FONT_GILL + "Gill Sans Medium.otf", 47)
FONT_HP_LOCATION_3 = (489-24, 80)
FONT_HP_LOCATION_2 = (489, 80)
FONT_HP_LOCATION_HP = (549, 80)

FONT_BASIC = ImageFont.truetype(_FONT_GILL + "GillSans Condensed Bold.otf", 24)
FONT_BASIC_LOCATION = (75, 30)

FONT_EVOLVES_FROM = ImageFont.truetype(_FONT_GILL + "Gill Sans Bold Italic.otf", 21)
# FONT_EVOLVES_FROM = ImageFont.truetype(_FONT_FRUTIGER + "Frutiger.ttf", 21)
# FONT_EVOLVES_FROM = ImageFont.truetype(_FONT_FRUTIGER_PRO + "Linotype  FrutigerLTProBoldCnIta.otf", 21)

FONT_EVOLVES_FROM_LOCATION = (162, 38)

FONT_PUT_ON = ImageFont.truetype(_FONT_GILL + "Gill Sans Medium.otf", 18)
FONT_PUT_ON_LOCATION = (663, 39)

FONT_LVL = ImageFont.truetype(_FONT_SIMPLO + "Simplo-Black.otf", 20)
FONT_LVL_LOCATION_2 = (424, 97)
FONT_LVL_LOCATION_3 = (424-24, 97)


# CARD TOP MIDDLE 

FONT_INFO_BAR_LOCATION = (368, 576)
# FONT_INFO_BAR = ImageFont.truetype(_FONT_GILL + "GillSans Condensed Bold.otf", 25)
FONT_INFO_BAR = ImageFont.truetype(_FONT_GILL + "Gill Sans Bold Italic.otf", 25)


# CARD MIDDLE  

FONT_MOVE_TITLE = ImageFont.truetype(_FONT_GILL + "GillSans Condensed Bold.otf", 40)
FONT_MOVE_DESCRIPTION_LARGE = ImageFont.truetype(_FONT_GILL + "Gill Sans Medium.otf", 30)
FONT_MOVE_DESCRIPTION_MEDIUM = ImageFont.truetype(_FONT_GILL + "Gill Sans Medium.otf", 24)
FONT_MOVE_DESCRIPTION_SMALL = ImageFont.truetype(_FONT_GILL + "Gill Sans Medium.otf", 20)
FONT_MOVE_SIZES = (FONT_MOVE_DESCRIPTION_LARGE, FONT_MOVE_DESCRIPTION_MEDIUM, FONT_MOVE_DESCRIPTION_SMALL)
FONT_MOVE_REAL_HEIGHT = (FONT_MOVE_DESCRIPTION_LARGE.getbbox('X')[3] - FONT_MOVE_DESCRIPTION_LARGE.getbbox('X')[1],
                       FONT_MOVE_DESCRIPTION_MEDIUM.getbbox('X')[3] - FONT_MOVE_DESCRIPTION_MEDIUM.getbbox('X')[1],
                       FONT_MOVE_DESCRIPTION_SMALL.getbbox('X')[3] - FONT_MOVE_DESCRIPTION_SMALL.getbbox('X')[1])
FONT_MOVE_DAMAGE = ImageFont.truetype(_FONT_GILL + "Gill Sans Medium.otf", 50)

move_details = namedtuple('move_details', ['font', 'initial_gap', 'text_space', 'text_height', 'char_width'])

# CARD BOTTOM 

FONT_WEAKNESS = ImageFont.truetype(_FONT_GILL + "GillSans Condensed Bold.otf", 18)
FONT_WEAKNESS_LOCATION = (74, 888)
FONT_WEAKNESS_NUMBER = ImageFont.truetype(_FONT_GILL + "Gill Sans Medium.otf", 28)
FONT_RESISTANCE_LOCATION = (227, 888)
FONT_RETREAT_LOCATION = (83, 927)
SYMBOL_WEAKNESS_LOCATION = (152, 879)
SYMBOL_RESISTANCE_LOCATION = (311, 879)
SYMBOL_RETREAT_LOCATION = (152, 924)

FONT_DESCRIPTION = ImageFont.truetype(_FONT_GILL + "Gill Sans Bold Italic.otf", 15)
FONT_DESCRIPTION_LOCATION = (411, 879)

# CARD VERY BOTTOM 

FONT_ARTIST = ImageFont.truetype(_FONT_GILL + "GillSans Condensed Bold.otf", 16)
FONT_ARTIST_LOCATION = (42, 977)
FONT_COPYRIGHT = ImageFont.truetype(_FONT_GILL + "Gill Sans Medium.otf", 14)
FONT_COPYRIGHT_LOCATION = (317, 977)
SYMBOL_RARITY_LOCATION = (654, 976)
SYMBOL_EXPANSION_LOCATION = (673, 971)
FONT_SET_NUMBER_LOCATION = (647, 977)



def get_weakness(type_1, type_2=None):
    if type_1 == 'normal' and type_2 is not None:
        type_1 = type_2
    if type_1 == 'normal':
        return 'fighting'
    elif type_1 == 'fighting':
        return 'psychic'
    elif type_1 == 'flying':
        return 'electric'
    elif type_1 in ('grass', 'bug'):
        return 'fire'
    elif type_1 == 'water':
        return 'grass'
    elif type_1 == 'ice':
        return 'steel'
    elif type_1 == 'fire':
        return 'water'
    elif type_1 == 'fighting':
        return 'psychic'
    elif type_1 == 'rock':
        return 'grass'
    elif type_1 == 'ground':
        return 'grass'
    elif type_1 == 'psychic':
        return 'dark'
    elif type_1 == 'ghost':
        return 'dark'
    elif type_1 == 'fairy':
        return 'dark'
    elif type_1 == 'electric':
        return 'fighting'
    elif type_1 == 'dark':
        return 'fighting'
    elif type_1 == 'poison':
        return 'fighting'
    elif type_1 == 'steel':
        return 'fire'
    elif type_1 == 'dragon':
        return None 
    return None 


def get_resistance(type_1, type_2=None):
    if type_1 == 'normal' and type_2 is not None:
        type_1 = type_2
    if type_1 == 'normal':
        return None
    elif type_1 == 'flying':
        return 'fighting'
    elif type_1 in ('grass', 'bug'):
        return None 
    elif type_1 == 'water':
        return None 
    elif type_1 == 'ice':
        return None 
    elif type_1 == 'fire':
        return None 
    elif type_1 == 'fighting':
        return None 
    elif type_1 == 'rock':
        return None 
    elif type_1 == 'ground':
        return 'electric'
    elif type_1 == 'psychic':
        return 'fighting'
    elif type_1 == 'ghost':
        return 'fighting'
    elif type_1 == 'electric':
        return 'steel'
    elif type_1 == 'dark':
        return 'psychic'
    elif type_1 == 'fairy':
        return None 
    elif type_1 == 'poison':
        return None 
    elif type_1 == 'steel':
        return 'grass'
    elif type_1 == 'dragon':
        return None 


def get_card_type(type_1, type_2=None):
    if type_1 == 'normal' and type_2 is not None:
        type_1 = type_2
    if type_1 == 'rock':
        type_1 = 'fighting'
    elif type_1 == 'ground':
        type_1 = 'fighting'
    elif type_1 == 'ice':
        type_1 = 'water'
    elif type_1 == 'bug':
        type_1 = 'grass'
    elif type_1 == 'poison':
        type_1 = 'dark'
    elif type_1 == 'flying':
        type_1 = 'colorless'
    elif type_1 == 'normal':
        type_1 = 'colorless'
    elif type_1 == 'fairy':
        type_1 = 'psychic'
    return type_1


def open_resize_paste(main_image, other_image_path, resize=OUTPUT_SIZE, keep_resize_ratio=False, location=(0,0), center=False):
    if other_image_path is None:
        return main_image
    other_image = Image.open(os.path.join(this_dir, other_image_path), mode='r').convert('RGBA')
    if resize is not None:
        if keep_resize_ratio:
            # Get the larger of the two ratios
            if resize[0] / other_image.size[0] > resize[1] / other_image.size[1]:
                # Using the ratio of the existing width, calculate the new height
                resize = (int(resize[1] * other_image.size[0] / other_image.size[1]), resize[1])
            else:
                # Using the ratio of the existing height, calculate the new width
                resize = (resize[0], int(resize[0] * other_image.size[1] / other_image.size[0]))
        other_image = other_image.resize(resize)
    if center:
        location = (location[0] - other_image.size[0] // 2, location[1] - other_image.size[1] // 2)
    main_image.paste(other_image, location, other_image)
    return main_image

def paste_symbol(main_image, other_image_path, size=2, location=(0, 0)):
    other_image = Image.open(other_image_path, mode='r').convert('RGBA')
    if size == 3:
        size = SYMBOL_LARGE_SIZE
    elif size == 2:
        size = SYMBOL_MEDIUM_SIZE
    elif size == 1:
        size = SYMBOL_SMALL_SIZE
    else:
        raise ValueError('Invalid size')
    other_image = other_image.resize(size)
    main_image.paste(other_image, location, other_image)
    return main_image


def get_icon(name):
    icons = glob.glob(os.path.join(this_dir, 'resource', 'pokemon_art', '*' + name.lower() + '*' + '.png'))
    if icons:
        return icons[0]

def get_card_type(type_1, type_2=None):
    if type_1 == 'rock':
        type_1 = 'fighting'
    elif type_1 == 'ground':
        type_1 = 'fighting'
    elif type_1 == 'ice':
        type_1 = 'water'
    elif type_1 == 'bug':
        type_1 = 'grass'
    elif type_1 == 'poison':
        type_1 = 'dark'
    elif type_1 == 'flying':
        type_1 = 'colorless'
    elif type_1 == 'normal':
        type_1 = 'colorless'
    elif type_1 == 'ghost':
        type_1 = 'psychic'
    elif type_1 == 'fairy':
        type_1 = 'psychic'
    return type_1


def get_text_color(type_1, type_2=None):
    # The color of the text on the card
    if get_card_type(type_1) in ('dark', 'dragon'):
        return COLOR_WHITE, COLOR_WHITE_FLAVOR
    return COLOR_BLACK, COLOR_BLACK_FLAVOR

def get_ability_color(type_1, type_2=None):
    # The color of the ability text
    if get_card_type(type_1) == 'fire':
        return COLOR_BLUE
    return COLOR_RED


def draw_text(draw, text, font, bottom_xy, max_height, max_width, text_color):
    """
    :param ImageDraw.Draw draw
    """
    width = draw.textlength(text, font)
    font_size = min(max_width / width, 1)
    width = draw.textlength(text, font, font_size=int(25 * font_size))
    draw_x = bottom_xy[0]
    draw_y = bottom_xy[1]
    draw.text((draw_x, draw_y), text, font=font, fill=text_color, anchor='ma')

KEYWORDS = ['paralyzed', 'poisoned', 'confused', 'burned', 'active', 'pokemon', 'pokemon\'s' 'special', 'energy', 
'benched', 'basic', 'weakness', 'resistance', 'defending']
def capitalise_keywords(phrase):
    resp=""
    v = phrase.split()
    for x in v:
        if x.lower() not in KEYWORDS:
            resp += (" " + x)
        else:
            resp += (" " + x.capitalize())

    resp = resp.replace('Pokemon', 'Pokémon')  # Use the correct e 
    return resp.strip()


def get_all_word_widths(text, font):
    # This returns the width of each word in the text 
    words = text.split(" ")
    word_widths = {}
    for word in words:
        word_widths[word] = font.getbbox(word)[2] - font.getbbox(word)[0]
    return word_widths


def get_lines_required(text, font, max_width):
    # This returns the number of lines required to display the text in the given font and max width 
    words = text.split(" ")
    minimum_space = 8  # font.getbbox(' ')[2] - font.getbbox(' ')[0]  # Space width
    lines = 0
    current_width = 0
    character_count = 0 
    max_character_count = 0
    for word in words:
        word_width = font.getbbox(word)[2] - font.getbbox(word)[0]
        if current_width + word_width > max_width:
            lines += 1
            current_width = 0
            max_character_count = max(max_character_count, character_count)
            character_count = 0
        
        character_count += len(word) + 1 # +1 for the space
        current_width += word_width + minimum_space  # Add space width
    if current_width > 0:
        lines += 1
        max_character_count = max(max_character_count, character_count)
    return lines, max_character_count 


def justify_text(draw, maxwidth, **kwargs):
    # This draws text with justified spacing between words
    words = kwargs['text'].split(" ")
    words_length = sum(draw.textlength(w, font=kwargs['font']) for w in words)
    space_length = (maxwidth - words_length) / (len(words) - 1)
    x = kwargs['xy'][0]
    y = kwargs['xy'][1]
    for word in words:
        kwargs.update({'xy': (x, y), 'text': word})
        draw.text(**kwargs)
        x += draw.textlength(word, font=kwargs['font']) + space_length


def squash_text(real_image, original_draw, maxwidth, minxratio=1, *args, **kwargs):
    # This draws text with reduced spacing between words to fit a max width 
    base_width = original_draw.textlength(kwargs['text'], kwargs['font'])
    xratio = min(maxwidth / base_width, minxratio)
    if xratio == 1:
        original_draw.text(*args, **kwargs)
        return 
    
    text_layer = Image.new('RGBA', OUTPUT_SIZE, COLOR_EMPTY)
    draw = ImageDraw.Draw(text_layer)
    draw.text(*args, **kwargs)
    text_layer = text_layer.resize((int(text_layer.size[0] * xratio), int(text_layer.size[1])))
    real_image.paste(text_layer, (int(kwargs['xy'][0] * (1 - xratio)), 0), text_layer)

def safe_int(value, default=0):
    """Safely convert a value to an integer, returning a default if conversion fails."""
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


class Card(object):
    def __init__(self, existing, id, name, type1, type2, weight, height, genus, hp, level, stage, 
                 prev_evolution_name, next_evolution_name, ability_name, ability, 
                 move_1_name, move_1_cost, move_1_damage, move_1_symbol, move_1_description, 
                 move_2_name, move_2_cost, move_2_damage, move_2_symbol, move_2_description, 
                 retreat, artist, rarity, flavor_text):
        self.id = int(id)
        self.name = name.capitalize() if name else ''
        self.type1 = type1.strip().lower()
        self.type2 = type2.strip().lower() if type2 else None
        self.weight = weight
        self.height = height
        self.genus = genus
        self.hp = safe_int(hp, 0)
        self.level = int(level)
        self.stage = stage
        self.prev_evolution_name = prev_evolution_name
        self.next_evolution_name = next_evolution_name
        self.ability_name = ability_name
        self.ability = ability
        self.move_1_name = move_1_name
        self.move_1_cost = move_1_cost
        self.move_1_damage = safe_int(move_1_damage, 0)
        self.move_1_symbol = move_1_symbol
        self.move_1_description = move_1_description
        self.move_2_name = move_2_name
        self.move_2_cost = move_2_cost
        self.move_2_damage = safe_int(move_2_damage, 0)
        self.move_2_symbol = move_2_symbol
        self.move_2_description = move_2_description
        self.retreat = retreat
        self.artist = artist
        self.rarity = rarity
        self.flavor_text = flavor_text

        self.draw = None 
        self.new_image = None
        
        self.text_color, self.flavor_color = get_text_color(self.type1, self.type2)
        self.ability_color = get_ability_color(self.type1, self.type2)

    def create(self):
        self.create_blank()
        self.add_background()
        self.add_frame()
        self.add_art()  # Do art before the evolution box
        self.add_title()
        self.add_level()
        self.add_hp()
        self.add_evolution_box()
        self.add_put_on()

        self.add_symbol()  # Symbol goes after the evolution box so it overlaps the lines 

        self.add_species_banner()
        self.add_moves()
        self.add_weakness()
        self.add_resistance()
        self.add_retreat()
        self.add_description()
        self.add_artist()
        self.add_copyright()
        self.add_set_number()
        self.add_rarity()

    def save(self, output_name=None):
        if output_name is None:
            output_name = os.path.join(OUTPUT_DIR, str(self.id) + '_' + self.name.lower() + '.png')
        if self.new_image is None:
            raise ValueError('Card not created yet. Call create_blank() first.')
        self.new_image.save(output_name)

    def create_blank(self):
        self.new_image = Image.new('RGBA', OUTPUT_SIZE, COLOR_BLACK)
        self.draw = ImageDraw.Draw(self.new_image)

    def add_background(self):
        # This is used to add a background to the card
        open_resize_paste(self.new_image, TEXTURE[get_card_type(self.type1)])

    def add_frame(self):
        open_resize_paste(self.new_image, 'resource/base_card_parts/boarder.png')
        open_resize_paste(self.new_image, 'resource/base_card_parts/number_box.png')
        open_resize_paste(self.new_image, 'resource/base_card_parts/base_box.png')

        # CARD BOTTOM 
        self.draw.line(xy=((62, 871), (386, 871)), fill=self.text_color, width=5)
        self.draw.line(xy=((62, 918), (386, 918)), fill=self.text_color, width=2)
        self.draw.line(xy=((62, 966), (664, 966)), fill=self.text_color, width=5)

    def add_symbol(self):
        # This is used to add a symbol to the card
        paste_symbol(self.new_image, SYMBOLS[get_card_type(self.type1)], size=3, location=(614, 62))

    def add_title(self):
        if self.stage == 0:
            self.draw.text(FONT_NAME_LOCATION, self.name, self.text_color, font=FONT_NAME)
        elif self.stage == 1:
            self.draw.text(FONT_NAME_LOCATION, self.name, self.text_color, font=FONT_NAME)
        elif self.stage == 2 or self.stage == 3:
            squash_text(self.new_image, self.draw, maxwidth=381-182, xy=FONT_NAME_STAGE_LOCATION, text=self.name, fill=self.text_color, font=FONT_NAME)

    def add_put_on(self):
        if self.stage == 0:
            self.draw.text(text='Baby Pokémon count as a Basic Pokémon.', xy=FONT_PUT_ON_LOCATION, fill=self.text_color, font=FONT_PUT_ON, anchor='ra')

        elif self.stage == 1:
            self.draw.text(FONT_BASIC_LOCATION, 'BASIC', fill=COLOR_BLACK, font=FONT_BASIC)

        elif self.stage in (2, 3):
            stage_text = 'Stage 1 Pokémon' if self.stage == 3 else 'Basic Pokémon'
            put_on_text = f'Put {self.name} on the {stage_text}'

            squash_text(self.new_image, self.draw, maxwidth=381-162, xy=FONT_EVOLVES_FROM_LOCATION, text="Evolves from " + self.prev_evolution_name.capitalize(), fill=self.text_color, font=FONT_EVOLVES_FROM)
            squash_text(self.new_image, self.draw, maxwidth=265, xy=FONT_PUT_ON_LOCATION, text=put_on_text, fill=self.text_color, font=FONT_PUT_ON, anchor='ra')

    def add_level(self):
        lv_loc = FONT_LVL_LOCATION_3 if self.hp >= 100 else FONT_LVL_LOCATION_2 
        self.draw.text(lv_loc, 'LV.' + str(int(self.level or 1)), self.text_color, font=FONT_LVL)

    def add_hp(self):
        hp_loc = FONT_HP_LOCATION_3 if self.hp >= 100 else FONT_HP_LOCATION_2
        self.draw.text(hp_loc, str(self.hp), self.text_color, font=FONT_HP)
        self.draw.text(FONT_HP_LOCATION_HP, "HP", self.text_color, font=FONT_HP, align='right')

    def add_evolution_box(self):
        # CARD TOP 
        if self.stage == 0:
            open_resize_paste(self.new_image, 'resource/base_card_parts/basic.png')
            self.draw.text(FONT_BASIC_LOCATION, 'BABY', fill=COLOR_BLACK, font=FONT_BASIC)

        elif self.stage == 1:
            open_resize_paste(self.new_image, 'resource/base_card_parts/basic.png')
            self.draw.text(FONT_BASIC_LOCATION, 'BASIC', fill=COLOR_BLACK, font=FONT_BASIC)

        elif self.stage == 2:
            open_resize_paste(self.new_image, 'resource/base_card_parts/stage_line.png')
            open_resize_paste(self.new_image, 'resource/base_card_parts/stage_box.png')
            self.draw.rectangle((58, 64, 151, 141), fill=COLOR_GREY)
            self.draw.text((67, 40), 'STAGE1', COLOR_BLACK, font=FONT_BASIC)

            open_resize_paste(self.new_image, get_icon(self.prev_evolution_name), resize=(151 - 58 - 6, 141 - 64 - 6), keep_resize_ratio=True, location=(103, 103), center=True)

        elif self.stage == 2 or self.stage == 3:
            open_resize_paste(self.new_image, 'resource/base_card_parts/stage_line.png')
            open_resize_paste(self.new_image, 'resource/base_card_parts/stage_line.png', location=(0, 6))  # Draw an extra line 
                
            open_resize_paste(self.new_image, 'resource/base_card_parts/stage_box.png')
            self.draw.rectangle((58, 64, 151, 141), fill=COLOR_GREY)

            self.draw.text((64, 40), 'STAGE 2', COLOR_BLACK, font=FONT_BASIC)

            open_resize_paste(self.new_image, get_icon(self.prev_evolution_name), resize=(151 - 58 - 6, 141 - 64 - 6), keep_resize_ratio=True, location=(103, 103), center=True)

    def add_art(self):
        card_art = glob.glob(os.path.join(this_dir, 'generated_card_art', "{}_{}.png".format(self.id, self.name)))
        if card_art:
            open_resize_paste(self.new_image, card_art[0], resize=(566, 398), location=(82, 143))
        open_resize_paste(self.new_image, 'resource/base_card_parts/box_boarder.png')


    def add_species_banner(self):
        text = "NO. {:03d} {} HT: {} WT: {} lbs.".format(
            self.id, 
            str(self.genus).title(), 
            str(self.height),
            str(self.weight)
        )
        squash_text(self.new_image, self.draw, maxwidth=508, minxratio=0.9, xy=FONT_INFO_BAR_LOCATION, text=text, font=FONT_INFO_BAR, fill=COLOR_BLACK, anchor='ma')

    def add_moves(self): 
        MOVE_Y_OFFSET = 0 
        MOVE_BASE_Y_OFFSET = 620 
        MOVE_TITLE_HEIGHT = 40  # The amount of space the titles take up

        MOVE_START_GAP = (24, 12, 8)  # The gap from title to line 
        TEXT_SPACING = (12, 10, 8)  # The gap between each line in the description 
        SPLITTER_GAP = (30, 24, 10)  # The gap around the splitter 


        def get_block_sizes(text1, text2=None, is_ability=False, title2=False):
            available_height = 245 

            # Calculate the initial space 
            len_text1 = len(text1) if text1 is not None else 0
            len_text2 = len(text2) if text2 is not None else 0
            if not is_ability and (
                (len_text1 <= 70 and len_text2 == 0) or (len_text1 <= 200 and not title2) or (len_text1 == 0 and len_text2 <= 70)
            ):
                initial_gap = 44 
            else:
                initial_gap = 0

            # Start with the largest font and spacing and work down until it fits 
            for (font, font_height), text_space, splitter_gap, start_gap in itertools.product(zip(FONT_MOVE_SIZES, FONT_MOVE_REAL_HEIGHT), TEXT_SPACING, SPLITTER_GAP, MOVE_START_GAP):
                if splitter_gap == SPLITTER_GAP[-1] and text_space != TEXT_SPACING[-1]:
                    continue  # Don't use the smallest splitter gap with the largest text space
                logger.debug('font_height %s text_space %s splitter_gap %s start_gap %s ' % (font_height, text_space, splitter_gap, start_gap))
                # Calculate the amount of space the text takes up
                if text1 is not None:
                    lines1, max_char_width1 = get_lines_required(text1, font, max_width=596)
                else:
                    lines1, max_char_width1 = 0, 0
                logger.debug('lines1 %s max_char_width1 %s' % (lines1, max_char_width1))
                if text2 is not None:
                    lines2, max_char_width2 = get_lines_required(text2, font, max_width=596) 
                else:
                    lines2, max_char_width2 = 0, 0
                logger.debug('lines2 %s max_char_width2 %s' % (lines2, max_char_width2))

                text1_total = lines1 * text_space + lines1 * font_height + start_gap + MOVE_TITLE_HEIGHT 
                logger.debug('text1_total %s' % text1_total)
                if title2 or is_ability:
                    text2_total = lines2 * text_space  + lines2 * font_height + start_gap + MOVE_TITLE_HEIGHT 
                else:
                    assert lines2 == 0, lines2
                    text2_total = 0  
                logger.debug('text2_total %s' % text2_total)

                # Add the gap size to the total 
                move_total = text1_total + text2_total + initial_gap + splitter_gap * 2
                logger.debug('move_total %s' % move_total)

                if move_total <= available_height:
                    logger.debug('move_total %s <= available_height %s' % (move_total, available_height))
                    break 

            # For a move, there is the first gap and line spacing
            # Calculate the gap sizes based on the number of lines 
            block_size = (
                initial_gap,
                move_details(font, start_gap, text_space, font_height, max_char_width1), 
                splitter_gap, 
                move_details(font, start_gap, text_space, font_height, max_char_width2), 
            )

            return block_size


        # Determine which move blocks we need to draw 
        if self.ability_name != None and self.move_1_name != None:
            blocks = ('gap', 'ability', 'splitter', 'move_1')
            block_sizes = get_block_sizes(self.ability, self.move_1_description, is_ability=True)
        elif self.ability_name != None and self.move_1_name == None:
            blocks = ('gap', 'ability',)
            block_sizes = get_block_sizes(self.ability, is_ability=True)
        elif self.move_1_name != None and self.move_2_name != None:
            blocks = ('gap', 'move_1', 'splitter', 'move_2')
            block_sizes = get_block_sizes(self.move_1_description, self.move_2_description, title2=True)
        elif self.move_1_name != None:
            blocks = ('gap', 'move_1',)
            block_sizes = get_block_sizes(self.move_1_description)
        else:
            blocks = ()  # Unfinished card 
            block_sizes = ()

        def draw_move(column, current_y, move_font, start_gap, text_space, font_height, description_width):
            MOVE_Y_OFFSET = current_y

            cost = getattr(self, column + '_cost')
            name = getattr(self, column + '_name')
            damage = getattr(self, column + '_damage')
            symbol = getattr(self, column + '_symbol')
            description = getattr(self, column + '_description')

            if cost is None:
                return  # Incomplete move 
            for i, char in enumerate(cost.strip()):
                paste_symbol(self.new_image, SYMBOLS[char], size=2, location=(67 + i * 42, MOVE_BASE_Y_OFFSET + MOVE_Y_OFFSET))
            
            self.draw.text((257, MOVE_BASE_Y_OFFSET + MOVE_Y_OFFSET + 6), name.strip().title(), self.text_color, font=FONT_MOVE_TITLE)
            
            if damage:
                try:
                    self.draw.text((602, MOVE_BASE_Y_OFFSET + MOVE_Y_OFFSET + 2), "{:>3}".format(damage), self.text_color, font=FONT_MOVE_DAMAGE, align='right')
                except ValueError:
                    pass  # most likely None 

            if symbol:
                self.draw.text((668, MOVE_BASE_Y_OFFSET + MOVE_Y_OFFSET + 2), symbol, self.text_color, font=FONT_MOVE_DAMAGE)
            
            MOVE_Y_OFFSET += MOVE_TITLE_HEIGHT  # Jump below the title 

            if description and len(description):
                MOVE_Y_OFFSET += start_gap
                
                move_description = textwrap.wrap(capitalise_keywords(description), width=description_width)
                last_line = move_description.pop()
                for line in move_description:
                    justify_text(self.draw, maxwidth=596, xy=(67, MOVE_BASE_Y_OFFSET + MOVE_Y_OFFSET), text=line, fill=self.text_color, font=move_font)
                    MOVE_Y_OFFSET += text_space + font_height
                    
                self.draw.text((67, MOVE_BASE_Y_OFFSET + MOVE_Y_OFFSET), last_line, fill=self.text_color, font=move_font) 
                MOVE_Y_OFFSET += font_height

            return MOVE_Y_OFFSET


        def draw_ability(_, current_y, move_font, start_gap, text_space, font_height, description_width):
            MOVE_Y_OFFSET = current_y
            self.draw.text((67, MOVE_BASE_Y_OFFSET + MOVE_Y_OFFSET), "Ability: {}".format(self.ability_name), self.ability_color, font=FONT_MOVE_TITLE)
            
            MOVE_Y_OFFSET += MOVE_TITLE_HEIGHT  # Jump below the title 

            MOVE_Y_OFFSET += start_gap
            ability_description = textwrap.wrap(capitalise_keywords(self.ability), width=description_width)
            last_line = ability_description.pop()

            for line in ability_description:
                justify_text(self.draw, maxwidth=596, xy=(67, MOVE_BASE_Y_OFFSET + MOVE_Y_OFFSET), text=line, fill=self.text_color, font=move_font)
                MOVE_Y_OFFSET += text_space + font_height 

            self.draw.text((67, MOVE_BASE_Y_OFFSET + MOVE_Y_OFFSET), text=last_line, fill=self.text_color, font=move_font)
            MOVE_Y_OFFSET += font_height

            return MOVE_Y_OFFSET


        for block, block_size in zip(blocks, block_sizes):
            if block is None:
                break
            if block == 'gap':
                MOVE_Y_OFFSET += block_size
            elif block == 'ability':
                MOVE_Y_OFFSET = draw_ability(block, MOVE_Y_OFFSET, *block_size)
            elif block == 'splitter':
                # Draw black line
                MOVE_Y_OFFSET += int(block_size) 
                self.draw.line(xy=((69, MOVE_BASE_Y_OFFSET + MOVE_Y_OFFSET), (668, MOVE_BASE_Y_OFFSET + MOVE_Y_OFFSET)), fill=self.text_color, width=2)
                MOVE_Y_OFFSET += int(block_size) - 2 
            elif block == 'move_1' or block == 'move_2':
                MOVE_Y_OFFSET = draw_move(block, MOVE_Y_OFFSET, *block_size)


    def add_weakness(self):
        self.draw.text(FONT_WEAKNESS_LOCATION, "weakness", self.text_color, font=FONT_WEAKNESS) 
        weakness = get_weakness(self.type1, self.type2)
        if weakness:
            paste_symbol(self.new_image, SYMBOLS[get_card_type(weakness)], size=1, location=SYMBOL_WEAKNESS_LOCATION)
            self.draw.text((191, 888), text='x', fill=self.text_color, font=FONT_WEAKNESS)
            self.draw.text((202, 885), text='2', fill=self.text_color, font=FONT_WEAKNESS_NUMBER)

    def add_resistance(self):
        resistance = get_resistance(self.type1, self.type2)
        self.draw.text(FONT_RESISTANCE_LOCATION, "resistance", self.text_color, font=FONT_WEAKNESS) 
        if resistance:
            paste_symbol(self.new_image, SYMBOLS[get_card_type(resistance)], size=1, location=SYMBOL_RESISTANCE_LOCATION)
            self.draw.text((349, 883), text='-', fill=self.text_color, font=FONT_WEAKNESS_NUMBER)
            self.draw.text((361, 885), text='20', fill=self.text_color, font=FONT_WEAKNESS_NUMBER)

    def add_retreat(self):
        self.draw.text(FONT_RETREAT_LOCATION, "retreat", self.text_color, font=FONT_WEAKNESS) 
        self.draw.text((93, 941), "cost", self.text_color, font=FONT_WEAKNESS) 
        if str(self.retreat) != 'nan':
            for i in range(0, int(self.retreat)):
                paste_symbol(self.new_image, SYMBOLS['colorless'], size=1, location=(152 + 38 * i, 924))

    def add_description(self):
        """
        Add the flavor text 
        """
        # 34 = too big 
        # 32 = too small for charizard 
        self.draw.text(FONT_DESCRIPTION_LOCATION, "\n".join(textwrap.wrap(str(self.flavor_text.strip("\"")), width=32)), self.flavor_color, FONT_DESCRIPTION, 
                       spacing=7)

    def add_artist(self):
        self.draw.text(FONT_ARTIST_LOCATION, "Illus. " + str(self.artist), self.text_color, font=FONT_ARTIST)

    def add_copyright(self):
        self.draw.text(FONT_SET_NUMBER_LOCATION, str(self.id) + "/251", self.text_color, font=FONT_ARTIST, anchor='ra')

    def add_set_number(self):
        self.draw.text(FONT_COPYRIGHT_LOCATION, "©2016 Pokémon", self.text_color, font=FONT_COPYRIGHT)

    def add_rarity(self):
        if self.rarity == 1:
            # self.draw a circle
            self.draw.circle((660, 982), radius=5, fill=self.text_color)
        elif self.rarity == 2:
            # Draw a diamond
            center = (660, 982)
            self.draw.polygon([(center[0]-6, center[1]), (center[0], center[1]-6), (center[0]+6, center[1]), (center[0], center[1]+6)], fill=self.text_color)
        elif self.rarity == 3:
            other_image = Image.open(os.path.join(this_dir, 'resource/base_card_parts/star.png'), mode='r').convert('RGBA')
            self.new_image.paste(other_image, (654, 977), other_image)



def main():
    df = pandas.read_csv(os.path.join(this_dir, 'cards.csv'))
    df = df.where(pandas.notnull(df), None)

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    for row_dict in df.to_dict(orient="records"):
        # if row_dict['id'] != 142:
        #     continue
        try:
            card = Card(**row_dict)
            card.create()
            card.save()
            logger.info('Created card %s (%s)', card.id, card.name)
        except KeyboardInterrupt:
            logger.info('Stopping early...')
            break
        except BaseException as e:
            raise


if __name__ == '__main__':
    main()
