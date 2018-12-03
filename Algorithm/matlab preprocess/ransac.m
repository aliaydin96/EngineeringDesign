% Sree Prasanna Rajagopal, 
% [Mechanical Engineering Department, IIT Guwahati] February 2013
function [bestModel,bestInliers,bestOutliers,bestError] = ransac(thresError,N,d,iterations)
syms inliers outliers ni no;
% model
bestModel = [];
bestInliers = [];
bestOutliers = [];
bestError = inf;
reply = input('Random generation (1) or input data  (2)?\n');
if (reply == 1)
    data= rand(2,N);
else
    data = input('Enter the data matrix in 2xN format.\n');
end    
for i=1:iterations
    randomP = randperm(N);
    p1 = [ data(1,randomP(1)), data(2,randomP(1)) ];
    p2 = [ data(1,randomP(2)), data(2,randomP(2)) ];
    
    inliers = [];
    outliers = [];
    ni = 0;
    no = 0;
    
    a_model = ( p1(2) - p2(2) )/ ( p1(1) - p2(1) );
    b_model = p1(2) - a_model*p1(1);
    
    totalError = 0;
    
    for p=1:N
        point = data(:,p);
        error = abs( data(1,p)*a_model + b_model - data(2,p) )/ sqrt( a_model^2 + 1);
        
        if( thresError < error )
            outliers(:,no+1) = point;
            no = no+1;
        else 
            totalError = totalError + error;
            inliers(:,ni+1) = point;
            ni = ni+1;
        end
    end % data iteration end
        
    % check model
    
    if ( bestError > totalError && d < ni )
        bestModel = [a_model,b_model];
        bestInliers = inliers;
        bestOutliers = outliers;
        bestError = totalError;
    end
        
    
    
end % main iteration end
return;