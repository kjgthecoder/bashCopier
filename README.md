# bashCopier

## Introduction

This software initiative was born from my experiences in Professor Corkan's Linux/Unix course at the University of Central Arkansas. Throughout the semester, we frequently engaged in assignments that involved copying sample scripts from PDF documents into our terminal environment. These tasks served to deepen our understanding of the concepts elucidated during our lectures.

However, one significant challenge was that pasting from a PDF into vim often led to the loss of original formatting. In addition, the process retained all line numbers, which proved to be a nuisance. Recognizing this issue, I sought to develop a program that would bridge this gap, streamlining and automating the process.

Developing 'bashCopier' provided me with valuable experience in using the tkinter framework. This allowed me to learn and understand the nuances of event handling and GUI creation in Python. The final product is a user-friendly tool that formats copied scripts correctly, irrespective of their source.

The envisioned program functions as an intermediary - users can copy content from a PDF into the application, which then presents the correctly formatted code. This code is then automatically copied to the clipboard, ready to be pasted directly into vim.

## Enhancements

During the development process, I identified areas for enhancement within the formatting function. To make the tool more user-friendly, I decided to incorporate interactive elements. This led to the addition of buttons that can adjust the indentation of each line. Any modifications made are instantly reflected in the clipboard contents, ensuring that users always have access to the most recent version of their code.

## Drawbacks

If it is a long script (longer than 20 lines) the GUI's length may exceed the length of a horizontal monitor. (Want to fix in the future)

## Dependencies

The following libraries are needed if not already installed: 

- tkinter
- pyperclip
- re

## Sample Scripts

Below are some example scripts to try:

**Example 1** - Copying Code from VIM (white space precedes each number line)
```bash
  1 #!/bin/bash
  2
  3 # Check number of arguments
  4 if [ $# -ne 1 ]; then
  5     echo "Usage: ./count_files.sh directory"
  6     exit 1
  7 fi
  8
  9 # Check if argument is directory
 10 if [ ! -d "$1" ]; then
 11     echo "Error: First parameter must be a directory (dir)."
 12     exit 1
 13 fi
 ```

**Example 2** - Copying code from a PDF
```bash
1 #!/bin/bash
2 read -p "word1:" word1
3 read -p "word2:" word2
4 if test "$word1" = "$word2"
5 then
6 echo "Match"
7 fi
```

**Example 3** - Leading white space only
```bash
    #!/bin/bash
    read -p "word1:" word1
    read -p "word2:" word2
    if test "$word1" = "$word2"
    then
    echo "Match"
    fi
```


