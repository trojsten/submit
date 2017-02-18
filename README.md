# submit
Reusable django application for handling submits, reviews and communication with automatic judge.

### submits
`SubmitReceiver` configures one type of submits (one submit form) for a specific task.

`Submit` belongs to one `SubmitReceiver` and stores data about user's submission: file, time

### reviews
`Review` stores all feedback data: reviewer's comment, reviewed file with comments, testing protocol, score.

Each submit can have one or more reviews. Only the last review is presented to the user.

### communication with judge
- send submitted file to judge via socket connection
- receiver testing protocol via POST from judge
- parse protocol to display its content on submit page

### components of GUI
- Submit form templatetag - to upload files
- Submit list templatetag - list of a group of submits
- Submit page - a page with all information about one submit
- Admin
