from transformers import pipeline
summarizer = pipeline("summarization", model="philschmid/bart-large-cnn-samsum")

conversation = '''In terms of handling the events with time management, that's what's lacking. It'll be better if they utilize every available room to manage the times set of each events. \n 
Need to improve on planning the event. \n 
more e-sports. \n 
for me more esport events and more speakers. \n 
improve and give internet signal for all students \n 
more esports event and upgrade the computers. \n 
i think the place because its very small and i suggest that outsider let them go inside and partake the event. \n 
i would suggest that there are dota2 on the next e-sports event. \n 
organize and prioritize those important events. \n 
Next time more cooperate from students and faculty. \n 
good connection and good venue. \n 
venue. \n 
maintaining facilitate and cooperation, teamwork of students. \n                              
'''

result = summarizer(conversation)

print(type(result[0]))
print(result[0]['summary_text'])