# README #

This folder contains a test runner for the ACE Card Testing Framework.
It is designed to be run on a BeagleBone Black through ssh.

### General Use Instructions ###

1. Use ssh to connect to the BeagleBone Black
   - Open the Command Prompt
   - type `ssh debian@beaglebone`
   - enter the BeagleBone password
2. Type `./run_server.sh`
   - This will start the server
   - You can press Ctrl+C at anytime to stop the server

### Troubleshooting ###

Error message: bad magic number in...
Run `git clean -xfd` in the `ace-bbb-test-runner` directory

### Development Instructions ###

1. Download and install PyCharm Community edition.
2. Open the `ace-bbb-test-runner` folder in PyCharm
3. Mark the following folders as "Sources Root" in PyCharm by right clicking on
   the folder in the Project window, then going to
   "Mark Directory As" > "Sources Root":
   - `ace-bbb-test-runner`
   - `Submodules`
4. Run `git submodule init`, then `git submodule update` in the
   `ace-bbb-test-runner` folder
5. To run the project in debug mode, go to
   `bbb_test_runner/TestRunnerManager.py`
   then right click on the "Play" button to the left of
   `if __name__ = "__main__"`
   and then click "Debug 'TestRunnerManager'"

### Development Notes/Troubleshooting ###

The BeagleBone may ship with both python 2 and python 3. To check the alias for
each version, try running need to run `python --version` and `python3 --version`
