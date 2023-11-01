from collections import defaultdict
import random

tries = 0

def main():
    
    alphabet_freq_dict = defaultdict(lambda: defaultdict(int)) # 0-4 인데스에서 각 알파벳의 빈도를 저장. 빈도는 all_answers.txt를 기반으로 함
    wrong_alph = set() # Guess 한 후 틀리다 나온 알파벳 저장

    with open('all_answers.txt', 'r') as all_words:
        possible_words = all_words.read().split('\n')
    
    # 시뮬을 위해 임의로 답 설정
    num = random.randint(0, len(possible_words))
    answer = possible_words[num]
    print("Answer is: " + answer)

    # 모든 인덱스의 알파벳 빈도 구하기
    for word in possible_words:
        for i in range(5):
            alphabet_freq_dict[i][word[i]] += 1
            
    # 모든 단어들을 가능성 높은 순으로 정렬
    possible_words.sort(key=lambda x: sum(alphabet_freq_dict[i][x[i]] for i in range(5)), reverse=True)
    
    # 첫번째 Guess
    guess = possible_words[0]
    possible_words = possible_words[1:]
    
    feedback = checkAnswer(answer, guess, wrong_alph)
    
    # 첫번째 Guess에서 y, g 못구했을 시
    index_stopped = 1
    while('y' not in feedback and 'g' not in feedback):
        for i in guess:
            wrong_alph.add(i)
        for i, word in enumerate(possible_words):
            flag = 0
            for letter in wrong_alph:
                if letter in word:
                    flag = 1
                    break
            if flag == 0:
                index_stopped = i
                guess = word
                break
        feedback = checkAnswer(answer, guess, wrong_alph)
    if index_stopped > 1: 
        possible_words = possible_words[index_stopped:] 
        
    # 답 구할 때 까지 반복
    new_possible_words = []
    while(True):
        for index, word in enumerate(possible_words):
            
            flag = checkIfPossibleGuess(word, guess, wrong_alph, feedback)
                    
            if not flag:
                new_possible_words = possible_words[index+1:]
            else:
                new_possible_words = possible_words[index:]
                guess = new_possible_words[0]
                feedback = checkAnswer(answer, guess, wrong_alph)
    
def checkIfPossibleGuess(word, guess, wrong_alph, feedback):
    # 단어에 기존에 제외되 알파벳이 있는 경우 제외
    for alph in word:
        if alph in wrong_alph:
            return 0
        
    # 기존 Guess에서 얻은 feedback을 통해 단어 제외
    for i, letter in enumerate(guess):
        if (feedback[i] == 'g' and word[i] != letter):
            return 0
        if (feedback[i] == 'y' and (letter not in word or letter == word[i])):
            return 0
    return 1
    
def checkAnswer(answer, guess, wrong_alph):
    '''
    Answer 와 Guess 를 비교하고 둘이 똑같으면 프로그램 종료. 아니면 크기 5의 리스트를 리턴함. 
    리스트 구성: 현재 인덱스에 단어가 일치하면 g. 단어 존재하지만 인덱스 틀림 y. 그냥 없음 -.
    '''
    
    global tries
    tries+=1
    print("Guess is: " + guess + ".", end='\t')
    
    if answer == guess:
        print(f"Guess is correct. Game ended in {tries} tries")
        exit()
        
    feedback = []
    for i, letter in enumerate(guess):
        if letter == answer[i]:
            feedback.append("g")
        elif letter in answer:
            feedback.append("y")
        else:
            wrong_alph.add(letter)
            feedback.append('-')
    print("Guess is incorrect: " + str(feedback))
    return feedback
    
def firstGuess():
    pass


if __name__ == '__main__':
    main()