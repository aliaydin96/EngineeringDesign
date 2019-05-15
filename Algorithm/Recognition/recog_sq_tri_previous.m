clc; close all;
turning_point = zeros(2,4);
for z = 1:25
    data_path = ['testy\TE-2\data', num2str(z), '.csv'];
    %% loading and designating data
    
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
    if(rmin <= 2200)
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
        sec_der = der(1,2:end)-der(1,1:end-1);
        filt_der = conv(der,[1 1 1]/3);
        filt_der = filt_der(1,2:end-1);
%         filt_der = conv(filt_der,[1 1 1]/3);
%         filt_der = filt_der(1,2:end-1);
        fprintf("rms = %4.1f  ",sum(filt_der));
        %% just visualization;
        figure,subplot(1,2,2);
        stem(filt_der,'r'); 
        xlabel('Measurement Number');
        ylabel('Change in r, mm');
        title('Filtered derivative'); 
        grid on;
        subplot(1,2,1);
        plot(data(1,min_ind:max_ind).*cos(theta(1,min_ind:max_ind)),...
            data(1,min_ind:max_ind).*sin(theta(1,min_ind:max_ind)),'.r');
        hold on;
        xlabel('x, mm');
        ylabel('y, mm');
        title('Object Measurement');
        grid on;
        %% finding turning points
        turning_point(:,1)= [data(1,min_ind);sel_th(1,1)];
        turning_point(:,4)= [data(1,max_ind);sel_th(1,end)];
        for i = 1:length(der)
            if(filt_der(1,i) >= -1)   %% critical parameter
                turning_point(1,2) =  sel_r(1,i-1);
                turning_point(2,2) =  sel_th(1,i-1);
                break;
            end
        end
        for i = 1:length(der)
            if(filt_der(1,end-i) <= 1)
                turning_point(1,3) =  sel_r(1,end-i+1);
                turning_point(2,3) =  sel_th(1,end-i+1);
                break;
            end
        end
        %just plotting
        plot(turning_point(1,:).*cos(turning_point(2,:)),...
            turning_point(1,:).*sin(turning_point(2,:)),'*g');
        axis equal; hold off; legend('measurement','edges of objects')
%         
        %% angle analysis
        %convert them into polar coordinates
        x_tur = turning_point(1,:).*cos(turning_point(2,:));
        y_tur = turning_point(1,:).*sin(turning_point(2,:));
        
        dis_tur1 = x_tur(1,2:4)-x_tur(1,1:3);  %distance between two turning point, no need to take sqrt
        dis_tur1 = dis_tur1.^2;
        dis_tur2 = y_tur(1,2:4)-y_tur(1,1:3);
        dis_tur2 = dis_tur2.^2;
        dise = dis_tur1+dis_tur2; %square of actual distance;
        
        dis1 = [(x_tur(1,3)-x_tur(1,1))^2, (x_tur(1,4)-x_tur(1,2))^2];
        dis2 = [(y_tur(1,3)-y_tur(1,1))^2, (y_tur(1,4)-y_tur(1,2))^2];
        disq = dis1+dis2;
        
        an_tur1 = (dise(1,1)+dise(1,2)-disq(1,1))/(2*sqrt(dise(1,1)*dise(1,2)));
        an_tur2 = (dise(1,3)+dise(1,2)-disq(1,2))/(2*sqrt(dise(1,3)*dise(1,2)));
        an_tur1 = abs(acos(an_tur1))*180/pi;
        an_tur2 = abs(acos(an_tur2))*180/pi;
        %just plotting
        %     fprintf("an_tur1 = %3.1f\n",an_tur1);
        %     fprintf("an_tur2 = %3.1f\n",an_tur2);
        
        %% generating results;
        % firstly get-closer command will be generated if it is required. Donot
        % forget
        %checking if we have a corner
        dummy_an = an_tur1+an_tur2-180;
        %     fprintf("an = %3.1f\n", dummy_an);
        %     fprintf("dis = %3.1f\n", dise(1,2));
        if(dise(1,2)<2209)
            if((dummy_an <= 80) && (dummy_an >= 50))
                fprintf("%d ",z);
                fprintf("triangular w/ angle= %2.1f", dummy_an);
                fprintf(" ,rmin = %3d\n",rmin);
            end
            if((dummy_an <= 120) && (dummy_an >= 80)&&(an_tur1<140)&&(an_tur2<140))
                fprintf("%d ",z);
                fprintf("square w/ angle= %2.1f", dummy_an);
                fprintf(" ,rmin = %3d\n",rmin);
            elseif((an_tur1>140)&&(an_tur2>140))
                fprintf("%d ",z);
                fprintf("triangle");
                fprintf(" ,rmin = %3d\n",rmin);
            end
        end
        if(dise(1,2)>=2209) %considering edges
            if ((an_tur1 >= 95)&&(an_tur2 >= 95))
                if((dise(1,2) < 4900)&&((dise(1,2) >= 2209)))
                    fprintf("%d ",z);
                    fprintf('sqare w/ edge = %4.f', sqrt(dise(1,2)));
                    fprintf(" ,rmin = %3d\n",rmin);
                end
                if((dise(1,2) >= 4900)&&(dise(1,2) <= 8100))
                    fprintf("%d ",z);
                    fprintf('triangular w/ edge = %4.f', sqrt(dise(1,2)));
                    fprintf(" ,rmin = %3d\n",rmin);
                end
            end
        else
            %         fprintf("%d ",z);
            %         fprintf("patlak\n");
        end
        
    else
        fprintf("not in range\n");
    end
    
    
end

%%SelmanDinç