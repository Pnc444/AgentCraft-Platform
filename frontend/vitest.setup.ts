/**
 * jsdom does not implement scrolling. Components that scroll a pane after a
 * slide change (PaginatedExam's rAF scroll-to-top, and anything like it) would
 * otherwise throw unhandled "Not implemented" errors *after* their tests have
 * already passed — 39 green tests with two red errors underneath, which trains
 * everyone to ignore red. Scroll position is not something these tests assert,
 * so a no-op is the honest stub.
 */
Element.prototype.scrollTo = () => {};
window.scrollTo = () => {};
