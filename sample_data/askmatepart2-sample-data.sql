--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.6
-- Dumped by pg_dump version 9.5.6

ALTER TABLE IF EXISTS ONLY public.question DROP CONSTRAINT IF EXISTS pk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question DROP CONSTRAINT IF EXISTS fk_user_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.answer DROP CONSTRAINT IF EXISTS pk_answer_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.answer DROP CONSTRAINT IF EXISTS fk_user_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.answer DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS pk_comment_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS fk_answer_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS fk_user_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS pk_question_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.tag DROP CONSTRAINT IF EXISTS pk_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS fk_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.user_data DROP CONSTRAINT IF EXISTS pk_user_id CASCADE;

DROP TABLE IF EXISTS public.question;
CREATE TABLE question (
    id serial NOT NULL,
    submission_time timestamp without time zone,
    view_number integer,
    vote_number integer,
    title text,
    message text,
    image text,
    user_id integer,
    accepted_answer integer
);

DROP TABLE IF EXISTS public.answer;
CREATE TABLE answer (
    id serial NOT NULL,
    submission_time timestamp without time zone,
    vote_number integer,
    question_id integer,
    message text,
    image text,
    user_id integer
);

DROP TABLE IF EXISTS public.comment;
CREATE TABLE comment (
    id serial NOT NULL,
    question_id integer,
    answer_id integer,
    message text,
    submission_time timestamp without time zone,
    edited_count integer,
    user_id integer
);


DROP TABLE IF EXISTS public.question_tag;
CREATE TABLE question_tag (
    question_id integer NOT NULL,
    tag_id integer NOT NULL
);

DROP TABLE IF EXISTS public.tag;
CREATE TABLE tag (
    id serial NOT NULL,
    name text
);

DROP TABLE IF EXISTS public.user;
DROP TABLE IF EXISTS public.user_data;
CREATE TABLE public.user_data (
    id serial NOT NULL,
    login text,
    password text,
    registration_date timestamp without time zone,
    questions_number integer,
    answers_number integer,
    comments_number integer,
    user_reputation integer
);

INSERT INTO public.user_data VALUES (1, 'user1@gmail.com', '$2b$12$lLTE7KoA70AxpVdJ3yjKMuJX7jlEhyjpAxDmCvHR1XFUERWN/F4s2', '2017-04-28 08:29:00', 2, 2, 0, -200);
INSERT INTO public.user_data VALUES (2, 'user2@gmail.com', '$2b$12$lLTE7KoA70AxpVdJ3yjKMuJX7jlEhyjpAxDmCvHR1XFUERWN/F4s2', '2017-04-28 08:29:00', 1, 2, 2, 70);
INSERT INTO public.user_data VALUES (3, 'user3@gmail.com', '$2b$12$lLTE7KoA70AxpVdJ3yjKMuJX7jlEhyjpAxDmCvHR1XFUERWN/F4s2', '2017-04-28 08:29:00', 3, 3, 1, 80);
INSERT INTO public.user_data VALUES (4, 'user4@gmail.com', '$2b$12$lLTE7KoA70AxpVdJ3yjKMuJX7jlEhyjpAxDmCvHR1XFUERWN/F4s2', '2017-04-28 08:29:00', 2, 1, 4, 30);
INSERT INTO public.user_data VALUES (5, 'user5@gmail.com', '$2b$12$lLTE7KoA70AxpVdJ3yjKMuJX7jlEhyjpAxDmCvHR1XFUERWN/F4s2', '2017-04-28 08:29:00', 0, 2, 1, 20);
INSERT INTO public.user_data VALUES (6, 'admin@gmail.com', '$2b$12$X.K0XpVZyiyzL0JNeKOMZuPM..fQyhU/naH2XIQ6UeQpjcYYKhC4y', '2017-04-28 08:29:00', 0, 0, 0, 0);
-- simple user pass = 1
-- admin pass = 12345


ALTER TABLE ONLY answer
    ADD CONSTRAINT pk_answer_id PRIMARY KEY (id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT pk_comment_id PRIMARY KEY (id);

ALTER TABLE ONLY question
    ADD CONSTRAINT pk_question_id PRIMARY KEY (id);

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT pk_question_tag_id PRIMARY KEY (question_id, tag_id);

ALTER TABLE ONLY tag
    ADD CONSTRAINT pk_tag_id PRIMARY KEY (id);

ALTER TABLE ONLY user_data
    ADD CONSTRAINT pk_user_id PRIMARY KEY (id);

ALTER TABLE ONLY question
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES user_data(id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_answer_id FOREIGN KEY (answer_id) REFERENCES answer(id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES user_data(id);

ALTER TABLE ONLY answer
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id);

ALTER TABLE ONLY answer
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES user_data(id);

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id);

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT fk_tag_id FOREIGN KEY (tag_id) REFERENCES tag(id);


INSERT INTO question VALUES (1, '2021-04-20 08:29:00', 108, 47, 'How to make lists contain only distinct element in Python?', 'I am totally new to this, any hints?', NULL, 3, 2);
INSERT INTO question VALUES (2, '2021-06-15 12:50:00', 123, 55, 'What is the difference between "@" and "=" in directive scope in AngularJS?', 'And here are some relevant snippets: from the HTML and the pane directive. There are several things I do not get:
* Why do I have to use "{{title}}" with "@" and "title" with "="?
* Can I also access the parent scope directly, without decorating my element with an attribute?
* The documentation says "Often it is desirable to pass data from the isolated scope via expression and to the parent scope", but that seems to work fine with bidirectional binding too. Why would the expression route be better?', 'question2.png', 1, 1);
INSERT INTO question VALUES (3, '2021-08-22 06:13:45', 56, 16, 'What is the difference between "git pull" and "git fetch"?', 'What are the differences between git pull and git fetch?', NULL, 4, 4);
INSERT INTO question VALUES (4, '2021-10-29 02:10:00', 32, 2, 'What are metaclasses in Python?', 'In Python, what are metaclasses and what do we use them for?', NULL, 3, NULL);
INSERT INTO question VALUES (5, '2021-10-29 07:09:00', 201, 104, 'What is the difference between INNER JOIN, LEFT JOIN, RIGHT JOIN and FULL JOIN?', 'What is the difference between INNER JOIN, LEFT JOIN, RIGHT JOIN and FULL JOIN in MySQL?', NULL, 4, 7);
INSERT INTO question VALUES (6, '2021-12-03 14:53:22', 97, 45, 'Why is processing a sorted array faster than processing an unsorted array?', 'Here is a piece of C++ code that shows some very peculiar behavior. For some strange reason, sorting the data (before the timed region) miraculously makes the loop almost six times faster.', 'question6.png', 2, 8);
INSERT INTO question VALUES (7, '2021-12-05 18:02:00', 73, 35, 'How can I create a memory leak in Java?', 'I just had an interview where I was asked to create a memory leak with Java.
Needless to say, I felt pretty dumb having no clue on how to even start creating one.
What would an example be?', NULL, 1, NULL);
INSERT INTO question VALUES (8, '2021-11-29 01:15:18', 15, 9, 'Help!', '??', 'question8.png', 3, NULL);

SELECT pg_catalog.setval('question_id_seq', 8, true);


INSERT INTO answer VALUES (1, '2021-06-17 21:07:00', 92, 2, '* Why do I have to use "{{title}}" with "@" and "title" with "="?
@ binds a local/directive scope property to the evaluated value of the DOM attribute. If you use title=title1 or title="title1", the value of DOM attribute "title" is simply the string title1. If you use title="{{title}}", the value of the DOM attribute "title" is the interpolated value of {{title}}, hence the string will be whatever parent scope property "title" is currently set to. Since attribute values are always strings, you will always end up with a string value for this property in the directive has scope when using @.
= binds a local/directive scope property to a parent scope property. So with =, you use the parent model/scope property name as the value of the DOM attribute. You can nott use {{}}s with =.

With @, you can do things like title="{{title}} and then some" -- {{title}} is interpolated, then the string "and them some" is concatenated with it. The final concatenated string is what the local/directive scope property gets. (You can not do this with =, only @.)
With @, you will need to use attr.$observe("title", function(value) { ... }) if you need to use the value in your link(ing) function. E.g., if(scope.title == "...") will not work like you expect. Note that this means you can only access this attribute asynchronously. You do nott need to use $observe() if you are only using the value in a template. E.g., template: "<div>{{title}}</div>".
With =, you don not need to use $observe.
* Can I also access the parent scope directly, without decorating my element with an attribute?
Yes, but only if you do not use an isolate scope. Remove this line from your directive

scope: { ... }

and then your directive will not create a new scope. It will use the parent scope. You can then access all of the parent scope properties directly.
* The documentation says "Often it is desirable to pass data from the isolated scope via an expression and to the parent scope", but that seems to work fine with bidirectional binding too. Why would the expression route be better?
Yes, bidirectional binding allows the local/directive scope and the parent scope to share data. "Expression binding" allows the directive to call an expression (or function) defined by a DOM attribute -- and you can also pass data as arguments to the expression or function. So, if you do not need to share data with the parent -- you just want to call a function defined in the parent scope -- you can use the & syntax.', NULL, 5);
INSERT INTO answer VALUES (2, '2021-04-22 10:45:50', 70, 1, 'The simplest is to convert to a set then back to a list. One disadvantage with this is that it will not preserve the order. You may also want to consider if a set would be a better data structure to use in the first place, instead of a list.', 'answer2.png', 3);
INSERT INTO answer VALUES (3, '2021-07-21 13:22:15', 12, 2, 'f you would like to see more how this work with a live example. http://jsfiddle.net/juanmendez/k6chmnch/', 'answer3.png', 3);
INSERT INTO answer VALUES (4, '2021-07-21 17:01:15', 50, 4, 'In the simplest terms, git pull does a git fetch followed by a git merge.
You can do a git fetch at any time to update your remote-tracking branches under refs/remotes/<remote>/. This operation never changes any of your own local branches under refs/heads, and is safe to do without changing your working copy. I have even heard of people running git fetch periodically in a cron job in the background (although I would nott recommend doing this).
A git pull is what you would do to bring a local branch up-to-date with its remote version, while also updating your other remote-tracking branches.
From the Git documentation for git pull:
In its default mode, git pull is shorthand for git fetch followed by git merge FETCH_HEAD.', NULL, 5);
INSERT INTO answer VALUES (5, '2021-08-28 15:00:01', 47, 3, 'It is important to contrast the design philosophy of git with the philosophy of a more traditional source control tool like SVN.
Subversion was designed and built with a client/server model. There is a single repository that is the server, and several clients can fetch code from the server, work on it, then commit it back to the server. The assumption is that the client can always contact the server when it needs to perform an operation.
Git was designed to support a more distributed model with no need for a central repository (though you can certainly use one if you like). Also git was designed so that the client and the "server" do not need to be online at the same time. Git was designed so that people on an unreliable link could exchange code via email, even. It is possible to work completely disconnected and burn a CD to exchange code via git.
In order to support this model git maintains a local repository with your code and also an additional local repository that mirrors the state of the remote repository. By keeping a copy of the remote repository locally, git can figure out the changes needed even when the remote repository is not reachable. Later when you need to send the changes to someone else, git can transfer them as a set of changes from a point in time known to the remote repository.
* git fetch is the command that says "bring my local copy of the remote repository up to date."
* git pull says "bring the changes in the remote repository to where I keep my own code."
Normally git pull does this by doing a git fetch to bring the local copy of the remote repository up to date, and then merging the changes into your own code repository and possibly your working copy.
The take away is to keep in mind that there are often at least three copies of a project on your workstation. One copy is your own repository with your own commit history. The second copy is your working copy where you are editing and building. The third copy is your local "cached" copy of a remote repository.', NULL, 2);
INSERT INTO answer VALUES (6, '2021-04-20 08:29:00', -103, 1, 'Just read the documentation!', NULL, 1);
INSERT INTO answer VALUES (7, '2021-11-02 17:37:40', 70, 5, 'Here:', 'answer7.png', 1);
INSERT INTO answer VALUES (8, '2021-12-03 17:50:02', 66, 6, 'As what has already been mentioned by others, what behind the mystery is Branch Predictor.
I am not trying to add something but explaining the concept in another way. There is a concise introduction on the wiki which contains text and diagram. I do like the explanation below which uses a diagram to elaborate the Branch Predictor intuitively.', 'answer8.png', 3);
INSERT INTO answer VALUES (9, '2021-12-06 19:41:00', 33, 7, 'Any time you keep references around to objects that you no longer need you have a memory leak. See Handling memory leaks in Java programs for examples of how memory leaks manifest themselves in Java and what you can do about it.', NULL, 4);
INSERT INTO answer VALUES (10, '2021-11-14 22:08:56', 5, 4, 'A metaclass is the class of a class. A class defines how an instance of the class (i.e. an object) behaves while a metaclass defines how a class behaves. A class is an instance of a metaclass.
While in Python you can use arbitrary callables for metaclasses (like Jerub shows), the better approach is to make it an actual class itself. type is the usual metaclass in Python. type is itself a class, and it is its own type. You will not be able to recreate something like type purely in Python, but Python cheats a little. To create your own metaclass in Python you really just want to subclass type.
A metaclass is most commonly used as a class-factory. When you create an object by calling the class, Python creates a new class (when it executes the "class" statement) by calling the metaclass. Combined with the normal __init__ and __new__ methods, metaclasses therefore allow you to do "extra things" when creating a class, like registering the new class with some registry or replace the class with something else entirely.
When the class statement is executed, Python first executes the body of the class statement as a normal block of code. The resulting namespace (a dict) holds the attributes of the class-to-be. The metaclass is determined by looking at the baseclasses of the class-to-be (metaclasses are inherited), at the __metaclass__ attribute of the class-to-be (if any) or the __metaclass__ global variable. The metaclass is then called with the name, bases and attributes of the class to instantiate it.
However, metaclasses actually define the type of a class, not just a factory for it, so you can do much more with them. You can, for instance, define normal methods on the metaclass. These metaclass-methods are like classmethods in that they can be called on the class without an instance, but they are also not like classmethods in that they cannot be called on an instance of the class. type.__subclasses__() is an example of a method on the type metaclass. You can also define the normal "magic" methods, like __add__, __iter__ and __getattr__, to implement or change how the class behaves.
Here is an aggregated example of the bits and pieces:', 'answer10.png', 2);

SELECT pg_catalog.setval('answer_id_seq', 10, true);


INSERT INTO comment VALUES (1, NULL, 2, 'i am wrong or with python3k the values will be preserved, cause set now are sorted?', '2021-04-30 17:13:59', 1,4);
INSERT INTO comment VALUES (2, NULL, 6, 'Really useful! If I need another source, I also could find it in Internet. The best advice ever!', '2021-04-20 17:43:10', 0, 3);
INSERT INTO comment VALUES (3, NULL, 1, 'Writing "@" or "=" is so much clearer then writing "eval-dom" or "parent-scope" or any other human-readable text. Good design decision.', '2021-06-30 22:03:21', 3, 2);
INSERT INTO comment VALUES (4, 2, NULL, 'Huh, this is a really weird behavior, especially when not using interpolation and just trying to pass a string. Apparently the pull request has indeed been merged into the development builds and is in 1.1.5 and 1.2.0 RC builds. Good on them for fixing this very unintuitive behavior!', '2021-06-19 05:12:34', 0, 4);
INSERT INTO comment VALUES (5, NULL, 4, '"A "git pull" is what you would do to bring your repository up to date" <- is not the repository update already done by fetch? do not you mean it brings your local branches up-to-date with the remote branches? To the merge: It merges the remote branches with your local copies of those branches, or what exactly does it merge here?', '2021-07-22 10:08:00', 2, 2);
INSERT INTO comment VALUES (6, NULL, 7, 'I have a problem with the whole concept: those are visual representations of union, intersect, except, etc. They have no visual representation of projection therefore cannot be joins. I think it will confuse more than benefit when the context is joins.', '2021-11-03 12:06:31', 2, 4);
INSERT INTO comment VALUES (7, 8, NULL, 'More details please ', '2021-11-29 10:22:00', 0, 5);
INSERT INTO comment VALUES (8, 8, NULL, 'Will somebody delete it??', '2021-11-30 20:01:18', 0, 4);

SELECT pg_catalog.setval('comment_id_seq', 8, true);


INSERT INTO tag VALUES (1, 'python');
INSERT INTO tag VALUES (2, 'sql');
INSERT INTO tag VALUES (3, 'C ++');
INSERT INTO tag VALUES (4, 'java');
INSERT INTO tag VALUES (5, 'html');
INSERT INTO tag VALUES (6, 'git');

SELECT pg_catalog.setval('tag_id_seq', 5, true);

INSERT INTO question_tag VALUES (1, 1);
INSERT INTO question_tag VALUES (2, 5);
INSERT INTO question_tag VALUES (3, 6);
INSERT INTO question_tag VALUES (4, 1);
INSERT INTO question_tag VALUES (5, 2);
INSERT INTO question_tag VALUES (6, 3);
INSERT INTO question_tag VALUES (7, 4);
