#!/usr/bin/env python

def main():
    import sys
    
    
    class String(object):
        
        def __init__(self, s):
            self.s = s
            self.vowels = self._vowels()
            self.words = self._words()
            self.max_word_len = self._max_word_len()
        
        def _vowels(self):
            num = 0
            for i in self.s:
                if i in 'aeiouAEIOU':
                    num += 1
            self._vowels = num
            return num
        
        def _words(self):
            num = len(self.s.split())
            self._words = num
            return num
        
        def _max_word_len(self):
            m = 0
            for word in self.s.split():
                if len(word) > m:
                    m = len(word)
            self._max_word_len = m
            return m
    
    strings = []
    for line in sys.stdin.readlines():
        strings.append(String(line.replace('\n', '')))
    
    # http://docs.python.org/2/howto/sorting.html
    #strings.sort(key=lambda x: x.max_word_len)
    #strings.sort(key=lambda x: x.words)
    #strings.sort(key=lambda x: x.vowels)
    strings.sort(key=lambda x: (x.vowels, x.words, x.max_word_len))
    
    for string in strings:
        print string.s

if __name__ == '__main__':
    main()

