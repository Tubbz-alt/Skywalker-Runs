Archive of Skywalker Alignments
===============================

This repo serves as the working directory of each Skywalker run and as an
archive of previous runs.

Basic Usage
-----------

Alignments are performed by executing the *run_skywalker_template.ipynb*
notebook. Changes to the alignment proceedure are made only in this file.
Snapshots of the notebook can be made using the *archive.py* script.

Notebook Archive
----------------

Previous runs are in directories named by the date the alignment was run, and
the files themselves are named using the template name, date and time it was
saved.

*Note* - Older notebooks may not follow the convention above.

Adding Sanpshots
----------------

To create a snapshot of the template notebook, simply run the *archive.py*
script,

    python archive.py

A new file should be added that has the directory and name structure mentioned
above. The script takes additional arguments if slight deviations of the
general work-flow is needed. Valid arguments are:

    -h, --help           show this help message and exit
    -v, --verbose        Increase verbosity.
    -d, --debug          Run in debug mode.
    --log_dir P          Path to save the logs in.
    -t P, --template P   Template file path to be copied.
    -s P, --save_path P  Save path for copied file.
