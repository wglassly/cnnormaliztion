# Parse the xml files and convert to integer dataset for the Deep Learning model
python parse_with_sys.py $1 $2 $3

# Extract the embeddings for the words in the vocabulary from the pre-trained word2vec file
python extract_embeddings.py $2

# Re-compile the trec_eval script
cd trec_eval-8.0
make clean
make
cd ..
