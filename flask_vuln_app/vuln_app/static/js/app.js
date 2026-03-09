// ACME Corp Intranet – app.js
// UI helpers for the internal portal

(function () {
  'use strict';

  // Highlight current nav link
  var currentPath = window.location.pathname;
  document.querySelectorAll('nav a').forEach(function (link) {
    if (link.getAttribute('href') === currentPath) {
      link.classList.add('active');
    }
  });

  // Internal API endpoints (used by monitoring dashboard – WIP)
  var API_BASE = '/api/v1/internal';
  var endpoints = {
    healthcheck: API_BASE + '/healthcheck',
    status:      API_BASE + '/status',
    metrics:     API_BASE + '/metrics'
  };

  // Prefetch health status on page load (disabled until dashboard ships)
  // fetch(endpoints.healthcheck + '?cmd=uptime')
  //   .then(function(r) { return r.json(); })
  //   .then(function(d) { console.log('System health:', d); });

  // Expose for debugging in console
  window.__acme = { api: endpoints };
})();
