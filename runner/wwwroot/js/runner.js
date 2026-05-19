window.runnerJs = {

    initScrollSync: function (textareaId, gutterId) {
        const ta = document.getElementById(textareaId);
        const gutter = document.getElementById(gutterId);
        if (!ta || !gutter) return;
        ta.addEventListener('scroll', function () {
            gutter.scrollTop = ta.scrollTop;
        });
    },

    autoResizeAndReport: function (textareaId) {
        const ta = document.getElementById(textareaId);
        if (ta) {
            ta.style.height = 'auto';
            ta.style.height = ta.scrollHeight + 'px';
            const gutter = document.getElementById('gutter');
            if (gutter) gutter.style.minHeight = ta.scrollHeight + 'px';
        }
        requestAnimationFrame(function () {
            const runner = document.querySelector('.runner');
            const h = runner ? runner.offsetHeight : 400;
            window.parent.postMessage({ type: 'runner-height', height: h + 4 }, '*');
        });
    },

    reportHeight: function () {
        requestAnimationFrame(function () {
            const runner = document.querySelector('.runner');
            const h = runner ? runner.offsetHeight : 400;
            window.parent.postMessage({ type: 'runner-height', height: h + 4 }, '*');
        });
    }

};
