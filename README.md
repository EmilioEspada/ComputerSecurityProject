CS-492-02 Spring 2024 Computer Security Course Project

Emilio Espada and William Horton
Professor Zabihimayvan

Project Survey

Introduction to the Project
  The primary goal of the project is to create a website with a login system. Each user will
have a notes feature on their accounts. Each user will be able to create a note to store text, which
can be stored as a card for their account. Each card will be stored on the account which will
display every time a user logs into their account. A card can be sent to another user using their
username, and the text will be hashed using Tiger Hash, while also being encrypted signed with
the user’s private key. This file will be sent to the other user, and the other user can choose to
accept it or not. If they accept, they can view the card after using the other user’s public key,
decrypting the message.
  There will be 4 topics which will be relevant to the project, encryption and decryption,
tiger hash, authentication, and public key cryptography. Encryption and decryption are relevant
to the encryption and decryption of the authentication system for user accounts, tiger hash, as
well as public key cryptography. Tiger hash will be relevant to hashing the messages of the
notes. Public key cryptography will be relevant to the digital signatures that will be sent with the
notes. Authentication will be relevant to the login system which will be done using Django.

Background and Literature Review
  The relevant research to the project focuses on Tiger Hash, Encryption and Decryption,
modern authentication systems, and public key cryptography. Each will be summarized.
  Tiger hash is a hash function in which processes 512 bit blocks and produces a 192 bit
hash value [1]. It is an iterative hash function in which consists of two parts: the key schedule,
and state update transformation. During the state update transformation, the Tiger Hash starts
from an initial value of “IV of three 64-bit words and updates them in three passes of eight
rounds each” [1]. During each round, three state variables are processed through multiple
functions and shifted with one another during each transformation/round. At the last round, the
initial values and the output values from the last round are combined resulting in a final hash
value for the next block. The key schedule is “an invertible function that changes a small number
of bits in the messages which will affect a lot of bits in the next pass” [1]. The key schedule
modifies its inputs in two steps of computation, and afterwards the final values are the output and
the message words for the next pass.
  Encryption and decryption are a cryptography method in which a message is converted
into a cipher through some encryption algorithm, and can be decrypted from the cipher message,
back into the regular message using a decryption algorithm [2]. Multiple algorithms can be
combined to create more diverse and secure messages if wanted for a certain cryptographic
system. There are many different algorithms that are used for encrypting and decrypting.
  Authentication is a type of system that requires the need for the “verification of a user’s
identity” [3]. This type of system requires that a user’s information on a system must only be
intended for that user or a certain group, if they know the required information to access that
account information. There are many distinct types of authentication systems, some of which
require more than one step of verification from the user’s side to verify their identity, such as two
factor authentication. Usually, however, the primary gateway to an account is a username, and
password, both of which should only be known to the user, otherwise their information on their
account is not private and secure.
  Public key cryptography comes down to a public key and a private key, one for
encrypting or signing, and the other for decrypting or verifying. One of these keys can be made
public and the other is private. This makes it so that keys do not need to be sent over during
messages, and messages will be secure if the private key remains. This makes it so that “anyone
can encipher messages, but only the intended recipient can decipher messages” [4].

Methodology
  The project's methodology will be based on understanding of the Tiger Hash function,
documentation for creating the necessary website, and research around peer-to-peer file sharing
to share data across accounts.
  The primary tools that will be used for the project will be as follows
    1. PyCharm – An IDE which allows for the creation of websites through HTML, CSS, and
    JavaScript, as well as coding in Python
    2. Django – A python web-based framework which will be used for the creation of the
    website with generative html depending on the user’s account. Will also be used for user
    authentication for security and will be the place will the notes application will be coded
    with Tiger Hash.
    3. PythonAnywhere – A cloud deployment website in which our website will be available to
    the general public.
  The following steps will be the current course in which the project will be done.
    1. Create GitHub project – based on Django
    2. Create the user interface for login/account creation
    3. Create the basic notes application for creating/editing/deleting notes.
    4. Encrypt and decrypt the note messages using tiger hash.
    5. Utilize public key cryptography for the notes
    6. Cloud Deploy the website using Pythonanywhere.com

Expected Outcomes
  The outcome of the project will be a website built from Django in which will have a login
system, where a user can create an account and login using said account. Once logging into the
website, the user will be able to create notes, which have text stored inside them. The user can
edit, delete, or add new notes depending on their preferences. A user can send over a note in
which using another user’s username will be sent over to another user’s account. This note that is
sent over will be hashed using Tiger Hash, and the hash will be checked before sending the
message and after the other user receives it, to check for verification and data corruption. There
will also be a public key cryptographic system for the notes as well, where a user is required to
sign a message with their private key, and the other user on the other side must use a public key
to decrypt the message. User’s public keys will be viewable to others as they are supposed to be
public knowledge. The other user receiving the message must verify that they want to receive the
file. If they do, the note will be added to their account with the sent user’s username alongside it.

Timeline
3/4 Survey Submit
  - This will be when our survey will be due and marks the start of the project. However, we
need to wait for feedback to progress to the next step.
3/8 Final Project Proposal Finish
  - After feedback is received, we can start our final proposal that will be due by 3/18.
3/18 Final Project Proposal Submit
3/22 - Start working on the UI – Basic HTML/CSS
  - Right after spring break, the first step will be to get the basic UI done, and the overall
  design. While there might be basic functionality, most of this will be designing the
  website so that later features can be added modularly.
3/29 - Login System Complete During Meeting – Start Assigning Tasks for Notes Application
  - The basic login system is primarily an extension of the UI and can be easily done during
  a meeting. This is when we will start figuring out how to code in a Notes application and
  how the notes will be stored.
4/5 - Basic Note Application Finish – No Hashing or Public Key Crypto currently
  - The basic note application should be done by this time, and the next step will be to plan
  out how to integrate the notes system with hashing and public key cryptography.
4/12 - Tiger Hash Integration
  - Tiger hash must be integrated by this time, where the message will be hashed and sent to
  the other user, and verified with the website that there was no change to the message.
4/19 – Public Key Crypto Integration
  - Public key crypto must be done by this time, each user will have a public and private key.
  A user will use their private key to encrypt their message and sign it, and send it, which
  will then be decrypted by the other user using the sending user’s public key.
4/26 - Presentation Complete, Video Demo Done
  - Wrapping up, where most material should be completed.

Resources
The primary tools and software that will be used for the project will be as follows:
  - PyCharm – a IDE that can be used to create website applications using the coding
  languages HTML, CSS, JavaScript, and Django
  - Django – a python-based web framework in which helps with the generating of websites
  based on given information given a created template
  - PythonAnywhere – a cloud deployment system to deploy the website we will create to
  the public domain.
  - Computer – a required tool that is needed to utilize PyCharm software

Ethical Considerations and Guidelines
Ethical Considerations
  - Due to using a public website, information and accounts created on the website could
  potentially be hacked
  - Due to that a user can send messages to any other user if they have their username, a
  certain user might be able to send messages to another user, although the receiving user
  will still have to verify the messages sent before receiving them
Ethical Guidelines – from the ACM Code of Ethics Booklet [5]
  - 1.7 Honor Confidentiality
  o Our system will ensure that a user’s created notes will only be viewable by the
  user themselves and anyone who they have agreed to send their note to.
  - 2.6 Perform Work only in areas of competence
  o While implementing algorithms into our system, if we come across barriers
  beyond our skill to overcome, we will ask our instructor permission to change our
  implementation of our system to use a different algorithm that we are more
  familiar with.
  - 1.2 Avoid Harm
  o Our system will not be malicious and not spread malware to the users that use the
  system. The system will only be used for its intended purpose, which is to store
  notes for users and send notes to other users securely. Users will not be able to
  send notes maliciously to others as a verification system will be put in place to
  ensure that users do not spam other users.
  - 2.9 Design and implement systems that are robust and usably secure.
  o The systems that will be put in place will be secure and perform to the user’s
  expectations. If there are systems in which we are unsure of the security or the
  potential for unpredictable behavior, those systems will not be put in place, and a
  secure solution will be put in place instead.

Conclusion
  The basic premise of the project will be to integrate the following topics into a notes website:
encryption and decryption, authentication, tiger hash, and a public cryptography system. These
together will create a secure and private system in which each user will have access to their own
notes, and can send notes over to one another, as well as receive notes after verification. The
software will be written in the IDE PyCharm and written in the framework of Django. This will
then be posted on PythonAnywhere for cloud deployment. There are four ethical guidelines we
will consider when creating the project to ensure that our system is safe, secure, and performs to
the intended functionality that our user’s expect: Honor Confidentiality, Perform Work only in
areas of competence, Avoid Harm, and Design and implement systems that are robustly and
usably secure. Together, this makes up the basic gist that our project consists of, and the
expected goals which we hope to complete before the deadline.
  The project's overall impact will be to demonstrate the above topics of Computer Security
and display their usefulness in a system where we share information from one user to another.
This emphasizes the importance of these topics' role in security and their importance to the
overall general research they are a part of.
References

[1] F. Mendel and V. Rijmen, “Cryptanalysis of the Tiger Hash Function,” in Advances in
  Cryptology – ASIACRYPT 2007, vol. 4833, K. Kurosawa, Ed., in Lecture Notes in
  Computer Science, vol. 4833., Berlin, Heidelberg: Springer Berlin Heidelberg, 2007, pp.
  536–550. doi: 10.1007/978-3-540-76900-2_33.

[2] B. Kaushik, V. Malik, and V. Saroha, “A Review Paper on Data Encryption and Decryption,”
  IJRASET, vol. 11, no. 4, pp. 1986–1992, Apr. 2023, doi: 10.22214/ijraset.2023.50101.

[3] M. Papathanasaki, L. Maglaras, and N. Ayres, “Modern Authentication Methods: A
  Comprehensive Survey,” AI, Computer Science and Robotics Technology, Jun. 2022, doi:
  10.5772/acrt.08.

[4] D. Liestyowati, “Public Key Cryptography,” J. Phys.: Conf. Ser., vol. 1477, no. 5, p. 052062,
  Mar. 2020, doi: 10.1088/1742-6596/1477/5/052062.

[5] D. Gotterbarn et al., “ACM Code of Ethics and Professional Conduct”.
