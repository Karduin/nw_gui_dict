# NovelWriter GUI Dictionary

> **A challenge with the documentation is definitely to keep the text in it in sync with the same labels on the GUI.**

The aim of these two python scripts is to create a kind of reference dictionary to maintain consistency between GUI and documentation translations.

All nw_xx_XX.ts language files in the i18n folder can be used. So if you want to translate the documentation into your language and use the same terms as the GUI, this little application will let you search the source for the original string and see its translation.

## how does it work?

### You will need:
* Python
* Flask module
* This repository
* A nw_xx_XX.ts file

### Procedure:
* First run ts_to_sqlite.py with nw_xx_XX.ts as argument.

Example:
```python

python ts_to_sqlite.py nw_fr_FR.ts
```

It will build the database `nw_gui_dict.db`
* Second run nw_gui_dict.py and go to http://localhost:5000

    Then search search for what you want.


### What we get
* Enpty string in search field show all.
* You can perform a partial search, for example `head` return all entry with head inside.

*PS: I know you shouldn't use the development server, but for a small local application it should be fine.*