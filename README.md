
# 3D Parametric Human Model App

Created with PyQt5 and PyVista, the application will serve as a convenient viewer of parametric human body models. The core functionalities include:
* Load human body models which are stored in .k files
* Adjust the model by changing parameters including gender, stature, BMI, age and SHS (i.e. seated height/stature)
* Do comparisons between human models with different parameters
* Export the model into .k file according to the parameters of that model 

The application has not been packaged into an executable yet because it's still in the stage of development and more functionalities may be added in the future.

This project is developed under supervision of [Dr. Jingwen Hu](https://sites.google.com/umich.edu/jingwenhu/home?authuser=0).

## Setup
Currently, the application is only compatible with the human models created by UMTRI researchers. You will need two additional files in order to run the application: one is the baseline human body model and the other is the statistical model. Once you have these files, put them in the same folder with other files in this repo. Then, please follow the setup instructions corresponding to your device's system and run the following command after you finish the setup:
```
$ python3 App.py
```
### MacOS
First make sure that you have installed Homebrew and you also have python installed through Homebrew. Install gcc in case you haven't done so:
```
# Compiling qd requires GCC. Apple uses LLVM/clang by default
$ brew install gcc

```
Depending on the version of gcc installed, run the following commands:
```
$ export CC=gcc-[version]  # e.g. gcc-12
$ export CXX=g++-[version]
$ export LD=g++-[version]
```
Finally, create a virtual environment and install all required packages except qd:
```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```
### Windows
For Windows users, it is recommended to use Ubuntu running on WSL (Windows Subsystem for Linux). If you have that installed, please follow the setup instruction for Linux.
### Linux (Ubuntu)
First please ensure that python3 and gcc are installed. Then run:
```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```
### Installation of qd
The application uses a package called qd to process .k file. Try ```$ pip install qd``` first. If it fails, then it means that you have to compile the package manually. Run commands below:
```
$ which python  # make sure virtual environment is activated
$ cd ..
$ git clone https://github.com/qd-cae/qd-cae-python.git
$ cd qd-cae-python
$ python setup.py install 
```

## Demo

Coming soon...

