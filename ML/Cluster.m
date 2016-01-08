classdef Cluster
    %UNTITLED2 Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
        cluster_id;
        member_id;
        valid;
    end
    
    methods
        function obj = Cluster(id, member, v)
            if nargin > 0
              obj.cluster_id = id;
              obj.member_id = member;
              obj.valid = v;
            end
        end
    end
    
end
