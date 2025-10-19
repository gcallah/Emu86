### Styling
* [ ] Headers dissapear after select `MIPS Mnemonic Machine Language HEX`
* [ ] [feedback page](Emu86/templates/feedback.html) weird placeholder of empty spaces for the textarea section

### Security
* [X]  [mysite settings](mysite/settings.py) secrete key exposed
  * [X] Add the instruction to create `.env` to README
  * [ ] Write a test to ensure `SECURITY_KEY` exists in `.env`

### Possible typo
* [ ] [help page](Emu86/templates/help.html):  In `About Emu86` section: `As of right now, we do not cover these AT&amp;T addressing modes: (%ebx, %eax, 2) and var(, 1). If needed,`

### Failures
* [X] Django/Python Compatability (`Django module not found`)
  * [X] Upgraded Django version installed
  * [X] Upgraded Django syntax for URL
