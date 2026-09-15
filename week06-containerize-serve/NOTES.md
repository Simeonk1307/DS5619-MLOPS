# NOTES.md — Week 6: Containerize and Serve a Detector

**Student ID used with `generate_for_student.py`:**
<!-- paste the --student-id value you used -->
112301031


## Built image size

<!-- What image size did `docker images` report for week6-detector? -->
157MB


## Swapping in a real checkpoint

<!-- What's the single biggest thing you'd change about this Dockerfile if
     src/mock_detector.py were swapped for a real torch-based checkpoint?
     (Think about what that does to build time and image size.) -->
- to use pytorch compatible base image
- to add torch as a dependency in requirements.txt which will significantly increase build time and size of image
