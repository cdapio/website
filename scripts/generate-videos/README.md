# Generate Videos

Generates a list of videos from in CDAP youtube channel

# Requirements
Python 2.7+

# Usage

Install dependencies:

```sh
pip install --user -r requirements.txt
```

Run script:

```
$ python main.py -o /path/to/output.json
```

All arguments:

```
$ python main.py -h
usage: main.py [-h] -o OUTPUT -k API_KEY [-v VISIBLE] [-u UPDATE]
               [--update-attributes UPDATE_ATTRIBUTES]

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Absolute path to output file.
  -k API_KEY, --api-key API_KEY
                        Youtube API key.
  -v VISIBLE, --visible VISIBLE
                        Append new videos as visible
  -u UPDATE, --update UPDATE
                        Update existing videos
  --update-attributes UPDATE_ATTRIBUTES, --update-attributes UPDATE_ATTRIBUTES
                        Comma separated list of attributes allowed to update
```