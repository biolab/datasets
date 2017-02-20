# Orange data set repository

A collection of descriptions of data sets that are served in Data Set widget in [Orange](http://orange.biolab.si).

Each data set is described with a record that contains the following attributes:

    {
        "name": "wine.tab", # data set file name
        "title": "wine tasting",  # a short title (less then 40 characters)
        "description": "Wine profiling data with attributes from chemical analysis",  # description of the data set
        "tags": ["classification", "small"],  # any tags
        "target": "categorical",  # categorical, numeric, None
        "version": "1.0",  # data set version
        "year": 1991,  # year the original data set was published
        "collection": "UCI",  # name of original repository (like UCI)
        "instances": 178,  # number of data instances
        "missing": false,  # contains missing values?
        "variables": 13,  # number of independent variables
        "source": "https://archive.ics.uci.edu/ml/datasets/Wine",  # web page of original
        "size": 10991,  # data size in bytes
        "file": "http://my.web.server/wine.xls"  # the file will be downloaded from
    }
