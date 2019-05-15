clc; close all;
%algorithm works with 97 success rate.
for z = 1:75
    flag = 0;
    fprintf(" %d ",z);   
    data= csvread(['T1\data',num2str(z),'.csv']);
    theta = (0:1:399)*pi/200;
    for i = 1:400
        if(data(1,i) == 0)
            data(1,i) = 500;
        end
    end
    [trivial1,rmin_ind]= min(data);
    
    for i = 1:30
        if(data(1,(rmin_ind+i)) < 240)
            max_ind = rmin_ind+i;
        end
        if(data(1,(rmin_ind-i)) < 240)
            min_ind = rmin_ind-i;
        end
    end
    sel_r = data(1,min_ind:max_ind);
    sel_th = theta(1,min_ind:max_ind);
    sel_x = sel_r.*cos(sel_th);
    sel_y = sel_r.*sin(sel_th);
    
    [rmin, min_ind] = min(sel_r);
    
    der = sel_r(1,2:end)-sel_r(1,1:end-1);
    f_der = conv(der,[1 1 1]/3);
    f_der = f_der(1,2:end-1);
    xmin = sel_x(1,min_ind);
    ymin = sel_y(1,min_ind);
    p1x = sel_x(1,1);
    p1y = sel_y(1,1);
    p4x = sel_x(1,end);
    p4y = sel_y(1,end);
    rms = sqrt(sum(der.*der)/length(der));
    rms = sqrt(rms);
    for i = 1:length(der)
        if(f_der(1,i) >= -rms)  
            p2x =  sel_x(1,i);
            p2y =  sel_y(1,i);
            break;
        end
    end
    
    for i = 1:length(der)
        if(f_der(1,end-i) <= rms)
            p3x =  sel_x(1,end-i);
            p3y =  sel_y(1,end-i);
            break;
        end
    end
    de1 = (p1x-p2x)^2+(p1y-p2y)^2;
    de2 = (p3x-p2x)^2+(p3y-p2y)^2;
    de3 = (p4x-p3x)^2+(p3y-p4y)^2;
    dq1 = (p1x-p3x)^2+(p1y-p3y)^2;
    dq2 = (p2x-p4x)^2+(p2y-p4y)^2;
    a1 = (de1+de2-dq1)/(2*sqrt(de1*de2));
    a2 = (de3+de2-dq2)/(2*sqrt(de3*de2));
    a1 = acos(a1)*180/pi;
    a2 = acos(a2)*180/pi;
    
    orian = (p3x-p2x)*(p2x+p3x)+(p3y-p2y)*(p2y+p3y);
    orian = orian/(sqrt(de2*((p2x+p3x)^2+(p2y+p3y)^2)));
    orian = acos(orian)*180/pi;
    
    d1 = (ymin-p1y)^2+(xmin-p1x)^2;
    d2 = (ymin-p4y)^2+(xmin-p4x)^2;
    corner_angle = (p1x-p4x)^2+(p1y-p4y)^2;
    corner_angle = acos((d1+d2-corner_angle)/(2*sqrt(d1*d2)));
    corner_angle = corner_angle*180/pi;

    
    %classification no result is flag
    if(de2 < 1300)
       %we are on the corner
       
       if(corner_angle < 75)
           fprintf("T cor.an= %.1f\t",corner_angle);
           flag = 1;
       end
       if(corner_angle > 75)
           fprintf("S cor.an= %.1f\t",corner_angle);
           flag = 1;
       end  
        % p1 = plot(z,corner_angle,'.r'); hold on;    
    end
    
    if((a1 >= 130)&&(de1 > 400))
        if(a2 < 80)
            fprintf(" T ed.an= %.1f \t",a2);
            flag = 1;
        end
        %else may be addded.
    end
    if((a2 >= 130)&&(de3 > 400))
        if(a1 < 80)
            fprintf(" T ed.an= %.1f\t",a1);
            flag = 1;
        end
        %else may be addded.
    end
    if(orian<90)
        rotation = 90-orian;
        a = a1;
    else
        rotation = orian-90;
        a = a2;
    end
    if((rotation >= 30)&&(a <= 85))
        fprintf("T1\t");
        flag = 1;
    end
    
    if(sqrt(de2)>= 69)
        fprintf("T2\t")
        flag = 1;
    end
    
    ax1 = (p2x-xmin)^2+(p2y-ymin)^2;
    ay1 = (p1x-xmin)^2+(p1y-ymin)^2;
    ay1 = (ax1+de1-ay1)/(2*sqrt(ax1*de1));
    ay1 = acos(ay1)*180/pi;
    
    ax2 = (p3x-xmin)^2+(p3y-ymin)^2;
    ay2 = (p4x-xmin)^2+(p4y-ymin)^2;
    ay2 = (ax2+de3-ay2)/(2*sqrt(ax2*de3));
    ay2 = acos(ay2)*180/pi;
    
    
    if((ay1>155)&&(ay2>155))
        if(corner_angle < 75)
            fprintf("SX = %d\t", corner_angle);
            flag = 1;
        end        
    end
    fprintf(" \n");
    
%     if(flag == 0)
%         figure('Name',num2str(z));
% %         subplot(1,2,2);
% %         stem(f_der,'r'); hold on;
% %         xlabel('Measurement Number');
% %         ylabel('Change in r, mm');
% %         title('Filtered derivative');
% %         grid on;
% %         subplot(1,2,1);
%         plot(sel_x,sel_y,'.r');
%         hold on;
%         plot(p1x,p1y,'*g');
%         plot(p2x,p2y,'*b');
%         plot(p3x,p3y,'*c');
%         plot(p4x,p4y,'*m');
%         axis equal; hold off;
%         xlabel('x, mm');
%         ylabel('y, mm');
%         title('Object Measurement');
%         grid on;
%         if (orian<=90)
%            txt3 = ['go right orian=',num2str(orian,'%.1f')];
%         else
%            txt3 = ['go left orian=',num2str(orian,'%.1f')];
%         end
% %         txt1 = ['a1=', num2str(a1,'%.1f')];
% %         txt2 = ['a2=', num2str(a2,'%.1f')];
%         
% %         text(xmin-20, ymin+100,txt1,'FontSize',9);
% %         text(xmin-20, ymin+90,txt2,'FontSize',9);
%         text(xmin-20, ymin+20,txt3, 'FontSize',9);
%     end
    
end


%%SelmanDinç