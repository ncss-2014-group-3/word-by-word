import word
import story

story1 = story.Story.from_id(1)
if story1:
    story1.remove()
    

story1 = story.Story("My first story", "Hello")
hello_word = story1.first_word()



world_word = hello_word.add_child("world")
im_word = world_word.add_child("I'm")
im_word.add_child("Amanda")
im_word.add_child("Jye")

print(story1.word_count())