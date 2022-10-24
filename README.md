# SentenceSaver

The SentenceSaver was a project for the DubHacks 2022 hackathon at the University of Washington.

# Main Functions:
1) Correct spelling and grammatical errors using the Sapling.AI API (https://sapling.ai/api)
2) Return links to grammar-learning resources based on the types of mistakes made in the original writing

![Screen Shot 2022-10-24 at 12 17 22 PM](https://user-images.githubusercontent.com/54155011/197608489-55714c52-3bf5-4f53-b89c-513ab0602f33.png)
![Screen Shot 2022-10-24 at 12 17 43 PM](https://user-images.githubusercontent.com/54155011/197608507-33cbb64b-b289-42da-8e2c-e048ecf49474.png)


# How we made it:
We designed the backend using the Flask Python framework to create a local server and designed the frontend using vanilla HTML/CSS. We also used the Sapling.AI API to return both the corrected writing and the grammatical error types for the recommendation system. The recommendation system was hard-coded to return specific links for related error codes for a proof of concept.

# Challenges we faced:
One of the more difficult tasks was collecting the information we needed for the recommendation system from the API. Sapling.AI provided codes relating to the mistakes that were seen in the input (eg. "PUNCT" for punctuation error), but sometimes incorrectly identified or generalized the errors (eg. "OTHER" when there should be a specific error). Another challenge we faced was attempting to build a user data collection/visualization feature. We started by building functions for a SQLite database, but we faced multiple bugs that we were not able to clear before the hackathon time limit. As a result, we presented only our core functions.

# Future improvements:
1) Complete the data collection/visualization feature to allow users to see what grammatical problems were most common in their writing
2) Provide a more scalable solution for personalized recommendations that does not involve as much hard-coding

# How to try it out: 

# Team:
Daniel Kim, David Gim, Edward Lee, John Lee
