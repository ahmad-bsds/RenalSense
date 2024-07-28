from langchain.text_splitter import RecursiveCharacterTextSplitter


example_text = """
To the uninitiated, a data analysis may appear to follow a
linear, one-step-after-the-other process which at the end,
arrives at a nicely packaged and coherent result. In reality,
data analysis is a highly iterative and non-linear process,
better reflected by a series of epicycles (see Figure), in which
information is learned at each step, which then informs
whether (and how) to refine, and redo, the step that was
just performed, or whether (and how) to proceed to the next
step.
An epicycle is a small circle whose center moves around
the circumference of a larger circle. In data analysis, the
iterative process that is applied to all steps of the data
analysis can be conceived of as an epicycle that is repeated
for each step along the circumference of the entire data
analysis process. Some data analyses appear to be fixed and
linear, such as algorithms embedded into various software
platforms, including apps. However, these algorithms are
final data analysis products that have emerged from the very
non-linear work of developing and refining a data analysis
so that it can be “algorithmized.”
"""

def chunk_text(text: str):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 15,
        chunk_overlap= 5
    )
    text = text_splitter.split_text(text)
    return text

# text = chunk_text(example_text)
# print(text)