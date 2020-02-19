===========
mentormatch
===========

J&J Cross-Sector Mentoring Program utility that matches mentors with mentees.

Applications Format
--------------------
* In MS Forms, export the applications to excel. Do this for both mentors and mentees.
* Combine these into a single excel file, with the mentor applications on a **mentor** worksheet and the mentees on a **mentee** worksheet.
* Add a third worksheet titled **favor**.
  * Cell A1: ``wwid``
  * Cell B1: ``favor``
  * Filling out the remaining rows of this worksheet is optional, but the worksheet and its headers are not.
  * If there are any **mentees** you want to give priority to, add their wwid to column A. Add a positive integer to column B. Default to assigning a **favor** of 1 to these mentees. That alone with give them preference over all others. If you want to give any mentees on this sheet priority over others on the sheet, then give them a higher number. You can use as many different numbers as you like. 


Quick Start
-----------------
1. **Install Python**
    a. Install Python 3.8. You'll need elevated priveleges to do so. Be sure to check the "Add to PATH" box during installation.
#. **Open a terminal (Command Prompt or PowerShell)**
    a. Press the ``Windows Key`` and type ``cmd`` to search for the Windows command prompt
#. **Install** ``mentormatch``
    a. In Command Prompt, type ``pip install mentormatch``
    #. If this throws an error, try instead: ``python -m pip install mentormatch``. Hint: the up-arrow accesses previous commands to reduce the amount of typing you need to do.
#. **Run** ``mentormatch``
    a. In Command Prompt, type ``mentormatch``
    #. Follow the instructions to 
