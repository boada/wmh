import matplotlib.pyplot as plt
import itertools
import numpy as np
import pandas as pd

def plot_confusion_matrix(cm,
                          classes,
                          normalize=False,
                          title='Faction',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    plt.figure(figsize=(8, 8))
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    #plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=90)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        if j > i:
            plt.text(j,
                     i,
                     format(cm[i, j], fmt),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    #plt.ylabel('Caster 2')
    #plt.xlabel('Caster 1')


if __name__ == "__main__":
    df = pd.read_json('wtc_data/wtc2017_lists.json')
    factions = df.faction.unique()

    for f in factions:
        #c1 = [i[0] for i in df.loc[df.faction == f, 'list1']]
        #c2 = [i[0] for i in df.loc[df.faction == f, 'list2']]
        c1 = [i for i in df.loc[df.faction == f, 'theme1']]
        c2 = [i for i in df.loc[df.faction == f, 'theme2']]
        size = np.unique(c1 + c2).size
        cm = np.zeros((size, size), dtype=int)
        d = {n: i for i, n in enumerate(np.unique(c1 + c2))}
        for x, y in zip(c1, c2):
            if d[y] > d[x]:
                cm[d[x]][d[y]] += 1
            else:
                cm[d[y]][d[x]] += 1

        plot_confusion_matrix(cm, title=f, classes=np.unique(c1 + c2))

        #plt.savefig('{}_caster.png'.format(f.replace(' ', '_')), bbox='tight')
        plt.savefig('{}_theme.png'.format(f.replace(' ', '_')), bbox='tight')
        plt.close()
