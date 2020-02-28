"""
Code from:
      https://github.com/nlpyang/BertSum/blob/master/LICENSE
under:
      Apache License 2.0
"""
import math
import rouge
from rouge.rouge_score import Ngrams


def _rouge_clean(s):
    # return re.sub(r'[^a-zA-Z0-9 ]', '', s)
    return s


def greedy_selection(doc_sent_list, abstract_sent_list,
                     summary_size, exclusive_ngrams=False):
    """Greedy ext-oracle on lists of sentences

    Args:
        doc_sent_list(list): list of doc sentences (itself a list of words)
        abstract_sent_list(list): list of abstract sentences
                                  (itself a list of words)
        summary_size(int): size of the summary, in sentences

    Returns:
        selected(list): list of selected sentences
    """
    def _get_word_ngrams(n, sentences):
        return rouge.rouge_score._get_ngrams(
            n, sentences, exclusive=exclusive_ngrams)

    max_rouge = 0.0
    abstract = sum(abstract_sent_list, [])
    abstract = _rouge_clean(' '.join(abstract)).split()
    sents = [_rouge_clean(' '.join(s)).split() for s in doc_sent_list]
    evaluated_1grams = [_get_word_ngrams(1, sent) for sent in sents]
    reference_1grams = _get_word_ngrams(1, abstract)
    evaluated_2grams = [_get_word_ngrams(2, sent) for sent in sents]
    reference_2grams = _get_word_ngrams(2, abstract)

    selected = []
    for s in range(summary_size):
        cur_max_rouge = max_rouge
        cur_id = -1
        for i in range(len(sents)):
            if (i in selected):
                continue
            c = selected + [i]
            candidates_1 = [evaluated_1grams[idx] for idx in c]
            candidates_1 = Ngrams.union(*candidates_1)
            candidates_2 = [evaluated_2grams[idx] for idx in c]
            candidates_2 = Ngrams.union(*candidates_2)
            rouge_1 = cal_rouge(candidates_1, reference_1grams)['f']
            rouge_2 = cal_rouge(candidates_2, reference_2grams)['f']
            rouge_score = rouge_1 + rouge_2
            if rouge_score > cur_max_rouge:
                cur_max_rouge = rouge_score
                cur_id = i
        if (cur_id == -1):
            return selected, sents
        selected.append(cur_id)
        max_rouge = cur_max_rouge

    return sorted(selected), sents


def combination_selection(doc_sent_list, abstract_sent_list, summary_size,
                          exclusive_ngrams=False):
    """Combination ext-oracle on lists of sentences

    Args:
        doc_sent_list(list): list of doc sentences (itself a list of words)
        abstract_sent_list(list): list of abstract sentences
                                  (itself a list of words)
        summary_size(int): size of the summary, in sentences

    Returns:
        selected(list): list of selected sentences
    """
    import itertools

    def _get_word_ngrams(n, sentences):
        return rouge.rouge_score._get_ngrams(
            n, sentences, exclusive=exclusive_ngrams)

    max_rouge = 0.0
    max_idx = (0, 0)
    abstract = sum(abstract_sent_list, [])
    abstract = _rouge_clean(' '.join(abstract)).split()
    sents = [_rouge_clean(' '.join(s)).split() for s in doc_sent_list]
    evaluated_1grams = [_get_word_ngrams(1, sent) for sent in sents]
    reference_1grams = _get_word_ngrams(1, abstract)
    evaluated_2grams = [_get_word_ngrams(2, sent) for sent in sents]
    reference_2grams = _get_word_ngrams(2, abstract)

    impossible_sents = []

    min_summary_size = math.ceil(summary_size / 2)
    for s in range(min_summary_size, summary_size + 1):
        combinations = itertools.combinations(
            [i for i in range(len(sents)) if i not in impossible_sents], s + 1)
        for c in combinations:
            candidates_1 = [evaluated_1grams[idx] for idx in c]
            candidates_1 = Ngrams.union(*candidates_1)
            candidates_2 = [evaluated_2grams[idx] for idx in c]
            candidates_2 = Ngrams.union(*candidates_2)
            rouge_1 = cal_rouge(candidates_1, reference_1grams)['f']
            rouge_2 = cal_rouge(candidates_2, reference_2grams)['f']

            rouge_score = rouge_1 + rouge_2
            if (s == 0 and rouge_score == 0):
                impossible_sents.append(c[0])
            if rouge_score > max_rouge:
                max_idx = c
                max_rouge = rouge_score
    return sorted(list(max_idx)), sents


def cal_rouge(evaluated_ngrams, reference_ngrams):
    reference_count = len(reference_ngrams)
    evaluated_count = len(evaluated_ngrams)

    overlapping_ngrams = evaluated_ngrams.intersection(reference_ngrams)
    overlapping_count = len(overlapping_ngrams)

    return rouge.rouge_score.f_r_p_rouge_n(
        evaluated_count, reference_count, overlapping_count)
