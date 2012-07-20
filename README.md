PyPi Example
============

example project to configure a private PyPi Cheeseshop on OpenShift

How to run on OpenShift
----------------------------

Create a "Python 2.6" application called 'pypi' or whatever, then clone the
application repository.

Add this repo as an upstream remote and pull contents

    cd pypi
    git remote add upstream -m master git://github.com/masci/pypi-example.git
    git pull -s recursive -X theirs upstream master
    
Then push to your app repo

    git push

That's it, you can now checkout your application at:

    http://pypi-$yourlogin.rhcloud.com

Login as **admin** with password **admin**

Techies
-------
You can password-protect your cheeshop in settings.py:

    PASSWORD_PROTECT_PYPI = True

Django users will be logged in through HTTP Basic authentications, so pip and
easy_install can play the game.

Built on:
 - djangopypi
 - django-sendfile
