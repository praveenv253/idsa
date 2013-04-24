#!/usr/bin/env python

# No classes!

def main():
    import sys

    def inorder(bst):
        if bst[1]:
            inorder(bst[1])
        sys.stdout.write((str(bst[0]) + '\n') * bst[3])
        if bst[2]:
            inorder(bst[2])
    
    def preorder(bst):
        sys.stdout.write(str(bst[0]) + '\n')
        if bst[1]:
            preorder(bst[1])
        if bst[2]:
            preorder(bst[2])
    
    def postorder(bst):
        if bst[1]:
            postorder(bst[1])
        if bst[2]:
            postorder(bst[2])
        sys.stdout.write(str(bst[0]) + '\n')
    
    bst = ['', [], [], 1]
    
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
                            loc[2] = [value, [], [], 1]
                            found = True
                    elif value < loc[0]:
                        if loc[1]:
                            loc = loc[1]
                        else:
                            loc[1] = [value, [], [], 1]
                            found = True
                    else:
                        loc[3] += 1
                        found = True
        
        elif op == 'print_sort':
            if bst[0]:
                inorder(bst)
        elif op == 'print_pre':
            if bst[0]:
                preorder(bst)
        elif op == 'print_post':
            if bst[0]:
                postorder(bst)


if __name__ == '__main__':
    main()
