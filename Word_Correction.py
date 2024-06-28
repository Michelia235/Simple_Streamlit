import streamlit as st


def levenshtein_distance(token1, token2):
    if not isinstance(token1, str) or not isinstance(token2, str):
        print('Hãy nhập lại 2 chữ cái')

    if token1 == '':
        return len(token1)
    if token2 == '':
        return len(token2)

    token1 = token1.lower()
    token2 = token2.lower()

    n = len(token1)
    m = len(token2)

    lev = [[0 for _ in range(m + 1)] for _ in range(m + 1)]

    for i in range(n+1):
        lev[i][0] = i

    for j in range(m+1):
        lev[0][j] = j

    for i in range(1, n+1):
        for j in range(1, m+1):
            del_cost = lev[i-1][j] + 1
            ins_cost = lev[i][j-1] + 1
            sub_cost = lev[i-1][j-1] + (1 if token1[i-1] != token2[j-1] else 0)
            lev[i][j] = min(del_cost, ins_cost, sub_cost)

    distance = float(lev[n][m])
    return distance


def load_vocab(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    words = sorted(set([line.strip().lower() for line in lines]))
    return words


vocabs = load_vocab(file_path=r'C:\Users\Administrator\Desktop\AIO-Exercise\project1\data\vocab.txt')

st.title("Word Correction using Levenshtein Distance")
word = st.text_input('Word:')

if st.button("Compute"):    

    # compute levenshtein distance
    leven_distances = dict()
    for vocab in vocabs:
        leven_distances[vocab] = levenshtein_distance(word, vocab)

    # sorted by distance
    sorted_distences = dict(
        sorted(leven_distances.items(), key=lambda item: item[1]))
    correct_word = list(sorted_distences.keys())[0]
    st.write('Correct word: ', correct_word)

    col1, col2 = st.columns(2)
    col1.write('Vocabulary:')
    col1.write(vocabs)

    col2.write('Distances:')
    col2.write(sorted_distences)


if __name__ == "__main__":
    # main()
    print(levenshtein_distance("elmets", "elements"))
