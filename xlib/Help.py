#
# Help class for on-line documentation /help in tdl
# M. Newville Univ of Chicago, T. Trainor, Univ of Alaska, Fairbanks (2005,2006)
#
# --------------
# Modifications
# --------------
#  28-Apr-06 T2 - moved show/help from shell into Help class
#
#  20-Mar-06 MN - changed to have a Help class that contains a dictionary of
#                 help topics
#                
#
#
##########################################################################


ShellUsage = """
  Tdl command-line shell help:
   
"""

HelpHelp =  """
  ###########################################################################
   = Help options =
    help                  # Help options (this list)
    help topics  (-t)     # list topics for additional help
    help <name>           # Detailed help on specific topic, function, or variable
    (see also: 'help show')
  ###########################################################################
"""

HelpShow =  """
  ###########################################################################
   = Show options =
    show                  # summary list of groups, functions and variables
    show groups    (-g)   # list currently defined groups
    show group <name>     # list functions and variables in named group
    show functions (-f)   # list functions, organized by group
    show variables (-v)   # list variables, organized by group
    show <name>           # show details on specific function, or variable
    (see also: 'help' and 'help topics')
  ###########################################################################
"""

Overview = """
This is TDL (Tiny Data Language, Matt Newville and Tom Trainor 2006).

Tdl is a data processing language written in python and designed to be 
  - easy to use for novices.
  - complete enough for intermediate to advanced data processing.
  - data-centric, so that arrays of data are easy to manage and use.
  - easily extendable with python.
 
Tdl uses Numeric Python and SciPy for all its numerical functionality, so
processing arrays of numerical data is easy and fast, and a wide range
of 'advanced numeric capabilities' such as FFTs and non-linear least squares
minimization is (potentially) available for Tdl.

TDL Features:

==Simple Syntax:
  Variable and function names are simple, undecorated strings.

==Data Types:
  Variabls can contain any of the following data types:  ints, floats,
    complex, strings, lists, dictionaries (hashes), or NumPy arrays.

  Multi-dimensional data can be accessed either element-by-element or with
  more complicated "slices":
        tdl> x   = 1             # int
        tdl> y   = 7 + 2j        # complex number:  real + imag'j'
        tdl> arr = arange(10)    # simple array 
        tdl> print arr 
            [0 1 2 3 4 5 6 7 8 9 10]
        tdl> print arr[3]
            3
        tdl> print arr[2:8]
            [2 3 4 5 6 7]
        tdl> str = 'here is a string'
        tdl> print str[0:6]
            here i

==Full Featured, extensible:  many useful functions for numerical data
  processing are built in to Tdl.  More importantly, it is easy to add more
  functions, either from Python or as Tdl procedures (see below). 

==Namespaces:  Each variable and function has two parts to its name:
  a Group Name and Variable Name.  The fully qualified name includes a '.'
  and looks like group.var.

  Unqualified names (ie, a name without a 'group.' prefix) will use a default
  order to determine which Group to associate with a name:  There is always
  a "Default Data Group" and a "Default Function Group" each of which can be
  changed during a TDL session.  At startup, there are two pre-defined groups:
  "_builtin", which contains many built in functions and constants (sin and pi,
  for example), and "_main".  At startup, "_main" is empty, and is set as the
  "Default Data Group" and "Default Function Group".
  
  When creating or assigning a variable without an explicit group name, the default
  Data Group is used.  When creating or assigning a procedure without an explicit
  group name, the default Function Group is used.
  
  When using (say, on the right-hand side of a statement) a variable or function with
  an unqualified group name, the first matching name in the list
     (Default Data Group, Default Function Group, "_main", "_builtin") 

  is used.  The Default Data Group can be changed with
        tdl> datagroup('mydata')

  and the Default Function Group can be changed with 
        tdl> funcgroup('myfuncs')

  Assigning a fully qualified variable or function to a group that previously did
  not exist will create that group:
        tdl> x = 1
        tdl> group1.x = 3.3
        tdl> print x
            1
        tdl> datagroup('group1')
        tdl> print x
            3.3
        tdl> print _main.x, group1.x
            1 3.3
        tdl> show groups
            Default Data Group = group1
            Default Function Group = _main
            All Groups:
                _main  _builtin  group1
  
==Functions and Commands.  Functions and commands have similiar name structure as
  data (group.func,group.cmd). 
  The default group name for functions and commands is _main (functions and commands with
  this group name do not need full name qualification).
  Eg. you can also assign variables variable values with setvar() function:
        tdl> setvar('v', 2.3, group='group1')
        tdl> print group1.v

  The potential advantage here is that 'v' and 'group1' are string types,
  not literal variable names, so they can be computed or passed in a
  procedure. 

==Clean syntax for programming:
  The syntax is "Python Inspired", with some notable exceptions.  Most
  importantly, indentation level is not significant, and blocks end with
  with explicit 'end' statements.  A typical for-block will look like this:

        for i in range(10):
            print i
        endfor     

  There are also while blocks and if-elif-else blocks:
        n = 0
        while n<10: 
           print ' n = ',n
           if n==3: print 'here is 3!!'
               n = n + 1
           endwhile
     
        if n > 10:
            print 'No'
        elif n > 5 and n < 8:
            print 'Maybe'
        else:
            print 'Yep'
        endif

  A design goal is that well-formed tdl code should be very easy to
  translate into valid python (and vice versa).

==User-defined functions (aka procedures):
  User defined functions can be written in tdl:
        def  myfunc(arg1, option='test'):
             'documentation string'
              print 'this is my funcition ', arg1
              print 'optional param = ', option
              if type(option) != 'string':     
                  print 'option must be a string!!'
                  return False
              endif
              value = sqrt(arg1)
              x.tmp = value
              return value > 10.
        enddef

  which could be called as 
        tdl> ret = myfunc(3., option = 'xx')
        tdl> print ret, x.tmp
          False 1.73205080757

==dofile() function:
  you can run a file of tdl commands with the dofile() function:
        tdl> dofile('myfile.tdl')

==eval() function:
  you can construct a tdl expression on the fly from strings and execute it:

        tdl> eval("%s.value = %f" %  ['group', 10.2])
        tdl> print group.value 
          10.2

==read_ascii() function:
  you can read in ASCII column data files very easily.

        tdl> read_ascii('my.dat', group='f')
          ['f', 'x', ''y']
      
  this read 2 columns (labeled 'x' and 'y') from the column file and
  created the array variables f.x and f.y.  Also created was f.titles
  to hold the titles in the data file (non-numeric content at the top of
  the file) and f.column_labels

==On-line help:
  well, this is in progress....

==Easy to add your python functions, including getting access to all  
  the 'data groups' inside your python function.

==Differences between tdl and Python (for python users):
  -  tdl has many builtins and assumes Numerical data. 
  -  tdl has no tuples. Lists are used in their place.
  -  indentation does not matter. blocks are ended with 'end***' 
     (if / endif , for /endfor, def/enddef)
  -  when in doubt, assignment makes a copy, and does not give a reference
  -  data types are NOT objects, and so have no methods.  You must use
     procedural approaches 
       x = arange(100)
       reshape(x,[10,10])   instead of x.shape = (10,10)
"""

HelpStrings = """
  Working with strings:

  strings are sequence of text characters. To specify a string, you enclose it in quotes,
  either single or double quotes:
      tdl>  x = 'this is a string'
      tdl>  x = "A string with a ' in it "

  There are a few special characters that can be included in strings by 'escaping' them with a
  backlash character "\\".  The most important of these are '\\n' to write a newline character,
  and '\\t' to write a tab character.  Other escaped characters are:
      \\n   newline
      \\r   carriage return
      \\f   form feed
      \\v   vertical tab
      \\b   backspace
      \\t   tab
      \\a   bell
      \\"   literal "
      \\'   literal '
      \\\   the backslach character itself.
      
  You can escape quote characters ('\\"' or '\\'') so that they do not mark the end of a
  string sequence: 
      tdl> x = 'a string\\'s string'
      tdl> y = "\\"a string with a double quote\\", he said."

 
  ==Multi-line Strings with Triple Quotes
   
  Tdl allows multi-line strings (that is strings that span lines).  One simple way to do this is
  to include a newline character ('\\n') character in the string, but this is not always sufficient.
  Another way is to use triple quotes (three quotes in a row: either ''' or  \"\"\") to enclose the
  string.  With this approach, the newlines of the enclosed string are preserved:

     tdl> long_string = '''Here is a mult-line string
     ...> line #2
     ...> line #3 of the long string '''

     tdl> print long_string
     Here is a mult-line string
     line #2
     line #3 of the long string

  As with single quote strings, you have the choice of using single or double quotes, and can
  use escaped character and escaped quotes.

  ==String Formatting

  It is often desirable to create strings from program data. To do this, you *format a string*.
  This is done by putting format codes in a string and supplying values to fill in.  Format
  codes use the '%' character to mark the formatting to do.

  Following normal conventions, a formatted string for a floating point number might look like this: 

      tdl> print "x = %8.4f" % sqrt(12)
      x =   3.4641
      
  The "%8.4f" tells the formatting to format a floating point number (the 'f') with 8 total numbers
  and 4 numbers after the decimal point.   A plain '%' is used to separate the format string and the
  value(s) to format.  Other format codes:

      ......
  
  ==Using a dictionary for string formatting

    Borrowing from Python, tdl also allow you to format a string using a dictionary instead of a
    simple list.  This can be a big advantage when formatting many values or formatting data from
    complicated data structures.  In this method, you explicitly set the dictionary key to use by
    naming them between the '%' and the format code:
    
      tdl> data  = {'name':'File 1', 'date':'Monday, April 3, 2006', 'x': 12.4}
      tdl> print " %(name)s , x = %(x)f" % data
      File 1 , x = 12.4
     
"""

HelpDicts = """
  Working with dictionaries:

"""

HelpArrays = """
  Working with arrays:

"""

HelpLists = """
  Working with lists:
  
"""

HelpControl = """
   Help on Programming Control structures (conditionals, loops, etc)

   Program Control structures are important for controlling what parts of
   a program are run.  If you're familiar with other programming languages,
   the concepts and syntax here should be fairly straightforward.

   The basic concept here is to define blocks of code (that is multiple lines
   of code) to be run as a group.  This allows the block of code to be run
   only under some conditions, or to be run repeatedly with different values
   for some variables in the block.
   
   The syntax of tdl uses a colon ':' and a small number of keywords to define
   the blocks of code:
       if x==0:
          print 'cannot divide by zero'
       else:
          x = 2 /x
       endif
   

 = If statements:

   if statements run a block of code only if some condition is met.  Since this
   is so common, there are a few variations allowed in tdl.  First is the
   one line version:

       if x<0:  x = -x

   which will set x to -x (that is, this will make sure x>=0).  In general, the
   if statement looks like:
       if condition:

   where the ending ':' is important (to indicate where the condition end).
   The "condition" is a statement that is evaluated as a boolean value (either
   True or False -- all numeric values are True except 0.0).  The boolean
   operations 'and', 'or' , and 'not' to construct complex conditions:

       if x>0 and x<10:

       if (x>0 and (b>1 or c>1)):


   A warning: in many programming languages multiple conditions can be relied upon
   to only evaluate until the truth of the statement can be determined.  This is NOT
   the case in tdl: the entire statement may be evaluated.

   The second version uses the same 'if condition:', but on a line by itself, followed
   by  multiple statements.  This version ends with 'endif' to indicate how far the 
   block of code extends:
       if x < 0  :
           x = -x
           print ' x set to ',x 
       endif

   Next, there's the 'if-else-endif' version which runs either one block or the
   other, and looks like this (note the 
       if x<0:
           x = -x
           print ' x set to ',x 
       else:
           print ' x was positive to begin with'
       endif

   The final and most complete variation uses 'elif' (pronounced "else if") to allow
   multiple conditions to be tested:
   
       if x<0:
           x = -x
           print ' x set to ',x 
       elif x>10:
           x = 10
           print ' x was too big, set to ', x
       else:
           print ' x was OK to begin with'
       endif

   Multiple 'elif' blocks can be given, though all 'elif' statements must be
   after the 'if' statements, and an 'else' statement (if present) must be last.
   And the entire construct must end with an 'endif'

   In such constructs, the first block with a condition that is True, and no other
   blocks will be run.

 = For loops:

   for loops repeat a block of code, usually incrementing some value used in
   the loop.  Usually, a for loop runs a predictable number of times (see the
   section below on Break and Continue for when it does not!). A for loop
   looks like:
    
       for i in [1,2,3]:
           print i, i*i
       endfor

   The basic syntax for the first line is 'for <variable> in <list>:'  The list
   can be either a real list or a numerical array -- a very common approach is to
   use the range() function to generate a list of numbers:
       for i in range(10):
           print i, 10-i, i*(10-i)
           if i < 2: print ' i < 2!! '
       endfor

   The block is run repeatedly with the loop variable i set to each value in the
   list.

   There is also a 'one-line' version of the for loop:
  
       for i in [1,2,3]: call_some_function(i)
   

 = While loops:

   while loops are similar to for loops, repeatedly running a block of code
   as long as some condition is true:

      x = 1
      while x<4:
         print x
         x = x + 1
      endwhile

   prints
     1.0
     2.0
     3.0

   Beware that a while loop makes it easy to make an "infinite loop" (for example, if
   the value of x had not been increased in the block).
   
 = Break and Continue in For and While loops

   In both for loops and while loops, the block can be exited with a 'break' statement.
   
   
 = Try / Except blocks:

   Sometimes error happen, and it's desirable to run some block of code

       x = 0
       a = 2.
       try:
           y = a/ x
       except:
           print "OK,  that didn't work so well!"
       endtry
      
"""
#  one quote mark: ' to fix emacs colorization
#########################################################
import types, sys
from Util   import show_list, split_arg_str, show_more

class Help:
    """ basic help mechanism for Tdl """

    def __init__(self,tdl=None,output=None):
        h = self.topics = {}
        h['help']  = HelpHelp
        h['show']  = HelpShow
        h['shell_usage'] = ShellUsage
        h['overview'] = Overview
        h['strings'] = HelpStrings
        h['dicts'] =   HelpDicts
        h['arrays'] =  HelpArrays
        h['lists'] =   HelpLists
        h['control'] = HelpControl
        self.list_topics()

        self.tdl = tdl

        if output is not None:
            self.output = output
        else:
            self.output = sys.stdout

    def list_topics(self):
        x = " ".join(self.topics.keys())
        self.help_topics = x.split()
        self.help_topics.sort()

    def add_topic(self,name,text):
        if type(name) != types.StringType:
            name = str(name)
        self.topics[name] = text

    def get_help(self,name):
        if name in self.topics.keys():
            return self.topics[name]
        return "No help available for %s" % (name)

    ###
    def show_function(self,args):
        lout = []
        fcns = self.tdl.symbolTable.listFunctions()
        grps  = fcns.keys()
        
        if len(args)>0:
            g = []
            for i in args:
                if i in grps: g.append(i)
            grps = g
        grps.sort()
        for g in grps:
            flist = fcns[g]
            if len(flist) > 0:
                fout = [f[0] for f in flist]
                lout.append("== Functions in '%s'\n" % (g))
                lout.append("%s\n" % (show_list(fout)))
        lout = "".join(lout)
        show_more(lout,writer=self.output)

    def show_variable(self,args):
        lout = []
        fcns = self.tdl.symbolTable.listVariables()
        grps  = fcns.keys()
        
        if len(args)>0:
            g = []
            for i in args:
                if i in grps: g.append(i)
            grps = g
        grps.sort()
        for g in grps:
            flist = fcns[g]
            if len(flist) > 0:
                fout = [f[0] for f in flist]
                lout.append("== Variables in '%s'\n" % (g))
                lout.append("%s\n" % (show_list(fout)))
        lout = "".join(lout)
        show_more(lout,writer=self.output)


    def show_groups(self,args=None,skip=None):
        " print list of groups"
        x = self.tdl.symbolTable.listGroups()

        if skip is None:  skip = []
        lout = []
        def showGroup(x,prefix='',indent=-1):
            px = '%s %s' % (' '*2*indent,prefix)
            for k,v in x.items():
                nam = "%s%s" % (px,k)
                lout.append(" %s:\n" % nam)
                if len(v)>0:
                    showGroup(v, prefix="%s." % (nam) , indent=indent+1)
        showGroup(x,prefix='',indent=0)
        show_more(lout,writer=self.output)
        
#         print form % (self.tdl.symbolTable.dataGroup,self.tdl.symbolTable.funcGroup)
#         print "   ==Currently defined groups: "
#         show_more(show_list(l,ncol=4),writer=self.output,prefix='   ')

    def show_group(self,args = None):
        " list all contents of a group "
        lout = []
        dat  = self.tdl.symbolTable.listAll()
        grps = dat.keys()
        
        if args is not None:
            args = args.split()
            if len(args)>0:
                g = []
                for i in args:
                    if i in grps: g.append(i)
                grps = g
        grps.sort()
        for g in grps:
            lout.append("== Group '%s'\n" % (g))
            for k in dat[g]:
                lout.append(" %s = %s\n" % k)
        lout = "".join(lout)
        show_more(lout,writer=self.output)

    
    def show(self,argin):
        args = argin.strip().split()
        key = None
        if len(args) > 0:  key = args.pop(0).strip()
        
        if key is None:
            form = "\nDefault Data group = %s\nDefault Func group = %s\n"
            print form % (self.tdl.symbolTable.dataGroup,self.tdl.symbolTable.funcGroup)
            f = self.tdl.symbolTable.listFunctions()
            d = self.tdl.symbolTable.listVariables()
            #for grp in self.tdl.symbolTable.listGroups():
            #    print "\n===Group: %s" % grp
            #    for t,name in ((f,'functions'),(d,'variables')):
            #        n = 0
            #        if t.has_key(grp):  n = len(t[grp])
            #        print "   %i %s " % (n,name)
            txt = {'g':[],'f':[],'v':[]}
            ngrps = 0
            for grp in self.tdl.symbolTable.listGroups():
                txt['g'].append("===Group: %s" % (grp))
                if f.has_key(grp):
                    n = len(f[grp])
                else:
                    n = 0
                txt['f'].append(" %i functions" % (n))
                if d.has_key(grp):
                    n = len(d[grp])
                else:
                    n = 0
                txt['v'].append(" %i variables" % (n))
                ngrps = ngrps +1
            j = 0; k = 0; ncol = 4
            while True:
                t = ''
                for k in range(ncol):
                    if j+k < ngrps:
                        t = "%s %-20s\t" % (t,txt['g'][j+k])
                print t
                t= ''
                for k in range(ncol):
                    if j+k < ngrps:
                        t = "%s %-20s\t" % (t,txt['f'][j+k])
                print t
                t = ''
                for k in range(ncol):
                    if j+k < ngrps:
                        t = "%s %-20s\t" % (t,txt['v'][j+k])
                print t
                print "\n"
                j = j + k + 1
                if j >= ngrps: break
        elif key  in ( '-f', 'functions','function'):
            self.show_function(args)
        elif key  in ( '-v', 'variables','variable'):
            self.show_variable(args)
        elif key in ('-g', 'groups'):
            self.show_groups()
        elif key in ('group') and len(args)>0:
            self.show_group(args[0].strip())
        else:
            args.insert(0,key)
            self.show_symbols(args)

    def help(self,argin):
        args = argin.strip().split()
        key = None
        if len(args) > 0:  key = args.pop(0).strip()
        if key is None:
            print self.topics['help']
        elif key in ('-t','topics'):
            self.list_topics()
            print "\n==Additional help is avaiable on the following topics:\n"
            print  show_list(self.help_topics, ncol = 5)
            print ""
        elif key in self.help_topics:
            show_more(self.get_help(key),writer=self.output)
        else:
            args.insert(0,key)
            self.show_symbols(args,msg='help')
    
    def show_symbols(self,args,msg='show'):
        for key in args:
            if key.endswith(','): key=key[:-1]
            key.strip()
            if len(key)>0:
                if self.tdl.symbolTable.hasGroup(key):
                    self.show_group(key)
                elif self.tdl.symbolTable.getFunction(key):
                    self.show_function([key])
                elif self.tdl.symbolTable.getVariable(key):
                    self.show_variable([key])
                elif msg == 'show':
                    print "  Cannot find '%s' (try 'help show' or 'show groups')" % key
                else:
                    print "  No help on '%s'.  Try 'help' or 'help topics'" % key