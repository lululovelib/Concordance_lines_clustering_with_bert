import os
import re
from random import choice as choice

sentence_boundary_signs = "(\.|\!|\?)(|[\"\'“”‘’])\s+"


def find_left_boundary(boundary_sign, string):
    """
    used in left context of the node word.
    return (the last index number + 1) of the last matched item.
    """
    iterator = re.finditer(boundary_sign, string)
    index_list = []
    for i in iterator:
        index_list.append((i.end()))
    return max(index_list)


def find_right_boundary(boundary_sign, string):
    """
    used in right context of the node word.
    return (the first index number + 1) of the first matched item.
    """
    iterator = re.finditer(boundary_sign, string)
    index_list = []
    for ii in iterator:
        index_list.append(ii.start() + 1)
    return min(index_list)


def count_and_sort_list(input_list, reverse=True):
    """
    Enter a list and the function will return a list of tuple[(freq1, item1), (freq2, item2), ...]
    By default the tuples are ranked by a higher-to-lower frequency order
    """
    freq_list, freq_rank_dict = [], {}
    for i in input_list:
        freq_rank_dict[i] = freq_rank_dict.get(i, 0) + 1
    for k, v in freq_rank_dict.items():
        freq_list.append((v, k))
    freq_list.sort(reverse=reverse)
    return freq_list


def sample_with_fixed_intervals(list_object, sample_number):
    sampled_list_object = []
    if len(list_object) <= sample_number:
        sampled_list_object = list_object
    else:
        if len(list_object) % sample_number == 0:
            interval = len(list_object) / sample_number
            first_item_index = choice(range(int(interval)))
            sampled_list_object.append(list_object[first_item_index])
            for i in range(1, sample_number):
                sampled_list_object.append(list_object[first_item_index + i * int(interval)])
        else:
            interval = len(list_object) // (sample_number - 1)
            first_item_index = choice(range(int(interval)))
            sampled_list_object.append(list_object[first_item_index])
            for i in range(1, sample_number - 1):
                sampled_list_object.append(list_object[first_item_index + i * int(interval)])
            sampled_list_object.append(choice(list_object[len(list_object) - len(list_object) % (sample_number - 1):]))
    return sampled_list_object


def concord_one_pattern(
        pattern_str, corpus_path, encoding="utf8", ignore_case=True, delete_pattern_str=None,
        left_context_size=50, right_context_size=50, remove_blank_lines=False, remove_pos=True,
        select_pattern_str=None, sample_num=None, stop_at_boundary=True
):
    pattern_str_temp = " " + pattern_str + " "
    if remove_pos:
        left_context_size = int(left_context_size * 1.5)
        right_context_size = int(right_context_size * 1.5)
    text = ''

    if os.path.isfile(corpus_path):
        with open(corpus_path, 'r', encoding=encoding) as fi:
            text = fi.read()
        if remove_blank_lines:
            text = re.sub('\n', ' ', text)

    else:
        for root, dirs, files in os.walk(corpus_path):
            for f in files:
                text_file = os.path.join(root, f)
                with open(text_file, 'r', encoding=encoding) as fi:
                    text += fi.read()
        if remove_blank_lines:
            text = re.sub('\n', ' ', text)

    if ignore_case:
        search_items = re.finditer(pattern_str_temp, text, re.IGNORECASE)
    else:
        search_items = re.finditer(pattern_str_temp, text)

    item_start_index_list, item_end_index_list = [], []
    for search_item in search_items:
        item_start_index_list.append(search_item.start())
        item_end_index_list.append(search_item.end())

    concord_start_index_list, concord_end_index_list = [], []
    for item_start_index in item_start_index_list:
        if item_start_index < left_context_size:
            temp_left_context = text[:item_start_index + 1]
            if re.findall(sentence_boundary_signs, temp_left_context) and stop_at_boundary:
                concord_start_index = find_left_boundary(sentence_boundary_signs, temp_left_context)
            else:
                concord_start_index = 0
        else:
            temp_left_context = text[item_start_index - left_context_size:item_start_index + 1]
            if re.findall(sentence_boundary_signs, temp_left_context) and stop_at_boundary:
                concord_start_index = item_start_index - left_context_size + find_left_boundary(sentence_boundary_signs,
                                                                                                temp_left_context)
            else:
                concord_start_index = item_start_index - left_context_size
        concord_start_index_list.append(concord_start_index)

    for item_end_index in item_end_index_list:
        if item_end_index + right_context_size > len(text):
            temp_right_context = text[item_end_index:]
            if re.findall(sentence_boundary_signs, temp_right_context) and stop_at_boundary:
                concord_end_index = item_end_index + find_right_boundary(sentence_boundary_signs, temp_right_context)
            else:
                concord_end_index = len(text)
        else:
            temp_right_context = text[item_end_index:item_end_index + right_context_size]
            if re.findall(sentence_boundary_signs, temp_right_context) and stop_at_boundary:
                concord_end_index = item_end_index + find_right_boundary(sentence_boundary_signs, temp_right_context)
            else:
                concord_end_index = item_end_index + right_context_size
        concord_end_index_list.append(concord_end_index)

    l1_word_list, r1_word_list, node_word_list, show_concordance_list, save_concordance_list, left_context_list, \
        right_context_list = [], [], [], [], [], [], []

    # Condition 1
    if delete_pattern_str and not select_pattern_str:
        for i in range(len(item_start_index_list)):
            delete_pattern_str_temp = " " + delete_pattern_str + " "
            node_word = text[item_start_index_list[i]:item_end_index_list[i]]
            left_context = text[concord_start_index_list[i]:item_start_index_list[i]]
            left_context = left_context if re.findall("\S+\s", left_context) == [] or left_context[0] == " " or \
                                           len(left_context) < left_context_size \
                else left_context.removeprefix(re.findall("\S+\s", left_context)[0])

            right_context = text[item_end_index_list[i]:concord_end_index_list[i] + 1]
            right_context = right_context if re.findall("\s\S+", right_context) == [] or right_context[-1] == " " or \
                                             len(right_context) < right_context_size + 1 \
                else right_context.removesuffix(re.findall("\s\S+", right_context)[-1])
            concord_instance_raw = left_context + node_word + right_context
            if not re.findall(delete_pattern_str_temp, concord_instance_raw, re.IGNORECASE):
                if remove_pos:
                    node_word_list.append(re.sub("_\S+", "", node_word.strip().lower()))
                    l1_word_list.append(re.sub("_\S+", "", left_context.split()[-1].lower())) if len(left_context) > 0 \
                        else l1_word_list.append("")
                    r1_word_list.append(re.sub("_\S+", "", right_context.split()[0].lower()))
                    left_context = re.sub("_\S+", "", left_context)
                    right_context = re.sub("_\S+", "", right_context)
                    node_word = re.sub("_\S+", "", node_word)
                    concordance_line_spaced = left_context.rjust(left_context_size) + '  ' + node_word + '  ' + \
                                              right_context.ljust(right_context_size)
                    concordance_line_raw = left_context + node_word + right_context
                    show_concordance_list.append(concordance_line_spaced)
                    save_concordance_list.append(concordance_line_raw)
                    left_context_list.append(left_context)
                    right_context_list.append(right_context)

                else:
                    node_word_list.append(node_word.strip().lower())
                    l1_word_list.append(left_context.split()[-1].lower()) if len(
                        left_context) > 0 else l1_word_list.append("")
                    r1_word_list.append(right_context.split()[0].lower())
                    concordance_line_spaced = left_context.rjust(left_context_size) + '  ' + node_word + '  ' + \
                                              right_context.ljust(right_context_size)
                    concordance_line_raw = left_context + node_word + right_context
                    show_concordance_list.append(concordance_line_spaced)
                    save_concordance_list.append(concordance_line_raw)
                    left_context_list.append(left_context)
                    right_context_list.append(right_context)
    # Condition 2
    elif select_pattern_str and not delete_pattern_str:
        for i in range(len(item_start_index_list)):
            select_pattern_str_temp = " " + select_pattern_str + " "
            node_word = text[item_start_index_list[i]:item_end_index_list[i]]
            left_context = text[concord_start_index_list[i]:item_start_index_list[i]]
            left_context = left_context if re.findall("\S+\s", left_context) == [] or left_context[0] == " " or \
                                           len(left_context) < left_context_size \
                else left_context.removeprefix(re.findall("\S+\s", left_context)[0])
            right_context = text[item_end_index_list[i]:concord_end_index_list[i] + 1]
            right_context = right_context if re.findall("\s\S+", right_context) == [] or right_context[-1] == " " or \
                                             len(right_context) < right_context_size + 1 \
                else right_context.removesuffix(re.findall("\s\S+", right_context)[-1])
            concord_instance_raw = left_context + node_word + right_context
            if re.findall(select_pattern_str_temp, concord_instance_raw, re.IGNORECASE):
                if remove_pos:
                    node_word_list.append(re.sub("_\S+", "", node_word.strip().lower()))
                    l1_word_list.append(re.sub("_\S+", "", left_context.split()[-1].lower())) if len(left_context) > 0 \
                        else l1_word_list.append("")
                    r1_word_list.append(re.sub("_\S+", "", right_context.split()[0].lower()))
                    left_context = re.sub("_\S+", "", left_context)
                    right_context = re.sub("_\S+", "", right_context)
                    node_word = re.sub("_\S+", "", node_word)
                    concordance_line_spaced = left_context.rjust(left_context_size) + '  ' + node_word + '  ' + \
                                              right_context.ljust(right_context_size)
                    concordance_line_raw = left_context + node_word + right_context
                    show_concordance_list.append(concordance_line_spaced)
                    save_concordance_list.append(concordance_line_raw)
                    left_context_list.append(left_context)
                    right_context_list.append(right_context)
                else:
                    node_word_list.append(node_word.strip().lower())
                    l1_word_list.append(left_context.split()[-1].lower()) if len(
                        left_context) > 0 else l1_word_list.append("")
                    r1_word_list.append(right_context.split()[0].lower())
                    concordance_line_spaced = left_context.rjust(left_context_size) + '  ' + node_word + '  ' + \
                                              right_context.ljust(right_context_size)
                    concordance_line_raw = left_context + node_word + right_context
                    show_concordance_list.append(concordance_line_spaced)
                    save_concordance_list.append(concordance_line_raw)
                    left_context_list.append(left_context)
                    right_context_list.append(right_context)
    # Condition 3
    elif delete_pattern_str and select_pattern_str:
        for i in range(len(item_start_index_list)):
            delete_pattern_str_temp = " " + delete_pattern_str + " "
            select_pattern_str_temp = " " + select_pattern_str + " "
            node_word = text[item_start_index_list[i]:item_end_index_list[i]]
            left_context = text[concord_start_index_list[i]:item_start_index_list[i]]
            left_context = left_context if re.findall("\S+\s", left_context) == [] or left_context[0] == " " or \
                                           len(left_context) < left_context_size \
                else left_context.removeprefix(re.findall("\S+\s", left_context)[0])
            right_context = text[item_end_index_list[i]:concord_end_index_list[i] + 1]
            right_context = right_context if re.findall("\s\S+", right_context) == [] or right_context[-1] == " " or \
                                             len(right_context) < right_context_size + 1 \
                else right_context.removesuffix(re.findall("\s\S+", right_context)[-1])
            concord_instance_raw = left_context + node_word + right_context
            if not re.findall(delete_pattern_str_temp, concord_instance_raw, re.IGNORECASE):
                if re.findall(select_pattern_str_temp, concord_instance_raw, re.IGNORECASE):
                    if remove_pos:
                        node_word_list.append(re.sub("_\S+", "", node_word.strip().lower()))
                        l1_word_list.append(re.sub("_\S+", "", left_context.split()[-1].lower())) if len(
                            left_context) > 0 \
                            else l1_word_list.append("")
                        r1_word_list.append(re.sub("_\S+", "", right_context.split()[0].lower()))
                        left_context = re.sub("_\S+", "", left_context)
                        right_context = re.sub("_\S+", "", right_context)
                        node_word = re.sub("_\S+", "", node_word)
                        concordance_line_spaced = left_context.rjust(left_context_size) + '  ' + node_word + '  ' + \
                                                  right_context.ljust(right_context_size)
                        concordance_line_raw = left_context + node_word + right_context
                        show_concordance_list.append(concordance_line_spaced)
                        save_concordance_list.append(concordance_line_raw)
                        left_context_list.append(left_context)
                        right_context_list.append(right_context)

                    else:
                        node_word_list.append(node_word.strip().lower())
                        l1_word_list.append(left_context.split()[-1].lower()) if len(
                            left_context) > 0 else l1_word_list.append("")
                        r1_word_list.append(right_context.split()[0].lower())
                        concordance_line_spaced = left_context.rjust(left_context_size) + '  ' + node_word + '  ' + \
                                                  right_context.ljust(right_context_size)
                        concordance_line_raw = left_context + node_word + right_context
                        show_concordance_list.append(concordance_line_spaced)
                        save_concordance_list.append(concordance_line_raw)
                        left_context_list.append(left_context)
                        right_context_list.append(right_context)
    # Condition 4
    elif not delete_pattern_str and not select_pattern_str:
        for i in range(len(item_start_index_list)):
            node_word = text[item_start_index_list[i]:item_end_index_list[i]]
            left_context = text[concord_start_index_list[i]:item_start_index_list[i]]
            left_context = left_context if re.findall("\S+\s", left_context) == [] or left_context[0] == " " or \
                                           len(left_context) < left_context_size \
                else left_context.removeprefix(re.findall("\S+\s", left_context)[0])
            right_context = text[item_end_index_list[i]:concord_end_index_list[i] + 1]
            right_context = right_context if re.findall("\s\S+", right_context) == [] or right_context[-1] == " " or \
                                             len(right_context) < right_context_size + 1 \
                else right_context.removesuffix(re.findall("\s\S+", right_context)[-1])
            if remove_pos:
                node_word_list.append(re.sub("_\S+", "", node_word.strip().lower()))
                l1_word_list.append(re.sub("_\S+", "", left_context.split()[-1].lower())) if len(left_context) > 0 \
                    else l1_word_list.append("")
                r1_word_list.append(re.sub("_\S+", "", right_context.split()[0].lower()))
                left_context = re.sub("_\S+", "", left_context)
                right_context = re.sub("_\S+", "", right_context)
                node_word = re.sub("_\S+", "", node_word)
                concordance_line_spaced = left_context.rjust(left_context_size) + '  ' + node_word + '  ' + \
                                          right_context.ljust(right_context_size)
                concordance_line_raw = left_context + node_word + right_context
                show_concordance_list.append(concordance_line_spaced)
                save_concordance_list.append(concordance_line_raw)
                left_context_list.append(left_context)
                right_context_list.append(right_context)
            else:
                node_word_list.append(node_word.strip().lower())
                l1_word_list.append(left_context.split()[-1].lower()) if len(left_context) > 0 else l1_word_list.append(
                    "")
                r1_word_list.append(right_context.split()[0].lower())
                concordance_line_spaced = left_context.rjust(left_context_size) + '  ' + node_word + '  ' + \
                                          right_context.ljust(right_context_size)
                concordance_line_raw = left_context + node_word + right_context
                show_concordance_list.append(concordance_line_spaced)
                save_concordance_list.append(concordance_line_raw)
                left_context_list.append(left_context)
                right_context_list.append(right_context)

    r1_tuple_list = list(zip(r1_word_list, show_concordance_list, save_concordance_list,
                             left_context_list, right_context_list, node_word_list))
    l1_tuple_list = list(zip(l1_word_list, show_concordance_list, save_concordance_list,
                             left_context_list, right_context_list, node_word_list))
    r1_tuple_list.sort()
    l1_tuple_list.sort()

    r1_remove_duplicate_tuple_list, l1_remove_duplicate_tuple_list = [], []

    if sample_num:
        r1_tuple_list = sample_with_fixed_intervals(r1_tuple_list, sample_num)
        l1_tuple_list = sample_with_fixed_intervals(l1_tuple_list, sample_num)

    concord_number = len(r1_tuple_list)
    if concord_number == 1:
        r1_remove_duplicate_tuple_list = r1_tuple_list
        l1_remove_duplicate_tuple_list = l1_tuple_list
    else:
        for i in range(concord_number):
            if r1_tuple_list[i][2] != r1_tuple_list[i - 1][2]:
                r1_remove_duplicate_tuple_list.append(r1_tuple_list[i])
            if l1_tuple_list[i][2] != l1_tuple_list[i - 1][2]:
                l1_remove_duplicate_tuple_list.append(l1_tuple_list[i])

    # Note:
    # r1_remove_duplicate_tuple_list: [(r1_word, concordance_line_spaced, concordance_line_raw, left_context,
    # right_context, node_word), (), ..., ()]
    # l1_remove_duplicate_tuple_list: [(l1_word, concordance_line_spaced, concordance_line_raw, left_context,
    # right_context, node_word), (), ..., ()]

    l1_freq_list = count_and_sort_list([t[0] for t in l1_remove_duplicate_tuple_list])
    r1_freq_list = count_and_sort_list([t[0] for t in r1_remove_duplicate_tuple_list])
    node_word_freq_list = count_and_sort_list([t[-1] for t in r1_remove_duplicate_tuple_list])

    return pattern_str, l1_freq_list, r1_freq_list, node_word_freq_list, \
           r1_remove_duplicate_tuple_list, l1_remove_duplicate_tuple_list


def save_or_show_concord(
        search_pattern_str_list, corpus_path, delete_pattern_str=None, select_pattern_str=None,
        encoding="utf8", save_concord=False, sample_num=None, stop_at_boundary=True,
        ignore_case=True, r1_alphabetical=False, left_context_size=50, right_context_size=50,
        remove_blank_lines=False, remove_pos=True, show_l1_r1_list=False, show_node_word_list=False
):
    pattern_str_list, l1_freq_list_list, r1_freq_list_list, node_word_freq_list_list, \
        r1_remove_duplicate_tuple_list_list, l1_remove_duplicate_tuple_list_list = [], [], [], [], [], []

    for pattern in search_pattern_str_list:
        one_pattern_result = concord_one_pattern(
            pattern, corpus_path=corpus_path, encoding=encoding, ignore_case=ignore_case,
            left_context_size=left_context_size, stop_at_boundary=stop_at_boundary,
            delete_pattern_str=delete_pattern_str,
            right_context_size=right_context_size, remove_blank_lines=remove_blank_lines,
            remove_pos=remove_pos, sample_num=sample_num, select_pattern_str=select_pattern_str
        )
        pattern_str_list.append(one_pattern_result[0])
        l1_freq_list_list.append(one_pattern_result[1])
        r1_freq_list_list.append(one_pattern_result[2])
        node_word_freq_list_list.append(one_pattern_result[3])

        r1_remove_duplicate_tuple_list_list.append(one_pattern_result[4])
        l1_remove_duplicate_tuple_list_list.append(one_pattern_result[5])

    concord_list = list(zip(
        pattern_str_list, r1_remove_duplicate_tuple_list_list, l1_remove_duplicate_tuple_list_list))
    concord_num_list = []
    for pattern_str, r1_remove_duplicate_tuple_list, l1_remove_duplicate_tuple_list in concord_list:
        if save_concord:
            concord_file_name = f"{pattern_str}_concord.txt"
            with open(concord_file_name, 'w', encoding=encoding) as f_clean:
                f_clean.write('')
            with open(concord_file_name, 'a', encoding=encoding) as f:
                if r1_alphabetical:
                    for i in range(len(r1_remove_duplicate_tuple_list)):
                        f.write(r1_remove_duplicate_tuple_list[i][2]+"\n")
                else:
                    for i in range(len(l1_remove_duplicate_tuple_list)):
                        f.write(l1_remove_duplicate_tuple_list[i][2]+"\n")
            print(f"The results of \"{pattern_str}\" have been saved in file!")

        else:
            print("\n" + "*" * left_context_size + " " + pattern_str + " " + "*" * right_context_size)
            n = 1
            most_digits = len(str(len(r1_remove_duplicate_tuple_list) + 1))
            if r1_alphabetical:
                for i in range(len(r1_remove_duplicate_tuple_list)):
                    print(str(n) + ' ' * (most_digits - len(str(n)) + 1) + r1_remove_duplicate_tuple_list[i][1])
                    n += 1
                concord_num_list.append(len(r1_remove_duplicate_tuple_list))
            else:
                for i in range(len(l1_remove_duplicate_tuple_list)):
                    print(str(n) + ' ' * (most_digits - len(str(n)) + 1) + l1_remove_duplicate_tuple_list[i][1])
                    n += 1
                concord_num_list.append(len(l1_remove_duplicate_tuple_list))

    info_list = list(zip(
        concord_num_list, pattern_str_list, l1_freq_list_list, r1_freq_list_list, node_word_freq_list_list))
    for concord_number, pattern_str, l1_list, r1_list, node_word_freq_list_list in info_list:
        print('-' * (left_context_size + right_context_size))
        print(f"You got ({concord_number}) instances with \"{pattern_str}\" from \"{corpus_path}\".")
        if show_l1_r1_list:
            print(f"L1 words: {l1_list[:50]}")
            print(f"R1 words: {r1_list[:50]}")
        if show_node_word_list:
            print(f"Node words: {node_word_freq_list_list}")