# IT7405 Project: Movie Review Website

## Requirements

- Python 3
- Git
- MongoDB Server

## Instructions

Create a new Python virtual environment:

    $ python -m venv venv

Then activate it:

| Platform | Shell      | Command to activate virtual environment |
|----------|------------|-----------------------------------------|
| POSIX    | bash/zsh   | `$ source <venv>/bin/activate`          |
|          | fish       | `$ source <venv>/bin/activate.fish`     |
|          | csh/tcsh   | `$ source <venv>/bin/activate.csh`      |
|          | PowerShell | `$ <venv>/bin/Activate.ps1`             |
| Windows  | cmd.exe    | `C:\> <venv>\Scripts\activate.bat`      |
|          | PowerShell | `PS C:\> <venv>\Scripts\Activate.ps1`   |

Then:

    $ pip -r requirements.txt    # install requirements
    $ python manage.py migrate   # set up database
    $ python manage.py runserver # run the server
