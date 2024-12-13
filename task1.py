import math
import random

# Find the probability distribution of the words that can be selected for the next word in the sentence
def find_next_dist(target_word, sentences):
    # Probability distribution is represented by a dictionary, keys are the words and the values are their probability.
    prob_dist = dict()
    word_count = 0
    for sentence in sentences:
        # In all sentences that include target word, update the count of the words that come before and after the
        # target word.
        if target_word in sentence:
            for i in range(len(sentence)):
                if sentence[i] == target_word:
                    num = prob_dist.get(sentence[i + 1], 0)
                    prob_dist.update({sentence[i + 1]: num + 1})
                    word_count += 1
    # Divide each count by the total word count to obtain probabilities.
    for key in prob_dist.keys():
        value = prob_dist.get(key)
        prob_dist.update({key: value / word_count})

    return prob_dist

# Generate the next word in the sentence using the probability distribution of possible words
def generate_next(word, input_list):
    prob_dist = find_next_dist(word, input_list)
    words = list(prob_dist.keys())
    probabilities = list(prob_dist.values())
    # Find the next word based on the probability distribution
    next_word = random.choices(words, probabilities)[0]
    return next_word

# Generates a full sentence starting with <start> and ending with <end>.
# This method keeps adding a word to the sentence until the <end> keyword is generated.
def generate_new_sentence(input_list):
    new_sentence = "<|start|>"
    word = "<|start|>"
    while word != "<|end|>":
        word = generate_next(word, input_list)
        new_sentence += " " + word

    return new_sentence

# Calculates the probability of a given sentence
# Returns 0 if sentence is impossible, otherwise returns the logarithm of the probability
def calc_sentence_prob(sentence, input_list):
    sentence_list = sentence.split(" ")
    if sentence_list[0] != "<|start|>" or sentence_list[-1] != "<|end|>":
        return None
    probability = 1
    for i in range(len(sentence_list) - 1):
        prob_dist = find_next_dist(sentence_list[i], input_list)
        probability *= prob_dist.get(sentence_list[i+1], 0)
    if probability == 0:
       return None
    return math.log(probability)


def compare_generated_and_actual_sentence(written_sentence, generated_sentence, input_list):
    generated_sentence_prob = calc_sentence_prob(generated_sentence, input_list)
    written_sentence_prob = calc_sentence_prob(written_sentence, input_list)

    print("Logarithm of the probability of generated sentence is: ", generated_sentence_prob)

    if written_sentence_prob is None:
        print("Written sentence is not probable.")
        return
    print("Logarithm of the probability of written sentence is: ", written_sentence_prob)


    if calc_sentence_prob(written_sentence, input_list) > calc_sentence_prob(generated_sentence, input_list):
        print("Written sentence is more probable than the generated sentence.")
    elif calc_sentence_prob(written_sentence, input_list) < calc_sentence_prob(generated_sentence, input_list):
        print("Generated sentence is more probable than the written sentence.")
    else:
        print("Generated sentence and written sentence are equally likely.")



# Read the sentences.txt file and process the input
DATA_PATH = "data/sentences.txt"
input_file = open(DATA_PATH, "r")
org_input_list = [sentence.split() for sentence in input_file.readlines()]

# generate 5 sentences
print("***************Example Sentences***************")
for i in range(5):
    sentence = generate_new_sentence(org_input_list)
    print(sentence)

print()
print("***************Comparison of the written and the  generated sentence***************")
generated_sentence = generate_new_sentence(org_input_list)
written_sentence = "<|start|> I enjoy hiking <|end|>"
print("Generated sentence: ", generated_sentence)
print("Written sentence: ", written_sentence)
compare_generated_and_actual_sentence(written_sentence , generated_sentence , org_input_list)
