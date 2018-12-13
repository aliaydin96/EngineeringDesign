set_1 = zeros(size(meas_1.Measurement));
for i = 1:length(meas_1.Measurement(1,:))
    set_1(:,i) = [cos(meas_1.Angle*(2*pi/360)) sin(meas_1.Angle*(2*pi/360));...
        -sin(meas_1.Angle*(2*pi/360)) cos(meas_1.Angle*(2*pi/360)) ]*meas_1.Measurement(:,i);
end
set_1 = set_1 + repmat(meas_1.Position,1,length(meas_1.Measurement(1,:)));

set_2 = zeros(size(meas_2.Measurement));
for i = 1:length(meas_2.Measurement(1,:))
    set_2(:,i) = [cos(meas_2.Angle*(2*pi/360)) sin(meas_2.Angle*(2*pi/360));...
        -sin(meas_2.Angle*(2*pi/360)) cos(meas_2.Angle*(2*pi/360)) ]*meas_2.Measurement(:,i);
end
set_2 = set_2 + repmat(meas_2.Position,1,length(meas_2.Measurement(1,:))) ;

set_3 = zeros(size(meas_3.Measurement));
for i = 1:length(meas_3.Measurement(1,:))
    set_3(:,i) = [cos(meas_3.Angle*(2*pi/360)) sin(meas_3.Angle*(2*pi/360));...
        -sin(meas_3.Angle*(2*pi/360)) cos(meas_3.Angle*(2*pi/360)) ]*meas_3.Measurement(:,i);
end
set_3 = set_3 + repmat(meas_3.Position,1,length(meas_3.Measurement(1,:))) ;

set_4 = zeros(size(meas_4.Measurement));
for i = 1:length(meas_4.Measurement(1,:))
    set_4(:,i) = [cos(meas_4.Angle*(2*pi/360)) sin(meas_4.Angle*(2*pi/360));...
        -sin(meas_4.Angle*(2*pi/360)) cos(meas_4.Angle*(2*pi/360)) ]*meas_4.Measurement(:,i);
end
set_4 = set_4 + repmat(meas_4.Position,1,length(meas_4.Measurement(1,:))) ;

plot(set_1(1,:),set_1(2,:),'r.');
hold on;
plot(set_2(1,:),set_2(2,:),'b.');
plot(set_3(1,:),set_3(2,:),'g.');
plot(set_4(1,:),set_4(2,:),'black.');
grid on;
