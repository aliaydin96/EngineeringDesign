delete(instrfind());
clear all;
clc;

% %setting commication port object
% %change the port COM11
comPort = serial('COM7','BaudRate',115200);
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
% % if(strcmp(comPort.Status,'closed'))
% %     fopen(comPort);
% % end
% % if(strcmp(comPort.Status,'closed'))
% %     fprintf('The port cannot be opened. The device is not connected properly');
% end
%% scanning the serial port and visualization
fopen(comPort);
intended_data_size = 90;
dx_1 = zeros(1,intended_data_size);
dy_1 = zeros(1,intended_data_size);
dx_2 = zeros(1,intended_data_size);
dy_2 = zeros(1,intended_data_size);
dx_1_dummy = 0;
dy_1_dummy = 0;
for index = 1:intended_data_size
    dx_1(1,index) = fscanf(comPort,'%d');
    dy_1(1,index) = (fscanf(comPort,'%d'));
    dx_2(1,index) = fscanf(comPort,'%d');
    dy_2(1,index) = (fscanf(comPort,'%d')); 
%     if( dx_1(1,index) > 250 )
%         dx_1(1,index) = 0;
%     end
    plot([dx_1(1,index) dx_1_dummy], [dy_1(1,index) dy_1_dummy], 'b');
    hold on
    plot(dx_2, dy_2, 'r.');
    drawnow;
    dx_1_dummy = dx_1(1,index);
    dy_1_dummy = dy_1(1,index);
end