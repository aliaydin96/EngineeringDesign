%%
test_1 = imread('test_1.JPG');
test_2 = imread('test_2.JPG');
test_3 = imread('test_3.JPG');
test_4 = imread('test_4.JPG');
test_5 = imread('test_5.JPG');
test_6 = imread('test_6.JPG');
test_7 = imread('test_7.JPG');
%%
test_1_gry = rgb2gray(test_1);
test_2_gry = rgb2gray(test_2);
test_3_gry = rgb2gray(test_3);
test_4_gry = rgb2gray(test_4);
test_5_gry = rgb2gray(test_5);
test_6_gry = rgb2gray(test_6);
test_7_gry = rgb2gray(test_7);
%%
first_thr = imbinarize(test_1_gry,graythresh(test_1_gry));
first_thr_map = not(first_thr);
map1 = robotics.BinaryOccupancyGrid(first_thr_map,100);
show(map1);
robotRadius = 0.2;
mapInflated = copy(map1);
inflate(mapInflated,robotRadius);
show(mapInflated);
grid on;
%%
scnd_thr = imbinarize(test_2_gry,graythresh(test_2_gry));
scnd_thr_map = not(scnd_thr);
map2 = robotics.BinaryOccupancyGrid(scnd_thr_map,100);
show(map2);
mapInflated2 = copy(map2);
inflate(mapInflated2,robotRadius);
show(mapInflated2);
grid on;
%%
thrd_thr = imbinarize(test_3_gry,graythresh(test_3_gry));
thrd_thr_map = not(thrd_thr);
map3 = robotics.BinaryOccupancyGrid(thrd_thr_map,50);
show(map3);
mapInflated3 = copy(map3);
inflate(mapInflated3,robotRadius);
show(mapInflated3);
grid on;
%%
frth_thr = imbinarize(test_4_gry,graythresh(test_4_gry));
frth_thr_map = not(frth_thr);
map4 = robotics.BinaryOccupancyGrid(frth_thr_map,100);
show(map4);
mapInflated4 = copy(map4);
inflate(mapInflated4,robotRadius);
show(mapInflated4);
grid on;
%%
fith_thr = imbinarize(test_5_gry,graythresh(test_5_gry));
fith_thr_map = not(fith_thr);
map5 = robotics.BinaryOccupancyGrid(fith_thr_map,10);
show(map5);
mapInflated5 = copy(map5);
inflate(mapInflated5,robotRadius);
show(mapInflated5);
grid on;
%%
sixth_thr = imbinarize(test_6_gry,graythresh(test_6_gry));
sixth_thr_map = not(sixth_thr);
map6 = robotics.BinaryOccupancyGrid(sixth_thr_map,100);
show(map6);
mapInflated6 = copy(map6);
inflate(mapInflated6,robotRadius);
show(mapInflated6);
grid on;
%%
svnth_thr = imbinarize(test_7_gry,graythresh(test_7_gry));
svnth_thr_map = not(svnth_thr);
map7 = robotics.BinaryOccupancyGrid(svnth_thr_map,100);
show(map7);
mapInflated7 = copy(map7);
inflate(mapInflated7,robotRadius);
show(mapInflated7);
grid on;
%%
prm = robotics.PRM;
%%
prm.Map = mapInflated;
prm.NumNodes = 50;
prm.ConnectionDistance = 0.5;
startLocation = [3 2];
endLocation = [7 9];
path = findpath(prm, startLocation, endLocation);
while isempty(path)
    % No feasible path found yet, increase the number of nodes
    prm.NumNodes = prm.NumNodes + 10;
    
    % Use the |update| function to re-create the PRM roadmap with the changed
    % attribute
    update(prm);
    
    % Search for a feasible path with the updated PRM
    path = findpath(prm, startLocation, endLocation);
end
path;
show(prm);
grid on;
%%
prm.Map = mapInflated2;
prm.NumNodes = 50;
prm.ConnectionDistance = 1;
startLocation2 = [1.5 1.5];
endLocation2 = [1.5 8.5];
path2 = findpath(prm, startLocation2, endLocation2);
while isempty(path2)
    % No feasible path found yet, increase the number of nodes
    prm.NumNodes = prm.NumNodes + 10;
    
    % Use the |update| function to re-create the PRM roadmap with the changed
    % attribute
    update(prm);
    
    % Search for a feasible path with the updated PRM
    path2 = findpath(prm, startLocation2, endLocation2);
end
path2;
show(prm);
grid on;
%%
prm.Map = mapInflated3;
prm.NumNodes = 50;
prm.ConnectionDistance = 1;
startLocation3 = [2.7 9.7];
endLocation3 = [15.6 16.9];
path3 = findpath(prm, startLocation3, endLocation3);
while isempty(path3)
    % No feasible path found yet, increase the number of nodes
    prm.NumNodes = prm.NumNodes + 10;
    
    % Use the |update| function to re-create the PRM roadmap with the changed
    % attribute
    update(prm);
    
    % Search for a feasible path with the updated PRM
    path3 = findpath(prm, startLocation3, endLocation3);
end
path3;
show(prm);
grid on;
%%
prm.Map = mapInflated4;
prm.NumNodes = 50;
prm.ConnectionDistance = 0.5;
startLocation4 = [7.5 2];
endLocation4 = [3 8];
path4 = findpath(prm, startLocation4, endLocation4);
while isempty(path4)
    % No feasible path found yet, increase the number of nodes
    prm.NumNodes = prm.NumNodes + 10;
    
    % Use the |update| function to re-create the PRM roadmap with the changed
    % attribute
    update(prm);
    
    % Search for a feasible path with the updated PRM
    path4 = findpath(prm, startLocation4, endLocation4);
end
path4;
show(prm);
grid on;
%%
prm.Map = mapInflated5;
prm.NumNodes = 50;
prm.ConnectionDistance = 5;
startLocation5 = [30 11.5];
endLocation5 = [15 65];
path5 = findpath(prm, startLocation5, endLocation5);
while isempty(path5)
    % No feasible path found yet, increase the number of nodes
    prm.NumNodes = prm.NumNodes + 10;
    
    % Use the |update| function to re-create the PRM roadmap with the changed
    % attribute
    update(prm);
    
    % Search for a feasible path with the updated PRM
    path5 = findpath(prm, startLocation5, endLocation5);
end
path5;
show(prm);
grid on;
%%
prm.Map = mapInflated6;
prm.NumNodes = 50;
prm.ConnectionDistance = 0.5;
startLocation6 = [6.5 1.5];
endLocation6 = [2 7];
path6 = findpath(prm, startLocation6, endLocation6);
while isempty(path6)
    % No feasible path found yet, increase the number of nodes
    prm.NumNodes = prm.NumNodes + 10;
    
    % Use the |update| function to re-create the PRM roadmap with the changed
    % attribute
    update(prm);
    
    % Search for a feasible path with the updated PRM
    path6 = findpath(prm, startLocation6, endLocation6);
end
path6;
show(prm);
grid on;
%%
prm.Map = mapInflated7;
prm.NumNodes = 50;
prm.ConnectionDistance = 0.5;
startLocation7 = [3.5 9];
endLocation7 = [8 2.3];
path7 = findpath(prm, startLocation7, endLocation7);
while isempty(path7)
    % No feasible path found yet, increase the number of nodes
    prm.NumNodes = prm.NumNodes + 10;
    
    % Use the |update| function to re-create the PRM roadmap with the changed
    % attribute
    update(prm);
    
    % Search for a feasible path with the updated PRM
    path7 = findpath(prm, startLocation7, endLocation7);
end
path7;
show(prm);
grid on;
%%