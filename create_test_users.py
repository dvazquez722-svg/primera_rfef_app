from supabase import create_client

SUPABASE_URL = "https://wanwjfizrjbubhpewwpf.supabase.co"
SUPABASE_SERVICE_ROLE_KEY = "sb_secret_ZsSNSSn1f7KxvWnPIawrJw_2xjQ6Wpv"

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_SERVICE_ROLE_KEY
)

users = [

    # PONFERRADINA

    ("entrenador@ponferradina.com", "Entrenador Ponferradina", "Entrenador", 2),
    ("analista@ponferradina.com", "Analista Ponferradina", "Analista", 2),
    ("directordeportivo@ponferradina.com", "Director Deportivo Ponferradina", "Director Deportivo", 2),
    ("ojeador@ponferradina.com", "Ojeador Ponferradina", "Ojeador", 2),
    ("preparador@ponferradina.com", "Preparador Físico Ponferradina", "Preparador Físico", 2),

    # CASTILLA

    ("entrenador@castilla.com", "Entrenador Castilla", "Entrenador", 30),
    ("analista@castilla.com", "Analista Castilla", "Analista", 30),
    ("directordeportivo@castilla.com", "Director Deportivo Castilla", "Director Deportivo", 30),
    ("ojeador@castilla.com", "Ojeador Castilla", "Ojeador", 30),
    ("preparador@castilla.com", "Preparador Físico Castilla", "Preparador Físico", 30),

]

PASSWORD = "Test123456!"

for email, full_name, role, team_id in users:

    try:

        auth_user = supabase.auth.admin.create_user({

            "email": email,
            "password": PASSWORD,
            "email_confirm": True

        })

        user_id = auth_user.user.id

        supabase.table(
            "users_profile"
        ).insert({

            "id": user_id,
            "full_name": full_name,
            "role": role,
            "team_id": team_id

        }).execute()

        print(f"✅ {email}")

    except Exception as e:

        print(f"❌ {email}")
        print(e)