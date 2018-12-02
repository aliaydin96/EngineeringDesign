clc;
clear;
%% Step 1: Read image Read in
RGB = imread('test_plane.png');
RGB = imresize(RGB,0.3);

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

%%
figure(1);
plot(X,Y,'o');
saveas(figure(1),'bold.png');
%%
X=X';
Y=Y';
shp = alphaShape(X,Y,8);
figure(3);
plot(shp)
saveas(figure(3),'line.png');

