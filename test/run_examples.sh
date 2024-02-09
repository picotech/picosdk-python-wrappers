#! /bin/bash

cd "${BASH_SOURCE%/*}" || exit

FILE_ERRORS=""
NEWLINE=$'\n'

for file in ../ps*Examples/*
do
    if [[ -f $file ]]; then
        echo $file
        PYTHONPATH=`pwd`/.. python $file
        if [ $? -ne 0 ]; then
            FILE_ERRORS="$FILE_ERRORS$file$NEWLINE"
        fi
    fi
done

echo $FILE_ERRORS

if [ -z "$FILE_ERRORS" ]; then
    exit 0
fi
exit 1
