%% Finding map from different observer points
% Observer Parameters
obs_1 = [meas_1.Position(1); meas_1.Position(2); meas_1.Angle]; %x1,y1,meas_1.Angle
obs_2 = [meas_2.Position(1); meas_2.Position(2); meas_2.Angle]; %x2,y2,meas_2.Angle
obs_3 = [meas_3.Position(1); meas_3.Position(2); meas_3.Angle]; %x1,y3,meas_3.Angle
obs_4 = [meas_4.Position(1); meas_4.Position(2); meas_4.Angle]; %x1,y3,meas_3.Angle
storage1 = zeros(2,1);
storage2 = zeros(2,1);
storage3 = zeros(2,1);
storage4 = zeros(2,1);
%% Loop iteration for each data
for i=1:70
    % Measured Data
    from_obs_1 = [meas_1.Measurement(1,i);meas_1.Measurement(2,i)]; %x1,y1
    from_obs_2 = [meas_2.Measurement(1,i);meas_2.Measurement(2,i)]; %x2,y2
    from_obs_3 = [meas_3.Measurement(1,i);meas_3.Measurement(2,i)]; %x3,y3
    from_obs_4 = [meas_4.Measurement(1,i);meas_4.Measurement(2,i)]; %x4,y4
    %%
    % Multiplying with transition matrix with relative position values
    Trans_matrix1 = [cosd(meas_1.Angle-90) -sind(meas_1.Angle-90) ; sind(meas_1.Angle-90) cosd(meas_1.Angle-90)];
    Trans_matrix2 = [cosd(meas_2.Angle-90) -sind(meas_2.Angle-90) ; sind(meas_2.Angle-90) cosd(meas_2.Angle-90)];
    Trans_matrix3 = [cosd(meas_3.Angle-90) -sind(meas_3.Angle-90) ; sind(meas_3.Angle-90) cosd(meas_3.Angle-90)];
    Trans_matrix4 = [cosd(meas_4.Angle-90) -sind(meas_4.Angle-90) ; sind(meas_4.Angle-90) cosd(meas_4.Angle-90)];
    obs_1_xy = obs_1(1:2);
    xy_rotated1 = Trans_matrix1*from_obs_1;
    obs_2_xy = obs_2(1:2);
    xy_rotated2 = Trans_matrix2*from_obs_2;
    obs_3_xy = obs_3(1:2);
    xy_rotated3 = Trans_matrix3*from_obs_3;
    obs_4_xy = obs_4(1:2);
    xy_rotated4 = Trans_matrix4*from_obs_4;
    % Relative position to absolute position

    %%
    xy_absolute1 = xy_rotated1+obs_1_xy;
    xy_absolute2 = xy_rotated2+obs_2_xy;
    xy_absolute3 = xy_rotated3+obs_3_xy;
    xy_absolute4 = xy_rotated4+obs_4_xy;
    %%
    % Storage part
    storage1 = [storage1,xy_absolute1];
    storage2 = [storage2,xy_absolute2];
    storage3 = [storage3,xy_absolute3];
    storage4 = [storage4,xy_absolute4];
    hold on;
    plot(storage1(1,:),storage1(2,:),'.')
    plot(storage2(1,:),storage2(2,:),'.')
    plot(storage3(1,:),storage3(2,:),'.')
    plot(storage4(1,:),storage4(2,:),'.')
end