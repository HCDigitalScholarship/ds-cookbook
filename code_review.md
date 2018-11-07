A code review is an opportunity for your co-workers to read your code and give feedback. It helps keep everyone on a project up-to-date about what's happening, it helps you improve your coding skills, and it reduces the chances of bugs making it to production.

The workflow for a code review is

1. You submit a pull request for your code on GitHub (step-by-step instructions below).
2. One or more of your co-workers look at your code, comment on it, and either approve it or request changes (step-by-step instructions below).
3. If your code review was approved, then you can merge and push it. If not, you need to make the requested changes and submit another commit to the pull request.

## How to create a code review on GitHub

1. Work on the code until you're ready to make a commit.

2. Switch to your personal branch, if you haven't already. If the branch doesn't exist, create it with `git checkout -b <your-username>`.
```
$ git checkout <your-username>
```

3. Make a commit locally on your own branch.
```
$ git commit
```

4. Push the branch to GitHub. If the branch hasn't been pushed to GitHub before, you'll need to run `git push --set-upstream origin <branch-name>` instead.
```
$ git push
```

5. Go to your project's main page on GitHub. There will be a box labelled "Your recently pushed branches" with your branch name and a button labelled "Compare & pull request." Click the button, which will bring you to a new page.

6. Click the cog next to "Reviewers" on the right and add whoever you'd like to review your pull request.

7. Make sure that the box at the top indicates that you are merging your branch into the master branch of the same repository. On some projects, like GAM, the default option is to merge into a forked version of the repository, which is not what you want.

8. Click "Create pull request."

9. Now it's time for your reviewers to take a look at your code. Instructions for that are in the section below. If all your reviewers approve your pull request, then you can merge your branch into master (locally, not on GitHub) and push it:
```
$ git checkout master
$ git merge <branch-name-from-step-1>
$ git push origin master
```

10. If one or more of your reviewers requested changes, then go ahead and make the changes locally and go back to step 1. It's a good idea to give your next commit the same title as your first one, except with `(revision for PR #nnn)` at the end, where `nnn` stands for the number of your PR on GitHub. Your commit will automatically get added to your open pull request, so you won't have to repeat steps 4-6.


## How to approve a code review or request changes on GitHub

1. Go to your project's main page on GitHub. Click the "Pull requests" tab at the top.

2. Click on the code review you want to look at.

3. Click on the tab that says "Files changed."

4. On this page, you should see the diff of all the changes made in the commit. If you hover over a line of the code, a blue button will pop up. Click it to add a comment (see below for guidelines on commenting). When the comment form pops up, make sure to choose the "Start review" button.

5. Once you've read all the code and made comments as appropriate, you can click the "Review changes" button at the top right. If you didn't have anything for them to change, you can approve the pull request. Otherwise, you should select "Request changes." Don't be afraid to request changes! Most code reviews will go through at least one revision before they're approved.

6. If you did request changes, then go back to step 1 once the changes have been made (it will be under the same pull request).


## Guidelines for code review
In addition to the guidelines below, please be kind when you are reviewing others' code. A code review should be a welcoming and collaborative environment, not a confrontational one.

### Things you should definitely comment on
A code review should not be approved if it contains any of these violations.

- Code errors
- Seriously flawed or unclear design (as long as you can articulate what is wrong with it and suggest some way to improve it--simply commenting "bad design" is not very helpful for the coder)


### Things you can comment on, but don't need to
A code review may be approved even if it contains some of these violations. It is up to the discretion of the reviewer.

- Minor improvements (e.g., making a function a line or two shorter)
- Missing tests
- Questions about the code
- Code style (for Python, follow [PEP8](https://www.python.org/dev/peps/pep-0008/) as much as possible)
- Typos in code comments

Feel free to leave a comment with positive feedback if you see something that you like!
