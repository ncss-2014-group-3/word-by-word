import word

hello_word = word.Word.from_id(1)
if hello_word:
    hello_word.remove()
    

hello_word = word.Word(False, 1, "hello")
world_word = hello_word.add_child("world")
im_word = world_word.add_child("I'm")
im_word.add_child("Amanda")
im_word.add_child("Jye")



