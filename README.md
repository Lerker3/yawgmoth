# Yawgmoth

Yawgmoth is a Discord chat bot for r/competitiveEDH.

To install Yawgmoth's dependencies, use:

```
$ sudo ./setup.sh
```

To run Yawgmoth, use:

```
$ ./start.sh [username] [password]
```

Future functionality:

* !help - Command listing
* !frenchban - French/Duel Commander banlist
* Fixed searching (fails on some strings - unknown reason)
* Advanced searches (color, type, P/T, CMC, etc)
* Give yawgmoth additional bot functionality to be an automoderator


How to use git with git bash:
 * Install Git Bash and open it in the folder where you want to save this project
 * Clone the directory into a local folder
    *  ` git clone https://github.com/alexgerst/yawgmoth.git `
 *  Before making ANY CHANGES to your local copy, first make a new branch!
    *  ` git checkout -b BRANCH_NAME `
 *  Update your files / make your changes and commit them to your branch periodically. To do this:
    *  ` git add FILENAMES `
    *  ` git commit `
        *  This will bring up a place to put a commit message. Hit 'a' to add text, then to close this hit 'esc' ':' 'w' 'q' 'enter'
 *  When you are done making changes to your branch and want to merge it into the master code, do the following
    *  ` git push -u origin BRANCH_NAME `
 *  Go onto the github website and make a PULL REQUEST. Request to pull into master
 *  Someone ELSE will pull your changes into master after at least TWO people have given it a LGTM (Looks good to me)
 *  After your changes have been pulled into master, you must update your local copy (and delete the old branch)
    *  ` git checkout master `
    *  ` git pull `
    *  ` git branch -d BRANCH_NAME `

