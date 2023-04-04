# How to download course materials

Those familiar with `git` and `github` should download and
administrate the course materials with `git`-commands. We will
introduce `git` and the concepts of *version control* at the end of
the term.

A way to obtain the materials easily without `git`-knowledge is:

1. Download the script [get_current_course_materials.sh](https://raw.githubusercontent.com/ocordes/Scientific_programming_with_Python_Summer_2023/master/retrieve_materials/get_current_course_materials.sh).

2. Create a directory, where you want to store course materials. This
only needs to be done once for the whole course.

3. Go to that directory and execute:

   ```
   user$ bash get_current_course_materials.sh
   Cloning into 'Scientific_programming_with_Python_Summer_2023'...
   .
   .
   .
   Please go to python_course_2023-04-04 and run 'jupyter notebook' or
   'jupyter lab'  there.

   user$ ls
   python_course_2023-04-04 ... # 2023-04-04 needs to be subtituted
                                # by the current date
   ```
4. if you are not in the jupyterhub-online-system, you can start
   the materials with:
   ```
   user$ cd python_course_2023-04-04
   user$ jupyter notebook       # to start working on the notebooks
   ```
   or 
   ```
   user$ cd python_course_2023-04-04
   user$ jupyter notebook       # to start working on the notebooks
   ```
   if you are in the jupyterhub-online-system, go to the file browser
   and open the notebooks inside ``python_course_2023-04-04``` 
5. Repeat step 3 whenever a new version of materials is available.


