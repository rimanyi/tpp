window.MathJax = {
  tex: {
    inlineMath: [["\\(", "\\)"]],
    displayMath: [["\\[", "\\]"]],
    processEscapes: true,
    processEnvironments: true
  },
  options: {
    ignoreHtmlClass: "tpp-nomath"
  }
};

// MathJax typesets a freshly loaded page by itself. The code below is needed only if the theme's
// "instant navigation" is ever switched on (pages are then swapped without a reload, and the new
// content has to be typeset by hand). It must not run on the first load: clearing MathJax's cache
// after the page has been typeset removes the styles that draw the characters, and every formula
// on the page becomes invisible.
let tppFirstLoad = true;
document$.subscribe(() => {
  if (tppFirstLoad) {
    tppFirstLoad = false;
    return;
  }
  if (window.MathJax && MathJax.typesetPromise) {
    if (MathJax.startup.output && MathJax.startup.output.clearCache) MathJax.startup.output.clearCache();
    MathJax.typesetClear();
    MathJax.texReset();
    MathJax.typesetPromise();
  }
});
