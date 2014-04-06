=======
docgrep
=======

Like ``grep``, but only searches through docstrings (in Python code).


Installation
============

From pip::

    $ pip install --upgrade docgrep


Example
=======

::

    $ docgrep -r 'Python 3.4' .
    ./asyncio/futures.py:113: """This class is *almost* compatible with concurrent.futures.Future.

        Differences:

        - result() and exception() do not take a timeout argument and
          raise an exception when the future isn't done yet.

        - Callbacks registered with add_done_callback() are always called
          via the event loop's call_soon_threadsafe().

        - This class is not compatible with the wait() and as_completed()
          methods in the concurrent.futures package.

        (In Python 3.4 or later we may be able to unify the implementations.)
        """
