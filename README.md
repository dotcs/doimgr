# doimgr
A command line tool using crossref.org's API to search _Digital object identifier
(DOI)_ and obtain formatted citations such as bibtex, apa, and a lot more

## Install
To install _doimgr_, you first need to clone the repository

```bash
git clone https://github.com/dotcs/doimgr.git
```

**Please note, that _doimgr_ is using Python version 3 and will not work with
older Python versions.**

Make sure, that you have installed all necessary packages

```bash
pip install -r requirements.txt
```

Depending on your system environment, you might be interested in using a
[virtual
environment](http://virtualenv.readthedocs.org/en/latest/virtualenv.html).

## Essential usage information
Roughly spoken, _doimgr_ consists of two main parts - finding and using the
relevant _DOI(s)_.

### Finding _DOIs_
The first step consists of searching and finding a specific
[_DOI_](http://en.wikipedia.org/wiki/Digital_object_identifier).

To search for a specific article, you can use the syntax

```bash
python doimgr.py search "Stephen Hawking A Brief History Of Time"
```

which will give some results like in the following list

    3.35 - 1989 - 10.2307/4612083       - A Brief History Of Time: From The Big Bang To Black Holes
    1.57 - 1988 - 10.1063/1.2811637     - A Brief History Of Time
    1.48 -    0 - 10.2139/ssrn.1707364  - Stephen Hawking's Brief History Of Time: A Narrative Perspective (Perspectiva Narrativa Sobre Historia Del Tiempo, De Stephen Hawking) (Spanish)
    [ ... and many more ...]

The columns show the following information:

1. Relevance/Score of the result
2. Year of publication
3. DOI
4. Title

Checking the title, you may find, that you are interested in the first result,
which is represented by the _DOI_ `10.2307/4612083`.

### Create a citation using a _DOI_
In the second step, the _DOI_ can be used to create a citation using the command

```bash
python doimgr.py cite 10.2307/4612083
```

This will generate the following output

     @article{Holyoke_1989, title={A Brief History of Time: From the Big Bang to Black Holes}, volume={47}, ISSN={0003-5769}, url={http://dx.doi.org/10.2307/4612083}, DOI={10.2307/4612083}, number={3}, journal={The Antioch Review}, publisher={JSTOR}, author={Holyoke, T. C. and Hawkings, Stephen}, year={1989}, pages={363}}

You can use this in your latex/bibtex file to cite Hawkings.

That was easy, wasn't it?

## Detailed usage information
We have learned about the basics of the tool by using `search` and `cite`
parameters. But this is not all, since we can define a lot more options to
state more precisely what we want to search and how we want the results to be
formatted.

### Use search boundaries
To gain more control about the results, there exists multiple option to
fine-tune our search.

In general it is a good idea, to have a look at the help, to see what is possible:

```bash
python doimgr.py search --help
```

#### Filter journals, books, and many more
We might be interested mostly in scientific articles, but not in books. Thus we
can make use of the `type` parameter:

```bash
python doimgr.py search "Stephen Hawkings" --type journal-article
```

The result then looks like this:

    3.40 - 1989 - 10.2307/4612083                - A Brief History Of Time: From The Big Bang To Black Holes
      TYPE      : journal-article
    1.76 - 2014 - 10.1038/nature.2014.14583      - Stephen Hawking: 'There Are No Black Holes'
      TYPE      : journal-article
    1.58 - 2012 - 10.1088/0264-9381/29/1/015004  - White Holes And Eternal Black Holes
      TYPE      : journal-article
    [ ... and many more ...]

Now every result is of the type `journal-article`. See the help to find out
what other types are possible.

### Specify citation format
To specify the citation format you can choose out of hundreds of different
formats. Most common citation formats are `bibtex`, `apa`, `ieee` and
`harvard1`. See all possible formats by having a look at the file
`API/styles.txt`.

Specify the format by the `--style` parameter

```bash
python doimgr.py cite 10.2307/4612083 --style ieee
```

This results in

    [1]T. C. Holyoke and S. Hawkings, “A Brief History of Time: From the Big Bang to Black Holes,” The Antioch Review, vol. 47, no. 3, p. 363, 1989.

## Using a config file for permanently enabling/disabling parameters
You find yourself using the same parameters again and again? - Use a config
file instead!

Let's say you want always to show the authors in your search queries. You can
do so by using the `--show-authors` flag for every query as in the following
example:

```bash
python doimgr.py search "Stephen Hawkings" --show-authors
```

Since it is annoying to do this every time, you better use a config file to
handle that for you.

The script tries to read a config file located at `~/.doimgrrc`. It is a good
start to copy the sample file and use it as a base

```bash
cp sample_config.cfg ~/.doimgrrc
```

To show permanently the authors, search for the `search` section and change the line

```config
show-authors   = False
```

to

```config
show-authors   = True
```

You can do that with all other options, too. This allows you to permanently
show authors, types, publisher and URL information. It also allows you to
change how the sorting is done (the default sorting is by the score of the
individual results), change the order in general, allows you to change how many
rows should be requested (= the maximum number of results per query) and much
more.

Also you can change the default style for the `cite` command by changing
`style` in the `cite` section.

## Good to know
### Simplify access to _doimgr_
Depending on your knowledge of Linux/Mac, you might know how to place the
script in your `$PATH` environment variable. If not, you might follow these
steps. It's easy to do.

1. Check if you have user `~/bin` folder by typing `mkdir ~/bin`. This will
   create a `bin`-folder inside your home-directory if you do not have one
   yet.
2. Make the script executable by running `chmod +x
   /path/to/doimgr/doimgr.py`, where you have to substitute the correct
   path
3. Link the file to the `bin`-folder by first navigating to the folder: `cd
   ~/bin`. Then create the link via `ln -s /path/to/doimgr/doimgr.py
   doimgr`.
4. Try to call the script via `doimgr --help`. If this shows the help the
   _doimgr_ command, you are done.

## Debugging and scripting
_doimgr_ supports different logging messages, that are shown. You can increase
the amount of messages by using `--log-level debug`.

```bash
python doimgr.py --log-level debug search "Stephen Hawkings"
```

Of course you can also script _doimgr_. It is a good idea, to use the `--quiet`
flag then, which suppresses all messages but the results of queries.

An example call could look like

```bash
python doimgr.py search "Stephen Hawkings Black Holes" --type journal-article --rows 3 | awk '{print $5}'
```

The results are then just the _DOIs_:

    10.2307/4612083
    10.1038/nature.2014.14583
    10.1088/0264-9381/29/1/015004
