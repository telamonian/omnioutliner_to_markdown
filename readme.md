# Convert OmniOutliner docs to markdown the easy way

I'm sharing some of my OmniOutliner files (in particular, my ongoing todo lists) online in a gitlab repo. However, not everybody has OmniOutliner (or a mac), so I figured it would be nice to display the contents of the .ooutline files directly via gitlab's (or github's) built in markdown rendering.

Unfortunately, there's no built-in support for markdown, and all of the existing solutions are clunky, to say the least. So I built this instead!

## Install

Clone/cd into the repo, then just do

    pip install .

## Use

    from ootomd import OOutlineToMarkdown
    OOutlineToMarkdown(<path-to-.ooutline-file>)

and that's it! See the docstring of `OOutlineToMarkdown` for more info on optional args.
