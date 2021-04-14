import argparse
import os
import pickle
from progress.bar import IncrementalBar 

from length_scorer import mean_length_score
from dataset_loader import load_text
from affix_searcher import Affix_searcher

def main(args):
    print('Loading data...')
    text = load_text(args.text)
    if (args.modus == 'training'):
        print('Starting training...')
        print('Counting mean length...')
        score = mean_length_score(text)
        length = int(score/args.coefficient)
        searcher = Affix_searcher(text, length, args.frequency)
        searcher.train()
        with open(os.path.join(args.folder, 'model.pkl'), 'wb') as output:
            pickle.dump(searcher, output, pickle.HIGHEST_PROTOCOL)
            print('Saved!')
    else:
        print('Starting prediction...')
        with open(os.path.join(args.folder, 'model.pkl'), 'rb') as inp:
            searcher = pickle.load(inp)
            dataset = searcher.predict(text)
            with open(os.path.join(args.folder, 'output.txt'), 'w', encoding='utf-8') as inp:
                counter = 0
                bar = IncrementalBar('Saving predictions...', max=len(text.split(' ')))
                for i in dataset:
                    morphemes_list = ""
                    if i[1]:
                        for m in i[1]:
                            morphemes_list += m + "|"
                    inp.write(str(counter) + "\t" + i[0] + "\t" + morphemes_list + "\n")
                    counter = counter + 1
                    
            

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--modus', '-m', default='training')
    parser.add_argument('--text', '-t')
    parser.add_argument('--coefficient', '-c', default=2)
    parser.add_argument('--folder', '-f', default=os.path.dirname(os.path.realpath(__file__)))
    parser.add_argument('--frequency', '-fr', default=100)
    args = parser.parse_args()
    main(args)