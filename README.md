# Novelan data
This is a python script reading the status of a Novelan heat pump using selenium. I use it to get the main information from my LA 16.1HV, not sure if it would work with other models.

The control unit of the heat pump needs to be on the same local network as the computer running the script, its address is passed using the '--ip_address' option.

With the default heat pump control unit settings, the password is left blank so we only need to send return on the login screen.

The status page is as far as I know only available in german but the script parses the contents and return values descriptions in english when called with the '--debug' flag.

The heat pump temperatures will be written in CSV files in the location set by the '--output_dir' argument. Current values will also be stored in *.temp files.

The current values can be used as input for OpenHab items. Example item files are provided, the URL pointing to the temperature files should be modified to match the target system. 

## Requirements
The script uses Selenium

On a Debian-like system, the dependencies can be installed with:

    sudo apt install python3-selenium

If the script is run on a Raspberry Pi with RaspberryOS, chromedriver must be installed:

    sudo apt install chromium-chromedriver

## Usage
    usage: novelan.py [-h] [-i IP_ADDRESS] [-o OUTPUT_DIR] [-d]

    Read status of a Novelan heat pump

    options:
    -h, --help            show this help message and exit
    -i IP_ADDRESS, --ip_address IP_ADDRESS
                            IP address of the heat pump
    -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                            Output directory where CSV files will be written
    -d, --debug           Debug mode, print results

The energy.py script can read the total kWh usage of the heat pump and store it in a text file containing datetime and kWh values:

    $ python3 energy.py --help
    usage: energy.py [-h] [-i IP_ADDRESS] [-f HISTORY_FILE] [-u] [-d DAILY_USE]

    Read energy usage of a Novelan heat pump

    optional arguments:
    -h, --help            show this help message and exit
    -i IP_ADDRESS, --ip_address IP_ADDRESS
                            IP address of the heat pump
    -f HISTORY_FILE, --history_file HISTORY_FILE
                            Text file where the energy usage will be stored
    -u, --update          Update the file containing the heat pump energy usage
    -d DAILY_USE, --daily_use DAILY_USE
                            Compute the heat pump energy usage for the last 24h
                            and store it into the file given as argument

    $ python3 energy.py -i 192.168.1.44 -f test --update
    $ nano test    # manually modify values
    $ python3 energy.py -i 192.168.1.44 -f test --update
    $ cat test 
    2022-12-20 11:09:32 = 14600.3
    2022-12-20 11:20:24 = 14600.7
    2022-12-21 11:21:23 = 14601.8
    $ python3 energy.py -i 192.168.1.44 -f test --daily_use daily
    $ cat daily && echo
    1.1999999999989086
    $ cat test 
    2022-12-20 11:09:32 = 14600.3
    2022-12-20 11:20:24 = 14600.7
    2022-12-21 11:21:23 = 14601.8
    2022-12-21 11:21:38 = 14601.9
