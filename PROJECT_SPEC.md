# Project Outline: Streamlit Medication Alert System with Supabase Backend

## Current Project Status (as of 29/08/2025)
The project has a functional Streamlit application with user authentication (login/signup). The backend is connected to a Supabase project with the necessary tables created.

Key implemented features include:
- **User Authentication**: Users can sign up and log in.
- **Role-Based Access Control**: A `profiles` table has been added to manage user roles (`pharmacist`, `practice_manager`, `doctor`, `administrator`). A "Manage Users" page is available for administrators to view and assign roles. Access to certain pages is now restricted by role.
- **Surgery Management**: Full CRUD (Create, Read, Update, Delete) functionality for GP surgeries is complete and restricted to administrators.
- **Data Viewing**: A dashboard to view the raw data from the `alerts`, `surgeries`, and `actions` tables is available.

Next steps will focus on implementing the alerts dashboard, action logging, and the web scraper for alerts.

---

## 1. Project Overview
This project involves building a web application using Streamlit as the frontend and Supabase as the backend for data storage and authentication. The core functionality includes:
- Scraping a medication alert website (e.g., a public source like MHRA or FDA alerts) to extract relevant data.
- Storing extracted alerts in a Supabase database.
- Providing a user interface for pharmacists to manage GP surgeries, record the number of patients affected by alerts, and log actions taken.
- Linking actions to specific alerts and surgeries via a relational database structure.
- Ensuring secure access for authenticated users (pharmacists).

The application will automate alert ingestion and provide a dashboard for monitoring and responding to alerts across multiple surgeries.

### Key Features
- **Alert Scraping**: Periodic scraping of a target website to fetch new medication alerts.
- **Database Management**: Store alerts, surgeries, and action logs.
- **User Dashboard**: Authenticated pharmacists can view alerts, manage surgeries, and record responses (e.g., patients affected, actions taken).
- **Reporting**: Basic views or exports of alert impacts across surgeries.
- **Notifications**: Optional email/SMS alerts for new entries (if integrated with Supabase edge functions).

### Assumptions
- The target medication alert website is publicly accessible and scrapable (e.g., using BeautifulSoup or Scrapy). If it's dynamic, Selenium might be needed.
- Supabase will handle PostgreSQL database, authentication, and real-time updates.
- Deployment: Streamlit app on Streamlit Cloud or Heroku; Supabase for backend.
- Scraping will run as a scheduled task (e.g., via GitHub Actions or Supabase cron jobs).
- Compliance: Ensure GDPR/HIPAA considerations for patient data (anonymized counts only).

## 2. Tech Stack
- **Frontend**: Streamlit (for UI, forms, dashboards).
- **Backend/Database**: Supabase (PostgreSQL-based, with auth and real-time subscriptions).
- **Scraping**: Python libraries like Requests, BeautifulSoup, or Scrapy.
- **Authentication**: Supabase Auth (email/password or OAuth).
- **Scheduling**: Supabase Edge Functions or external scheduler (e.g., APScheduler in a separate script).
- **Dependencies**:
  - `streamlit`
  - `supabase-py` (official Supabase Python client)
  - `requests`
  - `beautifulsoup4`
  - `pandas` (for data handling/export)
  - `python-dotenv` (for environment variables)
- **Version Control**: Git/GitHub.

## 3. Architecture
- **High-Level Flow**:
  1. Scraper script runs periodically → Extracts alerts → Inserts/updates into Supabase `alerts` table.
  2. Streamlit app authenticates users via Supabase.
  3. Users view alerts, select surgeries, and log actions in the `actions` table.
  4. Real-time updates: Use Supabase subscriptions to refresh dashboards on new data.
- **Components**:
  - **Scraper Module**: Standalone Python script.
  - **Streamlit App**: Main file (`app.py`) with pages for alerts, surgeries, and actions.
  - **Database**: Relational tables with foreign keys.
  - **Auth**: Role-based (e.g., pharmacists as users).
- **Deployment**:
  - Host Streamlit on Streamlit Sharing or Vercel.
  - Supabase project for DB and auth.
  - Environment variables for Supabase URL/key.

```
.
├── .gitignore
├── data/
├── images/
│   ├── logo.png
│   ├── pillio.png
│   ├── pillio2.png
│   ├── pillio_keep.png
│   └── pillio_logo.png
├── PROJECT_SPEC.md
├── README.md
├── requirements.txt
└── src/
    └── pillio/
        ├── __init__.py
        ├── scrappers/
        │   └── scrapper_one.py
        ├── streamlit_app.py
        └── support/
            ├── support_app.py
            ├── support_supabase.py
            └── support_ui.py
```

## 4. Database Schema
The database will use Supabase's PostgreSQL. Tables are designed to link alerts to actions and surgeries. Supabase handles the `auth.users` table automatically for authentication.

### Table Layout (in Markdown for Clarity)

| Table Name | Description | Columns |
|------------|-------------|---------|
| **alerts** | Stores scraped medication alerts. Primary table for alert data. | - `id`: integer (primary key, auto-generated)<br>- `title`: text<br>- `description`: text<br>- `severity`: character varying<br>- `medication_name`: character varying<br>- `issue_date`: date<br>- `source_url`: text<br>- `created_at`: timestamp without time zone (default now())<br>- `updated_at`: timestamp without time zone (default now())<br>- `alert_text`: text<br>- `source`: text<br>- `pdf_url`: text<br>- `alert_refernce`: text<br>- `ai_summary`: text<br>- `actions_required`: text<br>- `scrape_id`: text |
| **surgeries** | Manages GP surgeries/pharmacies. Used to track responses per location. | - `id`: integer (primary key, auto-generated)<br>- `name`: character varying<br>- `location`: character varying<br>- `contact_email`: character varying<br>- `pharmacist_id`: uuid (foreign key to auth.users)<br>- `created_at`: timestamp without time zone (default now())<br>- `updated_at`: timestamp without time zone (default now()) |
| **actions** | Links actions taken to alerts and surgeries. Separate table for many-to-many relationships. | - `id`: integer (primary key, auto-generated)<br>- `alert_id`: integer (foreign key to alerts.id)<br>- `surgery_id`: integer (foreign key to surgeries.id)<br>- `patients_affected`: integer<br>- `action_taken`: text<br>- `status`: character varying<br>- `recorded_by`: uuid (foreign key to auth.users.id)<br>- `recorded_date`: timestamp without time zone (default now())<br>- `notes`: text<br>- `created_at`: timestamp without time zone (default now())<br>- `updated_at`: timestamp without time zone (default now()) |
| **profiles** | Stores user profile information and roles. Linked to the `auth.users` table. | - `id`: uuid (primary key, auto-generated)<br>- `user_id`: uuid (foreign key to auth.users.id)<br>- `full_name`: text<br>- `role`: user_role (enum: 'pharmacist', 'practice_manager', 'doctor', 'administrator')<br>- `created_at`: timestamp with time zone (default now())<br>- `updated_at`: timestamp with time zone (default now()) |

### Relationships
- **One-to-Many**: One alert can have many actions (via `alert_id` FK in actions).
- **One-to-Many**: One surgery can have many actions (via `surgery_id` FK in actions).
- **Many-to-One**: Actions link back to users (pharmacists) via Supabase `auth.users`.
- **One-to-One**: Each user in `auth.users` has one corresponding entry in the `profiles` table.
- **Indexes**: Add indexes on foreign keys for performance (e.g., on `alert_id`, `surgery_id`).
- **Row-Level Security (RLS)**: Enable in Supabase to restrict access (e.g., pharmacists can only view/edit their assigned surgeries).

### SQL for Table Creation (for Supabase Setup)
You can run this in Supabase SQL editor:
```sql
-- Alerts Table
CREATE TABLE public.alerts (
  id integer NOT NULL DEFAULT nextval('alerts_id_seq'::regclass),
  title text NOT NULL,
  description text,
  severity character varying,
  medication_name character varying,
  issue_date date,
  source_url text,
  created_at timestamp without time zone DEFAULT now(),
  updated_at timestamp without time zone DEFAULT now(),
  alert_text text,
  source text,
  pdf_url text,
  alert_refernce text,
  ai_summary text,
  actions_required text,
  scrape_id text,
  CONSTRAINT alerts_pkey PRIMARY KEY (id)
);

-- Surgeries Table
CREATE TABLE public.surgeries (
  id integer NOT NULL DEFAULT nextval('surgeries_id_seq'::regclass),
  name character varying NOT NULL,
  location character varying,
  contact_email character varying,
  pharmacist_id uuid,
  created_at timestamp without time zone DEFAULT now(),
  updated_at timestamp without time zone DEFAULT now(),
  CONSTRAINT surgeries_pkey PRIMARY KEY (id),
  CONSTRAINT surgeries_pharmacist_id_fkey FOREIGN KEY (pharmacist_id) REFERENCES auth.users(id)
);

-- Actions Table
CREATE TABLE public.actions (
  id integer NOT NULL DEFAULT nextval('actions_id_seq'::regclass),
  alert_id integer,
  surgery_id integer,
  patients_affected integer,
  action_taken text,
  status character varying,
  recorded_by uuid,
  recorded_date timestamp without time zone DEFAULT now(),
  notes text,
  created_at timestamp without time zone DEFAULT now(),
  updated_at timestamp without time zone DEFAULT now(),
  CONSTRAINT actions_pkey PRIMARY KEY (id),
  CONSTRAINT actions_alert_id_fkey FOREIGN KEY (alert_id) REFERENCES public.alerts(id),
  CONSTRAINT actions_surgery_id_fkey FOREIGN KEY (surgery_id) REFERENCES public.surgeries(id),
  CONSTRAINT actions_recorded_by_fkey FOREIGN KEY (recorded_by) REFERENCES auth.users(id)
);

-- Profiles Table and User Role Type
CREATE TYPE public.user_role AS ENUM ('pharmacist', 'practice_manager', 'doctor', 'administrator');

CREATE TABLE public.profiles (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL,
  full_name text,
  role public.user_role NOT NULL DEFAULT 'pharmacist',
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  CONSTRAINT profiles_pkey PRIMARY KEY (id),
  CONSTRAINT profiles_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE
);

-- Trigger to create a profile for new users
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.profiles (user_id, full_name)
  VALUES (new.id, new.raw_user_meta_data->>'full_name');
  RETURN new;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE PROCEDURE public.handle_new_user();
```

## 5. Implementation Steps & Current Status

### 1. Setup Supabase
- [x] Create a Supabase project.
- [x] Enable authentication.
- [x] Create tables as per schema (`alerts`, `surgeries`, `actions`).
- [x] Implemented `profiles` table and `user_role` type for role-based access control.
- [x] Created a trigger (`handle_new_user`) to automatically populate the `profiles` table on user sign-up.
- [ ] **Next Step**: Set up Row-Level Security (RLS) policies for more granular access control.

### 2. Streamlit App Development
- [x] **Authentication**: Login and Sign-Up functionality is implemented.
- [x] **Role-Based Access**: The app now checks user roles to control access to specific pages.
- [x] **User Management**: An admin-only page to view all users and manage their roles has been implemented.
- [x] **Surgery Management**: Full CRUD functionality is implemented and restricted to administrators.
- [x] **Dataframe Viewer**: A tab to view raw database tables is available.
- [ ] **Next Step**: Implement the **Alerts Dashboard** to display alerts in a user-friendly way.
- [ ] **Next Step**: Implement **Actions Logging** functionality.

### 3. Scraper Development
- [ ] **Next Step**: Write a Python script (`scraper.py`).
- [ ] Use Requests/BeautifulSoup to fetch and parse the alert website.
- [ ] Extract fields like title, description, date.
- [ ] Use Supabase client to upsert into `alerts` table.
- [ ] Schedule via cron or GitHub Actions.

### 4. Testing
- [ ] Unit tests for scraper (mock responses).
- [ ] Integration tests for DB interactions.
- [x] UI tests: Manual testing of implemented features has been performed.
- [ ] Edge cases: Duplicate alerts, invalid inputs.

### 5. Deployment and Maintenance
- [ ] Deploy Streamlit to cloud.
- [ ] Set up monitoring for scraper failures.
- [ ] Backup Supabase DB regularly.
- [ ] Scale: If needed, add pagination for large datasets.

## 6. Potential Enhancements
- Integrate AI for alert summarization (e.g., using Grok API).
- Export reports to CSV/PDF.
- Role-based access (admin vs. pharmacist).
- Webhooks for real-time scraping triggers.

## 7. Risks and Mitigations
- **Scraping Legality**: Ensure compliance with website terms; use APIs if available.
- **Data Privacy**: Anonymize patient counts; use Supabase encryption.
- **Rate Limits**: Handle scraping delays to avoid bans.
- **Dependencies**: Pin versions to avoid breaks.

This outline provides a solid foundation. Start with Supabase setup and scraper prototype, then build the Streamlit UI iteratively.
