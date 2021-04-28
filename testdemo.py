import streamlit as st
import cv2

st.title("demo")
image=cv2.imread("https://github.com/BkSathish/myminiapp/blob/main/Resources/skimmer1a.jpg")
st.image(image, caption=None, width=590)
st.warning("updated")
