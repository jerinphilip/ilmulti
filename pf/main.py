from pf.dataset import MonolingualDataset

path = '/scratch/jerin/f-iitb/train.en'
save_path = '/scratch/jerin/f-iitb/'
dataset = MonolingualDataset.build(path, save_path, 10000)
for line in dataset:
    print(line)
