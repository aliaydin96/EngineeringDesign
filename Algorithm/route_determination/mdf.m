function [output] = mdf(input) %moving discard filter 
    %we know the certain length of the input is (1,200)
    %we dont use distance formula to increase eff. of the code piece
    %average distances is calculated via the difference between two
    %measurements since sampling angle diffrence is constant through out
    %the operation
    average = sum(abs(input(1,2:end)-input(1,1:end-1)))/(length(input)-1);
    discard_factor = 0.65;
    output = input;
    for i  = 1:(length(input)-1)
        if(input(1,i) >= 2500)
            input(1,i) = 0;
        end
        if(input(1,i+1) >= 2500)
            input(1,i+1) = 0;
        end
        if( abs(input(1,i+1)-input(1,i)) > discard_factor*average)
            output(1,i:i+1) = 0;
        else
            output(1,i) = input(1,i);
        end
    end
end