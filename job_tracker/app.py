from flask import Flask, render_template, request, redirect, url_for, flash
import json
import database as db

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'


#Dashboard

@app.route('/')
def dashboard():
    return render_template('dashboard.html',
        stats=db.get_dashboard_stats(),
        status_counts=db.get_status_counts(),
        recent=db.get_recent_applications())

#Companies

@app.route('/companies')
def companies():
    return render_template('companies.html', companies=db.get_all_companies())

@app.route('/companies/new', methods=['POST'])
def company_new():
    db.create_company(
        request.form['company_name'], request.form.get('industry'),
        request.form.get('website'),  request.form.get('city'),
        request.form.get('state'),    request.form.get('notes'))
    flash('Company added!', 'success')
    return redirect(url_for('companies'))

@app.route('/companies/<int:id>/edit', methods=['GET', 'POST'])
def company_edit(id):
    if request.method == 'POST':
        db.update_company(id,
            request.form['company_name'], request.form.get('industry'),
            request.form.get('website'),  request.form.get('city'),
            request.form.get('state'),    request.form.get('notes'))
        flash('Company updated!', 'success')
        return redirect(url_for('companies'))
    return render_template('companies.html',
        companies=db.get_all_companies(),
        edit_company=db.get_company(id))

@app.route('/companies/<int:id>/delete', methods=['POST'])
def company_delete(id):
    db.delete_company(id)
    flash('Company deleted.', 'info')
    return redirect(url_for('companies'))

#Jobs

def parse_jobs(rows):
    for r in rows:
        reqs = r.get('requirements')
        try:
            if reqs is None:
                r['requirements'] = []
            elif isinstance(reqs, str):
                parsed = json.loads(reqs)
                r['requirements'] = list(parsed) if isinstance(parsed, (list, dict)) else []
            elif isinstance(reqs, list):
                r['requirements'] = reqs
            elif isinstance(reqs, dict):
                r['requirements'] = list(reqs.values())
            else:
                r['requirements'] = []
        except Exception:
            r['requirements'] = []
    return rows

@app.route('/jobs')
def jobs():
    return render_template('jobs.html',
        jobs=parse_jobs(db.get_all_jobs()),
        companies=db.get_companies_list())

@app.route('/jobs/new', methods=['POST'])
def job_new():
    skills = [s.strip() for s in request.form.get('requirements', '').split(',') if s.strip()]
    db.create_job(
        request.form.get('company_id') or None, request.form['job_title'],
        request.form.get('job_type'),
        request.form.get('salary_min') or None, request.form.get('salary_max') or None,
        request.form.get('job_url'), request.form.get('date_posted') or None,
        json.dumps(skills))
    flash('Job added!', 'success')
    return redirect(url_for('jobs'))

@app.route('/jobs/<int:id>/edit', methods=['GET', 'POST'])
def job_edit(id):
    if request.method == 'POST':
        skills = [s.strip() for s in request.form.get('requirements', '').split(',') if s.strip()]
        db.update_job(id,
            request.form.get('company_id') or None, request.form['job_title'],
            request.form.get('job_type'),
            request.form.get('salary_min') or None, request.form.get('salary_max') or None,
            request.form.get('job_url'), request.form.get('date_posted') or None,
            json.dumps(skills))
        flash('Job updated!', 'success')
        return redirect(url_for('jobs'))
    edit_job = db.get_job(id)
    if edit_job and edit_job.get('requirements'):
        try:
            reqs = json.loads(edit_job['requirements']) if isinstance(edit_job['requirements'], str) else edit_job['requirements']
            edit_job['requirements_str'] = ', '.join(reqs) if isinstance(reqs, list) else ''
        except Exception:
            edit_job['requirements_str'] = ''
    return render_template('jobs.html',
        jobs=parse_jobs(db.get_all_jobs()),
        companies=db.get_companies_list(),
        edit_job=edit_job)

@app.route('/jobs/<int:id>/delete', methods=['POST'])
def job_delete(id):
    db.delete_job(id)
    flash('Job deleted.', 'info')
    return redirect(url_for('jobs'))

#Applications

@app.route('/applications')
def applications():
    return render_template('applications.html',
        applications=db.get_all_applications(),
        jobs=db.get_jobs_list())

@app.route('/applications/new', methods=['POST'])
def application_new():
    interview_raw = request.form.get('interview_data', '').strip()
    interview_json = None
    if interview_raw:
        try:
            interview_json = json.dumps(json.loads(interview_raw))
        except Exception:
            interview_json = json.dumps({'notes': interview_raw})
    db.create_application(
        request.form.get('job_id') or None, request.form['application_date'],
        request.form.get('status', 'Applied'), request.form.get('resume_version'),
        bool(request.form.get('cover_letter_sent')), interview_json,
        request.form.get('notes'))
    flash('Application added!', 'success')
    return redirect(url_for('applications'))

@app.route('/applications/<int:id>/edit', methods=['GET', 'POST'])
def application_edit(id):
    if request.method == 'POST':
        interview_raw = request.form.get('interview_data', '').strip()
        interview_json = None
        if interview_raw:
            try:
                interview_json = json.dumps(json.loads(interview_raw))
            except Exception:
                interview_json = json.dumps({'notes': interview_raw})
        db.update_application(id,
            request.form.get('job_id') or None, request.form['application_date'],
            request.form.get('status'), request.form.get('resume_version'),
            bool(request.form.get('cover_letter_sent')), interview_json,
            request.form.get('notes'))
        flash('Application updated!', 'success')
        return redirect(url_for('applications'))
    return render_template('applications.html',
        applications=db.get_all_applications(),
        jobs=db.get_jobs_list(),
        edit_application=db.get_application(id))

@app.route('/applications/<int:id>/delete', methods=['POST'])
def application_delete(id):
    db.delete_application(id)
    flash('Application deleted.', 'info')
    return redirect(url_for('applications'))

#Contacts

@app.route('/contacts')
def contacts():
    return render_template('contacts.html',
        contacts=db.get_all_contacts(),
        companies=db.get_companies_list())

@app.route('/contacts/new', methods=['POST'])
def contact_new():
    db.create_contact(
        request.form.get('company_id') or None, request.form['contact_name'],
        request.form.get('title'), request.form.get('email'),
        request.form.get('phone'), request.form.get('linkedin_url'),
        request.form.get('notes'))
    flash('Contact added!', 'success')
    return redirect(url_for('contacts'))

@app.route('/contacts/<int:id>/edit', methods=['GET', 'POST'])
def contact_edit(id):
    if request.method == 'POST':
        db.update_contact(id,
            request.form.get('company_id') or None, request.form['contact_name'],
            request.form.get('title'), request.form.get('email'),
            request.form.get('phone'), request.form.get('linkedin_url'),
            request.form.get('notes'))
        flash('Contact updated!', 'success')
        return redirect(url_for('contacts'))
    return render_template('contacts.html',
        contacts=db.get_all_contacts(),
        companies=db.get_companies_list(),
        edit_contact=db.get_contact(id))

@app.route('/contacts/<int:id>/delete', methods=['POST'])
def contact_delete(id):
    db.delete_contact(id)
    flash('Contact deleted.', 'info')
    return redirect(url_for('contacts'))

#Job Match

@app.route('/job-match', methods=['GET', 'POST'])
def job_match():
    results = []
    user_skills = ''
    if request.method == 'POST':
        user_skills = request.form.get('skills', '')
        skill_list  = [s.strip().lower() for s in user_skills.split(',') if s.strip()]
        if skill_list:
            for job in db.get_jobs_with_requirements():
                reqs_raw = job.get('requirements')
                try:
                    reqs = json.loads(reqs_raw) if isinstance(reqs_raw, str) else (reqs_raw or [])
                except Exception:
                    reqs = []
                if not reqs:
                    continue
                reqs_lower = [r.lower() for r in reqs]
                matched = [s for s in skill_list if s in reqs_lower]
                missing = [r for r in reqs if r.lower() not in skill_list]
                pct     = round(len(matched) / len(reqs) * 100)
                results.append({
                    'job_id': job['job_id'], 'job_title': job['job_title'],
                    'company_name': job['company_name'], 'job_type': job['job_type'],
                    'salary_min': job['salary_min'], 'salary_max': job['salary_max'],
                    'matched': matched, 'missing': missing,
                    'total_reqs': len(reqs), 'match_pct': pct,
                })
            results.sort(key=lambda x: x['match_pct'], reverse=True)
    return render_template('job_match.html', results=results, user_skills=user_skills)

if __name__ == '__main__':
    app.run(debug=True)
