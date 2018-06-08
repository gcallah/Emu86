#!/usr/bin/awk -f
# this file processes asm files to turn them into ptml files

BEGIN {
    INDENT1 = "    "
    INDENT2 = INDENT1 INDENT1
    INDENT3 = INDENT2 INDENT1
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
    print INDENT1 "<head>"
    print "<!--include head.txt -->"
    print INDENT2 "<title>"
    print INDENT3 "" title
    print INDENT2 "</title>"
    print INDENT1 "</head>"
    print ""
    print INDENT1 "<body>"
    print INDENT2 "<div class=\"wrapper\">"
    print "<!--include navbar.txt -->"
    print INDENT1 "<br>"
    print "<!--include sample_programs.txt -->"
    print INDENT3 "<div id=\"content\">"
    print INDENT3 "<h1>"
    print INDENT3 "" title
    print INDENT3 "</h1>"
}

END {
    if(!error) {
        leave_codeblock()
        print INDENT3 "</div>"
        print INDENT2 "</div>"
        print INDENT1 "</body>"
        print "</html>"
    }
}

/^;/ {
    sub(/; /, "")
    if(!in_comments) {
        in_comments = 1
        leave_codeblock()
    }
    print INDENT3 "<p>"
    print
    print INDENT3 "</p>"
    next
}

{ 
    if(in_comments) {
        in_comments = 0
        print INDENT3 "<pre>"
        print INDENT3 "<code>"
    }
    print
}

function leave_codeblock()
{
    print INDENT3 "</code>"
    print INDENT3 "</pre>"
}
