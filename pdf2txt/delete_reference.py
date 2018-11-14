import re

# Reference 제거
def del_ref(text):
    ref_start = max(text.rfind('Reference'),
                    text.rfind('REFERENCE'),
                    text.rfind('Bibliograph'),
                    text.rfind('BIBLIOGRAPH'))
    text = text[:ref_start]

    return text
