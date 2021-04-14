from collections import Counter
from progress.bar import IncrementalBar
import pandas as pd

class Affix_searcher:
    
    def __init__(self, text, length, limit):
        self.text = text
        self.length = length
        self.limit = limit
        self.suffixes = []
        self.prefixes = []
        self.roots = []
        
    def train(self):
        print('Collecting affixes and non-divisible words...')
        current_prefixes, current_suffixes, self.roots = self.scratch_search()
        for i in current_prefixes:
            self.prefixes.append(i[0])
        for i in current_suffixes:
            self.suffixes.append(i[0])
        self.roots.extend(self.root_search())
        new_prefixes, new_suffixes = self.additional_search()
        self.prefixes.extend(new_prefixes)
        self.suffixes.extend(new_suffixes)
    
    def predict(self, text):
        bar = IncrementalBar('Prediction...', max=len(self.text.split(' ')))
        results = []
        for u in text.split(' '):
            non_divisible = False
            morphemes = []
            for r in self.roots:
                if u == r:
                    non_divisible = True
                    break
            if non_divisible == True:
                results.append((u, morphemes))
                bar.next()
                continue            
            for s in self.suffixes:
                if u.endswith(s):
                    morphemes.append(s)
                    break
            for p in self.prefixes:
                if u.startswith(p):
                    morphemes.append(p)
                    break
            results.append((u, morphemes))
            bar.next()
        bar.finish()
        return results
                    
            
    
    def scratch_search(self):
        pseudo_prefixes = []
        pseudo_suffixes = []
        non_affixed = []
        for i in self.text.split(' '):
            if (len(i) > self.length):
                pseudo_prefixes.append(i[0:self.length])
                pseudo_suffixes.append(i[(len(i) - 1 - self.length):len(i)])
            else:
                non_affixed.append(i)
        pseudo_prefixes_counter = Counter(pseudo_prefixes).most_common(self.limit)
        pseudo_suffixes_counter = Counter(pseudo_suffixes).most_common(self.limit)
        return pseudo_prefixes_counter, pseudo_suffixes_counter, non_affixed
    
    def root_search(self):
        roots = []
        prestems = []
        poststems = []
        bar = IncrementalBar('Searching for prestems and poststems...', max=len(self.text.split(' ')))
        for u in self.text.split(' '):            
            if u in self.roots:
                bar.next()
                continue
            for s in self.suffixes:
                if u.endswith(s):
                    prestems.append(u.rstrip(s))
                    break
            for p in self.prefixes:
                if u.startswith(p):
                    poststems.append(u.lstrip(p))
                    break
            bar.next()
        bar.finish()
        bar = IncrementalBar('Splitting prestems and prefixes...', max=len(prestems))
        for u in prestems:
            coincidence_found = False
            for p in self.prefixes:
                if u.startswith(p):
                    roots.append(u.lstrip(p))
                    coincidence_found = True
                    break
            if coincidence_found == True:
                bar.next()
                continue
            else:
                roots.append(u)
                bar.next()
        bar.finish()
        bar = IncrementalBar('Splitting poststems and suffixes...', max=len(poststems))
        for u in poststems:
            coincidence_found = False
            for s in self.suffixes:
                if u.endswith(s):
                    roots.append(u.rstrip(s))
                    coincidence_found = True
                    break
            if coincidence_found == True:
                bar.next()
                continue
            else:
                roots.append(u)
                bar.next()
        bar.finish()
        return roots
    
    def additional_search(self):
        prefixes = []
        suffixes = []
        bar = IncrementalBar('Searching for prefixes and suffixes...', max=len(self.text.split(' ')))
        for u in self.text.split(' '):
            non_affixable = False
            for r in self.roots:
                if u == r:
                    non_affixable = True
                    break
                elif (u.startswith(r)):
                    suffixes.append(u.lstrip(r))
                elif (u.endswith(r)):
                    prefixes.append(u.rstrip(r))
                elif (r in u):
                    suffix, prefix = u.split(r, 1)
                    suffixes.append(suffix)
                    prefixes.append(prefix)
            if non_affixable == True:
                bar.next()
                break                    
            bar.next()        
        bar.finish()
        return prefixes, suffixes