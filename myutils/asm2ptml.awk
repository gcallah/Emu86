#!/usr/bin/awk -f
# this file processes asm files to turn them into ptml files

BEGIN {
    in_comments = 1
    error = 0
    if (ARGC < 2) {
        print "Must pass file to process" > "/dev/stderr"
        error = 1
        exit 1
    }
    split(ARGV[1], a, "/")
    title = a[2]
    print "<!DOCTYPE html>"
    print "<html>"
    print "    <head>"
    print "<!--include head.txt -->"
    print "        <title>"
    print "            " title
    print "        </title>"
    print "    </head>"
    print ""
    print "    <body>"
    print "        <div class=\"wrapper\">"
    print "<!--include navbar.txt -->"
    print "            <div id=\"content\">"
    print "            <h1>"
    print "            " title
    print "            </h1>"
}

END {
    if(!error) {
        print "            </code>"
        print "            </pre>"
        print "            </div>"
        print "        </div>"
        print "    </body>"
        print "</html>"
    }
}

/^;/ {
    sub(/; /, "")
    if(!in_comments) {
        in_comments = 1
        print "            </code>"
        print "            </pre>"
    }
    print "            <p>"
    print
    print "            </p>"
    next
}

{ 
    if(in_comments) {
        in_comments = 0
        print "            <pre>"
        print "            <code>"
    }
    print
}
