delete(instrfind());
clear all;
clc;
close all;

% %setting commication port object
% %change the port COM11
comPort = serial('COM6','BaudRate',115200);
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
% create vector to keep the previous data
intended_data_size = 200;
dx_1 = zeros(1,intended_data_size);
dy_1 = zeros(1,intended_data_size);
dx_2 = zeros(1,intended_data_size);
dy_2 = zeros(1,intended_data_size);
l_1 = zeros(1,intended_data_size);
l_2 = zeros(1,intended_data_size);
% mouse positions in xy coordinate
x_pos = 0;
y_pos = 0;
x1_pos = 0;
y1_pos = 0;
x2_pos = 0;
y2_pos = 0;
% the previous mouse positions
x_pos_initial = 0;
y_pos_initial = 0;
x1_pos_initial = 0;
y1_pos_initial = 0;
angle = 0; 
anglesum = 90;
s = 0;
sumx = 0;
sumy = 0;
for index = 1:intended_data_size
    % take data from serial port
    % this dx means it is instantenous data
    dx_1(1,index) = (fscanf(comPort,'%d')) / 7.35;
    dy_1(1,index) = (fscanf(comPort,'%d')) / 7.35;
    dx_2(1,index) = (fscanf(comPort,'%d')) / 7.35;
    dy_2(1,index) = (fscanf(comPort,'%d')) / 7.35; 
%     % to obtain xy position of mouse
    x1_pos = x1_pos_initial + dx_1(1, index);
    y1_pos = y1_pos_initial + dy_1(1, index);
%     x2_pos = x2_pos_initial + dx_2(1, index);
%     y2_pos = y2_pos_initial + dy_2(1, index);
    
     l_1(1,index) = sqrt(dx_1(1,index)^2 + dy_1(1,index)^2);
     l_2(1,index) = sqrt(dx_2(1,index)^2 + dy_2(1,index)^2);
     s = (l_1(1,index) + l_2(1,index)) / 2;
     
     if( (dy_1(1,index)>=0) & (dy_2(1,index)>=0)|| (dy_1(1,index)>=0) & (dy_2(1,index)<=0))%(dx_1(1,index)<=0) & (dx_2(1,index)<=0) &
            angle = anglesum - (l_1(1,index) - l_2(1,index)) / 1.1
            x_pos = s * cos(anglesum * pi / 180) + x_pos_initial;
            y_pos = s * sin(anglesum * pi / 180) + y_pos_initial;
     else
            angle = (l_1(1,index) - l_2(1,index)) / 1.1 + anglesum
            x_pos = -s * cos(anglesum * pi / 180) + x_pos_initial;
            y_pos = -s * sin(anglesum * pi / 180) + y_pos_initial;
     end

     anglesum = angle;

    xlim([-500 500]);
    ylim([-400 400]);
    hold on
    plot([x_pos x_pos_initial], [y_pos y_pos_initial], 'g');
    drawnow;
    
    x_pos_initial = x_pos;
    y_pos_initial = y_pos;
    x1_pos_initial = x1_pos;
    y1_pos_initial = y1_pos;


end