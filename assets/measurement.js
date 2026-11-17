/* Analytics only after permission. No message text, quiz answers or patient data. */
(function () {
  'use strict';
  if (window.__tifanyMeasurement) return;
  window.__tifanyMeasurement = true;
  var GA = 'G-CJ5CX7B1V5', KEY = 'tifany.analytics.v1', enabled = false, started = false;
  var banner;
  function saved() { try { return localStorage.getItem(KEY); } catch (_) { return null; } }
  function remember(value) { try { localStorage.setItem(KEY, value); } catch (_) {} }
  function enable() {
    enabled = true;
    window['ga-disable-' + GA] = false;
    if (started) {
      window.gtag('consent', 'update', {analytics_storage:'granted', ad_storage:'denied', ad_user_data:'denied', ad_personalization:'denied'});
      return;
    }
    started = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('consent', 'default', {analytics_storage:'granted', ad_storage:'denied', ad_user_data:'denied', ad_personalization:'denied'});
    window.gtag('js', new Date());
    window.gtag('config', GA, {send_page_view:false, allow_google_signals:false, allow_ad_personalization_signals:false, page_location:location.origin + location.pathname, page_referrer:document.referrer ? new URL(document.referrer).origin : ''});
    window.gtag('event', 'page_view', {send_to:GA, page_location:location.origin + location.pathname, page_referrer:document.referrer ? new URL(document.referrer).origin : '', page_title:document.title});
    var script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA;
    if (!['localhost','127.0.0.1','::1'].includes(location.hostname)) document.head.appendChild(script);
  }
  function disable() {
    enabled = false;
    window['ga-disable-' + GA] = true;
    if (window.gtag) window.gtag('consent', 'update', {analytics_storage:'denied', ad_storage:'denied', ad_user_data:'denied', ad_personalization:'denied'});
    document.cookie.split(';').forEach(function (cookie) {
      var name = cookie.split('=')[0].trim();
      if (!/^_ga(?:_|$)/.test(name)) return;
      var base = name + '=; Max-Age=0; path=/; SameSite=Lax';
      document.cookie = base;
      document.cookie = base + '; domain=' + location.hostname;
      document.cookie = base + '; domain=.' + location.hostname.replace(/^www\./, '');
    });
  }
  function show() { banner.hidden = false; }
  function choose(value) {
    remember(value);
    if (value === 'accepted') enable(); else disable();
    banner.hidden = true;
  }
  function init() {
    var style = document.createElement('style');
    style.textContent = '#cookie-choice{position:fixed;bottom:18px;left:18px;right:18px;z-index:10000;max-width:650px;background:#f4f0e9;color:#442a1e;padding:20px;border:1px solid #bfa694;border-radius:8px;box-shadow:0 8px 40px #0004;font:14px/1.5 Arial,sans-serif}#cookie-choice[hidden]{display:none}#cookie-choice p{margin:0 0 12px;color:#442a1e}#cookie-choice a{color:#442a1e}#cookie-choice .actions{display:flex;gap:10px;flex-wrap:wrap}#cookie-choice button{padding:12px 16px;cursor:pointer;border:1px solid #442a1e;border-radius:4px;background:#fff;color:#442a1e;font:inherit}#cookie-choice button:focus-visible{outline:3px solid #8b5540;outline-offset:3px}';
    document.head.appendChild(style);
    banner = document.createElement('section');
    banner.id = 'cookie-choice'; banner.setAttribute('aria-label', 'Preferências de cookies');
    banner.innerHTML = '<p>Podemos usar cookies de análise para entender as visitas e os cliques no WhatsApp? Você pode recusar e continuar navegando normalmente. <a href="/privacidade.html">Saiba mais</a>.</p><div class="actions"><button type="button" data-choice="rejected">Recusar análise</button><button type="button" data-choice="accepted">Aceitar análise</button></div>';
    document.body.appendChild(banner);
    banner.querySelectorAll('[data-choice]').forEach(function (button) { button.addEventListener('click', function () { choose(button.dataset.choice); }); });
    var pref = saved();
    banner.hidden = pref === 'accepted' || pref === 'rejected';
    if (pref === 'accepted') enable(); else disable();
    document.addEventListener('click', function (e) {
      var target = e.target && e.target.closest ? e.target : null;
      if (!target) return;
      if (target.closest('[data-cookie-settings]')) { show(); return; }
      var link = target.closest('a[href]');
      if (!enabled || !link) return;
      var url; try { url = new URL(link.href, location.href); } catch (_) { return; }
      if (url.hostname !== 'wa.me' || url.pathname !== '/5547997722437') return;
      var classes = ['header-cta','hero-cta','mobile-cta','pre-cta-btn','panel-link','proc-desc-link'];
      var origin = classes.find(function (name) { return link.classList.contains(name); }) || 'pagina';
      window.gtag('event', 'whatsapp_click', {send_to:GA, origem:origin, page_location:location.origin + location.pathname});
    }, true);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
