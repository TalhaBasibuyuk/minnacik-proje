import math
import random

import numpy as np
import json


def pretty_print_dict(d):
    print(json.dumps(d, indent=4, sort_keys=True))


def find_next_dist(target_word, sentences):
    prob_dist = dict()
    word_count = 0
    for sentence in sentences:
        if sentence.__contains__(target_word):
            for i in range(sentence.__len__()):
                if sentence[i] == target_word:
                    num = prob_dist.get(sentence[i + 1], 0)
                    prob_dist.update({sentence[i + 1]: num + 1})
                    word_count += 1

    for key in prob_dist.keys():
        value = prob_dist.get(key)
        prob_dist.update({key: value / word_count})

    return prob_dist


def generate_next(word, input_list):
    prob_dist = find_next_dist(word, input_list)
    words = list(prob_dist.keys())
    probabilities = list(prob_dist.values())
    next_word = random.choices(words, probabilities)[0]
    return next_word


def generate_new_sentence(input_list):
    new_sentence = "<|start|>"
    word = "<|start|>"
    while word != "<|end|>":
        word = generate_next(word, input_list)
        new_sentence += " " + word

    return new_sentence


def calc_sentence_prob(sentence, input_list):
    sentence_list = sentence.split(" ")
    probability = 1
    for i in range(sentence_list.__len__() - 1):
        prob_dist = find_next_dist(sentence_list[i], input_list)
        probability *= prob_dist.get(sentence_list[i+1])

    return math.log(probability)


DATA_PATH = "data/sentences.txt"
input_file = open(DATA_PATH, "r")
org_input_list = [sentence.split() for sentence in input_file.readlines()]

for i in range(10):
    sentence = generate_new_sentence(org_input_list)
    print(sentence + " " + str(calc_sentence_prob(sentence, org_input_list)))


