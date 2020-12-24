#!/bin/bash

find . -iname "*$1*" -type d |grep -c "./"$1|while read count;
do
if [ $count -gt 0 ]
then
    echo "$(find . -iname "*$1*" -type d | xargs du -h )"
    break
fi
done
