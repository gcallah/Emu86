#!/usr/bin/awk -f
# this file processes asm files to turn them into ptml files

BEGIN {
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
    print "            <pre>"
    print "            <code>"
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
    print "            </code>"
    print "            </pre>"
    print "            <p>"
    print
    print "            </p>"
    print "            <pre>"
    print "            <code>"
    next
}

{ print }
