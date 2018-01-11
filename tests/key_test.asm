INT 22                                                                                                                                               
MOV EBX,EAX                                                                                                                                          
MOV ECX,0                                                                                                                                            
MOV ESI,0                                                                                                                                            
                                                                                                                                                     
L1: MOV [ESI],EAX                                                                                                                                    
MOV EAX, 0
INT 22                                                                                                                                               
INC ECX                                                                                                                                              
CMP EBX,EAX                                                                                                                                          
INC ESI                                                                                                                                              
JNE L1                                                                                                                                               
                                                                                                                                                     
L2: MOV EAX, 0
INT 22                                                                                                                                           
DEC ECX                                                                                                                                              
CMP ECX,1                                                                                                                                            
JNE L2                                                                                                                                               
                                                                                                                                                     
MOV EAX, 0
INT 22                                                                                                                                               
MOV EBX,EAX                                                                                                                                          
                                                                                                                                                     
L3:MOV [ESI],EAX                                                                                                                                     
INC ESI                                                                                                                                              
MOV EAX, 0
INT 22                                                                                                                                               
CMP EBX,EAX                                                                                                                                          
JNE L3                                                                                                                                               
                                                                                                                                                     
                                                                                                                                                     
;GIRONAGIRONAGETSGETS   
