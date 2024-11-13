import topmost
from topmost.data import RawDataset
from topmost.preprocessing import Preprocessing


def train_lda_topmost(docs):
    preprocessing = Preprocessing(vocab_size=10000, stopwords='English')

    device = 'cuda' # or 'cpu'
    dataset = RawDataset(docs, preprocessing, device=device)

    trainer = topmost.trainers.FASTopicTrainer(dataset, verbose=True)
    top_words, doc_topic_dist = trainer.train()

    return top_words, doc_topic_dist, trainer


def inference_lda_topmost(trainer, new_docs):
    new_docs = [
        "This is a document about space, including words like space, satellite, launch, orbit.",
        "This is a document about Microsoft Windows, including words like windows, files, dos."
    ]

    new_theta = trainer.test(new_docs)
    print(new_theta.argmax(1))
    return new_theta