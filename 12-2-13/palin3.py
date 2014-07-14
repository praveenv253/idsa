#!/usr/bin/env python

def main():
    import sys

    # Throw away the first line
    sys.stdin.readline()
    for q in sys.stdin.readlines():
        q = q[:-1]   # Remove the trailing newline character
        l = len(q)
        if l == 1:
            # Take care of single digit input and single 9
            if q == '9':
                sys.stdout.write('11\n')
            else:
                sys.stdout.write(str(int(q) + 1) + '\n')
            continue
        if l % 2 == 0:
            # Look at numbers from the middle outwards and compare
            i = l/2
            j = i-1
            while q[i] == q[j] and j:
                i += 1
                j -= 1

            # If the entire string is a palindrome, then j would have become 0
            # and i would have become l-1
            if j == 0 and q[i] == q[j]:
                # The next palindrome involves incrementing from the middle and
                # taking care of carry
                pos = l/2 - 1
                if q[pos] == '9':
                    replacement = 0
                else:
                    replacement = str(int(q[pos]) + 1)
                # Take care of possible nines in the middle
                while replacement == 0 and pos > 0:
                    pos -= 1
                    if q[pos] == '9':
                        replacement = 0
                    else:
                        replacement = str(int(q[pos]) + 1)

                # By now, either replacement worked out, or pos is at zero.
                if pos == 0 and replacement == 0:
                    # All nines!
                    sys.stdout.write('1' + '0'*(len(q)-1) + '1\n')
                    continue                         # Go on to next input line
                # Not all nines. pos points to where replacement worked out.
                # Print out everything upto pos, excluded. Then print the
                # replacement, and finally print a suitable number of zeros.
                half_string = q[:pos] + replacement + '0'*(l/2-1-pos)
                sys.stdout.write(half_string + half_string[::-1] + '\n')
                continue

            # The entire string is not a palindrome. j may be zero, but then
            # the last digit did not match.
            if q[i] < q[j]:
                # This is the simplest case where the first non-matching i is
                # less than j. Meaning, we can just make i=j and be done.
                sys.stdout.write(q[:i] + q[:j+1][::-1] + '\n')
                continue
            else:
                # Otherwise, we need to start incrementing from the middle.
                pos = l/2 - 1
                if q[pos] == '9':
                    replacement = 0
                else:
                    replacement = str(int(q[pos]) + 1)
                # Take care of possible nines in the middle
                while replacement == 0 and pos > 0:
                    pos -= 1
                    if q[pos] == '9':
                        replacement = 0
                    else:
                        replacement = str(int(q[pos]) + 1)
                # By now, either replacement worked out, or pos is at zero.
                # Not all nines. pos points to where replacement worked out.
                # Print out everything upto pos, excluded. Then print the
                # replacement, and finally print a suitable number of zeros.
                half_string = q[:pos] + replacement + '0'*(l/2-1-pos)
                sys.stdout.write(half_string + half_string[::-1] + '\n')
                continue

        # Otherwise, string length is odd
        else:
            # Look at numbers from the middle outwards and compare
            i = l/2 + 1
            j = i-2
            while q[i] == q[j] and j:
                i += 1
                j -= 1

            # If the entire string is a palindrome, then j would have become 0
            # and i would have become l-1
            if j == 0 and q[i] == q[j]:
                # The next palindrome involves incrementing from the middle and
                # taking care of carry
                pos = l/2
                if q[pos] == '9':
                    replacement = 0
                else:
                    replacement = str(int(q[pos]) + 1)
                # Take care of possible nines in the middle
                while replacement == 0 and pos > 0:
                    pos -= 1
                    if q[pos] == '9':
                        replacement = 0
                    else:
                        replacement = str(int(q[pos]) + 1)
                # By now, either replacement worked out, or pos is at zero.
                if pos == 0 and replacement == 0:
                    # All nines!
                    sys.stdout.write('1' + '0'*(len(q)-1) + '1\n')
                    continue                         # Go on to next input line
                # Not all nines. pos points to where replacement worked out.
                # Print out everything upto pos, excluded. Then print the
                # replacement, and finally print a suitable number of zeros.
                if pos == l/2:
                    half_string = q[:pos]
                    sys.stdout.write(half_string + replacement + half_string[::-1] + '\n')
                else:
                    half_string = q[:pos] + replacement + '0'*(l/2-pos)
                    sys.stdout.write(half_string + '0' + half_string[::-1] + '\n')
                continue

            # The entire string is not a palindrome. j may be zero, but then
            # the last digit did not match.
            if q[i] < q[j]:
                # This is the simplest case where the first non-matching i is
                # less than j. Meaning, we can just make i=j and be done.
                sys.stdout.write(q[:i] + q[:j+1][::-1] + '\n')
                continue
            else:
                # Otherwise, we need to start incrementing from the middle.
                pos = l/2
                if q[pos] == '9':
                    replacement = 0
                else:
                    replacement = str(int(q[pos]) + 1)
                # Take care of possible nines in the middle
                while replacement == 0 and pos > 0:
                    pos -= 1
                    if q[pos] == '9':
                        replacement = 0
                    else:
                        replacement = str(int(q[pos]) + 1)
                # By now, either replacement worked out, or pos is at zero.
                # Not all nines. pos points to where replacement worked out.
                # Print out everything upto pos, excluded. Then print the
                # replacement, and finally print a suitable number of zeros.
                if pos == l/2:
                    half_string = q[:pos]
                    sys.stdout.write(half_string + replacement + half_string[::-1] + '\n')
                else:
                    half_string = q[:pos] + replacement + '0'*(l/2-1-pos)
                    sys.stdout.write(half_string + '0' + half_string[::-1] + '\n')
                continue

if __name__ == '__main__':
    main()
