[![Codacy Badge](https://app.codacy.com/project/badge/Grade/58819cf177b24671b65b8c6ac2083fe5)](https://www.codacy.com/manual/ale-ben/AnimeUnityUI?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ale-ben/AnimeUnityUI&amp;utm_campaign=Badge_Grade)
[![CodeFactor](https://www.codefactor.io/repository/github/ale-ben/animeunityui/badge)](https://www.codefactor.io/repository/github/ale-ben/animeunityui)

# AnimeUnityUI
## Installation
### Install virtualenv
1)	Make sure to have python3 installed by trying `python3 --version`
2)	Install python virtualenv package `pip3 install -U virtualenv` 

### Create virtualenv
1) Create virtualenv `python3 -m virtualenv venv`. This will create a venv folder with (almost) no package installed.
2) Enable virtualenv (see next paragraph)
3) Upgrade pip `pip install -U pip`
4) Install requirements `pip install -r requirements.txt`

## Work with virtualenv
#### Enable
You can enable the repo virtualenv with `source venv/bin/activate`, you'll notice a (venv) has appeared in your terminal.
By doing this you load all the requirements to run the python code.

#### Disable
To disable the virtualenv simply type `disable` in the terminal

## Run
### Interactive 
`python main.py`

### CLI
`python main.py -h` TODO: Flag documentation
