pypi-example
============

example project to configure a private PyPi Cheeseshop on OpenShift

Running on OpenShift
----------------------------

Create an account at http://openshift.redhat.com/

Create a "Python 2.6" application called 'pypi' or whatever

Add this upstream seambooking repo

    cd pypi
    git remote add upstream -m master git://github.com/masci/pypi-example.git
    git pull -s recursive -X theirs upstream master
    
Then push the repo upstream

    git push

That's it, you can now checkout your application at (default admin account is admin/admin):

    http://pypi-$yourlogin.rhcloud.com