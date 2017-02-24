# Orange data set repository

A collection of descriptions of data sets that are served in Data Set widget in [Orange](http://orange.biolab.si) and programs for generating the descriptions from a given data set.

Each data set is described with a record that contains the following attributes:

* name: data set file name
* title:  a short title (less then 40 characters)
* description:  description of the data set
* collection: name of original repository
* reference: any references to essential publications of the data set
* tags: a list of tags
* target: the type of target class, if any (categorical, numeric, or None)
* version:  data set version
* year: year when the data set was first published
* instances: number of data instances
* missing: does data contain any missing values?
* variables: number of independent variables (class and meta variables excluded)
* source: the web page from where the data set was obtained
* size: the size of the data set in bytes
* file: the web address of the Orange-readable file with the data set

Following is an example of description record for the wine data set. Note that the description would most often be longer and would contain at least a paragraph of text:

    {
        "name": "wine.tab", 
        "title": "wine tasting",  
        "description": "Wine profiling data with
	     attributes from chemical analysis.",  
        "tags": ["classification", "small"],  
        "target": "categorical",  
        "version": "1.0",  
        "year": 1991,  
        "collection": "UCI",  
	"reference": "Smit J, Miles C, Novak J (2016) On health impact of red wine, Altruism 18(3):42-142."
        "instances": 178,  
        "missing": false,  
        "variables": 13,  
        "source": "https://archive.ics.uci.edu/ml/datasets/Wine", 
        "size": 10991,  
        "file": "http://my.web.server/wine.xls"
    }
