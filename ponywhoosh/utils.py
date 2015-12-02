#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: d555

from pony import orm

@orm.db_session
def search(model, *arg, **kw):
    """Ponywhoosh function to perform searches on specific models. It takes up three arguments:

    Args:
        model (TYPE): Where you want to search. 
        *arg: The search string. 
        **kw: Aditional options like : 
            Include entity: To include the whole entity model from what you are searching. 
            Add_wildcards: The option to perform inexact searches (By default is False). 
            Something: It search first for exact terms but if it does not find anything it performs a search adding wildcards.

    Returns:
        TYPE: A result object dictionary. 
    """
    return model._pw_index_.search(*arg, **kw)


@orm.db_session
def delete_field(model, *arg):
    """ It deletes an specific field stored in the index.  

    Args:
        model (TYPE): Is the model from where you want to delete an specific field. 
        *arg: Fiedls. 

    Returns:
        TYPE: model without the desired field. 
    """
    return model._pw_index_.delete_field(*arg)


def full_search(pw, *arg, **kw):
    """ This function search in every model registered. And portrays the result in a dictionary where the keys are the models. 

    Args:
        pw (PonyWhoosh): This is where all the indexes are stored. 
        *arg: The search string. 
        **kw: The options available for a single search wildcards, something, fields, models, etc. 

    Returns:
        TYPE: Dictionary with all the the results for the models. 
    """
    return pw.search(*arg, **kw)
