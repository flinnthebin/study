#!/bin/python3

import os
import time
from termcolor import colored

class Question:
  def __init__(self, consider, prompt, answer, feedback):
    self.consider = consider
    self.prompt = prompt
    self.answer = answer
    self.feedback = feedback

w1_regexp_q = [
"Write a regexp to match C preprocessor commands in a C program source file:",
"Write a regexp to match all the lines in a C program except preprocessor commands:",
"Write a regexp to match all lines in a C program with trailing whitespace:",
"Write a regexp to match the names 'Barry', 'Harry', 'Larry' and 'Parry':",
"Write a regexp to match a string containing the word 'hello', followed later by the word 'world':",
"Write a regexp to match the word 'calendar' and mis-spellings where 'a' is replaced with 'e' or vice-versa:",
"Write a regexp to match a list of positive integers separated by commas, e.g. 2,4,8,16,32:",
"Write a regexp to match a C string whose last character is newline:",
]

w1_regexp_c = [
"""
 .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------. 
| .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |
| |  _______     | || |  _________   | || |    ______    | || |  _________   | || |  ____  ____  | || |   ______     | |
| | |_   __ \    | || | |_   ___  |  | || |  .' ___  |   | || | |_   ___  |  | || | |_  _||_  _| | || |  |_   __ \   | |
| |   | |__) |   | || |   | |_  \_|  | || | / .'   \_|   | || |   | |_  \_|  | || |   \ \  / /   | || |    | |__) |  | |
| |   |  __ /    | || |   |  _|  _   | || | | |    ____  | || |   |  _|  _   | || |    > `' <    | || |    |  ___/   | |
| |  _| |  \ \_  | || |  _| |___/ |  | || | \ `.___]  _| | || |  _| |___/ |  | || |  _/ /'`\ \_  | || |   _| |_      | |
| | |____| |___| | || | |_________|  | || |  `._____.'   | || | |_________|  | || | |____||____| | || |  |_____|     | |
| |              | || |              | || |              | || |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------' """
]

w1_regexp_a = [
"^#",
"^[^#]",
"\s$",
"[BHLP]arry",
"hello.*world",
"c[ae]l[ae]nd[ae]r",
"[1-9][0-9]*(,[1-9][0-9]*)*",
'"[^"]*\\n"',
]

w1_regexp_f = [
"""
^ - anchor to start of string
# - C preprocessor commands begin with a hash""",

"""
^ - anchor to start of string
[ - open character class
^ - not any of the following characters in the class
# - C preprocessor commands begin with a hash
] - close character class""",

"""
\ - escape character
s - escaped s refers to whitespace character
$ - anchor to end of string""",

"""
[BHLP] - any character in this set of 4 can begin the string
arry -  string concatenated to characters in the character class""",

"""
hello - string to match
.* - any number of characters repeated any number of times
world - string to complete match""",

"""
[ae]- any character in this set of 2 can take the place of the character class in the string""",

"""
[1-9][0-9]* - character classes, repeated any number of times
(,[1-9][0-9]*)* - a comma to separate, followed by character classes repeated any number of times, repeated again any number of times.""",

'''
" - a quotation to identify the start of the string
[^"] - not any of the following characters (no end quotation to finish the string)
*\\n" - any number of non-quotation characters followed by a newline and finished with an end quotation''',
]

w2_head_c = [
"""
 .----------------.  .----------------.  .----------------.  .----------------. 
| .--------------. || .--------------. || .--------------. || .--------------. |
| |  ____  ____  | || |  _________   | || |      __      | || |  ________    | |
| | |_   ||   _| | || | |_   ___  |  | || |     /  \     | || | |_   ___ `.  | |
| |   | |__| |   | || |   | |_  \_|  | || |    / /\ \    | || |   | |   `. \ | |
| |   |  __  |   | || |   |  _|  _   | || |   / ____ \   | || |   | |    | | | |
| |  _| |  | |_  | || |  _| |___/ |  | || | _/ /    \ \_ | || |  _| |___.' / | |
| | |____||____| | || | |_________|  | || ||____|  |____|| || | |________.'  | |
| |              | || |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------'  '----------------' 

Consider this Unix password file
(usually found in /etc/passwd):

root:ZHolHAHZw8As2:0:0:root:/root:/bin/dash
jas:iaiSHX49Jvs8.:100:100:John Shepherd:/home/jas:/bin/bash
andrewt:rX9KwSSPqkLyA:101:101:Andrew Taylor:/home/andrewt:/bin/cat
postgres::997:997:PostgreSQL Admin:/usr/local/pgsql:/bin/bash
oracle::999:998:Oracle Admin:/home/oracle:/bin/bash
cs2041:rX9KwSSPqkLyA:2041:2041:COMP2041 Material:/home/cs2041:/bin/bash
cs3311:mLRiCIvmtI9O2:3311:3311:COMP3311 Material:/home/cs3311:/bin/zsh
cs9311:fIVLdSXYoVFaI:9311:9311:COMP9311 Material:/home/cs9311:/bin/bash
cs9314:nTn.JwDgZE1Hs:9314:9314:COMP9314 Material:/home/cs9314:/bin/fish
cs9315:sOMXwkqmFbKlA:9315:9315:COMP9315 Material:/home/cs9315:/bin/bash""",
]

w2_head_q = [
"Provide a command that would display the first three lines of the /etc/passwd:",
"Provide a command that would display the first 5 lines and the file name tag:",
]

w2_head_a = [
"head -n3 /etc/passwd",
"head -n5 -v /etc/passwd",
]
w2_head_f = [
"""
head -n 3 --lines=[-]3, print the first 3 lines instead of the first 10; with the leading '-', print all but the last 3 lines of each file
/etc/passwd - a colon-separated file that contains the following information:

1.  User name
2.  Encrypted password
3.  User ID number (UID)
4.  User's group ID number (GID)
5.  Full name of the user (GECOS)
6.  User home directory
7.  Login shell""",

  """
head -5 --lines=[-]5, print the first 5 lines instead of the first 10; with the leading '-', print all but the last 5 lines of each file
-v --verbose, always print headers giving file names
/etc/passwd - a colon-separated file that contains the following information:

1.  User name
2.  Encrypted password
3.  User ID number (UID)
4.  User's group ID number (GID)
5.  Full name of the user (GECOS)
6.  User home directory
7.  Login shell""",
]

w2_grep_c = [
"""
 .----------------.  .----------------.  .----------------.  .----------------. 
| .--------------. || .--------------. || .--------------. || .--------------. |
| |    ______    | || |  _______     | || |  _________   | || |   ______     | |
| |  .' ___  |   | || | |_   __ \    | || | |_   ___  |  | || |  |_   __ \   | |
| | / .'   \_|   | || |   | |__) |   | || |   | |_  \_|  | || |    | |__) |  | |
| | | |    ____  | || |   |  __ /    | || |   |  _|  _   | || |    |  ___/   | |
| | \ `.___]  _| | || |  _| |  \ \_  | || |  _| |___/ |  | || |   _| |_      | |
| |  `._____.'   | || | |____| |___| | || | |_________|  | || |  |_____|     | |
| |              | || |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------'  '----------------' 

Consider this Unix password file
(usually found in /etc/passwd):

root:ZHolHAHZw8As2:0:0:root:/root:/bin/dash
jas:iaiSHX49Jvs8.:100:100:John Shepherd:/home/jas:/bin/bash
andrewt:rX9KwSSPqkLyA:101:101:Andrew Taylor:/home/andrewt:/bin/cat
postgres::997:997:PostgreSQL Admin:/usr/local/pgsql:/bin/bash
oracle::999:998:Oracle Admin:/home/oracle:/bin/bash
cs2041:rX9KwSSPqkLyA:2041:2041:COMP2041 Material:/home/cs2041:/bin/bash
cs3311:mLRiCIvmtI9O2:3311:3311:COMP3311 Material:/home/cs3311:/bin/zsh
cs9311:fIVLdSXYoVFaI:9311:9311:COMP9311 Material:/home/cs9311:/bin/bash
cs9314:nTn.JwDgZE1Hs:9314:9314:COMP9314 Material:/home/cs9314:/bin/fish
cs9315:sOMXwkqmFbKlA:9315:9315:COMP9315 Material:/home/cs9315:/bin/bash""",
]

w2_grep_q = [
"""
Provide a command that would display lines belonging to class accounts
(assuming that class accounts have a username that starts with either 
"cs", "se", "bi" or "en", followed by four digits):""",
"Provide a command that would display the username of everyone whose shell is /bin/bash:",
]

w2_grep_a = [
"grep -e '^(cs|se|bi|en)[0-9]{4}:' /etc/passwd",
"grep -e ':/bin/bash$' /etc/passwd | cut -d':' -f1",
]

w2_grep_f = [
"""
grep -e  - print lines matching an extended-regexp pattern 
^(cs|se|bi|en) - anchor to start of the word an alternation of these 4 substrings
[0-9]{4}: - character class of strings 0-9 repeated 4 times
/etc/passwd - a colon-separated file that contains the following information:

1.  User name
2.  Encrypted password
3.  User ID number (UID)
4.  User's group ID number (GID)
5.  Full name of the user (GECOS)
6.  User home directory
7.  Login shell""",

"""
grep -e  - print lines matching an extended-regexp pattern 
':/bin/bash$'  - substring to match, anchored to the end of the string
/etc/passwd - a colon-separated file that contains the following information:

1.  User name
2.  Encrypted password
3.  User ID number (UID)
4.  User's group ID number (GID)
5.  Full name of the user (GECOS)
6.  User home directory
7.  Login shell

| - pipe stdout from previous command to stdin of next command

cut - remove sections from each line of files
-d':' --delimiter=: use ':' instead of TAB for field delimiter
-f1 - select only field 1"""
]

w2_cut_c = [
"""
 .----------------.  .----------------.  .----------------. 
| .--------------. || .--------------. || .--------------. |
| |     ______   | || | _____  _____ | || |  _________   | |
| |   .' ___  |  | || ||_   _||_   _|| || | |  _   _  |  | |
| |  / .'   \_|  | || |  | |    | |  | || | |_/ | | \_|  | |
| |  | |         | || |  | '    ' |  | || |     | |      | |
| |  \ `.___.'\  | || |   \ `--' /   | || |    _| |_     | |
| |   `._____.'  | || |    `.__.'    | || |   |_____|    | |
| |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------' 

Consider this Unix password file
(usually found in /etc/passwd):

root:ZHolHAHZw8As2:0:0:root:/root:/bin/dash
jas:iaiSHX49Jvs8.:100:100:John Shepherd:/home/jas:/bin/bash
andrewt:rX9KwSSPqkLyA:101:101:Andrew Taylor:/home/andrewt:/bin/cat
postgres::997:997:PostgreSQL Admin:/usr/local/pgsql:/bin/bash
oracle::999:998:Oracle Admin:/home/oracle:/bin/bash
cs2041:rX9KwSSPqkLyA:2041:2041:COMP2041 Material:/home/cs2041:/bin/bash
cs3311:mLRiCIvmtI9O2:3311:3311:COMP3311 Material:/home/cs3311:/bin/zsh
cs9311:fIVLdSXYoVFaI:9311:9311:COMP9311 Material:/home/cs9311:/bin/bash
cs9314:nTn.JwDgZE1Hs:9314:9314:COMP9314 Material:/home/cs9314:/bin/fish
cs9315:sOMXwkqmFbKlA:9315:9315:COMP9315 Material:/home/cs9315:/bin/bash""",
]
w2_cut_q = [
"Provide a command that will extract the 10th column of characters from /etc/passwd:",
"Provide a command that will extract the first 5 characters from each line from /etc/passwd:",
"Provide a command that will extract from the 3rd character to the end of each line from /etc/passwd:",
"Provide a command that will extract the 8 characters from the beginning of each line from /etc/passwd:",
"Provide a command that will extract the entire line from /etc/passwd:",
"Provide a command that would display the username of all users from /etc/passwd:",
"Provide a command that would display the username and home directory of everyone whose shell is /bin/bash:",
"Provide a command that would display the username, UID and GID of everyone whos shell is /bin/bash in /etc/passwd:",
"Provide a command that would display all fields except the login shell of everyone whos shell is /bin/bash in /etc/passwd:",
"Provide a command that would display the username, UID and GID of everyone whos shell is /bin/bash in /etc/passwd, changing the output delimeter to a #:",
"Provide a command that would display the username, home directory and shell of the oracle user in /etc/passwd, changing the output delimeter to a newline:",
"Provide a command that would create a tab-separated file passwords.txt containing only the username and password of each user:",
]
w2_cut_a = [
"cut -c10 /etc/passwd",
"cut -c1-5 /etc/passwd",
"cut -c3- /etc/passwd",
"cut -c-8 /etc/passwd",
"cut -c- /etc/passwd",
"cut -d':' -f1 /etc/passwd",
"grep -e ':/bin/bash$' /etc/passwd | cut -d':' -f1,6",
"grep -e ':/bin/bash$' /etc/passwd | cut -d':' -f1,3,4",
"grep '/bin/bash' /etc/passwd | cut -d':' --complement -s -f7",
"grep '/bin/bash' /etc/passwd | cut -d':' -s -f1,3,4 --output-delimiter='#'",
"grep oracle /etc/passwd | cut -d':' -f1,6,7 --output-delimiter=$'\\n'",
"cut -d':' -f1,2 /etc/passwd | tr ':' '\\t' > passwords.txt",
]
w2_cut_f = [
"""
cut - remove sections from each line of files
-c10 --characters=10 select only the 10th character
/etc/passwd - a colon-separated file that contains the following information:

1.  User name
2.  Encrypted password
3.  User ID number (UID)
4.  User's group ID number (GID)
5.  Full name of the user (GECOS)
6.  User home directory
7.  Login shell""",

"""
cut - remove sections from each line of files
-c1-5 --characters=1-5 select only characters 1-5
/etc/passwd - a colon-separated file that contains the following information:

1.  User name
2.  Encrypted password
3.  User ID number (UID)
4.  User's group ID number (GID)
5.  Full name of the user (GECOS)
6.  User home directory
7.  Login shell""",

"""
cut - remove sections from each line of files
-c3- --characters=3- select all characters after the third character until EOL
/etc/passwd - a colon-separated file that contains the following information:

1.  User name
2.  Encrypted password
3.  User ID number (UID)
4.  User's group ID number (GID)
5.  Full name of the user (GECOS)
6.  User home directory
7.  Login shell""",

"""
cut - remove sections from each line of files
-c-8 --characters=-8 select all characters until the 8th character on each line
/etc/passwd - a colon-separated file that contains the following information:

1.  User name
2.  Encrypted password
3.  User ID number (UID)
4.  User's group ID number (GID)
5.  Full name of the user (GECOS)
6.  User home directory
7.  Login shell""",

"""
cut - remove sections from each line of files
-c- --characters=- no number specified, select all characters
/etc/passwd - a colon-separated file that contains the following information:

1.  User name
2.  Encrypted password
3.  User ID number (UID)
4.  User's group ID number (GID)
5.  Full name of the user (GECOS)
6.  User home directory
7.  Login shell""",

"""
cut - remove sections from each line of files
-d':' --delimiter=: use ':' instead of TAB for field delimiter
-f1 - select only field 1
/etc/passwd - a colon-separated file that contains the following information:

1.  User name
2.  Encrypted password
3.  User ID number (UID)
4.  User's group ID number (GID)
5.  Full name of the user (GECOS)
6.  User home directory
7.  Login shell""",

"""
grep -e - print lines matching an extended-regexp pattern 
':/bin/bash$'  - substring to match, anchored to the end of the string
/etc/passwd - a colon-separated file that contains the following information:

1.  User name
2.  Encrypted password
3.  User ID number (UID)
4.  User's group ID number (GID)
5.  Full name of the user (GECOS)
6.  User home directory
7.  Login shell

| - pipe stdout from previous command to stdin of next command

cut - remove sections from each line of files
-d':' --delimiter=: use ':' instead of TAB for field delimiter
-f1,6 - select only fields 1 and 6""",

"""
grep -e - print lines matching an extended-regexp pattern 
':/bin/bash$'  - substring to match, anchored to the end of the string
/etc/passwd - a colon-separated file that contains the following information:

1.  User name
2.  Encrypted password
3.  User ID number (UID)
4.  User's group ID number (GID)
5.  Full name of the user (GECOS)
6.  User home directory
7.  Login shell

| - pipe stdout from previous command to stdin of next command

cut - remove sections from each line of files
-d':' --delimiter=: use ':' instead of TAB for field delimiter
-f1,4,6 - select only fields 1, 4 and 6""",

"""
grep -e - print lines matching an extended-regexp pattern 
':/bin/bash$'  - substring to match, anchored to the end of the string
/etc/passwd - a colon-separated file that contains the following information:

1.  User name
2.  Encrypted password
3.  User ID number (UID)
4.  User's group ID number (GID)
5.  Full name of the user (GECOS)
6.  User home directory
7.  Login shell

| - pipe stdout from previous command to stdin of next command

cut - remove sections from each line of files
-d':' --delimiter=: use ':' instead of TAB for field delimiter
--complement - complement the set of selected bytes, characters or fields (set algebra type complement)
-s --only-delimited. do not print lines not containing delimiters
-f7 - select only field 7""",

"""
grep -e - print lines matching an extended-regexp pattern 
':/bin/bash$'  - substring to match, anchored to the end of the string
/etc/passwd - a colon-separated file that contains the following information:

1.  User name
2.  Encrypted password
3.  User ID number (UID)
4.  User's group ID number (GID)
5.  Full name of the user (GECOS)
6.  User home directory
7.  Login shell

| - pipe stdout from previous command to stdin of next command

cut - remove sections from each line of files
-d':' --delimiter=: use ':' instead of TAB for field delimiter
-s --only-delimited. do not print lines not containing delimiters
-f1,4,6 - select only fields 1, 4 and 6
--output-delimiter='#' - use '#' as the output delimiter, the default is to use the input delimiter""",

"""
grep -e - print lines matching an extended-regexp pattern 
oracle - substring to match
/etc/passwd - a colon-separated file that contains the following information:

1.  User name
2.  Encrypted password
3.  User ID number (UID)
4.  User's group ID number (GID)
5.  Full name of the user (GECOS)
6.  User home directory
7.  Login shell

| - pipe stdout from previous command to stdin of next command

cut - remove sections from each line of files
-d':' --delimiter=: use ':' instead of TAB for field delimiter
-f1,6,7 - select only fields 1, 6 and 7
--output-delimiter=$'\n' - use newline as the output delimiter, the default is to use the input delimiter""",

"""
cut - remove sections from each line of files
-d':' --delimiter=: use ':' instead of TAB for field delimiter
-f1,2 - select only fields 1 and 2
/etc/passwd - a colon-separated file that contains the following information:

1.  User name
2.  Encrypted password
3.  User ID number (UID)
4.  User's group ID number (GID)
5.  Full name of the user (GECOS)
6.  User home directory
7.  Login shell

| - pipe stdout from previous command to stdin of next command

tr - translate or delete characters
':' - 
'\\t' > passwords.txt """,
]

w2_tr_c = [
"""
 .----------------.  .----------------. 
| .--------------. || .--------------. |
| |  _________   | || |  _______     | |
| | |  _   _  |  | || | |_   __ \    | |
| | |_/ | | \_|  | || |   | |__) |   | |
| |     | |      | || |   |  __ /    | |
| |    _| |_     | || |  _| |  \ \_  | |
| |   |_____|    | || | |____| |___| | |
| |              | || |              | |
| '--------------' || '--------------' |
 '----------------'  '----------------' 

Consider this Unix password file
(usually found in /etc/passwd):

root:ZHolHAHZw8As2:0:0:root:/root:/bin/dash
jas:iaiSHX49Jvs8.:100:100:John Shepherd:/home/jas:/bin/bash
andrewt:rX9KwSSPqkLyA:101:101:Andrew Taylor:/home/andrewt:/bin/cat
postgres::997:997:PostgreSQL Admin:/usr/local/pgsql:/bin/bash
oracle::999:998:Oracle Admin:/home/oracle:/bin/bash
cs2041:rX9KwSSPqkLyA:2041:2041:COMP2041 Material:/home/cs2041:/bin/bash
cs3311:mLRiCIvmtI9O2:3311:3311:COMP3311 Material:/home/cs3311:/bin/zsh
cs9311:fIVLdSXYoVFaI:9311:9311:COMP9311 Material:/home/cs9311:/bin/bash
cs9314:nTn.JwDgZE1Hs:9314:9314:COMP9314 Material:/home/cs9314:/bin/fish
cs9315:sOMXwkqmFbKlA:9315:9315:COMP9315 Material:/home/cs9315:/bin/bash""",

"""
.----------------.  .----------------. 
| .--------------. || .--------------. |
| |  _________   | || |  _______     | |
| | |  _   _  |  | || | |_   __ \    | |
| | |_/ | | \_|  | || |   | |__) |   | |
| |     | |      | || |   |  __ /    | |
| |    _| |_     | || |  _| |  \ \_  | |
| |   |_____|    | || | |____| |___| | |
| |              | || |              | |
| '--------------' || '--------------' |
'----------------'  '----------------' 

Condsider the following I/O transformation:

===>Sample Input Data<===     |   ===> Sample Input Data <===     | ===> Sample Input Data <===     | ===> Sample Input Data <===
                              |                                   |                                 | 
1 234 5 678 9                 |  I can think of 100's             | A line with lots of numbers:    | Input with absolutely 0 digits in it
                              |  of other things I'd rather       | 123456789123456789123456789     | Well ... apart from that 1 ...
===>Corresponding Output<===  |  be doing than these 5 questions  | A line with all zeroes          | 
                              |                                   | 000000000000000000000000000     | ===> Corresponding Output <=== 
< <<< 5 >>> >                 |  ===> Corresponding Output <===   | A line with blanks at the end   |
                              |                                   | 1 2 3                           | Input with absolutely < digits in it
                              |  I can think of <<<'s             |                                 | Well ... apart from that < ...
                              |  of other things I'd rather       | ===> Corresponding Output <===  |
                              |  be doing than these 5 questions  | A line with lots of numbers:    | ===> Sample Input Data <===	
                                                                  | <<<<5>>>><<<<5>>>><<<<5>>>>     |
                                                                  | A line with all zeroes          | 1 2 4 8 16 32 64 128 256 512 1024
                                                                  | <<<<<<<<<<<<<<<<<<<<<<<<<<<     | 2048 4096 8192 16384 32768 65536
                                                                  | A line with blanks at the end   |
                                                                  | < < <                           | ===> Corresponding Output <===
                                                                                                    |
                                                                                                    | < < < > <> << >< <<> <5> 5<< <<<<
                                                                                                    | <<<> <<>> ><>< <><>< <<>>> >55<>
"""
]
w2_tr_q = [
"Provide a command that would create a copy of /etc/passwd called passwords.txt with tab-separated data instead of colon-separated data:",
"Provide a command that would create a copy of /etc/passwd called passwords.txt with all numeric values removed:",
"Provide a command that would create a copy of /etc/passwd called passwords.txt with all alphabetical values removed:",
"Provide a command that would create a copy of /etc/passwd called passwords.txt with  the complement of all numeric values removed:",
"Provide a command that would create a copy of /etc/passwd called passwords.txt with the complement of all alphabetical values removed:",
"Provide a command that would create a tab-separated file passwords.txt containing only the username and password of each user:",
"""
Write a tr command that reads from standard input and writes to standard output:.
It should:

-  map all digit characters whose values are less than 5 into the character '<'.

-  map all digit characters whose values are greater than 5 into the character '>'.

-  leave the digit character '5', and all non-digit characters, unchanged.""",
  ]
w2_tr_a = [
"tr ':' '\\t' < /etc/passwd > passwords.txt",
"tr -d [:digit:] < /etc/passwd > passwords.txt",
"tr -d [:alpha:] < /etc/passwd > passwords.txt",
"tr -cd [:digit:] < /etc/passwd > passwords.txt",
"tr -cd [:alpha:] < /etc/passwd > passwords.txt",
"cut -d':' -f1,2 /etc/passwd | tr ':' '\\t' > passwords.txt",
"tr '0123456789' '<<<<<5>>>>>'"  
]
w2_tr_f = [
"""
tr - translate or delete characters
':' - Set 1 (set to be translated)
'\\t' - Set 2 (translation set)
< /etc/passwd - redirect input from /etc/passwd to tr

/etc/passwd - a colon-separated file that contains the following information:

1.  User name
2.  Encrypted password
3.  User ID number (UID)
4.  User's group ID number (GID)
5.  Full name of the user (GECOS)
6.  User home directory
7.  Login shell

> passwords.txt - redirect output from tr to passwords.txt""",

"""
tr - translate or delete characters
-d --delete, delete characters in SET1, do not translate
[:digit:] - all digits
< /etc/passwd - redirect input from /etc/passwd to tr

/etc/passwd - a colon-separated file that contains the following information:

1.  User name
2.  Encrypted password
3.  User ID number (UID)
4.  User's group ID number (GID)
5.  Full name of the user (GECOS)
6.  User home directory
7.  Login shell

> passwords.txt - redirect output from tr to passwords.txt""",

"""
tr - translate or delete characters
-d --delete, delete characters in SET1, do not translate
[:alpha:] - all letters
< /etc/passwd - redirect input from /etc/passwd to tr

/etc/passwd - a colon-separated file that contains the following information:

1.  User name
2.  Encrypted password
3.  User ID number (UID)
4.  User's group ID number (GID)
5.  Full name of the user (GECOS)
6.  User home directory
7.  Login shell

> passwords.txt - redirect output from tr to passwords.txt""",

"""
tr - translate or delete characters
-c --complement, use the complement of SET1
-d --delete, delete characters in SET1, do not translate
[:digit:] - all digits
< /etc/passwd - redirect input from /etc/passwd to tr

/etc/passwd - a colon-separated file that contains the following information:

1.  User name
2.  Encrypted password
3.  User ID number (UID)
4.  User's group ID number (GID)
5.  Full name of the user (GECOS)
6.  User home directory
7.  Login shell

> passwords.txt - redirect output from tr to passwords.txt""",

"""
tr - translate or delete characters
-c --complement, use the complement of SET1
-d --delete, delete characters in SET1, do not translate
[:alpha:] - all letters
< /etc/passwd - redirect input from /etc/passwd to tr

/etc/passwd - a colon-separated file that contains the following information:

1.  User name
2.  Encrypted password
3.  User ID number (UID)
4.  User's group ID number (GID)
5.  Full name of the user (GECOS)
6.  User home directory
7.  Login shell

> passwords.txt - redirect output from tr to passwords.txt""",

"""
cut - remove sections from each line of files
-d':' - specify the delimiter as the colon character instead of the tab character (default)
-f1,2 - select only fields 1 and 2
/etc/passwd - a colon-separated file that contains the following information:

1.  User name
2.  Encrypted password
3.  User ID number (UID)
4.  User's group ID number (GID)
5.  Full name of the user (GECOS)
6.  User home directory
7.  Login shell

| - pipe stdout from previous command to stdin of next command

tr - translate or delete characters
':' - 
'\\t' > passwords.txt """,

"""tr - translate or delete characters
'0123456789' - Set 1 (set to be translated)
'<<<<<5>>>>>' - Set 2 (translation set)""",
]

w3_sort_c = [
"""
 .----------------.  .----------------.  .----------------.  .----------------. 
| .--------------. || .--------------. || .--------------. || .--------------. |
| |    _______   | || |     ____     | || |  _______     | || |  _________   | |
| |   /  ___  |  | || |   .'    `.   | || | |_   __ \    | || | |  _   _  |  | |
| |  |  (__ \_|  | || |  /  .--.  \  | || |   | |__) |   | || | |_/ | | \_|  | |
| |   '.___`-.   | || |  | |    | |  | || |   |  __ /    | || |     | |      | |
| |  |`\____) |  | || |  \  `--'  /  | || |  _| |  \ \_  | || |    _| |_     | |
| |  |_______.'  | || |   `.____.'   | || | |____| |___| | || |   |_____|    | |
| |              | || |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------'  '----------------' 

Consider a file benchmarks.txt containing tab-separated benchmarking results for 20 programs, in three different benchmarks, all measured in seconds.

program1	08	03	05
program2	14	03	05
program3	17	08	10
program4	15	11	05
program5	16	10	24
program6	15	09	17
program7	15	06	10
program8	17	10	17
program9	12	07	08
program10	09	04	16
program11	11	03	24
program12	16	11	20
program13	16	08	17
program14	08	07	06
program15	06	06	05
program16	12	05	08
program17	09	05	10
program18	06	06	06
program19	14	09	22
program20	16	04	24"""
]
w3_sort_q = [
"""
Write a sort command which sorts lines in benchmarks.txt into increasing numeric order evaluating field 2 and all fields following it, 
then field three and all fields following it:""",
"""
Write a sort command which sorts lines in benchmarks.txt into increasing numeric order evaluating field 2 then field three. In the event that
two lines are equal the entire line should be compared as a string of bytes to determine their order:""",
"""
Write a sort command which sorts lines in benchmarks.txt into increasing numeric order evaluating field 2 then field three. 
In the event that two lines are equal, only one should be kept:""",
"Write a sort command which sorts by the results in the second benchmark, then by the results in the first benchmark:",
"Write a sort command which sorts by the results in the third benchmark, then by the program number:",
]
w3_sort_a = [
"sort -n -k2 -k3 benchmarks.txt",
"sort -n -k2,3 benchmarks.txt",
"sort -n -u -k2,3 benchmarks.txt",
"sort -k3,3 -k2,2 benchmarks.txt",
"sort -k4,4 -k1.8,1n benchmarks.txt",
]
w3_sort_f = [
"""
sort -n --numeric-sort compare according to string numerical value
-k2 -k3 --key=KEYDEF sort via a key; KEYDEF gives location and type
benchmarks.txt - file to be sorted""",

"""
sort -n --numeric-sort compare according to string numerical value
-k2,3 --key=KEYDEF sort via a key; KEYDEF gives location and type
benchmarks.txt - file to be sorted""",

"""
sort -n --numeric-sort compare according to string numerical value
-u -unique with -c, check for strict ordering; without -c, output only the first of an equal run
-k2,3 --key=KEYDEF sort via a key; KEYDEF gives location and type. Field 2 is primary sort key and field 3 is secondary sort key
benchmarks.txt - file to be sorted""",

"""
sort - sort lines of text files
-k3,3 --key=KEYDEF sort via a key; KEYDEF gives location and type. Field 3 is primary sort key
-k2,2 --key=KEYDEF sort via a key; KEYDEF gives location and type. Field 3 is secondary sort key
benchmarks.txt - file to be sorted""",

"""
sort - sort lines of text files
-k4,4 - --key=KEYDEF sort via a key; KEYDEF gives location and type. Field 4 is primary sort key
-k1.8,1n - indicates field 1 character position 8 through field 1 character position n. Field 1 is secondary sort key
benchmarks.txt - file to be sorted""",
]

w3_sed_c = [
"""
 .----------------.  .----------------.  .----------------. 
| .--------------. || .--------------. || .--------------. |
| |    _______   | || |  _________   | || |  ________    | |
| |   /  ___  |  | || | |_   ___  |  | || | |_   ___ `.  | |
| |  |  (__ \_|  | || |   | |_  \_|  | || |   | |   `. \ | |
| |   '.___`-.   | || |   |  _|  _   | || |   | |    | | | |
| |  |`\____) |  | || |  _| |___/ |  | || |  _| |___.' / | |
| |  |_______.'  | || | |_________|  | || | |________.'  | |
| |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------' 

Consider a file benchmarks.txt containing tab-separated benchmarking results for 20 programs, in three different benchmarks, all measured in seconds.

program1	08	03	05
program2	14	03	05
program3	17	08	10
program4	15	11	05
program5	16	10	24
program6	15	09	17
program7	15	06	10
program8	17	10	17
program9	12	07	08
program10	09	04	16
program11	11	03	24
program12	16	11	20
program13	16	08	17
program14	08	07	06
program15	06	06	05
program16	12	05	08
program17	09	05	10
program18	06	06	06
program19	14	09	22
program20	16	04	24"""
]

w3_sed_q = [
"Write a sed command print the first line of benchmarks.txt.",
"Write a sed command that prints lines 1 to 5 of benchmarks.txt.",
"Write a sed command that prints lines 1 and the four lines following of benchmarks.txt.",
"Write a sed command that prints every other line of benchmarks.txt, starting with line 1.",
"Write a sed command which removes the leading zeroes from the benchmark times.",
"Write a sed command which removes the benchmark results from program2 through program13.",
]

w3_sed_a = [
"sed -n '1p' benchmarks.txt",
"sed -n '1,5p' benchmarks.txt",
"sed -n '1,+4p' benchmarks.txt",
"sed -n '1~2p' benchmarks.txt",
"sed -Ee 's/\\t0/\\t/g' benchmarks.txt",
"sed -Ee '/^program2\\b/,/^program13\\b/d' benchmarks.txt",
]
w3_sed_f = [
"""
sed - stream editor for filtering and transforming text 
-n, --quiet, --silent, suppress automatic printing of pattern space
'1p' - print the current pattern space. Leading 1 indicates line 1 
benchmarks.txt - file to be filtered and transformed""",

"""
sed - stream editor for filtering and transforming text 
-n, --quiet, --silent, suppress automatic printing of pattern space
'1,5p' - print the current pattern space. Leading 1,5 indicates address range of line 1 to line 5
benchmarks.txt - file to be filtered and transformed""",

"""
sed - stream editor for filtering and transforming text 
-n, --quiet, --silent, suppress automatic printing of pattern space
'1,+4p' - print the current pattern space. Leading 1,+4 indicates address range of line 1 and the following 4 lines.
benchmarks.txt - file to be filtered and transformed""",

"""
sed - stream editor for filtering and transforming text 
-n, --quiet, --silent, suppress automatic printing of pattern space
'1~2p' - print the current pattern space. Leading 1~2 indicates line 1 but not 2, printing every alternate starting at 1.
benchmarks.txt - file to be filtered and transformed""",

"""
sed - stream editor for filtering and transforming text 
-E - same as -r or --regexp-extended - use extended regular expressions in the script
-e --expression=script, add the script to the commands to be executed  
's/\\t0/\\t/g' - <ANSWER ME>
benchmarks.txt - file to be filtered and transformed""",

"""
sed - stream editor for filtering and transforming text 
-E - same as -r or --regexp-extended - use extended regular expressions in the script
-e --expression=script, add the script to the commands to be executed  
'/^program2\\b/,/^program13\\b/d' - <ANSWER ME>
benchmarks.txt - file to be filtered and transformed""",
]

w3_shell_c = [
"""
 .----------------.  .----------------.  .----------------.  .----------------.  .----------------. 
| .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |
| |    _______   | || |  ____  ____  | || |  _________   | || |   _____      | || |   _____      | |
| |   /  ___  |  | || | |_   ||   _| | || | |_   ___  |  | || |  |_   _|     | || |  |_   _|     | |
| |  |  (__ \_|  | || |   | |__| |   | || |   | |_  \_|  | || |    | |       | || |    | |       | |
| |   '.___`-.   | || |   |  __  |   | || |   |  _|  _   | || |    | |   _   | || |    | |   _   | |
| |  |`\____) |  | || |  _| |  | |_  | || |  _| |___/ |  | || |   _| |__/ |  | || |   _| |__/ |  | |
| |  |_______.'  | || | |____||____| | || | |_________|  | || |  |________|  | || |  |________|  | |
| |              | || |              | || |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------'  '----------------'  '----------------' 

Assume that we are in a shell where the following shell variable assignments have been performed,
and ls gives the following result:

$ x=2  y='Y Y'  z=ls

$ ls
    a       b       c

What will be displayed as a result of the following echo command: """
]

w3_shell_q = [
"echo a   b   c",
'echo "a   b   c"',
"echo $y",
"echo x$x",
"echo $xx",
"echo ${x}x",
'echo "$y"',
"echo '$y'",
"echo $($y)",
"echo $($z)",
"echo $(echo a b c)",
]

w3_shell_a = [
"a b c",
"a   b   c",
"Y Y",
"x2",
"",
"2x",
"Y Y",
"$y",
"Y: command not found",
"a b c",
"a b c",
]
w3_shell_f = [
"""
===> User Input <===	

echo a   b   c

===> Corresponding Output <===

a b c

===> Explanation <===

Spaces between arguments are not preserved;
echo puts one space between each argument.""",

"""
===> User Input <===	

echo "a   b   c"

===> Corresponding Output <===

a   b   c

===> Explanation <===

Spaces are preserved,
because the quotes turn "a   b   c" into a single argument to echo.""",

"""
===> User Input <===	

echo $y

===> Corresponding Output <===

Y Y

===> Explanation <===

$y expands into two separate arguments.""",

"""
===> User Input <===	

echo x$x

===> Corresponding Output <===

x2

===> Explanation <===

$x expands to 2 and is appended after the letter x.""",

"""
===> User Input <===	

echo $xx

===> Corresponding Output <===

  

===> Explanation <===

$xx is treated as a reference to the shell variable xx:
since there is no such variable, it expands to the empty string.""",

"""
===> User Input <===	

echo ${x}x

===> Corresponding Output <===

2x 

===> Explanation <===

${x} expands to 2 and the letter x is appended.""",

"""
===> User Input <===	

echo "$y"

===> Corresponding Output <===

Y Y

===> Explanation <===

$y expands into a single argument.""",

"""
===> User Input <===	

echo '$y'

===> Corresponding Output <===

$y

===> Explanation <===

Single quotes prevent variable expansion. """,

"""
===> User Input <===	

echo $($y)

===> Corresponding Output <===

Y: command not found

===> Explanation <===

$y expands to Y Y
which is then executed as a command because of the $();
since there is no command Y, an error message follows.""",

"""
===> User Input <===	

echo $($z)

===> Corresponding Output <===

a b c

===> Explanation <===

$z expands to ls,
which is then executed as a command,
giving the names of the files in the current directory,
which are treated as three separate arguments.""",

"""
===> User Input <===	

echo $(echo a b c)

===> Corresponding Output <===

a b c

===> Explanation <===

The inner echo command is executed,
giving a b c,
which are passed as arguments to the outer echo.""",
]

w3_args_c = [
"""
The following C program aims to give precise information about their command-line arguments:

  #include <stdio.h>

  int main(int argc, char *argv[]) {
    printf("#args = %d\\n", argc - 1);

    for (int i = 1; i < argc; i++) {
      printf("arg[%d] = \"%s\"\\n", i, argv[i]);
    }

    return 0;
  }

Assume that these programs are compiled in such a way that we may invoke them as ./args.
Consider the following examples of how it operates: 

./args a b c

#args = 3
arg[1] = "a"
arg[2] = "b"
arg[3] = "c"
args "Hello there"
#args = 1
arg[1] = "Hello there"

Assume that we are in a shell where the following shell variable assignments have been performed,
and ls gives the following result:

$ x=2  y='Y Y'  z=ls

$ ls
    a       b       c
    
What will be the output of the following command: """
]

w3_args_q = [
"./args x y   z",
"./args $(ls)",
"./args $y",
'./args "$y"',
'./args $(echo "$y")',
"./args $x$x$x",
"./args $x$y",
"./args $xy",
]

w3_args_a = [
"3 x y z",
"3 a b c",
"2 Y Y",
"1 Y Y",
"2 Y Y",
"1 222",
"2 2Y Y",
"0"
]
w3_args_f = [
"""
#args = 3
arg[1] = "x"
arg[2] = "y"
arg[3] = "z"

Each of the letters is a single argument (separated by spaces).""",

"""
#args = 3
arg[1] = "a"
arg[2] = "b"
arg[3] = "c"

The ls command is executed and its output is interpolated into the command line;
the shell then splits the command-line into arguments.""",

"""
#args = 2
arg[1] = "Y"
arg[2] = "Y"

$y expands to the string Y Y;
when the shell splits the line into words,
these two characters becomes separate arguments.""",

"""
#args = 1
arg[1] = "Y Y"

$y expands to Y Y within the quotes,
so it is treated as a single word when the shell breaks the line into arguments.""",

"""
#args = 2
arg[1] = "Y"
arg[2] = "Y"


The command within the backquotes expands to Y Y,
but since backquotes don't have a grouping function,
the two Y's are treated as separate arguments.""",

"""
#args = 1
arg[1] = "222"

$x expands into 2,
which is concatenated with itself three times.""",

"""
#args = 2
arg[1] = "2Y"
arg[2] = "Y"

$x expands to 2 and
$y expands to Y Y;
these two strings are concatenated to give 2Y Y and,
when the shell splits the line into words,
the second Y becomes an argument in its own right.""",

"""
#args = 0

There is no variable called xy,
so $xy expands to the empty string,
which vanishes when the shell splits the command line into words.""",
]

regexp = [Question(w1_regexp_c[0], w1_regexp_q[i], w1_regexp_a[i], w1_regexp_f[i]) for i in range(len(w1_regexp_q))]
head = [Question(w2_head_c[0], w2_head_q[i], w2_head_a[i], w2_head_f[i]) for i in range(len(w2_head_q))]
grep = [Question(w2_grep_c[0], w2_grep_q[i], w2_grep_a[i], w2_grep_f[i]) for i in range(len(w2_grep_q))]
cut = [Question(w2_cut_c[0], w2_cut_q[i], w2_cut_a[i], w2_cut_f[i]) for i in range(len(w2_cut_q))]
tr = [Question(w2_tr_c[0], w2_tr_q[i], w2_tr_a[i], w2_tr_f[i]) for i in range(len(w2_tr_q)-1)] + [Question(w2_tr_c[1], w2_tr_q[6], w2_tr_a[6], w2_tr_f[6])]
sort = [Question(w3_sort_c[0], w3_sort_q[i], w3_sort_a[i], w3_sort_f[i]) for i in range(len(w3_sort_q))]
shell = [Question(w3_shell_c[0], w3_shell_q[i], w3_shell_a[i], w3_shell_f[i]) for i in range(len(w3_shell_q))]
args = [Question(w3_args_c[0], w3_args_q[i], w3_args_a[i], w3_args_f[i]) for i in range(len(w3_args_q))]

def sleep(seconds):
    for i in range(seconds):
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break

def run_quiz(questions):
  score = 0
  os.system('cls||clear')
  for question in questions:
    print(colored(question.consider + "\n", 'white'))
    print(colored(question.prompt + "\n", 'white'))
    answer = input("$ ")
    if answer == question.answer:
      score += 1
      print(colored("\nThe correct answer is:\n", 'white'))
      print(colored(question.answer + "\n", 'green'))
    else:
      print(colored("\nThe correct answer is:\n", 'white'))
      print(colored(question.answer + "\n", 'red'))
    sleep(1)
    print(colored("----- Feedback -----", 'blue'))
    print(colored(question.feedback, 'blue'))
    sleep(30)
    os.system('cls||clear')
  print("you got", score, "out of", len(questions))
  sleep(3)

run_quiz(regexp)
run_quiz(head)
run_quiz(grep)
run_quiz(cut)
run_quiz(tr)
run_quiz(sort)
run_quiz(shell)
run_quiz(args)