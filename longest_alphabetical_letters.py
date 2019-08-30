import sys


def check_word(word):
    if len(word) < 1:
        return False
    previous_letter = 0
    repeat_count = 0
    for letter in word:
        letter = ord(letter.lower())
        if letter >= previous_letter:
            if letter == previous_letter:
                repeat_count += 1
                if repeat_count == 3:
                    return False
                else:
                    continue
            previous_letter = letter
            repeat_count = 0
            continue
        else:
            return False
    return True


def print_list(list):
    output = ""
    for item in list:
        output += str(item) + ", "
    return output[:-2]


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 law.py [dictionary text file]")
        exit(0)
    dict_filename = sys.argv[1]
    dictionary = open(dict_filename, "r")
    max_words = []
    max_length = 0
    for line in dictionary:
        for word in line.split():
            if check_word(word):
                if len(word) > max_length:
                    max_words = [word]
                    max_length = len(word)
                elif len(word) == max_length:
                    max_words.append(word)
    print("The longest word given with letters in alphabetical order is: ", print_list(max_words), ", with a length of ", max_length, " letters.", sep='')
    exit(0)
