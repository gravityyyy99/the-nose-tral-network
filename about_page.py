"""About me: a 3D scroll experience with a hologram of the author, built with three.js and GSAP."""
import base64
import os

import streamlit as st
import streamlit.components.v1 as components

import site_config as cfg
import ui

HERE = os.path.dirname(os.path.abspath(__file__))
AVATAR = "https://github.com/gravityyyy99.png"   # GitHub profile picture


def run():
    # full-bleed page: the 3D stage uses the whole width
    st.markdown("<style>.block-container{max-width:100% !important;padding:0 !important;}</style>",
                unsafe_allow_html=True)
    local = ""   # your own photo: drop it at assets/me.png (or me.jpg) and it is used automatically
    for name, mime in (("me.png", "image/png"), ("photo.png", "image/png"), ("profile.png", "image/png"),
                       ("me.jpg", "image/jpeg"), ("me.jpeg", "image/jpeg"), ("photo.jpg", "image/jpeg"),
                       ("profile.jpg", "image/jpeg")):
        path = os.path.join(HERE, "assets", name)
        if os.path.exists(path):
            with open(path, "rb") as img:
                local = f"data:{mime};base64," + base64.b64encode(img.read()).decode()
            break
    with open(os.path.join(HERE, "assets", "about3d.html"), encoding="utf-8") as f:
        html = (f.read().replace("__NAME__", cfg.AUTHOR).replace("__AVATAR__", AVATAR)
                .replace("__GHUSER__", cfg.GITHUB_URL.rstrip("/").split("/")[-1]).replace("__GITHUB__", cfg.GITHUB_URL).replace("__LINKEDIN__", cfg.LINKEDIN_URL).replace("__LOCAL__", local))
    with st.container(key="about3d"):
        components.html(html, height=700)
    ui.footer()
