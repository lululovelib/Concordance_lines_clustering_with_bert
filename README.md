Parameters	of save_or_show_concord in cluster.py module 

search_pattern_str_list: A list of string of regular expression patterns.
corpus_path: Either a file path or a directory path. All the files under the directory path should be in txt format.
delete_pattern_str: 	The regular expression pattern the matched concordance lines of which will be removed from the resulted lines of the initial search.
select_pattern_str: 	The regular expression pattern the matched concordance lines of which will be reserved among the resulted lines of the initial search.
encoding:	The encoding of both the input and output text files.
save_concord:	Default False, leading to a screen view of all the concordances; if set False the concordances will be saved in a file without the screen view. It should be noted that when displayed on screen, the concordance lines will be aligned by the position of the node words and two more spaces will be inserted between the node words and their right and left context; and when saved in files, the concordance lines will be aligned to the left without the extra spaces that highlights the node words.
sample_num:	The number of concordance lines to be samples. The sampling is done in such a way that every two consecutive sampled lines have the same interval. If set None, the concordance lines will be returned without sampling. If the value is larger than the total number of the concordance lines, the program will still return all the lines. 
stop_at_boundary:	If set True, each of the concordance lines will be cut at the beginning or end a sentence or paragraph. “.”, “!”, “?”, single quote and double quote signs follow by any blank space (represented by “\s+”) are identified as the boundary of the sentence or paragraph. 
ignore_case:	If set True, the search will be case-sensitive.
r1_alphabetical:	If set True, the concordance lines will be arranged by the alphabetical order of the collocate: word to the right of the node. If set False, they will be arranged alphabetically according to the collocate word to the left.   
left_context_size:	The number of characters to the left of the node in each concordance line.
right_context_size:	The number of characters to the right of the node in each concordance line.
remove_blank_lines:	It is important to make sure that there is no blank lines in all the input txt files because they may lead to the failure in aligning the concordance lines which brings difficulties to later observation. Set this True if you haven't removed all the blank lines form your texts; but doing this in the program may take considerable time for the program to run, so it's wiser to remove all the blank lines before feeding the files into the program.
remove_pos:	If set True, all the part-of-speech tags following a word and an underline “_” will be removed.
show_l1_r1_list:	If set True, the L1 and R1 collates in all the returned concordance lines will be presented by the order of their frequency. If set False, this won’t be presented.
show_node_word_list:	If set True, the node words in all the returned concordance lines will be presented by the order of their frequency. If set False, this won’t be presented. 

