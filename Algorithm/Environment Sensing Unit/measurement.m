%% scanning the serial port and visualization
close all;
fopen(comPort);
intended_data_size = 92;
rho = zeros(1,intended_data_size);
theta = zeros(1,intended_data_size);
for index = 1:intended_data_size
    rho(1,index) = fscanf(comPort,'%d'); %in mm
    theta(1,index) = (fscanf(comPort,'%d')); %in radians
    if( rho(1,index) > 280 )
        rho(1,index) = 0;
    end
    polarplot((theta*2*pi/360),rho,'b.');
    title('The measurements in polar coordinates,rho is in mm');
    drawnow;
end
[x,y] = pol2cart((theta*2*pi/360),rho);
 
x_transient = [];
y_transient = [];
for index = 1:length(x)
   if(~(x(1,index) == 0 && y(1,index) == 0))
      x_transient = [x_transient, x(1,index)];
      y_transient = [y_transient, y(1,index)];
   end
end
x = x_transient;
y = y_transient;

average_distance = 0;
for index = 2:length(x)
    average_distance = average_distance + sqrt((x(1, index-1)-x(1, index))^2 ...
    + (y(1, index-1)-y(1, index))^2);
end
average_distance = average_distance/(length(x)-1);

x_trans = [];
y_trans = [];
for index = 2:length(x)
    dummy = sqrt((x(1, index-1)-x(1, index))^2 + (y(1, index-1)-y(1, index))^2);
    if(dummy <= average_distance)
        x_trans = [x_trans, x(1,index)];
        y_trans = [y_trans, y(1,index)];
    end
end
x = x_trans;
y = y_trans;

%%clipping
x = x(1,3:end-2);
y = y(1,3:end-2);

%%plotting
figure;
grid on;
plot(x,y,'b.');
title('The measurements in cartesian coordinates');
xlabel('X axis, in mm');
ylabel('Y axis, in mm');
grid on;
fclose(comPort);
%%the code is implemented by selman dinc. in case of 