import streamlit as st
import os
import sqlite3
from typing import List
from database import get_conn
from utils import get_image_base64, human_time
import crud 

# --- CSS STYLES ---
def apply_theme():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Patrick+Hand&display=swap');
    html, body, [class*="css"] { font-family: 'Patrick Hand', cursive, sans-serif; color: #000000; }
    .stApp { background-color: #F3FFC6 !important; }
    h1, h2, h3 { font-weight: 900 !important; text-transform: uppercase; letter-spacing: 1px; background: #4FC3F7; display: inline-block; padding: 2px 10px; border: 2px solid black; box-shadow: 3px 3px 0px 0px black; transform: rotate(-1deg); color: black !important; }
    section[data-testid="stSidebar"] h1 { background: transparent !important; border: none !important; box-shadow: none !important; transform: rotate(0deg) !important; }
    p, div, span, label { color: #000000 !important; }
    div[data-testid="stVerticalBlockBorderWrapper"] { border: 3px solid #000000 !important; box-shadow: 6px 6px 0px 0px #000000 !important; border-radius: 5px !important; background-color: #ffffff !important; margin-bottom: 25px !important; padding: 15px !important; }
    hr { margin-top: 20px !important; margin-bottom: 20px !important; border-width: 0px !important; border-top: 4px solid #000000 !important; opacity: 1 !important; border-radius: 50% !important; }
    button[kind="primary"] { background-color: #29B6F6 !important; color: black !important; border: 3px solid black !important; box-shadow: 4px 4px 0px 0px black !important; font-weight: 900 !important; text-transform: uppercase; }
    button[kind="secondary"] { background-color: #B3E5FC !important; color: black !important; border: 3px solid black !important; box-shadow: 4px 4px 0px 0px black !important; font-weight: 900 !important; }
    button:active { box-shadow: 0px 0px 0px 0px black !important; transform: translate(4px, 4px) !important; }
    input, textarea { background-color: #ffffff !important; border: 3px solid black !important; color: black !important; box-shadow: 3px 3px 0px 0px #ccc !important; }
    input:disabled, textarea:disabled, input[disabled], textarea[disabled] { background-color: #f4f4f4 !important; color: #000000 !important; opacity: 1 !important; -webkit-text-fill-color: #000000 !important; border-color: #000000 !important; font-weight: bold !important; }
    section[data-testid="stSidebar"] { background-color: #F3FFC6 !important; border-right: 3px solid black !important; }
    section[data-testid="stSidebar"] .stButton > button { text-align: left !important; width: 100%; }
    section[data-testid="stSidebar"] button[kind="secondary"] { border-color: black !important; }
    section[data-testid="stSidebar"] button[kind="secondary"]:hover { background-color: #81D4FA !important; transform: none !important; box-shadow: 4px 4px 0px 0px black !important; }
    img { border: 2px solid black; }
    div[data-baseweb="toast"] { background-color: #F3FFC6 !important; border: 3px solid black !important; }
    header { visibility: visible !important; background: transparent !important; }
    header button, header svg { color: black !important; fill: black !important; }
    div[data-baseweb="popover"], div[data-baseweb="menu"], div[role="dialog"], ul[data-baseweb="menu"] { background-color: #F3FFC6 !important; border: 3px solid black !important; box-shadow: 5px 5px 0px 0px black !important; }
    div[data-baseweb="popover"] *, div[data-baseweb="menu"] *, div[role="dialog"] *, ul[data-baseweb="menu"] * { color: #000000 !important; background-color: transparent !important; }
    li[role="option"] { background-color: #F3FFC6 !important; color: black !important; border-bottom: 1px solid #000000 !important; }
    li[role="option"]:hover, li[role="option"][aria-selected="true"] { background-color: #4FC3F7 !important; color: black !important; }
    div[data-baseweb="select"] > div { background-color: #ffffff !important; border: 3px solid black !important; color: black !important; }
    div[data-testid="stSelectbox"] div { color: black !important; }
    div[data-testid="stFileUploaderDropzone"] { background-color: #F3FFC6 !important; border: 3px solid black !important; border-radius: 0px !important; }
    div[data-testid="stFileUploaderDropzone"] div, div[data-testid="stFileUploaderDropzone"] span, div[data-testid="stFileUploaderDropzone"] small { color: black !important; }
    div[data-testid="stFileUploaderDropzone"] svg { fill: black !important; stroke: black !important; }
    section[data-testid="stFileUploader"] button { background-color: #29B6F6 !important; color: black !important; border: 2px solid black !important; box-shadow: 3px 3px 0px 0px black !important; font-weight: 900 !important; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

# --- POST RENDERING ---
def render_post(p, key_prefix: str = "default"):
    p = dict(p)
    st.write("\n")
    
    with st.container(border=True):
        header_cols = st.columns([1, 5, 2]) 
        
        # 1. Profile Picture
        with header_cols[0]:
            img_src = "https://cdn-icons-png.flaticon.com/512/149/149071.png"
            if p.get('profile_pic_path') and os.path.exists(p['profile_pic_path']):
                b64 = get_image_base64(p['profile_pic_path'])
                if b64: img_src = f"data:image/png;base64,{b64}"
            
            st.markdown(f"""
                <div style="width: 55px; height: 55px; border-radius: 50%; overflow: hidden; display: flex; justify-content: center; align-items: center;">
                    <img src="{img_src}" style="width: 100%; height: 100%; object-fit: cover; border: none !important;">
                </div>
            """, unsafe_allow_html=True)
        
        # 2. Name & Date
        username = p['username']
        display_name = p['display_name']
        created = human_time(p['created_at'])
        header_cols[1].markdown(f"**@{username}** — *{display_name}* \n<div style='font-size: 0.8em; color: #555;'>{created}</div>", unsafe_allow_html=True)
        
        # 3. View Profile Button
        if header_cols[2].button("View Profile", key=f"{key_prefix}_view_profile:{p['id']}"):
            st.session_state.view = f"profile:{username}"
            st.rerun()
            
        # Post Text
        if p.get('text'): 
            st.markdown(f"<div style='margin-top: 10px; font-size: 1.4em; line-height: 1.4; color: #000;'>{p['text']}</div>", unsafe_allow_html=True)
        
        # Post Image
        if p.get('image_path'):
            abs_path = os.path.abspath(p['image_path'])
            if os.path.exists(abs_path):
                b64_str = get_image_base64(abs_path)
                if b64_str:
                    html = f"""<div style="width: 100%; margin-top: 10px; border: 3px solid black; box-shadow: 4px 4px 0px 0px black; overflow: hidden;"><img src="data:image/png;base64,{b64_str}" style="width: 100%; height: auto; display: block; object-fit: cover;"></div>"""
                    st.markdown(html, unsafe_allow_html=True)

        st.write("") 
        st.write("") 
        
        # Action Buttons
        row = st.columns([1,1,1]) 
        post_id = p['id']
        user = st.session_state.user
        
        liked = False
        bookmarked = False
        if user:
            liked = get_conn().cursor().execute("SELECT 1 FROM likes WHERE user_id = ? AND post_id = ?", (user['id'], post_id)).fetchone() is not None
            bookmarked = get_conn().cursor().execute("SELECT 1 FROM bookmarks WHERE user_id = ? AND post_id = ?", (user['id'], post_id)).fetchone() is not None
        
        like_icon = "❤️" if liked else "🤍"
        bookmark_icon = "✅" if bookmarked else "🔖"

        if user:
            if row[0].button(f"{like_icon} {crud.get_likes_for_post(post_id)}", key=f"{key_prefix}_like:{post_id}"):
                if liked: crud.unlike_post(user['id'], post_id)
                else: crud.like_post(user['id'], post_id)
                st.rerun()
            if row[1].button("💬 Reply", key=f"{key_prefix}_reply:{post_id}"):
                st.session_state.view = f"reply:{post_id}"
                st.rerun()
            if row[2].button(f"{bookmark_icon} Save", key=f"{key_prefix}_bm:{post_id}"):
                if bookmarked: crud.unbookmark_post(user['id'], post_id)
                else: crud.bookmark_post(user['id'], post_id)
                st.rerun()
        else:
            row[0].write(f"❤️ {crud.get_likes_for_post(post_id)}")
            row[1].write("💬")
            row[2].write("🔖")
            
        if key_prefix != "reply_ctx":
            replies = crud.get_replies_for_post(post_id)
            if replies:
                with st.expander(f"{len(replies)} replies"):
                    for r in replies:
                        st.markdown(f"**@{r['username']}** {human_time(r['created_at'])}")
                        st.write(r['text'])

    st.markdown("---")

# --- REAL-TIME CHAT ---
@st.fragment(run_every=2)
def render_realtime_chat(current_user_id, other_user_id, current_user_name, other_user_name):
    msgs = crud.get_messages_between(current_user_id, other_user_id)
    with st.container(height=400, border=True):
        if not msgs: 
            st.caption("No messages yet. Say hi! 👋")
        
        for m in msgs:
            is_me = (m['sender_id'] == current_user_id)
            if is_me:
                st.markdown(f"""
                <div style="display: flex; justify-content: flex-end; margin-bottom: 10px; padding-right: 5px;">
                <div style="background-color: #1D9BF0; color: white; padding: 10px 15px; border-radius: 20px 20px 2px 20px; max-width: 70%; font-family: sans-serif; font-size: 16px; box-shadow: 1px 1px 2px rgba(0,0,0,0.1);">
                {m['text']}
                </div></div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="display: flex; justify-content: flex-start; margin-bottom: 10px; padding-left: 5px;">
                <div style="background-color: #EFF3F4; color: black; padding: 10px 15px; border-radius: 20px 20px 20px 2px; max-width: 70%; font-family: sans-serif; font-size: 16px; border: 1px solid #e1e8ed;">
                {m['text']}
                </div></div>
                """, unsafe_allow_html=True)

def render_user_list(title: str, user_list: List[sqlite3.Row]):
    st.header(title)
    if not user_list:
        st.info("No users found.")
        return
    for u in user_list:
        with st.container(border=True):
            cols = st.columns([1, 4, 2])
            with cols[0]:
                img_src = "https://cdn-icons-png.flaticon.com/512/149/149071.png"
                if u['profile_pic_path'] and os.path.exists(u['profile_pic_path']):
                    b64 = get_image_base64(u['profile_pic_path'])
                    if b64: img_src = f"data:image/png;base64,{b64}"
                st.image(img_src, width=50)
            with cols[1]:
                st.write(f"**{u['display_name']}**")
                st.caption(f"@{u['username']}")
            with cols[2]:
                if st.button("View", key=f"list_view_{u['id']}"):
                    st.session_state.view = f"profile:{u['username']}"
                    st.rerun()
