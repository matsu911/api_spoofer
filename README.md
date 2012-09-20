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
### Generate stub code
    $ api_spoofer /bin/date > date_spoofer.c

### Compile to create shared object
    $ gcc -shared -fPIC -ldl -o date_spoofer.so date_spoofer.c

### Run with spoofer shared object
    $ LD_PRELOAD=date_spoofer.so date

### Show help
    $ test_env/bin/api_spoofer -h
    Usage: api_spoofer [options] bin_path

    Options:
      --version   show program's version number and exit
      -h, --help  show this help message and exit
      -I DIR      include directories

## License
Copyright &copy; 2012 Shigeaki Matsumura.  
Distributed under the GNU General Public License; see C-h t to view.  
