# README #

This folder contains a test runner for the ACE Card Testing Framework.
It is designed to be run on a BeagleBone Black.

### General Usage Instructions ###

Production staff should not need to directly interact with this software.
It is designed to run automatically upon starting up the BeagleBone.

To check if this is automatically running when powering up the BeagleBone,
you can simply click the `ace-test-framework/RunTests.bat` file on a computer
and start the tests. If there is an error stating that you are unable to
connect to the host address, try restarting the BeagleBone and then running 
`ace-test-framework/RunTests.bat` again. If the tests run, then this software
is already running!

If that does not work, follow the Initial Setup Instructions below to set up
the BeagleBone.

### Initial Setup Instructions ###

When initially setting up a new BeagleBone to run tests (i.e. on a BeagleBone
which has just had its memory flashed), you must do the following:

On your computer:
1. Open the Command Prompt
2. cd to the directory containing the `ace-bbb-test-runner` folder 
3. Run `scp -r ace-bbb-test-runner debian@beaglebone:/home/debian`
   - enter the BeagleBone password
4. Run `ssh debian@beaglebone`
   - enter the BeagleBone password
5. Run `cd ace-bbb-test-runner`
6. Run `sudo cp rc.local /etc/rc.local`
   - enter the BeagleBone password
7. Run `sudo chmod +x /etc/rc.local`
   - enter the BeagleBone password
   - This will automatically start the server when the BeagleBone starts up
     in the future
8. Run `cat /etc/network/interfaces`
9. One of the entries in the output of the above command will be of the form
   `ethernet_0123456789ab_cable`. Run
   `sudo connmanctl config ethernet_0123456789ab_cable --ipv4 manual 10.16.132.250 255.255.255.0 10.16.132.1 --nameservers 8.8.8.8`
   with `0123456789ab` replaced by the appropriate numbers and letters
   - This will ensure the server has the correct IP address
10. Restart the BeagleBone with the power button

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
each version, try running `python --version` and `python3 --version`
