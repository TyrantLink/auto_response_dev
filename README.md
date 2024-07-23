Repository hosting all scripted auto responses for [/reg/nal](https://github.com/tyrantlink/regnal)

## About
All scripted auto responses are stored in this repository. This repository is used to test the auto responses against a set of messages.
This repo compiles all auto responses with mypyc to increase speed and ensure type safety.

## Adding scripted auto responses to your server
1. invite [/reg/nal](https://discord.com/oauth2/authorize?client_id=839398546217893898&permissions=309506436225&scope=bot%20applications.commands) to your server
2. run /config
3. navigate to guild > auto_responses
4. click on the `scripted auto responses` button
5. click on `import by name` and type the name of file in [auto_responses](auto_responses) you want to import (without the .py extension)
6. that's it! the auto response should now be active in your server

## Requirements
- Python 3.11.x
- [mypyc](https://mypyc.readthedocs.io/en/latest/getting_started.html)

## Creating scripted auto responses
1. install the requirements listed above
2. fork this repository and clone it to your local machine
3. create a virtual environment with `python -m venv .venv` or `uv venv` if you are using uv (recommended)
4. enter the virtual environment with `source .venv/bin/activate`
5. install python requirements with `pip install -r requirements.txt` or `uv pip install -r requirements.txt` if you are using uv (recommended)
6. copy examples from the `example_files` directory into the root directory
7. create a new file in the `auto_responses` directory with a function named and change the `response` attribute of the auto response in the `auto_response.py` you created to the file name
8. configure the auto response in the `auto_response.py` file as needed
9. configure the test messages in `messages.py` as needed
10. test by running `python main.py`
11. if the test passes, compile the auto response with `mypyc ./auto_responses`
12. commit the changes to the repository and submit a pull request to the main repository

## Quick Notes
- i am pretty restrictive on what I accept as auto responses. But I'll allow almost anything as long as it's not harmful.
- if you are unsure about something, feel free to ask me in the [/reg/nal development server](https://discord.gg/4mteVXBDW7)
- auto responses that take longer than 5 seconds will not respond.
- by submitting a pull request, you agree that your code will be licensed under the [AGPL-3.0 license](LICENSE)
- if you want/need a third party library, first, make sure it's supported by mypyc, then ask me in the development server and i *might* add it
