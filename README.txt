Author: Brandon
Date: 5 March 2021

################################ PLEASE READ #################################
This file serves to formalise the workflow for backend, but frontend should read
too, to understand what backend is doing. 

If any endpoint is not functioning as it should, ping in the main telegram chat.
################################ PLEASE READ #################################

NUMBER 1 RULE OF CODING: ALWAYS PULL ORIGIN BEFORE YOU START TO CODE
NUMBER 1 RULE OF CODING: ALWAYS PULL ORIGIN BEFORE YOU START TO CODE
NUMBER 1 RULE OF CODING: ALWAYS PULL ORIGIN BEFORE YOU START TO CODE
NUMBER 1 RULE OF CODING: ALWAYS PULL ORIGIN BEFORE YOU START TO CODE
NUMBER 1 RULE OF CODING: ALWAYS PULL ORIGIN BEFORE YOU START TO CODE
Ok now onto the real stuff

Set up
1. Install tabnine
    - It will help you to do autocomplete really well, especially when you are writing the class for the SQL_ALCHEMY db object
2. Create virtual environment and run requirements.txt
    - open terminal inside VSC, ensure that you are in the correct working folder (root of esd-mentino)
    - run "python3 -m venv esd_mentino_env" 
    - run "source esd_mentino_env/bin/activate" , this will activate the virtual env 
    - cd into backend and run "pip install -r requirements.txt"
    - You have now set up the venv with all the correct packages in place
    ################################################################
    If you pip install a NEW PACKAGE!!!!!
    Remember to override the old requirements.txt
    - cd backend
    - "pip freeze > requirements.txt"
    - check that the requirements.txt has been overridden

Dev for backend
For development stage, may I propose the following workflow
1. Activate WAMP/MAMP database
2. Run init.sql inside
3. Create a new branch for your microservice that you are going to deploy
4. Copy boilerplate.py and start coding your flask application
5. Read through the comments inside the boilerplate.py
6. Rename boilerplate.py
7. Code away
8. Do localtesting to see if the result match the ones in this document - https://docs.google.com/document/d/1d8As63xcdk4aqrj6KGk09ldf6mHhyf9gIPqCwaMLLaM/edit
9. If all good, create request to merge branch into main
10. Message someone to do peer review 
11. If all good, peer reviewer please merge into main branch

Preparation of backend production ready docker-compose
- To be confirmed