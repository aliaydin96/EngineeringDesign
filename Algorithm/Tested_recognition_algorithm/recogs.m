data_path = 'C:\Users\AcmeCo\Desktop\testy\Cylinder5\data16.csv';
data = load(data_path);
%%determining where the center is located and curve-check.
for i = 1:400
    if(data(1,i) == 0)
        data(1,i) = 1000; % this assumption yields we get closer to the target
    end
end
designated_data = [ data(1,300:400), data(1,1:100)];
[rmin,rmin_ind]= min(designated_data);
% %% checking if it is in the range visually
% th = (0:1:399)*pi/200;
% selected_th = th(1,300:400);
% figure;
% plot(32*cos(th)+(rmin+32)*cos(selected_th(1,min_index)), ...
%     32*sin(th)+(rmin+32)*sin(selected_th(1,min_index)));
% xlim([0 400]); ylim ([-400 0]);
% hold on;
% plot(cos(selected_th).*designated_data,sin(selected_th).*designated_data);
% hold off;
%%
r_compare = 32^2;
variation = round(atan(25/(25+rmin))*200/pi)-1;
lower_index = rmin_ind-variation;
upper_index = rmin_ind+variation;
%no need to take sqrt since it slows the program
%we took the outer cicle diameter 37mm
prob = 0;
for i = lower_index:upper_index
    r_next = (rmin+25)^2+designated_data(1,i)^2-...
        2*designated_data(1,i)*(rmin+25)*cos(pi*(i-rmin_ind)/200);
    fprintf("r_next: %d, r_compare: %1.2f \n", r_next, r_compare);
    if(r_compare >= r_next)
        prob = prob +1;
    end
end
prob = prob/(upper_index-lower_index+1);
if (prob >= 0.4)
    bool = 1;
else
    bool = 0;
end
if(rmin < 250)
    fprintf("stable result %1.2f", prob);
end



%%SelmanDinç