%this script is for filtering with mdf and visualizing the data
%indicate final and start points using paint
close all;
direct = 'data2';
data = csvread(['C:\Users\AcmeCo\Desktop\route_determination\', direct, '.csv']);
data_txt = csvread(['C:\Users\AcmeCo\Desktop\route_determination\', direct, '.txt']);
set = mdf((data(1,:)+data(2,:))*0.5);
th = (0:1:199)*2*pi/200;
figure;
plot(set.*cos(th), set.*sin(th),'.r');
hold on;
%plotting robot boundary;
plot(75*cos(th), 75*sin(th),'-g');
plot([0 data_txt(1,1)], [0 data_txt(2,1)],'-b');
plot(75*cos(th)+data_txt(1,1), 75*sin(th)+data_txt(2,1),'-b');
axis equal;
grid on;
title('First-Iteration Route Determination');
xlabel('x axis, mm');
ylabel('y axis, mm');
legend('Test Env.','Initial Pos.','Path', 'Final Pos.')