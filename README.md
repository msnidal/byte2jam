# byte2jam

byte2jam is a new, human-friendly way of encoding data based around unique,
memorable musical sequences. In the same sense that a QR code encodes a byte
string into a machine-readable image format, byte2jam encodes a byte string
into a so-called "byte jam" - a unique, musically consistent and ear-pleasing
sequence of notes that can be read back into its original byte string. 

byte2jam is written in Python 2 and supports encoding any Python type that can
be read as a bytearray (near everything,) storing data in a schema class with
MIDI export/import and more to come.

## Getting Started

These instructions will get you a copy of the project up and running on your
local machine for development and testing purposes. See deployment for notes on
how to deploy the project on a live system.

### Prerequisites

For now, all you need to run byte2jam is a working Python 2 installation. This
project is packaged via setuptools and is intended to be hosted on pip once some
more core features are ironed out.

### Installing

In order to install the package, all you have to do is run the setup.py script
with Python and pass an install flag. For local installation:

```
python setup.py install --user
```

Or for a system-wide installation:

```
python setup.py install
```

### Testing

Lastly, you can run the test suite locally:

```
python setup.py test
```

## Built With

* [Python 2](https://www.python.org/) - Don't know what I'd do without it :')
* [python-midi](https://pypi.python.org/pypi/midi) - Used to export and import MIDI files

## Authors

* **Mark Snidal** - *Design, implementation, and testing* - [msnidal](https://github.com/msnidal)
* **Arielle Evans** - *Design, testing, and deployment* - [arevans3](https://github.com/arevans3)
* **Alex FL** - *Design and testing* - [Cyberunner23](https://github.com/Cyberunner23)

## License

This project is licensed under the LGPL License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

* In memory of Sheila Naftel, whose dedication and thoughtful passion for piano
  and musical theory education enabled this small project to exist.
