# GCode Web

This is a web app wrapping the [Conversational GCode](https://github.com/janion/ConversationalGCode) library. the aim is to allow users to create GCode jobs for simple operations without the need for 3D modelling. It is written in *Python* using the *Shiny* framework.

To launch in PyCharm, in the terminal, run the command `shiny run src/launcher.py`.

## To Do List:
- [X] Allow for custom naming of jobs (and files)
- [X] Allow removal of operations
- [X] Allow removal of jobs
- [X] Hook-up download buttons for generated files
- [X] Add "Download All" button for generated files
- [ ] Add all operations
  - [X] Circular pocket
  - [X] Rectangular pocket
  - [X] Circular profile
  - [X] Rectangular profile
  - [X] Drill
- [ ] Add validation for XY coordinates
- [ ] Add tooltips to all operation fields
- [ ] Add drill type to drill operation, then hide options accordingly
- [ ] Add save and load functionality for configurations
- [ ] Add ability to reorder operations
- [ ] Add tool options to validation in app

## Stretch Goals
- Generalise operations UI & server generation
- Add gcode visualisation
