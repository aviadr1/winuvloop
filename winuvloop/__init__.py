import sys

if sys.platform in ('win32', 'cygwin', 'cli'):
    import winloop
    run = winloop.run
    install = winloop.install
else:
    import uvloop
    run = uvloop.run
    install = uvloop.install

__all__ = [run, install]
