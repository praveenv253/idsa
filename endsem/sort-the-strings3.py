#!/usr/bin/env python

def main():
    import sys
    import re
    
    # http://docs.python.org/2/library/re.html
    # http://docs.python.org/2/howto/regex.html
    v = re.compile(r'[aeiouAEIOU]')
    w = re.compile(r' ')
    m = re.compile(r'\w')
    strings = []
    for line in sys.stdin.readlines():
        s = line.replace('\n', '')
        """
        vowels = 0
        for i in s:
            if i in 'aeiouAEIOU':
                vowels += 1
        a = s.split()
        words = len(a)
        max_word_len = 0
        for word in a:
            if len(word) > max_word_len:
                max_word_len = len(word)
        """
        vowels = len(v.findall(s))
        words = len(w.findall(s)) + 1
        max_word_len = 0
        for word in s.split():
            if len(word) > max_word_len:
                max_word_len = len(word)
        strings.append(([vowels, words, max_word_len], s))
    
    # http://docs.python.org/2/howto/sorting.html
    strings.sort(key=lambda x: x[0])
    
    for string in strings:
        print string[1]

if __name__ == '__main__':
    main()

