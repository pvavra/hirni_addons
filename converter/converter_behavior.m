function converter_behavior(filenameZip, subject, dirBids, session)
%% create temporary folder in which to work
[~,name,~] = fileparts(tempname);
dirTmp = sprintf('%sHIRNI_ADDON_%s',tempdir,name);
if exist(dirTmp,'dir')
    MAX_TRIES = 100000;
    for i = 1:MAX_TRIES
        dirTmpNext = sprintf('%s%i',dirTmp,randi(MAX_TRIES));
        if ~exist(dirTmpNext,'dir')
            dirTmp = dirTmpNext;
        end
    end
end
fprintf('creating tmp directory: %s\n',dirTmp);
mkdir(dirTmp)

%% make sure the file is 'get'
fullpathZip = sprintf('%s/%s', dirBids,filenameZip);
unix(sprintf('datalad get %s',fullpathZip));

if exist(fullpathZip ,'file')
    %% unzip input file into tmp dir
    unzip(fullpathZip ,dirTmp)

    %% list all files
    listing = dir(sprintf('%s/*.mat',dirTmp));

    %% convert each run to events.tsv
    switch session
        case {'001','002','003'}
            assert(length(listing) == 4, ...
                'wrong number of files found: %i',length(listing));
        case '004'
            assert(length(listing) == 9, ...
                'wrong number of files found: %i',length(listing));
        otherwise
            error('unknown session number %i',session);
    end

    for iFile = 1:length(listing)
        dirOutput = sprintf('%s/sub-%s/ses-%s/func',...
            dirBids,subject,session);
        % make sure output dir exists (esp for behavioral-only sessions)
        [~,~,~] = mkdir(dirOutput);

        [~,name,~] = fileparts(listing(iFile).name);

        % extract task-name from filename
        task = ExtractTaskName(name);

        % define TSV
        filenameTSV = sprintf('%s/%s_events.tsv',dirOutput,name);

        % load mat file content
        d = load(sprintf('%s/%s',listing(iFile).folder,listing(iFile).name));

        % convert content
        if strcmp(task,'localizer')
            t = convertLocalizer(d);
        else
            t = convert(d, session);
        end

        fprintf('writing file %s\n',filenameTSV);
        writetable(...
            t,...
            filenameTSV,...
            'Delimiter','tab',...
            'FileType','text',...
            'WriteVariableNames',1,...
            'WriteRowNames', 0);
    end
else
    fprintf('file was not found!\n')
end


% remove tmpDir
rmdir(dirTmp,'s')

end

function t = convert(d, session)

% define short/long
short = 0.5; long = 1.5;
nTrials = 100;

%% Simple sanity checks
assert(all(ismember(d.T.delayCueTarget,[short, long])))
assert(length(d.T.timestampTargetOn) == nTrials)

%%  infer block type
% if first half of trials has more short than long delays, short are
% expected, otherwise unexpected
if sum(d.T.delayCueTarget(1:50) == short) > 25
    shortBlockFirst = 1;
else
    shortBlockFirst = 0;
end

%% define trial type
isShort = d.T.delayCueTarget == short;
if shortBlockFirst
    expectingShort = [ones(50,1); zeros(50,1)];
else
    expectingShort = [ones(50,1); zeros(50,1)];
end

% using chmod-like trick to convert
trial_type_integer = isShort + 10 * expectingShort;
trial_type = arrayfun(@mapTrialType, trial_type_integer,...
    'UniformOutput',0);

%% define event onsets --- using Target Onset

if ismember(session,{'001','004'})
    time_offset = d.P.timestampsWaitForScanner(2);
else
    time_offset = d.T.timestampStartFirstBlock; % just use arbitrary timestamps
end

onset = d.T.timestampTargetOn - time_offset; % the second timestamp happened after first scanner-trigger
duration = d.T.durationTarget * d.P.ifi;

response_time = d.T.RT;

%% convert vectors into table
t = table(onset,duration, trial_type, response_time);

end

function label = mapTrialType(i)
switch i
    case 0
        label = 'longExpected';
    case 1
        label = 'shortUnexpected';
    case 10
        label = 'longUnexpected';
    case 11
        label = 'shortExpected';
end
end


function t = convertLocalizer(d)

time_offset = d.P.timestampsWaitForScanner(2);

onset_audio = d.T.timestampAudioOn - time_offset;
onset_visual = d.T.timestampVisualOn - time_offset;

duration_audio = d.T.timestampAudioOff - d.T.timestampAudioOn;
duration_visual = d.T.timestampVisualOff - d.T.timestampVisualOn;

onset = [onset_audio onset_visual];
duration = [duration_audio duration_visual];
trial_type = [...
    cellstr(repmat('audio',size(onset_audio))); ...
    cellstr(repmat('visual',size(onset_visual))) ...
    ];

% sort onsets by increasing time
[onset,indices] = sort(onset);
duration = duration(indices);
trial_type = trial_type(indices);

t = table(onset,duration, trial_type);

end


function task = ExtractTaskName( name )

task = '';

C = strsplit(name,'_');
for i = 1:numel(C)
    CC = strsplit(C{i},'-');
    if strcmp(CC{1},'task')
        task = CC{2};
    end
end

end
