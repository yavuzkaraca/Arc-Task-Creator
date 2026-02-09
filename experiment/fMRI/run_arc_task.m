function run_arc_task(manifestPath)

SKIP_SYNC_TESTS = 1;    % dev
DEV_WINDOWED = true;
DEV_WIN_ALPHA = 0.85;

try
    if nargin < 1 || isempty(manifestPath)
        manifestPath = 'manifest.json';
    end

    Screen('Preference','SkipSyncTests', SKIP_SYNC_TESTS);
    if DEV_WINDOWED, PsychDebugWindowConfiguration(0, DEV_WIN_ALPHA); end

    KbName('UnifyKeyNames');
    manifest = jsondecode(fileread(manifestPath));

    keySame = KbName(manifest.keys.same);
    keyDiff = KbName(manifest.keys.different);
    keyEsc  = KbName('ESCAPE');

    AssertOpenGL;
    [w, rect] = PsychImaging('OpenWindow', 0, [0 0 0]);
    Screen('ColorRange', w, 1);
    Screen('TextFont', w, 'Arial');

    baseDir = fileparts(which(manifestPath));
    if isempty(baseDir), baseDir = fileparts(manifestPath); end

    % --- preload textures referenced by manifest ---
    texCache = containers.Map();
    allImgs = collect_all_images(manifest);

    for i = 1:numel(allImgs)
        rel = char(allImgs{i});
        p = fullfile(baseDir, rel);
        im = imread(p);
        texCache(rel) = Screen('MakeTexture', w, im);
    end

    % --- log struct ---
    trialTemplate = struct('block_id',[],'family',"",'phase',"",'trial_index',[], ...
                           'img',"",'resp',"",'rt',[],'t',[]);
    log = struct;
    log.participant = manifest.participant;
    log.started_at = datestr(now,30);
    log.trials = repmat(trialTemplate,0,1);

    t0 = GetSecs();

    % --- task loop ---
    for b = 1:numel(manifest.blocks)
        block = manifest.blocks(b);

        for ph = 1:numel(block.phases)
            phase = block.phases(ph);

            % simple instruction screen
            Screen('FillRect', w, phase_bg_rgb(phase.bg));
            Screen('TextSize', w, 34);
            DrawFormattedText(w, 'Previous Rule', 'center', rect(4)*0.15, [1 1 1]);
            Screen('TextSize', w, 22);
            DrawFormattedText(w, sprintf('%s = SAME    %s = DIFFERENT\n(press either to start, ESC abort)', ...
                manifest.keys.same, manifest.keys.different), ...
                'center', rect(4)*0.25, [1 1 1]);

            % show first example image if present
            if isfield(phase,'example_images') && ~isempty(phase.example_images)
                ex = phase.example_images;
                if ischar(ex) || isstring(ex), ex = cellstr(ex); end
                key = char(ex{1});
                dst = CenterRectOnPointd([0 0 rect(3)*0.6 rect(4)*0.35], rect(3)/2, rect(4)*0.6);
                Screen('DrawTexture', w, texCache(key), [], dst);
            end

            Screen('Flip', w);
            wait_key([keySame keyDiff], keyEsc);

            % trials
            for t = 1:numel(phase.trials)
                tr = phase.trials(t);
                imgKey = char(tr.img);

                Screen('FillRect', w, phase_bg_rgb(phase.bg));
                draw_stimulus(w, rect, texCache(imgKey));
                stimOn = Screen('Flip', w);

                [respKey, respTime] = wait_key([keySame keyDiff], keyEsc);
                rt = respTime - stimOn;

                resp = "same";
                if respKey == keyDiff, resp = "different"; end

                trial = trialTemplate;
                trial.block_id = block.block_id;
                trial.family = string(block.family);
                trial.phase = string(phase.phase);
                trial.trial_index = t;
                trial.img = string(tr.img);
                trial.resp = resp;
                trial.rt = rt;
                trial.t = stimOn - t0;

                log.trials(end+1,1) = trial; %#ok<AGROW>
            end
        end
    end

    outName = sprintf('log_%s_%s.mat', string(manifest.participant), datestr(now,30));
    save(fullfile(baseDir, outName), 'log');

    Screen('CloseAll');

catch ME
    try, Screen('CloseAll'); end %#ok<TRYNC>
    rethrow(ME);
end

end

% -------- helpers --------

function allImgs = collect_all_images(manifest)
allImgs = {};
for b = 1:numel(manifest.blocks)
    for ph = 1:numel(manifest.blocks(b).phases)
        phase = manifest.blocks(b).phases(ph);

        if isfield(phase,'example_images') && ~isempty(phase.example_images)
            ex = phase.example_images;
            if ischar(ex) || isstring(ex), ex = cellstr(ex); end
            allImgs = [allImgs, ex(:)']; %#ok<AGROW>
        end

        if isfield(phase,'trials') && ~isempty(phase.trials)
            for t = 1:numel(phase.trials)
                allImgs{end+1} = char(phase.trials(t).img); %#ok<AGROW>
            end
        end
    end
end
[~, ia] = unique(allImgs, 'stable');
allImgs = allImgs(sort(ia));
end

function rgb = phase_bg_rgb(bg)
if isstring(bg) || ischar(bg), s = lower(char(bg)); else, s = 'black'; end
switch s
    case {'green','g'}, rgb = [0 0.25 0];
    case {'red','r'},   rgb = [0.25 0 0];
    case {'blue','b'},  rgb = [0 0 0.25];
    case {'gray','grey'}, rgb = [0.15 0.15 0.15];
    case {'white'},     rgb = [1 1 1];
    otherwise,          rgb = [0 0 0];
end
end

function draw_stimulus(w, rect, tex)
dst = CenterRectOnPointd([0 0 rect(3)*0.80 rect(4)*0.80], rect(3)/2, rect(4)/2);
Screen('DrawTexture', w, tex, [], dst);
end

function [k, t] = wait_key(allowed, keyEsc)
while true
    [down, secs, kc] = KbCheck;
    if down
        if kc(keyEsc), error('Aborted by user (ESC).'); end
        k = find(kc,1);
        if any(k == allowed)
            t = secs;
            KbReleaseWait;
            return
        end
    end
end
end
