# Chupamon Showdown by ChewyChupucabras
---
## Roster:
Ethan Sie:
- Database lead
- Basic site setup
  - Creating base tailwind for overall site design
  - SQLite db setup
  - Ensures all program file templates are accessible and ready for use
- Create the matching system through a dictionary of tracked active sessions
- Ensure turn-based system is working through database-tracked turns/games
- Will help to catch up with any other work

Tanzeem Hasan: 
- Javascript lead for more intricate animations and website capabilities 
  - Dynamic response design in the game page
  - Working with Ethan to create the mechanics behind the actual game component
- Ensure cleanliness of database code (as we are spending a lot of time populating the db)
- Determine settings that can be toggled in account settings
  - Possibly creating light/dark modes or more user customization to the site design

Brian Liu:
- Tailwind (css) lead for more intricate designs
  - The game page
  - Ladder (ranking) page
  - Handling dialogue output throughout the matches
- Handling damage calculations
- Creating a system for point calculations (elo) based on wins/loss, pokemon alive, etc
- Designing and adding responsiveness to match history page

## Project Description:

## Install Guide:
### Prerequisites:
Must have Git and Python installed beforehand.
1. Git: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
2. Python: https://www.python.org/downloads/
3. Using Git: https://novillo-cs.github.io/apcsa/tools/

### Procedure:
1. Locate green <>Code button on main page of project repository
2. Copy the HTTPS URL
3. Open the terminal on your local machine and navigate to the desired directory
4. Clone the repository in the corresponding directory:
```
git clone https://github.com/ethannsie/ChewyChupucabras__ethans175_tanzeemh2_brianl237.git
```
5. Setup a virtual environment
```
python3 -m venv <name>
```
6. Activate virtual environment
```
. <name>/bin/activate
```
7. cd into the repo, ```
cd PATH/TO/ChewyChupucabras__ethans175_tanzeemh2_brianl237```

8. Install required packages
```
pip install -r requirements.txt
```
## Launch Codes:
1. Navigate to app folder of project directory
```cd PATH/TO/ChewyChupucabras__ethans175_tanzeemh2_brianl237/app```
2. Run app
```python3 __init__.py```
3. Open firefox and go to the given link
```http://127.0.0.1:5000```
