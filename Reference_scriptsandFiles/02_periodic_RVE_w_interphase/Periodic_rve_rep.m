%% SCRIPT FOR GENERATION OF PERIODIC RVE
% ABEDIN GAGANI 2017 (c)
% All dimensions are in micron
clear
close all
%% Determination of number of fibers
vf0 = 0.60;      % Desired fiber volume fraction
L = 100;        % Length of the RVE
r = 8;          % Fiber radius
d = 2.005*r;      % Minimum distance between fibers
t = 0.01;      % Interphase thickness
% Same value as suggested by Yang et al. (2012)
RVET = 10;     % RVE thickness
% Minimum distance between fibers
% Objective volume fraction, RVE size, fiber radius
% We ll now compute the n° of fibers
nf0 = vf0*(L^2)/(pi*r^2);   % Objective number of fibers
N = round(nf0);            % It must be an integer
% we rounded to a integer n° of fibers
% we recompute now the volume fraction
vf = N * pi * r^2 / (L^2);         % Effective volume fraction

Right = [r, 0];
Left = [-r, 0];
Top = [0, r];
Bottom = [0, -r];
EdgeR = [L, 0];     % RVE Right side
EdgeL = [-L, 0];    % RVE Left side
EdgeT = [0, L];     % RVE Top side
EdgeB = [0, -L];    % RVE Bottom side

M = 0;          % Counter for fibers on the RVE's sides
P = 0;          % Counter for fibers on the RVE's corners

%% Generation of non overlapping random circles
newpt = @() rand([1,2]) * L;  % function to generate a new candidate point

%xy = newpt();  % matrix to store XY coordinates
xy=[];          % creates an empty matrix to store the fibers'centers
fails = 0;      % to avoid looping forever
cont = 0;       % variable for identification of fibers'positions
% cont=0 --> fiber inside the RVE
% cont=1 --> fiber on the RVE's side
% cont=2 --> fiber on the RVE's corner
f=0

for f = 0:1000000
while size(xy,1) < N+M+P
    % generate new point and test distance
    pt = newpt();
    cont = 0;
    if pt(1) + Right(1) > EdgeR(1)
        if pt(2) + Top(2) > EdgeT(2)
           pt_1= pt - EdgeR;
           pt_2= pt - EdgeT;
           pt_3= pt - EdgeR - EdgeT;
           cont = 2;
        elseif pt(2) + Bottom(2) < 0
               pt_1= pt + EdgeL;
               pt_2= pt + EdgeT;
               pt_3= pt + EdgeL + EdgeT;
               cont = 2;
        else
        pt_lat = pt + EdgeL;
        cont = 1;
        end
    elseif pt(1) + Left(1) < 0
        if pt(2) + Top(2) > L
           pt_1= pt + EdgeR;
           pt_2= pt - EdgeT;
           pt_3= pt + EdgeR - EdgeT;
           cont = 2;
        elseif pt(2) + Bottom(2) < 0
               pt_1= pt + EdgeR;
               pt_2= pt + EdgeT;
               pt_3= pt + EdgeR + EdgeT;
               cont = 2;
        else
           pt_lat = pt + EdgeR;
           cont = 1;
        end
    elseif pt(2) + Top(2) > L
        if pt(1) + Right(1) > L
           pt_1= pt - EdgeR;
           pt_2= pt - EdgeT;
           pt_3= pt - EdgeR - EdgeT;
           cont = 2;
        elseif pt(1) + Left(1) < 0
           pt_1= pt + EdgeR;
           pt_2= pt - EdgeT;
           pt_3= pt + EdgeR - EdgeT;
           cont = 2;
        else        
           pt_lat = pt - EdgeT;
           cont = 1;
        end
    elseif pt(2) + Bottom(2) < 0
        if pt(1) + Right(1) > L
           pt_1= pt - EdgeR;
           pt_2= pt + EdgeT;
           pt_3= pt - EdgeR + EdgeT;
           cont = 2;
        elseif pt(1) + Left(1) < 0
           pt_1= pt + EdgeR;
           pt_2= pt + EdgeT;
           pt_3= pt + EdgeR + EdgeT;
           cont = 2;
        else   
           pt_lat = pt + EdgeT;
           cont = 1;
        end
    else cont = 0; % The fiber is inside the RVE
    end
    
    if size(xy,1)==0
        if cont == 2
            xy = [xy; pt; pt_1; pt_2; pt_3];  % add four periodic fibers
            P = P + 3;
        elseif cont == 1
            xy = [xy; pt; pt_lat];  % add two periodic fibers
            M = M + 1;
        else
            xy = [xy; pt];  % add one fiber
        end
    else
        if cont == 2 && all(pdist2(xy, pt) > d) && all(pdist2(xy, pt_1) > d) && all(pdist2(xy, pt_2) > d) && all(pdist2(xy, pt_3) > d)
            xy = [xy; pt; pt_1; pt_2; pt_3];  % add it
            fails = 0;      % reset failure counter
            P = P + 3;
        elseif cont == 1 && all(pdist2(xy, pt) > d) && all(pdist2(xy, pt_lat) > d)
            xy = [xy; pt; pt_lat];  % add it
            fails = 0;      % reset failure counter
            M = M + 1;
        elseif all(pdist2(xy, pt) > d) && cont == 0
            xy = [xy; pt];  % add it
            fails = 0;      % reset failure counter
        else
            % increase failure counter,
            fails = fails + 1;
            % give up if exceeded some threshold
            if fails > 50000
                error('this is taking too long...');
            end
        end
    end
        f = f+1
end
        %% Per debugging
    if 0
        clf
        for i=1:size(xy,1)
    viscircles([xy(i,1), xy(i,2)], r);
        end
        hold on
        plot([0,0,L,L,0],[0,L,L,0,0],'r-')
        axis equal
        
        keyboard
    end
    %%
end




%% plot
%plot(xy(:,1), xy(:,2), 'x'), hold on
for i=1:size(xy,1)
    viscircles([xy(i,1), xy(i,2)], r);
end
if 0 % Set 0 if we don't want to create interphase
for i=1:size(xy,1)
    viscircles([xy(i,1), xy(i,2)], r+t);
end
end
%hold off
hold on
plot([0,0,L,L,0],[0,L,L,0,0],'r-')
axis equal
%% Print inp file ABAQUS
fid = fopen('RVE_input.py', 'w') ;                         % Opens file for writing

fprintf(fid,['# Input file - random periodic RVE \n# Abedin Gagani 2017 (c) \n'...
    'from part import * \nfrom material import * \nfrom section import * \n'...
'from assembly import *\nfrom step import *\nfrom interaction import *\n'...
'from load import *\nfrom mesh import *\nfrom optimization import *\n'...
'from job import *\nfrom sketch import *\nfrom visualization import *\n'...
'from connectorBehavior import *\n']);
fprintf(fid,['mdb.models[''Model-1''].ConstrainedSketch(name=''__profile__'', sheetSize=', num2str(2*L),'.0)\n']);
fprintf(fid,['mdb.models[''Model-1''].sketches[''__profile__''].rectangle(point1=(0.0, 0.0),\n']);
fprintf(fid,['    point2=(',num2str(L),'.0, ',num2str(L),'.0))\n']);
fprintf(fid,['mdb.models[''Model-1''].Part(dimensionality=THREE_D, name=''RVE-3D'', type=\n']);
fprintf(fid,['    DEFORMABLE_BODY)\n']);
fprintf(fid,['mdb.models[''Model-1''].parts[''RVE-3D''].BaseSolidExtrude(depth=',num2str(RVET),'.0, sketch=\n']);
fprintf(fid,['    mdb.models[''Model-1''].sketches[''__profile__''])\n']);
fprintf(fid,['del mdb.models[''Model-1''].sketches[''__profile__'']\n']);
fprintf(fid,['mdb.models[''Model-1''].ConstrainedSketch(gridSpacing=10.71, name=''__profile__'',\n']);
fprintf(fid,['    sheetSize=428.48, transform=\n']);
fprintf(fid,['    mdb.models[''Model-1''].parts[''RVE-3D''].MakeSketchTransform(\n']);
fprintf(fid,['    sketchPlane=mdb.models[''Model-1''].parts[''RVE-3D''].faces[4],\n']);
fprintf(fid,['    sketchPlaneSide=SIDE1,\n']);
fprintf(fid,'    sketchUpEdge=mdb.models[''Model-1''].parts[''RVE-3D''].edges[7],\n');
fprintf(fid,['    sketchOrientation=RIGHT, origin=(0.0, 0.0, ',num2str(RVET),'.0)))\n']);
fprintf(fid,'mdb.models[''Model-1''].parts[''RVE-3D''].projectReferencesOntoSketch(filter=\n');
fprintf(fid,'    COPLANAR_EDGES, sketch=mdb.models[''Model-1''].sketches[''__profile__''])\n');

% Save fibers
for i = 1:size(xy,1)
     fprintf(fid,['mdb.models[''Model-1''].sketches[''__profile__''].CircleByCenterPerimeter(center=(',num2str(xy(i,1)),', ',num2str(xy(i,2)),'), point1=(',num2str(xy(i,1)),', ',num2str(xy(i,2)+r),'))\n']);
end
fprintf(fid,'# Interphase\n');
% Save interphases
if 1 % Set 0 if we don't want to create interphase
for i = 1:size(xy,1)
     fprintf(fid,['mdb.models[''Model-1''].sketches[''__profile__''].CircleByCenterPerimeter(center=(',num2str(xy(i,1)),', ',num2str(xy(i,2)),'), point1=(',num2str(xy(i,1)),', ',num2str(xy(i,2)+r+t),'))\n']);
end
end
fprintf(fid,'mdb.models[''Model-1''].parts[''RVE-3D''].PartitionFaceBySketch(faces=\n');
fprintf(fid,'    mdb.models[''Model-1''].parts[''RVE-3D''].faces.getSequenceFromMask((''[#10 ]'',\n');
fprintf(fid,'    ), ), sketch=mdb.models[''Model-1''].sketches[''__profile__''], sketchUpEdge=\n');
fprintf(fid,'    mdb.models[''Model-1''].parts[''RVE-3D''].edges[7])\n');


 fclose(fid) ;  
