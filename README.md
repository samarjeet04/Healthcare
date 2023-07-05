# Healthcare
import fitz    

# opening the pdf file  
my_pdf = fitz.open("AR_Finland_2021.pdf")
  
# input text to be highlighted  
my_text = "blood"  
my_text1="aid"

for i in range(0, 10):
    # iterating through pages for highlighting the input phrase
    for n_page in my_pdf:
        matchWords = n_page.search_for(str(i)) + n_page.search_for(my_text) + n_page.search_for(my_text1)
        # print(matchWords)
        for word in matchWords:
            my_highlight = n_page.add_highlight_annot(word)
            my_highlight.update()

        # saving the pdf file as highlighted.pdf
    my_pdf.save("highlighted_text.pdf")
