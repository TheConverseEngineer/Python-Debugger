import sys

TargetFunc = None
class Debug:    #The debug class
    global TargetFunc

    def __init__(self, frame, event, arg):
        assert event == "call"  # assert that it is a call
        #identify call name, first line, filename
        self.FuncName = frame.f_code.co_name
        self.FirstLine = frame.f_code.co_firstlineno
        self.FileName = frame.f_code.co_filename
        self.Vars = {}
        if TargetFunc == self.FuncName: self.co = ""
        else: self.co = "co-function "
        print('\n')
        print('Debugging Function:', self.co + self.FuncName, '\n' + 'Located at:', self.FileName, '\n' + 'Starting on Line:', self.FirstLine + 1)


    #Find local line based on function
    def Head(self, frame, end, cont = ""):
        if end: return str('Line '+ str(frame.f_lineno - self.FirstLine + 1) + cont + ' (Programe Line ' + str(frame.f_lineno + 1) + '):') #last line
        else: return str('Line '+ str(frame.f_lineno - self.FirstLine) + ' (Programe Line ' + str(frame.f_lineno) + '):')
        

    #break up a dictionary into something easier to understand
    def Break(self, Type, dictionary):
        ret = ''
        if len(dictionary) > 0: # if it actually exists
            j = 0
            for i in dictionary.keys():
                if j != 0: #if i is not the first key
                    ret = str(str(ret) + '; ')
                ret = str(str(ret) + str(i) + ' has been ' + str(Type) + ' with a value of ' + str(dictionary.get(i)))
                j += 1
        return ret
    
    #tracer gets *called* by the interpreter
    def __call__(self, frame, event, arg):
        if event == "line":
            self.TraceVar(frame, event, arg, False)
            
        elif event in ("return", "exception"):
            self.TraceVar(frame, event, arg, True)
            self.trace_exit(frame, event, arg)
        else:
            raise RuntimeError("Invalid event: %r" % event)

    def TraceVar(self, frame, event, arg, end):
        NewVars = {}
        ChangedVars = {}
        for name, value in frame.f_locals.items(): # get the name and value of the variables
            if not name in self.Vars: #if the variable has not been added to the dictionary yet
                self.Vars[name] = value
                NewVars[name] = value
            elif self.Vars.get(name) != value: #if the variable has changed
                ChangedVars[name] = value
        #print results
        if (len(NewVars) != 0 or len(ChangedVars) != 0): #if something happened
                if len(ChangedVars) == 0: # If only new variables are added
                    print(self.Head(frame, end), self.Break('added', NewVars))
                elif len(NewVars) == 0: # If only changes to variables are made
                    print(self.Head(frame, end), self.Break('changed', ChangedVars))
                else: #if both new vars are added and pre-existing vars are changes
                    print(self.Head(frame, end), self.Break('added', NewVars), '\n' + self.Head(frame, end, cont='(cont.)'), self.Break('changed', ChangedVars))
        else: print(self.Head(frame, end), 'No variables were added or changed')
                

    def trace_exit(self, frame, event, arg):
        """Report the current trace on exit"""
        print('Exiting', self.co+self.FuncName)
        print('The final variable values for', self.co + self.FuncName, 'are:', self.Vars)
        print('\n')


#Test Functions
def Test1():
    a, c = 1, 2
    b = 2
    a, b = 3, 5

def Test2():
    a, b = 1, 2
    a, c = 5, 3

def Test3():
    a , b = 2, 3
    c = foo(a, b)

def foo(a, b):
    c = a*b
    return c
#run
print('Python Debugger - TheConverseEngineer')
opt = None
cmd = None
#while opt == None:
#    ipt = input('Please choose either [a]Run a custom function or [b]run a pre-made function:').lower()
 #   if ipt == 'a' or ipt == 'b': opt = ipt
  #  else: print('please input either "a" or "b"')
#    
#if (opt == 'a'):
    #pass #run a custom function

if (15 == 15): #run a example function
    print('Please select a test function to run from the list: {1: Test1, 2: Test2, 3: Test3}')
    print('Too learn more about a function, put a "h" in front of your choice')
    
    while cmd == None:
        ipt2 = input()
        
        if ipt2 in ['1', '2', '3', 'h1', 'h2', 'h3']:
            
            if ipt2 in ['h1', 'h2', 'h3']: #if it is a help
                
                if ipt2 == 'h1':
                    print('Test1 highlights: Contains 3 variables, two are declared on the same line, two are changed on the same line')

                if ipt2 == 'h2':
                    print('Test2 highlights: Contains 3 variables, two are declared on the same line, one is changed and one is declared  on the same line')

                if ipt2 == 'h3':
                    print('Test3 highlights: Contains 3 variables, two are declared on the same line, contains subfunction')

            else: #run a program
                cmd = str('Test'+ipt2)
        else:
            print('Please enter a valid option: [1, 2, 3, h1, h2, h3]')
                    
if cmd == 'Test1':
    TargetFunc = 'Test1'
    sys.settrace(Debug) 
    Test1()
    sys.settrace(None)
    
if cmd == 'Test2':
    TargetFunc = 'Test2'
    sys.settrace(Debug) 
    Test2()
    sys.settrace(None)

if cmd == 'Test3':
    TargetFunc = 'Test3'
    sys.settrace(Debug) 
    Test3()
    sys.settrace(None)
