%% reset
clear all
clc
load distmtx.mat
load urls
threshold = 26;

%% get distant matrix
% convert back to the format that linkage can process
[numNode, ~] = size(distmtx);
distmtx = squareform(distmtx);

% construct the hierarchical cluster tree
Z = linkage(distmtx, 'complete');
dendrogram(Z,0)

%% initialize cluster array
% Initialize the cluster array
cluster_arr(1,numNode) = Cluster(0,0,0);
for i=1:numNode
   cluster_arr(i).cluster_id = i;
   cluster_arr(i).member_id = i;
   cluster_arr(i).valid = 1;
end


%% loop to get the result
ii=1;
top_idx = numNode;
max_dist = 0;

[~,sizeC] = size(cluster_arr);
while sizeC >= threshold
    T = Z(ii,:);
    top_idx = top_idx + 1;
    
    if T(3) > max_dist
       max_dist = T(3); 
    end
    % pop
    clusterA = cluster_arr(T(1));
    clusterB = cluster_arr(T(2));
    cluster_arr(T(1)).valid = 0;
    cluster_arr(T(2)).valid = 0;
    
    if clusterA.valid ==0 || clusterB.valid==0
        fprintf('this is bull shit');
        break;
    end
    
    % merge
    temp_cluster = Cluster(top_idx, [clusterA.member_id, clusterB.member_id], 1);
    
    % push
    cluster_arr(end+1) = temp_cluster;
    
    % indexing
    sizeC = sizeC - 1;
    ii = ii + 1;
end

%% output labeled data
label = 1;
[~,sizeC] = size(cluster_arr);
fileID = fopen('../label','w');
for ii=1:sizeC
   if cluster_arr(ii).valid
       member_list = cluster_arr(ii).member_id;
       [~,length] = size(member_list);
       for jj=1:length
           fprintf(fileID, '%s %d ', strtrim( urls(member_list(jj),:) ), label);
       end
       label = label + 1;
   end
end


%% plot the result
dendrogram(Z,0)
hold on
a = xlim;
plot([a(1),a(2)],[max_dist,max_dist],'r-')
title('Dendrogram');
hold off
