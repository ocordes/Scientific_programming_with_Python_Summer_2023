#!/bin/bash

# script to retrieve current materials for 
# 'Scientific programming with  Python Summer 2023'.
# The script creates a subdirectory with the current date and puts
# course materials within.

# NOTE:
# If you are familiar with git, you should use git-commands to obtain and
# administrate the materials.

# git-repo for the course:
GIT_REPO=https://github.com/ocordes/Scientific_programming_with_Python_Summer_2023.git

DIR=python_course_$(date +'%F')

if [ ! -d ${DIR} ]; then
  mkdir -p ${DIR}
  cd ${DIR}
  git clone ${GIT_REPO}
  #
  echo ""
  echo "Please go to ${DIR} and run 'jupyter notebook' or"
  echo " 'jupyter lab'  there."
else
  echo "You probably already retrieved the materials from GitHub!"
  echo "If you want to retrieve them again, then explicitely"
  echo "delete the directory ${DIR} before calling this script!"
  exit 1;
fi

exit 0;
