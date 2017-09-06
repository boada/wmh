def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
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

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    #plt.title(title)
    #plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=90)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        if j > i:
            plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    #plt.ylabel('Caster 2')
    #plt.xlabel('Caster 1')

c1 = [i[0] for i in df['list1'][mask]]
c2 = [i[0] for i in df['list2'][mask]]
size = unique(c1+c2).size
cm = np.zeros((size,size), dtype=int)
d = {n:i for i, n in enumerate(unique(c1+c2))}
for x,y  in zip(c1, c2):
    if d[y] > d[x]:
        cm[d[x]][d[y]] += 1
    else:
        cm[d[y]][d[x]] += 1

plot_confusion_matrix(cm, classes=unique(c1+c2))
