from Foundation import *
from itertools import chain
import struct

__all__ = [
    'CompileAstrTellApp', 'CharInt', 'IntChar', 'InitAppleScript',
    'InitEventOutputHandler', 'CallAppleScript', 'RunAppleScript'
]

_astrPreambleApp = '''tell application "%s"'''

_astrPostambleApp = '''end tell'''

_astrPreambleAppSafe = '''on is_running(appName)
    tell application "System Events" to (name of processes) contains appName
end is_running

set %sWasRunning to is_running("%s")

tell application "%s"'''

_astrPostambleAppSafe = '''end tell

if not %sWasRunning then
    tell application "%s"
        quit
    end tell
end if'''

def CompileAstrTellApp(astr, appname, safe=True, tab=None):
    """Place arbitrary applescript within a "tell application..." context.

    :astr: applescript to run within the "tell application `appname`"
    :safe: If True, add guards that ensure that the runstate of `appname` is the same before and after the script is invoked.
        If `appname` is not running before the script is invoked, `appname` is closed at the end of the script.
        If `appname` is running before the script is invoked, nothing happens (ie it remains open).
    """
    if safe:
        preamb = _astrPreambleAppSafe % ((appname,)*3)
        postamb = _astrPostambleAppSafe % ((appname,)*2)
    else:
        preamb = _astrPreambleApp % appname
        postamb = _astrPostambleApp

    if tab is None: tab = ' '*4

    if isinstance(astr, str):
        # assume astr is single str
        alines = [preamb, tab + astr, postamb]
    else:
        # assume astr is sequence of str
        alines = chain((preamb,), (tab + aline for aline in astr), (postamb,))

    return '\n'.join(alines)

def CharInt(bites):
    """Get the integer representation of an NSAppleEventDescriptor 4 letter code.

        :code: str of length 4, e.g. b'buts'
        :Result: int, for example fourcharcode('buts')==1651864691
    """
    return struct.unpack('>I', bites)[0]

def IntChar(ent):
    """Inverse of CharInt
    """
    return struct.pack('>I', ent)

def InitAppleScript(astr, safe=True):
    if safe:
        # this prevents the `is_running` function from opening the application if it's closed
        astr = 'run script "%s"' % (astr.replace('"', r'\"'))

    return NSAppleScript.alloc().initWithSource_(astr)

def InitEventOutputHandler(name):
    evt = NSAppleEventDescriptor.appleEventWithEventClass_eventID_targetDescriptor_returnID_transactionID_(
        CharInt(b'ascr'), CharInt(b'psbr'), NSAppleEventDescriptor.nullDescriptor(), 0, 0
    )
    evt.setDescriptor_forKeyword_(NSAppleEventDescriptor.descriptorWithString_(name), CharInt(b'snam'))

    return evt


def CallAppleScript(astr, name, safe=True):
    aobj = InitAppleScript(astr=astr, safe=safe)
    evt = InitEventOutputHandler(name)

    ret = aobj.executeAppleEvent_error_(evt, None)

    return aobj,ret

def RunAppleScript(astr, safe=True):
    aobj = InitAppleScript(astr=astr, safe=safe)
    ret = aobj.executeAndReturnError_(None)

    return aobj, ret
