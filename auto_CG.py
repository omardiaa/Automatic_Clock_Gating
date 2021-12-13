import pyverilog.vparser.ast as vast
from pyverilog.vparser.parser import parse
from pyverilog.ast_code_generator.codegen import ASTCodeGenerator
import sys
from pprint import pprint

to_exclude = []
to_exclude1 = []
wires = []
counter = 0

class groups:
    ff = ""
    selection = ""
    inp = ""

def parseFile(fileName): 
    return parse(fileName) 

def createCG(clk, en, output): 
    clkgateArgs = [
    vast.PortArg("GCLK", vast.Identifier(output)),
    vast.PortArg("GATE", vast.Identifier(en)),
    vast.PortArg("CLK", vast.Identifier(clk))
    ]

    cG = vast.Instance("sky130_fd_sc_hd__dlclkp_1","_"+str(counter), tuple(clkgateArgs), tuple())

    return cG

def reachEnd2(definition,dff, inputPort, selectionLines, outputPort, inputComp):
    
    global to_exclude
    global to_exclude1
    for itemDeclaration in definition.items:
        if type(itemDeclaration).__name__ == "InstanceList":
            instance = itemDeclaration.instances[0]
            
            for port in instance.portlist:
                arg = str(port.argname)
                if(hasattr(port.argname,"ptr")):
                    arg=str(port.argname.var)+str(port.argname.ptr)

                # print(str(port.argname)==outputPort )
                # for curSel in selectionLines:
                #     if arg == curSel:
                #         print("Selection {} ".format(port.argname))

                if(str(instance.name)!=inputComp and arg==outputPort ):
                    gg = groups()
                    global wires
                    flag = 0
                    print("0. Name {} Module {} port {} arg {}".format(instance.name, instance.module,port.portname,arg))
                    gg.ff=dff
                    if(str(instance.name) != dff):
                        to_exclude1.append(instance.name)
                    else:
                        #Instance name == flip flop
                       
                        wires.append(arg)

                       
                        
                    #group.append(instance.name)
                    # group.append(instance.module)
                    
                    for port2 in instance.portlist:
                        arg2 = str(port2.argname)
                        if(hasattr(port2.argname,"ptr")):
                            arg2=str(port2.argname.var)+str(port2.argname.ptr)
                        if(str(port2.portname)!="X" and str(port2.portname)!="Y" and arg2!=outputPort and arg2!="clk" and instance.name!=dff):            
                            b=True                            
                            for curSel in selectionLines:
                                if arg2 == curSel:
                                    
                                    print("Selection: {}".format(arg2))
                                    gg.selection=arg2
                                    b=False
                                    
                            if b:
                                flag = 1
                                print("Input: {}".format(arg2))
                                gg.inp=arg2
                                to_exclude.append(gg)
                            
                            
                    for port2 in instance.portlist:
                        arg2 = str(port2.argname)
                        if(hasattr(port2.argname,"ptr")):
                            arg2=str(port2.argname.var)+str(port2.argname.ptr)

                        if(str(port2.portname)=="X" or str(port2.portname)=="Y"):
                            if(arg2==outputPort):
                                # print("1. Name {} Module {} port {} arg {}".format(instance.name, instance.module,port2.portname,arg2))
       
                                print("base case reached!")
                                break
                            else:
                                # print("2. Name {} Module {} port {} arg {}".format(instance.name, instance.module,port2.portname,arg2))
       
                                reachEnd2(definition,dff, inputPort, selectionLines, arg2, str(instance.name))

def main(): 

    f = "test2.gl.v"
    ast,_= parse([f]) #root node of the abstract syntax tree  
    description = ast.description  #moduleDef node 
    definition = description.definitions[0]
    global to_exclude
    global counter
    newrtl =[] 
    # print(definition.items)

    for itemDeclaration in definition.items:
        item_type = type(itemDeclaration).__name__
        if item_type == "Decl":
            # print(itemDeclaration.Identifier)
            newrtl.append(itemDeclaration)
           

    # reachEnd(5, definition,"r[3]","s","_03_","_41_")
    selectionLines = ["s","ld1","ld2"]
    for itemDeclaration in definition.items:
        if type(itemDeclaration).__name__ == "InstanceList":
            instance = itemDeclaration.instances[0]
            dIn=""
            for port in instance.portlist:
                if str(instance.module) == "sky130_fd_sc_hd__dfxtp_1" and port.portname=="D":
                    dIn = port.argname
            for port in instance.portlist:
                if str(instance.module) == "sky130_fd_sc_hd__dfxtp_1" and port.portname=="Q":
                    print(port.argname)
                    if(hasattr(port.argname,"ptr")):
                        reachEnd2(definition,instance.name,dIn,selectionLines,str(port.argname.var)+str(port.argname.ptr),instance.name)
                    else:
                        reachEnd2(definition,instance.name,dIn,selectionLines,str(port.argname),instance.name)

    print(to_exclude)

    print(to_exclude1)

    print(wires)

    for itemDeclaration in definition.items:
        item_type = type(itemDeclaration).__name__
        append = True
        if item_type == "InstanceList":
            instance = itemDeclaration.instances[0]
           
            b=True
            for ex in to_exclude1:
                if(ex==instance.name):
                    b=False
            if b:
                b2 = True
                for ex2 in to_exclude:#Flip Flops
                    # print("In: {} Ex: {}".format(instance.name,ex2))
                    if str(instance.name) == ex2.ff:
                        b2 = False
                if(b2):
                    print(instance.module)
                    newrtl.append(itemDeclaration)
            
            for ex in to_exclude:#Flip Flops
                
                if str(instance.name) == ex.ff:
                    newrtl.append(vast.InstanceList("sky130_fd_sc_hd__dlclkp_1", tuple(), tuple([createCG("clk", str(ex.selection), str(wires[counter]))])))     
                    for getPort in instance.portlist:
                        if(str(getPort.portname) == "D"):
                            print()
                            getPort.argname.name = ex.inp
                        elif(str(getPort.portname) == "CLK"):
                            getPort.argname.name = str(wires[counter])
                            print()
                    newrtl.append(itemDeclaration)
                    counter+=1 

    # for itemDeclaration in newrtl:
    #     item_type = type(itemDeclaration).__name__
    #     if item_type == "InstanceList":
    #         instance = itemDeclaration.instances[0]
            
    #         print(instance.module)
    #         for getPort in instance.portlist: 
    #             print("Port name: ") 
    #             print(getPort.portname)
    #             print("Arg name: ") 
    #             print(getPort.argname)


    definition.items = tuple(newrtl)
    codegen = ASTCodeGenerator()
    rslt = codegen.visit(ast)
    f = open("testUpdated5.v", "w+")
    f.write(rslt)
    f.close()                         
          
           
main()