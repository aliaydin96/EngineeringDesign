data=table2array(data1);
%%
rho= (data(1,:)+data(2,:))/2;
input=rho;
output=rho;
average = sum(abs(input(1,2:end)-input(1,1:end-1)))/(length(input)-1);
    discard_factor = 0.65;
    output = input;
    for i  = 1:(length(input)-1)
        if(input(1,i) >= 1500)
            input(1,i) = 0;
        end
        if(input(1,i+1) >= 1500)
            input(1,i+1) = 0;
        end
        if( abs(input(1,i+1)-input(1,i)) > discard_factor*average)
            output(1,i:i+1) = 0;
        else
            output(1,i) = input(1,i);
        end
    end
    
%%
theta= linspace(0,358.2,200);
theta= deg2rad(theta);


[x,y]=pol2cart(theta,rho);
[x1,y1]=pol2cart(theta,output);

%%
figure();
sz=25;
c=[1,0,0];
scatter(x,y,sz,c);
hold on;
sz=50;
c=[0, 0,1];
scatter(x1,y1,sz,c);
legend('\fontsize{16}Discarded points','\fontsize{16}Measurement Data');
title('\fontsize{16}\color{blue} Measurement for Data-1');
ylabel('\fontsize{16}\color{blue} y');
xlabel('\fontsize{16}\color{blue} x');
grid on;
grid minor;
