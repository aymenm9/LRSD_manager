


-- creat data base
-- @block
-- Create the admin table

CREATE TABLE IF NOT EXISTS admin (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    password_hash VARCHAR(255) NOT NULL
);

-- Create the departments table
CREATE TABLE IF NOT EXISTS departments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL
);

-- Create the teachers table
CREATE TABLE IF NOT EXISTS teachers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50) ,
    last_name VARCHAR(50) ,
    email VARCHAR(255),
    mark FLOAT ,
    grade VARCHAR(255) ,
    department_id INT DEFAULT NULL,
    INDEX idx_username (username),
    INDEX idx_department_id (department_id),
    FOREIGN KEY (department_id) REFERENCES departments(id)
);

-- Create the polycopies table
CREATE TABLE IF NOT EXISTS  polycopes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    pages INT NOT NULL,
    type ENUM('td', 'tp', 'cour') NOT NULL,
    date DATE NOT NULL,
    teacher_id INT NOT NULL,
    INDEX idx_teacher_id (teacher_id),
    FOREIGN KEY (teacher_id) REFERENCES teachers(id)
);

-- Create the online_courses table
CREATE TABLE IF NOT EXISTS online_courses (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    url VARCHAR(255) NOT NULL,
    date DATE NOT NULL,
    teacher_id INT NOT NULL,
    INDEX idx_teacher_id (teacher_id),
    FOREIGN KEY (teacher_id) REFERENCES teachers(id)
);

-- Create the supervision_l3 table
CREATE TABLE IF NOT EXISTS supervision_l3 (
    id INT PRIMARY KEY AUTO_INCREMENT,
    teacher_id INT NOT NULL,
    subject VARCHAR(255) NOT NULL,
    binome_1 VARCHAR(255) NOT NULL,
    binome_2 VARCHAR(255),
    INDEX idx_teacher_id (teacher_id),
    FOREIGN KEY (teacher_id) REFERENCES teachers(id)
);

-- Create the supervision_master table
CREATE TABLE IF NOT EXISTS supervision_master (
    id INT PRIMARY KEY AUTO_INCREMENT,
    teacher_id INT NOT NULL,
    subject VARCHAR(255) NOT NULL,
    binome_1 VARCHAR(255) NOT NULL,
    binome_2 VARCHAR(255),
    graduation_date DATE NOT NULL,
    INDEX idx_teacher_id (teacher_id),
    FOREIGN KEY (teacher_id) REFERENCES teachers(id)
);

-- Create the conferences table
CREATE TABLE IF NOT EXISTS conferences (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    place VARCHAR(255) NOT NULL,
    date DATE NOT NULL,
    teacher_id INT NOT NULL,
    INDEX idx_teacher_id (teacher_id),
    FOREIGN KEY (teacher_id) REFERENCES teachers(id)
);

--@block
-- Create the conference_assistants table
CREATE TABLE IF NOT EXISTS conference_assistants (
    id INT PRIMARY KEY AUTO_INCREMENT,
    conference_id INT NOT NULL,
    assistant_name VARCHAR(255) NOT NULL,
    INDEX idx_conference_id (conference_id),
    FOREIGN KEY (conference_id) REFERENCES conferences(id)
);

--@block
DROP TABLE conference_assistants;

-- conference assistants alert
--@block
ALTER TABLE conference_assistants
    ADD COLUMN id INT PRIMARY KEY AUTO_INCREMENT;

-- Create the intervention table
CREATE TABLE IF NOT EXISTS intervention (
    conference_id INT NOT NULL,
    intervention VARCHAR(255),
    INDEX idx_conference_id (conference_id),
    FOREIGN KEY (conference_id) REFERENCES conferences(id)
);

-- conference intervention alert
--@block
ALTER TABLE intervention
    ADD COLUMN id INT PRIMARY KEY AUTO_INCREMENT;

-- Create the articles table
CREATE TABLE IF NOT EXISTS articles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    date DATE NOT NULL,
    teacher_id INT NOT NULL,
    pages INT,
    journal VARCHAR(255),
    INDEX idx_teacher_id (teacher_id),
    FOREIGN KEY (teacher_id) REFERENCES teachers(id)
);

-- Create the coauthor table
CREATE TABLE IF NOT EXISTS coauthor (
    article_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    INDEX idx_article_id (article_id),
    FOREIGN KEY (article_id) REFERENCES articles(id)
);
-- coauthor alert
--@block
ALTER TABLE coauthor
    ADD COLUMN id INT PRIMARY KEY AUTO_INCREMENT;


-- UPDATE teachers
 --@block
ALTER TABLE teachers
    DROP COLUMN first_name,
    DROP COLUMN last_name,
    DROP COLUMN mark,
    DROP COLUMN grade,
    ADD COLUMN IF NOT EXISTS first_name VARCHAR(50),
    ADD COLUMN IF NOT EXISTS last_name VARCHAR(50),
    ADD COLUMN IF NOT EXISTS mark FLOAT,
    ADD COLUMN IF NOT EXISTS grade VARCHAR(50);







--@block
CREATE TABLE IF NOT EXISTS grade(grade VARCHAR(50));

--@block
ALTER TABLE teachers 
    ADD COLUMN IF NOT EXISTS img BLOB;

--@block
SELECT * FROM polycopes;

--@block
SELECT * FROM online_courses;
--@block
SELECT * FROM supervision_l3;
--@block
SELECT * FROM supervision_master;
--@block
SELECT * FROM conferences JOIN conference_assistants ON conference_assistants.conference_id = conferences.id ;
--@block
SELECT * FROM articles;
--@block
SELECT * FROM polycopes;
SELECT * FROM online_courses;
SELECT * FROM supervision_l3;
SELECT * FROM supervision_master;
SELECT * FROM conferences;
SELECT * FROM articles;