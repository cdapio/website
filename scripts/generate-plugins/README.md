# Plugin Repository

Generates a list of plugins in CDAP, including built-in plugins and plugins from Hub

# Requirements
Python 3.7

pip:

```
sudo apt install python3-pip
```

[Markdown](https://python-markdown.github.io/)
```
/usr/local/opt/python3/bin/python3 -m pip install --upgrade markdown
```

[Pypandoc](https://pypi.org/project/pypandoc/)
```
/usr/local/opt/python3/bin/python3 -m pip install --upgrade pypandoc
```

[Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
```
/usr/local/opt/python3/bin/python3 -m pip install --upgrade beautifulsoup4
```

[pytablewriter](https://github.com/thombashi/pytablewriter)
```
/usr/local/opt/python3/bin/python3 -m pip install --upgrade pytablewriter
```

[Pandas](https://pandas.pydata.org/)
```
/usr/local/opt/python3/bin/python3 -m pip install --upgrade pandas
```

# Usage
```
$ /usr/local/opt/python3/bin/python3  main.py -h
usage: main.py [-h] [-v CDAP_VERSION] [-o OUTPUT_PATH]
               cdap_sandbox_dir hub_dir

positional arguments:
  cdap_sandbox_dir      Absolute path to the directory containing the CDAP
                        Sandbox
  hub_dir               Absolute path to the directory containing the Hub
                        source

optional arguments:
  -h, --help            show this help message and exit
  -v CDAP_VERSION, --cdap_version CDAP_VERSION
                        CDAP version to build plugin list for
  -o OUTPUT_PATH, --output_path OUTPUT_PATH
                        Absolute path to output file. Output file must not
                        exist. Containing directory must exist.
```

