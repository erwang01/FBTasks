# QuickRead
Our Messenger chatbot automatically summarizes articles to streamline information intake on Facebook.

## The Inspiration
It's fairly obvious that traditional news sources like newspapers (even online publications) and television are being replaced by news transmitted by peers and influencers on social media. This is statistically true--Pew Research says as a percentage of US adults, 45% of Americans get news on Facebook. This is also anecdotally evident: a quick scroll through your NewsFeed shows you links shared by peers, from the serious--shootings, accidents, politics, and natural disasters--to the lighthearted--think BuzzFeed articles. 
It's pretty clear that there's no shortage of textual information to be synthesized on Facebook. This can create an overwhelming overload of information for some Facebook users. We wanted to find a way to make the experience of going on Facebook and using Facebook as a news source, as an increasing number of people are doing today, less cluttered and more personalized. 

## The Platform
As social media becomes increasingly popular with the youth largely spending their time on instant messaging services, it was a nautral choice to place our project on the Facebook Messenger platform. This platform places our product in the hands of millions and allows us to better integrate with the news feeds that our users read. Instead of scrolling through minefields of ads, QuickRead takes a link to any news story or article on the internet, and returns within a personalized Messenger chat for the user a brief, generated summary which represents the contents of the article. This summary is generated with the TextRank algorithm, and our tests with a variety of articles have shown strong results.

## Getting Started
Our Chat bot has the username: [qread.bot](https://www.facebook.com/qread.bot/) Please find us on Facebook and Messenger. We have yet to submit our bot for review so please shoot us an email at [erwang01@gmail.com](mailto:erwang01@gmail.com) if you would like to join our beta testing community.

If you would like to implement the bot for yourself, our source code is open on github.com/erwang01/FBTasks under the branch "news".

## Challenges
* The API documentation for Messenger was very sparse, requiring lots of low level debugging. We had to explore each JSON object manually to find hidden functionality not disclosed by the documentation.
* We had multiple false leads, not realizing that Messenger did not support text based interactions in group chats, requiring us to take the 1 on 1 bot approach.
* There were numerous challenges in developing an approach to stripping text from ad filled new articles and articles with long snippets of author bios and similar articles.

## What's Next
1. Submission to Facebook for approval and publication to the wider Facebook community rather than only approved testers and developers currently granted access.
2. Develop a chat extension to allow the chat bot to be used within group chats. This is specifically helpful for research groups sharing news articles that they found helpful.
3. Customization options allow for users to better customize the level of detail they would like in the summaries and how long each summary should be.
4. Text to speech functionality to make news articles into audiobooks
5. Suggested articles list will allow users to skip scrolling the newsfeed entirely, removing the problems where pressing the back button one too many times resets the newsfeed back to the top and forcing the user to scroll all the way back down.
