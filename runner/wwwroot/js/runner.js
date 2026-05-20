window.runnerJs = {

    initScrollSync: function (textareaId, gutterId) {
        // no-op when CodeMirror is active — CM handles scroll internally
        const ta = document.getElementById(textareaId);
        const gutter = document.getElementById(gutterId);
        if (!ta || !gutter) return;
        ta.addEventListener('scroll', function () {
            gutter.scrollTop = ta.scrollTop;
        });
    },

    updateGutter: function (gutterId, lines) {
        const gutter = document.getElementById(gutterId);
        if (!gutter) return;
        let text = '';
        for (let i = 1; i <= lines; i++) text += i + (i < lines ? '\n' : '');
        gutter.textContent = text;
    },

    reportHeight: function () {
        requestAnimationFrame(function () {
            const runner = document.querySelector('.runner');
            const h = runner ? runner.scrollHeight : 400;
            window.parent.postMessage({ type: 'runner-height', height: h + 4 }, '*');
        });
    },

    setEditorHeight: function (px) {
        const wrap = document.querySelector('.editor-wrap');
        if (wrap) wrap.style.height = px + 'px';
    },

    autoResizeAndReport: function () {},

    initResetBtn: function (btn) {
        var params = new URLSearchParams(window.location.search);
        var encoded = params.get('code');
        if (!encoded) { btn.style.display = 'none'; return; }

        var originalCode;
        try {
            var binary = atob(encoded);
            var bytes = new Uint8Array(binary.length);
            for (var i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
            originalCode = new TextDecoder('utf-8').decode(bytes);
        } catch (e) { btn.style.display = 'none'; return; }

        btn.addEventListener('click', function () {
            var ta = document.getElementById('codearea');
            if (!ta) return;
            if (ta._cmEditor) {
                ta._cmEditor.setValue(originalCode);
            } else {
                ta.value = originalCode;
                ta.dispatchEvent(new Event('input', { bubbles: true }));
            }
        });
    },

    initFullscreenBtn: function (btn) {
        var ICO_EXPAND   = '<path d="M1 4V1h3M8 1h3v3M11 8v3H8M4 11H1V8" stroke-linecap="round" stroke-linejoin="round"/>';
        var ICO_COMPRESS = '<path d="M4 1v3H1M11 4H8V1M8 11v-3h3M1 8h3v3" stroke-linecap="round" stroke-linejoin="round"/>';

        function setIcon(fs) {
            btn.querySelector('svg').innerHTML = fs ? ICO_COMPRESS : ICO_EXPAND;
            btn.title = fs ? 'Вийти з повноекранного режиму' : 'Повноекранний режим';
        }

        btn.addEventListener('click', function () {
            if (!document.fullscreenElement) {
                document.documentElement.requestFullscreen();
            } else {
                document.exitFullscreen();
            }
        });

        document.addEventListener('fullscreenchange', function () {
            setIcon(!!document.fullscreenElement);
        });
    },

    initCopyBtn: function (btn) {
        btn.addEventListener('click', function () {
            const ta = document.getElementById('codearea');
            if (!ta || !ta.value) return;
            navigator.clipboard.writeText(ta.value).then(function () {
                const orig = btn.textContent;
                btn.textContent = 'Скопійовано!';
                btn.style.color = 'var(--accent)';
                setTimeout(function () {
                    btn.textContent = orig;
                    btn.style.color = '';
                }, 1500);
            });
        });
    },

    initResizer: function (editorWrap, resizerEl) {
        const output = document.querySelector('.output');
        const outputBody = document.querySelector('.output-body');
        if (!output || !outputBody) return;

        let startY, startEditorH, startOutputH;

        resizerEl.addEventListener('mousedown', function (e) {
            startY = e.clientY;
            startEditorH = editorWrap.offsetHeight;
            startOutputH = output.offsetHeight;
            resizerEl.classList.add('dragging');
            document.body.style.cursor = 'ns-resize';
            document.body.style.userSelect = 'none';
            e.preventDefault();
        });

        document.addEventListener('mousemove', function (e) {
            if (!resizerEl.classList.contains('dragging')) return;
            const dy = e.clientY - startY;
            const total = startEditorH + startOutputH;
            const newEditorH = Math.max(60, Math.min(total - 40, startEditorH + dy));
            const newOutputH = total - newEditorH;

            editorWrap.style.flex = 'none';
            editorWrap.style.height = newEditorH + 'px';
            output.style.flex = 'none';
            output.style.height = newOutputH + 'px';
            output.style.maxHeight = 'none';
            outputBody.style.flex = '1';
            outputBody.style.minHeight = '0';
            outputBody.style.maxHeight = 'none';
        });

        document.addEventListener('mouseup', function () {
            if (!resizerEl.classList.contains('dragging')) return;
            resizerEl.classList.remove('dragging');
            document.body.style.cursor = '';
            document.body.style.userSelect = '';
        });
    },

    initCodeMirror: function (ta) {
        var CDN = 'https://cdn.jsdelivr.net/npm/codemirror@5.65.18/';

        var THEME = [
            '.CodeMirror{background:#24292e;color:#E1E4E8;font-family:"Cascadia Code","JetBrains Mono",Consolas,monospace;font-weight:400;font-size:13px;line-height:1.6;height:100%;border:none;}',
            '.CodeMirror-scroll{height:100%;}',
            '.CodeMirror-gutters{background:#24292e;border-right:1px solid #2f363d;}',
            '.CodeMirror-linenumber{color:#6A737D;padding:0 8px 0 4px;}',
            '.CodeMirror-cursor{border-left:2px solid #E1E4E8;}',
            '.CodeMirror-selected{background:#264f78;}',
            '.CodeMirror-focused .CodeMirror-selected{background:#264f78;}',
            '.cm-keyword{color:#F97583 !important;}',
            '.cm-string,.cm-string-2{color:#9ECBFF !important;}',
            '.cm-number{color:#79B8FF !important;}',
            '.cm-comment{color:#6A737D !important;font-style:italic;}',
            '.cm-variable,.cm-variable-2{color:#E1E4E8;}',
            '.cm-def{color:#B392F0 !important;}',
            '.cm-type{color:#B392F0 !important;}',
            '.cm-operator{color:#F97583 !important;}',
            '.cm-meta{color:#6A737D;}',
            '.cm-builtin{color:#79B8FF !important;}',
            '.cm-atom{color:#79B8FF !important;}',
            '.cm-property{color:#79B8FF;}',
            '.CodeMirror-matchingbracket{color:#E1E4E8 !important;outline:1px solid #6A737D;}',
            '.editor-wrap .CodeMirror{flex:1;min-width:0;}',
            '.editor-wrap .CodeMirror-scroll{overflow-x:auto;overflow-y:auto;}',
        ].join('\n');

        function injectStyle(css) {
            var s = document.createElement('style');
            s.textContent = css;
            document.head.appendChild(s);
        }

        function loadScript(src, cb) {
            var s = document.createElement('script');
            s.src = src; s.onload = cb;
            document.head.appendChild(s);
        }

        function createEditor() {
            // 1) fetch CM base CSS, 2) inject it, 3) inject our theme after
            fetch(CDN + 'lib/codemirror.css')
                .then(function (r) { return r.text(); })
                .then(function (cmCss) {
                    injectStyle(cmCss);   // CM base first
                    injectStyle(THEME);   // our theme after → always wins

                    var gutter = document.getElementById('gutter');
                    if (gutter) gutter.style.display = 'none';

                    var cm = CodeMirror.fromTextArea(ta, {
                        mode: 'text/x-csharp',
                        lineNumbers: true,
                        indentUnit: 4,
                        tabSize: 4,
                        indentWithTabs: false,
                        smartIndent: true,
                        matchBrackets: true,
                        lineWrapping: false,
                        extraKeys: {
                            'Ctrl-Enter': function () {
                                var btn = document.querySelector('.btn-primary');
                                if (btn && !btn.disabled) btn.click();
                            },
                            Tab: function (cm) { cm.replaceSelection('    '); }
                        }
                    });

                    cm.setSize('100%', '100%');

                    cm.on('change', function () {
                        ta.value = cm.getValue();
                        ta.dispatchEvent(new Event('input', { bubbles: true }));
                    });

                    ta._cmEditor = cm;
                    requestAnimationFrame(function () { cm.refresh(); });
                });
        }

        loadScript(CDN + 'lib/codemirror.js', function () {
            loadScript(CDN + 'mode/clike/clike.js', function () {
                createEditor();
            });
        });
    }

};

// Auto-inject UI elements once Blazor renders
(function () {
    function tryInject() {
        var toolbar    = document.querySelector('.toolbar');
        var editorWrap = document.querySelector('.editor-wrap');
        var output     = document.querySelector('.output');
        var ta         = document.getElementById('codearea');
        if (!toolbar || !editorWrap || !output || !ta) return false;

        var spacer = toolbar.querySelector('.spacer');

        // Copy button
        if (!document.getElementById('js-copy-btn')) {
            var btn = document.createElement('button');
            btn.id = 'js-copy-btn';
            btn.className = 'btn btn-ghost';
            btn.title = 'Скопіювати код';
            btn.innerHTML =
                '<svg class="ico" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round">' +
                '<rect x="4" y="1" width="7" height="8" rx="1"/>' +
                '<rect x="1" y="3" width="7" height="8" rx="1"/>' +
                '</svg><span>Копіювати</span>';
            toolbar.insertBefore(btn, spacer);
            window.runnerJs.initCopyBtn(btn);
        }

        // Reset button
        if (!document.getElementById('js-reset-btn')) {
            var rbtn = document.createElement('button');
            rbtn.id = 'js-reset-btn';
            rbtn.className = 'btn btn-ghost';
            rbtn.title = 'Скинути до оригіналу';
            rbtn.innerHTML =
                '<svg class="ico" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round">' +
                '<path d="M2 5a4 4 0 1 1 .5 3"/>' +
                '<path d="M2 2v3h3"/>' +
                '</svg><span>Скинути</span>';
            toolbar.insertBefore(rbtn, spacer);
            window.runnerJs.initResetBtn(rbtn);
        }

        // Fullscreen button — right side, after spacer
        if (!document.getElementById('js-fs-btn')) {
            var fsbtn = document.createElement('button');
            fsbtn.id = 'js-fs-btn';
            fsbtn.className = 'btn btn-ghost';
            fsbtn.title = 'Повноекранний режим';
            fsbtn.innerHTML =
                '<svg class="ico" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round">' +
                '<path d="M1 4V1h3M8 1h3v3M11 8v3H8M4 11H1V8"/>' +
                '</svg>';
            var status = toolbar.querySelector('.status');
            toolbar.insertBefore(fsbtn, status);
            window.runnerJs.initFullscreenBtn(fsbtn);
        }

        // Resizer
        if (!document.getElementById('js-resizer')) {
            var div = document.createElement('div');
            div.id = 'js-resizer';
            div.className = 'resizer';
            editorWrap.parentNode.insertBefore(div, output);
            window.runnerJs.initResizer(editorWrap, div);
        }

        // CodeMirror syntax highlighting
        if (!ta._cmEditor && !ta._cmPending) {
            ta._cmPending = true;
            window.runnerJs.initCodeMirror(ta);
        }

        return true;
    }

    var observer = new MutationObserver(function () {
        if (tryInject()) observer.disconnect();
    });
    observer.observe(document.body, { childList: true, subtree: true });
})();
