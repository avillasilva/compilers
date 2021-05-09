class Stack :
  def __init__(self) :
    self.items = []

  def push(self, item) :
    self.items.append(item)

  def pop(self) :
    return self.items.pop()

  def isEmpty(self) :
    return (self.items == [])

  def containsInScope(self, token) :
      size = self.items.__len__()
      for item in reversed(self.items) :
            if item == '$' :
              return False
            elif item == token:
                return True

  def contains(self, token) :
      return self.items.__contains__(token)

  def changeScope(self) :
      while(self.pop() != '$') :
          continue

  def checkDeclaration(self, token) :
    if(not self.containsInScope(token)) :
        self.push(token)
    else :
        self.semanticError(token, 'is already declared', )

  def semanticError(self, received, message):
    print('Error: ' + received + '  ' + message)

class SyntaxAndSemanticAnalyzer:
    def __init__(self, input):
        self.reader = open(input, 'r')
        self.index = 0
        self.buffer = None
        self.pile = Stack()

    def next(self):
        self.buffer = self.reader.readline().replace('\n', '').split()
        if not self.buffer:
            self.reader.close()
            return
    
    def analyse(self):
        self.next()
        self.program()

    def error(self, received, expected, line):
        print('Error: received ' + received + ', expected: ' + expected + ' in line: ' + line)
    
    
    def program(self):
        if self.buffer[0] == 'program':
            self.pile.push('$')
            self.next()

            if self.buffer[1] == 'identifier':
                self.pile.checkDeclaration(self.buffer[0])
                self.next()
            
                if self.buffer[0] == ';':
                    self.next()
                    self.var_declarations()
                    self.subprograms_declarations()
                    self.compound_cmd()
            
                    print(self.pile.items)  
                    if self.buffer[0] == '.':
                        return
                    else:    
                        self.error(self.buffer[0], '.', self.buffer[2])                  
                else:
                    self.error(self.buffer[0], ';', self.buffer[2])
            else:
                self.error(self.buffer[1], 'identifier', self.buffer[2])
        else:
            self.error(self.buffer[0], 'program declaration', self.buffer[2])
    
    def var_declarations(self):
        if self.buffer[0] == 'var':
            self.next()
            self.list_var_dec1()
        else:
            self.error(self.buffer[0], 'var, procedure, compound command declaration', self.buffer[2])
    
    def list_var_dec1(self):
        self.list_identifiers1()
        if self.buffer[0] == ':':
            self.next()
            self.type()
            if self.buffer[0] == ';':
                self.next()
            else:
                self.error(self.buffer[0], ';', self.buffer[2])
        else:
            self.error(self.buffer[0],':', self.buffer[2])

        if self.buffer[1] == 'identifier':    
            self.list_var_dec2()

    def list_var_dec2(self):
        self.list_identifiers1()
        if self.buffer[0] == ':':
            self.next()
            self.type()
            if self.buffer[0] == ';':
                self.next()
            else:
                self.error(self.buffer[0], ';', self.buffer[2])
        else:
            self.error(self.buffer[0],':', self.buffer[2])
        if self.buffer[1] == 'identifier':
            self.list_var_dec2()
        else:
            return
        
    def list_identifiers1(self):
        if self.buffer[1] == 'identifier':
            self.pile.checkDeclaration(self.buffer[0])
            self.next()
            if self.buffer[0] == ',':
                self.list_identifiers2()
        else:
            self.error(self.buffer[2], 'identifier', self.buffer[2])
    
    def list_identifiers2(self):
        
        if self.buffer[0] != '':
            if self.buffer[0] == ',':
                self.next()
                if self.buffer[1] == 'identifier':
                    self.pile.checkDeclaration(self.buffer[0])
                    self.next()
                else:
                    self.error(self.buffer[0], 'identifier', self.buffer[2])
                    return
            else:
                return
        self.list_identifiers2()

            
    def type(self):
        if self.buffer[0] in ['integer', 'real', 'boolean']:
            return self.next()
        else:
            self.error(self.buffer[0], 'integer, real or boolean', self.buffer[2])
    
    def subprograms_declarations(self):
        if self.buffer[0] == 'procedure':            
            self.subprog_declaration()
        else:
            return


    def subprog_declaration(self):
        if self.buffer[0] == 'procedure':            
            self.next()
            if self.buffer[1] == 'identifier':
                self.pile.checkDeclaration(self.buffer[0])
                self.pile.push('$')
                self.next()
                self.arguments()
                if self.buffer[0] == ';':
                    self.next()
                    self.var_declarations()
                    self.subprograms_declarations()
                    self.compound_cmd()
                    if self.buffer[0] != ';':
                        self.error(self.buffer[0], ';', self.buffer[2])
                    self.next()                                   
                else:
                    self.error(self.buffer,';', self.buffer[2])
            else:
                self.error(self.buffer[1], 'identifier', self.buffer[2]) 
            self.subprog_declaration()           
        else:            
            return        
                        
    def arguments(self):
        if self.buffer[0] == '(':
            self.next()
            self.list_param1()
            if self.buffer[0] == ')':
                self.next()
            else:
                self.error(self.buffer[0], ')', self.buffer[2])
        else:
            return

    def list_param1(self):
        self.list_identifiers1()
        if self.buffer[0] == ':':
            self.next()
            self.type()
            if self.buffer[0] == ';':
                self.list_param2()
            else:
                return
        else:
            self.error(self.buffer[0], ':', self.buffer[2])
        

    def list_param2(self):
        if self.buffer[0] == ';':
            self.next()
            self.list_identifiers1()
            if self.buffer[0] == ':':
                self.next()
                self.type
            else:
                self.error(self.buffer[0], ':', self.buffer[2])
        else:
            return
        self.list_param2()

    def compound_cmd(self):
        if self.buffer[0] == 'begin':
            self.next()
            self.optional_cmd()
            if self.buffer[0] != 'end':
                self.error(self.buffer[0], 'end', self.buffer[2])
            self.pile.changeScope()
        else:
            self.error(self.buffer[0],'begin', self.buffer[2])        
        self.next()

    def optional_cmd(self):
        self.list_cmd1()        

    def list_cmd1(self):
        self.cmd()
        if self.buffer[0] == ';':
            self.list_cmd2()

    def list_cmd2(self):
        if self.buffer[0] == ';':
            self.next()
            self.cmd()
        else:
            return
        self.list_cmd2()

    def cmd(self):
        if self.buffer[1] == 'identifier':
            if not self.pile.containsInScope(self.buffer[0]) or not self.pile.contains(self.buffer[0]):
                self.pile.semanticError(self.buffer[0], 'var not found')
            self.next()
            if self.buffer[0] == ':=':
                self.next()
                self.expr()
            elif self.buffer[0] == '(':
                self.procedure_activation()
        elif self.buffer[0] == 'begin':
            self.compound_cmd()
        elif self.buffer[0] == 'if':
            self.next()
            self.expr()
            if self.buffer[0] == 'then':
                self.next()
                self.cmd()
                self.else_part()
            else:
                self.error(self.buffer[0],'then', self.buffer[2])
        elif self.buffer[0] == 'while':
            self.next()
            self.expr()
            if self.buffer[0] == 'do':
                self.next()
                self.cmd()
            else:
                self.error(self.buffer[0],'do', self.buffer[2])

    def else_part(self):
        if self.buffer[0] == 'else':
            self.next()
            self.cmd()
            
    def procedure_activation(self):
        if self.buffer[0] == '(':
            self.next()
            self.list_expr1()
            if self.buffer[0] != ')':
                self.error(self.buffer[0],')', self.buffer[2])
            else:
                self.next()

    def list_expr1(self):
        self.expr()
        if self.buffer[0] == ',':
            self.list_expr2()

    def list_expr2(self):
        if self.buffer[0] == ',':
            self.next()
            self.expr()
        self.list_expr2()

    def expr(self):
        self.simple_expr1()
        if self.buffer[0] in ['=','<','>','<=','>=','<>']:
            self.relational_op()
            self.simple_expr1()
    
    def simple_expr1(self):
        if self.buffer[1] in ['identifier','integer','real','boolean'] or self.buffer[0] in ['(','not']:
            self.term1()
        elif self.buffer[0] in ['+','-']:
            self.next()
            self.signal()
            self.term1()
        
        self.simple_expr2()
    
    def simple_expr2(self):
        if self.buffer[0] in ['+','-','or']:
            self.next()
            self.term1()
            self.simple_expr2()

    def term1(self):
        if self.buffer[1] in ['identifier','integer','real','boolean']:
            self.factor()
            if self.buffer[0] in ['*','/','and']:
                self.term2()

    def term2(self):
        if self.buffer[0] in ['*','/','and']:
            self.next()
            self.factor()
        else:
            return
        self.term2()

    def factor(self):
        if self.buffer[1] == 'identifier':
            if not self.pile.containsInScope(self.buffer[0]) or not self.pile.contains(self.buffer[0]):
                self.pile.semanticError(self.buffer[0], 'var not found')
            self.next()
            if self.buffer[0] == '(':
                self.next()
                self.list_expr1()
                if self.buffer[0] != ')':
                    self.error(self.buffer[0],')', self.buffer[2])
            else: 
                return
        elif self.buffer[1] in ['integer','real','boolean']:
            return self.next()
        elif self.buffer[0] == '(':
            self.next()
            self.expr()
            if self.buffer[0] != ')':
                self.error(self.buffer[0],')', self.buffer[2])
        elif self.buffer[0] == 'not':
            self.next()
            self.factor()
    
    def signal(self):
        if self.buffer[0] in ['+','-']:
            return self.next()
        else:
            self.error(self.buffer[0],'+ , -', self.buffer[2])
    
    def relational_op(self):
        if self.buffer[0] in ['=','<','>','<=','>=','<>']:
            return self.next()
        else:
            self.error(self.buffer[0],'=,<,>,<=,>=,<>', self.buffer[2])

    def add_op(self):
        if self.buffer[0] in ['+','-','or']:
            return self.next()
        else:
            self.error(self.buffer[0],'+,-,or', self.buffer[2])

    def mul_op(self):
        if self.buffer[0] in ['*','/','and']:
            return self.next()
        else:
            self.error(self.buffer[0],'*,/,and', self.buffer[2])



sa = SyntaxAndSemanticAnalyzer('output/output.txt')
sa.analyse()