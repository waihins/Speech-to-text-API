import numpy

def WordErrorRate(script: str, ref: str) -> int:
    """
    Take input string and reference string and calculate word error rate (WER) with Levenshtein distance.

    Parameters:
        script (str): input string
        ref (str): reference string
    
    Return:
        WER (int): word error rate between two strings
    """

    origin = script.split(" ")
    reference = ref.split(" ")

    m = len(origin)
    n = len(reference)
    
    # if one of the lists is empty
    if m * n == 0:
        return m + n
    
    # create dp table
    d = [ [0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        d[i][0] = i
    for j in range(n + 1):
        d[0][j] = j
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            delete = d[i - 1][j] + 1
            insert = d[i][j - 1] + 1
            substitute = d[i - 1][j - 1] 
        
            if origin[i - 1] != reference[j - 1]:
                substitute += 1

            d[i][j] = min(delete, insert, substitute)
    
    return d[m][n] / n

if __name__ == "__main__":
    context = "this is texting input uh"
    ref = "this is a testing input"
    print(WordErrorRate(context, ref))