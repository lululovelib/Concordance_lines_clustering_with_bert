import os
import re
import time
from random import choice as choice

sentence_boundary_signs = "\.(|[\"\'“”‘’])\s+|\!(|[\"\'“”‘’])\s+|\?(|[\"\'“”‘’])\s+"


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


def concord_one_pattern(pattern_str, corpus_path, encoding, ignore_case, r1_alphabetical, delete_pattern_str,
                        save_concord, show_concord,
                        left_context_size, right_context_size, remove_blank_lines, remove_pos, select_pattern_str,
                        sample_num, stop_at_boundary
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

    l1_word_list, r1_word_list, node_word_list, concordance_list, left_context_list, right_context_list = \
        [], [], [], [], [], []

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
                    concord_instance_spaced = left_context.rjust(left_context_size) + '  ' + node_word + '  ' + \
                                              right_context.ljust(right_context_size)

                    concordance_list.append(concord_instance_spaced)
                    left_context_list.append(left_context)
                    right_context_list.append(right_context)

                else:
                    node_word_list.append(node_word.strip().lower())
                    l1_word_list.append(left_context.split()[-1].lower()) if len(
                        left_context) > 0 else l1_word_list.append("")
                    r1_word_list.append(right_context.split()[0].lower())
                    concord_instance_spaced = left_context.rjust(left_context_size) + '  ' + node_word + '  ' + \
                                              right_context.ljust(right_context_size)
                    concordance_list.append(concord_instance_spaced)
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
                    concord_instance_spaced = left_context.rjust(left_context_size) + '  ' + node_word + '  ' + \
                                              right_context.ljust(right_context_size)
                    concordance_list.append(concord_instance_spaced)
                    left_context_list.append(left_context)
                    right_context_list.append(right_context)
                else:
                    node_word_list.append(node_word.strip().lower())
                    l1_word_list.append(left_context.split()[-1].lower()) if len(
                        left_context) > 0 else l1_word_list.append("")
                    r1_word_list.append(right_context.split()[0].lower())
                    concord_instance_spaced = left_context.rjust(left_context_size) + '  ' + node_word + '  ' + \
                                              right_context.ljust(right_context_size)
                    concordance_list.append(concord_instance_spaced)
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
                        concord_instance_spaced = left_context.rjust(left_context_size) + '  ' + node_word + '  ' + \
                                                  right_context.ljust(right_context_size)
                        concordance_list.append(concord_instance_spaced)
                        left_context_list.append(left_context)
                        right_context_list.append(right_context)

                    else:
                        node_word_list.append(node_word.strip().lower())
                        l1_word_list.append(left_context.split()[-1].lower()) if len(
                            left_context) > 0 else l1_word_list.append("")
                        r1_word_list.append(right_context.split()[0].lower())
                        concord_instance_spaced = left_context.rjust(left_context_size) + '  ' + node_word + '  ' + \
                                                  right_context.ljust(right_context_size)
                        concordance_list.append(concord_instance_spaced)
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
                concord_instance_spaced = left_context.rjust(left_context_size) + '  ' + node_word + '  ' + \
                                          right_context.ljust(right_context_size)
                concordance_list.append(concord_instance_spaced)
                left_context_list.append(left_context)
                right_context_list.append(right_context)
            else:
                node_word_list.append(node_word.strip().lower())
                l1_word_list.append(left_context.split()[-1].lower()) if len(left_context) > 0 else l1_word_list.append(
                    "")
                r1_word_list.append(right_context.split()[0].lower())
                concord_instance_spaced = left_context.rjust(left_context_size) + '  ' + node_word + '  ' + \
                                          right_context.ljust(right_context_size)
                concordance_list.append(concord_instance_spaced)
                left_context_list.append(left_context)
                right_context_list.append(right_context)

    l1_freq_list = count_and_sort_list(l1_word_list)
    r1_freq_list = count_and_sort_list(r1_word_list)
    node_word_freq_list = count_and_sort_list(node_word_list)

    r1_word_concord_left_right_context_tuple_list = \
        list(zip(r1_word_list, concordance_list, left_context_list, right_context_list))
    l1_word_concord_left_right_context_tuple_list = \
        list(zip(l1_word_list, concordance_list, left_context_list, right_context_list))

    r1_word_concord_left_right_context_tuple_list.sort()
    l1_word_concord_left_right_context_tuple_list.sort()

    left_context_list_in_order, right_context_list_in_order = [], []
    n = 1

    # Condition 1
    if save_concord:
        concord_file_name = "concord.txt"
        with open(concord_file_name, 'w', encoding=encoding) as f_clean:
            f_clean.write('')
        with open(concord_file_name, 'a', encoding=encoding) as f:
            if r1_alphabetical:
                if sample_num:
                    r1_word_concord_left_right_context_tuple_list = sample_with_fixed_intervals(
                        r1_word_concord_left_right_context_tuple_list, sample_num)
                    for i in range(len(r1_word_concord_left_right_context_tuple_list)):
                        concord_i = r1_word_concord_left_right_context_tuple_list[i][1]
                        l_context = r1_word_concord_left_right_context_tuple_list[i][2]
                        r_context = r1_word_concord_left_right_context_tuple_list[i][3]
                        if concord_i != r1_word_concord_left_right_context_tuple_list[i - 1][1]:
                            f.write(concord_i + '\n')
                            left_context_list_in_order.append(l_context)
                            right_context_list_in_order.append(r_context)
                            n += 1
                else:
                    for i in range(len(r1_word_concord_left_right_context_tuple_list)):
                        concord_i = r1_word_concord_left_right_context_tuple_list[i][1]
                        l_context = r1_word_concord_left_right_context_tuple_list[i][2]
                        r_context = r1_word_concord_left_right_context_tuple_list[i][3]
                        if concord_i != r1_word_concord_left_right_context_tuple_list[i - 1][1]:
                            f.write(concord_i + '\n')
                            left_context_list_in_order.append(l_context)
                            right_context_list_in_order.append(r_context)
                            n += 1
            else:
                if sample_num:
                    r1_word_concord_left_right_context_tuple_list = sample_with_fixed_intervals(
                        r1_word_concord_left_right_context_tuple_list, sample_num)
                    for i in range(len(r1_word_concord_left_right_context_tuple_list)):
                        concord_i = l1_word_concord_left_right_context_tuple_list[i][1]
                        l_context = l1_word_concord_left_right_context_tuple_list[i][2]
                        r_context = l1_word_concord_left_right_context_tuple_list[i][3]
                        if concord_i != r1_word_concord_left_right_context_tuple_list[i - 1][1]:
                            f.write(concord_i + '\n')
                            left_context_list_in_order.append(l_context)
                            right_context_list_in_order.append(r_context)
                            n += 1
                else:
                    for i in range(len(r1_word_concord_left_right_context_tuple_list)):
                        concord_i = l1_word_concord_left_right_context_tuple_list[i][1]
                        l_context = l1_word_concord_left_right_context_tuple_list[i][2]
                        r_context = l1_word_concord_left_right_context_tuple_list[i][3]
                        if concord_i != r1_word_concord_left_right_context_tuple_list[i - 1][1]:
                            f.write(concord_i + '\n')
                            left_context_list_in_order.append(l_context)
                            right_context_list_in_order.append(r_context)
                            n += 1
            f.close()
        print(f"\nThe results of \"{pattern_str_temp.strip()}\" have been saved in file!")

    # Condition 2
    elif show_concord:
        if r1_alphabetical:
            if sample_num:
                r1_word_concord_left_right_context_tuple_list = sample_with_fixed_intervals(
                    r1_word_concord_left_right_context_tuple_list, sample_num)
                for i in range(len(r1_word_concord_left_right_context_tuple_list)):
                    concord_i = r1_word_concord_left_right_context_tuple_list[i][1]
                    l_context = r1_word_concord_left_right_context_tuple_list[i][2]
                    r_context = r1_word_concord_left_right_context_tuple_list[i][3]
                    if concord_i != r1_word_concord_left_right_context_tuple_list[i - 1][1]:
                        print(str(n) + ' ' * (5 - len(str(n))) + concord_i)
                        left_context_list_in_order.append(l_context)
                        right_context_list_in_order.append(r_context)
                        n += 1
            else:
                for i in range(len(r1_word_concord_left_right_context_tuple_list)):
                    concord_i = r1_word_concord_left_right_context_tuple_list[i][1]
                    l_context = r1_word_concord_left_right_context_tuple_list[i][2]
                    r_context = r1_word_concord_left_right_context_tuple_list[i][3]
                    if concord_i != r1_word_concord_left_right_context_tuple_list[i - 1][1]:
                        print(str(n) + ' ' * (5 - len(str(n))) + concord_i)
                        left_context_list_in_order.append(l_context)
                        right_context_list_in_order.append(r_context)
                        n += 1
        else:
            if sample_num:
                r1_word_concord_left_right_context_tuple_list = sample_with_fixed_intervals(
                    r1_word_concord_left_right_context_tuple_list, sample_num)
                for i in range(len(r1_word_concord_left_right_context_tuple_list)):
                    concord_i = l1_word_concord_left_right_context_tuple_list[i][1]
                    l_context = l1_word_concord_left_right_context_tuple_list[i][2]
                    r_context = l1_word_concord_left_right_context_tuple_list[i][3]
                    if concord_i != r1_word_concord_left_right_context_tuple_list[i - 1][1]:
                        print(str(n) + ' ' * (5 - len(str(n))) + concord_i)
                        left_context_list_in_order.append(l_context)
                        right_context_list_in_order.append(r_context)
                        n += 1
            else:
                for i in range(len(r1_word_concord_left_right_context_tuple_list)):
                    concord_i = l1_word_concord_left_right_context_tuple_list[i][1]
                    l_context = l1_word_concord_left_right_context_tuple_list[i][2]
                    r_context = l1_word_concord_left_right_context_tuple_list[i][3]
                    if concord_i != r1_word_concord_left_right_context_tuple_list[i - 1][1]:
                        print(str(n) + ' ' * (5 - len(str(n))) + concord_i)
                        left_context_list_in_order.append(l_context)
                        right_context_list_in_order.append(r_context)
                        n += 1

    # Condition 3
    else:
        if r1_alphabetical:
            if sample_num:
                r1_word_concord_left_right_context_tuple_list = sample_with_fixed_intervals(
                    r1_word_concord_left_right_context_tuple_list, sample_num)
                for i in range(len(r1_word_concord_left_right_context_tuple_list)):
                    concord_i = r1_word_concord_left_right_context_tuple_list[i][1]
                    l_context = r1_word_concord_left_right_context_tuple_list[i][2]
                    r_context = r1_word_concord_left_right_context_tuple_list[i][3]
                    if concord_i != r1_word_concord_left_right_context_tuple_list[i - 1][1]:
                        left_context_list_in_order.append(l_context)
                        right_context_list_in_order.append(r_context)
                        n += 1
            else:
                for i in range(len(r1_word_concord_left_right_context_tuple_list)):
                    concord_i = r1_word_concord_left_right_context_tuple_list[i][1]
                    l_context = r1_word_concord_left_right_context_tuple_list[i][2]
                    r_context = r1_word_concord_left_right_context_tuple_list[i][3]
                    if concord_i != r1_word_concord_left_right_context_tuple_list[i - 1][1]:
                        left_context_list_in_order.append(l_context)
                        right_context_list_in_order.append(r_context)
                        n += 1
        else:
            if sample_num:
                r1_word_concord_left_right_context_tuple_list = sample_with_fixed_intervals(
                    r1_word_concord_left_right_context_tuple_list, sample_num)
                for i in range(len(r1_word_concord_left_right_context_tuple_list)):
                    concord_i = l1_word_concord_left_right_context_tuple_list[i][1]
                    l_context = l1_word_concord_left_right_context_tuple_list[i][2]
                    r_context = l1_word_concord_left_right_context_tuple_list[i][3]
                    if concord_i != r1_word_concord_left_right_context_tuple_list[i - 1][1]:
                        left_context_list_in_order.append(l_context)
                        right_context_list_in_order.append(r_context)
                        n += 1
            else:
                for i in range(len(r1_word_concord_left_right_context_tuple_list)):
                    concord_i = l1_word_concord_left_right_context_tuple_list[i][1]
                    l_context = l1_word_concord_left_right_context_tuple_list[i][2]
                    r_context = l1_word_concord_left_right_context_tuple_list[i][3]
                    if concord_i != r1_word_concord_left_right_context_tuple_list[i - 1][1]:
                        left_context_list_in_order.append(l_context)
                        right_context_list_in_order.append(r_context)
                        n += 1

    print('-' * (left_context_size + right_context_size) + '\n' + '-' * (left_context_size + right_context_size) + '\n')
    concord_number = n - 1

    return concord_number, pattern_str, l1_freq_list, r1_freq_list, node_word_freq_list, \
           left_context_list_in_order, right_context_list_in_order


def return_left_right_context_list(pattern_str, corpus_path, delete_pattern_str=None, select_pattern_str=None,
                                   encoding='utf8',
                                   ignore_case=True, r1_alphabetical=None, left_context_size=100, right_context_size=100,
                                   save_concord=None, show_concord=None,
                                   remove_blank_lines=None, remove_pos=True, sample_num=None, stop_at_boundary=True):
    """
    Returns ONLY the left & right context of concordance lines.
    """
    temp_result = concord_one_pattern(pattern_str=pattern_str, corpus_path=corpus_path, encoding=encoding,
                                      ignore_case=ignore_case, r1_alphabetical=r1_alphabetical,
                                      delete_pattern_str=delete_pattern_str,
                                      left_context_size=left_context_size, stop_at_boundary=stop_at_boundary,
                                      right_context_size=right_context_size,
                                      remove_blank_lines=remove_blank_lines,
                                      remove_pos=remove_pos, sample_num=sample_num,
                                      select_pattern_str=select_pattern_str,
                                      save_concord=save_concord, show_concord=show_concord)
    left_context_list, right_context_list = temp_result[5], temp_result[6]
    return left_context_list, right_context_list


def save_or_show_concord(search_pattern_str_list, corpus_path, delete_pattern_str=None, select_pattern_str=None,
                         encoding='utf8', save_concord=None, show_concord=None,
                         ignore_case=True, r1_alphabetical=None, left_context_size=100,
                         right_context_size=100,
                         remove_blank_lines=None, remove_pos=True, show_l1_r1_list=None, show_node_word_list=None,
                         sample_num=None,
                         stop_at_boundary=True
                         ):
    """
    re_search_pattern_str_list: a LIST OF STRING of regular expression pattern
    corpus_path: Either a file path or a directory path. All the files under the directory path should be in txt format.
    r1_alphabetical: default None and the concordances will be arranged according to the alphabetical order of
        the first word to the LEFT of the node word ; if set True, the first word to the RIGHT of the node word.
    save_concord: default None and if set True, the concordances will be saved in a file without the screen view.
    show_concord: default None and if set True it will lead to a screen view of all the concordances;
    remove_blank_lines:  I recommend you to set it True if you haven't done this to your texts; but this may take
        considerable time for the program to run, so it's wiser to pre-process your text (remove all the blank lines)
        before feeding them into the program.
    """
    a = time.time()
    concord_number_list, pattern_str_list, l1_freq_list_list, r1_freq_list_list, node_word_freq_list_list \
        = [], [], [], [], []
    for pattern in search_pattern_str_list:
        temp_result = concord_one_pattern(pattern, corpus_path=corpus_path, encoding=encoding,
                                          ignore_case=ignore_case, r1_alphabetical=r1_alphabetical,
                                          save_concord=save_concord, delete_pattern_str=delete_pattern_str,
                                          left_context_size=left_context_size, stop_at_boundary=stop_at_boundary,
                                          right_context_size=right_context_size, show_concord=show_concord,
                                          remove_blank_lines=remove_blank_lines,
                                          remove_pos=remove_pos, sample_num=sample_num,
                                          select_pattern_str=select_pattern_str,
                                          )

        concord_number_list.append(temp_result[0])
        pattern_str_list.append(temp_result[1])
        l1_freq_list_list.append(temp_result[2])
        r1_freq_list_list.append(temp_result[3])
        node_word_freq_list_list.append(temp_result[4])

    output_list = list(zip(
        concord_number_list, pattern_str_list, l1_freq_list_list, r1_freq_list_list, node_word_freq_list_list))
    for concord_number, pattern_str, l1_list, r1_list, node_word_freq_list_list in output_list:
        print('-' * (left_context_size + right_context_size))
        print(f"You got ({concord_number}) instances with \"{pattern_str}\" from \"{corpus_path}\".")
        if show_l1_r1_list:
            print(f"L1 words: {l1_list[:50]}")
            print(f"R1 words: {r1_list[:50]}")
        if show_node_word_list:
            print(f"Node words: {node_word_freq_list_list}")
    b = time.time()
    print('-' * (left_context_size + right_context_size) + f"\nRunning time: {round(b - a, 2)}s\n")
