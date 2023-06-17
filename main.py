from concord import main as concord

# from keywords import *
# from cluster import *

concord(
    ###########  REGULAR EXPRESSION PATTERN(S)  ############
    search_pattern_str_list=[
"(it\s(\w+\s){1,3}|it[\'‘’]s\s(\w+\s){,3})reported(\sthat)?"
   ],

    #######################  CORPORA  ######################
    # corpus_path="E:\\corpora\\BNC_lite",
    corpus_path="E:\\corpora\\UKBC_lite",
    # corpus_path="E:\\corpora\\CARE_lite",
    # corpus_path="E:\\corpora\\UKBC_tagged_lite",
    # corpus_path="E:\\corpora\\CARE_tagged_lite",

    ######################  SETTINGS  ######################
    r1_alphabetical=True,
    # ignore_case=False,
    # remove_pos=True,
    # save_file=True,
    # show_l1_r1_list=True,
    # show_node_word_list=True,
    delete_pattern_str="reported\s(to|by|about)|comes after TfL|earned her a reported|turned down a reported|bought for a reported|"
                      "also reported|came after media reported|announced a reported|helped had reported|is observed that reported|"
                      "is unclear whether reported|is assumed the reported",

# select_pattern_str=,
    left_context_size=200,
    right_context_size=200,
    # sample_num=100
)
