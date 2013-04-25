#!/usr/bin/env python

def main():
    import sys
    
    
    class String(object):
        
        def __init__(self, s):
            self.s = s
            self._vowels = False
            self._words = False
            self._max_word_len = False
        
        def vowels(self):
            if self._vowels is not False:
                return self._vowels
            num = 0
            for i in self.s:
                if i in 'aeiou':
                    num += 1
            self._vowels = num
            return num
        
        def words(self):
            if self._words is not False:
                return self._words
            num = len(self.s.split())
            self._words = num
            return num
        
        def max_word_len(self):
            if self._max_word_len is not False:
                return self._max_word_len
            m = 0
            for word in self.s.split():
                if len(word) > m:
                    m = len(word)
            self._max_word_len = m
            return m
        
        def __cmp__(self, other):
            if self.vowels() != other.vowels():
                return int.__cmp__(self.vowels(), other.vowels())
            elif self.words() != other.words():
                return int.__cmp__(self.words(), other.words())
            return int.__cmp__(self.max_word_len(), other.max_word_len())
    
    
    strings = []
    for line in sys.stdin.readlines():
        strings.append(String(line.replace('\n', '')))
    
    strings.sort()
    
    for string in strings:
        print string.s

if __name__ == '__main__':
    main()

