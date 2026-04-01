CREATE DATABASE IF NOT EXISTS job_tracker;
USE job_tracker;

CREATE TABLE IF NOT EXISTS companies (
    company_id INT PRIMARY KEY AUTO_INCREMENT,
    company_name VARCHAR(100) NOT NULL,
    industry VARCHAR(50),
    website VARCHAR(200),
    city VARCHAR(50),
    state VARCHAR(50),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS jobs (
    job_id INT PRIMARY KEY AUTO_INCREMENT,
    company_id INT,
    job_title VARCHAR(100) NOT NULL,
    job_type ENUM('Full-time','Part-time','Contract','Internship'),
    salary_min INT,
    salary_max INT,
    job_url VARCHAR(300),
    date_posted DATE,
    requirements JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS applications (
    application_id INT PRIMARY KEY AUTO_INCREMENT,
    job_id INT,
    application_date DATE NOT NULL,
    status ENUM('Applied','Screening','Interview','Offer','Rejected','Withdrawn') DEFAULT 'Applied',
    resume_version VARCHAR(50),
    cover_letter_sent BOOLEAN DEFAULT FALSE,
    interview_data JSON,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (job_id) REFERENCES jobs(job_id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS contacts (
    contact_id INT PRIMARY KEY AUTO_INCREMENT,
    company_id INT,
    contact_name VARCHAR(100) NOT NULL,
    title VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),
    linkedin_url VARCHAR(200),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE SET NULL
);
