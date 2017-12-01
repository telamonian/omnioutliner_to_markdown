import re

__all__ = ['FixCheckBoxes', 'FixTabs', 'TxtToMarkdown']

reCheckBox = re.compile('\[(.)\]')
def replCheckBox(matchobj):
    if matchobj.group(1)=='-':
        return '[ ]'
    elif matchobj.group(1)=='+':
        return '[x]'
    else:
        return matchobj.group(0)

reTab = re.compile('\t')
def replTab(matchobj):
    return ' '*4

def FixCheckBoxes(lines):
    return [reCheckBox.sub(replCheckBox, line) for line in lines]

def FixTabs(lines):
    return [reTab.sub(replTab, line) for line in lines]

def TxtToMarkdown(fpath, encoding='ISO-8859-1'):
    with open(str(fpath), mode='r', encoding=encoding) as f:
        lines = [line for line in f]

    lines = FixCheckBoxes(lines)
    lines = FixTabs(lines)

    with open(str(fpath), mode='w', encoding='ISO-8859-1') as f:
        [f.write(line) for line in lines]