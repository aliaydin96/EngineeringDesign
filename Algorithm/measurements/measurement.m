clear;
clc;
%setting commication port object
comPort = serial('COM3','BaudRate',115200);
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
if(strcmp(comPort.Status,'closed'))
    fopen(comPort);
end
if(strcmp(comPort.Status,'closed'))
    fprintf('The port cannot be opened. The device is not connected properly');
end
intended_data_size = 70;
rho = zeros(1,intended_data_size);
theta = zeros(1,intended_data_size);
for index = 1:intended_data_size
    rho(1,index) = fscanf(comPort,'%d'); %in mm
    theta(1,index) = (fscanf(comPort,'%d')); %in radians
    polarplot((theta*2*pi/360),rho,'b.');
    title('The measurements in polar coordinates,rho is in mm');
    drawnow;
end
grid on;
[x,y] = pol2cart((theta*2*pi/360),rho);
figure;
grid on;
plot(x,y,'b.');
title('The measurements in cartesian coordinates');
xlabel('X axis, in mm');
ylabel('Y axis, in mm');
ylim([0, 1.2*max(y)]);
grid on;
fclose(comPort);
%%the code is implemented by selman dinc. in case of 