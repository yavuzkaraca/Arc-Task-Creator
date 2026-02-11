classdef utilities
methods(Static)

% ===================== json safety =====================
function v = geti(x, i)
    if iscell(x), v = x{i}; else, v = x(i); end
end

function s = asstruct(x)
    if iscell(x), s = x{1}; else, s = x; end
end

function c = to_cellstr(x)
    if ischar(x) || isstring(x), c = cellstr(x); else, c = x; end
end

function out = get_field_str(s, field)
    out = "";
    if isfield(s, field) && ~isempty(s.(field))
        out = string(s.(field));
    end
end

function out = get_field_strarr(s, field)
    out = strings(0,1);
    if isfield(s, field) && ~isempty(s.(field))
        out = string(s.(field));
    end
end

function out = get_field_numarr(s, field)
    out = [];
    if isfield(s, field) && ~isempty(s.(field))
        out = double(s.(field));
    end
end

function fam = trial_family(block, tr)
    if isfield(tr,'family') && ~isempty(tr.family)
        fam = string(tr.family);
    else
        fam = string(block.family);
    end
end

% ===================== logging =====================
function trialTemplate = trial_template()
    trialTemplate = struct( ...
        'block_id',[], ...
        'block_family',"", ...
        'trial_family',"", ...
        'phase',"", ...
        'phase_index',[], ...
        'trial_index',[], ...
        'bg',"", ...
        'hint',"", ...
        'tip',"", ...
        'sub_rule',"", ...
        'ids',strings(0,1), ...
        'seeds',[], ...
        'imgs',strings(0,1), ...
        'correct',"", ...
        'resp',"", ...
        'is_correct',[], ...
        'rt',[], ...
        't',[] ...
    );
end

% ===================== preloading =====================
function allImgs = collect_all_images(session)
    allImgs = {};
    for b = 1:numel(session.blocks)
        block = utilities.asstruct(session.blocks(b));
        for ph = 1:numel(block.phases)
            phase = utilities.asstruct(utilities.geti(block.phases, ph));

            if isfield(phase,'trial') && ~isempty(phase.trial)
                tr0 = utilities.asstruct(utilities.geti(phase.trial, 1));
                if isfield(tr0,'imgs') && ~isempty(tr0.imgs)
                    allImgs = [allImgs, utilities.to_cellstr(tr0.imgs)]; %#ok<AGROW>
                end
            end

            if isfield(phase,'trials') && ~isempty(phase.trials)
                for t = 1:numel(phase.trials)
                    tr = utilities.asstruct(utilities.geti(phase.trials, t));
                    if isfield(tr,'imgs') && ~isempty(tr.imgs)
                        allImgs = [allImgs, utilities.to_cellstr(tr.imgs)]; %#ok<AGROW>
                    end
                end
            end
        end
    end
    allImgs = unique(allImgs, 'stable');
end

% ===================== UI helpers =====================
function rgb = phase_bg_rgb(bgName)
    bgName = string(bgName);
    if bgName == "green"
        rgb = [0 0.45 0];
    elseif bgName == "red"
        rgb = [0.45 0 0];
    else
        rgb = [0 0 0];
    end
end

function [key, t] = wait_key(validKeys, escKey)
    % --- debounce BEFORE ---
    % If a key is still held from the previous screen, wait until release
    KbReleaseWait;

    while true
        [down, secs, kc] = KbCheck;
        if ~down
            continue
        end

        if kc(escKey)
            error('Experiment aborted (ESC).');
        end

        if any(kc(validKeys))
            key = find(kc, 1, 'first');
            t = secs;

            % --- debounce AFTER ---
            % Prevent same physical press leaking into next screen
            KbReleaseWait;
            return
        end
    end
end

% ===================== screens =====================
function [resp, rt, tOn] = phase_start_screen( ...
    w, rect, phase, tr, texCache, KEY_SAME_NAME, KEY_DIFF_NAME, keySame, keyDiff, keyEsc)

    Screen('FillRect', w, utilities.phase_bg_rgb(string(phase.bg)));
    utilities.draw_header(w, rect, phase);

    utilities.draw_two_stacked_imgs(w, rect, texCache, tr.imgs);

    tOn = Screen('Flip', w);
    [respKey, respTime] = utilities.wait_key([keySame keyDiff], keyEsc);
    rt = respTime - tOn;
    resp = "same"; if respKey == keyDiff, resp = "different"; end
end

function [resp, rt, stimOn] = decision_screen_twoimgs( ...
    w, rect, phase, tr, texCache, keySame, keyDiff, keyEsc)

    Screen('FillRect', w, utilities.phase_bg_rgb(string(phase.bg)));
    utilities.draw_header(w, rect, phase);

    utilities.draw_two_stacked_imgs(w, rect, texCache, tr.imgs);

    stimOn = Screen('Flip', w);
    [respKey, respTime] = utilities.wait_key([keySame keyDiff], keyEsc);
    rt = respTime - stimOn;
    resp = "same"; if respKey == keyDiff, resp = "different"; end
end

function draw_header(w, rect, phase)
    Screen('TextSize', w, 34);
    DrawFormattedText(w, char(string(phase.hint)), 'center', rect(4)*0.15, [1 1 1]);
    Screen('TextSize', w, 22);
    DrawFormattedText(w, char(string(phase.tip)), 'center', rect(4)*0.25, [1 1 1]);
end

function draw_two_stacked_imgs(w, rect, texCache, imgsField)
    imgs = utilities.to_cellstr(imgsField);
    if numel(imgs) < 2
        DrawFormattedText(w, '[need 2 imgs]', 'center', rect(4)*0.6, [1 1 1]);
        return
    end

    keyTop = char(imgs{1});
    keyBot = char(imgs{2});

    GAP = rect(4) * 0.02;
    wImg = rect(3) * 0.62;
    hImg = rect(4) * 0.26;

    topMargin = rect(4) * 0.34;
    bottomMargin = rect(4) * 0.06;

    availTop = topMargin;
    availBot = rect(4) - bottomMargin;

    stackH = 2*hImg + GAP;
    centerX = rect(3)/2;
    centerY = (availTop + availBot)/2;

    if stackH > (availBot - availTop)
        scale = (availBot - availTop) / stackH;
        hImg = hImg * scale;
        wImg = wImg * scale;
    end

    dstTop = CenterRectOnPointd([0 0 wImg hImg], centerX, centerY - (hImg/2 + GAP/2));
    dstBot = CenterRectOnPointd([0 0 wImg hImg], centerX, centerY + (hImg/2 + GAP/2));

    if isKey(texCache, keyTop)
        Screen('DrawTexture', w, texCache(keyTop), [], dstTop);
    else
        DrawFormattedText(w, '[missing top]', 'center', rect(4)*0.55, [1 1 1]);
    end

    if isKey(texCache, keyBot)
        Screen('DrawTexture', w, texCache(keyBot), [], dstBot);
    else
        DrawFormattedText(w, '[missing bottom]', 'center', rect(4)*0.80, [1 1 1]);
    end
end

end % methods
end % classdef
