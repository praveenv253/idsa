#!/usr/bin/env python

def main():
    import sys
    
    strings = []
    for line in sys.stdin.readlines():
        s = line.replace('\n', '')
        vowels = 0
        words = 0
        max_word_len = 0
        chars = 0
        for i in s:
            if i in 'aeiouAEIOU':
                vowels += 1
            elif i == ' ':
                words += 1
                chars = 0
                continue
            chars += 1
            if chars > max_word_len:
                max_word_len = chars
        if words:
            words += 1
        strings.append(([vowels, words, max_word_len], s))
    
    # http://docs.python.org/2/howto/sorting.html
    strings.sort(key=lambda x: x[0])
    
    for string in strings:
        print string[1]

if __name__ == '__main__':
    main()

