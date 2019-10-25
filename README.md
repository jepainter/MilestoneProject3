# Milestone Project 3: Ultimate Book Review Website

The deployed website can be accessed from here (Heroku): [Ultimate Book Review](https://ultimate-book-review.herokuapp.com/)

## Temporary note for the assessor (this section will be removed in future):

- The website has various user types that have different priviledges in terms of actions they can take.  For testing of the super user / administrative account please use the following log in information:
    - Email: ubradmin@yahoo.com
    - Password: qazwsxedc1234
- The information above is made available to the assessor to demonstrate the full functionality of the site, and will be changed once the assessment has been completed.
- Other account types (regular user) can be assessed by registering a new account.
- Visitor accounts need no registrations, and will demonstrate limited functionality of the site in line with previleges.

## Goal of the website

The website created is a responsive and interactive book review website (strongly relying on reading community contributions) giving the user the opportunity to view book reviews, create, update and delete their own book reviews, as well as provide comments and votes on books on the site. 

The website in addition also allows the site owner to manage book categories (create, update, delete), users (delete only), comments (create, edit (own) and delete (all)) and reviews (create, edit (own) and delete (all)).

Users are also afforded the opportunity to be directed to a third party website with the option to purchase the book, there by simulating the generation of income through referrals by the site owner to the third party.

### Project Purpose:
The project purpose is to demonstrate accessing, manipulating (through CRUD operations) and displaying data retrieved from a NoSQL database.
The website utilises a MongoDB database together with Python code to access and manipulate the data.  Visualisation is done with HTML, CSS and JavaScript where required, utilizing the Flask framework.

## Limitations:

- Screening for controversial content is not caterred for, however site owner has access to delete any content, regardless of contributor.
- User authentication may not be in line with best practises as it was not a requirement for this project, however some efforts have been made to determine type of user, session status etc.  Simple user authentication was required to manage content/options delivered to the user type(i.e. logged in vs not logged in, regular user vs super user).

## UX

This website provides the relevant functionality to satisfy the requirements, in detail (guided by user stories/requirements):
- Provide the opportunity to view books (read only) without having to register with or login to the site.
- Provide the opportunity to follow link to third party site to purchase a book.
- Provide the opportunity to register for or login to the site, in order to manage (create, update, delete for users, books, comments and reviews).
- Provide the opportunity for the site owner to create, update and delete categories as needed for the site.

### User Stories:
- As a new reader, I want to view reviews of books, with the option to purchase a copy of a book I'm interested in.
- As a member of the site, I want to be able to add books and reviews to the site to expand the catalogue.
- As a member of the site, I want to be able to edit or delete reviews that I have contributed to the catalogue.
- As a user of the site, I want to be able to upvote or downvote books I have seen, and provide comments to the review.
- As a member of the site, I want to be able to update my details, or delete my account, removing my contributions to the site.
- As the site owner, I want to be able to create, edit or delete categories of books on the site.
- As the site owner, I want to be able to manage comments, deleting them if necessary (if content not suitable).
- As the site owner, I want to generate referral income by linking to a third party site for site members to purchase books.

### Wireframes:
Wireframes for the initial development of the site and database structure can be found here:
- [Mobile](https://github.com/jepainter/MilestoneProject3/blob/master/development/Milestone%20Project%203%20-%20Mobile%20Design.pdf)
- [Desktop](https://github.com/jepainter/MilestoneProject3/blob/master/development/Milestone%20Project%203%20-%20Tablet%20and%20Desktop%20Design.pdf)
- [Database](https://github.com/jepainter/MilestoneProject3/blob/master/development/Milestone%20Project%203%20-%20Database%20Design.pdf)

### Design considerations:
It was decided to style the website with a elegant and cosy feel:
- Complementing yet contrasting colours.
- Multi page layout, with visibility of certain pages only available to logged in users (add book, edit book, delete book, etc.).
- Simple and logical navigation.
- Intuitive user input requirements for quick and easy information capturing.
- Feedback regarding success of input to keep user informed of progress/changes.

The design utilises the Bootstrap grid system, containers and components responsive to different screen sizes and devices, styled with the Bootswatch Lux theme. 

This site is limited to the use of HMTL, CSS, JavaScript, Flask, Python and MongoDB. 

## Features

### Existing Features
- Feature 1 - Navigation: Simple navigation of the site that jumps to the selected section on the site (at top of each page).
- Feature 2 - Books: Ability to view books in catalogue, and select a specific book for detailed info (review, comments, etc)
- Feature 3 - Add Book: Ability to add a book to the catalogue if user logged in.
- Feature 4 - Edit Book: Ability to edit the book details, if user is same contributor or super user.
- Feature 5 - Delete Book: Ability to delete a book, if the user is the same contributor or a super user (a measure to rectify inappropriate content).
- Feature 6 - Buy Book: Ability to follow a link to an external third party site to purchase said book (this is for demonstration of referral option only).
- Feature 7 - Add Review: Ability to add review for a specific book, if logged into the site.
- Feature 8 - Edit Review: Ability to edit a review for a specific book, if the user is the same contributor.
- Feature 9 - Delete Review: Ability to delete a review for a specific book, if the user is the same contributor or a super user (a measure to rectify inappropriate content).
- Feature 10 - Add Comment: Ability to add comment for a specific book, if logged into the site.
- Feature 11 - Edit Comment: Ability to edit a comment for a specific book, if the user is the same contributor.
- Feature 12 - Delete Comment: Ability to delete a comment for a specific book, if the user is the same contributor or a super user (a measure to rectify inappropriate content).
- Feature 13 - Categories: Ability to view categories of books and tailor search according to category.
- Feature 14 - Add Category: Ability to add a category to the site to expand catalogue (super user only).
- Feature 15 - Edit Category: Ability to update category info (super user only).
- Feature 16 - Delete Category: Ability to delete a category from the site (super user only).
- Feature 17 - Register User: Ability to register as a new user for increased functionality (only if logged in).
- Feature 18 - Log In: Ability to log in as user, for increased functionality.
- Feature 19 - Profile/User Management:  Ability to manage/update/delete own profile (regular user and super user) or delete any accounts (super user only).
- Feature 20 - Social Media: Links to social media platforms.

### Features Left to Implement
- Feature A - Avatar images for users.
- Feature B - Newsletter sign up to stay informed of new additions, improved functionality.
- Feature C - Pagination for greater result numbers to be implemented.
- Feature D - Forget password / log on details functionality.
- Feature E - Possibility to upload images and store in repository, rather than hotlinking to images.

## Technologies Used

The following languages, frameworks, libraries, IDE, repositories and tools were used for the creation of this website:

- [HTML](https://en.wikipedia.org/wiki/HTML)
    - This project utilises the **HTML** language and sematic elements for basic layout and function.   

- [CSS](https://en.wikipedia.org/wiki/Cascading_Style_Sheets)
    - This project is styled using **CSS** where required for classes and specific elements. 

- [Bootstrap](https://getbootstrap.com/)
    - This project utilizes the **Bootstrap** grid system and components (incorporated through the Bootstrap CDN), to create the layout and responsive design of the page.

- [Bootwatch](https://bootswatch.com/lux/)
    - This project relies on the Bootswatch Lux theme for styling of the site and Bootstrap grid system and components.

- [FontAwesome](https://fontawesome.com/)
    - This project utilises **FontAwesome CDN** for icons utilised on the website. 

- [jQuery](https://jquery.com/)
    - This project utilises **jQuery** for the responsive navbar.

- [Popper.js](https://popper.js.org/)
    - The project uses **Popper.js**  for the responsive navbar.

- [AWS Cloud9](https://www.awseducate.com)
    - This project was created using **AWS Cloud9** IDE for development, as well as committing of progress to GitHub and Heroku. 

- [Heroku](https://www.heroku.com/)
    - This project uses **Heroku** for hosting and running of the application.

- [GitHub](https://github.com)
    - This project uses **GitHub** for hosting of project repository. 

- [FreeLogoDesign](https://www.freelogodesign.org/)
    - Used **FreeLogoDesign.org** to generate a logos for the site.

- [Favicon](https://www.favicon-generator.org/)
    - Used **Favicon-generator.org** to generate at favicon for the site from a logo designed.

- [W3C CSS Validation Service](https://jigsaw.w3.org/css-validator/)
    - This project was tested using the **W3C CSS Validation Service** for checking conformity and validity of css content. 

- [Autoprefixer CSS Online](https://autoprefixer.github.io/)
    - Used **Autoprefixer CSS Online** tool to update/confirm prefixes for style.css code.

- [AutoPEP8](https://pypi.org/project/autopep8/)
    - Used **AutoPep8** to auto format Python code to conform to PEP8 standards.  Some deviation have been allowed for sake of readibility.

## Testing

Testing for this site was performed as follows:

### Code Validation:
The index.html file was not passed through the W3C HTML Validation site, due to the use of the Flask Framwork, many errors and warnings raised.
The style.css file was tested using the W3C CSS Validation site, with no errors reported.
The style.css file was run through the Autoprefixer CSS Online tool.

The site was tested on Google Chrome (desktop and mobile through dev tools), Opera (desktop only), Edge (desktop only) and Safari (mobile only iPhone6) for functionality.  Verified working well.

This site was also tested manually in line with the user stories and general functionality.  Testing is detailed in the testing matrix - [Testing Matrix](https://github.com/jepainter/MilestoneProject3/blob/master/testing/Milestone%20Project%203%20-%20Testing%20Matrix.pdf).

## Deployment

This project is deployed on Heroku and GitHub and is accessible as follows:
- Website: [Heroku](https://ultimate-book-review.herokuapp.com/)
- Repository: [GitHub](https://github.com/jepainter/MilestoneProject3)

For this project I used the AWS Cloud9 IDE platform [AWS Cloud9](https://www.awseducate.com) via the AWS Educate portal.
The platform allowed me to commit my pages (and changes) to Git, following which it was pushed through to the [GitHub repository](https://github.com/jepainter/MilestoneProject3).

Deployment of the website from to Heroku can accomplished through the following method: 
1. Log into the Heroku website. 
2. Install the Heroku CLI in the IDE terminal.
3. Log into Heroku from the IDE terminal using $ heroku login.
4. Clone the repository by typing ```heroku git:clone -a ultimate-book-review``` and then ```cd ultimate-book-review``` into your IDE terminal.
5. Changes and updates to code can be made in the IDE.
6. To deploy changes to Heroku type ```git add <your filename>```, followed by ```git commit -m "messaage regarding changes"``` and lastly ```git push heroku master``` into the IDE terminal.

This website can also be locally deployed by following the method outlined below:
1. Use the following link to access the project repository: [GitHub](https://github.com/jepainter/MilestoneProject3).
2. Click on the **Clone or Download** button, under the repository name.
3. Copy the clone URL for the repository, found in the **Clone with HTTPS** section. 
4. Open **Git Bash** in your local IDE environment.
5. Select the location to where the cloned directory must be made.
6. Input ```git clone``` together with the copied clone URL into Git Bash and press Enter.

The deployed version on **Heroku** is the same as the development version.

## Credits

### Content
- Book cover links have been obtained from Amazon's website, and used purely for educational purposes.
- Book details have been obtained from Amazon's website and used purely for educational purposes.
- Images links for categories have been sources from Google searches.
- Wallpaper background obtained from [Pixabay](https://pixabay.com/) and is used purely for educational purposes.
- Reviews have been sourced from [GoodReads's](https://www.goodreads.com/) website and is used purely for educational purposes.

### Code
- All efforts have been made to document code that has been adapted by means of comments in the relevant project files.
- Specifically the use of WTForms was made possible through the [WTForms documentation](https://wtforms.readthedocs.io/en/stable/index.htm) as well as [Codey Schafer's tutorial](https://www.youtube.com/watch?v=UIJKdCIEXUQ&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=3)
- User session management was adapted from the code tutorial from [Pretty Printed](https://www.youtube.com/watch?v=eBwhBrNbrNI).
- Code for the management of unavailable image links with replacement image was adapted from [ImageKit](https://blog.imagekit.io/how-to-handle-loading-images-that-may-not-exist-on-your-website-92e6c3c6ea63).
- Code for redirecting to a secure proxy (https) was obtained from the [Flask API Documentation](https://flask.palletsprojects.com/en/1.1.x/api/?highlight=url_for#flask.url_for).

### Acknowledgements
- I would like to thank my mentor, Dick Vlaanderen, for input provided during the development of the site.
