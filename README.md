# wolframBeta
Alan Chen, Julius Freyra, Stephanie Yoon, Angela Yu pd. 8
Final project

Our idea is to make a linear algebra calculator that will give the user solutions to otherwise time-consuming and tedious calculations. What makes it particularly intuitive to use is that the calculator will take input in three easy ways: LaTeX source code, uploaded pictures, and canvas drawings. Moreover, the calculator provides the LaTeX source code for each.

### Packages:
* Flask
* request
* Iterable
* requests

If you don't have any of these modules already, install them using pip install.

### Deployment

Your web server needs to give write permissions to the images folder to www-data.
For instance: 
$ chown www-data images
or
$ chgrp www-data images
