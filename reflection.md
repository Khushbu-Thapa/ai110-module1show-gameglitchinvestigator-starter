# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guess is 5 , Secret is 96 | Hint should be Go Higher | Hint Says Go Lower | N/A Console Error |
| Guess 96 , Secret is 27 | Hint should be Go Lower | Hint Says Go Higher | N/A Console Error |
| Enter the guess multiple times | When changing the Difficulty level, the game should reset | Game Over. Start a new game to try again | N/A |
| New Game | When clicked New Game, page should refresh and Error should go away | Error in the screen persists | N/A |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
--> Claude Code

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
--> The first issue that I asked Claude Code to fix is the "Go Lower" and "Go Higher" issue that the code had. The Claude code saw the error in the logic and then fixed it. This was on the point and immediately fixed the issue

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
--> When I asked Claude Code to look into the issue that the "Enter the Guess" space is not being set to empty after "New Game" is clicked. Claude code ran and did some thinking. After a while the codebase has been changed. But this didn't fix the issue. 

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  --> I tested it after codebase is updated.

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
  --> I installed pytest and ran it. All of the test written by code passed.

- Did AI help you design or understand any tests? How?
  --> Yes. Ut added mandatory and edge cases tests in order to help the app crash or fail.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
--> As per my understanding, Streamlit "reruns" allows the python script in the backend to run once the page is touched. Unlike any other Js based application where js script or functions are triggered only when buttons are clicked. 
 --> Since the python script is executed everytime, the session state is something like storage box which is used to store the variables and values. That is why one of the bug I found in the application was "Not clearing of the Enter the guess" value and Game Over/You Already Won messages. These are also stored for that particular user tab so even "New Game" is clicked, these information along with other essential information are saved. That is the reason, there were these bugs.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
   --> Always verify the changes along with reviewing the code update AI has done 
   --> Sometimes the fixes are not implemented the way you desire them to be. 

- What is one thing you would do differently next time you work with AI on a coding task?
 --> Follow the changes the AI is making to know what changes done so that troubleshooting is easier for me. 

- In one or two sentences, describe how this project changed the way you think about AI generated code.
  --> It is easier to take help of AI and if right instructions given, it can help in creating and fixing issue easily. 
