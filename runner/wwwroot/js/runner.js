window.runnerJs = {

    initScrollSync: function (textareaId, gutterId) {
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

    // stub for backward compat with cached Blazor — intentionally does nothing
    autoResizeAndReport: function () {},

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
    }

};

// Auto-inject UI elements once Blazor renders
(function () {
    function tryInject() {
        const toolbar = document.querySelector('.toolbar');
        const editorWrap = document.querySelector('.editor-wrap');
        const output = document.querySelector('.output');
        if (!toolbar || !editorWrap || !output) return false;

        // Copy button — inserted before the spacer
        if (!document.getElementById('js-copy-btn')) {
            const spacer = toolbar.querySelector('.spacer');
            const btn = document.createElement('button');
            btn.id = 'js-copy-btn';
            btn.className = 'btn btn-ghost';
            btn.title = 'Скопіювати код';
            btn.innerHTML =
                '<svg class="ico" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round">' +
                '<rect x="4" y="1" width="7" height="8" rx="1"/>' +
                '<rect x="1" y="3" width="7" height="8" rx="1"/>' +
                '</svg>' +
                '<span>Копіювати</span>';
            toolbar.insertBefore(btn, spacer);
            window.runnerJs.initCopyBtn(btn);
        }

        // Resizer between editor and output
        if (!document.getElementById('js-resizer')) {
            const div = document.createElement('div');
            div.id = 'js-resizer';
            div.className = 'resizer';
            editorWrap.parentNode.insertBefore(div, output);
            window.runnerJs.initResizer(editorWrap, div);
        }

        return true;
    }

    const observer = new MutationObserver(function () {
        if (tryInject()) observer.disconnect();
    });
    observer.observe(document.body, { childList: true, subtree: true });
})();
