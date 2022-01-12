# import libraries
import streamlit as st
from annotated_text import annotated_text
import spacy

# import models
@st.cache(show_spinner=False, allow_output_mutation=True, suppress_st_warning=True)
def load_models():
    dutch_model = spacy.load("./models/NL/nl_core_news_sm/nl_core_news_sm-3.2.0/")
    english_model = spacy.load("./models/ENG/en_core_web_sm/en_core_web_sm-3.2.0/")
    models = {"ENG": english_model, "NL": dutch_model}
    return models

# processing text input
def process_text(doc, selected_entities, anonymize=False):
    tokens = []
    for token in doc:
        if (token.ent_type_ == "PERSON") & ("PER" in selected_entities):
            tokens.append((token.text, "Person", "#faa"))
        elif (token.ent_type_ in ["GPE", "LOC"]) & ("LOC" in selected_entities):
            tokens.append((token.text, "Location", "#fda"))
        elif (token.ent_type_ == "ORG") & ("ORG" in selected_entities):
            tokens.append((token.text, "Organization", "#afa"))
        else:
            tokens.append(" " + token.text + " ")
    return tokens

# used for layout
row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns(
    (.1, 2, .2, 1, .1))

row0_1.title('Analyze your vacancy')

with row0_2:
    st.write('')

row0_2.subheader('')

row1_spacer1, row1_1, row1_spacer2 = st.columns((.1, 3.2, .1))

with row1_1:
    st.markdown("Hey there! Welcome to J4 Vacancy Analysis App. This app will detect non-inclusive words in vacancies and makes suggestions that will improve your vacancy")
    st.markdown(
        "**To begin, please enter the vacancy your are writing (or just use an example!).** 👇")

row2_spacer1, row2_1, row2_spacer2 = st.columns((.1, 3.2, .1))
with row2_1:
    default_example = st.selectbox("Select one of our sample vacancy texts", (
        "example1", "example2", "example3"))
    st.markdown("**or**")
    user_input = st.text_area(
        "Input your own vacancy")

uploaded_file = st.file_uploader("or Upload a file", type=["doc", "docx", "pdf", "txt"])
if uploaded_file is not None:
    text_input = uploaded_file.getvalue()
    text_input = text_input.decode("utf-8")

models = load_models()

selected_language = st.sidebar.selectbox("Select a language", options=["ENG", "NL"])
selected_entities = st.sidebar.multiselect(
    "Select the entities you want to detect",
    options=["LOC", "PER", "ORG"],
    default=["LOC", "PER", "ORG"],
)

selected_model = models[selected_language]

doc = selected_model(user_input)
tokens = process_text(doc, selected_entities)

annotated_text(*tokens)

"""
## Annotated text example

Below is an example of how to use the annotated_text function:


annotated_text(
    "This ",
    ("is", "verb", "#8ef"),
    " some ",
    ("annotated", "adj", "#faa"),
    ("text", "noun", "#afa"),
    " for those of ",
    ("you", "pronoun", "#fea"),
    " who ",
    ("like", "verb", "#8ef"),
    " this sort of ",
    ("thing", "noun", "#afa"),
)
st.markdown('#')
list = ['Wij zoeken een ',('starter','non-inclusive','#fea'), ' met weinig ervaring en ']

new_word = ('kennis', 'non-inclusive', '#faa')

list.append(new_word)

annotated_text(*list)
st.markdown('#')
"""