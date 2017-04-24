#!/usr/bin/awk -f

BEGIN {
    in_list = 0
}

/<instr>/    {
    print "<hr>"
    print "<h4>"
    next
}

/<\/instr>/  {
    print "</h4>\n" 
    next
}

/<syntax>/   { 
    print "<h5>Syntax</h5>\n"
    in_list = 1
    print "<ul>"
    next
}

/<\/syntax>/ { 
    print "</ul>"
    in_list = 0
    next
}

/<descr>/    {
    print "<h5>Description</h5>\n"
    print "<p>"
    next
}

/<\/descr>/  {
    print "</p>" 
    next
}

{
    if(in_list) {
        print "<li>" $0
    }
    else {
        print
    }
}
