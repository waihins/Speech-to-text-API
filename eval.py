def wer_calculator(script: str, ref: str) -> None:
    """
    Take input string and reference string and calculate word error rate (WER) with Levenshtein distance.
    Then print out the performace report.

    Parameters:
        script (str): input string
        ref (str): reference string
    """

    origin = script.split(" ")
    reference = ref.split(" ")

    m = len(origin)
    n = len(reference)
    
    # if one of the lists is empty
    if m * n == 0:
        return m + n
    
    # create dp and backtrack table
    dp = [ [0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            delete = dp[i - 1][j] + 1
            insert = dp[i][j - 1] + 1
            substitute = dp[i - 1][j - 1] 
        
            if origin[i - 1] != reference[j - 1]:
                substitute += 1

            dp[i][j] = min(delete, insert, substitute)

    insertion, deletion, substitute, correct = backtrack(dp)
    print_report(insertion, deletion, substitute, correct, len(reference), dp[m][n])

def backtrack(dp: list) -> list:
    """
    Helper function to backtrack the operations done by WER calculator
    """

    i = len(dp) - 1
    j = len(dp[0]) - 1

    insertion = 0
    deletion = 0
    substitute = 0
    correct = 0

    while i and j:
        up = dp[i-1][j]
        left = dp[i][j-1]
        diag = dp[i-1][j-1]
        target = min(up, left, diag)

        if target == diag:
            if diag == dp[i][j]:
                correct += 1
            else:
                substitute += 1
            i -= 1
            j -= 1
        elif target == up:
            insertion += 1
            i -= 1
        else:
            deletion += 1
            j -= 1
        
    return (insertion, deletion, substitute, correct)

def print_report(insertion: int, deletion: int, substitute: int, correct: int, ref: int, abs: int) -> None:
    """
    Print WER report with details
    """

    print("Performace Status Report\n")
    print("Total Number in Reference Text: {}".format(ref))
    print("Number of Insertion: {}".format(insertion))
    print("Number of Deletion: {}".format(deletion))
    print("Number of Substitution: {}\n".format(substitute))
    print("Word Accuracy: {:.2f}%".format(correct / ref * 100))
    print("Word Error Rate: {:.2f}%".format((substitute + deletion + insertion) / ref * 100))
    print("Word Error Rate (Absolute): {:.2f}%".format(abs / ref * 100))

if __name__ == "__main__":
    context = "hello this is podcasting house and if you've never joined us before this is a service we provide for you we put in front of you a suggestion first up all the podcast you might like to subscribe to and then if you like it you can go on over to bbc sounds if you're in the uk and"
    ref = "hello this is podcasting house and if you've never joined us before this is a service we provide for you we put in front of you a suggestion first up all the podcast you might like to subscribe to and then if you like it you can go on over to bbc sounds if you're in the uk and"
    wer_calculator(context, ref)