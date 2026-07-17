# Project Atlas Demo

Public Streamlit demo for Project Atlas, currently focused on Ben's Maths Coach.

This repo contains only the files needed to run the current demo app on Streamlit Community Cloud.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Current demo

Project Atlas presents one recommended maths mission, runs a short question session, marks answers deterministically, updates mastery, shows rewards earned for meaningful mission completion, explains why the mission was chosen, and ends with a Session Review.

Recent demo updates include:
- Session Review v1: what Ben practised, what improved, what remains difficult, what Atlas learned, and what Atlas will do next.
- Better Answer Marking v1: accepts simple equivalent answer forms such as `x = 4`, `4.0`, `.6`, `1/2`, and percentage signs when a percentage answer is requested.
- Mistake Memory v1: recurring mistakes become a small deterministic signal in the next mission recommendation.
- Recommendation Reasons v1: the mission screen and next-mission panel show the Decision Engine's supporting reasons.
