import re
from typing import Any


def get_src(data: str) -> tuple[Any, Any, bool]:
    match_src = re.search(r'src="([^"]*)"', data)
    match_answer = re.search(r'value="true".*?>([^<]+)', data)
    if match_src:
        return match_answer.group(1) or None, match_src.group(1), True
    else:
        return data, None, False



