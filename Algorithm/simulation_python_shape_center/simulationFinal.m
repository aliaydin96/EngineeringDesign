clc;
clear;
%% Step 1: Read image Read in
RGB = imread('simpified map.png');
% RGB = imresize(RGB,0.3);

% Step 2: Convert image from rgb to gray 
GRAY = rgb2gray(RGB);

% Step 3: Threshold the image Convert the image to black and white in order
% to prepare for boundary tracing using bwboundaries. 
threshold = graythresh(GRAY);
BW = im2bw(GRAY, threshold);
imshow(BW);
title('Binary Image');

%%
X=[];
Y=[];
A=size(BW);
lenX=A(1,1);
lenY=A(1,2);
for i=1:lenX
    for j=1:lenY
        if BW(i,j)==0
           X=[X,i];
           Y=[Y,j];
        end
        
        
    end
      
end
len=length(X);

%%
MapX=[];
MapY=[];
 a=0;
 x=1:len;
 x1=0;
 y1=0;
 for k=0:2
     
 for theta=-80:3:80
     m = tand(theta);
    mode=0;
    mode2=0;
    y= round(m*x)+k*200;
    plot(x,y);
    hold on;
    axis equal;
            
    for i=1:len
        
        for j=1:len
            if X(i)== x(j) && Y(i) == y(j) && mode ==0 && X(i)>k*200
            MapX=[MapX x(j)];
            MapY=[MapY y(j)];
%             a=i;
            plot(x,y);
            hold on;
            axis equal;
            mode=1;
            
            elseif X(i)== x(j) && Y(i) == y(j) && X(i)<k*200
                x1=x(j);
                y1=y(j);
            
              
               end
%             
            
        end
        
                
              
%             if a==i
%                 break;
%             end
%     
    end
                MapX=[MapX x1];
                MapY=[MapY y1];
                x1=0;
                y1=0;
 end
 end
    
%%
    hold on;
%     plot(X,Y,'bx');
    plot(MapX,MapY,'ro');
    axis equal;
    
    
       
    
       