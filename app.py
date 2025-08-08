import streamlit as st
import google.generativeai as genai 
from apikey import google_gemini_api_key


# Configure the API key
genai.configure(api_key=google_gemini_api_key)

# Set up the model configuration
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    }
]

# Create the model object (no api_key here)
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",  # Or "gemini-1.5-flash" for faster responses
    generation_config=generation_config,
    safety_settings=safety_settings
)

# Set app to wide mode
st.set_page_config(layout="wide")

# Title of the app
st.title('✍️🤖 BlogCraft: Your AI Blogging Companion')

# Create a subheader
st.subheader('Now you can craft perfect blogs with the help of AI - BlogCraft is your New AI Blogging Companion')

# Sidebar for user input
with st.sidebar:
    st.title('Input Your Blog Details')
    st.subheader('Enter Details of the Blog You want to Generate')

    # Blog Title
    blog_title = st.text_input('Blog Title')

    # Keywords input
    keywords = st.text_area('Keywords (comma separated)')

    # Number of words
    num_words = st.slider('Number of Words', min_value=250, max_value=1000, value=500, step=250)

    # Number of images
    num_images = st.number_input('Number of Images', min_value=1, max_value=5, step=1)
    
    prompt_parts = [
        f"Generate a comprehensive, engaging blog post relevant to the given title \"{blog_title}\" "
        f"and keywords \"{keywords}\". Make sure to incorporate these keywords in the blog post. "
        f"The blog should be approximately {num_words} words in length, suitable for an online audience. "
        f"Ensure the content is original, informative, and maintains a consistent tone throughout."
    ]

    # Submit button
    submit_button = st.button('Generate Blog')

if submit_button:
    response = model.generate_content(prompt_parts)

    st.title('YOUR BLOG POST:')
    st.write(response.text)

    # Allow user to upload image(s)
    st.subheader("📸 Upload Image(s) for Your Blog")

    uploaded_images = st.file_uploader(
        "Upload images to include in your blog (you can select multiple files)",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True
    )

    # Display uploaded images
    if uploaded_images:
        for image in uploaded_images:
            st.image(image, use_column_width=True)

