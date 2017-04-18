## Relativity Space - Software engineering candidates' homework
This readme contains problems that candidates can choose to work on as a take home assignment

### Instructions:
1. fork this repo
2. choose one of the problems from this repo to solve
    * You can use any language you want but python is recommended
    * Depending on your time and level of enthusiasm about the problem you can choose to do only parts of the problem
3. Once done send the link to your fork repo back to your interviewer

Open an issue on this repo if you have any questions about the problems.

Adding clarification and description as comments or readme file is welcomed if needed.

### Problem 1: Machine Vision - Feature extraction
The goal of the program is to extract features from a video file
1. Check out the video in /videos/weld.mp4
2. Use language and platform of your choice to measure width of the bead as shown in image below. You can choose any arbitrary  scale if you stay consistent.
  ![weld width](/images/weld_width.png)
3. You can first do measurement on only one frame
4. If you feel enthusiastic, apply the algorithm to every frame on the video
5. Capture measurements at 20Hz in a csv files that records width of the weld bead for each time increment

### Problem 2: STL manipulation
The goal of the program is to generate a STL file from any given multivariable expression.
1. The program will take a mathematical expression from command line. The expression will include two variables x and y and supports addition, subtraction, multiplication,, devision, and power function. The expression represents a 3D surface, in which x, y, and result of expression are three cartesian variables.
2. Program's task is to output an STL file that corresponds with the expression.
3. For extra bonus, you can also out put an image of the STL mesh.
4. The mesh should be fine enough to fairly represent details of the geometry.
