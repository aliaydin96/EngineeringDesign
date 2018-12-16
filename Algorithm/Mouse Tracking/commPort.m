clc;
clear all;
delete(instrfind());

comPort = serial('COM7','BaudRate',9600);
if (~strcmp(comPort.ByteOrder,'littleEndian'))
    set(comPort, 'ByteOrder','littleEndian','Parity','even',...
        'ReadAsyncMode', 'continuous');   
    switch (comPort.Terminator)
       case 'HF'
          set(comPort, 'Terminator','LF');
       case 'LF'
          set(comPort, 'Terminator','HF');
    end
end