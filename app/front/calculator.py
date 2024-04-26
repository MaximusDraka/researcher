import streamlit as st
import json
import requests
            

st.title("Basic calculator App")

option = st.selectbox('Which operation would you like to perform?',('Addition', 'Subtraction', 'Multiplication', 'Division'))

st.write("")
st.write("Select the numbers from the slider below")

x = st.slider('X',0,100,20)
y = st.slider('Y',0,130,10)

inputs = {"operation": option, "x": x, "y": y}

if st.button('Calculate'):
    response = requests.post(url="http://skillskeletonapi:8000/calculate", data=json.dumps(inputs))
    
    st.subheader("The answer is: {}".format(response.text))
