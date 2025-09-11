# Diagramme de la base de données HolbyDoc

```mermaid
erDiagram
    User ||--o{ Lesson : "possède"
    Course ||--o{ Lesson : "contient"
    
    User {
        int id PK
        string fname
        string lname
        string username
        string email
        string image_file
        text bio
        string password
    }
    
    Lesson {
        int id PK
        string title
        datetime date_posted
        text content
        string thumbnail
        string slug
        int user_id FK
        int course_id FK
    }
    
    Course {
        int id PK
        string title
        string description
        string icon
    }
```

**Légende :**
- `PK` = Primary Key (clé primaire)
- `FK` = Foreign Key (clé étrangère)
- Les relations montrent qu'un utilisateur peut avoir plusieurs leçons, et un cours peut contenir plusieurs leçons.
