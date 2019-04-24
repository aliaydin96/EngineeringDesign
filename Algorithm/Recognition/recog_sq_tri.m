clc; close all; clear all;
%% loading and designating data
turning_point = zeros(2,4);
data_path = 'C:\Users\AcmeCo\Desktop\testy\Triangular\data19.csv';
data = load(data_path);
theta = (0:1:399)*pi/200;
%%determining where the center is located and curve-check.
for i = 1:400
    if(data(1,i) == 0)
        data(1,i) = 500; % this assumption yields we get closer to the target
    end
end
%% locating rmin and rmin_ind
[rmin,rmin_ind]= min(data);
%% filtering 
for i = 1:30
    if(data(1,(rmin_ind+i)) < 250)
        max_ind = rmin_ind+i;
    end
    if(data(1,(rmin_ind-i)) < 250)
        min_ind = rmin_ind-i;
    end
end
sel_r = data(1,min_ind:max_ind);
sel_th = theta(1,min_ind:max_ind);
%%selected theta
der = sel_r(1,2:end)-sel_r(1,1:end-1);
filt_der = conv(der,[1 1 1]);
filt_der = filt_der(1,2:end-1);

% sec_der = filt_der(1,2:end)-filt_der(1,1:end-1);
% filt_sec_der = conv(sec_der,[1 1 1]);
% filt_sec_der = filt_sec_der(1,2:end-1);
% weight = sum(filt_sec_der.*filt_der);
% fprintf("weight = %5.f", weight);
%% just visualization;
figure; stem(der,'r');
figure; stem(filt_der,'r');
hold on;
stem([max_ind-rmin_ind], [1],'b');
hold off;
figure; plot(data(1,min_ind:max_ind).*cos(theta(1,min_ind:max_ind)),...
    data(1,min_ind:max_ind).*sin(theta(1,min_ind:max_ind)),'.r');
hold on;
%% finding turning points
turning_point(:,1)= [data(1,min_ind);sel_th(1,1)];
turning_point(:,4)= [data(1,max_ind);sel_th(1,end)];
for i = 1:length(der)
    if(der(1,i) >= -2)   %% critical parameter
       turning_point(1,2) =  sel_r(1,i-1);
       turning_point(2,2) =  sel_th(1,i-1);
       break;
    end    
end
for i = 1:length(der)
    if(der(1,end-i) <= 2)
       turning_point(1,3) =  sel_r(1,end-i+1);
       turning_point(2,3) =  sel_th(1,end-i+1);
       break;
    end    
end
%just plotting
plot(turning_point(1,:).*cos(turning_point(2,:)),...
    turning_point(1,:).*sin(turning_point(2,:)),'*g');
axis equal;

%% angle analysis
%convert them into polar coordinates
x_tur = turning_point(1,:).*cos(turning_point(2,:));
y_tur = turning_point(1,:).*sin(turning_point(2,:));
angle1 = atan((y_tur(1,2)-y_tur(1,1))/(x_tur(1,2)-x_tur(1,1)));
angle1 = abs(angle1*360/(2*pi));
angle2 = atan((y_tur(1,3)-y_tur(1,2))/(x_tur(1,3)-x_tur(1,2)));
angle2 = abs(angle2*360/(2*pi));
angle3 = atan((y_tur(1,4)-y_tur(1,3))/(x_tur(1,4)-x_tur(1,3)));
angle3 = abs(angle3*360/(2*pi));
an_tur1 = angle2+angle1; %degree
an_tur2 = 180-abs(angle3+angle2); %degree
%just plotting
fprintf("an_tur1 = %3.1f\n",an_tur1);
fprintf("an_tur2 = %3.1f\n",an_tur2);

dis_tur1 = x_tur(1,2:4)-x_tur(1,1:3);  %distance between two turning point, no need to take sqrt
dis_tur1 = dis_tur1.^2;
dis_tur2 = y_tur(1,2:4)-y_tur(1,1:3); 
dis_tur2 = dis_tur2.^2;
dis = dis_tur1+dis_tur2; %square of actual distance;

%% generating results;
%firstly get-closer command will be generated if it is required. Donot
%forget
%checking if we have a corner
if(dis(1,2)<1225)
    dummy_an = an_tur1+an_tur2-180;
   if((dummy_an <= 70) && (dummy_an >= 50))
       fprintf("triangular w/ angle= %d", dummy_an);
   end
   if((dummy_an <= 105) && (dummy_an >= 80))
       fprintf("square w/ angle= %d", dummy_an);
   end
end
if(dis(1,2)>=1225) %considering edges
       if ((an_tur1 >= 95)&&(an_tur2 >= 95))
           if((dis(1,2) <= 4000)&&((dis(1,2) >= 2209)))
                 fprintf('sqare w/ edge = %4.f\n', dis(1,2));  
           end
           if((dis(1,2) >= 4000)&&(dis(1,2) <= 8100))
               fprintf('triangular w/ edge = %4.f\n', dis(1,2));
           end        
       end
end




%%SelmanDinç