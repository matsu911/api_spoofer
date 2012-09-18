# API Spoofer

API spoofing tool for *nix OS.

## Requirements
* *nix OS
* Python 2.7.x
* CPP
* GCC

## Installation
`$ python setup.py install`

## Run Test Suite
`$ python setup.py test`

## Usage
    $ api_spoofer /bin/date > date_spoofer.c
    $ gcc -shared -fPIC -ldl -o date_spoofer.so date_spoofer.c
    $ LD_PRELOAD=date_spoofer.so date

## License
Copyright &copy; 2012 Shigeaki Matsumura.  
Distributed under the GNU General Public License; see C-h t to view.  
