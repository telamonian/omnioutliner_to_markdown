from pathlib import Path

from ootomd.appleScript import CompileAstrTellApp, RunAppleScript
from ootomd.txtToMarkdown import TxtToMarkdown

__all__ = ['formats', 'ActivateOutliner', 'GetFormatsOutliner', 'OOutlineToFormat', 'OOutlineToMarkdown']

# all of the format strings that OmniOutliner considers valid.
formats = {
    'com.omnigroup.omnioutliner.xmlooutline',
    'com.omnigroup.omnioutliner.ooutline',
    'com.omnigroup.omnioutliner.oooutline',
    'com.omnigroup.omnioutliner.xmlooutline-package',
    'com.omnigroup.omnioutliner.otemplate',
    'com.omnigroup.omnioutliner.otemplate-package',
    'com.omnigroup.omnioutliner.oo3',
    'com.omnigroup.omnioutliner.oo3-package',
    'com.omnigroup.omnioutliner.oo3template',
    'com.omnigroup.omnioutliner.oo3template-package',
    'org.opml.opml',
    'com.apple.news.opml',
    'org.opml.opmltemplate',
    'public.rtf',
    'public.plain-text',
    'com.apple.rtfd',
    'com.omnigroup.word.openxml.indented.Microsoft Word (indented)',
    'com.omnigroup.word.openxml.outline.Microsoft Word (outline)',
    'com.omnigroup.OmniOutliner.SimpleHTMLExport.HTML',
    'org.openxmlformats.presentationml.presentation.PowerPoint 2012 Format (pptx)',
    'com.omnigroup.OmniOutliner.OO3HTMLExport.OO3HTMLDynamic',
    'com.omnigroup.OmniOutliner.HTMLExport.HTMLDynamic',
    'com.microsoft.excel.openxml.document.Excel 2010 Format (xlsx)',
    'com.omnigroup.OmniOutliner.CSVExport.CSV',
    'markdown',
}
formatExtDct = {
    'org.opml.opml':                                     '.opml',
    'public.rtf':                                        '.rtf',
    'public.plain-text':                                 '.txt',
    'com.apple.rtfd':                                    '.rtfd',
    'com.omnigroup.OmniOutliner.CSVExport.CSV':          '.csv',
    'com.omnigroup.OmniOutliner.SimpleHTMLExport.HTML':  '.html',
    'com.omnigroup.OmniOutliner.HTMLExport.HTMLDynamic': '_dynamic.html',
    'markdown':                                          '.md',
}
extFormatDct = {val:key for key,val in formatExtDct.items()}


def _AstrActivateOutliner(safe):
    return CompileAstrTellApp('activate', appname='OmniOutliner', safe=safe)

def _AstrGetFormatsOutliner(safe):
    return CompileAstrTellApp('writable document types', appname='OmniOutliner', safe=safe)

def _AstrOOutlineToFormat(fpath, format, ext, fpathOut=None, safe=True):
    if format is None:
        if ext is not None and ext in extFormatDct:
            format = extFormatDct[ext]
    if format not in formats:
        raise ValueError('format not valid, should be one of formats. '
                         'format: %s, formats: %s' % (format, formats))

    if ext is None:
        if format in formatExtDct:
            ext = formatExtDct[format]
        else:
            ext = ''

    if fpathOut is None:
        fpathOut = Path(fpath).with_suffix(ext)

    # use plain text to form initial output (that will be cleaned up later) for  markdown
    if format=='markdown':
        format = extFormatDct['.txt']

    astr = [
        'open "%s"' % str(fpath),
        'expandAll',
        'close access (open for access ("%s" as POSIX file))' % str(fpathOut),    # this line is required to work around an osx sandboxing bug. See https://discourse.omnigroup.com/t/export-script-doesnt-work-anymore-in-sierra-10-12-2-fixed-in-sierra-10-12-4-or-see-thread-for-workaround
        'export document 1 to ("%s" as POSIX file) as "%s"' % (str(fpathOut), format),
        'close document 1'
    ]

    return CompileAstrTellApp(astr, appname='OmniOutliner', safe=safe),fpathOut


def ActivateOutliner(dryrun=False, safe=True):
    astr = _AstrActivateOutliner(safe=safe)

    if dryrun:
        return astr
    else:
        return RunAppleScript(astr=astr, safe=safe)

def GetFormatsOutliner(dryrun=False, safe=True):
    astr = _AstrGetFormatsOutliner(safe=safe)

    if dryrun:
        return astr
    else:
        return RunAppleScript(astr=astr, safe=safe)

def OOutlineToFormat(fpath, format=None, ext=None, fpathOut=None, dryrun=False, safe=True):
    """Convert an .ooutline to any format via a single Python function call.
    Uses some AppleScript, and so is dependent upon pyobjc.

    :fpath: Input file path. This is the .ooutline file that will be converted.
    :format: Any of the format str that OmniOutliner considers valid. A set containing all valid format str can be found at ootomd.formats.
    :ext: The filename extension that will be tacked onto the output file path in place of the input file's extension.
    :fpathOut: Output file path. If None, the converted file will be created at the same path as the input file, but with extension `ext`.

    Some args for debug
    :dryrun: return the AppleScript (as a string) and `fpathOut` instead of actually doing anything.
    :safe: if True, ensures that the runstate of OmniOutliner is unchanged by the actions of this function.
    """
    astr,fpathOut = _AstrOOutlineToFormat(fpath=fpath, format=format, ext=ext, fpathOut=fpathOut, safe=safe)

    if dryrun:
        return astr,fpathOut
    else:
        aret = RunAppleScript(astr=astr, safe=safe)

        if format=='markdown':
            # clean up the plain text output into proper markdown
            TxtToMarkdown(fpathOut)

        return aret

def OOutlineToMarkdown(fpath, format='markdown', ext='.md', fpathOut=None, dryrun=False, safe=True):
    """Convert an .ooutline to a markdown file via a single Python function call.
    Same as OOutlineToFormat, but with markdown-specific default args.

    :fpath: Input file path. This is the .ooutline file that will be converted.
    :format: Any of the format str that OmniOutliner considers valid. A set containing all valid format str can be found at ootomd.formats.
    :ext: The filename extension that will be tacked onto the output file path in place of the input file's extension.
    :fpathOut: Output file path. If None, the converted file will be created at the same path as the input file, but with extension `ext`.

    Some args for debug
    :dryrun: return the AppleScript (as a string) and `fpathOut` instead of actually doing anything.
    :safe: if True, ensures that the runstate of OmniOutliner is unchanged by the actions of this function.
    """
    return OOutlineToFormat(fpath=fpath, format=format, ext=ext, fpathOut=fpathOut, dryrun=dryrun, safe=safe)