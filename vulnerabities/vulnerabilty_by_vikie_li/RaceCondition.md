# What are race conditions
- Race conditions are one of the most interesting vulnerabilities in modern web applications. 
- They stem from simple programming mistakes developers often make, and these mistakes have proved costly: attackers have used race conditions to steal money from online banks, e-commerce sites, stock brokerages, and cryptocurrency exchanges.

# Mechanisms
- A race condition happens when two sections of code that are designed to be executed in a sequence get executed out of sequence. 
- To understand how this works, you need to first understand the concept of concurrency. 
- In computer science, concurrency is the ability to execute different parts of a program simultaneously without affecting the outcome of the program. 
- Concurrency can drastically improve the performance of programs because different parts of the program’s operation can be run at once.
- Concurrency has two types: multiprocessing and multithreading. 
- Multiprocessing refers to using multiple central processing units (CPUs), the hardware in a computer that executes instructions, to perform simultaneous computations. 
- On the other hand, multithreading is the ability  of a single CPU to provide multiple threads, or concurrent executions. 
- These threads don’t actually execute at the same time; instead, they take turns using the CPU’s computational power. 
- When one thread is idle, other threads can continue taking advantage of the unused computing resources. 
- For example, when one thread is suspended while waiting for user input, another can take over the CPU to execute its computations.
- Arranging the sequence of execution of multiple threads is called scheduling. 
- Different systems use different scheduling algorithms, depending on their performance priorities. 
- For example, some systems might schedule their tasks by executing the highest-priority tasks first, while another system might execute its tasks by giving out computational time in turns, regardless of priority.
- This flexible scheduling is precisely what causes race conditions. 
- Race conditions happen when developers don’t adhere to certain safe concurrency principles, as we’ll discuss later in this chapter. 
- Since the scheduling algorithm can swap between the execution of two threads at any time, you can’t predict the sequence in which the threads execute each action.
- In summary, race conditions happen when the outcome of the execution of one thread depends on the outcome of another thread, and when two threads operate on the same resources without considering that other threads are also using those resources. 
- When these two threads are executed simultaneously, unexpected outcomes can occur. 
- Certain programming languages, such as C/C++, are more prone to race conditions because of the way they manage memory

# When a Race Condition Becomes a Vulnerability
- A race condition becomes a vulnerability when it affects a security control mechanism. 
- In those cases, attackers can induce a situation in which a sensitive action executes before a security check is complete. 
- For this reason, race condition vulnerabilities are also referred to as time-of-check or time-of-use vulnerabilities.

# Hunting for Race Conditions
- Hunting for race conditions is simple. But often it involves an element of luck. 
- By following these steps, you can make sure that you maximize your chances of success.
# Step 1: Find Features Prone to Race Conditions
- Attackers use race conditions to subvert access controls. 
- In theory, any application whose sensitive actions rely on access-control mechanisms could be vulnerable.
- Most of the time, race conditions occur in features that deal with numbers, such as online voting, online gaming scores, bank transfers, e-commerce payments, and gift card balances. 
- Look for these features in an application and take note of the request involved in updating these numbers.
# Step 2: Send Simultaneous Requests
- You can then test for and exploit race conditions in the target by sending multiple requests to the server simultaneously.
- For example, if you have $3,000 in your bank account and want to see if you can transfer more money than you have, you can simultaneously send multiple requests for transfer to the server via the curl command. 
- If you’ve copied the command from Burp, you can simply paste the command into your terminal multiple times and insert a & character between each one. 
- In the Linux terminal, the & character is used to execute multiple commands simultaneously in the background:
```
curl (transfer $3000) & curl (transfer $3000) & curl (transfer $3000)
& curl (transfer $3000) & curl (transfer $3000) & curl (transfer $3000)
```
- Be sure to test for operations that should be allowed once, but not multiple times! 
- For example, if you have a bank account balance of $3,000, testing to transfer $5,000 is pointless, because no single request would be allowed. 
- But testing a transfer of $10 multiple times is also pointless, since you should be able to do that even without a race condition. 
- The key is to test the application’s limits by executing operations that should not be repeatable.

# Step 3: Check the Results
- Check if your attack has succeeded. 
- In our example, if your destination account ends up with more than a $3,000 addition after the simultaneous requests, your attack has succeeded, and you can determine that a race condition exists on the transfer balance endpoint.
- Note that whether your attack succeeds depends on the server’s process-scheduling algorithm, which is a matter of luck. 
- However, the more requests you send within a short time frame, the more likely your attack will succeed. 
- Also, many tests for race conditions won’t succeed the first time, so it’s a good idea to try a few more times before giving up.

# Step 4: Create a Proof of Concept
- Once you have found a race condition, you will need to provide proof of the vulnerability in your report. 
- The best way to do this is to lay out the steps needed to exploit the vulnerability. 
- For example, you can lay out the exploitation steps like so:
1. Create an account with a $3,000 balance and another one with zero balance. 
- The account with $3,000 will be the source account for our transfers, and the one with zero balance will be the destination.
2. Execute this command:
```
curl (transfer $3000) & curl (transfer $3000) & curl (transfer $3000)
& curl (transfer $3000) & curl (transfer $3000) & curl (transfer $3000)
```
- This will attempt to transfer $3,000 to another account multiple times simultaneously.
3. You should see more than $3,000 in the destination account. 
- Reverse the transfer and try the attack a few more times if you don’t see more than $3,000 in the destination account.

# Finding Your First Race Condition!
- Now you’re ready to find your first race condition. Follow these steps to manipulate web applications using this neat technique:
1. Spot the features prone to race conditions in the target application and copy the corresponding requests.
2. Send multiple of these critical requests to the server simultaneously. 
- You should craft requests that should be allowed once but not allowed multiple times.
3. Check the results to see if your attack has succeeded. And try to execute the attack multiple times to maximize the chance of success.
4. Consider the impact of the race condition you just found.
5. Draft up your first race condition report!