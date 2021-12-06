import pyverilog.vparser.ast as vast
from pyverilog.vparser.parser import parse
from pyverilog.ast_code_generator.codegen import ASTCodeGenerator
import sys

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


def main(): 

    f = "test2.gl.v"
    ast,_= parse([f]) #root node of the abstract syntax tree  
    description = ast.description  #moduleDef node 
    definition = description.definitions[0]

    newrtl =[] 


  
    for itemDeclaration in definition.items:
        item_type = type(itemDeclaration).__name__
        append = True
        if item_type == "InstanceList":
            instance = itemDeclaration.instances[0]
            inputD = ""
            outputQ = ""
            clk = ""
            if(instance.module == "sky130_fd_sc_hd__mux2_1" or instance.module ==  "sky130_fd_sc_hd__a21oi_1" or instance.module == "sky130_fd_sc_hd__a21oi_2"):
                append = False
                #don't append mux
            else:
                append = True

            if(instance.module == "sky130_fd_sc_hd__dfxtp_1"):
                
                for getPort in instance.portlist:
                    if(getPort.portname == "D"):
                        inputD = getPort.argname
                    elif(getPort.portname == "Q"):
                        outputQ = getPort.argname
                    elif(getPort.portname == "CLK"):
                        clk = getPort.argname
                # print("Q: {} D:{}".format(inputD, outputQ))
                muxIn=""
                en=""
                for itemDeclaration2 in definition.items:
                    item_type2 = type(itemDeclaration2).__name__
                    if item_type2 == "InstanceList":
                        instance2 = itemDeclaration2.instances[0]
                        if(instance2.module == "sky130_fd_sc_hd__mux2_1" or instance2.module ==  "sky130_fd_sc_hd__a21oi_1" or instance2.module == "sky130_fd_sc_hd__a21oi_2"):
                            for portout in instance2.portlist:
                                if(portout.argname == inputD):
                                    for getPort in instance2.portlist:
                                        if(getPort.portname=="S"):
                                            en=getPort.argname
                                        elif(getPort.portname =="A0" and getPort.argname != outputQ):
                                            muxIn = getPort.argname
                                        elif(getPort.portname =="A1" and getPort.argname != outputQ):
                                            muxIn = getPort.argname
                                    print("Module: {} - {} Mux Input: {} Enabler: {} clk: {} input D: {}".format(instance.module, instance.name,muxIn, en, clk, inputD))

                                    
                                    #newrtl.append(createCG(str(clk), str(en)))
                                    #clkgateArgs = [vast.PortArg("GCLK", vast.Identifier("__clockgate_output_gclk_")),vast.PortArg("GATE", vast.Identifier(str(en))),vast.PortArg("CLK", vast.Identifier(str(clk)))]
                                    #clkgate_cell = vast.Instance("sky130_fd_sc_hd__dlclkp","__clockgate_cell__",tuple(clkgateArgs),tuple())
                                    newrtl.append(vast.InstanceList("sky130_fd_sc_hd__dlclkp", tuple(), tuple([createCG(str(clk), str(en), str(inputD))])))
                

                for getPort in instance.portlist:
                    if(getPort.portname == "D"):
                        getPort.argname = muxIn
                    elif(getPort.portname == "CLK"):
                        getPort.argname = inputD
                       #update flipflop input to the old input of the mux [the input which was not connected to the output]
                
                if append:
                    newrtl.append(itemDeclaration)



    for itemDeclaration in newrtl:
        item_type = type(itemDeclaration).__name__
        if item_type == "InstanceList":
            instance = itemDeclaration.instances[0]
            
            print(instance.module)
            for getPort in instance.portlist: 
                print("Port name: ") 
                print(getPort.portname)
                print("Arg name: ") 
                print(getPort.argname)


    definition.items = tuple(newrtl)
    codegen = ASTCodeGenerator()
    rslt = codegen.visit(ast)
    f = open("testUpdated4.v", "w+")
    f.write(rslt)
    f.close()                         
          
           
main()

