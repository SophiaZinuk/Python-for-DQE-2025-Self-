hw_text = '''homEwork:
	tHis iz your homeWork, copy these Text to variable. 

	You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.

	it iZ misspeLLing here. fix “iZ” with correct “is”, but ONLY when it Iz a mistAKE. 

	last iz TO calculate nuMber OF Whitespace characteRS in this Text. caREFULL, not only Spaces, but ALL whitespaces. I got 87.'''


def sentence_correction(text):
	hw_text_new = ' '.join(text.split()).lower().split('. ')
	final_list = []
	for s in hw_text_new:
		final_list.append(''.join(s.capitalize()))
	normilized = '. '.join(final_list)
	return normilized.replace(' iz ', ' is ')

sentence_correction(hw_text)

def last_sentense_creation(text):
	new_text = text.split('. ')
	list_of_sentenses = [s.split(' ') for s in new_text]
	last_sentense = ' '.join([i[-1] for i in list_of_sentenses]).capitalize()
	return last_sentense

last_sentense_creation(sentence_correction(hw_text))

def last_sentense_creation_v2(text):
	last_sentense = ''
	new_text = text.split('. ')
	for s in new_text:
		for l in range(len(s) - 1, -1, -1):
			if s[l] == ' ':
				last_sentense += s[l:]
				break
	return last_sentense.strip().capitalize()

def last_sentense_creation_v3(text):
    last_sentense = ''
    new_text = text.split('. ')
    for s in new_text:
        last_sentense += s[s.rindex(' '):]
    return last_sentense.strip().capitalize()

last_sentense_creation_v2(sentence_correction(hw_text))
last_sentense_creation_v3(sentence_correction(hw_text))

def whitespaces_calculation(text):
	num = 0
	for char in text:
		if char.isspace():
			num += 1
	return num

whitespaces_calculation(hw_text)