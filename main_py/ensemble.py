

def run_ensemble_entropy_order(length, ensembleSize, interaction=0):
    import time

    for en in range(ensembleSize):
        start_t = time.time()



        end_t = time.time() - start_t
        print("Iteration {:4f} | Time elapsed {:.5f} sec".format(en, end_t))
        pass

    pass