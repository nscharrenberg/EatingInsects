% Give the name csv file that want ot be ploted 
data = readtable("DT_max_depth.csv");
% be sure the range of X_axis match the size of data 
X_axis = 2:20:402 ;
mean_score = data.mean_test_score;
% +2 is needed if the range is from 2 
best = (find(data.rank_test_score==1) - 1 ) +2  ; 

% add the correct names and will plot the result with vertical line on the
% best value 
figure("Name",'max depth DT')
plot(X_axis,mean_score)
title('Maximum depth - Decision tree')
xlabel('Maximum depth')
ylabel('Score')
xline(best)
legend('neg root mean squared error','Best result')