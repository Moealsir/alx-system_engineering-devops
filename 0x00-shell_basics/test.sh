#!/bin/bash
echo '0       string  SCHOOL  School data
!:mime School' > school

file -C -m school

git add .

git commit -m 'script'

git push
