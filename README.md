# GCode Web

This is a web app wrapping the [Conversational GCode](github.com/janion/ConversationalGCode) library. the aim is to allow users to create GCode jobs for simple operations without the need for 3D modelling. It is written in *Python* using the *Shiny* framework.

To launch in PyCharm, in the terminal, run the command `shiny run src/launcher.py`.

## To Do List:
- [X] Allow for custom naming of jobs (and files)
- [ ] Allow removal of operations
- [ ] Allow removal of jobs
- [X] Hook-up download buttons for generated files
- [X] Add "Download All" button for generated files
- [ ] Add save and load functionality for configurations
- [ ] Add the other operations
- [ ] Add tool options to validation in app

## Known Issues:
- Clashing names sometimes revert:
  - Create new job
  - Rename to "jobb"
  - Create second new job
  - Rename second job to "jobb"
  - Rename first job to "jobby"
  - Create third new job
  - See that second job has been renamed back to "job"
