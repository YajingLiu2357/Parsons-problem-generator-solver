# Parsons-problem-generator-solver

Macao Polytechnic University COMP490 Final Year Project (Parsons problem generator and solver)

Student: Yajing Liu

Supervisor: Philip Lei

## Report

Basic information about this project is shown in the following sections. And more details about this project can be seen in this [full report](https://github.com/YajingLiu2357/Parsons-problem-generator-solver/blob/main/document/P1908345_Jane_Final%20Report.docx).

## Introduction

Parsons problem is a type of programming question to let students drag and drop to reorder the jumbled prepared blocks of codes to build unique predefined solutions. This type of question has been applied in introductory programming courses (CS1) popularly. However, the application scope of Parsons problem has seldom been expanded to higher-level course such as Data Structures and Algorithms (CS2). Since students taking this course should be able to write some codes, the application of Parsons problem in CS2 should focus less on specific code writing and more on high-level issues. Thus it is of the essence to expand the traditional Parsons problem and make it more applicable in CS2.

This project aims to build a web application to apply Parsons problem in CS2. In this project, not only the common functions of traditional Parsons problem should be implemented (including inputting problems and solutions in Python, generating Parsons problems, solving Parsons problems, and giving feedback), but some changes should be made to adapt the specific exercise in CS2 (more different types of questions and more ways to handle difficulty levels).

## Problem Analysis

There are plenty of differences between the exercises in CS1 and CS2, it is not so proper to apply Parsons problem directly in CS2 without tailored improvement. To illustrate the difference in detail, four kinds of concrete questions from exercises in CS2 are analyzed(Completed analysis can be seen in the [report](https://github.com/YajingLiu2357/Parsons-problem-generator-solver/blob/main/document/P1908345_Jane_Final%20Report.docx)).

- **Object-oriented programming:** This model is not involved in CS1, but it is the foundation to implement different data structures. Because of involving this mode, the uniqueness of the correct answer is broken since the order of methods in a class can be changed without affecting correctness. To handle this problem, the project should only check the availability and the contents of methods but ignore the positions of the methods.

- **Algorithm analysis:** this concept is first introduced in CS2 and not mentioned in CS1. To help students learn algorithm analysis, comments are introduced as options for choosing proper big O classes to describe codes.
- **Recursion:** The recursion method requires students with a deeper understanding of the whole picture of entire methods besides concrete lines like CS1. For this reason, the traditional Parsons problem cannot reduce the difficulty as usual by providing code reading. To give students some ideas, a recursion question can be divided into several steps to let students build from the subproblem to the original recursion codes.
- **Comparison:** There are some similar codes in CS2, for example, the same data structure with different implementations or different algorithms for solving the same problems. Although it is okay to use the traditional Parsons problem individually for each one, it would be more worthwhile to have ways to help students compare similar codes and consolidate the differences and similarities between these codes. Comparison can be done by splitting two solutions from one code pool.

## Expanded Parsons Problem Design

Questions can be summarized as five different types (The same question can have multiple versions with different question types. Students can switch to easier versions.):

- **Traditional:** the most basic Parsons problem – only supports rearranging jumbled predefined codes and getting feedback about the reordered answers. This type of Parsons problem is used in CS1.
- **Multiple Step:** This type of Parsons problem divides the original codes into several steps to let students solve complex problems by solving each small part. It can be used in recursion problems or be used as pre-scaffold
- **Context:** Some ordered code blocks are provided as hints. This type of question can be used to handle the difficulty.
- **Algorithm Comparison:** This type of question is used to compare similar algorithms. In this type of question, students split one group of jumbled codes into two solutions.
- **Algorithm Analysis:** This type of question can introduce the time complexity of algorithm analysis by annotating given codes with big O class.

## Major Techniques and Tools Used

**Front-end**: TypeScript, Tailwind CSS, Vue.js 3.0, some Vue tools (Vue Router, Vuex, Vue Draggable), Axios

**Back-end**: Python, FastAPI, MariaDB

## Outcomes

Only the screenshots about different types of questions on the student end are shown.  The completed demo of the whole project can be seen in this [demo video](https://www.youtube.com/watch?v=PltkgK50wnw).

### Traditional Parsons Problem

The following figure shows the question page of the traditional Parsons problem. Students need to drag the jumbled codes from the left code pool, drop the codes in the right answer sheet in order, and push arrow buttons to set the proper indent of codes. After finishing, the codes are marked as different background colors to give students further instruction.

![traditional](https://github.com/YajingLiu2357/Parsons-problem-generator-solver/blob/main/document/traditional.png)

### Context

The following figure shows the question page of Parsons problem with context. Compared to the traditional Parsons problem, this form provides partially ordered code and placeholders in the initialization phase. This format allows students to get more hints by reading the code in context, thus reducing the difficulty of the problem.

![context](https://github.com/YajingLiu2357/Parsons-problem-generator-solver/blob/main/document/context.png)

### Multiple Step

The following figure shows the question page of the Multiple Step Parsons problem. Compared to the traditional Parsons problem, this form supports breaking a complex problem into several consecutive steps. It gives students hints by labeling the step number of different codes.

![multiple_step](https://github.com/YajingLiu2357/Parsons-problem-generator-solver/blob/main/document/multiple_step.png)

### Algorithm Comparison

The following figure shows the question page of Algorithm Comparison. Compared to the traditional Parsons problem, students need to split two algorithms mixed in left code pool to middle and right answer sheets separately. This form is worthwhile for students to distinguish similar algorithms and prevent students from using them mostly because of blurry memory.

![compare](https://github.com/YajingLiu2357/Parsons-problem-generator-solver/blob/main/document/compare.png)

## Conclusion

In conclusion, this project explored the possible application of Parsons problem in Data Structures and Algorithms. The new forms of Parsons problem that were developed in this project can support some situations not involved in introductory programming, including different block properties, the coexistence of lines and blocks, and the existence of multiple solutions. These new forms can also handle the difficulty level in different ways.

The project’s main contribution is to provide a new technical tool that can help students learn data structures and algorithms more effectively. It can not only improve students’ engagement and reduce students’ cognitive load as the traditional Parsons problem, but also can help students to consolidate knowledge though comparing similar concepts.

In the future, experiments will be conducted to compare the effectiveness of this tool with traditional learning methods. In addition, questionnaires will be sent to students and lecturers to collect their opinions on improving the system.
