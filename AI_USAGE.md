# AI Usage


## Which AI tool(s) I used
 For this assignment i used Claude ai and chatgpt

## The prompts I gave
i want to complete this assignment 
firstly explain me what exactly  i have to do
also explain me the logic to build this

ok so where should i start and explain me

okay tell me everything to do in one go

is there any changes that i should make or something

i have not created a virtual environmnet will it create an issue

do we need to create something visual in this assignment


## What output I accepted
from this system i accepted an output of running test cases , if the test cases run successfully then our logic is correct and if some test cases fail it means that there is some issue in our code
So through this system i ran  25 test cases each of which was run successfully, which means that the logic behind whether the box would be suitable for the order or not is correct

## What output I rejected or modified
So when i first ran the test cases test helpers didn’t produce decimal values this caused 12 failing tests , later i checked what was wrong with my code fixed it and found that all my test cases are successfully running now.

## Mistakes the AI made
So due to some mistakes in my prompt views.py was broken by shell escaping may be it had literal backslashes in the code, so i modified my code and fixed this issue. Also the test helpers did not produce decimal values this was also fixed. Also many minor changes were made in the system.

## How I verified the final code
So to verify the final code i run python manage.py first. Then i run python manage.py test -v 2 to check the test cases. So after this all my 25 test cases were run successfully with 0 failures. So the tests covered weight limits, dimensions, product rotation, quantities, exact-fit cases, invalid inputs, and API error handling.

## What did you learn in this assignment
 So by this assignment i learnt how selecting a shipping box is not just about comparing total volume. For this the individual dimensions and also the possible rotations need to be considered. Also i learnt that how i can improve the correctness or accuracy of the system by making the right changes. It also helped me in developing my knowledge in backend handling and logic building.
