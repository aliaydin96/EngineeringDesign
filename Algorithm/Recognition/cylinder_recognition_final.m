data_path = 'C:\Users\AcmeCo\Desktop\sa\data';
data_path = [data_path num2str(8) '.csv'];
data = load(data_path);
for i = 1:400
    if(data(1,i) == 0)
        data(1,i) = 500; % this assumption yields we get closer to the target
    end
end
[rmin,rmin_ind]= min(data); %%determining where the center is located
r_compare_max = 52^2;       %%parameters dont change
r_compare_min = 42^2;       %%parameters dont change
variation = round(atan(50/(50+rmin))*200/pi)-1;
lower_index = rmin_ind-variation;
upper_index = rmin_ind+variation;
prob1 = 0;
for i = lower_index:upper_index
    r_next = (rmin+50)^2+data(1,i)^2-...
        2*data(1,i)*(rmin+50)*cos(pi*(i-rmin_ind)/200);
    if(r_compare_max >= r_next) && (r_compare_min <= r_next)
        prob1 = prob1 +1;
    end
end
prob1 = prob1/(upper_index-lower_index+1);
%checking for small
r_compare = 30^2;
index_variation = round(atan(25/(25+rmin))*200/pi)-1;
lower_index_small = rmin_ind-index_variation;
upper_index_small = rmin_ind+index_variation;

prob2 = 0;
for i = lower_index_small:upper_index_small
    r_next = (rmin+25)^2+data(1,i)^2-...
        2*data(1,i)*(rmin+25)*cos(pi*(i-rmin_ind)/200);
    if(r_compare >= r_next)
        prob2 = prob2 +1;
    end
end
prob2 = prob2/(upper_index_small-lower_index_small+1);
if(prob1 >= 0.6)
    fprintf("%d mm\n",100);
end
if((prob1 <= 0.6)&&(prob2 >= 0.6))
    fprintf("%d mm\n",50);
end



