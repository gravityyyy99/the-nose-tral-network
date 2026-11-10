"""Aroma-GPT, a project called The Nose-tral Network. Run with `streamlit run app.py`."""
import json
import os
from urllib.parse import urlparse

import streamlit as st
import streamlit.components.v1 as components

import about_page
import docs_pages
import journey_page
import keywords_page
import site_config as cfg
import sniff_page
import ui

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
st.set_page_config(page_title="Aroma-GPT | The Nose-tral Network", layout="wide",
                   page_icon=os.path.join(ASSETS, "mark.svg"),
                   initial_sidebar_state="collapsed")   # menu starts closed on every refresh
st.session_state.setdefault("dark", True)   # new visitors land in dark mode
ui.inject_css()


def _home_url():
    """Home page URL of this app (works locally and once deployed); None if unknown."""
    try:
        u = urlparse(str(st.context.url))
        if u.scheme in ("http", "https") and u.netloc:
            return f"{u.scheme}://{u.netloc}/"
    except Exception:
        pass
    return None


# logo at the top of the menu (light or dark version); clicking it reloads the home page
logo = "logo_dark.svg" if ui.is_dark() else "logo.svg"
st.logo(os.path.join(ASSETS, logo), icon_image=os.path.join(ASSETS, "mark.svg"),
        size="large")   # no anchor: a plain click handler below reloads the home page in the same tab

# Page-level behaviour, injected once into the main page (so it survives re-renders):
#  - clicking the logo reloads the home page in the SAME tab
#  - the menu starts closed after every refresh (Streamlit would otherwise remember it open)
#  - the header (and the day/night switch) slide away on scroll down and return on scroll up
PAGE_JS = r"""
(function () {
  if (window.__aromaBoot) return; window.__aromaBoot = true;
  document.addEventListener('click', function (e) {
    var t = e.target && e.target.closest && e.target.closest(
      'img[data-testid="stLogo"],[data-testid="stLogoLink"],[data-testid="stSidebarLogo"],[data-testid="stHeaderLogo"]');
    if (!t) return; e.preventDefault(); e.stopPropagation(); window.location.assign(window.location.origin + '/');
  }, true);
  // choosing a section in the menu closes the menu (it can be reopened from the header)
  var closeMenu = function () {
    var b = document.querySelector('[data-testid="stSidebarCollapseButton"] button') || document.querySelector('[data-testid="stSidebarCollapseButton"]');
    if (b && b.offsetParent !== null) b.click();
  };
  document.addEventListener('click', function (e) {
    var a = e.target && e.target.closest && e.target.closest('[data-testid="stSidebarNav"] a, [data-testid="stSidebarNavLink"]');
    if (a) setTimeout(closeMenu, 120);   // once, right after the click, so it glides shut with the page change
  }, true);
  var n = 0, iv = setInterval(function () {
    var b = document.querySelector('[data-testid="stSidebarCollapseButton"] button') || document.querySelector('[data-testid="stSidebarCollapseButton"]');
    if (b && b.offsetParent !== null) { b.click(); clearInterval(iv); }
    else if (document.querySelector('[data-testid="stExpandSidebarButton"]') || ++n > 40) clearInterval(iv);
  }, 150);
  var last = 0;
  var hide = function (v) {
    [document.querySelector('[data-testid="stHeader"]'), document.querySelector('.st-key-themesw')]
      .forEach(function (el) { if (el) el.style.transform = v ? 'translateY(-130%)' : ''; });
  };
  document.addEventListener('scroll', function (e) {
    var m = e.target; if (!m || !m.getAttribute || m.getAttribute('data-testid') !== 'stMain') return;
    var t = m.scrollTop, d = t - last;
    if (t > 60 && d > 4) hide(true); else if (d < -4 || t <= 10) hide(false);
    last = t;
  }, true);
})();
"""
components.html(
    "<script>var d=window.parent.document;if(!window.parent.__aromaBoot){var s=d.createElement('script');"
    "s.textContent=" + json.dumps(PAGE_JS) + ";d.head.appendChild(s);}</script>", height=0)

# pages
sniff = st.Page(sniff_page.run, title="Sniff a smell", url_path="sniff", default=True)
keywords_page.SNIFF = sniff
keywords = st.Page(keywords_page.run, title="Smell keywords", url_path="keywords")
journey = st.Page(journey_page.run, title="Our journey", url_path="journey")
about = st.Page(about_page.run, title="About me", url_path="about")
chapters = docs_pages.build()
journey_page.BOOK = chapters
pg = st.navigation({"Try it": [sniff, keywords], "The story": [journey, about],
                    "Documentation": chapters}, expanded=True)

# day / night switch, top right of every page (animated sun and moon)
ui.hidden_theme_toggle()
ui.theme_switch()

with st.sidebar:
    st.link_button("GitHub", cfg.GITHUB_URL, width="stretch")
    st.link_button("LinkedIn", cfg.LINKEDIN_URL, width="stretch")
    st.caption(f"Created by {cfg.AUTHOR}")

pg.run()
