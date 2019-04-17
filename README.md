# Project PAIRS (Paper Artifical Intelligence Rock Sissors)

## CPSC 481 AI Project

### Team Members
* Stacey Frasier
* Brandon Hawkinson
* Jonathan Mouchou
* Michael Perna

### Setup Process

#### 0) Requirements:

To proceed with the following steps, we need to have both Python3 and pip3 installed. The following commands for Unix/Linux platforms and assume Python3 is already installed. Let's install pip3.

`sudo apt-get install python3-pip`

#### 1) Virtual Environment Setup:

Python has a virtual environment manager that we use to keep our dependencies the same.

If you're using Tuffix (https://github.com/kevinwortman/tuffix) or on a Unix/Linux platform and do not have VirtualEnv:

`sudo apt-get install python3-venv`

#### 2) Creating the Virtual Environment:

Navigate into the src directory:

`cd src`

Let's create the Virtual Environment:

`python3 -m venv venv`

#### 3) Activating the enviornment:

`. venv/bin/activate`

#### 4) Install the required dependencies with:

`pip3 install -r requirements.txt`