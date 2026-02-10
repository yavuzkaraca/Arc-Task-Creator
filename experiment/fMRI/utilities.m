classdef utilities
methods(Static)


function allImgs = collect_all_images(manifest)
    allImgs = {};

    for b = 1:numel(manifest.blocks)
        for ph = 1:numel(manifest.blocks(b).phases)
            phase = manifest.blocks(b).phases(ph);

            % ---- example images (2 stacked, but still just a list of paths) ----
            if isfield(phase,'example_images') && ~isempty(phase.example_images)
                ex = phase.example_images;
                if ischar(ex) || isstring(ex), ex = cellstr(ex); end
                allImgs = [allImgs, ex(:)']; %#ok<AGROW>
            end

            % ---- trial images: NEW manifest uses tr.imgs (two paths) ----
            if isfield(phase,'trials') && ~isempty(phase.trials)
                for t = 1:numel(phase.trials)
                    tr = phase.trials(t);

                    if isfield(tr,'imgs') && ~isempty(tr.imgs)
                        imgs = tr.imgs;
                        if ischar(imgs) || isstring(imgs), imgs = cellstr(imgs); end
                        allImgs = [allImgs, imgs(:)']; %#ok<AGROW>
                    elseif isfield(tr,'img') && ~isempty(tr.img)
                        % backward compatibility with old manifests
                        allImgs{end+1} = char(tr.img); %#ok<AGROW>
                    end
                end
            end
        end
    end

    % remove duplicates, preserve order
    [~, ia] = unique(allImgs, 'stable');
    allImgs = allImgs(ia);
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

end
end
