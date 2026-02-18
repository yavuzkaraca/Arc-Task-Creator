function run_experiment(sessionPath)
% Run by calling: run_experiment('session.json')

SKIP_SYNC_TESTS = 1;

try
    Screen('Preference','SkipSyncTests', SKIP_SYNC_TESTS);
    session = jsondecode(fileread(sessionPath));
    session = utilities.normalize_session(session);

    % ---- keys from session.json ----
    KbName('UnifyKeyNames');
    keySame = KbName(char(session.keys.same));
    keyDiff = KbName(char(session.keys.different));
    keyEsc  = KbName('ESCAPE');

    % ---- window ----
    AssertOpenGL;
    winRect = [0 0 1600 1600];  % [left top right bottom]
    [w, rect] = PsychImaging('OpenWindow', 0, [0 0 0], winRect);
    Screen('ColorRange', w, 1);
    Screen('TextFont', w, 'Arial');

    baseDir = fileparts(sessionPath);

    % ---- preload textures ----
    texCache = containers.Map();
    allImgs = utilities.collect_all_images(session);
    for i = 1:numel(allImgs)
        rel = char(allImgs{i});
        p = fullfile(baseDir, rel);

        im = imread(p);
        texCache(rel) = Screen('MakeTexture', w, im);
    end

    % ---- log init ----
    trialTemplate = utilities.trial_template();
    log = struct;
    log.participant = string(session.participant);
    log.started_at  = datestr(now,30);
    log.trials = repmat(trialTemplate, 0, 1);

    t0 = GetSecs();

    % ---- task loop ----
    for b = 1:numel(session.blocks)
        block = session.blocks(b);

        for ph = 1:numel(block.phases)
            phase = block.phases(ph);
            phaseName = string(phase.phase);

            % ---------- phase_start: single trial stored in phase.trial ----------
            if phaseName == "phase_start"
                if isfield(phase,'trial') && ~isempty(phase.trial)
                    tr0 = phase.trial(1);
                else
                    tr0 = struct;
                end

                [resp, rt, tOn] = utilities.twoimg_screen( ...
                    w, rect, phase, tr0, texCache, keySame, keyDiff, keyEsc);

                trial = utilities.make_trial( ...
                    trialTemplate, block, phase, ph, 0, tr0, resp, rt, tOn, t0);

                log.trials(end+1,1) = trial; %#ok<AGROW>
                continue
            end

            % ---------- inference/application: multiple trials in phase.trials ----------
            if ~isfield(phase,'trials') || isempty(phase.trials)
                continue
            end

            for t = 1:numel(phase.trials)
                tr = phase.trials(t);

                [resp, rt, tOn] = utilities.twoimg_screen( ...
                    w, rect, phase, tr, texCache, keySame, keyDiff, keyEsc);

                trial = utilities.make_trial( ...
                    trialTemplate, block, phase, ph, t, tr, resp, rt, tOn, t0);

                log.trials(end+1,1) = trial; %#ok<AGROW>
            end
        end
    end

    % ---- save log ----
    outName = sprintf('log_%s_%s.mat', string(session.participant), datestr(now,30));
    save(fullfile(baseDir, outName), 'log');

    Screen('CloseAll');

catch ME
    try, Screen('CloseAll'); end %#ok<TRYNC>
    rethrow(ME);
end
end
