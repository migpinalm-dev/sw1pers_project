from tqdm import tqdm
from ripser import ripser

def make_pers_diagram(data, thresh = 1):
    result = ripser(data, maxdim=1, thresh=1, coeff=13)    # coeff must not divide window size!
    return result['dgms']

def make_pers_diagrams(emb_windows):
    diagrams = []
    print()
    print("Forming persistence diagrams...\n")
    for window in tqdm(emb_windows):
        dgm = make_pers_diagram(window, thresh = 1)
        diagrams.append(dgm)
    return diagrams