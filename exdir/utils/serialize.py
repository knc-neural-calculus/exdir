"""attempting to allow serialization as json as well as yaml, for better portability

"""
import json
from typing import *

from ..core import constants

# HACK: this global variable can be changed when calling the serializer. Messy, but works
MODE : Literal['yaml', 'json'] = 'yaml'

AVAILIBLE_MODES : Dict[Literal['yaml', 'json'], Optional[bool]] = {
    'json': True, # json is in the standard library
    'yaml': None, 
}

# import packages
try:
    import ruamel_yaml as yaml
    AVAILIBLE_MODES['yaml'] = True
except (ImportError,ModuleNotFoundError) as e:
    try:
        import ruamel.yaml as yaml
        AVAILIBLE_MODES['yaml'] = True
    except (ImportError,ModuleNotFoundError) as e:
        AVAILIBLE_MODES['yaml'] = False


# provide functions
load : Optional[Callable] = None
dump : Optional[Callable] = None
DoubleQuotedScalarString : Optional[Callable] = None


# refresh things according to `MODE`
def refresh():
    # modify filename constants
    constants.META_FILENAME = f"exdir.{MODE}"
    constants.ATTRIBUTES_FILENAME = f"attributes.{MODE}"

    # global functions
    global load
    global dump
    global DoubleQuotedScalarString

    if MODE == 'yaml':
        load = yaml.safe_load

        dump = lambda data, file : yaml.dump(
            data, file,
            default_flow_style=False,
            allow_unicode=True,
            Dumper=yaml.RoundTripDumper,
        )

        DoubleQuotedScalarString = yaml.scalarstring.DoubleQuotedScalarString

    elif MODE == 'json':
        load = json.load

        dump = json.dump

        # CRIT: I have no idea what this function is supposed to do,
        #      but it seems that this wouldn't be relevant for json files 
        #      where we have everything in quotes anyway
        DoubleQuotedScalarString = lambda x : str(x)
    else:
        raise ValueError(f"unsupported mode: {MODE}")


refresh()