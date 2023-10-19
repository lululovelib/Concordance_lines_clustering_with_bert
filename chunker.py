import re


def return_np_patterns(text):
    """
    text: a string with TreeTagger POS
    return a list of all the noun phrases in that text
    """
    a_number = "(\w+|\w+[\,\.\-]\w+)_CD"

    # all forms of numbers
    number = f"([\w\-]+_RB\s)?($_$)?({a_number}\s)+to_\w+\s({a_number}\s)+|({a_number}\s)+of_\w+\s|{a_number}\s"
    # basic NPs
    np_1 = f"(\w+_PDT\s)?({number})?(\w+_DT\s)?({number})?([\w\-]+_RB\w*\s)*({number})?([\w\-]+_JJ\w*\s)*([\w\-]+_(NN\w*|PRP)\s)+"
    # possessive NPs
    np_2 = f"({np_1}(\'|\'s)_POS|[\w\-]+_PRP\$)\s({number})?([\w\-]+_JJ\w*\s)*([\w\-]+_NN\w*\s)+"
    # NP of NP
    np_3 = f"({np_1}|{np_2})of_\w+\s({np_1}|{np_2})"
    # all above combined
    np_patterns = f"{np_3}|{np_2}|{np_1}"

    pattern_list = []
    search_items = re.finditer(np_patterns, text.replace("''_'' ", "").replace("'_'' ", "").replace("``_`` ", ""))
    for search_item in search_items:
        pattern = re.sub("_\S+", "", search_item.group())
        pattern_list.append(pattern)
        return pattern_list


