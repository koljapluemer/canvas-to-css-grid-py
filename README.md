> [!NOTE]  
> *Archived Prototype. I will return to this crazy project when I ever have lots of time at my hands.*

Python-based attempts to convert Open Canvas Flowcharts to neat HTML/CSS with CSS grid.

## Attemps


### `src`

- new version
- TDD based
- so far, all tests green, but cannot yet place nodes (or edges)

#### Adding Code

*Info: There is currently no code here except classes, and tests using these classes*

0. Read class doc in `src/classes/.doc.md`

1. Start with a new folder in `src/tests`
2. Use the data in `src/tests/data` to create an `ObjectManager` and or `Grid`, and make a red test for the function to be implemented
3. Green the test 

Tip: Files in `src/tests/017_` (...) are validated to represent valid structures, and to be equivalent to one another.

### `_old`

`src/make_css_grid.py` actually produces decent output. Run and iterate.


## Testing

Go into `venv` at root, and run `pytest`.


## Check out

- Canvas Library: https://pypi.org/project/PyJSONCanvas/
