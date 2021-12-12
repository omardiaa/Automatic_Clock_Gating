import pyverilog.vparser.ast as vast
from pyverilog.vparser.parser import parse
from pyverilog.ast_code_generator.codegen import ASTCodeGenerator
import sys
from pprint import pprint

def parseFile(fileName): 
    return parse(fileName) 

def createCG(clk, en, output): 
    clkgateArgs = [
    vast.PortArg("GCLK", vast.Identifier(output)),
    vast.PortArg("GATE", vast.Identifier(en)),
    vast.PortArg("CLK", vast.Identifier(clk))
    ]

    cG = vast.Instance("sky130_fd_sc_hd__dlclkp","__clockgate_cell__", tuple(clkgateArgs), tuple())

    return cG

def reachEnd(ter, definition, outputPort, selectionLine, inputPort, inputComp):
    f = open("log", "a")
    if ter==0:
        quit()
    ter-=1
    for itemDeclaration in definition.items:
        if type(itemDeclaration).__name__ == "InstanceList":
            instance = itemDeclaration.instances[0]
            for port in instance.portlist:
                #print("Name {} Module {} port {} arg {}".format(instance.name, instance.module,port.portname,port.argname))
                          
                if(str(instance.name)!=inputComp and str(port.argname)==inputPort ):
                    for port2 in instance.portlist:
                        if(port2.argname!=port.argname and (str(port2.portname)=="X" or str(port2.portname)!="Y") ):
                            b = False
                            if  str(port2.argname)==outputPort or str(port2.argname)==selectionLine:
                                print("Base case reached")
                                # return
                            elif str(port2.argname)[0] == "<":

                                print("Base case reached 2")
                                break
                            else:
                                print("Name {} Module {} port {} arg {}".format(instance.name, instance.module,port2.portname,port2.argname))
                                reachEnd(ter, definition, outputPort, selectionLine, str(port2.argname), str(instance.name))


def reachEnd2(definition, inputPort, selectionLine, outputPort, inputComp):
    
    for itemDeclaration in definition.items:
        if type(itemDeclaration).__name__ == "InstanceList":
            instance = itemDeclaration.instances[0]
            
            for port in instance.portlist:
                arg = str(port.argname)
                if(hasattr(port.argname,"ptr")):
                    arg=str(port.argname.var)+str(port.argname.ptr)

                # print(str(port.argname)==outputPort )
                if(str(instance.name)!=inputComp and arg==outputPort ):
                    print("0. Name {} Module {} port {} arg {}".format(instance.name, instance.module,port.portname,arg))
       
                    for port2 in instance.portlist:
                        arg2 = str(port2.argname)
                        if(hasattr(port2.argname,"ptr")):
                            arg2=str(port2.argname.var)+str(port2.argname.ptr)

                        if(str(port2.portname)=="X" or str(port2.portname)=="Y"):
                            if(arg2==outputPort):
                                print("1. Name {} Module {} port {} arg {}".format(instance.name, instance.module,port2.portname,arg2))
       
                                print("base case reached!")
                                break
                            else:
                                print("2. Name {} Module {} port {} arg {}".format(instance.name, instance.module,port2.portname,arg2))
       
                                reachEnd2(definition, inputPort, selectionLine, arg2, str(instance.name))

def main(): 

    f = "test1.gl.v"
    ast,_= parse([f]) #root node of the abstract syntax tree  
    description = ast.description  #moduleDef node 
    definition = description.definitions[0]

    newrtl =[] 
    # print(definition.items)
    # for name, m in definition.items():
    #     description = vast.Description((m,))
    #     source = vast.Source('', description)
    #     print(m)

    # for itemDeclaration in definition.items:
    #     item_type = type(itemDeclaration).__name__
    #     if item_type == "Decl":
    #         # print(itemDeclaration.Identifier)
    #         newrtl.append(itemDeclaration)
           

    # reachEnd(5, definition,"r[3]","s","_03_","_41_")
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
                        reachEnd2(definition,dIn,"s",str(port.argname.var)+str(port.argname.ptr),instance.name)
                    else:
                        reachEnd2(definition,dIn,"s",str(port.argname),instance.name)

#   str(port.argname.var)+str(port.argname.ptr)

    # for itemDeclaration in definition.items:
    #     item_type = type(itemDeclaration).__name__
    #     append = True
    #     if item_type == "InstanceList":
    #         instance = itemDeclaration.instances[0]
    #         inputD = ""
    #         outputQ = ""
    #         clk = ""
    #         if(instance.module == "sky130_fd_sc_hd__mux2_1" or instance.module ==  "sky130_fd_sc_hd__a21oi_1" or instance.module == "sky130_fd_sc_hd__a21oi_2"):
    #             append = False
    #             #don't append mux
    #         else:
    #             append = True

    #         if(instance.module == "sky130_fd_sc_hd__dfxtp_1"):
                
    #             for getPort in instance.portlist:
    #                 if(getPort.portname == "D"):
    #                     inputD = getPort.argname
    #                 elif(getPort.portname == "Q"):
    #                     outputQ = getPort.argname
    #                 elif(getPort.portname == "CLK"):
    #                     clk = getPort.argname
    #             # print("Q: {} D:{}".format(inputD, outputQ))
    #             muxIn=""
    #             en=""
    #             for itemDeclaration2 in definition.items:
    #                 item_type2 = type(itemDeclaration2).__name__
    #                 if item_type2 == "InstanceList":
    #                     instance2 = itemDeclaration2.instances[0]
    #                     if(instance2.module == "sky130_fd_sc_hd__mux2_1" or instance2.module ==  "sky130_fd_sc_hd__a21oi_1" or instance2.module == "sky130_fd_sc_hd__a21oi_2"):
    #                         for portout in instance2.portlist:
    #                             if(portout.argname == inputD):
    #                                 for getPort in instance2.portlist:
    #                                     if(getPort.portname=="S"):
    #                                         en=getPort.argname
    #                                     elif(getPort.portname =="A0" and getPort.argname != outputQ):
    #                                         muxIn = getPort.argname
    #                                     elif(getPort.portname =="A1" and getPort.argname != outputQ):
    #                                         muxIn = getPort.argname
    #                                 print("Module: {} - {} Mux Input: {} Enabler: {} clk: {} input D: {}".format(instance.module, instance.name,muxIn, en, clk, inputD))

                                    
    #                                 #newrtl.append(createCG(str(clk), str(en)))
    #                                 #clkgateArgs = [vast.PortArg("GCLK", vast.Identifier("__clockgate_output_gclk_")),vast.PortArg("GATE", vast.Identifier(str(en))),vast.PortArg("CLK", vast.Identifier(str(clk)))]
    #                                 #clkgate_cell = vast.Instance("sky130_fd_sc_hd__dlclkp","__clockgate_cell__",tuple(clkgateArgs),tuple())
    #                                 newrtl.append(vast.InstanceList("sky130_fd_sc_hd__dlclkp", tuple(), tuple([createCG(str(clk), str(en), str(inputD))])))
                

    #             for getPort in instance.portlist:
    #                 if(getPort.portname == "D"):
    #                     getPort.argname = muxIn
    #                 elif(getPort.portname == "CLK"):
    #                     getPort.argname = inputD
    #                    #update flipflop input to the old input of the mux [the input which was not connected to the output]
                
    #             if append:
    #                 newrtl.append(itemDeclaration)



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


    # definition.items = tuple(newrtl)
    # codegen = ASTCodeGenerator()
    # rslt = codegen.visit(ast)
    # f = open("testUpdated4.v", "w+")
    # f.write(rslt)
    # f.close()                         
          
           
main()