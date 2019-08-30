import time


def remove_spaces(letters):
    clean=""
    for i in range(len(letters)):
        if letters[i] != " ":
            clean += letters[i]
        else:
            continue
    return clean


def str_sub(whole, part):
    i=0
    j=0
    new_str = ""
    while j < len(part):
        if part[j] == whole[i]:
            j += 1
            i += 1
        else:
            new_str += whole[i]
            i += 1
    return new_str + whole[i:]
	
def print_list(list):
	str = ""
	for item in list:
		str += item + ", "
	return str[:-2]


def find_a_word(letters, dict):                                 # Works
    print("Looking for a word with '", letters, "'", sep='')
    dict.seek(0)
    valid = []
    for word in dict:
        word = word[:-1]
        # print(word)
        #time.sleep(1)
        if sorted(letters) == sorted(word):
            # print("DING")
            valid.append(word)
    return valid


def find_words(letters, dict):
    dict.seek(0)
    print("Looking for words with '", letters, "'", sep='')
    clean = remove_spaces(letters)
    end_num = len(remove_spaces(letters))
    valid = []
    return find_words_help(clean, dict, valid, end_num)


def find_words_help(letters, dict, words, goal_num, building=""):           # Only does 1 sweep
    # print("letters: ",letters, "building: ", building)
    if len(remove_spaces(building)) == goal_num:
        # print("DING")
        words.append(building[:-1])

    dict.seek(0)
    # print("i: ", i, "chunk: ", letters[:i+1])
    for word in dict:
        # print("word: ", word)
        word = word[:-1]
        if word in letters and (len(word) > 1 || word == "I" || word == "a"):
            # print("found a start with", word)
            find_words_help(str_sub(letters, word), dict, words, goal_num, building + word + " ")
    return words


def main():
    dict_name = input("Enter the filename of your dictionary text file: ")
    try:
        my_dict = open(dict_name, 'r')
    except FileNotFoundError:
        print("No file called '", dict_name, "' found.", sep="")
        return -1
    letters_to_use = input("Enter letters to find words with: ")
    if not(remove_spaces(letters_to_use).isalpha()):
        print("Please only include letters.")
        my_dict.close()
        return -1
    if ' ' in letters_to_use:
        print("Spaces should not be included at this time.")
        # print(find_words(letters_to_use, my_dict))
    else:
        print("The words that can be made from ", letters_to_use, " are: ", print_list(find_a_word(remove_spaces(letters_to_use), my_dict)), ".", sep='')
    my_dict.close()
    return 0

if __name__ == "__main__":
	main()