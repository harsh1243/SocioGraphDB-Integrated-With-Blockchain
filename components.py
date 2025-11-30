import streamlit as st
import os
import sqlite3
import crud
from database import get_conn
from utils import get_image_base64, human_time

def render_user_list(title: str, users):
    st.header(title)
    if not users:
        st.info("No users found here.")
        return
    for u in users:
        with st.container(border=True):
            cols = st.columns([1, 6, 1])
            if u['profile_pic_path']:
                cols[0].image(u['profile_pic_path'], width=50)
            else:
                cols[0].markdown("👤", unsafe_allow_html=True)
            cols[1].markdown(f"**@{u['username']}** — *{u['display_name']}*")
            cols[1].caption(u['bio'])
            if cols[2].button("View", key=f"view_list_{u['id']}_{title.replace(' ', '_')}"):
                st.session_state.view = f"profile:{u['username']}"
                st.rerun()

# --- RENDER POST ---
def render_post(p, key_prefix: str = "default"):
    p = dict(p)
    st.write("\n")
    with st.container(border=True):
        header_cols = st.columns([1, 5, 1])
        with header_cols[0]:
            if p.get('profile_pic_path') and os.path.exists(p['profile_pic_path']):
                st.image(p['profile_pic_path'], width=50)
            else:
                st.markdown("<div style='font-size: 30px;'>👤</div>", unsafe_allow_html=True)
        
        username = p['username']
        display_name = p['display_name']
        created = human_time(p['created_at'])
        header_cols[1].markdown(f"**@{username}** — *{display_name}* \n<div style='font-size: 0.8em; color: gray;'>{created}</div>", unsafe_allow_html=True)
        
        if header_cols[2].button("View profile", key=f"{key_prefix}_view_profile:{p['id']}"):
            st.session_state.view = f"profile:{username}"
            st.rerun()
            
        st.markdown("---") 
        if p.get('text'): st.markdown(p['text'])
        
        if p.get('image_path'):
            abs_path = os.path.abspath(p['image_path'])
            if os.path.exists(abs_path):
                b64_str = get_image_base64(abs_path)
                if b64_str:
                    html = f"""<div style="width: 100%; margin-top: 10px; border-radius: 12px; overflow: hidden;"><img src="data:image/png;base64,{b64_str}" style="width: 100%; height: auto; display: block; object-fit: cover; border-radius: 12px;"></div>"""
                    st.markdown(html, unsafe_allow_html=True)

        st.write("") 
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
            if row[2].button(f"{bookmark_icon} Bookmark", key=f"{key_prefix}_bm:{post_id}"):
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

# --- REAL-TIME CHAT FRAGMENT ---
@st.fragment(run_every=2)
def render_realtime_chat(current_user_id, other_user_id, current_user_name, other_user_name):
    msgs = crud.get_messages_between(current_user_id, other_user_id)
    with st.container(height=300, border=True):
        if not msgs: st.caption("No messages yet. Say hi! 👋")
        for m in msgs:
            is_me = (m['sender_id'] == current_user_id)
            who = "You" if is_me else other_user_name
            style = "color: #1d9bf0;" if is_me else "color: #536471;"
            align = "text-align: right;" if is_me else "text-align: left;"
            st.markdown(f"<div style='{align} {style}'><b>{who}</b> <span style='font-size:0.8em'>({human_time(m['created_at'])})</span><br>{m['text']}</div>", unsafe_allow_html=True)
