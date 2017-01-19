#/bin/sh

# This generally should be run to start the work day: it puts you back in sync
# with the master branch. Of course, there are times you don't want that, and
# other time you may want to sync more often.

# $1 is the branch you are working on.

git checkout $1
git commit -a -m "Re-syncing with master."
git push origin $1
git checkout master
git pull origin master
git checkout $1
git merge master
