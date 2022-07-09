import re
from typing import List, Tuple, Optional
import inflect


def get_keys(value: str, key_pattern:str=r'\$\{([^{}]+)\}') -> List[Tuple[str, str, Optional[str]]]:
    # find all keys enclosed in ${}
    items = re.findall(key_pattern, value)
    items = list(set(items))
    # filter out var keys ${*:var}
    keys = [item for item in items if not item.endswith(':var')]
    # split indexed keys as in ${*.1} and ${*.2}...
    results = [(item, item.split('.')[0], str(item.split('.')[1]) if len(item.split('.')) > 1 else None) for item in keys]
    return results


def get_code(d: dict) -> str:
    code = d['code'] if 'code' in d else d['text']
    # should_format = d['format'] if 'format' in d else True
    # if should_format and isinstance(code, str) and not code.startswith('"') and not re.search(r'\$\{.*\}|\=|\n', code):  # type: ignore
        # code = re.sub(r'"', '', code)
        # code = f'"{code}"'
    # elif should_format and code.startswith('"') and code.endswith('"'):
    #     new_code = re.sub(r"\"", "", code[1:-1])
    #     code = new_code #f'"{new_code}"'
    
    code = str(code).strip()
    return code


def get_var(d: dict, context: List[str]) -> Optional[str]:
    if 'var' in d and d['var'] is not None:
        var = d['var']
    # elif 'code' in d and d['code'].startswith('"'):
    #     var = re.sub(r'"|^and$|^or$|^the$', '', d['code']).strip()
    #     var = re.sub(r'\s+', '_', var)
    #     var = '_'.join([(x if re.match(r"[-+]?\d+$", x) is None else inflect.engine().number_to_words(x)) for x in var.split('_')])
    #     var = re.sub(r'-', '_', var)
    #     var = re.sub(r'\:', '', var)
    #     var = var.lower()
    else:
        var = None
        
    return var