#!/usr/bin/env bash

read -r -d '' ASTR << EOM
tell application "OmniOutliner"
    writable document types
end tell
EOM

osascript -e "$ASTR"