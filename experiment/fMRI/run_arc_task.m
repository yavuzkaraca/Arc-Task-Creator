function run_arc_task(manifestPath)
% Run by calling run_arc_task('manifest.json')

SKIP_SYNC_TESTS = 1;    % dev: skip monitor timing calibration warnings

try
    Screen('Preference','SkipSyncTests', SKIP_SYNC_TESTS);
    manifest = jsondecode(fileread(manifestPath));

    % Keyboard button mappings
    KbName('UnifyKeyNames');
    keySame = KbName(manifest.keys.same);
    keyDiff = KbName(manifest.keys.different);
    keyEsc  = KbName('ESCAPE');

    AssertOpenGL; % Ensure ptb running with OpenGL support
    [w, rect] = PsychImaging('OpenWindow', 0, [0 0 0]); % screen id, [r,g,b]
    Screen('ColorRange', w, 1);
    Screen('TextFont', w, 'Arial');

    baseDir = fileparts(manifestPath);

    % --- preload textures referenced by manifest ---
    % bc loading images during trials would cause timing stutter
    texCache = containers.Map();
    allImgs = utilities.collect_all_images(manifest);

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
            Screen('FillRect', w, utilities.phase_bg_rgb(phase.bg));
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
            utilities.wait_key([keySame keyDiff], keyEsc);

            % trials
            for t = 1:numel(phase.trials)
                tr = phase.trials(t);
                imgKey = char(tr.img);

                Screen('FillRect', w, utilities.phase_bg_rgb(phase.bg));
                utilities.draw_stimulus(w, rect, texCache(imgKey));
                stimOn = Screen('Flip', w);

                [respKey, respTime] = utilities.wait_key([keySame keyDiff], keyEsc);
                rt = respTime - stimOn;

                resp = "same";
                if respKey == keyDiff, resp = "different"; end

                % log everything for the trial (which is a single row)
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

    % Build a log file in the same folder and save log struct there
    outName = sprintf('log_%s_%s.mat', string(manifest.participant), datestr(now,30));
    save(fullfile(baseDir, outName), 'log');

    Screen('CloseAll');

catch ME
    try, Screen('CloseAll'); end % close display even if the script errors
    rethrow(ME); % so that original error is accessible
end

end