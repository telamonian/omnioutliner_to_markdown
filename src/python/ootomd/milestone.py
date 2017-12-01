import gitlab as glab
import re

__all__ = ['FindGitlabDct', 'Milestone']

def FindGitlabDct(dcts, prop, propval, kindstr=None):
    """Find exactly one dict in a sequence of dicts `dcts` by testing `propval` against the `prop` property of each dict.

    :dcts: A sequence of dicts (such as that returned by gitlab.Gitlab.getgroups, .getprojects, etc).
    :prop: The property of each dict in `dcts` that will be tested.
    :propval: The searched-for value of dict['prop']. If a str is passed, the regex `re.search(propval, ...)` will be used to compare `propval` and dict['prop'].

    :return: exactly one dict. If zero or more than one dicts are found, an error is raised instead.
    """
    
    if isinstance(propval, str):
        propRe = re.compile(propval)
        dctsFound = [d for d in dcts if propRe.search(d[prop])]
    else:
        dctsFound = [d for d in dcts if propval==d[prop]]

    kindstr = ('of kind %s ' % kindstr) if kindstr is not None else ''
    if len(dctsFound)==0:
        raise ValueError("No dct %sfound in dcts for which dct[prop] matches propval."
                         "dcts: %s, prop: %s, propval: %s" % (kindstr, dcts, prop, propval))
    elif len(dctsFound) > 1:
        raise ValueError("Multiple dct %sfound in dcts for which dct[prop] matches propval. To resolve ambiguity, please specify complete propval exactly. "
                         "dcts: %s, prop: %s, propval: %s" % (kindstr, dcts, prop, propval))

    return dctsFound[0]

class Milestone(object):
    def __init__(self, host, token, projectTup=None, milestoneTup=None):
        self.host = host
        self.token = token
        
        self.projectTup = projectTup
        self.milestoneTup = milestoneTup

        self.projectDct = None
        self.milestoneDct = None

        self.gitlab = glab.Gitlab(self.host, oauth_token=self.token)

    def _fetchDct(self, getterName, prop, propval, getterArgs=None, getterKwargs=None, kindstr=None):
        if getterArgs is None: getterArgs = []
        if getterKwargs is None: getterKwargs = {}

        dcts = self.gitlab.__getattribute__(getterName)(*getterArgs, **getterKwargs)

        return FindGitlabDct(dcts=dcts, prop=prop, propval=propval, kindstr=kindstr)

    def fetchDct(self, tup=None):
        if tup is None: tup = self.milestoneTup

        self.fetchProjectDct()
        return self._fetchDct(getterName='getmilestones', getterArgs=(self.projectDct['id']), prop=tup[0], propval=tup[1], kindstr='milestone')

    def fetchProjectDct(self, tup=None):
        if tup is None: tup = self.projectTup

        self.projectDct = self._fetchDct(getterName='getprojects', prop=tup[0], propval=tup[1], kindstr='project')
        return self.projectDct