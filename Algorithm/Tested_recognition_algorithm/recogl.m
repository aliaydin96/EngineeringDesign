data_path = 'C:\Users\AcmeCo\Desktop\testy\Square\data5.csv';
  data = load(data_path);
  %%determining where the center is located and curve-check.
  for i = 1:400
     if(data(1,i) == 0)
        data(1,i) = 1000; % this assumption yields we get closer to the target
     end
  end
  designated_data = data(1,100:400);  
  [rmin,rmin_ind]= min(designated_data);
%%   checking if it is in the range, just visualization
%   th = (0:1:399)*pi/200;
%   selected_th = th(1,100:400);
%   figure;
%   plot(57*cos(th)+(rmin+50)*cos(selected_th(1,rmin_ind)), ...
%       57*sin(th)+(rmin+50)*sin(selected_th(1,rmin_ind)));
%   hold on;
%   plot(40*cos(th)+(rmin+50)*cos(selected_th(1,rmin_ind)), ...
%       40*sin(th)+(rmin+50)*sin(selected_th(1,rmin_ind)),'red');
%   plot(cos(selected_th).*designated_data,sin(selected_th).*designated_data);
%   hold off;
%   xlim([-400 400]); ylim ([-400 400]);
%   grid on;
%%
  r_compare_max = 57^2; 
  r_compare_min = 40^2; 
  variation = round(atan(50/(50+rmin))*200/pi)-1; 
  lower_index = rmin_ind-variation;
  upper_index = rmin_ind+variation;
  %no need to take sqrt since it slows the program
  %we took the outer cicle diameter 37mm
  prob = 0;
  for i = lower_index:upper_index
      r_next = (rmin+50)^2+designated_data(1,i)^2-...
          2*designated_data(1,i)*(rmin+50)*cos(pi*(i-rmin_ind)/200);
      fprintf("r_next = %d, min = %d, max  = %d\n",r_next ,r_compare_min,r_compare_max);
     if(r_compare_max >= r_next) && (r_compare_min <= r_next)
        prob = prob +1; 
     end
  end
  prob = prob/(upper_index-lower_index+1);
  if (prob >= 0.4)
     bool = 1; 
  else 
      bool = 0;
  end
  if(rmin < 250 && prob >= 0.6)
     fprintf("stable result %d", prob); 
  else
      fprintf("unstable result %d", prob); 
  end
  


%%SelmanDinç