import mysql.connector

#Configuration

DB_CONFIG = {
    'host':     'localhost',
    'user':     'appuser',
    'password': 'password123', 
    'database': 'job_tracker',
}

#Connection

def get_db():
    """Return a new MySQL connection."""
    return mysql.connector.connect(**DB_CONFIG)

#General query helper

def query(sql, params=None, fetchone=False, commit=False):
    """
    Execute a SQL statement and return results.

    Args:
        sql      : SQL string (use %s placeholders)
        params   : tuple of values to bind
        fetchone : if True, return a single row dict instead of a list
        commit   : if True, commit the transaction and return lastrowid

    Returns:
        list of dicts | single dict | lastrowid int
    """
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, params or ())
    if commit:
        conn.commit()
        result = cursor.lastrowid
    elif fetchone:
        result = cursor.fetchone()
    else:
        result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

#Company queries

def get_all_companies():
    return query("""
        SELECT c.*, COUNT(DISTINCT j.job_id) as job_count,
               COUNT(DISTINCT co.contact_id) as contact_count
        FROM companies c
        LEFT JOIN jobs j ON c.company_id = j.company_id
        LEFT JOIN contacts co ON c.company_id = co.company_id
        GROUP BY c.company_id
        ORDER BY c.company_name
    """)

def get_company(company_id):
    return query('SELECT * FROM companies WHERE company_id=%s', (company_id,), fetchone=True)

def create_company(name, industry, website, city, state, notes):
    return query(
        'INSERT INTO companies (company_name,industry,website,city,state,notes) VALUES (%s,%s,%s,%s,%s,%s)',
        (name, industry, website, city, state, notes), commit=True
    )

def update_company(company_id, name, industry, website, city, state, notes):
    return query(
        'UPDATE companies SET company_name=%s,industry=%s,website=%s,city=%s,state=%s,notes=%s WHERE company_id=%s',
        (name, industry, website, city, state, notes, company_id), commit=True
    )

def delete_company(company_id):
    # had to add to remove linked contacts and jobs (and their applications) first as it was giving me an error
    query('DELETE FROM contacts WHERE company_id=%s', (company_id,), commit=True)
    for job in query('SELECT job_id FROM jobs WHERE company_id=%s', (company_id,)):
        query('DELETE FROM applications WHERE job_id=%s', (job['job_id'],), commit=True)
    query('DELETE FROM jobs WHERE company_id=%s', (company_id,), commit=True)
    return query('DELETE FROM companies WHERE company_id=%s', (company_id,), commit=True)

#Job Queries

def get_all_jobs():
    return query("""
        SELECT j.*, c.company_name, COUNT(a.application_id) as app_count
        FROM jobs j
        LEFT JOIN companies c ON j.company_id = c.company_id
        LEFT JOIN applications a ON j.job_id = a.job_id
        GROUP BY j.job_id
        ORDER BY j.created_at DESC
    """)

def get_job(job_id):
    return query('SELECT * FROM jobs WHERE job_id=%s', (job_id,), fetchone=True)

def create_job(company_id, title, job_type, sal_min, sal_max, url, date_posted, requirements_json):
    return query(
        'INSERT INTO jobs (company_id,job_title,job_type,salary_min,salary_max,job_url,date_posted,requirements) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',
        (company_id, title, job_type, sal_min, sal_max, url, date_posted, requirements_json), commit=True
    )

def update_job(job_id, company_id, title, job_type, sal_min, sal_max, url, date_posted, requirements_json):
    return query(
        'UPDATE jobs SET company_id=%s,job_title=%s,job_type=%s,salary_min=%s,salary_max=%s,job_url=%s,date_posted=%s,requirements=%s WHERE job_id=%s',
        (company_id, title, job_type, sal_min, sal_max, url, date_posted, requirements_json, job_id), commit=True
    )

def delete_job(job_id):
    # added to remove linked applications first to avoid FK lock timeout as it was giving me an error
    query('DELETE FROM applications WHERE job_id=%s', (job_id,), commit=True)
    return query('DELETE FROM jobs WHERE job_id=%s', (job_id,), commit=True)

#Application Queries

def get_all_applications():
    return query("""
        SELECT a.*, j.job_title, c.company_name
        FROM applications a
        LEFT JOIN jobs j ON a.job_id = j.job_id
        LEFT JOIN companies c ON j.company_id = c.company_id
        ORDER BY a.application_date DESC
    """)

def get_application(application_id):
    return query('SELECT * FROM applications WHERE application_id=%s', (application_id,), fetchone=True)

def create_application(job_id, app_date, status, resume_ver, cover_letter, interview_json, notes):
    return query(
        'INSERT INTO applications (job_id,application_date,status,resume_version,cover_letter_sent,interview_data,notes) VALUES (%s,%s,%s,%s,%s,%s,%s)',
        (job_id, app_date, status, resume_ver, cover_letter, interview_json, notes), commit=True
    )

def update_application(application_id, job_id, app_date, status, resume_ver, cover_letter, interview_json, notes):
    return query(
        'UPDATE applications SET job_id=%s,application_date=%s,status=%s,resume_version=%s,cover_letter_sent=%s,interview_data=%s,notes=%s WHERE application_id=%s',
        (job_id, app_date, status, resume_ver, cover_letter, interview_json, notes, application_id), commit=True
    )

def delete_application(application_id):
    return query('DELETE FROM applications WHERE application_id=%s', (application_id,), commit=True)

#Contact Queries

def get_all_contacts():
    return query("""
        SELECT co.*, c.company_name
        FROM contacts co
        LEFT JOIN companies c ON co.company_id = c.company_id
        ORDER BY co.contact_name
    """)

def get_contact(contact_id):
    return query('SELECT * FROM contacts WHERE contact_id=%s', (contact_id,), fetchone=True)

def create_contact(company_id, name, title, email, phone, linkedin, notes):
    return query(
        'INSERT INTO contacts (company_id,contact_name,title,email,phone,linkedin_url,notes) VALUES (%s,%s,%s,%s,%s,%s,%s)',
        (company_id, name, title, email, phone, linkedin, notes), commit=True
    )

def update_contact(contact_id, company_id, name, title, email, phone, linkedin, notes):
    return query(
        'UPDATE contacts SET company_id=%s,contact_name=%s,title=%s,email=%s,phone=%s,linkedin_url=%s,notes=%s WHERE contact_id=%s',
        (company_id, name, title, email, phone, linkedin, notes, contact_id), commit=True
    )

def delete_contact(contact_id):
    return query('DELETE FROM contacts WHERE contact_id=%s', (contact_id,), commit=True)

#Dashboard Queries

def get_dashboard_stats():
    return {
        'total_applications': query('SELECT COUNT(*) as c FROM applications', fetchone=True)['c'],
        'total_companies':    query('SELECT COUNT(*) as c FROM companies', fetchone=True)['c'],
        'total_jobs':         query('SELECT COUNT(*) as c FROM jobs', fetchone=True)['c'],
        'total_contacts':     query('SELECT COUNT(*) as c FROM contacts', fetchone=True)['c'],
        'offers':             query("SELECT COUNT(*) as c FROM applications WHERE status='Offer'", fetchone=True)['c'],
        'interviews':         query("SELECT COUNT(*) as c FROM applications WHERE status='Interview'", fetchone=True)['c'],
    }

def get_status_counts():
    return query('SELECT status, COUNT(*) as count FROM applications GROUP BY status')

def get_recent_applications(limit=5):
    return query("""
        SELECT a.application_id, a.application_date, a.status,
               j.job_title, c.company_name
        FROM applications a
        LEFT JOIN jobs j ON a.job_id = j.job_id
        LEFT JOIN companies c ON j.company_id = c.company_id
        ORDER BY a.application_date DESC LIMIT %s
    """, (limit,))

#Job Match Query

def get_jobs_with_requirements():
    """Return all jobs that have non-empty requirements JSON."""
    return query("""
        SELECT j.job_id, j.job_title, j.job_type, j.salary_min, j.salary_max,
               j.requirements, c.company_name
        FROM jobs j
        LEFT JOIN companies c ON j.company_id = c.company_id
        WHERE j.requirements IS NOT NULL AND j.requirements != '[]'
    """)

#Dropdown Helpers

def get_companies_list():
    return query('SELECT company_id, company_name FROM companies ORDER BY company_name')

def get_jobs_list():
    return query("""
        SELECT j.job_id, j.job_title, c.company_name
        FROM jobs j LEFT JOIN companies c ON j.company_id=c.company_id
        ORDER BY c.company_name, j.job_title
    """)
