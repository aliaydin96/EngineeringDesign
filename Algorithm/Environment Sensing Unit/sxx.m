th = (0:1:199)'*2*pi/200;
figure;
polar(th,s(1:200,1),'.r');
hold on;
polar(th,s(201:400,1),'.g');