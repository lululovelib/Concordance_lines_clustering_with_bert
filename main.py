from concord import *
from chunker import *
from cluster import *

flag1 = True
# flag1 = False
if flag1:
    save_or_show_concord(
        ###########  REGULAR EXPRESSION PATTERN LIST ############
        search_pattern_str_list=[
            "faced\swith"
        ],
        delete_pattern_str="(are|\w+[’\']re|am|\w+[’\']m|is|\w+[’\']s|be|was|were|been)\s(\w+\s)?(likely\sto\sbe\s|being\s)?faced\swith",
        # select_pattern_str="",
        #######################  CORPORA  ####################
        # corpus_path="E:\\corpora\\BNC_lite",
        corpus_path="E:\\corpora\\UKBC_lite",
        # corpus_path="E:\\corpora\\CARE_lite",
        # corpus_path="E:\\corpora\\UKBC_tagged_lite",
        # corpus_path="E:\\corpora\\CARE_tagged_lite",
        ######################  SETTINGS  ######################
        # save_concord=True,
        # sample_num=100,
        # remove_pos=False,
        # r1_alphabetical=True,
        left_context_size=100,
        right_context_size=100,
        show_l1_r1_list=True,
        show_node_word_list=True,
    )

#####################################################################################################

# flag2 = True
flag2 = False
if flag2:

    tagged_tuple_list = concord_one_pattern(
        ###########  REGULAR EXPRESSION PATTERN  ############
        pattern_str="undergo_\w+",
        #######################  CORPORA  ######################
        # corpus_path="E:\\corpora\\BNC_lite",
        # corpus_path="E:\\corpora\\UKBC_lite",
        # corpus_path="E:\\corpora\\CARE_lite",
        corpus_path="E:\\corpora\\UKBC_tagged_lite",
        # corpus_path="E:\\corpora\\CARE_tagged_lite",
        ######################  SETTINGS  ######################
        remove_pos=False,  # The variable remove_pos has to be set False here!
    )[5]

    raw_tuple_list = concord_one_pattern(
        ###########  REGULAR EXPRESSION PATTERN  ############
        pattern_str="undergo_\w+",
        #######################  CORPORA  ######################
        # corpus_path="E:\\corpora\\BNC_lite",
        # corpus_path="E:\\corpora\\UKBC_lite",
        # corpus_path="E:\\corpora\\CARE_lite",
        corpus_path="E:\\corpora\\UKBC_tagged_lite",
        # corpus_path="E:\\corpora\\CARE_tagged_lite",
        ######################  SETTINGS  ######################
    )[5]

    # temp_result_tuple_list: [(r1_word, concordance_line_spaced, concordance_line_raw, left_context,
    # right_context, node_word), (), ..., ()]
    r1np_list = []
    for r in tagged_tuple_list:
        if return_np_patterns(r[4]) is not None:
            r1np_list.append(return_np_patterns(r[4])[0])
        else:
            r1np_list.append("")
    concordance_list_raw = [temp_tuple[2] for temp_tuple in raw_tuple_list]
    concordance_list_spaced = [temp_tuple[1] for temp_tuple in raw_tuple_list]
    r1_np_tuple_list = list(zip(r1np_list, concordance_list_spaced))
    full_concordance_tuple_list = list(zip(concordance_list_raw, concordance_list_spaced))

    corpus = r1_np_tuple_list[:20]
    # corpus = full_concordance_tuple_list[:20]

    kmeans_clustering(corpus, 3)
    # agglomerative_clustering(corpus, 1.5)
