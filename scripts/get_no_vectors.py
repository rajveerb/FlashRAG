import faiss, argparse

argparser = argparse.ArgumentParser(description='Get the number of vectors in the index')
argparser.add_argument('--index_file', type=str, required=True, help='Index file, for example, indexes/e5_Flat.index')

args = argparser.parse_args()

# Load 
index = faiss.read_index(args.index_file)
print("Number of vectors in the index:", index.ntotal)
# Number of vectors in the index: 21,015,324
# Index size in 61GB