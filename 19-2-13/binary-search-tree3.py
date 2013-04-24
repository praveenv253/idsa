#!/usr/bin/env python

# No classes and no functions!

def main():
    import sys
            
    bst = ['', [], [], 1, False]
    
    for line in sys.stdin.readlines():
        
        op = line.split()[0]
        
        if op == 'insert':
            value = float(line.split()[1])
            if bst[0] is '':
                bst[0] = value
            else:
                found = False
                loc = bst
                while not found:
                    if value > loc[0]:
                        if loc[2]:
                            loc = loc[2]
                        else:
                            loc[2] = [value, [], [], 1, False]
                            found = True
                    elif value < loc[0]:
                        if loc[1]:
                            loc = loc[1]
                        else:
                            loc[1] = [value, [], [], 1, False]
                            found = True
                    else:
                        loc[3] += 1
                        found = True
        
        elif op == 'print_sort':
            stack = []
            stack.append(bst)
            while stack:
                node = stack.pop()
                if node[1] and not node[1][4]:
                    stack.append(node)
                    stack.append(node[1])
                    continue
                sys.stdout.write((str(node[0]) + '\n') * node[3])
                node[4] = True
                if node[2] and not node[2][4]:
                    stack.append(node[2])


if __name__ == '__main__':
    main()
