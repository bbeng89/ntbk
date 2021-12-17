# NTBK

A simple, opinionated terminal notebook based loosely around the ideas of bullet journaling. 

## Why does this exist?

I used to be a dedicated bullet journaler until I got tired of the limitations of writing things by hand. I offloaded my todo list to Todoist and scheduling needs to the calendar provided by my email host. This works much better as I always have my phone on me, but I didn't always have my journal. However, I didn't have a good way of handling the long-form writing and journaling I did in my bullet journal. This is something I don't typically do "on the go" and instead prefer to type in vim as it's much faster and less limiting than pen and paper. I tried apps like Joplin but I really just wanted to be in the terminal with Vim and nothing else. I then tried just vim and NERDTree in Dropbox, which worked but I felt I needed some way of automating common tasks like opening todays "page" and quickly opening collections. That's where NTBK came in. 

### Philosophy

- Don't reinvent the wheel. Functions like todo lists and scheduling are handled better by other apps. Versioning and backup can be done by Dropbox, git, etc. It's up to the user and outside the scope of this project.
- No databases. Only work with the filesystem.
- It should be easy to navigate the generated file tree without ntbk. Ntbk only provides shortcuts.

## Usage

There are two types of files in ntbk - `logs` and `collections`. Logs are similar to the "daily log" in bullet journaling. They are just a page of text for the current day. Collections on the other hand contain related ideas and topics that don't belong to a particular day. For instance you might have a `recipes` collection or `books` collection. 

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

### Log

Log files are organized by year, month, then day. The default file for the day is `index.md` however, you can create as many files for the day as you like. This allows you to separate out different things for the day. For instance, you may want to keep your work notes in a separate file, or diary entries in a separate file. 

#### Opening log files

To open today's log file you can use the `today` command.

```
$ ntbk today
```

If today's date is 2021-12-16 this will open the file `log/2021/12-december/2021-12-16/index.md`. The file will be created if it doesn't already exist.

If you want to open a different file than `index.md` you can specify it as another parameter.

```
$ ntbk today work
```

Would open/create `log/2021/12-december/2021-12-16/work.md`

There are other shortcuts available as well.

```
$ ntbk yesterday
```

Would open/create `log/2021/12-december/2021-12-15/index.md`

```
$ ntbk tomorrow work
```

Would open/create `log/2021/12-december/2021-12-17/work.md`

```
$ ntbk date 2021-12-01
```

Would open/create `log/2021/12-december/2021-12-01/index.md`

Note that in all of these commands the `index.md` file is implied, unless you specify a different file name.

*Note - the filename `index.md` can be changed with the `default_filename` variable in `~/.config/ntbk/ntbk.yml`*

To list all the files for a given date use the `--list` flag

```
$ ntbk today --list
```

```
$ ntbk date 2021-12-14 --list
```

### Collections

Collections function very similarly to logs. To open/create a collection you use the `collection` command:

```
$ ntbk collection books
```
This would create the file `collections/books/index.md`

If you want to create a new file inside a collection, just pass it as another argument.

```
$ ntbk collection books 1984
```
Would create `collections/books/1984.md`

To list all your collections:

```
$ ntbk collections
```

To list all the files within a collection

```
$ ntbk collection books --list
```

### Templates

#### Writing Templates

The third directory in the `ntbk/` folder is `_templates`. Here you can create markdown files that will be used as a starting point for new files. Templates use the [Jinja2](https://jinja2docs.readthedocs.io/en/stable/templates.html) templating library, so all functions provided by jinja are available. 

By default there are only a few variables provided to the templates. They are: `now`, `today_iso`, `now_iso`, `today_long`, and `now_long`. Log files get an additional variable `log_date` which is the file's date. 

Additional variables can be provided in the config file and also with the `--vars` flag, which will be covered in a later section.

Given this template:

```
## Built in variables

{{ now.strftime('%A') }}
{{ today_iso }}
{{ now_iso }}
{{ today_long }}
{{ now_long }}
```

The following would be rendered:

```
## Built in variables

Thursday
2021-12-16
2021-12-16T13:18:37
Thursday, December 16, 2021
Thursday, December 16, 2021 01:18 PM
```

#### Using Templates

You can specify a template to be used with the `--template` or `-t` argument.

```
$ ntbk today diary --template diary.md
```

This will create the `diary.md` file for today using the `_templates/diary.md` template.

Collections can also use templates.

```
$ ntbk collection recipes meatloaf --template recipe.md
```

To see a list of templates available use the `templates` command

```
$ ntbk templates
```

You can also set a default template to be used for log entries and collections in your `~/.config/ntbk/ntbk.yml` file:

```
default_templates:
  log:
    index: log_default
    work: work_notes
  collection:
    books: book_review
    recipes: recipe
```
The `log` section defines the template to use for each type of log file. 

```
$ ntbk today
```
Would use the `log_default.md` template (note the .md extension is implicit in the config).

```
$ ntbk today work
```
Would use the `work_notes.md` template

For collections you can only specify a single template to be used by every file in the collection.

```
$ ntbk collection books 1984
```
Would use the `book_review.md` template

```
$ ntbk collection recipes
```
Would create an `index.md` file and use the `recipe.md` template.

#### Providing Additional Variables

If you have variables you want to be available to every template you can define them in the `template_vars` setting in `~/.config/ntbk/ntbk.yml`. You can provide any kind of data you like here. 

```
template_vars:
  owner: John Doe
  diary_tags:
    - diary
    - 2021
```

This would translate to a dict that can be used in your templates.

```
# Diary Entry
Author: {{ owner }}
Tags: {% for tag in diary_tags %}#{{ tag }} {% endfor %}
```

You can also provide additional variables with the `--vars` flag. These variables can only be simple strings in the format of `key=value`. You can provide as many as you like. Any values that contain spaces should be enclosed in quotes.

```
$ ntbk collection books dune --template book_review.md --vars title=Dune author="Frank Herbert"
```

---

If you have a default configured, but also use the `--template` argument, the default will be overridden. 

*Note - templates will only be used if the file you're opening doesn't exist or is empty. It will not overwrite existing files with the template content*

