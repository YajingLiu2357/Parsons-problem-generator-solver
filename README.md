# Parsons-problem-generator-solver

Macao Polytechnic University COMP490 Final Year Project (Parsons problem generator and solver)

Student: Yajing Liu

Supervisor: Philip Lei

## Report

Basic informaiton of this project is shown in the following sections. And more details about this project can be seen in this [full report](https://github.com/YajingLiu2357/Parsons-problem-generator-solver/blob/main/document/P1908345_Jane_Final%20Report.docx).

## Introduction

Parsons problem is a type of programming question to let students drag and drop to reorder the jumbled prepared blocks of codes to build the unique predefined solutions. This type of question has been applied in introductory programming courses (CS1) popularly. However, the application scope of Parsons problem has seldom been expanded to higher-level course such as Data Structures and Algorithms (CS2). Since students taking this course should be able to write some codes, the application of Parsons problem in CS2 should focus less on specific code writing and more on high level issues. Thus it is of the essence to expand traditional Parsons problem and make it more applicable in CS2.

This project aims to build a web application to apply Parsons problem in CS2. In this project, not only the common functions of traditional Parsons problem should be implemented (including inputting problems and solutions in Python, generating Parsons problems, solving Parsons problems and giving feedbacks), but also some changes should be made to adapt the specific exercise in CS2 (more different types of questions and more ways to handle difficulty levels).

## Problem Analysis

There are plenty of differences between the exercises in CS1 and CS2, it is not so proper to apply Parsons problem directly in CS2 without tailored improvement. To illustrate the difference in detail, four kinds of concrete questions from exercises in CS2 are analyzed(Completed analysis can be seen in the [report](https://github.com/YajingLiu2357/Parsons-problem-generator-solver/blob/main/document/P1908345_Jane_Final%20Report.docx)).

- **Object-oriented programming:** this model is not involved in CS1, but it is the foundation to implement different data structures. Because of involving this mode, the uniqueness of correct answer is broken since the order of methods in a class can be changed without affecting correctness. To handle this problem, the project should only check the availability and the contents of methods but ignore the positions of the methods.

- **Algorithm analysis:** this concept is first introduced in CS2 and not mentioned in CS1. To help students to learn algorithm analysis, comments is introduced as options for choosing proper big O classes to describe codes.
- **Recursion:** the recursion method requires students with deeper understanding in the whole picture of entire methods besides concrete lines like CS1. For this reason, the traditional Parsons problem cannot reduce the difficulty as usual through providing code reading. To give students some ideas, a recursion question can be divided into several steps to let students build from subproblem to the original recursion codes.
- **Comparison:** there are some similar codes in CS2, for example the same data structure with different implementation or different algorithm for solving the same problems. Although it is ok to use the traditional Parsons problem individually for each one, it would be more worthwhile to have ways to help students compare similar codes and consolidate the difference and similarities between these codes. Comparison can be done through splitting two solutions from one code pool.

## Expanded Parsons Problem Design

Questions can be summarized as five different types (Same question can have multiple versions with different question types. Students can switch to easier versions.):

- **Traditional:** the most basic Parsons problem – only support rearranging jumbled predefined codes and getting feedback about the reordered answers. This type of Parsons problem is used in CS1.
- **Multiple Step:** this type of Parsons problem divides the original codes into several steps to let students solve complex problems by solving each small part. It can be used in recursion problem or be used as pre-scaffold
- **Context:** some ordered code blocks are provided as hints. This type of question can be used to handle the difficulty.
- **Algorithm Comparison:** this type of question is used to compare similar algorithms. In this type of question, students split one group of jumbled codes into two solutions.
- **Algorithm Analysis:** this type of question can introduce the time complexity of algorithm analysis by annotating given codes with big O class.

## Major Techniques and Tools Used

**Front-end**: TypeScript, Tailwind CSS, Vue.js 3.0, some Vue tools (Vue Router, Vuex, Vue Draggable), Axios

**Back-end**: Python, FastAPI, MariaDB

## Outcomes

Only the screenshots about different types of questions in student end are shown.  The completed demo of whole project can be seen in this [demo video](https://www.youtube.com/watch?v=PltkgK50wnw).

### Traditional Parsons Problem

The follwoing figure shows the question page of traditional Parsons problem. Students need to drag the jumbled codes from left code pool, drop the codes in the right answer sheet in order, and push arrow buttons to set proper indent of codes. After finishing, the codes are marked as different background colors to give students further instruction.

![traditional](/Users/liuyajing/Documents/Final Year Project/Parsons-problem-generator-solver/document/traditional.png)

### Context

The following figure shows the question page of Parsons problem with context. Compared to the traditional Parsons problem, this form provides partially ordered code and placeholders in the initialization phase. This format allows students to get more hints by reading the code in context, thus reducing the difficulty of the problem.

![context](/Users/liuyajing/Documents/Final Year Project/Parsons-problem-generator-solver/document/context.png)

### Multiple Step

The following figure shows the question page of Multiple Step Parsons problem. Compared to the traditional Parsons problem, this form supports breaking a complex problem into several consecutive steps. It gives students hints by labeling step number of different codes.

![multiple_step](/Users/liuyajing/Documents/Final Year Project/Parsons-problem-generator-solver/document/multiple_step.png)

### Algorithm Comparison

The following figure shows the question page of Algorithm Comparison. Compared to the traditional Parsons problem, students need to split two algorithms mixed in left code pool to middle and right answer sheets separately. This form is worthwhile for students to distinguish similar algorithms and prevent students from using them mostly because of blurry memory.

![compare](/Users/liuyajing/Documents/Final Year Project/Parsons-problem-generator-solver/document/compare.png)

## Conclusion

In conclusion, this project explored the possible application of Parsons problem in Data Structures and Algorithms. The new forms of Parsons problem that were developed in this project can support some situations not involved in introductory programming, including different block property, the coexistence of lines and blocks, and the existence of multiple solutions. These new forms can also handle the difficulty level in different ways.

The project’s main contribution is to provide a new technical tool that can help students learn data structures and algorithms more effectively. It can not only improve students’ engagement and reducing students’ cognitive load as the traditional Parsons problem, but also can help students to consolidate knowledge though comparing similar concepts.

In the future, experiments will be conducted to compare the effectiveness of this tool with traditional learning methods. In addition, questionnaires will be sent to students and lecturers to collect their opinions on improving system.
