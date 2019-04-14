#!/usr/bin/env python3

from collections import defaultdict
from matplotlib import pyplot as plt




def histogram(word_dict: defaultdict, interactive=False):
    fig = plt.figure()
    ax = plt.subplot()
    words = list(word_dict.keys())
    counts = list(word_dict.values())
    wc = zip(words, counts)
    wc = sorted(wc, key=lambda elem: elem[1], reverse=True)
    words, counts = zip(*wc)
    bars = plt.bar(words, counts, color='g', tick_label=None)

    curr_word = ax.annotate("", xy=(0,0), xytext=(40,40),textcoords="offset points",
                    arrowprops=dict(arrowstyle="->"))
    curr_word.set_visible(False)

    def update_label(label, bar):
        x = bar.get_x()+bar.get_width()/2.
        y = bar.get_y()+bar.get_height()
        curr_word.xy = (x, y)
        curr_word.set_text(label)


    def draw_labels():
        for i, bar in enumerate(bars):
            offset_x = 10*(i % 20)
            offset_y = 15*(i % 20)
            x = bar.get_x()+bar.get_width()/2.
            y = bar.get_y()+bar.get_height()
            word = ax.annotate(words[i], xy=(x,y),
                xytext=(40 + offset_x,40 + offset_y),
                textcoords="offset points",
                bbox=dict(boxstyle="round", fc="0.8"),
                arrowprops=dict(arrowstyle="-", alpha=0.2))
        fig.canvas.draw_idle()



    def show_label_on_plot_hover(event):
        vis = curr_word.get_visible()
        hover_on_bar = False
        for i, bar in enumerate(bars):
            if bar.contains(event)[0]:
                hover_on_bar = True
                update_label(words[i], bar)
                curr_word.set_visible(True)
                break
        if vis and not hover_on_bar:
            curr_word.set_visible(False)
        fig.canvas.draw_idle()

    plt.xlabel('Words')
    plt.ylabel('Occurences')
    plt.title('Histogram of words in Ed Stafford: First Man Out')
    plt.tick_params(
        axis='x',    
        which='both',
        bottom=False,
        top=False,   
        labelbottom=False)
    if interactive:
        fig.canvas.mpl_connect('motion_notify_event', show_label_on_plot_hover)
    else:
        draw_labels()
    plt.show()


