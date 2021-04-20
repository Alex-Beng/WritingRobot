clear, clc, close all

getWaypoints;

ik = inverseKinematics('RigidBodyTree',gen3);
ikWeights = [1 1 1 1 1 1];
ikInitGuess = gen3.homeConfiguration;

% plot all waypoints
show(gen3,jointAnglesHome','Frames','off','PreservePlot',false);
xlim([-1 1]), ylim([-1 1]), zlim([0 1.2])
hold on
hTraj = plot3(waypoints(1,1),waypoints(2,1),waypoints(3,1),'b.-');
% plot3(waypoints(1,:),waypoints(2,:),waypoints(3,:),'ro','LineWidth',1);

trajType = 'quintic';
switch trajType
case 'trap'
    [q,qd,qdd] = trapveltraj(waypoints,numel(trajTimes));
                        
case 'cubic'
    [q,qd,qdd] = cubicpolytraj(waypoints,waypointTimes,trajTimes);
    
case 'quintic'
    [q,qd,qdd] = quinticpolytraj(waypoints,waypointTimes,trajTimes);
    
case 'bspline'
    ctrlpoints = waypoints; % Can adapt this as needed
    [q,qd,qdd] = bsplinepolytraj(ctrlpoints,waypointTimes([1 end]),trajTimes);
    
otherwise
    error('Invalid trajectory type! Use ''trap'', ''cubic'', ''quintic'', or ''bspline''');
end

% plot trajector s

set(hTraj,'xdata',q(1,:),'ydata',q(2,:),'zdata',q(3,:));

%% Trajectory following loop
for idx = 1:numel(trajTimes) 
    % Solve IK
    tgtPose = trvec2tform(q(:,idx)');
    [config,info] = ik(eeName,tgtPose,ikWeights,ikInitGuess);
    ikInitGuess = config;

    % Show the robot
    show(gen3,config,'Frames','off','PreservePlot',false);
    title(['Trajectory at t = ' num2str(trajTimes(idx))])
    drawnow    
end