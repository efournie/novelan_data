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

If the script is run on a Raspberry Pi with RaspberryOS, geckodriver must be installed:
    wget https://github.com/mozilla/geckodriver/releases/download/v0.23.0/geckodriver-v0.23.0-arm7hf.tar.gz
    tar xvzf geckodriver-v0.23.0-arm7hf.tar.gz && rm -f geckodriver-v0.23.0-arm7hf.tar.gz
    sudo mv geckodriver /usr/local/bin/

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
