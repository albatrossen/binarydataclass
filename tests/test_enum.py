from binarydataclass import from_bytes, Uint8
from dataclasses import dataclass
from enum import Enum, auto


class Cheese(Uint8, Enum):
    RED_LEICESTER = auto()
    TILSIT = auto()
    CAERPHILLY = auto()
    BEL_PAESE = auto()
    RED_WINDSOR = auto()
    STILTON = auto()
    EMMENTAL = auto()
    NORWEGIAN_JARLSBERGER = auto()
    LIPTAUER = auto()
    LANCASHIRE = auto()
    WHITE_STILTON = auto()
    DANISH_BLUE = auto()
    DOUBLE_GLOUCESTER = auto()
    CHESHIRE = auto()
    DORSET_BLUE_VINNEY = auto()
    BRIE = auto()
    ROQUEFORT = auto()
    PONT_L_EVEQUE = auto()
    PORT_SALUT = auto()
    SAVOYARD = auto()
    SAINT_PAULIN = auto()
    CARRE_DE_L_EST = auto()
    BOURSIN = auto()
    BRESSE_BLEU = auto()
    PERLE_DE_CHAMPAGNE = auto()
    CAMEMBERT = auto()
    GOUDA = auto()
    EDAM = auto()
    CAITHNESS = auto()
    SMOKED_AUSTRIAN = auto()
    JAPANESE_SAGE_DARBY = auto()
    WENSLEYDALE = auto()
    GREEK_FETA = auto()
    GORGONZOLA = auto()
    PARMESAN = auto()
    MOZZARELLA = auto()
    PIPPO_CREME = auto()
    DANISH_FIMBOE = auto()
    CZECH_SHEEP_S_MILK = auto()
    VENEZUELAN_BEAVER_CHEESE = auto()
    CHEDDAR = auto()
    ILLCHESTER = auto()
    LIMBURGER = auto()


@dataclass
class Cheeseshop:
    last_requested_out_of_stock_item: Cheese


def test_enum():
    obj = from_bytes(Cheeseshop, b"\x22")
    assert (
        type(obj.last_requested_out_of_stock_item) == Cheese
        and obj.last_requested_out_of_stock_item == Cheese.GORGONZOLA
    )
