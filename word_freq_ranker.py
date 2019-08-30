import sys
from operator import itemgetter

	
def word_clean(word):
    alpha = "abcdefghijklmnopqrstuvwxyz'"
    i = 0
    word = word.lower()
    while i < len(word):
        if word[i] not in alpha:
            if i == len(word) - 1:
                word = word[:i]
            else:
                word = word[:i] + word[i+1:]
        i += 1
    return word

def rank(filename):
    # Given a text file, this reads the files to creates a new text file containing all
    # words from the original document with their frequencies
    word_file = open(filename, "r")

    word_dict = {}
    for line in word_file:
        for word in line.split():
            word = word_clean(word)
            if word in word_dict:
                word_dict[word] += 1
            else:
                word_dict[word] = 1

    word_list = []
    for word in word_dict:
        word_list.append((word, word_dict[word]))
        word_list.sort(key=itemgetter(1), reverse=True)
		
    wff_name = "Word Frequencies for '" + filename[:-4] + "'.txt"
    ranked_word_file = open(wff_name, "w")
    for item in word_list:
        entry = item[0] + "  :  " + str(item[1]) + '\n'
        ranked_word_file.write(entry)

    print("Top 3 Most Frequent Words:")
    for i in range(1, 4):
        entry = word_list[i-1][0] + "  :  " + str(word_list[i-1][1])
        print(i, ". ", entry, sep='')

    word_file.close()
    ranked_word_file.close()
	
    return


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 word_rank.py [text file]")
        exit(0)
    if sys.argv[-1][-4:] != '.txt':
        print("Invalid file type (not a text file).")
        exit(0)
    file = sys.argv[1]
    rank(file)
    exit(0)
