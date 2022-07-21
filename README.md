# Digidoc
## What is digidoc?
Its a realtime document scanner or detector. It
automatically crops document from picture and resizes it to
specific dimensions.
https://ibb.co/QFwMDfR
## Where it is helpful?
It is helpful in offices where we have to scan documents
very quickly. For that we can set a camera shooting
towards table. If someone puts document on table, it will
automatically record the document and crop it and wait for
confirmation to save it in a specific folder.
## Working:
We tried using various ways to recognize documents in
noisy backgrounds by using python-openCV and setteled
to the most efficient and accurate configurations as below:
1. We first blur image to remove any noise.
2. Edges are then calculated using cv2-canny function
3. Then houghlines are calculated with some
configurations
4. Lines are then filtered according to their angles to get
parallel sets of lines
5. Parallel lines are selected to get biggest parallelogram
forming in picture. Its nothing but our document
6. This parallelogram shape is then converted to rectangle
by using perspective transform.
7. Finally we got the document image which we resize
into dimensions we want and show to user.
8. Further features like saving document or increasing
contrast can be added according to users needs(not
included in project)Functions Explainations:
I. select_doclines(): doclines create set of parallel lines
II. border_detect(): it detects borders i.e. selects parallel
lines to get biggest parallelogram possible
III. intersection(): finds corners from selected 4 lines
Requirements:
 Python(3.x recommended)
 openCV(3.4.x recommended)
 Numpy
