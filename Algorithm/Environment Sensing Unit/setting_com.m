clear;
clc;
%setting commication port object
comPort = serial('COM11','BaudRate',115200);
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
% if(strcmp(comPort.Status,'closed'))
%     fopen(comPort);
% end
% if(strcmp(comPort.Status,'closed'))
%     fprintf('The port cannot be opened. The device is not connected properly');
% end