function run_experiment(sessionPath)
% Run by calling: run_experiment('session.json')

SKIP_SYNC_TESTS = 1;

try
    Screen('Preference','SkipSyncTests', SKIP_SYNC_TESTS);
    session = jsondecode(fileread(sessionPath));

    % ---- keys from session.json ----
    KbName('UnifyKeyNames');
    KEY_SAME_NAME = char(session.keys.same);
    KEY_DIFF_NAME = char(session.keys.different);
    keySame = KbName(KEY_SAME_NAME);
    keyDiff = KbName(KEY_DIFF_NAME);
    keyEsc  = KbName('ESCAPE');

    AssertOpenGL;
    [w, rect] = PsychImaging('OpenWindow', 0, [0 0 0]);
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
    log.trials = repmat(trialTemplate,0,1);

    t0 = GetSecs();

    % ---- task loop ----
    for b = 1:numel(session.blocks)
        block = utilities.asstruct(session.blocks(b));

        for ph = 1:numel(block.phases)
            phase = utilities.asstruct(utilities.geti(block.phases, ph));
            phaseName = string(phase.phase);

            % ---------------- phase_start ----------------
            if phaseName == "phase_start"
                tr0 = utilities.asstruct(utilities.geti(phase.trial, 1));

                [resp, rt, tOn] = utilities.phase_start_screen( ...
                    w, rect, phase, tr0, texCache, ...
                    KEY_SAME_NAME, KEY_DIFF_NAME, keySame, keyDiff, keyEsc);

                trial = trialTemplate;
                trial.block_id     = block.block_id;
                trial.block_family = string(block.family);
                trial.trial_family = utilities.trial_family(block, tr0);
                trial.phase        = phaseName;
                trial.phase_index  = ph;
                trial.trial_index  = 0;
                trial.bg           = string(phase.bg);
                trial.hint         = string(phase.hint);
                trial.tip          = string(phase.tip);
                trial.sub_rule     = utilities.get_field_str(tr0, 'sub_rule');
                trial.ids          = utilities.get_field_strarr(tr0, 'ids');
                trial.seeds        = utilities.get_field_numarr(tr0, 'seeds');
                trial.imgs         = utilities.get_field_strarr(tr0, 'imgs');
                trial.correct      = "";
                trial.resp         = resp;
                trial.is_correct   = [];
                trial.rt           = rt;
                trial.t            = tOn - t0;

                log.trials(end+1,1) = trial; %#ok<AGROW>
                continue
            end

            % ---------------- inference/application ----------------
            if ~isfield(phase,'trials') || isempty(phase.trials)
                continue
            end

            for t = 1:numel(phase.trials)
                tr = utilities.asstruct(utilities.geti(phase.trials, t));

                [resp, rt, stimOn] = utilities.decision_screen_twoimgs( ...
                    w, rect, phase, tr, texCache, keySame, keyDiff, keyEsc);

                correct = utilities.get_field_str(tr, 'correct');
                is_correct = [];
                if correct == "same" || correct == "different"
                    is_correct = (resp == correct);
                end

                trial = trialTemplate;
                trial.block_id     = block.block_id;
                trial.block_family = string(block.family);
                trial.trial_family = utilities.trial_family(block, tr);
                trial.phase        = string(phase.phase);
                trial.phase_index  = ph;
                trial.trial_index  = t;
                trial.bg           = string(phase.bg);
                trial.hint         = string(phase.hint);
                trial.tip          = string(phase.tip);
                trial.sub_rule     = utilities.get_field_str(tr, 'sub_rule');
                trial.ids          = utilities.get_field_strarr(tr, 'ids');
                trial.seeds        = utilities.get_field_numarr(tr, 'seeds');
                trial.imgs         = utilities.get_field_strarr(tr, 'imgs');
                trial.correct      = correct;
                trial.resp         = resp;
                trial.is_correct   = is_correct;
                trial.rt           = rt;
                trial.t            = stimOn - t0;

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
