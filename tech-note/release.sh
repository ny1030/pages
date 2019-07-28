#!/bin/bash

make clean html
cp -rp ./build/html/* ../docs/
git add -A
git commit -m "[fix]"
git push origin master
