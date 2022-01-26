<p align="center">
<img src="https://user-images.githubusercontent.com/356577/146586531-01bbc413-a876-4c7b-a0a5-889b99558e19.png" />
</p>
<p align="center">
A simple, opinionated terminal notebook inspired by bullet journaling. 
</p>

![](https://img.shields.io/pypi/v/ntbk)
![](https://img.shields.io/pypi/pyversions/ntbk)
![](https://github.com/bbeng89/ntbk/workflows/Tests/badge.svg)
![](https://img.shields.io/github/license/bbeng89/ntbk)

# Contents

- [Contents](#contents)
  - [Why does this exist?](#why-does-this-exist)
  - [Project philosophy](#project-philosophy)
  - [Installation](#installation)
  - [Folder structure](#folder-structure)
  - [Usage](#usage)
    - [Opening today's log](#opening-todays-log)
    - [Opening logs for other days](#opening-logs-for-other-days)
    - [Listing log files](#listing-log-files)
    - [Jotting notes](#jotting-notes)
    - [Opening collections](#opening-collections)
    - [Listing collections](#listing-collections)
    - [Subdirectories in collections and logs](#subdirectories-in-collections-and-logs)
    - [Writing Templates](#writing-templates)
    - [Using templates](#using-templates)
    - [Listing available templates](#listing-available-templates)
    - [Default templates](#default-templates)
    - [Providing additional template variables in config](#providing-additional-template-variables-in-config)
    - [Providing additional template variables with --vars flag](#providing-additional-template-variables-with---vars-flag)
    - [Finding files](#finding-files)
    - [Finding directories](#finding-directories)
    - [Abbreviated commands](#abbreviated-commands)
  - [Config](#config)
  - [Roadmap](#roadmap)
  - [Contributing](#contributing)

## Why does this exist?

I used to be a dedicated bullet journaler until I got tired of not always having my notebook and the slowness of writing by hand. I moved my todo list to Todoist and scheduling to a web calendar, however, I still didn't have a good way of handling the long-form writing and journaling I did in my bullet journal. I tried apps like Joplin but I really wanted to only be in the terminal with Vim and nothing else. I tried Vim and NERDTree in Dropbox, which worked, but I felt I needed a way of automating common tasks like opening todays log and collections, so ntbk was born. 

## Project philosophy

- Don't reinvent the wheel. Todo lists and scheduling are handled better by other apps. Versioning and backup can be done by Dropbox and git. Grep works great for search. These tasks are up to the user and outside the scope of this project. ntbk only provides shortcuts to working with plain text files within its opinionated structure.
- It should be easy to navigate the generated file tree without ntbk.
- No databases. Only work with the filesystem.

## Installation

```console
foo@bar:~$ pip install ntbk
```

Once installed, just run:

```console
foo@bar:~$ ntbk
```

You will be prompted for the notebook directory and editor you want to use. This will create the config file and notebook folders for you then immediately open today's log. By default a simple template for log entries will be created for you at `_templates/log_default.md`.

## Folder structure

There are two main entities in ntbk - `logs` and `collections`. Logs are similar to the "daily log" in bullet journaling. They contain text for the current day. Collections on the other hand contain related ideas and topics that don't belong to a particular day. For instance you might have a `recipes` collection or `books` collection. 

An ntbk directory will look like the following:

```
    ntbk/
    ├─ _templates/
    │  ├─ diary.md
    │  ├─ book-review.md
    ├─ collections/
    │  ├─ reading/
    │  │  ├─ 1984.md
    │  ├─ recipes/
    │  │  ├─ index.md
    ├─ log/
    │  ├─ 2021/
    │  │  ├─ 01-january/
    │  │  │  ├─ 2021-01-01/
    │  │  │  │  ├─ index.md
    │  │  │  │  ├─ work.md
    │  │  │  ├─ 2021-01-02/
    │  │  │  │  ├─ index.md
```

Log files are organized by year, month, then day. The default file for the day is `index.md` however, you can create as many files for the day as you like. This allows you to separate out different things for the day. For instance, you may want to keep your work notes in a separate file, or diary entries in a separate file. 

Collections are very similar, but are not structured by date. A collection is essentially a folder, and the default file within it is `index.md`, though you can create any files within the collection you want.

## Usage

In the following examples it will be assumed today's date is 2021-12-16.

### Opening today's log

To open today's log file you can use the `today` command.

```console
foo@bar:~$ ntbk today
```

This will open the file `log/2021/12-december/2021-12-16/index.md`. The file will be created if it doesn't already exist.

Simply running the script without any arguments is the same as using the today command, however, you cannot add any additional arguments like `--template` or specify a different file (covered later). It's simply a shortcut to open today's index file.
 
 ```console
 foo@bar:~$ ntbk
 ```

If you want to open a different file than `index.md` you can specify it as another parameter.

```console
foo@bar:~$ ntbk today work
```

Would open/create `log/2021/12-december/2021-12-16/work.md`

### Opening logs for other days

```console
foo@bar:~$ ntbk yesterday
```

Would open/create `log/2021/12-december/2021-12-15/index.md`

```console
foo@bar:~$ ntbk tomorrow work
```

Would open/create `log/2021/12-december/2021-12-17/work.md`

```console
foo@bar:~$ ntbk date 2021-12-01
```

Would open/create `log/2021/12-december/2021-12-01/index.md`

Note that in all of these commands the `index.md` file is implied, unless you specify a different file name.

*Note - the filename `index.md` can be changed with the `default_filename` [config](#config) variable.*

### Listing log files

To list all the files for a given date use the `--list` flag

```console
foo@bar:~$ ntbk today --list
work
index
notes
```

```console
foo@bar:~$ ntbk date 2021-12-14 --list
index
```

### Jotting notes

Sometimes you just want to make a quick note without having to open your editor. To do this you can use the `jot` command. This command will only write to today's log.

```console
foo@bar:~$ ntbk jot "some quick note"
Jotted note to today's index file
```

If you'd like to jot to a different file you can specify the file after your note.

```console
foo@bar:~$ ntbk jot "some quick note" notes
Jotted note to today's notes file
```

To automatically add the current time before your jotted note use the `--timestamp` or `-s` flag.

```console
foo@bar:~$ ntbk jot "some note" --timestamp
Jotted note to today's index file
```

### Opening collections

Collections function very similarly to logs. To open/create a collection you use the `collection` command:

```console
foo@bar:~$ ntbk collection books
```

This would create the file `collections/books/index.md`

If you want to create a new file inside a collection, just pass it as another argument.

```console
foo@bar:~$ ntbk collection books 1984
```

Would create `collections/books/1984.md`

### Listing collections

To list all your collections:

```console
foo@bar:~$ ntbk collections
books [2 files]
travel-2022 [1 file]
recipes [1 file]
```

To list all the files within a collection

```console
foo@bar:~$ ntbk collection books --list
1984
brave-new-world
```

### Subdirectories in collections and logs

For collections, subdirectories are specified as part of the collection name:

```console
foo@bar:~$ ntbk collection books/fiction the-hobbit
```
This would open/create `collections/books/fiction/the-hobbit.md`

Listing a subdirectory is the same:

```console
foo@bar:~$ ntbk collection books/fiction --list
```

Logs are different since an alias like `today` or `yesterday` is often used. So for logs you specify the path with the filename.

```console
foo@bar:~$ ntbk today work/meeting-notes
```

This would open/create `log/2021/12-december/2021-12-16/work/meeting-notes.md`

To list files for this new `work` directory, just add a forward slash to the directory name and use the `--list` flag:

```console
foo@bar:~$: ntbk today work/ --list
```

You can go as deep as you want with this:

```console
foo@bar:~$: ntbk today work/meetings/ --list
```

In both collections and logs you can use the `--recursive` or `-r` flag to recursively list all files:

```console
foo@bar:~$: ntbk c books -lr
```

```console
foo@bar:~$: ntbk tod -lr
```

### Writing Templates

The third directory in the `ntbk/` folder is `_templates`. Here you can create markdown files that will be used as a starting point for new files. Templates use the [Jinja2](https://jinja2docs.readthedocs.io/en/stable/templates.html) templating library, so all functions provided by jinja are available. 

The following variables are available to templates by default. Additional variables can be provided in the [config file](#providing-additional-template-variables-in-config) and also with the [--vars flag](#providing-additional-template-variables-with---vars-flag).

| Variable     | Type     | Example                              | Notes                                                                       |
|--------------|----------|--------------------------------------|-----------------------------------------------------------------------------|
| `now`        | datetime |                                      | All python datetime methods are available                                   |
| `today_iso`  | string   | 2021-12-16                           |                                                                             |
| `now_iso`    | string   | 2021-12-16T13:18:37                  |                                                                             |
| `today_long` | string   | Thursday, December 16, 2021          |                                                                             |
| `now_long`   | string   | Thursday, December 16, 2021 01:18 PM |                                                                             |
| `log_date`   | datetime |                                      | Only available in templates for log files. Represents the date of the file. |

Given this template:

```markdown
## Built in variables

{{ now.strftime('%A') }}
{{ today_iso }}
{{ now_iso }}
{{ today_long }}
{{ now_long }}
```

The following would be rendered:

```markdown
## Built in variables

Thursday
2021-12-16
2021-12-16T13:18:37
Thursday, December 16, 2021
Thursday, December 16, 2021 01:18 PM
```

### Using templates

You can specify a template to be used with the `--template` or `-t` argument.

```console
foo@bar:~$ ntbk today diary --template diary
```

This will create the `diary.md` file for today using the `_templates/diary.md` template.

Collections can also use templates.

```console
foo@bar:~$ ntbk collection recipes meatloaf --template recipe
```

### Listing available templates

To see a list of templates available use the `templates` command. 

```console
foo@bar:~$ ntbk templates
bible-entry
grocery-list
book-review
journal_default
log_default
work-notes
```

### Default templates

You can also set a default template to be used for log entries and collections in your [config](#config) file:

```yaml
default_templates:
  log:
    index: log_default
    work: work_notes
  collection:
    books: book_review
    recipes: recipe
```

The `log` section defines the template to use for each type of log file. 

For example:

```console
foo@bar:~$ ntbk today
```

Would use the `log_default.md` template (note the .md extension is implicit in the config).

```console
foo@bar:~$ ntbk today work
```

Would use the `work_notes.md` template

For collections you can only specify a single template to be used by every file in the collection.

```console
foo@bar:~$ ntbk collection books 1984
```

Would use the `book_review.md` template

```console
foo@bar:~$ ntbk collection recipes
```

Would create an `index.md` file and use the `recipe.md` template.

If you have a default configured, but also use the `--template` argument, the default will be overridden. 

*Note - templates will only be used if the file you're opening doesn't exist or is empty. It will not overwrite existing files with the template content*

### Providing additional template variables in config

If you have variables you want to be available to every template you can define them in the `template_vars` setting in [your config](#config). You can provide any kind of data you like here. 

```yaml
template_vars:
  owner: John Doe
  diary_tags:
    - diary
    - 2021
```

The `owner` and `diary_tags` variables would now be available in your templates. 

```markdown
# Diary Entry
Author: {{ owner }}
Tags: {% for tag in diary_tags %}#{{ tag }} {% endfor %}
```

### Providing additional template variables with --vars flag

You can also provide additional variables at runtime with the `--vars` flag. These variables can only be simple strings in the format of `key=value`. You can provide as many as you like. Any values that contain spaces should be enclosed in quotes.

```console
foo@bar:~$ ntbk collection books dune --template book_review --vars title=Dune author="Frank Herbert"
```

### Finding files

Passing the `--find` or `-f` flag will output the files path rather than opening it in your editor.

```console
foo@bar:~$ ntbk today --find
/home/blake/ntbk/2021/12-december/2021-12-16/index.md
foo@bar:~$ ntbk today notes -f
/home/blake/ntbk/2021/12-december/2021-12-16/notes.md
foo@bar:~$ ntbk collection books --find
/home/blake/ntbk/collections/books
```

This can be useful if you want to do things like `cat` the contents of the file:

```console
foo@bar:~$ cat `ntbk today --find`
```

### Finding directories

Passing the `--find-dir` or `-d` flag will output the directory path.

```console
foo@bar:~$ ntbk today --find-dir
/home/blake/ntbk/2021/12-december/2021-12-16
foo@bar:~$ ntbk collection books -d
/home/blake/ntbk/collections/books
```

This can be useful if you want to do things like `cd` to the directory:

```console
foo@bar:~$ cd `ntbk today -d`
```

### Abbreviated commands

The following command abbreviations are available:

`today` = `tod`

`tomorrow` = `tom`

`yesterday` = `yest`

`date` = `dt` or `d`

`collection` = `col` or `c`

`collections` = `cols`

They can be used in place of any normal command. For example, to open the file for date 2021-12-01:

```console
foo@bar:~$ ntbk d 2021-12-01
```

## Config

The config file is located at `~/.config/ntbk/ntbk.yml`

Below is a sample config file with all options documented.

```yml
# Your notebook folder
ntbk_dir: ~/ntbk

# The editor to be used when opening files
editor: vim 

# Location of templates, relative to ntbk_dir
template_dir: _templates

# Filename to use if one is not specified
default_filename: index

# Mapping of default templates for log and collection files
default_templates:
  log:
    # use the log_default.md template any time an index.md file is created
    index: log_default
    # use the work_notes.md template any time a work.md file is created
    work: work_notes
  collection:
    # use the book_review.md template for all files created in the books collection
    books: book_review
    # use the recipe.md template for all files created in the recipes collection
    recipes: recipe

# User-defined variables that will be available in every template
template_vars:
  # the author var will be in every template and can be used like {{ author.first_name }}
  author:
    first_name: John
    last_name: Doe
  # this list will be available to every template
  default_tags:
    - "2020"
```

## Roadmap

There is a lot more that can be done with this app. The following are ideas/features I'd like to pursue:

- Vim plugin - I'd like to have a plugin so you can run ntbk commands from within vim, rather than going back to the terminal
- Html/PDF/etc generation with something like pandoc (or maybe even jekyll)
- Natural language processing so you can do things like `ntbk last monday`
- Possibly an accompanying mobile app one day. I'd like a very basic mobile markdown editor that worked with Dropbox (and maybe others) and had the ntbk shortcuts (today, collections, etc.)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)
