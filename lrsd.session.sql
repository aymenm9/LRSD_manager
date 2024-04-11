


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

-- Create the conference_assistants table
CREATE TABLE IF NOT EXISTS conference_assistants (
    conference_id INT NOT NULL,
    assistant_name VARCHAR(255) NOT NULL,
    INDEX idx_conference_id (conference_id),
    FOREIGN KEY (conference_id) REFERENCES conferences(id)
);

-- Create the intervention table
CREATE TABLE IF NOT EXISTS intervention (
    conference_id INT NOT NULL,
    intervention VARCHAR(255),
    INDEX idx_conference_id (conference_id),
    FOREIGN KEY (conference_id) REFERENCES conferences(id)
);

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

-- UPDATE teachers
 --@block
ALTER TABLE teachers
    DROP COLUMN first_name,
    DROP COLUMN last_name,
    DROP COLUMN mark,
    DROP COLUMN grade,
    ADD COLUMN first_name VARCHAR(50),
    ADD COLUMN last_name VARCHAR(50),
    ADD COLUMN mark FLOAT,
    ADD COLUMN grade VARCHAR(50);

