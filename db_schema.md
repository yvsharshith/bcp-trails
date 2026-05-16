# Database Schema Design for Blue Craft Design Studio

This document outlines the detailed backend database schema required to support the interactive and dynamic elements of the Blue Craft Design Studio website.

---

## 1. User Submissions & Lead Generation

### 1.1 Leads Table (`leads`)
Stores data from the "Book a Free Call" or consultation popup forms.

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | UUID | PRIMARY KEY | Unique identifier for the lead |
| `name` | VARCHAR(100) | NOT NULL | Full name of the prospect |
| `phone_number` | VARCHAR(20) | NOT NULL | Contact number |
| `requirement` | VARCHAR(100) | NOT NULL | e.g., 'Full Home', 'Kitchen', 'Wardrobe' |
| `location` | VARCHAR(255) | | User's project location or city |
| `status` | ENUM | DEFAULT 'NEW' | Allowed: 'NEW', 'CONTACTED', 'CONVERTED', 'LOST' |
| `notes` | TEXT | | Internal notes added by the sales team |
| `created_at` | TIMESTAMP | DEFAULT NOW() | Timestamp of submission |
| `updated_at` | TIMESTAMP | DEFAULT NOW() | Timestamp of last modification |

### 1.2 Contact Messages Table (`contact_messages`)
Stores general inquiries submitted through the "Contact Us" page.

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | UUID | PRIMARY KEY | Unique identifier for the message |
| `name` | VARCHAR(100) | NOT NULL | Sender's name |
| `email` | VARCHAR(255) | NOT NULL | Sender's email address |
| `phone` | VARCHAR(20) | | Sender's phone number |
| `message` | TEXT | NOT NULL | The body of the inquiry |
| `status` | ENUM | DEFAULT 'UNREAD' | Allowed: 'UNREAD', 'READ', 'RESPONDED' |
| `created_at` | TIMESTAMP | DEFAULT NOW() | Timestamp of submission |

### 1.3 Newsletter Subscribers Table (`subscribers`)
Stores email addresses for marketing and newsletter blasts.

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | UUID | PRIMARY KEY | Unique identifier |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL | Subscriber's email address |
| `is_active` | BOOLEAN | DEFAULT TRUE | Indicates if they are currently subscribed |
| `subscribed_at`| TIMESTAMP | DEFAULT NOW() | Timestamp of subscription |

---

## 2. Dynamic Content Management (CMS)

### 2.1 Projects Table (`projects`)
Stores metadata for items in the Portfolio/Projects gallery.

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | UUID | PRIMARY KEY | Unique identifier for the project |
| `title` | VARCHAR(255) | NOT NULL | Project title (e.g., 'Modern Villa') |
| `slug` | VARCHAR(255) | UNIQUE, NOT NULL | URL-friendly identifier |
| `category` | VARCHAR(100) | NOT NULL | e.g., 'Residential', 'Commercial' |
| `description` | TEXT | | Detailed description of the project |
| `client_name` | VARCHAR(150) | | Name of the client (optional) |
| `completion_date`| DATE | | When the project was completed |
| `is_published` | BOOLEAN | DEFAULT FALSE | Whether it is visible on the site |
| `created_at` | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| `updated_at` | TIMESTAMP | DEFAULT NOW() | Last update timestamp |

### 2.2 Project Images Table (`project_images`)
Stores the images associated with a project (One-to-Many relationship with `projects`).

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | UUID | PRIMARY KEY | Unique identifier for the image record |
| `project_id` | UUID | FOREIGN KEY | References `projects.id` ON DELETE CASCADE |
| `image_url` | VARCHAR(500) | NOT NULL | URL of the image stored in cloud (S3, etc.) |
| `alt_text` | VARCHAR(255) | | SEO alt text for the image |
| `is_featured` | BOOLEAN | DEFAULT FALSE | If TRUE, this is the thumbnail of the project |
| `display_order`| INT | DEFAULT 0 | Sorting order in the gallery |

### 2.3 Services Table (`services`)
Stores the different services offered by the studio.

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | UUID | PRIMARY KEY | Unique identifier for the service |
| `name` | VARCHAR(150) | NOT NULL | e.g., 'Modular Kitchens' |
| `slug` | VARCHAR(150) | UNIQUE, NOT NULL | URL-friendly identifier |
| `short_desc` | VARCHAR(500) | NOT NULL | Brief summary for listing pages |
| `long_desc` | TEXT | | Detailed explanation for the service page |
| `icon_url` | VARCHAR(500) | | URL to the service icon or representative image |
| `is_active` | BOOLEAN | DEFAULT TRUE | Whether the service is currently offered |
| `created_at` | TIMESTAMP | DEFAULT NOW() | Creation timestamp |

### 2.4 Blog Posts Table (`blog_posts`)
Stores the articles shown in the "Trending" or Blog section.

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | UUID | PRIMARY KEY | Unique identifier for the article |
| `title` | VARCHAR(255) | NOT NULL | Title of the blog post |
| `slug` | VARCHAR(255) | UNIQUE, NOT NULL | URL-friendly identifier |
| `excerpt` | VARCHAR(500) | | Short summary shown on cards |
| `content` | TEXT | NOT NULL | Full HTML or Markdown content |
| `author_name` | VARCHAR(100) | | Name of the writer |
| `featured_image`| VARCHAR(500) | | URL for the main article image |
| `status` | ENUM | DEFAULT 'DRAFT' | Allowed: 'DRAFT', 'PUBLISHED', 'ARCHIVED' |
| `published_at` | TIMESTAMP | | When the post goes live |
| `created_at` | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| `updated_at` | TIMESTAMP | DEFAULT NOW() | Last update timestamp |

---

## 3. Administration & System

### 3.1 Admin Users Table (`admin_users`)
Stores credentials for the CMS dashboard access.

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | UUID | PRIMARY KEY | Unique identifier for the admin |
| `name` | VARCHAR(100) | NOT NULL | Admin's full name |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL | Login email address |
| `password_hash`| VARCHAR(255) | NOT NULL | Bcrypt hashed password |
| `role` | ENUM | DEFAULT 'EDITOR' | Allowed: 'SUPERADMIN', 'EDITOR' |
| `last_login` | TIMESTAMP | | Track last successful login |
| `created_at` | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| `updated_at` | TIMESTAMP | DEFAULT NOW() | Last update timestamp |
